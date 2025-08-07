#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''

## 使用
- 需安裝套件 : conda install -c conda-forge opencv
python3 -m pip install opencv-python
(ref: https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwi_t9_Rwov5AhVMqVYBHdLODrQQFnoECCcQAQ&url=https%3A%2F%2Fresearchdatapod.com%2Fpython-modulenotfounderror-no-module-named-cv2%2F&usg=AOvVaw2_s76JWRae1yekPVnlgZhZ)
- 將這個 .py 檔放到想篩選圖片的資料夾內
- 執行 python檔: python3 image_filter.py
- 若有不符合之色碼會新建資料夾,複製.png圖片檔進資料夾,並建立 .csv檔,顯示不符合色碼之 [X座標, y座標, 色碼],可用 Excel 匯入 .csv檔查看  
## 需求
- 請使用者輸入符合色碼組(零到多組不等)
- 選擇想篩選的資料夾(內含 .jpg .png .xcf)
    - 讀取圖片,只讀取 png 檔
    - 遍歷圖片所有 pixel 
    - 取得每一 pixel 的 hex 色碼
    - 判斷是否符合輸入篩選的色碼組
    - 若不符合，
        - 檢查資料夾是否存在,若不存在就新增資料夾
        - 檢查圖片是否存在,若不存在就複製圖片檔到新資料夾內
        - 新增csv檔
        - 紀錄xy位置和色碼
        - [excel] 在 excel 整理出不符合單一色碼(e.g. 若有 3 個不符合的 #ffffff 色碼,只記錄一個 #ffffff)
- 模組化
'''

"""
- 請使用者輸入符合色碼組(零到多組不等)
- 選擇想篩選的資料夾(內含 .jpg .png .xcf)
    - 讀取圖片,只讀取 png 檔
    - 遍歷圖片所有 pixel 
    - 取得每一 pixel 的 hex 色碼
    - 判斷是否符合輸入篩選的色碼組
    - 若不符合，新增資料夾，複製圖片檔到新資料夾內，新增csv檔，紀錄xy位置和色碼,在 excel 整理出不符合單一色碼(e.g. 若有 3 個不符合的 #ffffff 色碼,只記錄一個 #ffffff)

"""
import shutil, os
import cv2
import numpy as np
import sys
import csv

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
        
def rgb_to_hex(rgb_color, to_hex = False):
    '''RGB 轉 HEX
    :param rgb_color: RGB顏色元組,TUPLE[int, int, int]
    :param to_hex:    是否轉十六進位字串,默認不轉
    :return: int or str
    
    >>> rgb_to_hex((255, 255, 255))
    >>> 16777215
    
    >>> rgb_to_hex((255, 255, 255), to_hex = True)
    >>> #FFFFFF
    '''
    r, g, b = rgb_color
    result = (r << 16) + (g << 8) + b
    rgb_hex_str = "#{:02x}{:02x}{:02x}".format(r, g, b)
    return rgb_hex_str if to_hex else result
 
# 讀取圖像,解決 imread 不能讀中文路徑的問題
def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
    # imdecode讀取的是rgb,如果後續需要opencv處理的話,需要轉換成bgr,轉換後圖片顏色會變化
    # [Wrong colours with cv2.imdecode (python opencv)](https://stackoverflow.com/questions/52494592/wrong-colours-with-cv2-imdecode-python-opencv)
    #cv_img=cv2.cvtColor(cv_img,cv2.COLOR_RGB2BGR)
    return cv_img
    
np.set_printoptions(threshold=sys.maxsize) # 這裡多加一行代碼，避免控制台輸出省略號的問題

# 請使用者輸入符合色碼組(零到多組不等)
# rgb_hex_list = list(input("請輸入想篩選的色碼組 e.g. #FFFFFF #408080 #FFD306").split())
rgb_hex_list =["#ffffff", "#000000", "#ff0000", "#00ffff", "#b15bff", "#408080", "#ffd306"]

# 選擇想篩選的資料夾(內含 .jpg .png .xcf)
fn = sys.argv[1]
if os.path.exists(fn):
    print(f"path: {os.path.basename(fn)}")
folder_path = fn
#folder_path = os.path.abspath('.') # .py 檔放在要篩選的資料夾內時使用

folder_to_be_fixed = "folder_to_be_fixed" # 想新增的待修正資料夾名稱
folder_to_be_fixed_path = os.path.join(folder_path,folder_to_be_fixed)

for filename in os.listdir(folder_path):
# 讀取圖片,只讀取 png 檔
    if not filename.endswith('.png'): 
        continue # 跳過 .png 以外的檔
    file_path = os.path.join(folder_path, filename)
    print(file_path)
    #img = cv2.imread(file_path) # 讀取圖片 
    img = cv_imread(file_path)
    cv2.imshow("test",img)
    print(img.shape) # 顯示圖片的寬,高,顏色通道數

    # 遍歷圖片所有 pixel 
    for x in range(img.shape[0]):  # 圖片的高
        for y in range(img.shape[1]):  # 圖片的寬
            px = img[x, y]
            #print(px)    # 這樣就可以取得每個點的 bgr 值

            b, g, r = img[x, y] # opencv 數值是 b,g,r
            #print("RGB = {} {} {}".format(r, g, b))
            rgb_color = (r, g ,b)
            
            # 取得每一 pixel 的 hex 色碼
            rgb_hex_str = rgb_to_hex(rgb_color,to_hex=True)
            #print("hex(r) {} hex(r)[-2:] {}".format(hex(r), hex(r)[-2:]))
            #rgb_hex = hex(r)[-2:].replace("x", "0") + hex(g)[-2:].replace("x", "0") + hex(b)[-2:].replace("x", "0") # rgb轉 hex 色碼
            #rgb_hex_str = "#{}".format(rgb_hex)
            #print(rgb_hex_str)
            #print("RGB Hex = #{}".format(rgb_hex))

            # 判斷是否符合輸入篩選的色碼組
            if rgb_hex_str  == "#ffffff":
                continue
            if rgb_hex_str  not in rgb_hex_list:
                print(f"{filename} 不符合色碼組 {px} {rgb_hex_str}")
                
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
                    
