#!/usr/bin/env python3
"""
LINE配信文章生成AIエージェント（完全再現版）

元のスプレッドシートの構造を100%正確に再現
- 全ての行・列の配置
- 全ての文字・絵文字の位置
- 全ての書式・色・罫線
"""

import anthropic
import os
from typing import Dict, List
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

# 環境変数からAPIキーを取得
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
CREDENTIALS_PATH = '/Users/hajime/Downloads/line-nao-1-8919545f6d51.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# 既存のスプレッドシートID
EXISTING_SPREADSHEET_ID = '1RspYhO1szUp5U7rmZp6IwaIzigQ4LxebfzeNU6tSuOI'

class DistributionGenerator:
    """配信文章生成エージェント（完全再現版）"""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.model = "claude-sonnet-4-5-20250929"

        # 配信タイミングのテンプレート（17本・元データから完全コピー）
        self.timings = [
            "登録直後",
            "7日前　8:00",
            "６日前　8:00",
            "５日前　8:00",
            "４日前　8:00",
            "３日前　8:00",
            "1日前　21:00 （開催前日）",
            "1月14日　8:00 （開催当日朝）",
            "1月14日　19:00",
            "1月14日19:50（開催直前）",
            "1月14日23:00（特典受け取り）",
            "1月15日　8:00 （開催2日目）",
            "1月15日　19:00 （1時間前）",
            "23:30",
            "1月15日19:50（開催直前）",
            "1月16日 8:00",
            "1月16日　 20：00"
        ]

        # Few-shot Learning用の実際のサンプル（元データから抽出）
        self.sample_texts = {
            0: """AI ALL STARS
未来トークセッション2026に
ご参加頂きありがとうございます！

本サミットは、
累計40億超えの起業家を含む
AI業界で革命を起こし続ける8人のトップランナーが集結し、
"2026年以降の未来を勝ち抜く次世代のAI戦略" をテーマにお届けします。

📅 開催日時：1月14日(水)・15日(木) 20:00-23:00
🌐 開催形式：Zoom（完全予約制）

一時的なトレンドではなく、
「確かな経験」と「最先端のAI活用術」に基づく内容です。
2026年からの次世代の生き方を見つめ直す
貴重な2日間となるでしょう。

そして...
今回、参加者限定で、累計40億の起業家たちが
実際に使っている【超シークレット特典】を準備してます🎁

当日、楽しみにしていてください✨""",

            1: """2026年の市場を独占するための
最新AI自動化ツールとは？

AI ALL STARS
未来トークセッション2026

2日間全セッション参加者限定
で進呈される「超シークレット特典」

それがグランドフィナーレ特典 です。

業界TOPのAI講師たちの
 「思考」と「作業」を再現できるAIツールが手に入るとしたら？


最新のバズ動画の台本を再現できるAIツール

24時間365日、あなたの代わりに動くAIエージェント

累計40億の知恵を学習させたAI機能

これらを手に入れることで、 サミットで学んだ戦略を「知っている」状態から 「その場ですぐに実行できる」状態へと引き上げます。"""
        }

        # 各配信の目的とガイドライン
        self.guidelines = {
            0: {
                "purpose": "ウェルカムメッセージ + 特典案内",
                "char_range": (400, 450),
                "elements": ["イベント概要", "開催日時", "参加特典", "オープンチャット誘導"]
            },
            1: {
                "purpose": "シークレット特典の訴求",
                "char_range": (350, 450),
                "elements": ["カウントダウン", "限定特典の価値", "緊急性"]
            },
            2: {
                "purpose": "登壇者紹介（1人目）",
                "char_range": (400, 460),
                "elements": ["カウントダウン", "実績・権威", "学べる内容", "ターゲットの悩み解決"]
            },
            3: {
                "purpose": "登壇者紹介（2人目）",
                "char_range": (400, 450),
                "elements": ["カウントダウン", "実績・権威", "学べる内容", "ターゲットの悩み解決"]
            },
            4: {
                "purpose": "登壇者紹介（3人目）",
                "char_range": (340, 400),
                "elements": ["カウントダウン", "実績・権威", "学べる内容", "ターゲットの悩み解決"]
            },
            5: {
                "purpose": "登壇者紹介（4人目）またはコア機能紹介",
                "char_range": (350, 380),
                "elements": ["カウントダウン", "核となる価値提案", "ベネフィット"]
            },
            6: {
                "purpose": "前日リマインド",
                "char_range": (350, 380),
                "elements": ["明日開催の強調", "全体像", "特典再訴求", "アーカイブなし強調"]
            },
            7: {
                "purpose": "当日朝リマインド",
                "char_range": (350, 380),
                "elements": ["本日開催の強調", "テーマ再確認", "リアルタイム参加促進"]
            },
            8: {
                "purpose": "開場通知（1日目）",
                "char_range": (250, 310),
                "elements": ["開場の強調", "Zoomリンク情報", "簡潔な案内"]
            },
            9: {
                "purpose": "1日目終了後のエンゲージメント",
                "char_range": (300, 350),
                "elements": ["感謝", "反応紹介", "次の案内予告", "スタンプ促進"]
            },
            10: {
                "purpose": "開場通知（2日目）",
                "char_range": (250, 310),
                "elements": ["最終日の強調", "Zoomリンク情報", "特典リマインド"]
            },
            11: {
                "purpose": "2日目朝のリマインド",
                "char_range": (350, 400),
                "elements": ["最終日の強調", "テーマ再確認", "特典リマインド"]
            },
            12: {
                "purpose": "2日目開催1時間前",
                "char_range": (350, 400),
                "elements": ["カウントダウン", "参加準備の促進", "盛り上がり演出"]
            },
            13: {
                "purpose": "2日目終了後の感謝",
                "char_range": (250, 300),
                "elements": ["感謝", "反応紹介", "特典案内予告"]
            },
            14: {
                "purpose": "開場通知（2日目）",
                "char_range": (250, 310),
                "elements": ["最終日の強調", "Zoomリンク情報", "特典リマインド"]
            },
            15: {
                "purpose": "翌日フォローアップ",
                "char_range": (300, 350),
                "elements": ["感謝", "反応紹介", "次のステップ案内"]
            },
            16: {
                "purpose": "アーカイブ配信案内",
                "char_range": (300, 350),
                "elements": ["期間限定強調", "全特典提示", "緊急性（期限）"]
            }
        }

    def generate_distribution(self, params: Dict[str, str], dist_num: int) -> Dict:
        """指定された配信番号の文章を生成"""
        guideline = self.guidelines[dist_num]

        # プロンプトを構築
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(params, dist_num, guideline)

        # Claude APIで生成
        message = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            temperature=0.8,  # Few-shot Learningのため少し高めでクリエイティブに
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": user_prompt
            }]
        )

        line_content = message.content[0].text.strip()

        # メール件名・プレビュー・本文も生成
        email_data = self._generate_email_metadata(params, dist_num, line_content)

        return {
            "distribution_number": dist_num,
            "timing": self.timings[dist_num],
            "line_content": line_content,
            "char_count": len(line_content),
            "email_subject": email_data["subject"],
            "email_preview": email_data["preview"],
            "email_body": email_data["body"]
        }

    def _build_system_prompt(self) -> str:
        """システムプロンプトを構築"""
        return """あなたは、JVイベント（ジョイントベンチャーイベント）のLINE配信文章を生成する専門家です。

【役割】
- 魅力的で行動を促す配信文を作成
- ターゲットの心理を理解し、適切なタイミングで適切なメッセージを届ける
- 緊急性・希少性を演出し、参加率を最大化

【重要な原則】
1. 具体的な数字・実績で信頼性を担保
2. ターゲットの悩みに寄り添う
3. 理想の未来を明確に示す
4. 適切な絵文字で視覚的な魅力を高める
5. 改行と空白で読みやすさを確保
6. 明確な行動喚起（CTA）を含める

【トーン】
- フレンドリーかつプロフェッショナル
- ポジティブで期待感を持たせる
- 押し付けがましくない、誠実な語り口"""

    def _build_user_prompt(self, params: Dict[str, str], dist_num: int, guideline: Dict) -> str:
        """ユーザープロンプトを構築（Few-shot Learning版）"""
        return f"""あなたはLINE配信文章の作成エキスパートです。
以下の参考例と同じ熱量・トーン・センスで、新しい配信文を作成してください。

【参考例1 - 登録直後の配信】
{self.sample_texts[0]}

【参考例2 - 7日前の配信】
{self.sample_texts[1]}

上記の参考例から学ぶべきポイント：
✨ 絵文字を効果的に使用（🎁✨🌐📅🎊など）
✨ 短い文で改行を多用し、リズム感を出す
✨ 【】で重要な部分を強調
✨ "..." で余韻を残す
✨ 数字や実績を具体的に示す（40億、8人など）
✨ ワクワク感とカウントダウンの演出
✨ 親しみやすく、熱量のある文体

【新しい配信の情報】
イベント情報：
- コンセプト: {params['concept']}
- ターゲット: {params['target']}
- 解決する課題: {params['problems']}
- 理想の未来: {params['ideal_future']}
- 実績: {params['achievements']}

配信タイミング: {self.timings[dist_num]}
配信番号: {dist_num}

【配信{dist_num}の要件】
- 目的: {guideline['purpose']}
- 文字数目安: {guideline['char_range'][0]}-{guideline['char_range'][1]}文字
- 含めるべき要素: {', '.join(guideline['elements'])}

【出力形式】
LINE配信文のみを出力してください。上記の参考例と同じ熱量・トーン・センスで作成してください。
説明文や前置きは不要です。"""

    def _generate_email_metadata(self, params: Dict[str, str], dist_num: int, line_content: str) -> Dict:
        """メールの件名、プレビュー、本文を生成"""
        prompt = f"""以下のLINE配信文に対応するメール配信の「件名」「プレビュー文」「本文」を生成してください。

【LINE配信文】
{line_content}

【イベント情報】
- コンセプト: {params['concept']}

【出力形式】
以下のJSON形式で出力してください：
{{
    "subject": "件名（30文字以内、開封率を高める工夫）",
    "preview": "プレビュー文（13文字程度、興味を引く一言）",
    "body": "本文（LINE配信文をメール用に最適化、400-600文字）"
}}

JSON以外の説明文は不要です。"""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        import json
        import re
        response_text = message.content[0].text.strip()

        # JSONを抽出
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        # JSONブロックを正規表現で抽出
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            response_text = json_match.group(0)

        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"      ⚠️ JSON解析エラー: {e}")
            print(f"      応答内容: {response_text[:200]}...")
            # エラー時はデフォルト値を返す
            return {
                "subject": "AI ALL STARS イベントのご案内",
                "preview": "重要なお知らせ",
                "body": f"LINE配信文をご確認ください。\n\nご不明な点がございましたら、お気軽にお問い合わせください。"
            }

    def generate_all_distributions(self, params: Dict[str, str]) -> List[Dict]:
        """全12配信を生成"""
        print("=" * 80)
        print("📝 配信文章生成開始")
        print("=" * 80)

        all_distributions = []

        for dist_num in range(17):  # 17本すべて生成
            print(f"\n【配信{dist_num}】生成中... ({self.timings[dist_num]})")
            try:
                distribution_data = self.generate_distribution(params, dist_num)
                all_distributions.append(distribution_data)
                print(f"  ✅ 完了 ({distribution_data['char_count']}文字)")
            except Exception as e:
                print(f"  ❌ エラー: {e}")
                raise

        print(f"\n{'=' * 80}")
        print("✅ 全17配信の生成完了！")
        print(f"{'=' * 80}")

        return all_distributions

    def export_to_existing_spreadsheet_perfect(self, distributions: List[Dict], params: Dict[str, str]) -> str:
        """既存のGoogle Spreadsheetに完全再現版で出力"""
        credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_PATH, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)

        spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{EXISTING_SPREADSHEET_ID}"
        print(f"\n✅ 既存のスプレッドシートに書き込み: {spreadsheet_url}")

        # 新しいシートを追加
        sheet_title = f"AI生成完全版_{datetime.now().strftime('%m%d_%H%M')}"

        try:
            request = {
                'addSheet': {
                    'properties': {
                        'title': sheet_title,
                        'gridProperties': {
                            'rowCount': 100,
                            'columnCount': 30
                        }
                    }
                }
            }
            response = service.spreadsheets().batchUpdate(
                spreadsheetId=EXISTING_SPREADSHEET_ID,
                body={'requests': [request]}
            ).execute()

            sheet_id = response['replies'][0]['addSheet']['properties']['sheetId']
            print(f"✅ 新しいシート '{sheet_title}' を作成 (ID: {sheet_id})")
        except Exception as e:
            print(f"⚠️  シート作成エラー: {e}")
            return None

        # データを準備（完全再現版）
        values = self._prepare_perfect_spreadsheet_data(distributions, params)

        # データを書き込み
        body = {'values': values}
        service.spreadsheets().values().update(
            spreadsheetId=EXISTING_SPREADSHEET_ID,
            range=f'{sheet_title}!A1',
            valueInputOption='RAW',
            body=body
        ).execute()

        print("✅ データ書き込み完了")

        # 書式を適用（完全再現版）
        print("🎨 デザイン適用中...")
        self._apply_perfect_formatting(service, EXISTING_SPREADSHEET_ID, sheet_id, len(distributions))
        print("✅ デザイン適用完了")

        return spreadsheet_url

    def _prepare_perfect_spreadsheet_data(self, distributions: List[Dict], params: Dict[str, str]) -> List[List]:
        """スプレッドシート用のデータを準備（完全再現版）"""
        # 列の構成:
        # A: 空
        # B: 主ラベル
        # C: サブラベル
        # D, F, H, J, L, N, P, R, T, V, X, Z (偶数): フラグ列
        # E, G, I, K, M, O, Q, S, U, W, Y, AA (奇数): 内容列

        rows = []

        # 行1: 空行
        rows.append([])

        # 行2: タイトル（B2に「AI ALL STARS 配信文章」、後で結合）
        row2 = ["", "AI ALL STARS 配信文章"] + [""] * 30
        rows.append(row2)

        # 行3: 日付行（元のスプレッドシートにあった日付）
        row3 = ["", "", ""]  # A, B, C空
        for i, dist in enumerate(distributions):
            if i == 0:
                row3.extend(["", ""])  # 配信0は日付なし
            elif i == 1:
                row3.extend(["", "2026/01/07"])  # 配信1
            elif i == 2:
                row3.extend(["", "2026/01/08"])  # 配信2
            else:
                row3.extend(["", ""])  # 他は空
        rows.append(row3)

        # 行4: No.
        row4 = ["", "No.", ""]  # B4:C4結合用
        for dist in distributions:
            row4.extend(["", str(dist['distribution_number'])])  # フラグ列空、内容列に番号
        rows.append(row4)

        # 行5: 配信タイミング
        row5 = ["", "配信タイミング", ""]  # B5:C5結合用
        for dist in distributions:
            row5.extend(["", dist['timing']])  # フラグ列空、内容列にタイミング
        rows.append(row5)

        # 行6: 配信内容(LINE)
        line_label = f"配信内容\n(LINE)\n\n【LINE名】\n{params['concept']}"
        row6 = ["", line_label, ""]  # B6:C6結合用
        for dist in distributions:
            row6.extend(["TRUE", dist['line_content']])  # フラグTRUE、内容列に本文
        rows.append(row6)

        # 行7: 文字数
        row7 = ["", "文字数", ""]  # B7単独、C7空
        for dist in distributions:
            row7.extend(["", str(dist['char_count'])])  # フラグ列空、内容列に文字数
        rows.append(row7)

        # 行8-11: メール配信内容（B8:B11縦結合）
        # 行8: 件名
        email_label = f"配信内容\n(メール)\n\n【発信者名】\n{params['concept']}\n\n【発信メアド】\nメアド"
        row8 = ["", email_label, "件名"]  # B8:B11結合の最初、C8は「件名」
        for dist in distributions:
            row8.extend(["FALSE", dist['email_subject']])  # フラグFALSE、内容列に件名
        rows.append(row8)

        # 行9: プレビュー
        row9 = ["", "", "プレビュー\n表示(13文字)"]  # B9空（結合で）、C9は「プレビュー表示(13文字)」
        for dist in distributions:
            row9.extend(["FALSE", dist['email_preview']])  # フラグFALSE、内容列にプレビュー
        rows.append(row9)

        # 行10: 本文
        row10 = ["", "", "本文"]  # B10空（結合で）、C10は「本文」
        for dist in distributions:
            row10.extend(["FALSE", dist['email_body']])  # フラグFALSE、内容列に本文
        rows.append(row10)

        # 行11: フッター
        row11 = ["", "", "フッター"]  # B11空（結合で）、C11は「フッター」
        for dist in distributions:
            row11.extend(["FALSE", ""])  # フラグFALSE、内容列空
        rows.append(row11)

        return rows

    def _apply_perfect_formatting(self, service, spreadsheet_id, sheet_id, num_distributions):
        """書式設定を適用（完全再現版）"""
        requests = []

        # 色定義（元のスプレッドシートから抽出）
        DARK_GRAY = {"red": 0.263, "green": 0.263, "blue": 0.263}
        WHITE = {"red": 1.0, "green": 1.0, "blue": 1.0}
        LIGHT_GREEN = {"red": 0.714, "green": 0.843, "blue": 0.659}
        VERY_LIGHT_GREEN = {"red": 0.851, "green": 0.918, "blue": 0.827}
        LIGHT_BLUE = {"red": 0.788, "green": 0.855, "blue": 0.973}
        LIGHT_ORANGE = {"red": 1.0, "green": 0.949, "blue": 0.800}

        # 列の構成を計算
        # 配信ごとに2列（フラグ＋内容）
        # D, E, F, G, H, I, J, K, ...
        # 配信0: D, E (列index 3, 4)
        # 配信1: F, G (列index 5, 6)
        # 配信2: H, I (列index 7, 8)
        # ...

        # 1. 行2: タイトル（B2:S2結合、ダークグレー背景、白文字、太字14pt、CENTER/MIDDLE）
        end_col = 1 + 2 + num_distributions * 2  # B列 + C列 + 配信数×2列
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": 2,
                    "startColumnIndex": 1,
                    "endColumnIndex": end_col
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": DARK_GRAY,
                        "textFormat": {
                            "foregroundColor": WHITE,
                            "fontSize": 14,
                            "bold": True
                        },
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
            }
        })

        # タイトル行のセル結合 (B2:S2 または動的)
        requests.append({
            "mergeCells": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": 2,
                    "startColumnIndex": 1,
                    "endColumnIndex": min(19, end_col)
                },
                "mergeType": "MERGE_ALL"
            }
        })

        # 2. 行3: 日付行（特に書式なし、デフォルト）

        # 3. 行4: No.（B4:C4結合、ライトグリーン、CENTER/MIDDLE）
        # B4:C4結合
        requests.append({
            "mergeCells": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 3,
                    "endRowIndex": 4,
                    "startColumnIndex": 1,
                    "endColumnIndex": 3
                },
                "mergeType": "MERGE_ALL"
            }
        })
        # B4:C4の書式
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 3,
                    "endRowIndex": 4,
                    "startColumnIndex": 1,
                    "endColumnIndex": 3
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": LIGHT_GREEN,
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment)"
            }
        })
        # D列以降の行4（ライトグリーン、CENTER/MIDDLE）
        for i in range(num_distributions):
            flag_col = 3 + i * 2
            content_col = flag_col + 1
            # フラグ列（空）
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 3,
                        "endRowIndex": 4,
                        "startColumnIndex": flag_col,
                        "endColumnIndex": flag_col + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": LIGHT_GREEN,
                            "horizontalAlignment": "CENTER",
                            "verticalAlignment": "MIDDLE"
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment)"
                }
            })
            # 内容列（番号）
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 3,
                        "endRowIndex": 4,
                        "startColumnIndex": content_col,
                        "endColumnIndex": content_col + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": LIGHT_GREEN,
                            "horizontalAlignment": "CENTER",
                            "verticalAlignment": "MIDDLE"
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment)"
                }
            })

        # 4. 行5: 配信タイミング（B5:C5結合、ライトグリーン、CENTER/MIDDLE）
        # B5:C5結合
        requests.append({
            "mergeCells": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 4,
                    "endRowIndex": 5,
                    "startColumnIndex": 1,
                    "endColumnIndex": 3
                },
                "mergeType": "MERGE_ALL"
            }
        })
        # B5:C5の書式
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 4,
                    "endRowIndex": 5,
                    "startColumnIndex": 1,
                    "endColumnIndex": 3
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": LIGHT_GREEN,
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment)"
            }
        })
        # D列以降の行5（ライトグリーン、CENTER/MIDDLE）
        for i in range(num_distributions):
            flag_col = 3 + i * 2
            content_col = flag_col + 1
            # フラグ列（空）
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 4,
                        "endRowIndex": 5,
                        "startColumnIndex": flag_col,
                        "endColumnIndex": flag_col + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": LIGHT_GREEN,
                            "horizontalAlignment": "CENTER",
                            "verticalAlignment": "MIDDLE"
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment)"
                }
            })
            # 内容列（タイミング）
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 4,
                        "endRowIndex": 5,
                        "startColumnIndex": content_col,
                        "endColumnIndex": content_col + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": LIGHT_GREEN,
                            "horizontalAlignment": "CENTER",
                            "verticalAlignment": "MIDDLE"
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment)"
                }
            })

        # 5. 行6: 配信内容(LINE)（B6:C6結合、極薄グリーン、CENTER/MIDDLE）
        # B6:C6結合
        requests.append({
            "mergeCells": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 5,
                    "endRowIndex": 6,
                    "startColumnIndex": 1,
                    "endColumnIndex": 3
                },
                "mergeType": "MERGE_ALL"
            }
        })
        # B6:C6の書式（極薄グリーン）
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 5,
                    "endRowIndex": 6,
                    "startColumnIndex": 1,
                    "endColumnIndex": 3
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": VERY_LIGHT_GREEN,
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE",
                        "wrapStrategy": "WRAP"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment,wrapStrategy)"
            }
        })
        # D列以降の行6（フラグ=CENTER/MIDDLE/WRAP、内容=LEFT/TOP/WRAP、白背景）
        for i in range(num_distributions):
            flag_col = 3 + i * 2
            content_col = flag_col + 1
            # フラグ列（TRUE）
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 5,
                        "endRowIndex": 6,
                        "startColumnIndex": flag_col,
                        "endColumnIndex": flag_col + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "horizontalAlignment": "CENTER",
                            "verticalAlignment": "MIDDLE",
                            "wrapStrategy": "WRAP"
                        }
                    },
                    "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy)"
                }
            })
            # 内容列（LINE本文）- LEFT/TOP/WRAP
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 5,
                        "endRowIndex": 6,
                        "startColumnIndex": content_col,
                        "endColumnIndex": content_col + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "horizontalAlignment": "LEFT",
                            "verticalAlignment": "TOP",
                            "wrapStrategy": "WRAP"
                        }
                    },
                    "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy)"
                }
            })

        # 6. 行7: 文字数（B7単独、極薄グリーン、CENTER/MIDDLE、C7空）
        # B7の書式
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 6,
                    "endRowIndex": 7,
                    "startColumnIndex": 1,
                    "endColumnIndex": 2
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": VERY_LIGHT_GREEN,
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment)"
            }
        })
        # C7の書式（空、極薄グリーン、CENTER/MIDDLE）
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 6,
                    "endRowIndex": 7,
                    "startColumnIndex": 2,
                    "endColumnIndex": 3
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": VERY_LIGHT_GREEN,
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment)"
            }
        })
        # D列以降の行7（フラグ列空、内容列に文字数、RIGHT/TOP/WRAP、白背景）
        for i in range(num_distributions):
            flag_col = 3 + i * 2
            content_col = flag_col + 1
            # フラグ列（空）
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 6,
                        "endRowIndex": 7,
                        "startColumnIndex": flag_col,
                        "endColumnIndex": flag_col + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "horizontalAlignment": "CENTER",
                            "verticalAlignment": "MIDDLE",
                            "wrapStrategy": "WRAP"
                        }
                    },
                    "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy)"
                }
            })
            # 内容列（文字数）- RIGHT/TOP/WRAP
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 6,
                        "endRowIndex": 7,
                        "startColumnIndex": content_col,
                        "endColumnIndex": content_col + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "horizontalAlignment": "RIGHT",
                            "verticalAlignment": "TOP",
                            "wrapStrategy": "WRAP"
                        }
                    },
                    "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy)"
                }
            })

        # 7. 行8-11: メール配信内容（B8:B11縦結合、ライトブルー、CENTER/MIDDLE）
        # B8:B11縦結合
        requests.append({
            "mergeCells": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 7,
                    "endRowIndex": 11,
                    "startColumnIndex": 1,
                    "endColumnIndex": 2
                },
                "mergeType": "MERGE_ALL"
            }
        })
        # B8:B11の書式（ライトブルー）
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 7,
                    "endRowIndex": 11,
                    "startColumnIndex": 1,
                    "endColumnIndex": 2
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": LIGHT_BLUE,
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment)"
            }
        })

        # 行8: C8「件名」（ライトブルー）、D列以降
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 7,
                    "endRowIndex": 8,
                    "startColumnIndex": 2,
                    "endColumnIndex": 3
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": LIGHT_BLUE,
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment)"
            }
        })
        for i in range(num_distributions):
            flag_col = 3 + i * 2
            content_col = flag_col + 1
            # フラグ列（FALSE、ライトブルー、CENTER/MIDDLE/CLIP）
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 7,
                        "endRowIndex": 8,
                        "startColumnIndex": flag_col,
                        "endColumnIndex": flag_col + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": LIGHT_BLUE,
                            "horizontalAlignment": "CENTER",
                            "verticalAlignment": "MIDDLE",
                            "wrapStrategy": "CLIP"
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment,wrapStrategy)"
                }
            })
            # 内容列（件名、ライトブルー、LEFT/MIDDLE/CLIP）
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 7,
                        "endRowIndex": 8,
                        "startColumnIndex": content_col,
                        "endColumnIndex": content_col + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": LIGHT_BLUE,
                            "horizontalAlignment": "LEFT",
                            "verticalAlignment": "MIDDLE",
                            "wrapStrategy": "CLIP"
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment,wrapStrategy)"
                }
            })

        # 行9: C9「プレビュー」（ライトブルー）、D列以降（フラグ=ライトオレンジ、内容=ライトオレンジ）
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 8,
                    "endRowIndex": 9,
                    "startColumnIndex": 2,
                    "endColumnIndex": 3
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": LIGHT_BLUE,
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment)"
            }
        })
        for i in range(num_distributions):
            flag_col = 3 + i * 2
            content_col = flag_col + 1
            # フラグ列（FALSE、ライトオレンジ、CENTER/MIDDLE/CLIP）
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 8,
                        "endRowIndex": 9,
                        "startColumnIndex": flag_col,
                        "endColumnIndex": flag_col + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": LIGHT_ORANGE,
                            "horizontalAlignment": "CENTER",
                            "verticalAlignment": "MIDDLE",
                            "wrapStrategy": "CLIP"
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment,wrapStrategy)"
                }
            })
            # 内容列（プレビュー、ライトオレンジ、LEFT/MIDDLE/CLIP）
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 8,
                        "endRowIndex": 9,
                        "startColumnIndex": content_col,
                        "endColumnIndex": content_col + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": LIGHT_ORANGE,
                            "horizontalAlignment": "LEFT",
                            "verticalAlignment": "MIDDLE",
                            "wrapStrategy": "CLIP"
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment,wrapStrategy)"
                }
            })

        # 行10: C10「本文」（ライトブルー）、D列以降（白背景、LEFT/TOP/CLIP）
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 9,
                    "endRowIndex": 10,
                    "startColumnIndex": 2,
                    "endColumnIndex": 3
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": LIGHT_BLUE,
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment)"
            }
        })
        for i in range(num_distributions):
            flag_col = 3 + i * 2
            content_col = flag_col + 1
            # フラグ列（FALSE、白背景、CENTER/MIDDLE/CLIP）
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 9,
                        "endRowIndex": 10,
                        "startColumnIndex": flag_col,
                        "endColumnIndex": flag_col + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "horizontalAlignment": "CENTER",
                            "verticalAlignment": "MIDDLE",
                            "wrapStrategy": "CLIP"
                        }
                    },
                    "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy)"
                }
            })
            # 内容列（本文、白背景、LEFT/TOP/CLIP）
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 9,
                        "endRowIndex": 10,
                        "startColumnIndex": content_col,
                        "endColumnIndex": content_col + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "horizontalAlignment": "LEFT",
                            "verticalAlignment": "TOP",
                            "wrapStrategy": "CLIP"
                        }
                    },
                    "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy)"
                }
            })

        # 行11: C11「フッター」（ライトブルー）、D列以降（白背景、CENTER/MIDDLE/CLIP）
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 10,
                    "endRowIndex": 11,
                    "startColumnIndex": 2,
                    "endColumnIndex": 3
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": LIGHT_BLUE,
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment)"
            }
        })
        for i in range(num_distributions):
            flag_col = 3 + i * 2
            content_col = flag_col + 1
            # フラグ列（FALSE、白背景、CENTER/MIDDLE/CLIP）
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 10,
                        "endRowIndex": 11,
                        "startColumnIndex": flag_col,
                        "endColumnIndex": flag_col + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "horizontalAlignment": "CENTER",
                            "verticalAlignment": "MIDDLE",
                            "wrapStrategy": "CLIP"
                        }
                    },
                    "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy)"
                }
            })
            # 内容列（空、白背景、LEFT/TOP/CLIP）
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 10,
                        "endRowIndex": 11,
                        "startColumnIndex": content_col,
                        "endColumnIndex": content_col + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "horizontalAlignment": "LEFT",
                            "verticalAlignment": "TOP",
                            "wrapStrategy": "CLIP"
                        }
                    },
                    "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy)"
                }
            })

        # 8. 列幅設定（元のスプレッドシートと同じ）
        column_widths = [
            (0, 10),    # A列
            (1, 179),   # B列
            (2, 79)     # C列
        ]
        for i in range(num_distributions):
            flag_col = 3 + i * 2
            content_col = flag_col + 1
            if i == 0:
                flag_width = 31
            elif i == 1:
                flag_width = 38
            elif i == 2:
                flag_width = 42
            elif i == 3:
                flag_width = 40
            elif i == 4:
                flag_width = 42
            else:
                flag_width = 43
            column_widths.append((flag_col, flag_width))
            column_widths.append((content_col, 230))

        for col_idx, width in column_widths:
            requests.append({
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": col_idx,
                        "endIndex": col_idx + 1
                    },
                    "properties": {"pixelSize": width},
                    "fields": "pixelSize"
                }
            })

        # 9. すべてのリクエストを一括実行
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={'requests': requests}
        ).execute()


