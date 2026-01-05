"""
無料サロン生500名の場合のコスト分析
総コスト1万円以内での適切な月間利用回数を算出
"""

# コスト設定
api_cost_per_use = 0.38  # 円/回
budget_total = 10000  # 円/月（予算上限）
free_users = 500  # 無料サロン生の人数

print("=" * 70)
print("【無料サロン生500名のコスト分析】")
print("=" * 70)
print()
print(f"無料サロン生数: {free_users}名")
print(f"総予算上限: {budget_total:,}円/月")
print(f"API単価: {api_cost_per_use}円/回")
print()

# インフラコストのシナリオ分析
scenarios = [
    ("シナリオ1: インフラ4,500円（100人時と同じ）", 4500),
    ("シナリオ2: インフラ6,000円（500人でやや増加）", 6000),
    ("シナリオ3: インフラ8,000円（500人で大幅増加）", 8000),
]

print("=" * 70)
print("【インフラコスト別シナリオ】")
print("=" * 70)
print()

results = []

for scenario_name, infra_cost in scenarios:
    print(f"{scenario_name}")
    print("-" * 70)
    print(f"  インフラコスト: {infra_cost:,}円/月")

    # API予算
    api_budget = budget_total - infra_cost
    print(f"  API予算: {api_budget:,}円/月")

    if api_budget <= 0:
        print(f"  ⚠️ インフラコストだけで予算オーバー！")
        print()
        continue

    # 総使用回数
    total_uses = int(api_budget / api_cost_per_use)
    print(f"  総使用可能回数: {total_uses:,}回/月")

    # 1人あたりの使用回数
    uses_per_user = total_uses / free_users
    uses_per_user_int = int(uses_per_user)

    print(f"  1人あたり: {uses_per_user:.1f}回/月 → {uses_per_user_int}回/月")

    # 実際のコスト
    actual_api_cost = uses_per_user_int * free_users * api_cost_per_use
    actual_total_cost = actual_api_cost + infra_cost

    print(f"  実際のAPIコスト: {actual_api_cost:,.0f}円/月")
    print(f"  実際の総コスト: {actual_total_cost:,.0f}円/月")
    print(f"  予算残: {budget_total - actual_total_cost:,.0f}円")
    print()

    results.append({
        'scenario': scenario_name,
        'infra': infra_cost,
        'uses': uses_per_user_int,
        'total_cost': actual_total_cost
    })

# 推奨設定
print("=" * 70)
print("【推奨設定】")
print("=" * 70)
print()

# 中間シナリオを推奨
recommended_infra = 6000
recommended_api_budget = budget_total - recommended_infra
recommended_total_uses = int(recommended_api_budget / api_cost_per_use)
recommended_uses_per_user = int(recommended_total_uses / free_users)

print(f"インフラコスト想定: {recommended_infra:,}円/月")
print(f"API予算: {recommended_api_budget:,}円/月")
print(f"推奨利用回数: **月{recommended_uses_per_user}回/人**")
print()

actual_api_cost = recommended_uses_per_user * free_users * api_cost_per_use
actual_total_cost = actual_api_cost + recommended_infra

print(f"実際のコスト:")
print(f"  API: {actual_api_cost:,.0f}円/月")
print(f"  インフラ: {recommended_infra:,}円/月")
print(f"  合計: {actual_total_cost:,.0f}円/月")
print()

print(f"1日あたりの使用頻度: {recommended_uses_per_user / 30:.1f}回/日")
print()

# 前回の15回との比較
print("=" * 70)
print("【前回提案（15回）との比較】")
print("=" * 70)
print()

previous_uses = 15
previous_api_cost_per_user = previous_uses * api_cost_per_use
previous_infra_per_user = 45  # 100人時の1人あたりインフラコスト

print(f"前回提案: 月{previous_uses}回/人")
print(f"  想定コスト（100人規模）: {previous_api_cost_per_user + previous_infra_per_user:.1f}円/人")
print(f"  500人での総コスト: {(previous_api_cost_per_user * 500) + recommended_infra:,.0f}円/月")
print()

print(f"今回提案: 月{recommended_uses_per_user}回/人")
print(f"  実際のコスト: {actual_total_cost:,.0f}円/月")
print()

if previous_uses > recommended_uses_per_user:
    reduction = previous_uses - recommended_uses_per_user
    print(f"⚠️ 500人規模では月{reduction}回削減が必要")
else:
    increase = recommended_uses_per_user - previous_uses
    print(f"✅ 500人規模では月{increase}回増やせます")

print()

# 比較表
print("=" * 70)
print("【500人規模での利用回数比較表】")
print("=" * 70)
print()

print("| 月間回数 | APIコスト | 総コスト（*1） | 予算内 | 1日あたり |")
print("|---------|----------|-------------|--------|----------|")

test_uses = [5, 8, 10, 12, 15, 20]
for uses in test_uses:
    api_cost = uses * free_users * api_cost_per_use
    total_cost = api_cost + recommended_infra
    is_ok = "✅" if total_cost <= budget_total else "❌"
    per_day = uses / 30
    print(f"| {uses:2d}回/人  | {api_cost:6.0f}円 | {total_cost:7.0f}円   | {is_ok}   | {per_day:4.1f}回  |")

print()
print("*1 インフラコスト6,000円を含む")
print()

print("=" * 70)
