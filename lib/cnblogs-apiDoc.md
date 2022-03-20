博客园API文档，非官方文档，从博客园后台的网络通信过程中总结



## 目录


1. [获取用户随笔分类列表](#1-获取用户随笔分类列表)

2. [获取用户随笔列表](#2-获取用户随笔列表)

3. [获取随笔内容](#3-获取随笔内容)

<br></br>

## 1 获取用户随笔分类列表

**请求方式：**GET

**请求地址：**https://i.cnblogs.com/api/category/blog/1/edit

**参数列表：**

| 参数名 | 类型 | 必须 | 描述 | 示例 |
| ------ | ---- | ---- | ---- | ---- |
| /      |      |      |      |      |

**详细说明：**根据用户Cookie获取用户的随笔分类的列表

**请求示例：**

```
https://i.cnblogs.com/api/category/blog/1/edit
```

**返回示例：**

```json
[
  {
    "categoryId": 1895777,
    "title": "Bug Solution",
    "visible": true,
    "description": "Windows、Linux使用过程中的bug解决办法",
    "updateTime": "2022-01-08T21:45:04.607",
    "count": 3,
    "order": null
  }
]
```

<br></br>

## 2 获取用户随笔列表

**请求方式：**GET

**请求地址：**https://i.cnblogs.com/api/posts/list

**参数列表：**

| 参数名  | 类型 | 必须 | 描述                                   | 示例    |
| :------ | ---- | ---- | -------------------------------------- | ------- |
| p       | int  | 是   | 页数，第几页                           | 1       |
| cid     | int  | 否   | 分类id，获取分类下的文章。空为所有文章 | 1895777 |
| tid     |      | 否   |                                        |         |
| t       | int  | 是   | 文章类型：随笔为1，文章为2，日记为128  | 1       |
| cfg     |      | 否   |                                        |         |
| search  |      | 否   |                                        |         |
| orderBy |      | 否   |                                        |         |
| scid    |      | 否   |                                        |         |

**详细说明**：分页获取用户的随笔列表，每页只能获取10个

**请求示例：**

```
https://i.cnblogs.com/api/posts/list?p=1&cid=&tid=&t=1&cfg=0&search=&orderBy=&scid=
```

**返回示例：**

```json
{
  "postList": [
    {
      "id": 16013455,
      "title": "Windows oh my zsh终极解决方案，还得是WSL",
      "url": "//www.cnblogs.com/yunmuq/p/16013455.html",
      "isPublished": false,
      "isDraft": true,
      "feedBackCount": 0,
      "webCount": 0,
      "aggCount": 0,
      "viewCount": 0,
      "datePublished": "2022-03-16T16:51:00",
      "entryName": null,
      "postType": 1,
      "postConfig": 16888,
      "dateUpdated": "2022-03-17T15:40:00",
      "accessPermission": 0,
      "isInSiteHome": false,
      "isInSiteCandidate": false,
      "isMarkdown": true
    }
  ],
  "postsCount": 46,
  "pageIndex": 1,
  "pageSize": 10,
  "categoryName": ""
}
```

<br></br>

## 3 获取随笔内容

**请求方式：**GET

**请求地址：**[https://i.cnblogs.com/api/posts/{id}](https://i.cnblogs.com/api/posts/{id})

**参数列表：**

| 参数名 | 类型 | 必须 | 描述   | 示例     |
| :----- | ---- | ---- | ------ | -------- |
| id     | int  | 是   | 随笔id | 15980094 |

**详细说明**：分页获取用户的随笔列表，每页只能获取10个

**请求示例：**

```
https://i.cnblogs.com/api/posts/15980094
```

**返回示例：**

```json
{
  "blogPost": {
    "id": 15980094,
    "postType": 1,
    "accessPermission": 0,
    "title": "【教程】电脑怎么禁用主板蓝牙，使用蓝牙适配器？",
    "url": "//www.cnblogs.com/yunmuq/p/15980094.html",
    "postBody": "<br></br>\n有时主板蓝牙出毛病，比如蓝牙耳机播放卡顿，蓝牙版本过低等，购买了新的USB蓝牙适配器，怎么正确使用呢？...",
    "categoryIds": [
      1899874
    ],
    "inSiteCandidate": false,
    "inSiteHome": false,
    "siteCategoryId": null,
    "blogTeamIds": [],
    "isPublished": true,
    "displayOnHomePage": true,
    "isAllowComments": true,
    "includeInMainSyndication": true,
    "isPinned": false,
    "isOnlyForRegisterUser": false,
    "isUpdateDateAdded": false,
    "entryName": null,
    "description": "",
    "featuredImage": null,
    "tags": [],
    "password": null,
    "datePublished": "2022-03-08T13:52:00",
    "isMarkdown": true,
    "isDraft": false,
    "autoDesc": "有时主板蓝牙出毛病，比如蓝牙耳机播放卡顿，蓝牙版本过低等，购买了新的USB蓝牙适配器，怎么",
    "changePostType": false,
    "blogId": 650454,
    "author": "云牧青",
    "removeScript": false,
    "clientInfo": null,
    "changeCreatedTime": false,
    "canChangeCreatedTime": false,
    "isContributeToImpressiveBugActivity": false
  },
  "myConfig": {
    "canInSiteCandidate": false,
    "noSiteCandidateMsg": "发布时间超过10小时的随笔不能投稿到首页候选区",
    "canInSiteHome": false,
    "noSiteHomeMsg": "发布时间超过1小时的随笔不能投稿到网站首页",
    "myTeamCollection": [],
    "editor": {
      "id": 5,
      "host": "//common.cnblogs.com",
      "cdnRefreshId": null
    }
  }
}
```

