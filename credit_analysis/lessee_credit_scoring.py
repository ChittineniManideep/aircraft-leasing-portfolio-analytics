"""
Lessee airline credit risk scoring — a simplified internal credit score for
each lessee airline in the portfolio, built from the financial/operational
metrics a lessor's credit team actually looks at: leverage, profitability,
scale, payment history, and state-ownership as a (imperfect but real)
support-risk proxy.

This isn't a claim to replicate a rating agency's methodology — it's a
transparent, defensible scoring framework of the kind a junior analyst
would be asked to build and explain, weighted and documented so every
score traces back to a specific input.
"""
import pandas as pd
import numpy as np

lessees = pd.read_csv("data/lessee_airlines.csv")

def normalize(series, invert=False):
    s = (series - series.min()) / (series.max() - series.min())
    return 1 - s if invert else s

# Each factor normalized 0-1, weighted, summed into a 0-100 score.
# Weights reflect what actually drives default/restructuring risk in
# airline credit: leverage and profitability dominate; scale, tenure,
# and payment history are secondary but real signals.
lessees["score_leverage"] = normalize(lessees.debt_to_ebitda, invert=True) * 30       # lower leverage = better
lessees["score_profitability"] = normalize(lessees.operating_margin_pct) * 25          # higher margin = better
lessees["score_scale"] = normalize(lessees.fleet_size) * 10                            # larger fleet = more resilient
lessees["score_load_factor"] = normalize(lessees.load_factor_pct) * 10                 # utilization efficiency
lessees["score_payment_history"] = normalize(lessees.on_time_lease_payment_history_pct) * 15
lessees["score_tenure"] = normalize(lessees.years_in_operation) * 5
lessees["score_state_support"] = lessees.state_owned * 5                               # state ownership as support proxy, not a guarantee

lessees["credit_score"] = (
    lessees.score_leverage + lessees.score_profitability + lessees.score_scale
    + lessees.score_load_factor + lessees.score_payment_history
    + lessees.score_tenure + lessees.score_state_support
).round(1)

def risk_band(score):
    if score >= 70:
        return "Investment-Grade Equivalent"
    elif score >= 50:
        return "Stable Sub-Investment Grade"
    elif score >= 30:
        return "Elevated Risk — Watch List"
    else:
        return "High Risk — Enhanced Monitoring"

lessees["risk_band"] = lessees.credit_score.apply(risk_band)

output_cols = [
    "lessee_airline", "lessee_region", "fleet_size", "debt_to_ebitda",
    "operating_margin_pct", "load_factor_pct", "on_time_lease_payment_history_pct",
    "state_owned", "credit_score", "risk_band",
]
lessees[output_cols].sort_values("credit_score", ascending=False).to_csv(
    "credit_analysis/lessee_credit_scores.csv", index=False
)

print(lessees.risk_band.value_counts())
print(f"\nPortfolio exposure by risk band (aircraft count):")
fleet = pd.read_csv("data/fleet_and_leases.csv")
exposure = fleet.merge(lessees[["lessee_airline", "risk_band"]], on="lessee_airline")
print(exposure.risk_band.value_counts())
