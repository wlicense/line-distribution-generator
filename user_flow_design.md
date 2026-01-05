# ユーザー動線設計 - AIプロンプトライブラリ

## 1. 新規登録フロー

### ステップ1: 初回アクセス
```
トップページ
   ↓
「新規登録」ボタン
   ↓
登録フォーム
```

### ステップ2: 登録フォーム入力
```
【必須項目】
- メールアドレス（ログインID）
- 電話番号（パスワード）
- 氏名

【同意項目】
☑ 利用規約に同意する
☑ SMS送信に同意する（電話番号にショートメッセージを送信します）
```

### ステップ3: SMS認証
```
入力した電話番号にSMS送信
   ↓
「登録が完了しました。電話番号宛にSMSを送信しました。」
   ↓
SMS内容:
「AIプロンプトライブラリへようこそ！
 ログイン情報:
 - ID: {メールアドレス}
 - パスワード: {電話番号}

 利用規約: https://example.com/terms
 プライバシーポリシー: https://example.com/privacy」
```

### ステップ4: ログイン
```
ログイン画面
   ↓
メールアドレス: user@example.com
パスワード: 09012345678（電話番号）
   ↓
ダッシュボード
```

---

## 2. プラン選択フロー

### ダッシュボード画面
```
┌─────────────────────────────────────┐
│ 【現在のプラン】                        │
│ 無料サロン生（月10回）                   │
│                                       │
│ ┌──────────────────────────────┐   │
│ │ プラン変更・アップグレード         │   │
│ └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

### プラン選択画面
```
┌────────────────────────────────────────────┐
│ プランを選択してください                        │
├────────────────────────────────────────────┤
│ ☑ 無料サロン生                                │
│   月10回 | 無料                               │
│   ✅ アカウント共有OK                          │
│   ✅ 友人・受講生に使わせられます                │
│                                              │
│ ☐ サブスク生                                  │
│   月200回 | 9,800円/月                        │
│   ✅ グループコンサル参加権                     │
│   ✅ アカウント共有OK                          │
│   ✅ 好きな価格で再販できます                   │
│   【申し込む】ボタン                           │
│                                              │
│ ☐ 本コース生                                  │
│   月1,000回 | 19,800円/月                     │
│   ✅ 本コース全コンテンツ                       │
│   ✅ アカウント共有OK                          │
│   ✅ 個別コンサル優先枠                        │
│   【申し込む】ボタン                           │
└────────────────────────────────────────────┘
```

---

## 3. サブスク申し込みフロー（UnivaPay決済）

### ステップ1: プラン確認
```
「サブスク生プラン」申し込み
   ↓
確認画面:
┌──────────────────────────┐
│ サブスク生プラン           │
│ 月額: 9,800円              │
│ 利用回数: 月200回           │
│ グループコンサル参加権      │
│                           │
│ ☑ 利用規約に同意する       │
│                           │
│ 【UnivaPay決済へ進む】    │
└──────────────────────────┘
```

### ステップ2: UnivaPay決済
```
UnivaPay決済画面（外部リンク）
   ↓
クレジットカード情報入力
   ↓
決済完了
   ↓
リダイレクト: 当サイトの決済完了ページ
```

### ステップ3: 決済完了通知
```
決済完了ページ
   ↓
SMS送信:
「サブスク生プランへのアップグレードが完了しました！
 月額: 9,800円
 利用回数: 月200回

 次回決済日: 2025-02-05

 ダッシュボード: https://example.com/dashboard」
   ↓
ダッシュボードへリダイレクト
```

---

## 4. アカウント共有フロー（リセラー機能）

### マスターアカウント画面
```
ダッシュボード
   ↓
「アカウント管理」タブ
   ↓
┌──────────────────────────────────────┐
│ 【マスターアカウント情報】              │
│ プラン: サブスク生                      │
│ クレジットプール: 200回（残180回）       │
│                                        │
│ 【サブアカウント一覧】                  │
│ ┌────────────────────────────────┐ │
│ │ サブアカウント1                   │ │
│ │ メール: friend1@example.com      │ │
│ │ 使用回数: 10回                    │ │
│ │ 【削除】                          │ │
│ └────────────────────────────────┘ │
│                                        │
│ 【新規サブアカウント追加】              │
│   メールアドレス: ________________     │
│   電話番号: ________________           │
│   【追加】                             │
└──────────────────────────────────────┘
```

### サブアカウント作成フロー
```
マスターが「新規サブアカウント追加」
   ↓
メールアドレス・電話番号入力
   ↓
SMS送信:
「{マスター氏名}さんからAIプロンプトライブラリのアカウントが共有されました！

 ログイン情報:
 - ID: {メールアドレス}
 - パスワード: {電話番号}

 マスターアカウント: {マスター氏名}
 利用可能回数: 共有プール（残180回）

 ログイン: https://example.com/login」
   ↓
サブアカウントでログイン可能
```

---

## 5. ログインフロー

### 通常ログイン
```
ログイン画面
   ↓
メールアドレス: user@example.com
パスワード: 09012345678
   ↓
認証成功
   ↓
ダッシュボード
```

### パスワード忘れ（電話番号忘れ）
```
「パスワードを忘れた」リンク
   ↓
