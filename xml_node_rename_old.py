"""
xml_node_rename.py

需求:
1. 指定 old xml 和 new xml 路徑 (檔名相同) 及更動的劣化類別
2. 移除 old xml 的 特定劣化類別節點 (ex. <crack>)
3. 把 new xml 特定劣化類別節點 append 到 old xml 

程式:
- 選取新、舊資料夾路徑(GUI或手動填)-手動填 , 指定劣化類別
- 遍歷選取資料夾讀取 .xml 檔
- 移除舊的劣化類別節點,將更動的劣化類別節點複製,並寫入到舊的 .xml 檔

使用:
- 安裝套件 : 不需安裝,使用內建lib
- 執行 python:
```
    下面指令會使用 --new_folder 資料夾內的指定劣化類別節點 --deteriorate , 替代掉 --old_folder 內的指定劣化類別節點
    > python3 xml_node_move.py --deteriorate crack efflorescence --old_folder "要被置換的舊節點資料夾路徑" --new_folder "新節點資料夾路徑"

    可以把上面的 --deteriorate --old_folder --newfolder 換成簡寫的 -d -o -n ,如下所示（空格是為了和上面清楚對照可以不需要這麼多空格) 
    > python3 xml_node_move.py -d            crack efflorescence -o           "要被置換的舊節點資料夾路徑" -n           "新節點資料夾路徑"
```
指令參數說明：
```
    -d, --deteriorate  
        指定劣化類別,可指定一個到多個,例如. `-d crack` 或 `-d crack efflorescence`,這些劣化類別的節點會被置換掉
    -o, --old_folder
        要被置換掉的 .xml 檔案所在的資料夾路徑,例如. `D:\labelImg提交檔案`
    -n, --new_folder
        用來置換的調整過後的新劣化節點的 .xml 檔所在的資料夾路徑,例如. `D:\labelImg提交檔案\白華_efflorescence`
```
- 將 old 資料夾的 .xml檔內的特定劣化節點資訊(e.g. <crack>附帶的框選位置尺寸資訊) 換成 new 資料夾的 .xml檔的劣化節點資訊
"""


import csv
import os
import xml.etree.ElementTree as ET
import collections
import sys
import argparse

# 創建 .csv 檔
def create_csv(file_path, header_row):
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
        
# 定義輸入參數
parser = argparse.ArgumentParser()
parser.add_argument("-p",
                    "--path",
                    nargs=1,
                    type=str,
                    help="這是路徑--path")
parser.add_argument("-o",
                    "--old_tag",
                    nargs='*',
                    help="請輸入 要被置換的劣化標註 e.g. water_gain",
                    type=str)
parser.add_argument("-n",
                    "--new_tag",
                    nargs='*',
                    help="請輸入新劣化標註 e.g. infiltration_crack",
                    type=str)
args = parser.parse_args()
folder_path =  args.path[0]
det_orig = args.old_tag
det_new = args.new_tag
print(f"第 1 個引數：{args.path},type={type(args.path)}")
print(f"第 2 個引數: {args.old_tag}, type={type(args.old_tag)}")
print(f"第 3 個引數：{args.new_tag}, type={type(args.new_tag)}")

# 若要置換的old_tag劣化類別和new_tag劣化類別數量不一致,跳出提示並終止程式
if len(det_orig) != len(det_new):
    print(f"old_tag: {args.old_tag} 和 new_tag: {args.new_tag} ,數量不一致,請重新輸入old_tag 和 new_tag 前後對照!" )
    sys.exit()

"""讀取 XML 檔案"""

#count_det = {} # 用於計算圖片個劣化類別總數
count_det = collections.defaultdict(int)
for filename in os.listdir(folder_path):
# 讀取檔案,只讀取 xml 檔
    if not filename.endswith('.xml'): 
        continue # 跳過 .xml 以外的檔
    file_path = os.path.join(folder_path, filename)
    print(file_path)

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
        #print(f"name.text: {name.text}")
        det[name.text] += 1 # 計算劣化數量
        #print(f"det[name.text]: {det[name.text]}")
        #det_orig_dict = {i:item for i,item in enumerate(det_orig)}
        #print(f"enumerate(det_orig): {det_orig_dict}")
        """
        # 錯誤
        for i,item in enumerate(det_orig):

            if name.text in det_orig_dict.values():
                print(f"if name.text in det_orig_dict.values():name.text: {name.text}")
                print(f"i: {i},item: {item}")
                name.text = det_new[i]
                print(f"i:{i} det_new[i]: {det_new[i]}")
                print(f"name.text = det_new[i]: {name.text}")
        """
        for i in range(len(det_orig)):
            if name.text == det_orig[i]:
                name.text = det_new[i]
                print(f"i: {i}, det_orig[i]:{det_orig[i]}, det_new[i]: {det_new[i]}")
                file_path = os.path.join(folder_path, filename)
                tree.write(file_path,encoding="UTF-8")
        det[name.text] += 1
    print(f"det: {det}")
    print(det.keys(),filename)
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
print(count_det)
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