# AIプロンプトライブラリ - プロジェクト引き継ぎ書

## 📋 プロジェクト概要

### プロジェクト名
**AIプロンプトライブラリ - 3層サブスクリプションモデル + リセラー機能**

### 目的
- 500/1000/2000個のAIプロンプトを3つのプランで提供
- 無料サロン生からサブスク転換を最大化
- アカウント共有によるバイラル拡散
- 高利益率（98%以上）のSaaSビジネス

### 現在のステータス
- ✅ 価格設定モデル完成（心理学分析済み）
- ✅ リセラーモデル設計完成
- ✅ ユーザー動線設計完成
- ⏳ 実装待ち（これから開始）

---

## 🎯 ビジネスモデル

### 3つのプラン

| プラン | 月額 | 回数 | アカウント共有 | 主な機能 |
|--------|------|------|--------------|----------|
| **無料サロン生** | 無料 | 月10回 | ✅ OK | プロンプト利用のみ |
| **サブスク生** | 9,800円 | 月200回 | ✅ OK | グルコン参加 + プロンプト |
| **本コース生** | 19,800円 | 月1,000回 | ✅ OK | 本コース全特典 + プロンプト |

### 重要な特徴
1. **全プランでアカウント共有OK** → リセラーモデル
2. **追加クレジット販売なし** → シンプルな料金体系
3. **電話番号パスワード認証** → SMS通知連携
4. **卸売価格モデル** → ユーザーが自由に価格設定可能

---

## 💰 収益モデル

### 原価構造
- API単価: 0.38円/回（GPT-3.5 Turbo）
- インフラ: 6,000円/500人 or 45円/人

### 粗利率
- 無料: コスト7,900円/500人（予算内）
- サブスク: 粗利率98.8%（原価121円/月）
- 本コース: 粗利率97.9%（原価425円/月）

### リセラー収益例
- 個人コーチ: 10名に15,000円で販売 → 月52,000円利益
- オンラインサロン: 50名に付加価値提供 → 会員満足度UP
- 家族シェア: 4人で割り勘 → 1人2,450円/月

---

## 🔐 認証・決済システム

### 認証方式
- **ログインID**: メールアドレス
- **パスワード**: 電話番号（ハイフンなし、例: 09012345678）
- **SMS認証**: Twilio経由で確認コード送信

### 決済システム（UnivaPay）
- **決済リンク**: https://univa.cc/i3anjt
- **金額**: 9,800円（固定）
- **用途**: サブスク生プラン申し込み
- **重要**: このリンク1個のみ、1個ずつ申し込みさせる
- **本コース生**: 別途19,800円の決済リンクが必要（未作成）

### Twilio SMS設定
```
用途:
1. 新規登録完了通知（ログイン情報送信）
2. サブアカウント追加通知
3. 決済完了通知
4. パスワードリマインダー

SMS送信先: 登録した電話番号
形式: 日本の携帯番号（090/080/070から始まる11桁）
```

---

## 📂 ファイル構成

### 既存システム（現在稼働中）

#### 500版（無料サロン生用）
- **パス**: `/Users/hajime/Desktop/n8n/chat_system/`
- **ポート**: 5004
- **データ**: SQLite (`chat_system.db`)
- **HTML**: `templates/dashboard.html`
- **プロンプト**: HTMLに直接埋め込み

#### 1000版（サブスク生用）
- **パス**: `/Users/hajime/Desktop/n8n/chat_system_1000/`
- **ポート**: 5005
- **データ**: JSON (`prompts_1000_data.json`)
- **HTML**: `templates/dashboard.html`

#### 2000版（本コース生用）
- **パス**: `/Users/hajime/Desktop/n8n/chat_system_2000/`
- **ポート**: 5006
- **データ**: JSON (`prompts_2000_data.json`)
- **HTML**: `templates/dashboard.html`

### 分析・設計ドキュメント（作成済み）

```
/Users/hajime/Desktop/
├── reseller_model_analysis.py          # リセラーモデル分析
├── user_flow_design.md                 # ユーザー動線設計（★重要）
├── final_pricing_model.md              # 最終価格設定
├── subscription_tier_analysis.py       # サブスク層分析（200回推奨）
├── freemium_psychology_analysis.py     # 心理学分析（10回推奨）
├── credit_pricing_90percent_profit.py  # クレジット価格設定
├── free_tier_500_users_analysis.py     # 無料層500人分析
├── revised_pricing_model.py            # 改訂価格モデル
├── business_model_proposal.md          # ビジネスモデル提案
└── PROJECT_HANDOVER.md                 # このファイル
```

