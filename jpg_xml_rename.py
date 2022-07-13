import shutil
import logging
import os, sys

# debug message in log file
logging.basicConfig(filename="log_filename.txt", 
                    level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# folder path,用在 python xml_parse_count.py "指定資料夾"
fn = sys.argv[1]
if os.path.exists(fn):
    print(os.path.basename(fn))
folder_path = fn

# 遍歷 folder,讀取 xml file

# 取得所有檔案與子目錄名稱
files = os.listdir(folder_path)

# 改檔名串接數字
stream_num = 4075
# 改檔名串接字串
stream_word= "_CTCI"
# 更名後新檔案存放位置
new_foldername ="多重劣化" 
"""
# 遞迴列出所有子目錄與檔案
for root, dirs, files in os.walk(folder_path):
    print("路徑：", root)
    print("  目錄：", dirs)
    print("  檔案：", files)
    for _file in files:
        filename = _file.lower() # 副檔名統一小寫
        file_rootname = filename.split(".")[0]
        file_typename = filename.split(".")[1]
        print(f"file_rootname: {file_rootname}")
        fullpath = os.path.join(root,_file)

        # jpg 和 xml 分開處理(條件必須是不同檔案類型的排列順序相同)
        if not filename.startswith("."):
            newpath = os.path.join(root, str(stream_num) + stream_word+"."+file_typename)
            if (filename.endswith(".xml")) :
                print(f".xml file: {_file} \newpath: {newpath}")
                #os.rename(fullpath, fullpath.)
            if (filename.endswith(".jpg")) :
                print(f".jpg file: {_file} \nnewpath: {newpath}")
        # jpg 和 xml 一起改(要考慮更改後遍歷檔案仍會處理到的情況)
        #if (filename.endswith(".xml") | filename.endswith(".jpg") ) & (not filename.startswith(".")):
        #print(f"_file: {_file}")

        #shutil.move(file_rootname)
    """
# 遞迴列出所有子目錄與檔案
for root, dirs, files in os.walk(folder_path):
    print("路徑：", root)
    print("  目錄：", dirs)
    print("  檔案：", files)
    
    for _file in files:
        filename = _file.lower() # 副檔名統一小寫
        file_rootname = filename.split(".")[0]
        file_typename = filename.split(".")[1]
        fullpath = os.path.join(root,_file)
        newpath = os.path.join(root, str(stream_num) + stream_word+"."+file_typename)
        # 跳過 .xml 以外的檔
        if not filename.endswith('.xml'):
            continue
        print(_file)
        # 更名 .xml 檔
        print(f"fullpath: {fullpath}\nnewpath: {newpath}")
        os.rename(fullpath, newpath)
        # 更名 .jpg 檔
        print(f"jpg fullpath: {fullpath.replace('.xml', '.jpg')}\n jpg newpath: {newpath.replace('.xml', '.jpg')}")
        os.rename(fullpath.replace(".xml", ".jpg"), newpath.replace(".xml", ".jpg"))
        # 移動 .xml .jpg 檔
        new_folderpath = os.path.join(folder_path,new_foldername)
        if not os.path.exists(new_folderpath):
            os.makedirs(new_folderpath)
        shutil.move(newpath, new_folderpath)
        shutil.move(newpath.replace(".xml", ".jpg"), new_folderpath)
        stream_num += 1

