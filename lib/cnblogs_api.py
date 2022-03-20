from math import ceil
import httpx

TIMEOUT = 10


def get_category_list(http_header):
    r = httpx.get("https://i.cnblogs.com/api/category/blog/1/edit", headers=http_header, timeout=TIMEOUT)
    return r.json()


def get_posts_list(http_header, category_id=""):
    """
    分页获取随笔列表，并把他们拼接成一页
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
    r = httpx.get(rf"https://i.cnblogs.com/api/posts/{id}", headers=http_header, timeout=TIMEOUT)
    return r.json()
