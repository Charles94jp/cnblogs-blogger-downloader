import json
import os
import re
from datetime import datetime, timedelta

import httpx

import lib.cnblogs_api as api


class CnblogsDownloader:
    __http_headers = ""
    __category = {}
    __workdir = ""
    __download_img = False
    __total_essay = 0
    __updated_essay = 0
    __is_first_run = True
    __last_update = None
    __FLAG_FILE_NAME = ".CnblogsDownloaderFlag.json"

    def __init__(self, cnblogs_cookie, workdir, download_img=False):
        self.__http_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/99.0.4844.74 Safari/537.36",
            "Referer": "https://i.cnblogs.com/",
            "Cookie": rf".Cnblogs.AspNetCore.Cookies={cnblogs_cookie}"}
        self.__category = api.get_category_list(self.__http_headers)
        self.__workdir = workdir
        self.__download_img = download_img
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
        for category in self.__category:
            dirname = category["title"]
            dirname = re.sub(rf'(\\|/|\?|\||"|:|\*|<|>)', " ", dirname)
            if not os.path.isdir(dirname):
                os.mkdir(dirname)
            os.chdir(rf"{self.__workdir}\{dirname}")

            essays = api.get_posts_list(self.__http_headers, category_id=str(category["categoryId"]))
            self.__total_essay = self.__total_essay + essays["postsCount"]
            for essay_pre in essays["postList"]:

                filename = essay_pre["title"]
                # 替换特殊字符，Windows文件名不允许出现特殊字符： \/:*?"<>|
                filename = re.sub(rf'(\\|/|\?|\||"|:|\*|<|>)', " ", filename)
                filename = rf'{filename}{"[非公开]" if not essay_pre["isPublished"] else ""}' \
                           rf'{"[草稿]" if essay_pre["isDraft"] else ""}.md'

                essay_date_updated = datetime.strptime(essay_pre["dateUpdated"], "%Y-%m-%dT%H:%M:%S")
                if (not self.__is_first_run) and os.path.isfile(filename) and \
                        (self.__last_update - essay_date_updated).total_seconds() > 0:
                    print(rf"已是最新：{dirname}\{filename}")
                    continue
                essay = api.get_post_by_id(self.__http_headers, str(essay_pre["id"]))

                essay_content = essay["blogPost"]["postBody"]
                if self.__download_img:
                    essay_content = CnblogsDownloader.__download_replace_img(filename, essay_content)

                with open(filename, "w", encoding="utf-8") as f:
                    f.write(essay_content)
                self.__updated_essay = self.__updated_essay + 1
                print(rf"已下载随笔：{dirname}\{filename}")

            os.chdir(self.__workdir)
        print(rf"总共{self.__total_essay}篇随笔，更新了{self.__updated_essay}篇")
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        with open(rf"{self.__workdir}\{self.__FLAG_FILE_NAME}", "w", encoding="utf-8") as f:
            f.write(rf'{{"last_update": "{now}"}}')
        os.chdir(current_path)

    @staticmethod
    def __download_replace_img(essay_title, essay_content):
        img_url = []

        # bug：写成lambda表达式用or连接两句时，只会执行最后一个表达式，猜测是因为前面的语句没有返回值
        def replace(m):
            img_url.append(m.group(2) if m.group(2) else m.group(6))
            return rf"{m.group(1)}{m.group(3)}{m.group(4)}" if m.group(3) else rf"{m.group(5)}{m.group(7)}{m.group(8)}"

        # 正则中使用(?:)非捕获元无效
        essay_content = re.sub(r'(!\[[^\]]*?\]\()([^\)]*/([^\)]*?))(\))|(<img[^>]*?src=")([^"]*/([^"]*?))("[^>]*?>)',
                               replace, essay_content)
        img_url = set(img_url)
        http_headers = {"Referer": "https://i.cnblogs.com/"}
        for url in img_url:
            # 不再校验文件名的合法性
            img_name = url.split("/")[-1]
            if os.path.isfile(img_name):
                print(rf"图片已存在：{img_name}")
                continue
            try:
                r = httpx.get(url, headers=http_headers, timeout=api.TIMEOUT)
                with open(img_name, "wb") as f:
                    f.write(r.content)
                print(rf"已下载图片：{img_name}")
            except Exception as e:
                print(f"error: 为《{essay_title}》下载图片失败，链接：{url}")
        return essay_content