---

## 🗄️ データベース設計

### users テーブル（新規作成が必要）

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- 認証情報
    email TEXT UNIQUE NOT NULL,              -- ログインID
    phone TEXT NOT NULL,                     -- パスワード（電話番号）
    name TEXT NOT NULL,                      -- 氏名

    -- プラン情報
    plan TEXT DEFAULT 'free',                -- 'free', 'sub', 'premium'
    monthly_limit INTEGER DEFAULT 10,        -- 月間利用上限
    monthly_usage INTEGER DEFAULT 0,         -- 今月の使用回数
    usage_reset_date DATE,                   -- 使用回数リセット日

    -- アカウント構造
    master_account_id INTEGER,               -- サブアカウントの場合、マスターID
    is_master BOOLEAN DEFAULT 1,             -- マスターアカウントか

    -- 同意・規約
    terms_agreed BOOLEAN DEFAULT 0,          -- 利用規約同意
    sms_agreed BOOLEAN DEFAULT 0,            -- SMS送信同意
    terms_agreed_at DATETIME,                -- 同意日時

    -- 決済情報
    univapay_customer_id TEXT,               -- UnivaPay顧客ID
    univapay_charge_id TEXT,                 -- 最新決済ID
    next_billing_date DATE,                  -- 次回決済日
    subscription_status TEXT DEFAULT 'none', -- 'none', 'active', 'cancelled'

    -- タイムスタンプ
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,

    FOREIGN KEY (master_account_id) REFERENCES users(id)
);

-- インデックス
CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_phone ON users(phone);
CREATE INDEX idx_master_account ON users(master_account_id);
CREATE INDEX idx_plan ON users(plan);
```

### sub_accounts テーブル（新規作成が必要）

```sql
CREATE TABLE sub_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    master_id INTEGER NOT NULL,              -- マスターアカウントID
    sub_id INTEGER NOT NULL,                 -- サブアカウントID
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,                      -- 作成者（マスターID）
    status TEXT DEFAULT 'active',            -- 'active', 'suspended', 'deleted'

    FOREIGN KEY (master_id) REFERENCES users(id),
    FOREIGN KEY (sub_id) REFERENCES users(id),
    FOREIGN KEY (created_by) REFERENCES users(id),

    UNIQUE(master_id, sub_id)
);

-- インデックス
CREATE INDEX idx_master ON sub_accounts(master_id);
CREATE INDEX idx_sub ON sub_accounts(sub_id);
```

### payments テーブル（新規作成が必要）

```sql
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,

    -- 決済情報
    plan TEXT NOT NULL,                      -- 'sub', 'premium'
    amount INTEGER NOT NULL,                 -- 9800 or 19800
    currency TEXT DEFAULT 'JPY',

    -- UnivaPay連携
    univapay_charge_id TEXT UNIQUE,
    univapay_customer_id TEXT,

    -- ステータス
    status TEXT DEFAULT 'pending',           -- 'pending', 'completed', 'failed', 'refunded'
    payment_method TEXT,                     -- 'credit_card', etc.

    -- メタデータ
    metadata TEXT,                           -- JSON形式のメタデータ

    -- タイムスタンプ
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,

    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- インデックス
CREATE INDEX idx_user_payments ON payments(user_id);
CREATE INDEX idx_univapay_charge ON payments(univapay_charge_id);
CREATE INDEX idx_payment_status ON payments(status);
```

### usage_logs テーブル（既存拡張が必要）

```sql
-- 既存のchat_logsテーブルを拡張するか、新規作成
CREATE TABLE usage_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    prompt_number INTEGER NOT NULL,          -- 使用したプロンプト番号
    prompt_title TEXT,
    api_cost REAL DEFAULT 0.38,              -- API原価
    used_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- インデックス
CREATE INDEX idx_user_usage ON usage_logs(user_id);
CREATE INDEX idx_usage_date ON usage_logs(used_at);
```

---

## 🔌 API連携

### 1. UnivaPay決済

#### 基本情報
```
決済リンク: https://univa.cc/i3anjt
金額: 9,800円（固定）
用途: サブスク生プラン申し込み

