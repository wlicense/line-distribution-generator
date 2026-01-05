#!/usr/bin/env python3
"""
Google Sheets出力テスト
"""
import os
from distribution_generator_perfect import DistributionGenerator

def test_sheets_output():
    """Google Sheets出力のテスト"""
    print("=" * 50)
    print("Google Sheets出力テスト開始")
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

    # ジェネレーターを初期化
    try:
        generator = DistributionGenerator()
        print(f"✅ DistributionGenerator 初期化成功")
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")
        return False

    # 3つの配信文を生成
    print(f"\n📝 3つの配信文を生成中...")
    distributions = []
    for i in range(3):
        try:
            print(f"  配信{i}を生成中...")
            dist = generator.generate_distribution(params, i)
            distributions.append(dist)
            print(f"  ✅ 配信{i} 完了（{dist['char_count']}文字）")
        except Exception as e:
            print(f"  ❌ 配信{i}でエラー: {e}")
            return False

    # Google Sheetsに出力
    print(f"\n📤 Google Sheetsに出力中...")
    try:
        url = generator.export_to_existing_spreadsheet_perfect(distributions, params)
        print(f"✅ スプレッドシート出力成功！")
        print(f"📎 URL: {url}")
        return True
    except Exception as e:
        print(f"❌ 出力エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_sheets_output()
    print("\n" + "=" * 50)
    if success:
        print("✅ Google Sheetsテスト成功！")
        print("ブラウザでスプレッドシートを確認してください")
    else:
        print("❌ Google Sheetsテスト失敗")
    print("=" * 50)
