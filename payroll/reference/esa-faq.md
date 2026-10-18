# Common employee pay questions — Ontario (Employment Standards Act, 2000)

Answer from this file; company-specific details come from `config/company.yaml`.
These are ESA *minimums* — the employment contract or policy may be more generous.

## Pay cycle
- **Pay day:** the employer must set a recurring pay period and pay day (ESA Part V).
  Use `payroll_calc.py calendar` for the actual dates and the company holiday rule.
- **Pay day on a holiday/weekend:** the company `holiday_rule` decides (default: pay
  the previous business day). The ESA allows the contract to define this.
- **Cutoff:** changes (raises, banking, TD1, address) must be in by the
  `payroll_cutoff` in company.yaml to make that cheque; otherwise next cycle.

## Pay statements
- A wage statement is required on or before each pay day: pay period, rate, gross,
  each deduction and its purpose, and net. It may be electronic if the employee can print it.

## Vacation
| Service | Minimum time | Minimum vacation pay |
|---|---|---|
| < 5 years | 2 weeks | 4% of gross wages |
| 5+ years | 3 weeks | 6% of gross wages |
- Vacation pay is earned on all wages (incl. commissions/most bonuses, excluding vacation pay itself).
- Paid before the vacation is taken, on each cheque (if agreed in writing, shown separately), or per company policy.

## Public holidays (9 under the ESA)
New Year's Day, Family Day, Good Friday, Victoria Day, Canada Day, Labour Day,
Thanksgiving, Christmas Day, Boxing Day.
- **Civic Holiday (Aug) and Easter Monday are not ESA holidays** — company policy decides.
- Public holiday pay = (regular wages + vacation pay in the 4 work weeks before the
  holiday week) ÷ 20.
- Working the holiday: regular pay + a substitute day off, or premium pay (1.5×) +
  public holiday pay, by agreement.

## Overtime
- Over 44 hours in a work week at 1.5× regular rate (unless exempt, e.g. many managers).
- Banked time off in lieu at 1.5 hours per OT hour only with a written agreement.

## Deductions from pay
- Only statutory (tax, CPP, EI), court-ordered (garnishments), or with the
  employee's written authorization naming a specific amount. Employers cannot deduct
  for shortages, breakage, or customers who walk out without paying.

## Leaving the company
- **Final pay** (wages, accrued vacation pay, termination/severance pay) is due by the
  later of 7 days after employment ends or the next regular pay day.
- Record of Employment (ROE) is issued for EI; final pay includes final T4 amounts.

## Minimum wage (from Oct 1, 2026)
General $17.95/hr; students under 18 working ≤ 28 h/week in school terms $16.90/hr.

## Escalate, don't answer
Disputes about unpaid wages, termination/severance entitlements, or misclassification
→ HR/payroll contact, or the Ontario Ministry of Labour ESA claims process.
