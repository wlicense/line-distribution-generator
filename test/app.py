#!/usr/bin/env python3
"""
LINE配信文章生成Webアプリ（Streamlit版）
"""

import streamlit as st
import os
from distribution_generator_perfect import DistributionGenerator

# ページ設定
st.set_page_config(
    page_title="LINE配信文章生成AIエージェント",
    page_icon="💬",
    layout="wide"
)

# Beautiful LINE Design with Glassmorphism
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700;900&display=swap');

    /* Beautiful gradient background */
    .stApp {
        background: linear-gradient(135deg, #E8F8EF 0%, #F5FCFA 50%, #FFFFFF 100%);
        font-family: 'Noto Sans JP', sans-serif;
    }

    /* Beautiful headers with LINE colors */
    h1 {
        color: #06C755 !important;
        font-weight: 900 !important;
        text-shadow: 0 4px 12px rgba(6, 199, 85, 0.15);
        letter-spacing: -0.5px;
    }

    h2 {
        color: #00A300 !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px;
    }

    h3 {
        color: #00B900 !important;
        font-weight: 600 !important;
    }

    /* Beautiful glassmorphism button */
    .stButton>button {
        background: linear-gradient(135deg, #06C755 0%, #00B900 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 16px 32px !important;
        font-weight: 700 !important;
        font-size: 1.1em !important;
        box-shadow: 0 8px 32px rgba(6, 199, 85, 0.25),
                    0 4px 16px rgba(6, 199, 85, 0.15) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .stButton>button::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent) !important;
        transition: left 0.5s !important;
    }

    .stButton>button:hover::before {
        left: 100% !important;
    }

    .stButton>button:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 12px 48px rgba(6, 199, 85, 0.35),
                    0 8px 24px rgba(6, 199, 85, 0.2) !important;
    }

    .stButton>button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }

    /* Beautiful glassmorphism sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg,
            rgba(240, 249, 244, 0.95) 0%,
            rgba(255, 255, 255, 0.95) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border-right: none !important;
        box-shadow: 4px 0 24px rgba(6, 199, 85, 0.05) !important;
    }

    /* Beautiful success messages */
    .stSuccess {
        background: linear-gradient(135deg, #E8F8EF 0%, #F0FCF5 100%) !important;
        border-left: 5px solid #06C755 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        box-shadow: 0 4px 16px rgba(6, 199, 85, 0.1) !important;
        animation: slideInRight 0.5s ease-out !important;
    }

    /* Beautiful animated progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #06C755 0%, #00B900 100%) !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(6, 199, 85, 0.3) !important;
        animation: pulse 2s ease-in-out infinite !important;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }

    /* Beautiful input fields with glassmorphism */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(6, 199, 85, 0.15) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) !important;
    }

    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #06C755 !important;
        box-shadow: 0 0 0 4px rgba(6, 199, 85, 0.1),
                    0 4px 16px rgba(6, 199, 85, 0.15) !important;
        background: rgba(255, 255, 255, 1) !important;
        transform: translateY(-2px) !important;
    }

    /* Beautiful form labels */
    .stTextInput>label,
    .stTextArea>label {
        color: #00A300 !important;
        font-weight: 600 !important;
        font-size: 0.95em !important;
        margin-bottom: 8px !important;
    }

    /* Beautiful expander with glassmorphism */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg,
            rgba(240, 249, 244, 0.8) 0%,
            rgba(255, 255, 255, 0.8) 100%) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        border-left: 5px solid #06C755 !important;
        padding: 16px !important;
        box-shadow: 0 4px 16px rgba(6, 199, 85, 0.08) !important;
        transition: all 0.3s ease !important;
    }

    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg,
            rgba(240, 249, 244, 1) 0%,
            rgba(255, 255, 255, 1) 100%) !important;
        box-shadow: 0 6px 24px rgba(6, 199, 85, 0.12) !important;
        transform: translateX(4px) !important;
    }

    /* Beautiful metrics cards */
    [data-testid="stMetricValue"] {
        color: #06C755 !important;
        font-weight: 900 !important;
        font-size: 2em !important;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(135deg,
            rgba(255, 255, 255, 0.9) 0%,
            rgba(240, 249, 244, 0.9) 100%) !important;
        padding: 20px !important;
        border-radius: 16px !important;
        border: 2px solid rgba(6, 199, 85, 0.1) !important;
        box-shadow: 0 8px 24px rgba(6, 199, 85, 0.08) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 32px rgba(6, 199, 85, 0.15) !important;
    }

    /* Beautiful animations */
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Beautiful columns */
    [data-testid="column"] {
        animation: fadeIn 0.6s ease-out !important;
    }

    /* Beautiful form container */
    [data-testid="stForm"] {
        background: linear-gradient(135deg,
            rgba(255, 255, 255, 0.95) 0%,
            rgba(240, 249, 244, 0.95) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 24px !important;
        padding: 32px !important;
        box-shadow: 0 12px 48px rgba(6, 199, 85, 0.08),
                    0 0 1px rgba(6, 199, 85, 0.1) !important;
        border: 1px solid rgba(6, 199, 85, 0.1) !important;
    }

    /* Beautiful divider */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg,
            transparent 0%,
            rgba(6, 199, 85, 0.3) 50%,
            transparent 100%) !important;
        margin: 32px 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# タイトル
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #06C755 0%, #00B900 100%); border-radius: 16px; margin-bottom: 30px; box-shadow: 0 8px 24px rgba(6, 199, 85, 0.3);'>
    <h1 style='color: white !important; font-size: 2.5em; margin: 0; text-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
        💬 LINE配信文章生成AIエージェント
    </h1>
    <p style='color: white; opacity: 0.95; margin-top: 10px; font-size: 1.1em;'>
        AIが自動生成する17本の配信文
    </p>
</div>
""", unsafe_allow_html=True)

# 説明
st.markdown("""
### 📝 使い方
1. 下記のフォームにイベント情報を入力してください
2. 「17本の配信文を生成する」ボタンをクリック
3. 生成が完了すると、Google Spreadsheetへのリンクが表示されます

**所要時間**: 約1〜2分（17本すべて生成）
""")

st.markdown("---")

# サイドバー
with st.sidebar:
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
        st.error("❌ システム設定エラーが発生しました。管理者にお問い合わせください。")
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
            generator = DistributionGenerator()

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
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #F0F9F4 0%, #E8F8EF 100%); border-radius: 12px; margin-top: 30px;'>
    <p style='color: #06C755; font-size: 1.2em; font-weight: 600; margin: 0;'>💬 LINE配信文章生成AIエージェント v2.0</p>
    <p style='color: #00A300; margin-top: 8px; margin-bottom: 0;'>AIが17本の配信文を自動生成</p>
    <p style='color: #888; font-size: 0.9em; margin-top: 8px;'>
        <span style='margin: 0 8px;'>💬 LINE配信最適化</span>
        <span style='margin: 0 8px;'>📊 スプレッドシート自動出力</span>
        <span style='margin: 0 8px;'>⚡ 高速生成</span>
    </p>
</div>
""", unsafe_allow_html=True)
