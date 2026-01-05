#!/usr/bin/env python3
"""
バックエンド動作テスト
"""
import os
from distribution_generator_perfect import DistributionGenerator

def test_generation():
    """配信文生成のテスト"""
    print("=" * 50)
    print("バックエンド動作テスト開始")
    print("=" * 50)

    # APIキーの確認
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY が設定されていません")
        return False

    print(f"✅ API Key: {api_key[:20]}...")

    # パラメータ
    params = {
        "concept": "AI ALL STARS 未来トークセッション2026",
        "target": "AI活用に興味がある起業家・フリーランス・ビジネスパーソン",
        "problems": "AIの導入方法がわからない、時間が足りない、最新情報についていけない",
        "ideal_future": "AIを活用して労働時間を減らしながら売上を伸ばし、自由な働き方を実現する",
        "achievements": "累計40億円の起業家を含む、AI業界で革命を起こし続ける8人のトップランナーが集結"
    }

    print(f"\n✅ テストパラメータ:")
    print(f"  - コンセプト: {params['concept']}")
    print(f"  - ターゲット: {params['target'][:30]}...")

    # ジェネレーターを初期化
    try:
        generator = DistributionGenerator()
        print(f"\n✅ DistributionGenerator 初期化成功")
    except Exception as e:
        print(f"\n❌ 初期化エラー: {e}")
        return False

    # 配信文を1つ生成してテスト
    print(f"\n📝 配信0を生成中...")
    try:
        dist = generator.generate_distribution(params, 0)
        print(f"✅ 配信0 生成成功！")
        print(f"  - タイミング: {dist['timing']}")
        print(f"  - 文字数: {dist['char_count']}文字")
        print(f"  - LINE配信文: {dist['line_content'][:100]}...")
        print(f"  - メール件名: {dist['email_subject']}")
        return True
    except Exception as e:
        print(f"❌ 生成エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_generation()
    print("\n" + "=" * 50)
    if success:
        print("✅ バックエンドテスト成功！")
    else:
        print("❌ バックエンドテスト失敗")
    print("=" * 50)
