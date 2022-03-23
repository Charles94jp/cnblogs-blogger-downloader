<h1 align="center">
  <a href="#">
  <img src="./img/logo.png" width ="530px">
  </a>
  <br>
</h1>

<p align="center">
<a target="_blank" href="https://www.gnu.org/licenses/gpl-3.0.zh-cn.html"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg"></a>  
<a href="#python3"><img src="https://img.shields.io/badge/python-v3.8-blue"></a>
<a href="https://www.python-httpx.org/"><img src="https://img.shields.io/badge/httpx-v0.22.0-brightgreen"></a>
</p>
本程序意在让各位博客园作者拿回属于自己的文章。程序会以博客园的随笔分类来建立文件夹并下载相应的文章，文章格式为md格式



# Usage

## Configuration

运行前需要进行配置：

1. 打开浏览器登录博客园，登录时勾选"记住我"

2. 登录后浏览器按F12，找到Cookie，拷贝`.Cnblogs.AspNetCore.Cookies`的值到`main.py`的`COOKIE`中

3. `main.py`中`dl.CnblogsDownloader`的第二个参数为下载路径

可选的配置：

**将随笔中引用的图片一并离线到随笔的文件夹**，需要更改`main.py`

```python
# 将此行
downloader = dl.CnblogsDownloader(COOKIE, "D:\cnblogs")
# 改为
downloader = dl.CnblogsDownloader(COOKIE, "D:\cnblogs", download_img=True)
```

md中的链接会自动替换



## Dependencies

```
pip install httpx
```



## Start

配置好程序并安装好httpx依赖后，命令行运行：

```python
python main.py
```

会看到打印的输出:

![example](./img/example.png)



## Features

下载的文件名为随笔标题，分类和标题中的特殊字符`\/:*?"<>|`会被空格代替，文件编码为UTF-8

程序会区分你的随笔是否是公开的，是否是草稿状态，并在文件名后追加`[非公开]`或`[草稿]`

程序只能在Windows下运行，未做其他系统适配

如果你在博客园中删除了一篇文章，程序不会删除相应的本地文章

`.CnblogsDownloaderFlag.json`中保存着上次运行程序的时间，如果博客园中的文章未更新，那么不会反复下载

一旦程序决定要下载某篇随笔，那么它会覆盖此随笔及其引用的图片



# For Developer

博客园公开的api文档：https://api.cnblogs.com/help

但显然不够用，而且要申请api权限，于是自己根据网络通信总结了几个重要的api的文档：[cnblogs-apiDoc](/lib/cnblogs-apiDoc.md)

本项目的开源协议为：[GPL-3.0 License](/LICENSE)