"""
利益率90%でのクレジット追加販売価格の算出
"""

# コスト設定
api_cost_per_use = 0.38  # 円/回
target_profit_margin = 0.90  # 利益率90%

print("=" * 70)
print("【利益率90%でのクレジット追加販売価格】")
print("=" * 70)
print()
print(f"API単価: {api_cost_per_use}円/回")
print(f"目標利益率: {target_profit_margin * 100}%")
print()

# 計算式
print("計算式:")
print(f"  利益率 = (売価 - 原価) ÷ 売価")
print(f"  {target_profit_margin} = (売価 - 原価) ÷ 売価")
print(f"  売価 = 原価 ÷ (1 - {target_profit_margin})")
print(f"  売価 = 原価 ÷ {1 - target_profit_margin}")
print(f"  売価 = 原価 × {1 / (1 - target_profit_margin)}")
print()

# クレジット回数のオプション
credit_options = [10, 20, 30, 50, 100, 150, 200, 300, 500]

print("=" * 70)
print("【理論価格（利益率90%ちょうど）】")
print("=" * 70)
print()

print("| 回数  | 原価   | 理論売価 | 1回単価 |")
print("|------|--------|---------|---------|")

theoretical_prices = []
for uses in credit_options:
    cost = uses * api_cost_per_use
    theoretical_price = cost / (1 - target_profit_margin)
    per_use = theoretical_price / uses
    theoretical_prices.append((uses, cost, theoretical_price, per_use))
    print(f"| {uses:4d}回 | {cost:5.1f}円 | {theoretical_price:7.1f}円 | {per_use:6.1f}円 |")

print()

# 実用的な価格設定（100円単位に切り上げ）
print("=" * 70)
print("【実用価格（100円単位切り上げ）】")
print("=" * 70)
print()

import math

print("| 回数  | 原価   | 実用価格 | 実利益率 | 1回単価 | 原価の何倍 |")
print("|------|--------|---------|---------|---------|-----------|")

practical_prices = []
for uses in credit_options:
    cost = uses * api_cost_per_use
    theoretical_price = cost / (1 - target_profit_margin)

    # 100円単位に切り上げ
    practical_price = math.ceil(theoretical_price / 100) * 100

    # 実際の利益率を計算
    actual_profit_margin = ((practical_price - cost) / practical_price) * 100
    per_use = practical_price / uses
    cost_multiplier = practical_price / cost

    practical_prices.append((uses, cost, practical_price, actual_profit_margin, per_use))
    print(f"| {uses:4d}回 | {cost:5.1f}円 | {practical_price:6,d}円 | {actual_profit_margin:6.2f}% | {per_use:6.1f}円 | {cost_multiplier:5.1f}倍 |")

print()

# 500円単位バージョンも提示
print("=" * 70)
print("【実用価格（500円単位切り上げ）】")
print("=" * 70)
print()

print("| 回数  | 原価   | 実用価格 | 実利益率 | 1回単価 | 原価の何倍 |")
print("|------|--------|---------|---------|---------|-----------|")

for uses in credit_options:
    cost = uses * api_cost_per_use
    theoretical_price = cost / (1 - target_profit_margin)

    # 500円単位に切り上げ
    practical_price_500 = math.ceil(theoretical_price / 500) * 500

    # 実際の利益率を計算
    actual_profit_margin = ((practical_price_500 - cost) / practical_price_500) * 100
    per_use = practical_price_500 / uses
    cost_multiplier = practical_price_500 / cost

    print(f"| {uses:4d}回 | {cost:5.1f}円 | {practical_price_500:6,d}円 | {actual_profit_margin:6.2f}% | {per_use:6.1f}円 | {cost_multiplier:5.1f}倍 |")

print()

# 推奨価格設定
print("=" * 70)
print("【推奨価格設定】")
print("=" * 70)
print()

recommendations = [
    (10, 100, "お試し・少量追加"),
    (20, 100, "ちょい足し"),
    (30, 200, "週1回ペース"),
    (50, 200, "月末の追加需要"),
    (100, 500, "ヘビーユーザー向け"),
    (200, 1000, "大量追加"),
    (300, 1500, "プレミアムパック"),
    (500, 2000, "超大量パック"),
]

print("| 回数  | 推奨価格 | 原価   | 利益率  | 1回単価 | 用途               |")
print("|------|---------|--------|---------|---------|-------------------|")

for uses, price, purpose in recommendations:
    cost = uses * api_cost_per_use
    profit_margin = ((price - cost) / price) * 100
    per_use = price / uses
    print(f"| {uses:4d}回 | {price:6,d}円 | {cost:5.1f}円 | {profit_margin:6.2f}% | {per_use:6.1f}円 | {purpose:18s} |")

print()

# 前回提案との比較
print("=" * 70)
print("【前回提案との比較】")
print("=" * 70)
print()

previous_prices = [
    (10, 500),
    (50, 2000),
    (100, 3500),
    (200, 6500),
]

print("| 回数  | 前回価格 | 前回利益率 | 今回価格（90%） | 価格差  | 削減率 |")
print("|------|---------|-----------|---------------|--------|-------|")

for uses, prev_price in previous_prices:
    cost = uses * api_cost_per_use
    prev_margin = ((prev_price - cost) / prev_price) * 100

    # 今回の90%利益率価格（100円単位）
    theoretical_price = cost / (1 - target_profit_margin)
    new_price = math.ceil(theoretical_price / 100) * 100

    price_diff = prev_price - new_price
    reduction_rate = (price_diff / prev_price) * 100

    print(f"| {uses:4d}回 | {prev_price:6,d}円 | {prev_margin:8.2f}% | {new_price:12,d}円 | {price_diff:5,d}円 | {reduction_rate:5.1f}% |")

print()
print("⚠️ 前回提案（97-99%利益率）から大幅値下げになります")
print("   利益率を90%に下げることで、ユーザーにとってお得な価格設定になります")
print()

print("=" * 70)
print("【まとめ】")
print("=" * 70)
print()
print("利益率90%の場合、原価の10倍が理論価格となります。")
print("100円単位に切り上げると、実利益率は90-95%になります。")
print()
print("推奨:")
print("  - 小額パック（10-50回）: 100-200円")
print("  - 中額パック（100回）: 500円")
print("  - 大額パック（200-500回）: 1,000-2,000円")
print()
print("これにより前回提案より大幅に安く、ユーザーにとって購入しやすい価格になります。")
print("=" * 70)
