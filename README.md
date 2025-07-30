# labelimg_deteriorate
python xml 的CRUD處理 用在 AI影像標註
---


前置參考:
[python之lxml快速上手_Element（一）](https://www.twblogs.net/a/5b8cbda02b7177188334f4b7)

[python之lxml快速上手_Element（二）](https://www.twblogs.net/a/5b8cbda02b7177188334f4b6)

[python之lxml快速上手_ElementTree（三）](https://www.twblogs.net/a/5b8cbda52b7177188334f4bc)
<details  ><summary>labelImg 輸出 xml格式參考</summary>

```
    
<annotation>
	<folder>D2_picked</folder>
	<filename>20160801174444_real_0.jpg</filename>
	<path>D:\修改中\labelimg標註\girder\Class2\D2_picked\20160801174444_real_0.jpg</path>
	<source>
		<database>Unknown</database>
	</source>
	<size>
		<width>922</width>
		<height>688</height>
		<depth>3</depth>
	</size>
	<segmented>0</segmented>
	<object>
		<name>spalling</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>224</xmin>
			<ymin>277</ymin>
			<xmax>332</xmax>
			<ymax>334</ymax>
		</bndbox>
	</object>
	<object>
		<name>corrosion</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>192</xmin>
			<ymin>393</ymin>
			<xmax>275</xmax>
			<ymax>459</ymax>
		</bndbox>
	</object>
	<object>
		<name>corrosion</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>619</xmin>
			<ymin>265</ymin>
			<xmax>697</xmax>
			<ymax>323</ymax>
		</bndbox>
	</object>
</annotation>

```

</details>


檔案位置: 

---

```
xml_parse_count.py # 只計算數量不輸出 .csv 檔
xml_parse_count_csv.py # 計算數量並輸出 .csv檔
```
## 需求
![](https://i.imgur.com/OPr0ymS.png)

1. 計算劣化數量
    - 選取資料夾路徑(GUI或手動填)-手動填
    - 遍歷選取資料夾讀取 .xml 檔
    - 列出該張圖片的所有劣化分類
    - 計算各項劣化圖片總數量
    

    ## 使用
    - 安裝套件 : 不需安裝,使用內建lib
    - 執行 python檔: 
    `> python3 xml_parse_count_csv.py "要處理的資料夾路徑"`
    - 印出總數及各劣化數量如下範例:
    `Total xml : 6, defaultdict(<class 'int'>, {'crack_00': 3, 'rusty_water': 1, 'spalling': 4, 'crack_AC': 1, 'crack': 1, 'corrosion': 1})`
    - 輸出 .csv 檔包含劣化數量資訊方便匯入到 excel 處理
    (_csvfile.csv 存放處理一個資料夾的結果)
    (_csvtotal.csv 存放處理多個資料夾的結果,用excel 匯入來加總所有處理資料夾的結果)

---

`xml_parse_split_deteriorate.py`
## 需求
![](https://i.imgur.com/nFt8lB1.png)


2. 複製 .jpg圖片 和輸出 單一劣化 .xml檔 到新建的單一劣化資料夾 
    前置作業: 
        - 比對同一張圖片的多重劣化和個單一劣化的 xml 內容結構差異,確認需更改的地方
    程式:
        - 選取資料夾路徑(GUI或手動填)-手動填
        - 遍歷選取資料夾讀取 .xml 檔
        - 將劣化類別複製,並寫入到分別的劣化類別 .xml 檔
        - 複製.jpg圖片到劣化類別資料夾
        - 模組化

    ## 使用
    - 安裝套件 : 不需安裝,使用內建lib
    - 將這個 .py 檔放到想篩選圖片的資料夾內
    - 執行 python檔: 
    `> python3 xml_parse_split_deteriorate.py "要處理的路徑"`
    - 輸出單一劣化資料到對應的資料夾,複製.jpg 圖片檔並抽取單一劣化 .xml 檔進資料夾


---

地雷or障礙:
- xml 節點處理:
    1. 篩選劣化節點
        - 使用字典的方式,劣化種類放進 key,劣化數量放進 value 達成,範例如下:
        `{'crack':2, 'spalling':3, 'water_gain': 7}`
        - 搭配 collections.defaultdict 建立預設值為 0 的字典,將讀到的 xml <tag> 放到字典的key,xml <tag> 的數量放到字典的 value,用來計算單張圖片劣化類別的節點數(也就是一張圖有多少個特定劣化框選數量)
    
    2. 節點剪下貼上新xml檔
        - 上半部 xml結構組出來

擴展:
`所有 .py`
    1. 讀取要處理的資料夾 folder_path
    - 使用 Argparse 取代 sys.argv[1],好處是可輸入來源資料夾和目的資料夾,命令列夾 -h 會有說明
    `jpg_xml_rename.py`
    2. os.walk()會遞迴便利資料夾,但是沒有排序
`使用csv的 .py`
    3. 使用pandas 取代
    4. (X) 使用 *args **kwargs 來傳 header_row
    
