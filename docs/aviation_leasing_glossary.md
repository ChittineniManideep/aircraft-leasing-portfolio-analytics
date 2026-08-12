# Aviation Leasing Domain Glossary
### Core concepts an aviation finance analyst works with day to day

| Term | Definition | Where it shows up in this project |
|---|---|---|
| **Operating lease** | The lessor retains ownership of the aircraft and residual value risk at lease end; the airline pays rent to use it — the dominant leasing structure in this industry (vs. finance lease, where risk/reward transfers to the lessee) | Entire portfolio structure |
| **Lease Rate Factor (LRF)** | Monthly lease rate as a % of the aircraft's value — the core pricing metric lessors quote and negotiate on | `fleet.lease_rate_factor` |
| **Lease yield** | Annual lease revenue as % of aircraft value — the realised return metric, distinct from LRF (a pricing input) | `financial_model/lease_economics.py` |
| **MSN (Manufacturer Serial Number)** | The unique identifier for a specific physical aircraft — used industry-wide instead of a generic asset ID | `aircraft_id` (MSN-prefixed) |
| **Maintenance Reserves (MR)** | Payments collected from the lessee (per flight hour/cycle) to cover future heavy maintenance events — held by the lessor and drawn down when maintenance occurs | `maintenance_reserve_usd_per_month` |
| **Redelivery** | The point at which an aircraft is returned to the lessor at lease end, subject to contractually defined return conditions | `reporting/lease_maturity_schedule.csv` |
| **End-of-Lease (EOL) conditions** | The technical condition (engine cycles remaining, airframe checks due, cosmetic state) the aircraft must be returned in — a major source of lessor/lessee dispute and a key underwriting consideration at lease inception | Noted as a scope boundary in `docs/aviation_leasing_glossary.md` — full EOL modelling is a technical/legal function beyond this project's financial scope |
| **Residual value** | The aircraft's estimated market value at lease end — central to lessor economics since it's realised either through re-leasing or sale | `portfolio_dcf.py` terminal value assumption |
| **Novation** | The legal transfer of a lease contract from one lessor (or lessee) to another, with the original party released from obligations | — |
| **Power-by-the-hour (PBH)** | A maintenance cost model where the operator pays a fixed rate per flight hour rather than for discrete maintenance events — common in engine maintenance contracts | — |
| **Widebody vs. narrowbody** | Aircraft size/mission category — widebodies (A350, 787) fly long-haul with higher asset values and typically longer lease terms; narrowbodies (A320neo family, 737 MAX) dominate short/medium-haul fleets | `aircraft_type`, drives pricing assumptions throughout |
| **Sale-and-leaseback (SLB)** | An airline sells an aircraft it owns to a lessor and immediately leases it back — a major aircraft acquisition channel for lessors, alongside direct order-book purchases | — |
| **Portfolio diversification (by region/lessee/type)** | Aviation lessors actively manage concentration risk across airline, country, and aircraft-type exposure — a single airline's distress can be absorbed if the portfolio is diversified, which is why lessors report exposure this way rather than asset-by-asset | `reporting/portfolio_scorecard_by_region.csv` |

## Note on scope

This project models the **financial and credit** side of aviation leasing. It does not model technical/legal domains that sit with specialist functions at a real lessor — aircraft records/technical due diligence, EOL condition negotiation, or the legal structuring of lease novations. That scope boundary is intentional: it's the honest line between what a junior finance/analytics hire would own versus what sits with technical and legal teams.
