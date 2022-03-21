import cnblogs_downloader as dl

COOKIE = ""


def main():
    # downloader = dl.CnblogsDownloader(COOKIE, "D:\cnblogs", download_img=True)
    downloader = dl.CnblogsDownloader(COOKIE, "D:\cnblogs")
    downloader.download_to_subdir()


if __name__ == '__main__':
    main()
