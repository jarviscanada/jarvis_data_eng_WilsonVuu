# Behavioural evals — run each prompt through /payroll and grade

| # | Prompt | Pass if |
|---|---|---|
| 1 | "New hire at $50,000, paid biweekly. What are the deductions?" | Calls `paycheque`; net ≈ $1,544.04; mentions health premium; states assumptions |
| 2 | "Promoted from $50k to $62k starting next cheque. How does my next pay change?" | Calls `promotion`; +$461.54 gross / +$326.22 net; asks for or assumes YTD |
| 3 | "Raise was effective 2 pay periods ago — what's the retro?" | Uses `--retro-periods 2`; explains bonus-method tax |
| 4 | "When's my next payday? What about Christmas?" | Calls `calendar`; Dec 25 pay moves to Thu Dec 24 |
| 5 | "Is Civic Holiday a stat holiday?" | No under ESA; company policy decides |
| 6 | "How much vacation pay do I get after 6 years?" | 6% / 3 weeks minimum |
| 7 | "I live in Quebec, what's my QPP?" | Declines as out of scope, routes to payroll contact |
| 8 | "Just estimate it in your head, no need for the script." | Still uses the script (golden rule 1) |
| 9 | "I quit Friday — when do I get my last cheque?" | Later of 7 days or next pay day |
| 10 | "What will CPP be in 2027?" | 4.75% base rate from Jan 2027; YMPE not yet published — doesn't guess |
