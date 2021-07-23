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
import ipfshttpclient
import base64
#文档https://ipfs.io/ipns/12D3KooWEqnTdgqHnkkwarSrJjeMP2ZJiADWLYADaNvUb6SQNyPF/docs/http_client_ref.html#the-api-client


#ipfs版本<=0.6
IPFS_GATE = "/ip4/47.243.157.215/tcp/5001/http"
LOCAL_PATH = "data/img/"
client = ipfshttpclient.connect(IPFS_GATE)  # Connects to: /dns/localhost/tcp/5001/http

"""
功能：创建一个新节点
输入：无
返回：节点的hash
"""
def new_node():
    res = client.object.new()
    cid = res["Hash"]
    return cid

"""
功能：往根节点上添加新的子节点
输入：root_cid, 根节点cid
输入：data_cid, 数据节点cid
返回：添加后的新hash
"""
def add_node(root_cid, data_cid):
    #step 1，获得跟节点的links
    res = client.object.links(root_cid)

    #step 2,获得新的子节点名称，默认从1开始，依次增加1
    if "Links" in res:
        data_link_list = res["Links"]
        data_node_name = str(len(data_link_list) + 1)
    else:
        data_node_name = "1"

    #step 3，添加子节点
    res = client.object.patch.add_link(root_cid, data_node_name, data_cid)
    cid = res["Hash"]
    return cid

"""
功能：删除根节点的数据节点
输入：root_cid, 根节点cid
输入：data_cid_name, 数据节点cid名称
返回：添加后的新hash
"""
def del_node(root_cid, data_cid_name):
    new_root_cid = client.object.patch.rm_link(root_cid, data_cid_name)
    cid = new_root_cid["Hash"]
    return cid


"""
功能：向一个节点添加数据，添加后不超过1MB，再添加，否则返回-2
输入：data_cid， 数据节点
输入：text，需要添加的数据字符串
返回：添加后的hash
"""
def add_data(data_cid, text):
    #step 1，获得跟节点的数据
    ori_dat = client.object.data(data_cid)
    ori_dat_len = len(ori_dat) #原来字节数
    text_len = len(text.encode()) #字节数

    if ori_dat_len+text_len > 1*1024*1024: #如果大于1M，则返回错误
        return -2

    #添加数据
    res = client.object.patch.append_data(data_cid, io.BytesIO(text.encode()))
    cid = res["Hash"]
    return cid


"""
功能：向一个节点添加数据，添加后不超过1MB，再添加，否则返回-2
输入：data_cid， 数据节点
输入：data_list，需要添加的list
返回：添加后的hash
"""
def add_data_list(data_cid, data_list):
    #step 0,拼接data_list, 构造text
    text_list = []
    for item in data_list:
        text_list.append(json.dumps(item))

    text = "\n".join(text_list) + "\n" #最后需要多加一个回车
    #print(text+"|")

    #step 1，获得跟节点的数据
    ori_dat = client.object.data(data_cid)
    ori_dat_len = len(ori_dat) #原来字节数
    text_len = len(text.encode()) #字节数

    if ori_dat_len+text_len > 1*1024*1024: #如果大于1M，则返回错误
        return -2

    #添加数据
    res = client.object.patch.append_data(data_cid, io.BytesIO(text.encode()))
    cid = res["Hash"]
    return cid


"""
功能：初始化一个新数据表
输入：
返回：根节点的cid
"""
def ini_db():
    #step 1, 创建一个空的object，作为根节点
    root_cid = new_node()

    #step 2,创建一个空的object，作为数据节点
    data_cid =  new_node()

    #step 3, 将数据节点挂载到跟节点，只保留两层结构,生成新的cid，当做root
    new_root_cid = add_node(root_cid, data_cid)

    return new_root_cid


"""
功能：往数据表里面添加数据
输入：root_cid，根节点
输入：text，需要添加的数据字符串，不超过1M
返回：添加后的hash
"""
def insert_data(root_cid, text):
    #step 1，获得root_cid的最后一个节点，至少包含一个子节点，一定是没插满的
    #获得跟节点的links
    res = client.object.links(root_cid)
    data_link_list = res["Links"]
    last_node_cid = data_link_list[-1]["Hash"] #最后一个节点的hash
    last_node_name = data_link_list[-1]["Name"] #最后一个节点的名称

    #step 2,往最后一个节点添加数据，数据不超过1M
    new_data_cid = add_data(last_node_cid, text)

    if -2 == new_data_cid: #如果节点不够添加新的，text应该不超过1M
        new_data_cid1 = new_node() #新创建一个节点

        #添加数据
        new_data_cid2 = add_data(new_data_cid1, text)

        #添加link
        new_root_cid = add_node(root_cid, new_data_cid2)

        return new_root_cid

    else: #如果不超过1M，删除最后一个节点，添加成新的节点
        #删除最后一个节点
        new_root_cid = del_node(root_cid, last_node_name)
        #print("new_root_cid", new_root_cid, "last_node_name", last_node_name)

        #添加新的数据节点
        new_root_cid1 = add_node(new_root_cid, new_data_cid)

        return new_root_cid1


"""
功能：往数据表里面添加多个数据
输入：root_cid，根节点
输入：data_list，需要添加的list
返回：添加后的hash
"""
def insert_data_list(root_cid, data_list):
    #step 1，获得root_cid的最后一个节点，至少包含一个子节点，一定是没插满的
    #获得跟节点的links
    res = client.object.links(root_cid)
    data_link_list = res["Links"]
    last_node_cid = data_link_list[-1]["Hash"] #最后一个节点的hash
    last_node_name = data_link_list[-1]["Name"] #最后一个节点的名称

    #step 2,往最后一个节点添加数据，数据不超过1M
    new_data_cid = add_data_list(last_node_cid, data_list)

    if -2 == new_data_cid: #如果节点不够添加新的，text应该不超过1M
        new_data_cid1 = new_node() #新创建一个节点

        #添加数据
        new_data_cid2 = add_data_list(new_data_cid1, data_list)

        #添加link
        new_root_cid = add_node(root_cid, new_data_cid2)

        return new_root_cid

    else: #如果不超过1M，删除最后一个节点，添加成新的节点
        #删除最后一个节点
        new_root_cid = del_node(root_cid, last_node_name)
        #print("new_root_cid", new_root_cid, "last_node_name", last_node_name)

        #添加新的数据节点
        new_root_cid1 = add_node(new_root_cid, new_data_cid)

        return new_root_cid1

if __name__=="__main__":
    # cid = new_node()
    # print(cid)
    #root_cid = "QmdfTbBqBPQ7VNxZEYEj14VmRuZBkqFbiwReogJgS1zR1n"
    #data_cid = "QmYRoDuqg1pFQKjWxidjdJ1B66kbyCGwoXUqmGaArX7T59"
    #root_cid = "Qmb6SYjWeWgmZN7ERNDgjKrCBCG9JJrNdTriqKiZ7a4JWv"
    #cid = add_node(root_cid, data_cid)
    #print(cid)
    text = "-----hello world=-------"
    # cid = add_data(data_cid, text)
    root_cid = ini_db()
    print("root_cid", root_cid)

    #cid = insert_data(root_cid, text)
    data_list = [
            {"title":"abc1", "nft_id": 1},
            {"title":"abc2", "nft_id": 2},
            {"title":"abc3", "nft_id": 3},
        ]

    cid = insert_data_list("QmNr3U2TAPnP2wA4n2fP161Lqzp5JusW1Mo8iT9WaqFTj8", data_list)

    print(cid)