"""
Synthetic aircraft leasing portfolio — fleet, lease contracts, and lessee
airlines, shaped like a real Dublin-based lessor's book (mixed narrowbody/
widebody, global lessee spread, staggered lease maturities).
"""
import numpy as np
import pandas as pd

np.random.seed(11)
N_AIRCRAFT = 120

aircraft_types = np.random.choice(
    ["A320neo", "A321neo", "B737 MAX 8", "A350-900", "B787-9"],
    N_AIRCRAFT, p=[0.30, 0.20, 0.25, 0.13, 0.12]
)
# Widebodies (A350/787) carry higher list price and longer lease terms
is_widebody = np.isin(aircraft_types, ["A350-900", "B787-9"])

list_price_usd_m = np.where(
    is_widebody,
    np.random.normal(120, 15, N_AIRCRAFT),
    np.random.normal(48, 8, N_AIRCRAFT),
).round(1)

aircraft_age_years = np.random.uniform(0.5, 12, N_AIRCRAFT).round(1)
lease_term_years = np.where(is_widebody,
                             np.random.uniform(8, 12, N_AIRCRAFT),
                             np.random.uniform(6, 10, N_AIRCRAFT)).round(1)

lessee_regions = np.random.choice(
    ["Europe", "North America", "Asia-Pacific", "Latin America", "Middle East"],
    N_AIRCRAFT, p=[0.28, 0.15, 0.32, 0.15, 0.10]
)
lessee_airlines = [f"Airline-{r[:3].upper()}-{np.random.randint(1,25):02d}" for r in lessee_regions]

# Lease Rate Factor (LRF) — monthly lease rate as a % of aircraft value.
# Typical range ~0.6%-0.9% for modern narrowbody/widebody on 8-10yr leases.
base_lrf = np.where(is_widebody, 0.0068, 0.0075)
lrf = np.clip(np.random.normal(base_lrf, 0.0008, N_AIRCRAFT), 0.005, 0.011)

monthly_lease_rate_usd = (list_price_usd_m * 1_000_000 * lrf).round(0)

fleet = pd.DataFrame({
    "aircraft_id": [f"MSN{60000+i}" for i in range(N_AIRCRAFT)],
    "aircraft_type": aircraft_types,
    "list_price_usd_m": list_price_usd_m,
    "aircraft_age_years": aircraft_age_years,
    "lease_term_years": lease_term_years,
    "lease_rate_factor": lrf.round(5),
    "monthly_lease_rate_usd": monthly_lease_rate_usd,
    "lessee_airline": lessee_airlines,
    "lessee_region": lessee_regions,
    "lease_start_year": np.random.choice(range(2019, 2025), N_AIRCRAFT),
    "maintenance_reserve_usd_per_month": (monthly_lease_rate_usd * np.random.uniform(0.12, 0.22, N_AIRCRAFT)).round(0),
})
fleet["lease_end_year"] = fleet.lease_start_year + fleet.lease_term_years.round(0).astype(int)

# --- Lessee airline financial profile (drives credit scoring) ---
unique_lessees = fleet[["lessee_airline", "lessee_region"]].drop_duplicates().reset_index(drop=True)
n_lessees = len(unique_lessees)

unique_lessees["fleet_size"] = np.random.randint(15, 220, n_lessees)
unique_lessees["load_factor_pct"] = np.clip(np.random.normal(81, 6, n_lessees), 60, 95).round(1)
unique_lessees["debt_to_ebitda"] = np.clip(np.random.gamma(3, 1.2, n_lessees), 0.8, 12).round(2)
unique_lessees["operating_margin_pct"] = np.clip(np.random.normal(7, 6, n_lessees), -15, 22).round(1)
unique_lessees["state_owned"] = np.random.choice([1, 0], n_lessees, p=[0.20, 0.80])
unique_lessees["years_in_operation"] = np.random.randint(2, 60, n_lessees)
unique_lessees["on_time_lease_payment_history_pct"] = np.clip(
    np.random.normal(96, 5, n_lessees), 60, 100
).round(1)

fleet.to_csv("data/fleet_and_leases.csv", index=False)
unique_lessees.to_csv("data/lessee_airlines.csv", index=False)

print(f"aircraft: {len(fleet)} rows")
print(f"lessee airlines: {len(unique_lessees)} rows")
