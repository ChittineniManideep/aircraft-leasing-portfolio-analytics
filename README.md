# Aircraft Leasing Portfolio Analytics
### A simulated fleet + lease portfolio for an aircraft lessor — financial modelling, lessee credit analysis, and portfolio reporting

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
