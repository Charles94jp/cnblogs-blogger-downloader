import json
import os
import re
import threading
from datetime import datetime

import httpx

import lib.cnblogs_api as api


class CnblogsDownloader:
    __FLAG_FILE_NAME = ".CnblogsDownloaderFlag.json"

    """
    called by :py:func:`CnblogsDownloader.__download_replace_img`
    正则中使用(?:)非捕获元无效
    """
    __IMG_PATTERN = re.compile(r'(!\[[^\]]*?\]\()([^\)]*/([^\)]*?))(\))|(<img[^>]*?src=")([^"]*/([^"]*?))("[^>]*?>)')

    def __init__(self, cnblogs_cookie, workdir, download_img=False):
        self.__total_essay = 0
        self.__updated_essay = 0
        self.__is_first_run = True
        self.__last_update = None
        self.__workdir = workdir
        self.__download_img = download_img
        self.__lock = threading.Lock()
        self.__http_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/99.0.4844.74 Safari/537.36",
            "Referer": "https://i.cnblogs.com/",
            "Cookie": rf".Cnblogs.AspNetCore.Cookies={cnblogs_cookie}"}
        self.__category = api.get_category_list(self.__http_headers)

        flag_path = rf"{workdir}\{self.__FLAG_FILE_NAME}"
        if os.path.isfile(flag_path):
            self.__is_first_run = False
            flag = None
            with open(flag_path, "r", encoding="utf-8") as f:
                flag = json.load(f)
                pass
            # download_to_subdir最后还有写入操作
            last_update = flag["last_update"]
            self.__last_update = datetime.strptime(last_update, "%Y-%m-%dT%H:%M:%S")

    def download_to_subdir(self):
        current_path = os.getcwd()
        os.chdir(self.__workdir)
        self.__category.append({"categoryId": 0, "title": "未分类"})
        download_threads = []
        for category in self.__category:
            # (category,) 一个元素的元组 (category)是列表转元组
            download_thread = threading.Thread(target=self.__category_download_thread, args=(category,))
            download_thread.start()
            download_threads.append(download_thread)
        for download_thread in download_threads:
            download_thread.join()
        print(rf"总共{self.__total_essay}篇随笔，更新了{self.__updated_essay}篇")
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        with open(rf"{self.__workdir}\{self.__FLAG_FILE_NAME}", "w", encoding="utf-8") as f:
            f.write(rf'{{"last_update": "{now}"}}')
        os.chdir(current_path)

    def __category_download_thread(self, category):
        """
        每个分类一个线程去下载随笔内容，需要的话，还有下载图片
        多线程共用一个工作目录，任何一个线程os.chdir都会改变整个程序的工作目录
        """
        dirname = category["title"]
        dirname = re.sub(rf'(\\|/|\?|\||"|:|\*|<|>)', " ", dirname)
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        write_absolute_path = rf"{self.__workdir}\{dirname}"

        essays = api.get_posts_list(self.__http_headers, category_id=str(category["categoryId"]))
        self.__lock.acquire()
        self.__total_essay = self.__total_essay + essays["postsCount"]
        self.__lock.release()
        for essay_pre in essays["postList"]:
            filename = essay_pre["title"]
            # 替换特殊字符，Windows文件名不允许出现特殊字符： \/:*?"<>|
            filename = re.sub(rf'(\\|/|\?|\||"|:|\*|<|>)', " ", filename)
            filename = rf'{filename}{"[非公开]" if not essay_pre["isPublished"] else ""}' \
                       rf'{"[草稿]" if essay_pre["isDraft"] else ""}.md'

            essay_date_updated = datetime.strptime(essay_pre["dateUpdated"], "%Y-%m-%dT%H:%M:%S")
            if (not self.__is_first_run) and os.path.isfile(rf"{write_absolute_path}\{filename}") and \
                    (self.__last_update - essay_date_updated).total_seconds() > 0:
                self.__lock.acquire()
                print(rf"已是最新：{dirname}\{filename}")
                self.__lock.release()
                continue
            essay = api.get_post_by_id(self.__http_headers, str(essay_pre["id"]))

            essay_content = essay["blogPost"]["postBody"]
            if self.__download_img:
                essay_content = CnblogsDownloader.__download_replace_img(filename, essay_content, write_absolute_path)

            with open(rf"{write_absolute_path}\{filename}", "w", encoding="utf-8") as f:
                f.write(essay_content)
            self.__lock.acquire()
            self.__updated_essay = self.__updated_essay + 1
            print(rf"已下载随笔：{dirname}\{filename}")
            self.__lock.release()

    @staticmethod
    def __download_replace_img(essay_title, essay_content, workdir):
        """
        替换文章内容中的图片，包括![]()和<img src="xx" style="height:450px">的格式
        img标签中其他属性也会被保留，比如替换后为<img src="./img/xx" style="height:450px">
        最后根据图片链接下载图片

        :return: 完成替换后的文章内容
        """
        img_url = []

        # bug：写成lambda表达式用or连接两句时，只会执行最后一个表达式，猜测是因为前面的语句没有返回值
        def replace(m):
            img_url.append(m.group(2) if m.group(2) else m.group(6))
            return rf"{m.group(1)}./img/{m.group(3)}{m.group(4)}" if m.group(
                3) else rf"{m.group(5)}./img/{m.group(7)}{m.group(8)}"

        essay_content = CnblogsDownloader.__IMG_PATTERN.sub(replace, essay_content)
        http_headers = {"Referer": "https://i.cnblogs.com/"}
        if len(img_url) > 0 and (not os.path.isdir(rf"{workdir}\img")):
            os.mkdir(rf"{workdir}\img")
        for url in img_url:
            # 不再校验文件名的合法性
            img_name = url.split("/")[-1]
            img_path = rf"{workdir}/img/{img_name}"
            if os.path.isfile(img_path):
                print(rf"图片已存在：{img_name}")
                continue
            try:
                r = httpx.get(url, headers=http_headers, timeout=api.TIMEOUT)
                with open(img_path, "wb") as f:
                    f.write(r.content)
                print(rf"已为《{essay_title}》下载图片：{img_name}")
            except Exception as e:
                print(f"error: 为《{essay_title}》下载图片失败，链接：{url}")
        return essay_content
