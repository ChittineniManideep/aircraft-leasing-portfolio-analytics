# Aircraft Leasing Portfolio Analytics
### A simulated fleet + lease portfolio for an aircraft lessor — financial modelling, lessee credit analysis, and portfolio reporting

## Why this project exists

Built to close the two real gaps in an otherwise strong application for a **junior aviation finance / leasing analyst** role in Dublin: aviation domain vocabulary and credit analysis. The financial modelling, Excel, Python/SQL, and reporting skills behind this were already proven — see the related [Real Estate FP&A project](../real-estate-fpa-modelling-project) for the DCF/IRR/NPV foundation this reuses.

| JD Requirement | Where it's addressed |
|---|---|
| Financial analysis / financial statements | `financial_model/lease_economics.py` — per-aircraft P&L, lease yield |
| Financial modelling — forecasts, investment analysis | `financial_model/portfolio_dcf.py` — 10-year portfolio DCF, IRR/NPV, Base/Bear/Bull scenarios |
| Excel — advanced modelling | `financial_model/lease_model_export.csv` — structured for direct Excel pivot/model use |
| Data analytics / Python / SQL | Whole repo — pandas-based modelling, structured like a SQL-ready fact table |
| Portfolio reporting, performance reporting | `reporting/portfolio_scorecard.csv` |
| **Aviation domain (leasing, aircraft, airline markets)** | `docs/aviation_leasing_glossary.md`, fleet/lease structure throughout |
| **Credit analysis (key skill)** | `credit_analysis/lessee_credit_scoring.py` |

## The simulated portfolio

A mid-size aircraft lessor's fleet: narrowbody and widebody aircraft (A320neo family, 737 MAX, A350, 787) on operating leases to airlines across Europe, Asia-Pacific, and Latin America — the actual shape of a Dublin-based lessor's book (AerCap, SMBC Aviation Capital, Avolon all run comparable global, multi-region portfolios).

## Repo structure

```
aircraft-leasing-portfolio-analytics/
├── README.md
├── data/
│   └── generate_leasing_portfolio.py     # Fleet, leases, lessee airlines
├── financial_model/
│   ├── lease_economics.py                # Per-aircraft lease yield, MR reserve accrual
│   └── portfolio_dcf.py                  # Portfolio-level DCF, IRR/NPV, 3 scenarios
├── credit_analysis/
│   └── lessee_credit_scoring.py          # Airline lessee credit risk scoring model
├── reporting/
│   └── portfolio_scorecard.csv           # Committee-ready portfolio KPIs
└── docs/
    └── aviation_leasing_glossary.md      # Lease rate factor, MR reserves, redelivery, EOL conditions, etc.
```
