#!/usr/bin/env python3
"""
LINE配信文章生成Webアプリ（Streamlit版）- GORGEOUS EDITION
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

# 🌟 GORGEOUS DESIGN with NEON GLOW & HIGH CONTRAST ✨
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700;900&display=swap');

    /* 🎨 Dark Elegant Background with LINE Green Gradient */
    .stApp {
        background: linear-gradient(135deg, #001a0d 0%, #003d1f 50%, #00522a 100%);
        font-family: 'Noto Sans JP', sans-serif;
    }

    /* 🌟 All text WHITE for maximum contrast */
    .stApp, p, span, label, div {
        color: #FFFFFF !important;
    }

    /* ✨ GLOWING Neon Headers */
    h1 {
        color: #FFFFFF !important;
        font-weight: 900 !important;
        font-size: 2.8em !important;
        text-shadow:
            0 0 20px rgba(6, 199, 85, 1),
            0 0 40px rgba(6, 199, 85, 0.8),
            0 0 60px rgba(6, 199, 85, 0.6),
            0 4px 20px rgba(0, 0, 0, 0.8);
        animation: titleGlow 3s ease-in-out infinite alternate;
        letter-spacing: 1px;
    }

    @keyframes titleGlow {
        0% {
            text-shadow:
                0 0 20px rgba(6, 199, 85, 1),
                0 0 40px rgba(6, 199, 85, 0.8),
                0 0 60px rgba(6, 199, 85, 0.6);
        }
        50% {
            text-shadow:
                0 0 30px rgba(6, 199, 85, 1),
                0 0 60px rgba(6, 199, 85, 1),
                0 0 90px rgba(6, 199, 85, 0.8);
        }
        100% {
            text-shadow:
                0 0 40px rgba(6, 199, 85, 1),
                0 0 80px rgba(6, 199, 85, 1),
                0 0 120px rgba(6, 199, 85, 1);
        }
    }

    h2 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.8em !important;
        text-shadow: 0 0 20px rgba(6, 199, 85, 0.8), 0 2px 8px rgba(0,0,0,0.5);
        margin-top: 30px !important;
    }

    h3 {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 1.3em !important;
        text-shadow: 0 0 15px rgba(6, 199, 85, 0.6);
    }

    /* 💎 GORGEOUS Sparkling Button with Rainbow Shimmer */
    .stButton>button {
        background: linear-gradient(135deg, #06C755 0%, #00ff7f 50%, #06C755 100%) !important;
        background-size: 200% 200% !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 24px 48px !important;
        font-weight: 900 !important;
        font-size: 1.4em !important;
        box-shadow:
            0 0 30px rgba(6, 199, 85, 0.8),
            0 0 60px rgba(6, 199, 85, 0.6),
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255,255,255,0.3) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
        animation: shimmer 3s ease-in-out infinite, pulse 2s ease-in-out infinite !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

    @keyframes shimmer {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes pulse {
        0%, 100% {
            box-shadow:
                0 0 30px rgba(6, 199, 85, 0.8),
                0 0 60px rgba(6, 199, 85, 0.6),
                0 8px 32px rgba(0, 0, 0, 0.4);
        }
        50% {
            box-shadow:
                0 0 50px rgba(6, 199, 85, 1),
                0 0 100px rgba(6, 199, 85, 0.8),
                0 12px 48px rgba(0, 0, 0, 0.5);
        }
    }

    /* ✨ Sparkle Effect on Button */
    .stButton>button::before {
        content: '✨' !important;
        position: absolute !important;
        top: 50% !important;
        left: -30px !important;
        transform: translateY(-50%) !important;
        font-size: 1.5em !important;
        animation: sparkleMove 2s ease-in-out infinite !important;
    }

    .stButton>button::after {
        content: '✨' !important;
        position: absolute !important;
        top: 50% !important;
        right: -30px !important;
        transform: translateY(-50%) !important;
        font-size: 1.5em !important;
        animation: sparkleMove 2s ease-in-out infinite 1s !important;
    }

    @keyframes sparkleMove {
        0%, 100% { opacity: 0; transform: translateY(-50%) scale(0.5); }
        50% { opacity: 1; transform: translateY(-50%) scale(1.2); }
    }

    .stButton>button:hover {
        transform: translateY(-6px) scale(1.05) !important;
        box-shadow:
            0 0 60px rgba(6, 199, 85, 1),
            0 0 120px rgba(6, 199, 85, 0.8),
            0 16px 64px rgba(0, 0, 0, 0.6) !important;
    }

    .stButton>button:active {
        transform: translateY(-2px) scale(0.98) !important;
    }

    /* 📝 WIDE & COMFORTABLE Input Fields - WHITE background for maximum readability */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 3px solid rgba(6, 199, 85, 0.4) !important;
        border-radius: 16px !important;
        padding: 20px 24px !important;
        font-size: 1.1em !important;
        line-height: 1.8 !important;
        color: #000000 !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
        box-shadow:
            0 4px 16px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255,255,255,0.8) !important;
        min-height: 150px !important;
    }

    .stTextInput>div>div>input {
        min-height: 60px !important;
    }

    .stTextArea>div>div>textarea {
        min-height: 200px !important;
    }

    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #06C755 !important;
        box-shadow:
            0 0 0 4px rgba(6, 199, 85, 0.3),
            0 0 30px rgba(6, 199, 85, 0.6),
            0 8px 32px rgba(0, 0, 0, 0.3) !important;
        background: rgba(255, 255, 255, 1) !important;
        transform: translateY(-3px) !important;
    }

    /* 🏷️ Bold WHITE Labels */
    .stTextInput>label,
    .stTextArea>label {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.2em !important;
        margin-bottom: 12px !important;
        text-shadow: 0 0 10px rgba(6, 199, 85, 0.6), 0 2px 4px rgba(0,0,0,0.5);
        display: block !important;
    }

    /* 🎨 Glowing Card Container */
    [data-testid="stForm"] {
        background: linear-gradient(135deg,
            rgba(0, 60, 30, 0.85) 0%,
            rgba(0, 40, 20, 0.85) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 32px !important;
        padding: 48px !important;
        box-shadow:
            0 0 60px rgba(6, 199, 85, 0.4),
            0 20px 80px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255,255,255,0.1) !important;
        border: 2px solid rgba(6, 199, 85, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    /* ✨ Animated Border Glow */
    [data-testid="stForm"]::before {
        content: '' !important;
        position: absolute !important;
        top: -2px !important;
        left: -2px !important;
        right: -2px !important;
        bottom: -2px !important;
        background: linear-gradient(45deg,
            transparent 0%,
            rgba(6, 199, 85, 0.6) 25%,
            rgba(0, 255, 127, 0.8) 50%,
            rgba(6, 199, 85, 0.6) 75%,
            transparent 100%) !important;
        border-radius: 32px !important;
        z-index: -1 !important;
        animation: borderGlow 4s linear infinite !important;
        background-size: 400% 400% !important;
    }

    @keyframes borderGlow {
        0% { background-position: 0% 50%; }
        100% { background-position: 400% 50%; }
    }

    /* 🌈 Gorgeous Sidebar with Glow */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg,
            rgba(0, 50, 25, 0.95) 0%,
            rgba(0, 30, 15, 0.95) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 2px solid rgba(6, 199, 85, 0.4) !important;
        box-shadow:
            4px 0 30px rgba(6, 199, 85, 0.3),
            inset -1px 0 0 rgba(6, 199, 85, 0.2) !important;
    }

    /* 💚 Success Messages with Sparkle */
    .stSuccess {
        background: linear-gradient(135deg,
            rgba(6, 199, 85, 0.2) 0%,
            rgba(0, 255, 127, 0.2) 100%) !important;
        border-left: 6px solid #06C755 !important;
        border-radius: 16px !important;
        padding: 20px !important;
        color: #FFFFFF !important;
        box-shadow:
            0 0 30px rgba(6, 199, 85, 0.4),
            0 4px 16px rgba(0, 0, 0, 0.3) !important;
        animation: successPulse 2s ease-in-out infinite !important;
    }

    @keyframes successPulse {
        0%, 100% {
            box-shadow:
                0 0 30px rgba(6, 199, 85, 0.4),
                0 4px 16px rgba(0, 0, 0, 0.3);
        }
        50% {
            box-shadow:
                0 0 50px rgba(6, 199, 85, 0.6),
                0 6px 24px rgba(0, 0, 0, 0.4);
        }
    }

    /* 📊 Glowing Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg,
            #06C755 0%,
            #00ff7f 50%,
            #06C755 100%) !important;
        background-size: 200% 100% !important;
        border-radius: 10px !important;
        box-shadow: 0 0 20px rgba(6, 199, 85, 0.8) !important;
        animation: progressGlow 2s ease-in-out infinite !important;
    }

    @keyframes progressGlow {
        0% {
            background-position: 0% 50%;
            box-shadow: 0 0 20px rgba(6, 199, 85, 0.8);
        }
        50% {
            background-position: 100% 50%;
            box-shadow: 0 0 40px rgba(6, 199, 85, 1);
        }
        100% {
            background-position: 0% 50%;
            box-shadow: 0 0 20px rgba(6, 199, 85, 0.8);
        }
    }

    /* 💎 Glowing Metrics Cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg,
            rgba(6, 199, 85, 0.15) 0%,
            rgba(0, 255, 127, 0.15) 100%) !important;
        padding: 28px !important;
        border-radius: 20px !important;
        border: 2px solid rgba(6, 199, 85, 0.4) !important;
        box-shadow:
            0 0 30px rgba(6, 199, 85, 0.3),
            0 8px 32px rgba(0, 0, 0, 0.4) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-6px) scale(1.03) !important;
        box-shadow:
            0 0 50px rgba(6, 199, 85, 0.6),
            0 12px 48px rgba(0, 0, 0, 0.5) !important;
    }

    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 900 !important;
        font-size: 2.5em !important;
        text-shadow: 0 0 20px rgba(6, 199, 85, 0.8);
    }

    /* 🎯 Gorgeous Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg,
            rgba(0, 60, 30, 0.7) 0%,
            rgba(0, 40, 20, 0.7) 100%) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 16px !important;
        border-left: 6px solid #06C755 !important;
        padding: 20px !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 20px rgba(6, 199, 85, 0.2) !important;
        transition: all 0.3s ease !important;
    }

    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg,
            rgba(6, 199, 85, 0.3) 0%,
            rgba(0, 255, 127, 0.2) 100%) !important;
        box-shadow: 0 6px 30px rgba(6, 199, 85, 0.4) !important;
        transform: translateX(6px) !important;
    }

    /* 🌟 Divider with Glow */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg,
            transparent 0%,
            rgba(6, 199, 85, 0.8) 50%,
            transparent 100%) !important;
        margin: 40px 0 !important;
        box-shadow: 0 0 20px rgba(6, 199, 85, 0.4) !important;
    }

    /* 🎨 Column Animation */
    [data-testid="column"] {
        animation: fadeInUp 0.8s ease-out !important;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>
""", unsafe_allow_html=True)

