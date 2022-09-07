#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 上面兩行是for python2(一定要原封不動放最上面) ,否則遇到中文會跳錯 SyntaxError: Non-ASCII character '\xe4' in file xml_parse_count.py on line 6, but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details
import csv
import os
import platform
import subprocess
import xml.etree.ElementTree as ET
import collections
import sys
import re


# 劣化標註列表
det_list = ["crack", 
            "spalling",
            "efflorescence",
            "corrosion",
            "water_gain",
            "rusty_water"]

# 用在 python xml_parse_count.py "指定資料夾"
# 若存在 sys.argv[1] 就用來當路徑,否則就用.py 檔所在資料夾當路徑
try :
    fn = sys.argv[1]
except:
    fn = os.path.abspath('.')
    
print(fn)
print(os.path.isdir(fn))
if os.path.exists(fn):
    print(os.path.basename(fn))
folder_path = fn

"""讀取 XML 檔案"""


count = 0 # 用於計算總xml數(若每張都有輸出xml即是總張數)
count_det = collections.defaultdict(int) # 用於計算圖片個劣化類別總數
count_2000 = 0 # 用於計算2000張內不包含裂縫和無劣化的張數

for filename in os.listdir(folder_path):
# 讀取檔案,只讀取 xml 檔
    if not filename.endswith('.xml'): 
        continue # 跳過 .xml 以外的檔
    file_path = os.path.join(folder_path, filename)
    print(file_path)

    # 用於計算總xml數(若每張都有輸出xml即是總張數)
    count += 1

    # 從檔案載入並解析 XML 資料
    tree = ET.parse(file_path)
    root = tree.getroot()
    """尋找 XML 節點"""
    # 搜尋所有子節點
    # 用 Pythoninc 的 collections.defaultdict取代,計算單張圖片劣化類別
    deteriorate = root.findall("./object/name")
    det = collections.defaultdict(int)
    for name in deteriorate:
        det[name.text] += 1
    # 無劣化以 "other" 代表
    if not det:
        print(f"not det: {filename}")
        det["other"] += 1 
    print(det)
    print(f"det.keys: {det.keys()}, filename: {filename}")
    
    # 計算各圖片劣化類別總數
    for k in det.keys():
        count_det[k] += 1
"""
# 計算2000張內不包含裂縫和無劣化的張數
    flag = 0
    for i in det_list:
        if  re.match("crack",i):
            continue
        flag |= det.get(i,0) 
    if flag > 0:
        count_2000 += 1
"""
print(f"Total xml : {count}, {count_det}")
# print(f"count_2000: {count_2000}")
