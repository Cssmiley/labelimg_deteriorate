#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 上面兩行是for python2(一定要原封不動放最上面) ,否則遇到中文會跳錯 SyntaxError: Non-ASCII character '\xe4' in file xml_parse_count.py on line 6, but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details
import csv
import logging
import os
import platform
import subprocess
import xml.etree.ElementTree as ET
import collections
import sys
import re
# debug message in log file
logging.basicConfig(filename="log_filename.txt", 
                    level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")


# 創建 .csv 檔
def create_csv(file_path, header_row):
    logging.debug(f"create_csv({file_path}, {header_row})")
    path = file_path
    with open(path, 'w+') as file:
        csv_write = csv.writer(file)
        csv_write.writerow(header_row)
        file.close()

# 寫入到 .csv 檔
def write_csv(file_path,data_row):
    path = file_path
    with open(path, 'a+') as file:
        csv_write = csv.writer(file)
        csv_write.writerow(data_row)
        file.close()

def write_dict_to_csv(csv_path,data_dict,header_row):   
    logging.debug(f"write_dict_to_csv({csv_path},{data_dict})")
    with open(csv_path,'a+',encoding='utf8',newline='') as csv_output:
        #for i, d in enumerate(count_det):
        #   print(i,d)
        writer = csv.DictWriter(csv_output, fieldnames=header_row, extrasaction='ignore')
        print(f"data_dict{data_dict}")
        writer.writerow(data_dict)
        csv_output.close()
"""
# 使用pandas
import pandas as pd 
def write_pd_to_csv(csv_path,data_dict):   
    logging.debug(f"write_dict_to_csv({csv_path},{data_dict})")
    with open(csv_path,'a+',encoding='utf8',newline='') as csv_output:
        #for i, d in enumerate(count_det):
        #   print(i,d)
        #writer = csv.DictWriter(csv_output, fieldnames=data_dict.keys(),delimiter=",")
        writer = csv.DictWriter(csv_output, fieldnames=data_dict,delimiter=",")
        print(f"data_dict{data_dict}")
        #writer.writeheader()
        #for key in data_dict:
        #    print(f" key in data_dict: {key,data_dict[key]}")
        writer.writerow(data_dict)
        csv_output.close()
"""

# 劣化標註列表
det_list = ["crack", 
            "crack_01",
            "crack_AC",
            "crack_AC_01",
            "spalling",
            "efflorescence",
            "corrosion",
            "water_gain",
            "rusty_water"]
# 選擇想篩選的資料夾(內含 .jpg .png .xcf)
"""
response = input("是否輸入資料夾名稱, Y:自行輸入資料夾, N:搜尋.py檔案所在資料夾: ").upper()
if response == "Y":
    folder_path = input("請輸入資料夾名稱: ")
    print(folder_path)
elif response == "N":
    folder_path = os.path.abspath('.') # .py 檔放在要篩選的資料夾內時使用
else:
    print("Thanks")
    sys.exit()
"""
# 用在 python xml_parse_count.py "指定資料夾"

fn = sys.argv[1]
print(fn)
print(os.path.isdir(fn))
if os.path.exists(fn):
    print(os.path.basename(fn))
folder_path = fn
print(f"folder_path: {folder_path}")

#csv_path = os.path.join(folder_path, "csvfile.csv")
folder_name = os.path.basename(folder_path)
print(f"folder_name: {folder_name}")
csv_path = os.path.join(".",folder_name+"_csvfile.csv")
csv_total_path = os.path.join(".","_csvtotal.csv")
"""讀取 XML 檔案"""

count = 0 # 用於計算總xml數(若每張都有輸出xml即是總張數)
#count_det = {} # 用於計算圖片個劣化類別總數
count_det = collections.defaultdict(int) # 用於計算圖片個劣化類別總數
count_2000 = 0 # 用於計算2000張內不包含裂縫和無劣化的張數

for filename in os.listdir(folder_path):
# 讀取檔案,只讀取 xml 檔
    filename = filename.lower() # 副檔名統一小寫
    if not filename.endswith('.xml'): 
        continue # 跳過 .xml 以外的檔
    file_path = os.path.join(folder_path, filename)
    print(file_path)

    # 用於計算總xml數(若每張都有輸出xml即是總張數)
    count += 1

    # 從檔案載入並解析 XML 資料
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # 用 Pythoninc 的 collections.defaultdict取代,計算單張圖片劣化類別的個數(一個框選算一個)
    deteriorate = root.findall("./object/name")
    det = collections.defaultdict(int)
    for name in deteriorate:
        det[name.text] += 1
    print(f"det: {det}")
    print(f"det.keys: {det.keys()},set(det):{set(det)}, filename: {filename}")

    
    # use dict  as header
    filename_dict ={"filename":filename}
    csv_header_dict= {**filename_dict,**det} # 把filename 和 劣化 組一起當作第一標題列（csv要匯入excel做處理)
    """
    print(f"csv_header: {csv_header_dict}")
    if not os.path.exists(csv_path):
        #create_csv(csv_path,csv_header_dict.keys())
        create_csv(csv_path,csv_header_dict)
    #write_dict_to_csv(csv_path,csv_header_dict)
    write_pd_to_csv(csv_path,csv_header_dict)
    """
    # use list as header
    filename_list = ["filename"]
    # 把 檔名 和所有劣化類別組起來,當作csv檔匯入excel後的標題列
    for i in (det_list):
        filename_list.append(i)
    csv_header_list= filename_list
    print(f"csv_header_list: {csv_header_list}")

    if not os.path.exists(csv_path):
        create_csv(csv_path,csv_header_list)
    write_dict_to_csv(csv_path,csv_header_dict,csv_header_list)
    #write_pd_to_csv(csv_path,csv_header_dict) ＃ 試著用 pandas 處理
    
    """
    # 用不寫死的方式,試著組出 標題列 header 的內容
    det = {}
    for object_tag in root.iter('object'):
        name = object_tag.find('name').text
        if name not in det.keys():
            det[name] = 1
        else:
            det[name] += 1
    print(det) 
    print(det.keys())
    """

    # 計算各圖片劣化類別總數(一張圖有一種劣化算一個)
    for k in det.keys():
        count_det[k] += 1
    
    # 額外處理,計算2000張內部不包含裂縫和無劣化的張數
    flag = 0
    for i in det_list:
        if  re.match("crack",i):
            continue
        flag |= det.get(i,0) 
    if flag > 0:
        count_2000 += 1

    
    
# use dict  as header
foldername_dict ={"folder_path":folder_path}
#csv_total_header_dict= {**foldername_dict,**det}

# use list as header
foldername_list = ["folder_path"]
for i in (det_list):
    foldername_list.append(i)
csv_total_header_list= foldername_list

count_det_data={**foldername_dict,**count_det}
print(f"count_det_data: {count_det_data}")  
if not os.path.exists(csv_total_path):
    create_csv(csv_total_path,csv_total_header_list)
write_dict_to_csv(csv_total_path,count_det_data,csv_total_header_list)
#write_pd_to_csv(csv_path,csv_header_dict)

print(f"Total xml : {count}, {count_det }, {set(count_det)}")
print(f"count_2000: {count_2000}")


