<h1 align="center">
   Cnblogs Blogger Downloader
  <br>
  <br>
</h1>

本程序意在让各位博客园上写作的作者拿回属于自己的文章。程序会以博客园的随笔分类来建立文件夹并下载响应的文章，文章格式为md格式

使用时先浏览器登录博客园，登录时勾选"记住我"

登录后浏览器按F12，找到Cookie，拷贝`.Cnblogs.AspNetCore.Cookies`的值到`main.py`的`COOKIE`中，运行`main.py`即可

下载的文件名为随笔标题，分类和标题中的特殊字符`\/:*?"<>|`会被空格代替，文件编码为UTF-8

程序会区分你的随笔是否是公开的，是否是草稿状态，并在文件名后追加`[非公开]`或`[草稿]`

程序只能在Windows下运行，未做其他系统适配

图片暂不支持下载

博客园公开的api文档：https://api.cnblogs.com/help

但显然不够用，而且要申请api权限，于是自己根据网络通信总结了几个重要的api的文档：[cnblogs-apiDoc](/lib/cnblogs-apiDoc.md)

本项目的开源协议为：[GPL-3.0 License](/LICENSE)