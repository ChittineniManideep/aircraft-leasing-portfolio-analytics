"""
Portfolio-level 10-year DCF with Bear/Base/Bull scenarios — same modelling
pattern as the real estate FP&A project (10yr cashflow, scenario toggle,
IRR/NPV), applied to an aircraft lease portfolio: lease revenue runs off
as leases mature/re-lease, offset by residual value realisation at end
of economic life.
"""
import numpy as np
import numpy_financial as npf
import pandas as pd

fleet = pd.read_csv("data/fleet_and_leases.csv")
portfolio_value_usd = (fleet.list_price_usd_m * 1_000_000).sum()
annual_lease_revenue = (fleet.monthly_lease_rate_usd * 12).sum()

YEARS = 10
DISCOUNT_RATE = 0.085  # portfolio-level WACC assumption for an aviation lessor

scenarios = {
    "Bear": {"re_lease_rate_decline": -0.15, "utilization": 0.90, "residual_haircut": -0.20},
    "Base": {"re_lease_rate_decline": -0.05, "utilization": 0.96, "residual_haircut": -0.10},
    "Bull": {"re_lease_rate_decline": 0.03, "utilization": 0.99, "residual_haircut": -0.05},
}

results = {}
for name, s in scenarios.items():
    cashflows = [-portfolio_value_usd]  # Year 0: portfolio acquisition outflow (illustrative)
    revenue = annual_lease_revenue
    for yr in range(1, YEARS + 1):
        # lease rates reset (decline/grow per scenario) roughly every 3 years on re-lease
        if yr % 3 == 0:
            revenue *= (1 + s["re_lease_rate_decline"])
        yr_cf = revenue * s["utilization"]
        cashflows.append(yr_cf)

    # Terminal value: residual aircraft value at end of year 10, haircut per scenario
    residual_value = portfolio_value_usd * 0.55 * (1 + s["residual_haircut"])  # ~55% base residual at yr10
    cashflows[-1] += residual_value

    irr = npf.irr(cashflows)
    npv = npf.npv(DISCOUNT_RATE, cashflows)
    results[name] = {
        "irr_pct": round(irr * 100, 2),
        "npv_usd_m": round(npv / 1_000_000, 1),
        "terminal_residual_usd_m": round(residual_value / 1_000_000, 1),
        "year1_cashflow_usd_m": round(cashflows[1] / 1_000_000, 1),
    }

scenario_df = pd.DataFrame(results).T
scenario_df.index.name = "scenario"
scenario_df.to_csv("financial_model/portfolio_dcf_scenarios.csv")

print(f"Portfolio acquisition value: ${portfolio_value_usd/1_000_000:,.1f}M")
print(f"Year 1 lease revenue: ${annual_lease_revenue/1_000_000:,.1f}M\n")
print(scenario_df.to_string())