# ✨ GORGEOUS Title with Neon Glow
st.markdown("""
<div style='text-align: center; padding: 40px; background: linear-gradient(135deg, rgba(6, 199, 85, 0.3) 0%, rgba(0, 255, 127, 0.2) 100%); border-radius: 24px; margin-bottom: 40px; box-shadow: 0 0 60px rgba(6, 199, 85, 0.5), 0 12px 48px rgba(0, 0, 0, 0.6); border: 2px solid rgba(6, 199, 85, 0.5); backdrop-filter: blur(20px);'>
    <h1 style='color: white !important; font-size: 3em; margin: 0;'>
        💬 LINE配信文章生成AIエージェント ✨
    </h1>
    <p style='color: white; opacity: 0.95; margin-top: 16px; font-size: 1.3em; text-shadow: 0 2px 8px rgba(0,0,0,0.5);'>
        AIが自動生成する17本の配信文
    </p>
</div>
""", unsafe_allow_html=True)

# 説明
st.markdown("""
### 📝 使い方

1. **下記のフォームに情報を入力** - 広々とした入力欄で快適に入力できます
2. **「17本の配信文を生成する」ボタンをクリック** - キラキラ光るボタンです
3. **Google Spreadsheetへのリンクが表示されます** - 約1〜2分で完了

""")