⚠️ 重要制約:
- このリンク1個のみ使用可能
- 1個ずつ申し込みさせる（同時に複数申し込み不可）
- 本コース生（19,800円）は別途リンクが必要
```

#### 実装方針
```python
# config.py
UNIVAPAY_PAYMENT_LINK = "https://univa.cc/i3anjt"
SUBSCRIPTION_PRICE = 9800  # 円

# 申し込みフロー
# 1. ユーザーが「サブスク生に申し込む」ボタンクリック
# 2. 確認画面表示（金額: 9,800円）
# 3. UnivaPay決済リンクへリダイレクト
# 4. 決済完了後、Webhookで通知受信
# 5. データベース更新（plan='sub', monthly_limit=200）
# 6. SMS送信（決済完了通知）
```

#### Webhook処理（重要）
```python
@app.route('/webhook/univapay', methods=['POST'])
def univapay_webhook():
    """
    UnivaPay決済完了時のWebhook

    想定ペイロード:
    {
        "event": "charge.finished",
        "data": {
            "id": "charge_xxx",
            "amount": 9800,
            "currency": "JPY",
            "status": "successful",
            "metadata": {
                "user_id": "12345",
                "plan": "sub"
            }
        }
    }
    """
    payload = request.json

    # 1. 署名検証（セキュリティ）
    # 2. user_id取得
    # 3. データベース更新
    # 4. SMS送信
    # 5. 200 OK返却

    return jsonify({"status": "ok"}), 200
```

### 2. Twilio SMS

#### 基本情報
```
用途: ユーザーへの通知・認証
送信タイミング:
  1. 新規登録完了時
  2. サブアカウント追加時
  3. 決済完了時
  4. パスワードリマインダー

必要な環境変数:
  TWILIO_ACCOUNT_SID=ACxxxxxxxxxx
  TWILIO_AUTH_TOKEN=your_auth_token
  TWILIO_PHONE_NUMBER=+815012345678
```

#### 実装例
```python
from twilio.rest import Client

def send_sms(to_phone, message):
    """
    SMS送信

    Args:
        to_phone: 送信先電話番号（例: 09012345678）
        message: 送信メッセージ

    Returns:
        message.sid: Twilio メッセージID
    """
    # 電話番号を国際形式に変換
    if to_phone.startswith('0'):
        to_phone = '+81' + to_phone[1:]

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=to_phone
    )

    return message.sid

# 使用例: 新規登録時
def send_registration_sms(user):
    message = f"""AIプロンプトライブラリへようこそ！

【ログイン情報】
ID: {user.email}
パスワード: {user.phone}

【重要なリンク】
利用規約: https://example.com/terms
ログイン: https://example.com/login

ご登録ありがとうございます。"""

    send_sms(user.phone, message)
```

---

## 🎨 ユーザー動線（詳細は user_flow_design.md 参照）

### 1. 新規登録フロー

```
トップページ
   ↓
「新規登録」ボタン
   ↓
登録フォーム
   - メールアドレス
   - 電話番号
   - 氏名
   ☑ 利用規約に同意する
   ☑ SMS送信に同意する
   ↓
SMS送信（ログイン情報）
   ↓
ログイン画面
```

### 2. ログインフロー

```
ログイン画面
   ↓
メールアドレス: user@example.com
パスワード: 09012345678（電話番号）
   ↓
ダッシュボード
```

### 3. サブスク申し込みフロー

```
ダッシュボード
   ↓
「サブスク生に申し込む」ボタン
   ↓
確認画面:
  - プラン: サブスク生
  - 月額: 9,800円
  - 回数: 月200回
  - グルコン参加権
  ☑ 利用規約に同意する
   ↓
UnivaPay決済リンクへリダイレクト
https://univa.cc/i3anjt
   ↓
カード情報入力・決済
   ↓
Webhook受信（バックエンド）
   ↓
データベース更新:
  - plan = 'sub'
  - monthly_limit = 200
  - next_billing_date = now + 1 month
   ↓
SMS送信（決済完了通知）
   ↓
決済完了ページ
   ↓
