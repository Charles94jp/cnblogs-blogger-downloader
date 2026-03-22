import argparse
import os
import shutil

import cnblogs_downloader as dl
from configparser import ConfigParser


def main():
    """
    读取配置文件、初始化程序并开始下载

    """
    description = """博客园博客下载器
    
使用前先配置config.ini文件

Features:
- 默认为增量下载模式，.CnblogsDownloaderFlag.json中保存着上次运行程序的时间，如果博客园中的文章未更新，那么不会反复下载
- 下载的文件名为随笔标题，分类和标题中的特殊字符\/:*?"<>|会被空格代替，文件编码为UTF-8
- 程序会区分你的随笔是否是公开的，是否是草稿状态，并在文件名后追加[非公开]或[草稿]
- 如果你在博客园中删除了一篇文章，程序不会删除相应的本地文章，使用-c变为全量下载模式可以解决
- 配置download_images后，每次下载随笔，都会覆盖此随笔及其引用的图片，某个图片不被引用后，本地并不会删除，使用-c变为全量下载模式可以解决
- 随笔中代码块中的图片也会被下载，只要它的链接是有效的"""
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--clean-before-download', action='store_true',
                        help='由增量下载变为全量下载，先清空工作目录，再下载')
    args = parser.parse_args()

    config = ConfigParser()
    config.read("config.ini", encoding="utf-8")
    workdir = config.get("main", "work_directory")

    # 如果指定了清空参数
    if os.path.exists(workdir) and args.clean_before_download:
        if os.path.exists(workdir):
            shutil.rmtree(workdir)
            print(f"已清空工作目录: {workdir}")
        os.makedirs(workdir)
        print(f"已创建工作目录: {workdir}")

    downloader = dl.CnblogsDownloader(config.get("main", ".Cnblogs.AspNetCore.Cookies"),
                                      workdir,
                                      download_img=config.get("main", "download_images"))
    downloader.download_to_subdir()


if __name__ == '__main__':
    main()
