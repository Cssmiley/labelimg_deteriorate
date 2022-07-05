#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 上面兩行是for python2(一定要原封不動放最上面) ,否則遇到中文會跳錯 SyntaxError: Non-ASCII character '\xe4' in file xml_parse_count.py on line 6, but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details
'''
## 使用
- 需安裝套件 : conda install -c conda-forge opencv
- 將這個 .py 檔放到想篩選圖片的資料夾內
- 執行 python檔: python3 image_filter.py
- 若有不符合之色碼會新建資料夾,複製.png圖片檔進資料夾,並建立 .csv檔,顯示不符合色碼之 [X座標, y座標, 色碼],可用 Excel 匯入 .csv檔查看  

## 需求
整理發問後當作範例的圖片與問題供之後參考
1. 計算劣化數量
- 選取資料夾路徑(GUI或手動填)
- 遍歷選取資料夾讀取 .xml 檔
- 列出該張圖片的所有劣化分類
- 計算各項劣化圖片總數量

2.複製 .jpg圖片 和輸出 單一劣化 .xml檔 到新建的單一劣化資料夾 
前置作業: 
    - 比對同一張圖片的多重劣化和個單一劣化的 xml 內容結構差異,確認需更改的地方
程式:
- 選取資料夾路徑(GUI或手動填)
- 遍歷選取資料夾讀取 .xml 檔
- 將劣化類別複製,並寫入到分別的劣化類別 .xml 檔
	- 檢查是否存在劣化類別資料夾
	- - [excel] 在 excel 整理出不符合單一色碼(e.g. 若有 3 個不符合的 #ffffff 色碼,只記錄一個 #ffffff)
- 模組化

地雷or障礙:
- xml 節點處理:
    1. 篩選劣化節點
    2. 節點剪下貼上新xml檔
        - 上半部 xml結構組出來
"""
<annotation>
	<folder>CTCI_0_2000</folder>
	<filename>875_CTCI.jpg</filename>
	<path>D:\修改中\labelimg標註\CTCI_0_2000\875_CTCI.jpg</path>
	<source>
		<database>Unknown</database>
	</source>
	<size>
		<width>1248</width>
		<height>963</height>
		<depth>3</depth>
	</size>
	<segmented>0</segmented>
            """
        - 下半部 劣化節點 篩選後複製貼上
# 下半部處理前
"""
	<object>
		<name>crack</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>1107</xmin>
			<ymin>664</ymin>
			<xmax>1128</xmax>
			<ymax>717</ymax>
		</bndbox>
	</object>
	<object>
		<name>rusty_water</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>663</xmin>
			<ymin>391</ymin>
			<xmax>713</xmax>
			<ymax>541</ymax>
		</bndbox>
	</object>
	<object>
		<name>rusty_water</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>383</xmin>
			<ymin>399</ymin>
			<xmax>395</xmax>
			<ymax>421</ymax>
		</bndbox>
	</object>
	<object>
		<name>corrosion</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>690</xmin>
			<ymin>366</ymin>
			<xmax>708</xmax>
			<ymax>383</ymax>
		</bndbox>
	</object>
	<object>
		<name>corrosion</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>384</xmin>
			<ymin>387</ymin>
			<xmax>394</xmax>
			<ymax>397</ymax>
		</bndbox>
	</object>
</annotation>
"""
'''

"""
- 請使用者選擇資料夾
- 選擇想篩選的資料夾(內含 .jpg .xml)
    - 讀取圖片,只讀取 png 檔
    - 遍歷圖片所有 pixel 
    - 取得每一 pixel 的 hex 色碼
    - 判斷是否符合輸入篩選的色碼組
    - 若不符合，新增資料夾，複製圖片檔到新資料夾內，新增csv檔，紀錄xy位置和色碼,在 excel 整理出不符合單一色碼(e.g. 若有 3 個不符合的 #ffffff 色碼,只記錄一個 #ffffff)

"""

import csv
import os
import platform
import subprocess
import xml.etree.ElementTree as ET
import collections
import sys
import re
# 創建 .csv 檔
def create_csv(file_path, header_row):
    path = file_path
    with open(path, 'w+') as file:
        csv_write = csv.writer(file)
        csv_write.writerow(header_row)
        file.close()

def create_csv_without_header_row(file_path):
    path = file_path
    with open(path, 'w+') as file:
        csv_write = csv.writer(file)
        #csv_write.writerow()
        file.close()      
        
# 寫入到 .csv 檔
def write_csv(file_path,data_row):
    path = file_path
    with open(path, 'a+') as file:
        csv_write = csv.writer(file)
        csv_write.writerow(data_row)
        file.close()