ダッシュボードへリダイレクト
```

### 4. アカウント共有フロー

```
ダッシュボード（マスターアカウント）
   ↓
「アカウント管理」タブ
   ↓
「新規サブアカウント追加」
   - メールアドレス
   - 電話番号
   - 氏名
   ↓
サブアカウント作成
   ↓
SMS送信（サブアカウントへ）:
  「{マスター氏名}さんからアカウントが共有されました」
   ↓
サブアカウントでログイン可能
```

---

## 🛠️ 技術スタック

### バックエンド
- **言語**: Python 3.x
- **フレームワーク**: Flask
- **データベース**: SQLite3
- **認証**: Flask-Login（セッション管理）
- **API連携**: requests, twilio

### フロントエンド
- **テンプレート**: Jinja2
- **CSS**: カスタムCSS（既存）
- **JavaScript**: バニラJS

### 外部サービス
- **UnivaPay**: 決済処理
- **Twilio**: SMS送信
- **OpenAI**: GPT-3.5 Turbo API

### 環境変数（.env ファイル）
```bash
# OpenAI
OPENAI_API_KEY=sk-xxxxx

# Twilio
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_PHONE_NUMBER=+815012345678

# UnivaPay
UNIVAPAY_PAYMENT_LINK=https://univa.cc/i3anjt
UNIVAPAY_WEBHOOK_SECRET=xxxxx

# App
FLASK_SECRET_KEY=your-secret-key
DATABASE_PATH=/Users/hajime/Desktop/n8n/chat_system/chat_system.db
```

---

## 📝 実装フェーズ

### フェーズ1: 認証システム（優先度: 最高）

#### タスク
- [ ] データベースマイグレーション（usersテーブル作成）
- [ ] 新規登録画面（register.html）
- [ ] ログイン画面（login.html）
- [ ] 電話番号パスワード認証実装
- [ ] Twilio SMS連携
- [ ] 利用規約ページ作成
- [ ] 同意チェックボックス実装

#### 期待される成果物
```
/Users/hajime/Desktop/n8n/chat_system/
├── app.py（拡張）
├── templates/
│   ├── register.html（新規）
│   ├── login.html（新規）
│   └── terms.html（新規）
├── static/
│   └── css/auth.css（新規）
├── migrations/
│   └── 001_create_users_table.sql（新規）
└── utils/
    └── sms.py（新規）
```

### フェーズ2: UnivaPay決済連携（優先度: 高）

#### タスク
- [ ] プラン選択画面（plans.html）
- [ ] サブスク申し込み確認画面
- [ ] UnivaPay決済リンクへのリダイレクト実装
- [ ] Webhookエンドポイント作成
- [ ] 決済完了処理実装
- [ ] 決済完了SMS送信
- [ ] paymentsテーブル作成・記録

#### 期待される成果物
```
/Users/hajime/Desktop/n8n/chat_system/
├── app.py（拡張）
├── templates/
│   ├── plans.html（新規）
│   ├── subscribe_confirm.html（新規）
│   └── payment_success.html（新規）
├── migrations/
│   └── 002_create_payments_table.sql（新規）
└── utils/
    └── univapay.py（新規）
```

### フェーズ3: アカウント共有機能（優先度: 中）

#### タスク
- [ ] アカウント管理画面（account_management.html）
- [ ] サブアカウント追加機能
- [ ] クレジットプール管理
- [ ] sub_accountsテーブル作成
- [ ] サブアカウントへのSMS通知
- [ ] サブアカウント削除機能

#### 期待される成果物
```
/Users/hajime/Desktop/n8n/chat_system/
├── app.py（拡張）
├── templates/
│   └── account_management.html（新規）
├── migrations/
│   └── 003_create_sub_accounts_table.sql（新規）
└── utils/
    └── account_sharing.py（新規）
```

### フェーズ4: 使用回数管理・リセット（優先度: 中）

#### タスク
- [ ] 月次使用回数リセット（Cron/スケジューラー）
- [ ] 使用回数チェック機能
- [ ] 使用上限到達時の通知
- [ ] usage_logsテーブル作成
- [ ] ダッシュボードに使用状況表示

#### 期待される成果物
```
/Users/hajime/Desktop/n8n/chat_system/
├── cron/
│   └── reset_monthly_usage.py（新規）
├── utils/
│   └── usage_manager.py（新規）
└── templates/
    └── dashboard.html（拡張）
