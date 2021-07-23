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

#编码与解码的处理对象是byte

local_file = "color1.jpg"
# 编码
f = open(local_file, "rb")
#编码
base64_data = base64.b64encode(f.read()) #输出bytes
print(base64_data)

base64_data_str = str(base64_data)
print(base64_data_str[0:100])

base64_data_str = base64_data.decode()
print(base64_data_str.encode())