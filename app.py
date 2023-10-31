# app.py
from flask import Flask, request, render_template, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# 定義 Elasticsearch 的基本設定
elasticsearch_url = "http://140.115.126.33:9200"  # Elasticsearch 伺服器地址
index_name = "科展17-22"  # 索引名稱
username = "elastic"
password = "ytwu35415"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    search_term = request.form.get("search_term")

    # 定義搜索查詢
    search_query = {
        "query": {
            "match": {
                "摘要": search_term
            }
        }
    }

    # 執行 Elasticsearch 搜尋
    response = requests.get(f"{elasticsearch_url}/{index_name}/_search", json=search_query, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        # 解析和處理搜索結果
        search_results = response.json()
        results = []

        for hit in search_results["hits"]["hits"]:
            if hit['_score'] > 5:
                doc_source = hit['_source']
                # if "科目" in doc_source:
                #     del doc_source["科目"]
                # 擴展結果以包括摘要和關鍵詞欄位
                result = {
                    "科目": doc_source.get("科目", "未提供科目"),
                    "分數": hit['_score'],
                    "名稱": doc_source.get("名稱", "未提供名稱"),
                    "摘要": doc_source.get("摘要", "未提供摘要"),
                    "關鍵詞一": doc_source.get("關鍵詞一", "未提供關鍵詞"),
                    "關鍵詞二": doc_source.get("關鍵詞二", "未提供關鍵詞"),
                    "關鍵詞三": doc_source.get("關鍵詞三", "未提供關鍵詞")
                }
                results.append(result)

        return jsonify(results)
    else:
        return jsonify({"error": "搜索失敗"})

if __name__ == "__main__":
    app.run(debug=True)