```

---

## 🚨 重要な制約・注意事項

### 1. UnivaPay決済リンク
```
⚠️ 超重要:
- 決済リンク: https://univa.cc/i3anjt
- 金額: 9,800円（固定）
- このリンク1個しかない
- 1個ずつ申し込みさせる（同時申し込み不可）
- サブスク生プランのみ対応
- 本コース生（19,800円）は別途リンクが必要（未作成）

実装上の対応:
- ユーザーが「申し込む」ボタンをクリック
- 確認画面で「金額: 9,800円」を明示
- UnivaPay決済リンクへリダイレクト
- Webhookで決済完了を検知
- データベース更新（plan='sub', monthly_limit=200）
```

### 2. 電話番号パスワード
```
⚠️ セキュリティ考慮:
- パスワードは電話番号（ハイフンなし）
- 例: 09012345678
- データベースにはハッシュ化して保存
- SMS送信時は平文で送信（ログイン情報通知のため）

実装:
from werkzeug.security import generate_password_hash, check_password_hash

# 登録時
hashed_phone = generate_password_hash(phone)

# ログイン時
if check_password_hash(user.phone, entered_phone):
    # ログイン成功
```

### 3. アカウント共有制限
```
⚠️ リスク管理:
- 1マスターアカウントあたりサブアカウント上限: 50名
- クレジットプールは共有（全サブが消費）
- サブアカウントはグルコン参加不可（マスターのみ）

実装:
# サブアカウント追加時
if count_sub_accounts(master_id) >= 50:
    return error("サブアカウント上限（50名）に達しています")
```

### 4. SMS送信コスト
```
⚠️ コスト管理:
- Twilio: 約10円/通
- 送信タイミングを最小限に
- 必須: 新規登録、決済完了、サブアカウント追加
- 任意: パスワードリマインダー

実装:
# SMS送信ログを記録
CREATE TABLE sms_logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    phone TEXT,
    message TEXT,
    sent_at DATETIME,
    twilio_sid TEXT,
    status TEXT
);
```

---

## 🔍 既存コードの理解

### 現在の app.py 構造（500版）

```python
# /Users/hajime/Desktop/n8n/chat_system/app.py

from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import openai

app = Flask(__name__)

# 主要エンドポイント
@app.route('/')
def index():
    # ログインチェック
    # ダッシュボード表示

@app.route('/chat', methods=['POST'])
def chat():
    # プロンプト使用
    # OpenAI API呼び出し
    # 使用回数カウント
    # chat_logsに記録

@app.route('/login', methods=['GET', 'POST'])
def login():
    # 現在はメアド＋パスワード
    # →電話番号パスワードに変更必要

# データベース
def get_db():
    conn = sqlite3.connect('chat_system.db')
    return conn

# 既存テーブル
# - users
# - chat_logs
# - usage_limits
# - advertisements
# - leak_attempts
# - payment_history
```

### 必要な変更点

1. **usersテーブル拡張**
```sql
-- 既存のusersテーブルに追加カラム
ALTER TABLE users ADD COLUMN phone TEXT;
ALTER TABLE users ADD COLUMN plan TEXT DEFAULT 'free';
ALTER TABLE users ADD COLUMN monthly_limit INTEGER DEFAULT 10;
ALTER TABLE users ADD COLUMN monthly_usage INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN master_account_id INTEGER;
ALTER TABLE users ADD COLUMN is_master BOOLEAN DEFAULT 1;
-- など
```

2. **認証ロジック変更**
```python
# 旧: メアド + パスワード
# 新: メアド + 電話番号

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    phone = request.form['phone']  # 電話番号をパスワードとして使用

    user = get_user_by_email(email)
    if user and check_password_hash(user.phone, phone):
        session['user_id'] = user.id
        return redirect(url_for('dashboard'))
```

3. **使用回数チェック**
```python
@app.route('/chat', methods=['POST'])
def chat():
    user = get_current_user()

    # プランに応じた上限チェック
    if user.monthly_usage >= user.monthly_limit:
        return jsonify({
            "error": "今月の利用上限に達しました",
            "message": "プランをアップグレードしてください",
            "upgrade_link": "/plans"
        })

    # OpenAI API呼び出し
    # ...

    # 使用回数カウント
    user.monthly_usage += 1
    update_user_usage(user.id, user.monthly_usage)
