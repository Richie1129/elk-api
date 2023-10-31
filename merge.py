import os
import pandas as pd

# 設定包含CSV文件的資料夾路徑
folder_path = 'D:\科展\科展'

# 獲取資料夾中的所有CSV文件
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 創建一個空的DataFrame來存儲合併後的數據
merged_data = pd.DataFrame()

# 遍歷每個CSV文件並合併到merged_data
for csv_file in csv_files:
    file_path = os.path.join(folder_path, csv_file)
    data = pd.read_csv(file_path)
    merged_data = pd.concat([merged_data, data])

# 保存合併後的數據到一個新的CSV文件
merged_data.to_csv('科展17-22.csv', index=False)