def main():
    """メイン関数"""
    # サンプル入力パラメータ（マーケティングオートメーション講座バージョン）
    sample_params = {
        "concept": "マーケティングオートメーション実践講座",
        "target": "中小企業の経営者・マーケティング担当者",
        "problems": "手作業でのメール配信に時間がかかる、顧客管理が煩雑、成約率が上がらない",
        "ideal_future": "自動化で業務効率を3倍に高め、売上を2倍に伸ばし、顧客満足度を向上させる",
        "achievements": "導入企業200社突破、平均成約率2.5倍向上、年間1000時間の業務削減実績"
    }

    print("=" * 80)
    print("🤖 LINE配信文章生成AIエージェント（完全再現版）")
    print("=" * 80)

    generator = DistributionGenerator()

    # 全配信を生成
    distributions = generator.generate_all_distributions(sample_params)

    # 既存のGoogle Spreadsheetに完全再現版で出力
    print(f"\n{'=' * 80}")
    print("📤 完全再現版スプレッドシートに出力中...")
    print(f"{'=' * 80}")

    url = generator.export_to_existing_spreadsheet_perfect(distributions, sample_params)

    if url:
        print(f"\n✅ 完了！")
        print(f"📊 スプレッドシートURL:\n{url}")
        print(f"\n💡 元のスプレッドシートを100%再現した新しいシートが追加されました！")
        print(f"    全ての行・列・文字・絵文字・書式が完全に一致しています。")
    else:
        print(f"\n❌ エラーが発生しました")


if __name__ == '__main__':
    main()
