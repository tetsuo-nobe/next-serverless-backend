import json
import boto3
import os

ddb = boto3.client("dynamodb")
table_name = os.environ["TABLE_NAME"]

def lambda_handler(event, context):
    try:
        msg = {}
        #
        response = ddb.scan(TableName=table_name)
        ddb_formats_items = response.get("Items",[])
        allItems = []
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
            allItems.append(formated_item)
        msg = {"message": "すべての商品の取得成功","allItems": allItems}
    except Exception as e:
        msg = {"message": "すべての商品の取得失敗"}
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