import json
import boto3
import os

# クライアントオブジェクトの取得
ddb = boto3.client("dynamodb")

# テーブル名とセカンダリインデックス名を取得
table_name = os.environ["TABLE_NAME"]
category_index_name = os.environ["CATEGORY_INDEX_NAME"]


# カテゴリ + 商品名前方一致の検索
def category_itemName_search(category, itemName):
    response = ddb.query(
          TableName=table_name,
          IndexName=category_index_name,
          KeyConditionExpression='category = :category and begins_with(itemName, :itemName)',
          ExpressionAttributeValues={
            ':category': {"S": category},
            ':itemName': {"S": itemName}
          }
    )   
    return response

# カテゴリだけの検索
def category_search(category):
    response = ddb.query(
          TableName=table_name,
          IndexName=category_index_name,
          KeyConditionExpression='category = :category',
          ExpressionAttributeValues={
            ':category': {"S": category}
          }
    )   
    return response

# 商品名前方一致だけの検索
def itemName_search(itemName):
    response = ddb.scan(
          TableName=table_name,
          FilterExpression='begins_with(itemName , :itemName)',
            ExpressionAttributeValues={
                ':itemName': {'S': itemName},
            }
    )   
    return response


# すべての商品を取得
def all_search():
    response = ddb.scan(
          TableName=table_name
    )   
    return response


def lambda_handler(event, context):
    try:
        msg = {}
        response = {}

        # 条件値の取得
        body = json.loads(event["body"])
        category = body.get("category","all")
        itemName = body.get("itemName","")

        # 条件値から検索方法を判断
        if  category != "all"  and len(itemName) > 0:
            response = category_itemName_search(category, itemName)
        #
        if category != "all" and len(itemName) == 0:
            response = category_search(category)
        #
        if  category == "all" and len(itemName) > 0:
            response = itemName_search(itemName)
        #
        if category == "all" and len(itemName) == 0:
            response = all_search()
        
        # レスポンスの処理
        ddb_formats_items = response.get("Items",[])
        Items = []
        for item in ddb_formats_items:
            formated_item = {
                    "id": item["id"]["S"],
                    "itemName": item["itemName"]["S"],
                    "category": item["category"]["S"],
                    "categoryName": item["categoryName"]["S"],
                    "price": item["price"]["N"],
                    "description": item["description"]["S"],
                    "image": item["image"]["S"]
            }
            Items.append(formated_item)
        msg = {"message": "商品の取得成功","Items": Items}
    except Exception as e:
        msg = {"message": "商品の取得失敗"}
        print(f"予期しないエラーが発生しました: {e}")

    #
    return {
        "statusCode": 200,
        "body": json.dumps(msg,
          ensure_ascii=False
        ),
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "application/json; charset=UTF-8",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "PUT,GET,POST,DELETE,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type,X-CSRF-TOKEN"
         }
    }