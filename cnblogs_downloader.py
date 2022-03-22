import os
import re

import httpx

import lib.cnblogs_api as api


class CnblogsDownloader:
    __http_headers = ""
    __category = {}
    __workdir = ""
    __download_img = False

    def __init__(self, cnblogs_cookie, workdir, download_img=False):
        self.__http_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/99.0.4844.74 Safari/537.36",
            "Referer": "https://i.cnblogs.com/",
            "Cookie": rf".Cnblogs.AspNetCore.Cookies={cnblogs_cookie}"}
        self.__category = api.get_category_list(self.__http_headers)
        self.__workdir = workdir
        self.__download_img = download_img

    def download_to_subdir(self):
        current_path = os.getcwd()
        os.chdir(self.__workdir)
        self.__category.append({"categoryId": 0, "title": "未分类"})
        for category in self.__category:
            dirname = category["title"]
            dirname = re.sub(rf'(\\|/|\?|\||"|:|\*|<|>)', ' ', dirname)
            if not os.path.isdir(dirname):
                os.mkdir(dirname)
            os.chdir(rf"{self.__workdir}\{dirname}")

            essays = api.get_posts_list(self.__http_headers, category_id=str(category["categoryId"]))
            for essay_pre in essays["postList"]:
                essay = api.get_post_by_id(self.__http_headers, str(essay_pre["id"]))
                filename = essay["blogPost"]["title"]
                # 替换特殊字符，Windows文件名不允许出现特殊字符： \/:*?"<>|
                filename = re.sub(rf'(\\|/|\?|\||"|:|\*|<|>)', ' ', filename)
                filename = rf'{filename}{"[非公开]" if not essay["blogPost"]["isPublished"] else ""}' \
                           rf'{"[草稿]" if essay["blogPost"]["isDraft"] else ""}.md'

                essay_content = essay["blogPost"]["postBody"]
                if self.__download_img:
                    essay_content = CnblogsDownloader.__download_replace_img(filename, essay_content)

                with open(filename, "w", encoding='utf-8') as f:
                    f.write(essay_content)
                print(rf'已下载文章：{dirname}\{filename}')

            os.chdir(self.__workdir)
        os.chdir(current_path)

    @staticmethod
    def __download_replace_img(essay_title, essay_content):
        img_url = []
        # 替换所有![]() <img src="">的图片地址为![](./xx)，同时把被替换的图片url放在img_url中
        essay_content = re.sub(r'!\[[^\]]*?\]\(([^\)]*/([^\)]*?))\)|<img[^>]*?src="([^"]*/([^"]*?))"[^>]*?>',
                               lambda m: img_url.append(m.group(1) if m.group(1) else m.group(3)) or
                                         rf'![](./{m.group(2) if m.group(2) else m.group(4)})',
                               essay_content)
        img_url = set(img_url)
        http_headers = {"Referer": "https://i.cnblogs.com/"}
        for url in img_url:
            # 不再校验文件名的合法性
            try:
                r = httpx.get(url, headers=http_headers, timeout=api.TIMEOUT)
                img_name = url.split('/')[-1]
                with open(img_name, 'wb') as f:
                    f.write(r.content)
                print(rf'已下载图片：{img_name}')
            except Exception as e:
                print(f'error: 为《{essay_title}》下载图片失败，链接：{url}')
        return essay_content
