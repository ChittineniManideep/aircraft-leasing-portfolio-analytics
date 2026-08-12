"""
Per-aircraft lease economics: annual lease yield, maintenance reserve
accrual, and a simplified operating P&L per aircraft — the building block
the portfolio DCF aggregates up from.
"""
import pandas as pd

fleet = pd.read_csv("data/fleet_and_leases.csv")

fleet["annual_lease_revenue_usd"] = fleet.monthly_lease_rate_usd * 12
fleet["annual_mr_reserve_usd"] = fleet.maintenance_reserve_usd_per_month * 12

# Lease yield: annual lease revenue as % of aircraft value — the headline
# metric lessors report per-asset and portfolio-wide (distinct from LRF,
# which is a pricing input; yield is the realised return metric)
fleet["lease_yield_pct"] = (
    fleet.annual_lease_revenue_usd / (fleet.list_price_usd_m * 1_000_000) * 100
).round(2)

# Simplified depreciation: straight-line to a 15% residual over a 25yr
# economic life, standard operating-lessor convention
fleet["annual_depreciation_usd"] = (
    fleet.list_price_usd_m * 1_000_000 * 0.85 / 25
).round(0)

# Simplified debt service: assume 70% LTV, 4.5% cost of debt, interest-only
# approximation for this model's purposes
fleet["annual_debt_service_usd"] = (
    fleet.list_price_usd_m * 1_000_000 * 0.70 * 0.045
).round(0)

fleet["net_operating_income_usd"] = (
    fleet.annual_lease_revenue_usd
    - fleet.annual_depreciation_usd
    - fleet.annual_debt_service_usd
)

output_cols = [
    "aircraft_id", "aircraft_type", "lessee_airline", "lessee_region",
    "list_price_usd_m", "lease_rate_factor", "annual_lease_revenue_usd",
    "lease_yield_pct", "annual_mr_reserve_usd", "annual_depreciation_usd",
    "annual_debt_service_usd", "net_operating_income_usd",
]
fleet[output_cols].to_csv("financial_model/lease_model_export.csv", index=False)

print(fleet.groupby("aircraft_type")[["lease_yield_pct", "net_operating_income_usd"]].mean().round(1))
print(f"\nPortfolio avg lease yield: {fleet.lease_yield_pct.mean():.2f}%")
print(f"Portfolio total annual lease revenue: ${fleet.annual_lease_revenue_usd.sum():,.0f}")
