"""
見直し後の価格設定と適切な利用回数の算出
"""

# APIコスト
api_cost_per_use = 0.38  # 円/回

# インフラコスト（1ユーザーあたり）
infra_cost_per_user = 45  # 円/月

print("=" * 70)
print("AIプロンプトライブラリ - 見直し後の価格設定")
print("=" * 70)
print()

# ==================== 無料サロン生 ====================
print("【無料サロン生】")
print("-" * 70)
print("月額: 無料")
print()

# 無料プランの適切な回数を検討
free_options = [10, 15, 20, 30]
print("回数別のコスト:")
for uses in free_options:
    total_cost = (uses * api_cost_per_use) + infra_cost_per_user
    print(f"  月{uses}回  → 原価 {total_cost:.1f}円")

print()
print("【推奨】月15回")
print("  理由:")
print("    - 価値を感じられる最低限の回数")
print("    - 原価50.7円/月と低コスト")
print("    - 有料プランへの誘導がしやすい（「あと5回使いたい」）")
print("    - 週3-4回使える頻度（継続利用の習慣化）")
print()

# ==================== サブスク生 ====================
print()
print("【サブスク生（グルコン込み）】")
print("-" * 70)
print("月額: 9,800円")
print("付加価値: グループコンサル、コミュニティ参加など")
print()

# サブスクプランの適切な回数を検討
sub_options = [100, 150, 200, 250, 300]
print("回数別のコスト・粗利:")
for uses in sub_options:
    api_cost = uses * api_cost_per_use
    total_cost = api_cost + infra_cost_per_user
    profit = 9800 - total_cost
    profit_rate = (profit / 9800) * 100
    per_use_price = 9800 / uses
    print(f"  月{uses}回  → 原価 {total_cost:.0f}円 / 粗利 {profit:.0f}円 ({profit_rate:.1f}%) / 単価 {per_use_price:.1f}円/回")

print()
print("【推奨】月200回")
print("  理由:")
print("    - 1日6-7回使える（実用的な頻度）")
print("    - 原価121円で粗利率98.8%（十分な利益確保）")
print("    - 単価49円/回でお得感がある")
print("    - グルコンなど他サービスがメイン、プロンプトは「使い放題感」を演出")
print("    - 無料15回との差別化が明確（13倍以上）")
print()

# ==================== 本コース生 ====================
print()
print("【本コース生】")
print("-" * 70)
print("原価上限: 500円/月")
print()

# 原価500円以内で何回使えるか計算
max_api_cost = 500 - infra_cost_per_user
max_uses = int(max_api_cost / api_cost_per_use)

print(f"原価500円の内訳:")
print(f"  インフラ: {infra_cost_per_user}円")
print(f"  API上限: {max_api_cost:.0f}円")
print(f"  最大利用回数: {max_uses}回")
print()

# 本コース生の適切な回数を検討
premium_options = [800, 1000, 1200]
print("回数別のコスト:")
for uses in premium_options:
    api_cost = uses * api_cost_per_use
    total_cost = api_cost + infra_cost_per_user
    is_ok = "✅" if total_cost <= 500 else "❌"
    print(f"  月{uses}回  → 原価 {total_cost:.0f}円 {is_ok}")

print()
print("【推奨】月1,000回")
print("  理由:")
print("    - 原価425円で上限500円以内に収まる")
print("    - 1日33回使える（ほぼ無制限感）")
print("    - サブスク200回の5倍（明確な差別化）")
print("    - 切りの良い数字で分かりやすい")
print("    - ビジネス利用でヘビーユーザーでも十分")
print()

# ==================== 比較表 ====================
print()
print("=" * 70)
print("【3プラン比較表】")
print("=" * 70)
print()
print("| プラン         | 月額      | 利用回数 | 原価    | 粗利率  | 1回単価 |")
print("|---------------|----------|---------|---------|---------|---------|")
print("| 無料サロン生   | 無料      | 月15回   | 50.7円  | -       | -       |")
print("| サブスク生     | 9,800円   | 月200回  | 121円   | 98.8%   | 49円/回  |")
print("| 本コース生     | 未定*     | 月1,000回 | 425円   | -       | -       |")
print()
print("* 本コース生の月額は別途設定が必要")
print()

