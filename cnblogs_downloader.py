import os
import re

import lib.cnblogs_api as api


class CnblogsDownloader:
    _http_header = ""
    _category = {}
    _workdir = ""

    def __init__(self, cnblogs_cookie, workdir):
        self._http_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/99.0.4844.74 Safari/537.36",
            "Cookie": rf".Cnblogs.AspNetCore.Cookies={cnblogs_cookie}"}
        self._category = api.get_category_list(self._http_header)
        self._workdir = workdir

    def download_to_subdir(self):
        current_path = os.getcwd()
        os.chdir(self._workdir)
        temp_category = {
            "categoryId": 0,
            "title": "未分类"}
        self._category.append(temp_category)
        for category in self._category:
            dirname = category["title"]
            dirname = re.sub(rf'(\\|/|\?|\||"|:|\*|<|>)', ' ', dirname)
            if not os.path.isdir(dirname):
                os.mkdir(dirname)
            os.chdir(rf"{self._workdir}\{dirname}")

            essays = api.get_posts_list(self._http_header, category_id=str(category["categoryId"]))
            for essay_pre in essays["postList"]:
                essay = api.get_post_by_id(self._http_header, str(essay_pre["id"]))
                filename = essay["blogPost"]["title"]
                # 替换特殊字符，Windows文件名不允许出现特殊字符： \/:*?"<>|
                filename = re.sub(rf'(\\|/|\?|\||"|:|\*|<|>)', ' ', filename)
                filename = rf'{filename}{"[非公开]" if not essay["blogPost"]["isPublished"] else ""}' \
                           rf'{"[草稿]" if essay["blogPost"]["isDraft"] else ""}.md'
                with open(filename, "w", encoding='utf-8') as f:
                    f.write(essay["blogPost"]["postBody"])
                print(rf'已下载：{dirname}\{filename}')

            os.chdir(self._workdir)
        os.chdir(current_path)