メールアドレス入力
   ↓
登録済み電話番号にSMS送信:
「パスワード（電話番号）の確認

 ログイン情報:
 - ID: {メールアドレス}
 - パスワード: {電話番号}

 ログイン: https://example.com/login」
```

---

## 6. 利用規約・同意フロー

### 新規登録時
```
登録フォーム
   ↓
☑ 利用規約に同意する（必須）
   └ リンク: 利用規約全文
☑ SMS送信に同意する（必須）
   └ 説明: 「電話番号にショートメッセージを送信します」
   ↓
全チェック必須で登録ボタン有効化
```

### SMS内容（利用規約リンク含む）
```
「AIプロンプトライブラリへようこそ！

【ログイン情報】
ID: {email}
パスワード: {phone}

【重要なリンク】
利用規約: https://example.com/terms
プライバシーポリシー: https://example.com/privacy

ご登録ありがとうございます。」
```

---

## 7. UnivaPay決済連携

### UnivaPay設定
```python
# UnivaPay設定（環境変数）
UNIVAPAY_APP_ID = "your_app_id"
UNIVAPAY_SECRET = "your_secret"
UNIVAPAY_API_URL = "https://api.univapay.com"

# サブスクプラン設定
SUBSCRIPTION_PLANS = {
    "sub": {
        "name": "サブスク生",
        "amount": 9800,
        "currency": "JPY",
        "period": "monthly",
        "uses": 200
    },
    "premium": {
        "name": "本コース生",
        "amount": 19800,
        "currency": "JPY",
        "period": "monthly",
        "uses": 1000
    }
}
```

### 決済フロー
```
1. ユーザーが「申し込む」ボタンクリック
   ↓
2. バックエンドでUnivaPay決済リンク生成
   POST /charges
   {
     "amount": 9800,
     "currency": "JPY",
     "customer_email": "user@example.com",
     "metadata": {
       "plan": "sub",
       "user_id": "12345"
     }
   }
   ↓
3. UnivaPay決済ページへリダイレクト
   ↓
4. ユーザーがカード情報入力・決済
   ↓
5. Webhookで決済完了通知受信
   ↓
6. データベース更新:
   - user.plan = "sub"
   - user.monthly_limit = 200
   - user.next_billing_date = now + 1 month
   ↓
7. 決済完了ページへリダイレクト
   ↓
8. SMS送信（決済完了通知）
```

---

## 8. データベース設計

### users テーブル
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,           -- ログインID
    phone TEXT NOT NULL,                  -- パスワード（電話番号）
    name TEXT NOT NULL,                   -- 氏名
    plan TEXT DEFAULT 'free',             -- free, sub, premium
    monthly_limit INTEGER DEFAULT 10,     -- 月間利用上限
    monthly_usage INTEGER DEFAULT 0,      -- 今月の使用回数
    master_account_id INTEGER,            -- サブアカウントの場合、マスターID
    is_master BOOLEAN DEFAULT 1,          -- マスターアカウントか
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    terms_agreed BOOLEAN DEFAULT 0,       -- 利用規約同意
    sms_agreed BOOLEAN DEFAULT 0,         -- SMS送信同意
    univapay_customer_id TEXT,            -- UnivaPay顧客ID
    next_billing_date DATE,               -- 次回決済日
    FOREIGN KEY (master_account_id) REFERENCES users(id)
);
```

### sub_accounts テーブル
```sql
CREATE TABLE sub_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    master_id INTEGER NOT NULL,           -- マスターアカウントID
    sub_id INTEGER NOT NULL,              -- サブアカウントID
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (master_id) REFERENCES users(id),
    FOREIGN KEY (sub_id) REFERENCES users(id)
);
```

### payments テーブル
```sql
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    plan TEXT NOT NULL,                   -- sub, premium
    amount INTEGER NOT NULL,
    currency TEXT DEFAULT 'JPY',
    univapay_charge_id TEXT,
    status TEXT,                          -- pending, completed, failed
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 9. SMS送信設定

### Twilio設定（推奨）
```python
from twilio.rest import Client

TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "+815012345678"  # Twilio取得番号

def send_sms(to_phone, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=to_phone
    )
    return message.sid
```

### SMS送信タイミング
1. **新規登録完了時**: ログイン情報・利用規約リンク
2. **サブアカウント追加時**: 共有通知・ログイン情報
3. **決済完了時**: プラン変更通知・次回決済日
4. **パスワード忘れ**: 電話番号（パスワード）の確認

---

## 10. 実装優先順位

### フェーズ1（必須）
1. ✅ ユーザー登録・ログイン（電話番号パスワード）
2. ✅ SMS送信（Twilio連携）
3. ✅ 利用規約・同意チェックボックス
4. ✅ プラン表示・選択画面

### フェーズ2（重要）
5. ✅ UnivaPay決済連携
6. ✅ サブスク申し込みフロー
7. ✅ 決済Webhook処理
8. ✅ プラン変更後のSMS通知

### フェーズ3（拡張）
9. ✅ アカウント共有機能（マスター/サブ）
10. ✅ サブアカウント管理画面
11. ✅ クレジットプール管理

---

この設計で実装を進めますか？
