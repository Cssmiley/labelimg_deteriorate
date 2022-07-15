#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 上面兩行是for python2(一定要原封不動放最上面) ,否則遇到中文會跳錯 SyntaxError: Non-ASCII character '\xe4' in file xml_parse_count.py on line 6, but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details

"""
需求: 計算劣化數量

- 選取資料夾路徑(GUI或手動填)-手動填
- 遍歷選取資料夾讀取 .xml 檔
- 列出該張圖片的所有劣化分類
- 計算各項劣化圖片總數量

使用
- 安裝套件 : 不需安裝,使用內建lib
- 執行 python檔:
    `> python3 xml_parse_count_csv.py "要處理的資料夾路徑"`
- 印出總數及各劣化數量如下範例:
    `Total xml : 6, defaultdict(<class 'int'>, {'crack_00': 3, 'rusty_water': 1, 'spalling': 4, 'crack_AC': 1, 'crack': 1, 'corrosion': 1})`
- 輸出 .csv 檔包含劣化數量資訊方便匯入到 excel 處理 
"""
import xml.etree.ElementTree  as ET
import logging
import os, sys
import shutil
import collections
# debug message in log file
logging.basicConfig(filename="log_filename.txt", 
                    level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# folder_path,用在指定要處理的資料夾 ｀python xml_parse_count.py "指定資料夾"｀
fn = sys.argv[1]
if os.path.exists(fn):
    print(os.path.basename(fn))
folder_path = fn


# 輸出單一劣化的 .xml
def write_single_deteriorate_xml(object_tag,out_xml_path):
# 組合要寫入 xml 的節點    
    # 建立labelImg輸出的 xml 檔的第一個節點 <annotation>
    xml_annotation = ET.Element("annotation")
    
    # 接著貼上上半段所有不是 <object> 的節點
    for child in root:
        if child.tag == "object":
            continue # 跳過 <object> 節點
        xml_annotation.append(child)
    # 最後再貼上特定的劣化節點    
    find_object = f"object[name='{object_tag}']"
    for xml_object in root.findall(find_object):
        logging.debug(f"xml_object: {xml_object}")
        xml_annotation.append(xml_object)
# 將組合好的節點寫入 .xml 檔
    tree._setroot(xml_annotation) # 將上面組合好的最上層節點 <annotation>設成根節點
    tree.write(out_xml_path, encoding="UTF-8")
    logging.debug(f"write_single_deteriorate_xml({object_tag})") # log down debug message for log file
 
# 遍歷 folder,讀取 xml file
for filename in os.listdir(folder_path):

    # 讀取檔案,只讀取 xml 檔
    filename = filename.lower() # 副檔名統一小寫
    if not filename.endswith('.xml'):
        continue # 跳過 .xml 以外的檔
    file_path = os.path.join(folder_path, filename)
    # read .xml file
    xml_path = file_path
    tree = ET.parse(xml_path)
    root = tree.getroot()

# 蒐集 <object> 底下的 <name> tag（也就是這張圖的所有劣化類別名稱),存到字典方便後續操作
    """用 collections.defaultdict 建立預設值為 0 的字典,
    將讀到的<name> 放到字典的 key,<name> 的數量放到字典的 value,
    用來計算單張圖片劣化類別的節點數(也就是一張圖有多少個特定劣化框選數量)"""
    deteriorate = root.findall("./object/name") # 取得所有類別名稱
    det = collections.defaultdict(int) 
    for name in deteriorate:
        det[name.text] += 1
    print(f"filename: {filename} \ndet: {det}")

# 排除無劣化的 xml 檔,依據劣化輸出 xml
    if not det:
        continue # 跳過沒有框選劣化的空 xml
    for key in det.keys():
    # deteriorate_folder_path,用在輸出各劣化類別資料夾路徑
        # deteriorate_folder_path = os.path.join(folder_path ,key) 
        deteriorate_folder_path = os.path.join(".",key)
        # output_xml_path,用在輸出的 .xml檔完整路徑
        output_xml_path = os.path.join(deteriorate_folder_path, filename.replace(".jpg",".xml"))
       
# 根據字典的keys(),建立資料夾並輸出新.xml檔
        
        # 檢查單一劣化資料夾是否已經存在,若不存在就新增資料夾
        if not os.path.exists(deteriorate_folder_path):
            os.makedirs(deteriorate_folder_path)
        # 檢查圖片是否存在,若不存在就複製 .jpg 檔到新資料夾內
        jpg_path = os.path.join(folder_path, filename.replace(".xml",".jpg"))
        jpg_copy_path = os.path.join(deteriorate_folder_path,filename.replace(".xml",".jpg"))
        if not os.path.exists(jpg_copy_path):
            shutil.copy(jpg_path, jpg_copy_path)
        # 寫入單一劣化 .xml 檔到單一劣化資料夾
        write_single_deteriorate_xml(key,output_xml_path)


