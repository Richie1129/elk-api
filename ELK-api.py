import requests
from requests.auth import HTTPBasicAuth

username = "elastic"
password = "ytwu35415"

# 定義 Elasticsearch 的基本設置
elasticsearch_url = "http://140.115.126.33:9200"  # Elasticsearch 伺服器地址
index_name = "科展17-22"  # 索引名稱

# 定義搜索查詢
search_query = {
    "query": {
        "match": {
            "摘要": "細胞"
        }
    }
}

# 執行 Elasticsearch 搜索
response = requests.get(f"{elasticsearch_url}/{index_name}/_search", json=search_query, auth=HTTPBasicAuth(username, password))

# 檢查是否成功
if response.status_code == 200:
    # 解析和處理搜索結果
    search_results = response.json()
    for hit in search_results["hits"]["hits"]:
        if hit['_score'] > 5:
            doc_source = hit['_source']
            if "科目" in doc_source:
                del doc_source["科目"]
            print(f"文檔 ID: {hit['_id']}, 分數: {hit['_score']}, 文章: {doc_source}")
        # 這裡您可以處理搜索結果中的文檔

else:
    print(f"搜索失敗，狀態碼: {response.status_code}")