def write_dict_to_csv(csv_path,data_dict):   
    with open(csv_path,'a+',encoding='utf8',newline='') as f:
        #for i, d in enumerate(count_det):
        #   print(i,d)
        w = csv.DictWriter(f, data_dict)
        print(data_dict.keys())
        w.writeheader()
        for key in data_dict.keys():
            print(key)
            
        w.writerow(data_dict)
        f.close()

# 請使用者輸入符合色碼組(零到多組不等)
# rgb_hex_list = list(input("請輸入想篩選的色碼組 e.g. #FFFFFF #408080 #FFD306").split())
rgb_hex_list =["#ffffff", "#000000", "#ff0000", "#00ffff", "#b15bff", "#408080", "#ffd306"]

# 劣化標註列表
det_list = ["crack", 
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
#folder_path = os.path.abspath('.') # .py 檔放在要篩選的資料夾內時使用
# folder_path = r"/Users/2020mac01/Documents/測量與空間資訊_project/練習專案_to_bedeleted"
# pic_path = r"/Users/2020mac01/Documents/測量與空間資訊_project/練習專案_to_bedeleted/hexcode_20190819102713_703_65573_real_0_test_tobedelete_2.png" # 圖片路徑

folder_to_be_fixed = "folder_to_be_fixed" # 想新增的待修正資料夾名稱
folder_to_be_fixed_path = os.path.join(folder_path,folder_to_be_fixed)
csv_path = os.path.join(folder_path, "csvfile.csv")
"""讀取 XML 檔案"""



# 從字串中取得並解析 XML 資料
# root = ET.fromstring(country_data_as_string)


"""
path = folder_path
def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])
open_file(path)
"""

count = 0 # 用於計算總xml數(若每張都有輸出xml即是總張數)
#count_det = {} # 用於計算圖片個劣化類別總數
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
    
    # 節點 tag 屬性
    #print(root.tag)
    # 節點 attrib 屬性
    #print(root.attrib)
    # 子節點與屬性
    #for child in root:
    #    print(child.tag, child.attrib)
        
    # 使用索引存取節點
    #print(root[0].text)
    # 取得指定的屬性值
    #print(root[0].get('name'))
    
    """尋找 XML 節點"""
    # 搜尋所有子節點
    
    
    # 用 Pythoninc 的 collections.defaultdict取代,計算單張圖片劣化類別
    deteriorate = root.findall("./object/name")
    det = collections.defaultdict(int)
    for name in deteriorate:
        det[name.text] += 1
    print(det)
    print(f"det.keys: {det.keys()}, filename: {filename}")
    """
    if not os.path.exists(csv_path):
        create_csv_without_header_row(csv_path)
    write_dict_to_csv(csv_path,det)
    """
    """
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
    # 計算各圖片劣化類別總數
    for k in det.keys():
        count_det[k] += 1
    # 計算2000張內部包含裂縫和無劣化的張數
    """
    if  (det.get("spalling",0) |
        det.get("efflorescence",0) |
        det.get("rusty_water",0) |
        det.get("water_gain",0) |
        det.get("corrosion",0)) != 0  :
        count_2000 += 1
    """
    flag = 0
    for i in det_list:
        if  re.match("crack",i):
            continue
        flag |= det.get(i,0) 
    if flag > 0:
        count_2000 += 1

print(f"Total xml : {count}, {count_det}")
print(f"count_2000: {count_2000}")




# 新增csv檔，紀錄xy位置和色碼,在 excel 整理出不符合單一色碼(e.g. 若有 3 個不符合的 #ffffff 色碼,只記錄一個 #ffffff)
"""
csv_path = os.path.join(folder_to_be_fixed_path, filename.replace(".png", ".csv"))
header_row = ["檔名","x座標", "y座標", "色碼"]
if not os.path.exists(csv_path):
    create_csv(csv_path, header_row)
write_csv(csv_path,[filename,y, x,rgb_hex_str])
"""
"""          
                # 若不符合,檢查資料夾是否存在,若不存在就新增資料夾
                if not os.path.exists(folder_to_be_fixed_path): 
                    os.makedirs(folder_to_be_fixed_path)
                
                # 檢查圖片是否存在,若不存在就複製圖片檔到新資料夾內
                pic_copy_path = os.path.join(folder_to_be_fixed_path,filename)
                if not os.path.exists(pic_copy_path):
                    shutil.copy(file_path, folder_to_be_fixed_path)
                
                # 新增csv檔，紀錄xy位置和色碼,在 excel 整理出不符合單一色碼(e.g. 若有 3 個不符合的 #ffffff 色碼,只記錄一個 #ffffff)
                csv_path = os.path.join(folder_to_be_fixed_path, filename.replace(".png", ".csv"))
                header_row = ["檔名","x座標", "y座標", "色碼"]
                if not os.path.exists(csv_path):
                    create_csv(csv_path, header_row)
                write_csv(csv_path,[filename,y, x,rgb_hex_str])
"""