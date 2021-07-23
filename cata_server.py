#!/usr/bin/env python3
#coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Sun 01 Mar 2020 09:08:42 PM CST
# File Name: index.py
# Description:
######################################################################
import json
import time
import sys
import web
import json
import sync_ipfs
import sync_minerva
import minerva_service

urls = (
    '/hello', 'hello',
    '/upload_file', 'upload_file',#文件上传
    '/insert_metadata','insert_metadata',#插入一条元数据
    '/get_metadata','get_metadata',#获得一条元数据
    '/search_metadata','search_metadata',#搜索元数据
    '/ini_db','ini_db',#初始化数据库表
)

'''
测试
'''
class hello:
    def GET(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Content-Type','text/json; charset=utf-8', unique=True)
        web.header('Access-Control-Allow-Credentials', 'true')

        return "hello"


'''
上传文件
'''
class upload_file:
    def POST(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Content-Type','text/json; charset=utf-8', unique=True)
        web.header('Access-Control-Allow-Credentials', 'true')

        data = json.loads(web.data()) #base64格式的图片
        base64_str = data["file"]

        cid = sync_ipfs.upload_base64(base64_str)

        result = {}
        result["status"] = 0
        result["msg"] = "success"
        result["cid"] = cid

        return json.dumps(result, ensure_ascii=False)

'''
插入元数据
'''
class insert_metadata:
    def POST(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Content-Type','text/json; charset=utf-8', unique=True)
        web.header('Access-Control-Allow-Credentials', 'true')

        data_str = web.data()
        data = json.loads(data_str)

        uri = data["db"] #默认是ipfs的
        root_cid = uri.replace("ipfs://", "")
        meta_data = data["metatdata"]
        #print(root_cid, meta_data)

        new_root_cid = sync_minerva.insert_data_list(root_cid, meta_data)

        result = {}
        result["status"] = 0
        result["msg"] = "success"
        result["cid"] = new_root_cid

        return json.dumps(result, ensure_ascii=False)


'''
获得一条元数据
'''
class get_metadata:
    def GET(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Content-Type','text/json; charset=utf-8', unique=True)
        web.header('Access-Control-Allow-Credentials', 'true')

        param = web.input(db_link="", nft_id="")
        db_link = param.db_link
        nft_id = param.nft_id

        result = minerva_service.get_nft_by_id(db_link, nft_id)

        return json.dumps(result, ensure_ascii=False)

'''
搜索元数据
'''
class search_metadata:
    def POST(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Content-Type','text/json; charset=utf-8', unique=True)
        web.header('Access-Control-Allow-Credentials', 'true')

        param = web.input(db_link="", field="", word="")
        db_link = param.db_link
        field = param.field
        word = param.nft_id

        result = minerva_service.search_nft(db_link, field, word)
        return json.dumps(result, ensure_ascii=False)

'''
初始化minerva数据库表
'''
class ini_db:
    def GET(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Content-Type','text/json; charset=utf-8', unique=True)
        web.header('Access-Control-Allow-Credentials', 'true')
        cid = sync_minerva.ini_db()
        result = {}
        result["status"] = 0
        result["msg"] = "success"
        result["cid"] = cid

        return json.dumps(result, ensure_ascii=False)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()