st.markdown("---")

# サイドバー
with st.sidebar:
    st.markdown("### 📖 入力ガイド")
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
        concept = st.text_area(
            "💡 イベントのコンセプト",
            value="AI ALL STARS 未来トークセッション2026",
            help="イベントの名称やキャッチコピーを入力してください",
            height=200
        )

        target = st.text_area(
            "🎯 ターゲット",
            value="AI活用に興味がある起業家・フリーランス・ビジネスパーソン",
            help="想定する参加者層を具体的に入力してください",
            height=200
        )

        problems = st.text_area(
            "⚠️ 解決する課題",
            value="AIの導入方法がわからない、時間が足りない、最新情報についていけない",
            help="ターゲットが抱えている悩みや課題を入力してください",
            height=200
        )

    with col2:
        ideal_future = st.text_area(
            "🌟 理想の未来",
            value="AIを活用して労働時間を減らしながら売上を伸ばし、自由な働き方を実現する",
            help="イベント参加後の変化や得られる成果を入力してください",
            height=200
        )

        achievements = st.text_area(
            "🏆 実績・権威",
            value="累計40億円の起業家を含む、AI業界で革命を起こし続ける8人のトップランナーが集結",
            help="信頼性を示す実績や数字を入力してください",
            height=200
        )

    st.markdown("---")

    # 生成ボタン
    submitted = st.form_submit_button(
        "🚀 17本の配信文を生成する ✨",
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
                        height=250,
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
<div style='text-align: center; padding: 32px; background: linear-gradient(135deg, rgba(6, 199, 85, 0.2) 0%, rgba(0, 255, 127, 0.1) 100%); border-radius: 20px; margin-top: 40px; box-shadow: 0 0 40px rgba(6, 199, 85, 0.3); border: 2px solid rgba(6, 199, 85, 0.3); backdrop-filter: blur(10px);'>
    <p style='color: #FFFFFF; font-size: 1.4em; font-weight: 700; margin: 0; text-shadow: 0 0 20px rgba(6, 199, 85, 0.8);'>💬 LINE配信文章生成AIエージェント v2.0</p>
    <p style='color: #FFFFFF; margin-top: 12px; margin-bottom: 0; font-size: 1.1em; text-shadow: 0 2px 8px rgba(0,0,0,0.5);'>AIが17本の配信文を自動生成</p>
    <p style='color: #FFFFFF; font-size: 1em; margin-top: 16px; opacity: 0.9;'>
        <span style='margin: 0 12px;'>💬 LINE配信最適化</span>
        <span style='margin: 0 12px;'>📊 スプレッドシート自動出力</span>
        <span style='margin: 0 12px;'>⚡ 高速生成</span>
    </p>
</div>
""", unsafe_allow_html=True)
