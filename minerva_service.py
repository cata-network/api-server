#!/usr/bin/env python3
#coding=utf-8
#########################################################################
# Author: @maris
# Created Time: May 18  2017 18:55:41 PM CST
# File Name:spider.py
# Description:minerva服务
#########################################################################
import sys
import re
import json
import time
import io
import requests

HOST = "http://47.243.157.215:8047/query.json"

"""
功能：获得nft查询结果
输入：db_link, 数据表的链接，形式如/ipfs/QmUtyPDpYMv2tHg7yZSgdUahgEaFjeSwEWx8XjQ7gVaSRW#json
输入：nft_id, nft id，数据表默认需要包含字段中nft_id
返回：result, 查询结果列表
"""
def get_nft_by_id(db_link, nft_id):
    #step 1，构造query
    #query = "select * from "
    query = "select * from ipfs.`{}` where nft_id={}".format(
        db_link, nft_id
    )
    #print(query)
    #step 2,构造请求
    url = HOST
    header = {"Content-Type": "application/json"}
    data = {
        "queryType":"SQL",
        "query": query
    }

    res = requests.post(url, data=json.dumps(data), headers=header)
    #print(res.json())
    data = res.json()

    result = {}
    result["status"] = 0
    result["msg"] = data["queryState"]
    result["query_id"] = data["queryId"]
    result["results"] = data["rows"]

    return result


"""
功能：获得nft查询结果
输入：db_link, 数据表的链接，形式如/ipfs/QmUtyPDpYMv2tHg7yZSgdUahgEaFjeSwEWx8XjQ7gVaSRW#json
输入：field，搜索字段，目前暂时只支持一个
输入：word, 搜索关键词，
返回：result, 查询结果列表
"""
def search_nft(db_link,field, word):
    #step 1，构造query
    #query = "select * from "
    query = "select * from ipfs.`{}` where `{}` like '%{}%'".format(
        db_link, field, word
    )
    #print(query)
    #step 2,构造请求
    url = HOST
    header = {"Content-Type": "application/json"}
    data = {
        "queryType":"SQL",
        "query": query
    }

    res = requests.post(url, data=json.dumps(data), headers=header)
    #print(res.json())
    data = res.json()

    result = {}
    result["status"] = 0
    result["msg"] = data["queryState"]
    result["query_id"] = data["queryId"]
    result["results"] = data["rows"]

    return result


if __name__=="__main__":
    nft_id = 1
    db_link = "/ipfs/QmYUQee1mTUGjEMtk2ZBn8LdE1YVWueF3q5ec7WMgXsGfc#json"
    #result = get_nft_by_id(db_link, nft_id)
    field = "title"
    word = "bc1"
    result = search_nft(db_link,field, word)
    print(json.dumps(result))


