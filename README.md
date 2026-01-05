# 商品情報の検索アプリケーションのバックエンド

* フロントエンドは Next.js を想定しており、API Gateway の API で連携する。
* Lambda 関数と DynamoDB テーブル、グローバルセカンダリインデックスを使用
* Cognito ユーザープールで認証
    - フロントエンドは Amplify UI Livrary でサインインページを構成 
* API Gateway の API は、Cognito オーソライザーで認可
  
