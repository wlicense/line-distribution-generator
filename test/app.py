#!/usr/bin/env python3
"""
LINE配信文章生成Webアプリ（Streamlit版）
"""

import streamlit as st
import os
from distribution_generator_perfect import DistributionGeneratorPerfect

# ページ設定
st.set_page_config(
    page_title="LINE配信文章生成AIエージェント",
    page_icon="🤖",
    layout="wide"
)

# タイトル
st.title("🤖 LINE配信文章生成AIエージェント")
st.markdown("---")

# 説明
st.markdown("""
### 📝 使い方
1. 下記のフォームにイベント情報を入力してください
2. 「17本の配信文を生成する」ボタンをクリック
3. 生成が完了すると、Google Spreadsheetへのリンクが表示されます

**所要時間**: 約1〜2分（17本すべて生成）
""")

st.markdown("---")

# サイドバーで環境変数の設定状況を表示
with st.sidebar:
    st.header("⚙️ 設定状況")

    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if anthropic_key and anthropic_key.startswith("sk-ant-"):
        st.success("✅ ANTHROPIC_API_KEY: 設定済み")
    else:
        st.error("❌ ANTHROPIC_API_KEY: 未設定")
        st.info("環境変数 `ANTHROPIC_API_KEY` を設定してください")

    st.markdown("---")
    st.markdown("### 📖 ガイド")
    st.markdown("""
    **コンセプト**: イベントの名称やキャッチコピー

    **ターゲット**: 想定する参加者層

    **解決する課題**: ターゲットが抱える悩み

    **理想の未来**: イベント参加後の変化

    **実績**: 権威性や信頼性を示す数字
    """)

# メインフォーム
st.header("📋 イベント情報を入力")

with st.form("event_params"):
    col1, col2 = st.columns(2)

    with col1:
        concept = st.text_input(
            "イベントのコンセプト *",
            value="AI ALL STARS 未来トークセッション2026",
            help="イベントの名称やキャッチコピーを入力"
        )

        target = st.text_area(
            "ターゲット *",
            value="AI活用に興味がある起業家・フリーランス・ビジネスパーソン",
            help="想定する参加者層を具体的に入力",
            height=100
        )

        problems = st.text_area(
            "解決する課題 *",
            value="AIの導入方法がわからない、時間が足りない、最新情報についていけない",
            help="ターゲットが抱えている悩みや課題を入力",
            height=100
        )

    with col2:
        ideal_future = st.text_area(
            "理想の未来 *",
            value="AIを活用して労働時間を減らしながら売上を伸ばし、自由な働き方を実現する",
            help="イベント参加後の変化や得られる成果を入力",
            height=100
        )

        achievements = st.text_area(
            "実績・権威 *",
            value="累計40億円の起業家を含む、AI業界で革命を起こし続ける8人のトップランナーが集結",
            help="信頼性を示す実績や数字を入力",
            height=100
        )

    st.markdown("---")

    # 生成ボタン
    submitted = st.form_submit_button(
        "🚀 17本の配信文を生成する",
        type="primary",
        use_container_width=True
    )

# 生成処理
if submitted:
    # バリデーション
    if not all([concept, target, problems, ideal_future, achievements]):
        st.error("❌ すべての項目を入力してください")
    elif not os.environ.get("ANTHROPIC_API_KEY"):
        st.error("❌ ANTHROPIC_API_KEY が設定されていません")
    else:
        # パラメータをまとめる
        params = {
            "concept": concept,
            "target": target,
            "problems": problems,
            "ideal_future": ideal_future,
            "achievements": achievements
        }

        # 進捗表示
        st.markdown("---")
        st.header("🔄 生成中...")

        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # ジェネレーターを初期化
            generator = DistributionGeneratorPerfect()

            # 配信文を生成
            status_text.text("📝 17本の配信文を生成中...")
            distributions = []

            for i in range(17):
                progress_bar.progress((i + 1) / 17)
                status_text.text(f"📝 配信{i}を生成中... ({generator.timings[i]})")

                try:
                    dist = generator.generate_distribution(params, i)
                    distributions.append(dist)
                except Exception as e:
                    st.warning(f"⚠️ 配信{i}でエラー: {e}")
                    # エラーでも続行

            progress_bar.progress(1.0)
            status_text.text("✅ 17本の配信文生成完了！")

            # スプレッドシートに出力
            st.text("📤 スプレッドシートに書き込み中...")
            spreadsheet_url = generator.export_to_existing_spreadsheet_perfect(distributions, params)

            # 完了メッセージ
            st.success("✅ すべての処理が完了しました！")

            # 結果表示
            st.markdown("---")
            st.header("📊 生成結果")

            # スプレッドシートリンク
            st.markdown(f"### 📎 [スプレッドシートを開く]({spreadsheet_url})")

            # 統計情報
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("生成数", f"{len(distributions)}本")
            with col2:
                avg_chars = sum(d['char_count'] for d in distributions) / len(distributions)
                st.metric("平均文字数", f"{int(avg_chars)}文字")
            with col3:
                total_chars = sum(d['char_count'] for d in distributions)
                st.metric("総文字数", f"{total_chars}文字")

            # 配信一覧
            st.markdown("### 📝 生成された配信一覧")
            for dist in distributions:
                with st.expander(f"配信{dist['distribution_number']}: {dist['timing']} ({dist['char_count']}文字)"):
                    st.text_area(
                        "LINE配信文",
                        dist['line_content'],
                        height=200,
                        key=f"line_{dist['distribution_number']}"
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        st.text_input(
                            "メール件名",
                            dist['email_subject'],
                            key=f"subject_{dist['distribution_number']}"
                        )
                    with col2:
                        st.text_input(
                            "プレビュー",
                            dist['email_preview'],
                            key=f"preview_{dist['distribution_number']}"
                        )

        except Exception as e:
            st.error(f"❌ エラーが発生しました: {e}")
            st.exception(e)

# フッター
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🤖 LINE配信文章生成AIエージェント v2.0</p>
    <p>Powered by Claude (Anthropic) & Streamlit</p>
</div>
""", unsafe_allow_html=True)
