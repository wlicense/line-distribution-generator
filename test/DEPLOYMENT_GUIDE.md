# 🚀 Streamlit Cloudへのデプロイ完全ガイド

## ✅ 準備完了の確認

コードは既にGitHubにプッシュ済みです:
- Repository: https://github.com/wlicense/line-distribution-generator
- Branch: main

## 📋 デプロイ手順

### ステップ1: Streamlit Cloudにアクセス

1. [https://share.streamlit.io/](https://share.streamlit.io/) を開く
2. 「Sign up」または「Sign in」をクリック
3. GitHubアカウントでログイン

### ステップ2: 新しいアプリをデプロイ

1. ダッシュボードで「New app」ボタンをクリック
2. 以下の情報を入力:
   - **Repository**: `wlicense/line-distribution-generator`
   - **Branch**: `main`
   - **Main file path**: `test/app.py`

### ステップ3: 環境変数を設定（最重要）

「Advanced settings」をクリックして、「Secrets」に以下を追加:

```toml
ANTHROPIC_API_KEY = "your-anthropic-api-key-here"

[google]
GOOGLE_CREDENTIALS_JSON = '''
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "your-cert-url"
}
'''
```

**重要な注意点**:
- `ANTHROPIC_API_KEY`には実際のAPIキーを入力してください
- `GOOGLE_CREDENTIALS_JSON`には、`/Users/hajime/Downloads/line-nao-1-8919545f6d51.json` ファイルの**全内容**を入力してください
- JSONの前後に `'''` （3つのシングルクォート）を忘れずに

### ステップ4: デプロイ実行

1. 「Deploy!」ボタンをクリック
2. 数分待つとデプロイが完了します
3. URLが発行されます（例: `https://line-distribution-generator.streamlit.app`）

## ✅ 動作確認

デプロイ後、以下を確認してください:

1. アプリのURLにアクセスできる
2. サイドバーに「ANTHROPIC_API_KEY: 設定済み」と表示される
3. フォームに入力して「生成する」ボタンをクリック
4. 17本の配信文が生成される
5. Google Spreadsheetへのリンクが表示される

## 🔧 トラブルシューティング

### エラー: "ANTHROPIC_API_KEY: 未設定"

→ Streamlit CloudのSecretsを確認してください。APIキーが正しく設定されているか確認。

### エラー: "Could not find credentials"

→ `GOOGLE_CREDENTIALS_JSON`が正しく設定されているか確認してください。
   - JSON全体がコピーされているか
   - `'''` が前後にあるか
   - 余計なスペースや改行がないか

### アプリが起動しない

1. Streamlit CloudのLogsタブを確認
2. エラーメッセージを確認して対処
3. requirements.txtに必要なパッケージが全て含まれているか確認

## 📞 サポート

問題が解決しない場合は、以下の情報を準備してGitHub Issuesで質問してください:
- エラーメッセージの全文
- Streamlit Cloudのログ
- 実行した手順

## 🎉 成功したら

デプロイが成功したら、URLを共有して誰でも使えるようにしましょう！

**URL**: `https://あなたのアプリ名.streamlit.app`