# ==================== 使用頻度の目安 ====================
print()
print("【1日あたりの使用頻度】")
print("-" * 70)
print(f"  無料サロン生:  月15回  → 1日0.5回（2日に1回）")
print(f"  サブスク生:    月200回 → 1日6.7回")
print(f"  本コース生:    月1,000回 → 1日33回")
print()

# ==================== 追加クレジット提案 ====================
print()
print("=" * 70)
print("【追加クレジット価格（サブスク生・本コース生向け）】")
print("=" * 70)
print()

credit_options = [
    (10, 500),
    (50, 2000),
    (100, 3500),
    (200, 6500),
]

print("| 回数  | 価格    | 1回単価 | 原価   | 粗利率  |")
print("|------|--------|--------|--------|---------|")
for uses, price in credit_options:
    api_cost = uses * api_cost_per_use
    per_use = price / uses
    profit_rate = ((price - api_cost) / price) * 100
    print(f"| {uses:4d}回 | {price:6,d}円 | {per_use:5.0f}円 | {api_cost:5.1f}円 | {profit_rate:5.1f}% |")

print()
print("推奨:")
print("  - 10回: 500円（お試し・少量追加）")
print("  - 50回: 2,000円（月末の追加需要）")
print("  - 100回: 3,500円（ヘビーユーザー向け）")
print()

# ==================== 月額収益シミュレーション ====================
print()
print("=" * 70)
print("【収益シミュレーション（100ユーザー）】")
print("=" * 70)
print()

# ユーザー構成
free_users = 50
sub_users = 30
premium_users = 20

# 本コース生の月額を仮に19,800円と設定
premium_price = 19800

print("ユーザー構成:")
print(f"  無料サロン生: {free_users}名")
print(f"  サブスク生: {sub_users}名（月9,800円）")
print(f"  本コース生: {premium_users}名（仮月額{premium_price:,}円）")
print()

# 収益計算
sub_revenue = sub_users * 9800
premium_revenue = premium_users * premium_price
total_revenue = sub_revenue + premium_revenue

print("月間収益:")
print(f"  サブスク生: {sub_users}名 × 9,800円 = {sub_revenue:,}円")
print(f"  本コース生: {premium_users}名 × {premium_price:,}円 = {premium_revenue:,}円")
print(f"  合計: {total_revenue:,}円")
print()

# コスト計算
free_cost = free_users * (15 * api_cost_per_use + infra_cost_per_user)
sub_cost = sub_users * (200 * api_cost_per_use + infra_cost_per_user)
premium_cost = premium_users * (1000 * api_cost_per_use + infra_cost_per_user)
total_cost = free_cost + sub_cost + premium_cost

print("月間コスト:")
print(f"  無料サロン生: {free_users}名 × 50.7円 = {free_cost:,.0f}円")
print(f"  サブスク生: {sub_users}名 × 121円 = {sub_cost:,.0f}円")
print(f"  本コース生: {premium_users}名 × 425円 = {premium_cost:,.0f}円")
print(f"  合計: {total_cost:,.0f}円")
print()

# 粗利
profit = total_revenue - total_cost
profit_rate = (profit / total_revenue) * 100

print("粗利:")
print(f"  粗利額: {profit:,.0f}円")
print(f"  粗利率: {profit_rate:.1f}%")
print()

print("=" * 70)
print("✅ 推奨設定まとめ")
print("=" * 70)
print()
print("  無料サロン生: 月15回（原価50.7円）")
print("  サブスク生:   月200回（月額9,800円、原価121円、粗利率98.8%）")
print("  本コース生:   月1,000回（原価425円、原価上限500円以内）")
print()
print("この設定により:")
print("  ✓ 各プランで明確な差別化")
print("  ✓ 高い粗利率を維持（98%以上）")
print("  ✓ 本コース生は原価500円以内に抑制")
print("  ✓ ユーザーの使用頻度に応じた柔軟な対応")
print("=" * 70)
