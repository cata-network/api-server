#!/usr/bin/env python3
#coding=utf-8
#########################################################################
# Author: @maris
# Created Time: May 18  2017 18:55:41 PM CST
# File Name:spider.py
# Description:把图片同步到ipfs
#########################################################################
import sys
import re
import json
import time
import io
import requests
import ipfshttpclient
import base64


#ipfs版本<=0.6
IPFS_GATE = "/ip4/47.242.44.241/tcp/5001/http"
LOCAL_PATH = "data/img/"

"""
功能:上传本地文件到ipfs
输入:local_file, 本地文件名，需
返回:ipfs的cid
"""
def upload_file(local_file):
    client = ipfshttpclient.connect(IPFS_GATE)  # Connects to: /dns/localhost/tcp/5001/http
    res = client.add(local_file)
    cid = res["Hash"]
    return cid

"""
功能:上传url文件到ipfs
输入:url, 文件url
返回:ipfs的cid
"""
def upload_url(url):
    #step 1,下载文件
    #网络流将以text 的方式传输到 COS
    header = {}
    header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    res = requests.get(url, headers=header)

    local_file = LOCAL_PATH + url.split("/")[-1] #文件名，最后一个字符串
    #data_file = open(local_file, "wb")
    #data_file.write(res.content) #写入文件
    #data_file.close()
    #res.close()

    #step 2,写入ipfs
    cid = upload_file((io.BytesIO(res.content)))

    return cid


"""
功能：上传base64字符串，str
输入：base64_text, base64后的字符串
返回：ipfs的cid
"""
def upload_base64(base64_str):
    #step 1, base64字符串转bytes,注意可能的包含 data:image/gif;base64,
    # item_list = base64_text.split(',')
    # if len(item_list) > 1: #如果包含需要去掉
    #     base64_text = item_list[1]

    #step 2，上传到ipfs
    #解码
    image_data = base64.b64decode(base64_str.encode())
    cid = upload_file((io.BytesIO(image_data)))
    return cid


if __name__ == "__main__":
    local_file = "color1.jpg"
    # cid = upload_file(local_file)

    # url = "http://chia1-1300721637.cos.ap-shanghai.myqcloud.com/img/user/170cd338a921c6d66d2882cd6f2b715e.jpg"
    # cid = upload_url(url)
    # print(cid)

    #编码
    f = open(local_file, "rb")
    base64_data = base64.b64encode(f.read()) #bytes
    #print(base64_data)
    #print(base64_data.decode())

    cid = upload_base64(base64_data.decode()) #输入str
    print(cid)
    #http://47.242.44.241:8080/ipfs/QmSvf8vZ8cUCTGGqi3yQ51pmFMP4Kyv19g2zK3wvzE6ynm

