# 商品情報の検索アプリケーションのバックエンド

* フロントエンドは Next.js を想定しており、API Gateway の API で連携する
* 商品画像は S3 バケットに保存
* Lambda 関数と DynamoDB テーブル、グローバルセカンダリインデックスを使用
* Cognito ユーザープールで認証
    - フロントエンドは Amplify UI Livrary でサインインページを構成 
* API Gateway の API は、Cognito オーソライザーで認可
* 
  <img width="940" height="422" alt="next-serverless-backend" src="https://github.com/user-attachments/assets/2a1ec66d-87b2-4c62-9557-5d2327640573" />

