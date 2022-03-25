# 文档注释采用sphinx的reStructuredText语法，可以使用sphinx构建api文档

from math import ceil
import httpx

TIMEOUT = 5
"""HTTP连接超时时间"""


def get_category_list(http_header):
    """
    获取用户的博客分类

    :param dict http_header: 其中应当包含Cookie
    :rtype: dict
    :return: 详情参见接口文档: `/lib/cnblogs-apiDoc </lib/cnblogs-apiDoc.html>`_
    """
    r = httpx.get("https://i.cnblogs.com/api/category/blog/1/edit", headers=http_header, timeout=TIMEOUT)
    return r.json()


def get_posts_list(http_header, category_id=""):
    """
    分页获取随笔列表，并把他们拼接成一页返回

    :param dict http_header: 其中应当包含Cookie
    :param int category_id: get_category_list结果中分类对应的id，不设置时查询所有随笔
    :rtype: dict
    :return: 详情参见接口文档: `/lib/cnblogs-apiDoc </lib/cnblogs-apiDoc.html>`_
    """
    r = httpx.get(rf"https://i.cnblogs.com/api/posts/list?p=1&cid={category_id}&tid=&t=1&cfg=0&search=&orderBy=&scid=",
                  headers=http_header, timeout=TIMEOUT)
    result = r.json()
    pmax = ceil(result["postsCount"] / 10)
    if pmax > 1:
        for page in range(2, pmax + 1):
            r = httpx.get(
                rf"https://i.cnblogs.com/api/posts/list?p={page}&cid={category_id}&tid=&t=1&cfg=0&search=&orderBy=&scid=",
                headers=http_header, timeout=TIMEOUT)
            r = r.json()
            result["postList"] = result["postList"] + r["postList"]
    result["pageSize"] = len(result["postList"])
    if not result["pageSize"] == result["postsCount"]:
        raise Exception("合并分页出错")
    return result


def get_post_by_id(http_header, id):
    """
    获取随笔详情

    :param dict http_header: 其中应当包含Cookie
    :param int id: 从`get_posts_list`结果中随笔对应的id
    :rtype: dict
    :return: 详情参见接口文档: `/lib/cnblogs-apiDoc </lib/cnblogs-apiDoc.html>`_
    """
    r = httpx.get(rf"https://i.cnblogs.com/api/posts/{id}", headers=http_header, timeout=TIMEOUT)
    return r.json()
