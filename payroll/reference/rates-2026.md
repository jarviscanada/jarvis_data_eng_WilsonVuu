# 2026 payroll rates — Ontario employees

Source of truth: CRA **T4127 Payroll Deductions Formulas**, 122nd edition (Jan 1, 2026)
and 123rd edition (Jul 1, 2026). The July edition made **no Ontario changes**.
These numbers are mirrored in `scripts/payroll_calc.py` (dict `R`). Change both together.

## CPP (Canada Pension Plan)
| Item | 2026 |
|---|---|
| Employee rate (base 4.95% + first additional 1.00%) | 5.95% |
| Basic exemption | $3,500/yr (prorated per pay: $3,500 ÷ periods) |
| YMPE (earnings ceiling) | $74,600 |
| Max employee CPP | $4,230.45 |
| CPP2 rate (YMPE → YAMPE) | 4.00% |
| YAMPE | $85,000 |
| Max employee CPP2 | $416.00 |
| Employer | matches employee CPP and CPP2 |

Tax treatment: base CPP (4.95/5.95 of CPP) → non-refundable credit; the
enhanced part (1.00/5.95 of CPP + all CPP2) → deduction from income (factor F5).

Upcoming: Jan 1, 2027 base CPP employee rate drops 4.95% → 4.75% (announced Apr 28, 2026).

## EI (Employment Insurance, outside Quebec)
| Item | 2026 |
|---|---|
| Employee rate | 1.63% |
| Maximum insurable earnings | $68,900 |
| Max employee premium | $1,123.07 |
| Employer | 1.4 × employee (max $1,572.30) |

## Federal income tax
| Taxable income | Rate | Constant K |
|---|---|---|
| 0 – 58,523 | 14% | 0 |
| 58,523 – 117,045 | 20.5% | 3,804 |
| 117,045 – 181,440 | 26% | 10,241 |
| 181,440 – 258,482 | 29% | 15,685 |
| 258,482+ | 33% | 26,024 |

Basic personal amount $16,452 (phases down to $14,829 between $181,440 and $258,482).
Canada employment amount $1,501. Credits at 14%.

## Ontario income tax
| Taxable income | Rate | Constant KP |
|---|---|---|
| 0 – 53,891 | 5.05% | 0 |
| 53,891 – 107,785 | 9.15% | 2,210 |
| 107,785 – 150,000 | 11.16% | 4,376 |
| 150,000 – 220,000 | 12.16% | 5,876 |
| 220,000+ | 13.16% | 8,076 |

- Basic personal amount $12,989 (credit at 5.05%).
- Surtax: 20% of basic Ontario tax over $5,818 + 36% of basic Ontario tax over $7,446.
- Ontario tax reduction: 2 × ($300 + $554 per eligible dependant) − Ontario tax, floored at 0.
- Ontario Health Premium (by annual taxable income):

| Income | Premium |
|---|---|
| ≤ $20,000 | $0 |
| $20,000–36,000 | 6% of excess over $20,000, max $300 |
| $36,000–48,000 | $300 + 6% of excess over $36,000, max $450 |
| $48,000–72,000 | $450 + 25% of excess over $48,000, max $600 |
| $72,000–200,000 | $600 + 25% of excess over $72,000, max $750 |
| > $200,000 | $750 + 25% of excess over $200,000, max $900 |

## Per-pay formula (T4127 Option 1, simplified)
1. CPP = 5.95% × (gross − 3,500/P), capped at the annual max minus YTD.
2. EI = 1.63% × gross, capped at annual max minus YTD.
3. A (annual taxable income) = P × (gross − RRSP/RPP − union dues − F5).
4. Federal T1 = R×A − K − 14%×(TD1 claim) − 14%×(annualized base CPP + EI) − 14%×CEA.
5. Ontario T2 = basic Ontario tax + surtax − tax reduction + health premium.
6. Tax per pay = (T1 + T2) ÷ P.

## Ontario minimum wage (ESA)
General $17.95/hr and students under 18 $16.90/hr, effective Oct 1, 2026
(was $17.60 / $16.60). Adjusted every Oct 1 by Ontario CPI.
