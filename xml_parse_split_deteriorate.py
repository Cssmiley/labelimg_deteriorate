"""
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

# 蒐集<object>的tag,存到字典方便後續操作
# 根據字典的keys(),建立資料夾並輸出.xml檔
    - 檢查資料夾是否存在,不存在才建立資料夾
    - 檢查.xml檔是否存在,不存在才輸出.xml
    - 寫入.xml檔
        
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

# folder path,用在 python xml_parse_count.py "指定資料夾"
fn = sys.argv[1]
if os.path.exists(fn):
    print(os.path.basename(fn))
folder_path = fn


# write xml with deteriorarion 
def write_single_deteriorate_xml(object_tag,out_xml_path):
    
    xml_annotation = ET.Element("annotation")
    for child in root:
        if child.tag == "object":
            continue
        xml_annotation.append(child)
    find_object = f"object[name='{object_tag}']"

    for xml_object in root.findall(find_object):
        logging.debug(f"xml_object: {xml_object}")
        xml_annotation.append(xml_object)
    tree._setroot(xml_annotation)
    tree.write(out_xml_path, encoding="UTF-8")
    logging.debug(f"write_single_deteriorate_xml({object_tag})") # log down debug message for log file
 
# 遍歷 folder,讀取 xml file
for filename in os.listdir(folder_path):

    # 讀取檔案,只讀取 xml 檔
    if not filename.endswith('.xml'):
        continue # 跳過 .xml 以外的檔
    file_path = os.path.join(folder_path, filename)
    # read .xml file
    xml_path = file_path
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 蒐集<object>的tag,存到字典方便後續操作
    # 用 Pythoninc 的 collections.defaultdict取代,計算單張圖片劣化類別
    deteriorate = root.findall("./object/name")
    det = collections.defaultdict(int) 
    for name in deteriorate:
        det[name.text] += 1
    print(f"det: {det}")

    # 排除無劣化的 xml 檔,依據劣化輸出 xml
    if not det:
        continue
    for key in det.keys():
        # deteriorate_folder_path,用在輸出各劣化類別資料夾
        deteriorate_folder_path = os.path.join(folder_path ,key)
        # output_xml_path
        output_xml_path = os.path.join(deteriorate_folder_path, filename.replace(".jpg",".xml"))
        # 根據字典的keys(),建立資料夾並輸出新.xml檔
        # 檢查單一劣化資料夾是否存在,若不存在就新增資料夾
        if not os.path.exists(deteriorate_folder_path):
            os.makedirs(deteriorate_folder_path)
        # 檢查圖片是否存在,若不存在就複製 .jpg 檔到新資料夾內
        jpg_path = os.path.join(folder_path, filename.replace(".xml",".jpg"))
        jpg_copy_path = os.path.join(deteriorate_folder_path,filename.replace(".xml",".jpg"))
        if not os.path.exists(jpg_copy_path):
            shutil.copy(jpg_path, jpg_copy_path)
        # 寫入單一劣化 .xml 檔到單一劣化資料夾
        write_single_deteriorate_xml(key,output_xml_path)


