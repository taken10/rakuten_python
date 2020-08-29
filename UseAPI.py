import requests
import csv
import sys

# 取得件数
hits_number = 10

# API実行に必要な楽天アプリIDを外部CSVから読み込む
with open("csv/application_id.csv") as f:
    app_id = f.read()

# 検索キーワードを実行時入力
input_keyword = input("検索キーワード入力(複数ワード可): ")
 
def kick_rakten_api():
    try:
        REQUEST_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
    
        # パラメータ生成
        search_param = set_api_parameter()
        # getリクエスト
        response = requests.get(REQUEST_URL, search_param)
        # APIから返却された出力パラメーターを取得
        result = response.json()

        # 検索結果が1件以上の場合
        if result["hits"] > 0:
            result_list = []
            # 必要なパラメータを取り出してリスト化
            for i in result["Items"]:
                item_list = []
                item = i["Item"]
                item_list.append("商品名: " + item["itemName"])
                item_list.append("URL: " + item["itemUrl"])
                item_list.append("価格: " + str(item["itemPrice"]) + "円")
                result_list.append(item_list)
            # 確認用出力
            print(result_list)

            # 結果リストをCSV出力(同名CSVファイルが存在する場合は上書き)
            with open("csv/resultlist.csv", "w", encoding="Shift_jis") as f:
                writer = csv.writer(f, lineterminator="\n")
                writer.writerows(result_list)
        else:
            print("検索結果が0件です。")
    except Exception as e:
        print(e)

def set_api_parameter():
    parameter = {
          "format"        : "json"  # レスポンス形式
        , "keyword"       : input_keyword  # 検索キーワード
        , "applicationId" : [app_id]
        , "availability"  : 1   # 販売可能な商品のみ
        , "hits"          : hits_number  # 取得件数
        , "sort"          : "-reviewAverage"    # レビュー平均順（降順）
        }
    return parameter
 
kick_rakten_api()