```

---

## 📚 参考ドキュメント

### 作成済みドキュメント
1. **user_flow_design.md** - ユーザー動線設計（★最重要）
2. **reseller_model_analysis.py** - リセラーモデル分析
3. **final_pricing_model.md** - 最終価格設定
4. **freemium_psychology_analysis.py** - 無料10回の心理学的根拠

### 外部ドキュメント
- UnivaPay API: （URL不明、要確認）
- Twilio SMS API: https://www.twilio.com/docs/sms
- OpenAI API: https://platform.openai.com/docs

---

## 🎯 次のステップ（実装開始時）

### ステップ1: 環境準備
```bash
cd /Users/hajime/Desktop/n8n/chat_system

# 環境変数ファイル作成
cat > .env << EOF
OPENAI_API_KEY=sk-xxxxx
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_PHONE_NUMBER=+815012345678
UNIVAPAY_PAYMENT_LINK=https://univa.cc/i3anjt
FLASK_SECRET_KEY=your-secret-key
EOF

# 必要なパッケージインストール
pip install twilio python-dotenv
```

### ステップ2: データベースマイグレーション
```bash
# バックアップ
cp chat_system.db chat_system.db.backup

# マイグレーション実行
python migrations/001_create_users_table.py
```

### ステップ3: 認証システム実装
```bash
# 新規ファイル作成
touch templates/register.html
touch templates/login.html
touch templates/terms.html
touch utils/sms.py

# app.py 拡張開始
```

### ステップ4: テスト
```bash
# 開発サーバー起動
python app.py

# ブラウザで確認
http://localhost:5004/register
http://localhost:5004/login
```

---

## 🆘 トラブルシューティング

### よくある問題

#### 1. Twilio SMS送信エラー
```
エラー: Unable to create record
原因: 電話番号形式が間違っている

解決策:
- 日本の携帯: +8190xxxxxxxx 形式
- ハイフンなし
- 先頭の0を削除して+81を付ける
```

#### 2. UnivaPay Webhook受信できない
```
エラー: Webhook呼ばれない
原因: UnivaPay側の設定不足

解決策:
- UnivaPay管理画面でWebhook URL登録
- https://your-domain.com/webhook/univapay
- ngrokなどでローカル開発時もテスト可能
```

#### 3. データベースロック
```
エラー: database is locked
原因: SQLite同時書き込み制限

解決策:
- connection.commit()後に必ずclose()
- または PostgreSQL/MySQLへ移行検討
```

---

## 📞 連絡先・リソース

### プロジェクトオーナー
- 名前: Hajime
- 作業ディレクトリ: `/Users/hajime/Desktop/`

### 重要なリンク
- UnivaPay決済: https://univa.cc/i3anjt
- システム500版: http://localhost:5004
- システム1000版: http://localhost:5005
- システム2000版: http://localhost:5006

### 開発環境
- OS: macOS (Darwin 24.3.0)
- Python: 3.x
- Git: 初期化済み（/Users/hajime/Desktop/.git）

---

## ✅ チェックリスト（実装前の確認）

### 環境確認
- [ ] Python 3.x インストール済み
- [ ] pip パッケージマネージャー利用可能
- [ ] Twilio アカウント作成済み
- [ ] Twilio 電話番号取得済み
- [ ] UnivaPay アカウント確認
- [ ] OpenAI API キー取得済み

### 設計確認
- [ ] user_flow_design.md 読了
- [ ] データベース設計理解
- [ ] UnivaPay決済フロー理解
- [ ] SMS送信タイミング理解
- [ ] アカウント共有ロジック理解

### 実装準備
- [ ] .env ファイル作成
- [ ] データベースバックアップ
- [ ] Gitコミット（作業前）
- [ ] 開発ブランチ作成（推奨）

---

## 📝 更新履歴

- 2025-01-05: 初版作成（プロジェクト引き継ぎ書）
- 内容: 価格設定、リセラーモデル、ユーザー動線、データベース設計、実装フェーズ

---

**このドキュメントを読めば、他のエージェントや開発者が即座にプロジェクトを引き継いで実装を開始できます。**
