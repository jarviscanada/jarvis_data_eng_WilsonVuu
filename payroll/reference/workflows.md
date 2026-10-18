# Playbooks

## 1. New hire — "Starting at $50k, what comes off my cheque?"
Ask (only if missing): pay frequency (default to company.yaml), any RRSP/benefit/union
deductions, TD1 claims beyond basic.

Run: `python3 scripts/payroll_calc.py paycheque --salary 50000 --freq biweekly`

Example answer:
> **Net ≈ $1,544.04 every two weeks** on $1,923.08 gross.
> | Gross | CPP | EI | Federal tax | Ontario tax | Net |
> |---|---|---|---|---|---|
> | $1,923.08 | $106.41 | $31.35 | $153.27 | $88.01 | $1,544.04 |
> - Ontario tax includes the $600/yr Ontario Health Premium (~$23/cheque).
> - No CPP2: you're under the $74,600 YMPE.
> - Assumes basic TD1 claims and no benefit or RRSP deductions.

Mid-year hire: CPP basic exemption still applies per pay; annual maximums are not
prorated for EI. For TD1 claims, remind them to file TD1 and TD1ON in week one.

## 2. Promotion — "I got promoted to $62k effective next pay. What changes?"
Ask: old and new salary, effective date (vs pay periods already paid), and YTD gross,
CPP, EI from their latest stub (needed to tell whether a maximum will be hit).

Run: `... promotion --old 50000 --new 62000 --ytd-gross <G> --ytd-cpp <C> --ytd-ei <E>`
Add `--retro-periods N` if the raise is effective N periods in the past.

Explain:
- Gross +$461.54, net +$326.22 per cheque — about 71% of the raise reaches the
  cheque because the raise is taxed at the marginal rate (20.5% federal + 9.15%
  Ontario once over the first brackets) plus CPP and EI.
- Retro pay is a separate line taxed with the bonus method.
- If YTD + remaining pay crosses $68,900, EI stops partway through the year;
  likewise CPP at $74,600 — the cheque gets bigger in those final periods.

## 3. Payroll calendar — "When is my next pay? Is Christmas a problem?"
Run: `... calendar --from <today> --count 6`
Answer with the next date first, then the list. Call out any date moved for a
holiday/weekend, and the cutoff for changes.

## 4. Year-end questions (Nov–Jan)
- Last 2026 pay date and first 2027 pay date (calendar).
- CPP restarts on the first January cheque; 2027 base rate 4.75% (new YMPE TBD
  until CRA publishes the January 2027 T4127 — say so, don't guess).
- T4 slips are issued by end of February.

## Escalation triggers
Quebec or another province, federal employer, contractor/T4A, garnishments,
termination disputes, a stub that doesn't match the estimate by more than a few
dollars → explain what's likely and route to the payroll contact.
