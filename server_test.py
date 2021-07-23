#!/usr/bin/env python3
#coding=utf-8
#########################################################################
# Author: @maris
# Created Time: May 18  2017 18:55:41 PM CST
# File Name:spider.py
# Description:把元数据同步到ipfs
#########################################################################
import sys
import re
import json
import time
import io
import requests
import urllib.parse
import base64

END_POINT = "http://api.cata.show/"


#元数据插入测试
def get_metadata_test():
    db_link = "/ipfs/QmYUQee1mTUGjEMtk2ZBn8LdE1YVWueF3q5ec7WMgXsGfc#json"
    nft_id = 1

    url = END_POINT + "get_metadata?db_link={}&nft_id={}".format(
        urllib.parse.quote(db_link),
        nft_id
    )
    #print(url)
    res = requests.get(url)

    return res.text


#元数据插入测试
def insert_metadata_test():
    url = END_POINT + "insert_metadata"
    header = {"Content-Type": "application/json"}
    data = {
        "db":"ipfs://QmNr3U2TAPnP2wA4n2fP161Lqzp5JusW1Mo8iT9WaqFTj8",
        "metatdata":[
            {"title":"abc1", "nft_id": 1},
            {"title":"abc2", "nft_id": 2},
            {"title":"abc3", "nft_id": 3},
        ],
    }
    res = requests.post(url, data=json.dumps(data), headers=header)

    return res.text

#元数据搜索测试
def search_metadata_test():
    db_link = "/ipfs/QmYUQee1mTUGjEMtk2ZBn8LdE1YVWueF3q5ec7WMgXsGfc#json"
    field = "name"
    word = "bc1"

    url = END_POINT + "search_metadata?db_link={}&field={}&word={}".format(
        urllib.parse.quote(db_link),
        field,
        word
    )
    #print(url)
    res = requests.get(url)

    return res.text

#图片上传测试
def upload_file_test():
    local_file = "color1.jpg"
    f = open(local_file, "rb")
    base64_bytes = base64.b64encode(f.read())
    base64_str = base64_bytes.decode()

    url = END_POINT + "upload_file"
    header = {"Content-Type": "application/json"}
    data = {
        "file": base64_str
    }

    res = requests.post(url, data=json.dumps(data), headers=header)

    return res.text

if __name__=="__main__":
    #res = insert_metadata_test()
    res = get_metadata_test()

    #res = upload_file_test()
    print(res)