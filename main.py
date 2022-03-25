import cnblogs_downloader as dl
from configparser import ConfigParser


def main():
    """
    读取配置文件、初始化程序并开始下载

    """
    config = ConfigParser()
    config.read("config.ini", encoding="utf-8")
    downloader = dl.CnblogsDownloader(config.get("main", ".Cnblogs.AspNetCore.Cookies"),
                                      config.get("main", "work_directory"),
                                      download_img=config.get("main", "download_images"))
    downloader.download_to_subdir()


if __name__ == '__main__':
    main()
