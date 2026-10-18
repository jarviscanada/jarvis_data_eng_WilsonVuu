#!/usr/bin/env python3
"""
Ontario payroll calculator — CRA T4127 "Option 1" formulas, 2026 rates.

The LLM never does payroll arithmetic itself; it calls this script.

Subcommands
  paycheque  Per-pay deductions for a salary (new hire, current pay).
  promotion  Before/after comparison for a raise, incl. optional retro pay.
  calendar   Upcoming pay dates for the company pay cycle, with stat holidays.

Examples
  python3 payroll_calc.py paycheque --salary 50000 --freq biweekly
  python3 payroll_calc.py promotion --old 50000 --new 62000 --freq biweekly \
      --ytd-gross 38461.60 --retro-periods 2
  python3 payroll_calc.py calendar --from 2026-10-13 --count 6

Add --json for machine-readable output.
Rates: reference/rates-2026.md (source: CRA T4127, 122nd/123rd editions).
"""
import argparse, json, sys
from datetime import date, timedelta
from pathlib import Path

# ---------------------------------------------------------------- 2026 rates
R = {
    "year": 2026,
    # CPP
    "cpp_rate": 0.0595, "cpp_base_rate": 0.0495, "cpp_first_add_rate": 0.0100,
    "ympe": 74_600.0, "basic_exemption": 3_500.0, "cpp_max": 4_230.45,
    "cpp_base_max": 3_519.45,
    "cpp2_rate": 0.04, "yampe": 85_000.0, "cpp2_max": 416.00,
    # EI (outside Quebec)
    "ei_rate": 0.0163, "mie": 68_900.0, "ei_max": 1_123.07,
    # Federal
    "fed_brackets": [(0, 0.14, 0), (58_523, 0.205, 3_804), (117_045, 0.26, 10_241),
                     (181_440, 0.29, 15_685), (258_482, 0.33, 26_024)],
    "fed_low_rate": 0.14, "bpaf_max": 16_452.0, "bpaf_min": 14_829.0,
    "bpaf_phase_start": 181_440.0, "bpaf_phase_end": 258_482.0, "cea": 1_501.0,
    # Ontario
    "on_brackets": [(0, 0.0505, 0), (53_891, 0.0915, 2_210), (107_785, 0.1116, 4_376),
                    (150_000, 0.1216, 5_876), (220_000, 0.1316, 8_076)],
    "on_low_rate": 0.0505, "on_bpa": 12_989.0,
    "on_surtax": [(5_818.0, 0.20), (7_446.0, 0.36)],
    "on_s2": 300.0, "on_y_per_dependant": 554.0,
}
FREQ = {"weekly": 52, "biweekly": 26, "semimonthly": 24, "monthly": 12}


def bracket(a, table):
    rate, const = table[0][1], table[0][2]
    for threshold, r, k in table:
        if a >= threshold:
            rate, const = r, k
    return rate, const


def bpaf(net_income):
    if net_income <= R["bpaf_phase_start"]:
        return R["bpaf_max"]
    if net_income >= R["bpaf_phase_end"]:
        return R["bpaf_min"]
    span = R["bpaf_phase_end"] - R["bpaf_phase_start"]
    return R["bpaf_max"] - (net_income - R["bpaf_phase_start"]) * (R["bpaf_max"] - R["bpaf_min"]) / span


def ohp(a):
    """Ontario Health Premium (V2) on annual taxable income A."""
    if a <= 20_000: return 0.0
    if a <= 36_000: return min(300.0, 0.06 * (a - 20_000))
    if a <= 48_000: return min(450.0, 300 + 0.06 * (a - 36_000))
    if a <= 72_000: return min(600.0, 450 + 0.25 * (a - 48_000))
    if a <= 200_000: return min(750.0, 600 + 0.25 * (a - 72_000))
    return min(900.0, 750 + 0.25 * (a - 200_000))


def r2(x):
    return round(x + 1e-9, 2)


def cpp_for_period(pi, p, ytd_pi=0.0, ytd_cpp=0.0, ytd_cpp2=0.0, pm=12):
    max_c = R["cpp_max"] * pm / 12
    c = max(0.0, min(max_c - ytd_cpp, R["cpp_rate"] * (pi - R["basic_exemption"] / p)))
    # CPP2: earnings between YMPE and YAMPE (cumulative)
    lo = max(R["ympe"], ytd_pi)
    hi = min(R["yampe"], ytd_pi + pi)
    c2 = max(0.0, min(R["cpp2_max"] - ytd_cpp2, R["cpp2_rate"] * max(0.0, hi - lo)))
    return r2(c), r2(c2)


def ei_for_period(ie, ytd_ei=0.0):
    return r2(max(0.0, min(R["ei_max"] - ytd_ei, R["ei_rate"] * ie)))


def annual_tax(a, p, c, ei, tc=None, tcp=None, dependants=0, k3=0.0, k3p=0.0):
    """Returns (federal T1, ontario T2 breakdown) on annualized income A."""
    tc = bpaf(a) if tc is None else tc
    tcp = R["on_bpa"] if tcp is None else tcp
    base_cpp_annual = min(p * c * (R["cpp_base_rate"] / R["cpp_rate"]), R["cpp_base_max"])
    ei_annual = min(p * ei, R["ei_max"])
    # federal
    rate, k = bracket(a, R["fed_brackets"])
    k1 = R["fed_low_rate"] * tc
    k2 = R["fed_low_rate"] * base_cpp_annual + R["fed_low_rate"] * ei_annual
    k4 = min(R["fed_low_rate"] * a, R["fed_low_rate"] * R["cea"])
    t3 = max(0.0, rate * a - k - k1 - k2 - k3 - k4)
    t1 = t3
    # ontario
    v, kp = bracket(a, R["on_brackets"])
    k1p = R["on_low_rate"] * tcp
    k2p = R["on_low_rate"] * base_cpp_annual + R["on_low_rate"] * ei_annual
    t4 = max(0.0, v * a - kp - k1p - k2p - k3p)
    v1 = sum(rt * max(0.0, t4 - th) for th, rt in R["on_surtax"])
    v2 = ohp(a)
    s = max(0.0, min(t4 + v1, 2 * (R["on_s2"] + R["on_y_per_dependant"] * dependants) - (t4 + v1)))
    t2 = max(0.0, t4 + v1 - s) + v2
    return t1, {"basic": t4, "surtax": v1, "tax_reduction": s, "health_premium": v2, "total": t2}


def paycheque(salary, freq, ytd_pi=0.0, ytd_cpp=0.0, ytd_cpp2=0.0, ytd_ei=0.0,
              rrsp_rpp=0.0, union_dues=0.0, dependants=0, tc=None, tcp=None,
              extra_tax=0.0, vacation_pay_pct=0.0):
    p = FREQ[freq]
    gross = salary / p
    vac = gross * vacation_pay_pct
    i = gross + vac
    c, c2 = cpp_for_period(i, p, ytd_pi, ytd_cpp, ytd_cpp2)
    ei = ei_for_period(i, ytd_ei)
    f5 = c * (R["cpp_first_add_rate"] / R["cpp_rate"]) + c2
    a = max(0.0, p * (i - rrsp_rpp - f5 - union_dues))
    # K2 note: if CPP/EI is capped this period, use the annual maximum
    c_for_k2 = R["cpp_max"] / p if (ytd_cpp + c >= R["cpp_max"] - 0.005 and ytd_cpp > 0) else c
    ei_for_k2 = R["ei_max"] / p if (ytd_ei + ei >= R["ei_max"] - 0.005 and ytd_ei > 0) else ei
    t1, on = annual_tax(a, p, c_for_k2, ei_for_k2, tc, tcp, dependants)
    fed = r2(t1 / p); prov = r2(on["total"] / p)
    tax = r2(fed + prov + extra_tax)
    deductions = r2(c + c2 + ei + tax + rrsp_rpp + union_dues)
    return {
        "inputs": {"annual_salary": salary, "frequency": freq, "periods_per_year": p},
        "gross_pay": r2(i),
        "cpp": c, "cpp2": c2, "ei": ei,
        "federal_tax": fed, "ontario_tax": prov, "income_tax_total": tax,
        "other_deductions": r2(rrsp_rpp + union_dues),
        "total_deductions": deductions,
        "net_pay": r2(i - deductions),
        "annualized_taxable_income": r2(a),
        "ontario_breakdown_annual": {k: r2(v) for k, v in on.items()},
        "employer_cost": {"cpp_match": r2(c + c2), "ei_1_4x": r2(ei * 1.4)},
    }


def bonus_tax(salary, freq, bonus, ytd_bonus=0.0, dependants=0):
    """T4127 non-periodic method: tax on (annual income + bonus) minus tax without it."""
    base = paycheque(salary, freq, dependants=dependants)
    p = FREQ[freq]
    a = base["annualized_taxable_income"]
    c = base["cpp"]; ei = base["ei"]
    c_b = R["cpp_rate"] * bonus; ei_b = R["ei_rate"] * bonus
    t1a, ona = annual_tax(a + ytd_bonus, p, c, ei, dependants=dependants)
    t1b, onb = annual_tax(a + ytd_bonus + bonus - c_b * (R["cpp_first_add_rate"] / R["cpp_rate"]),
                          p, c, ei, dependants=dependants)
    tax = r2((t1b + onb["total"]) - (t1a + ona["total"]))
    return {"gross": r2(bonus), "cpp_approx": r2(c_b), "ei_approx": r2(ei_b),
            "income_tax": tax, "net_approx": r2(bonus - c_b - ei_b - tax)}


def promotion(old, new, freq, ytd_pi=0.0, ytd_cpp=0.0, ytd_cpp2=0.0, ytd_ei=0.0,
              retro_periods=0, dependants=0):
    before = paycheque(old, freq, dependants=dependants)
    after = paycheque(new, freq, ytd_pi, ytd_cpp, ytd_cpp2, ytd_ei, dependants=dependants)
    out = {"before": before, "after_next_cheque": after,
           "delta_gross": r2(after["gross_pay"] - before["gross_pay"]),
           "delta_net": r2(after["net_pay"] - before["net_pay"])}
    p = FREQ[freq]
    if retro_periods:
        retro = (new - old) / p * retro_periods
        out["retro_pay"] = bonus_tax(new, freq, retro, dependants=dependants)
        out["retro_pay"]["periods"] = retro_periods
    # When will CPP / EI max out at the new salary?
    per = new / p
    out["ei_maxes_out"] = ytd_pi + per * remaining_periods_estimate(freq) >= R["mie"]
    out["cpp_maxes_out"] = ytd_pi + per * remaining_periods_estimate(freq) >= R["ympe"]
    return out


def remaining_periods_estimate(freq, today=None):
    today = today or date.today()
    days_left = (date(today.year, 12, 31) - today).days
    return max(0, round(days_left / (365 / FREQ[freq])))


# ---------------------------------------------------------------- calendar
def easter(y):
    a = y % 19; b, c = divmod(y, 100); d, e = divmod(b, 4)
    f = (b + 8) // 25; g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30; i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7; m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31; day = ((h + l - 7 * m + 114) % 31) + 1
    return date(y, month, day)


def nth_weekday(y, m, weekday, n):
    d = date(y, m, 1)
    d += timedelta(days=(weekday - d.weekday()) % 7)
    return d + timedelta(weeks=n - 1)


def ontario_holidays(y):
    """The 9 ESA public holidays + Civic Holiday (not statutory, but banks close)."""
    vic = date(y, 5, 24)  # Victoria Day: Monday before May 25
    while vic.weekday() != 0:
        vic -= timedelta(days=1)
    return {
        date(y, 1, 1): "New Year's Day",
        nth_weekday(y, 2, 0, 3): "Family Day",
        easter(y) - timedelta(days=2): "Good Friday",
        vic: "Victoria Day",
        date(y, 7, 1): "Canada Day",
        nth_weekday(y, 8, 0, 1): "Civic Holiday (not an ESA holiday; banks closed)",
        nth_weekday(y, 9, 0, 1): "Labour Day",
        nth_weekday(y, 10, 0, 2): "Thanksgiving Day",
        date(y, 12, 25): "Christmas Day",
        date(y, 12, 26): "Boxing Day",
    }


def load_company(path):
    cfg = {}
    p = Path(path)
    if p.exists():
        for line in p.read_text().splitlines():
            line = line.split("#", 1)[0].strip()
            if ":" in line:
                k, v = line.split(":", 1)
                cfg[k.strip()] = v.strip().strip('"')
    return cfg


def calendar(start, count, cfg):
    freq = cfg.get("pay_frequency", "biweekly")
    anchor = date.fromisoformat(cfg.get("anchor_pay_date", "2026-01-09"))
    rule = cfg.get("holiday_rule", "previous_business_day")
    lag = int(cfg.get("days_after_period_end", "6"))
    out = []
    if freq in ("weekly", "biweekly"):
        step = 7 if freq == "weekly" else 14
        d = anchor
        while d < start:
            d += timedelta(days=step)
        dates = [d + timedelta(days=step * n) for n in range(count)]
    else:
        days = [int(x) for x in cfg.get("semimonthly_days", "15,31").split(",")] if freq == "semimonthly" else [int(cfg.get("monthly_day", "31"))]
        dates, y, m = [], start.year, start.month
        while len(dates) < count:
            for dd in days:
                last = (date(y + (m // 12), m % 12 + 1, 1) - timedelta(days=1)).day
                cand = date(y, m, min(dd, last))
                if cand >= start and len(dates) < count:
                    dates.append(cand)
            m += 1
            if m > 12: m, y = 1, y + 1
    for d in dates:
        hol = {**ontario_holidays(d.year), **ontario_holidays(d.year + 1)}
        actual, notes = d, []
        while actual.weekday() >= 5 or actual in hol:
            if actual in hol: notes.append(f"{hol[actual]} on {actual}")
            actual += timedelta(days=-1 if rule == "previous_business_day" else 1)
        period_end = d - timedelta(days=lag)
        start_p = period_end - timedelta(days=(14 if freq == "biweekly" else 7) - 1) if freq in ("weekly", "biweekly") else None
        out.append({"scheduled": d.isoformat(), "actual_deposit": actual.isoformat(),
                    "weekday": actual.strftime("%A"),
                    "period": f"{start_p} to {period_end}" if start_p else None,
                    "moved": actual != d, "notes": notes})
    return {"frequency": freq, "holiday_rule": rule, "pay_dates": out}


# ---------------------------------------------------------------- CLI
def fmt_money(x):
    return f"${x:,.2f}"


def print_cheque(res, title):
    print(f"\n{title}")
    print(f"  Gross pay ............ {fmt_money(res['gross_pay'])}")
    for k, label in [("cpp", "CPP"), ("cpp2", "CPP2"), ("ei", "EI"),
                     ("federal_tax", "Federal tax"), ("ontario_tax", "Ontario tax (incl. health premium)")]:
        print(f"  {label:<20} - {fmt_money(res[k])}")
    if res["other_deductions"]:
        print(f"  Other (RRSP/dues)    - {fmt_money(res['other_deductions'])}")
    print(f"  Net pay .............. {fmt_money(res['net_pay'])}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    def common(sp):
        sp.add_argument("--freq", choices=FREQ, default="biweekly")
        sp.add_argument("--dependants", type=int, default=0, help="for Ontario tax reduction")
        sp.add_argument("--ytd-gross", type=float, default=0.0)
        sp.add_argument("--ytd-cpp", type=float, default=0.0)
        sp.add_argument("--ytd-cpp2", type=float, default=0.0)
        sp.add_argument("--ytd-ei", type=float, default=0.0)
        sp.add_argument("--json", action="store_true")
    pc = sub.add_parser("paycheque"); common(pc)
    pc.add_argument("--salary", type=float, required=True)
    pc.add_argument("--rrsp", type=float, default=0.0, help="per-pay RRSP/RPP deduction")
    pc.add_argument("--union-dues", type=float, default=0.0)
    pc.add_argument("--td1-federal", type=float, help="federal TD1 total claim (default: BPAF)")
    pc.add_argument("--td1-ontario", type=float, help="TD1ON total claim (default: 12,989)")
    pc.add_argument("--vacation-pay-on-cheque", type=float, default=0.0, help="e.g. 0.04")
    pr = sub.add_parser("promotion"); common(pr)
    pr.add_argument("--old", type=float, required=True)
    pr.add_argument("--new", type=float, required=True)
    pr.add_argument("--retro-periods", type=int, default=0)
    bo = sub.add_parser("bonus"); common(bo)
    bo.add_argument("--salary", type=float, required=True)
    bo.add_argument("--amount", type=float, required=True)
    ca = sub.add_parser("calendar")
    ca.add_argument("--from", dest="start", default=date.today().isoformat())
    ca.add_argument("--count", type=int, default=6)
    ca.add_argument("--company", default=str(Path(__file__).resolve().parent.parent / "config" / "company.yaml"))
    ca.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.cmd == "paycheque":
        res = paycheque(a.salary, a.freq, a.ytd_gross, a.ytd_cpp, a.ytd_cpp2, a.ytd_ei,
                        a.rrsp, a.union_dues, a.dependants, a.td1_federal, a.td1_ontario,
                        vacation_pay_pct=a.vacation_pay_on_cheque)
        if a.json: print(json.dumps(res, indent=2)); return
        print_cheque(res, f"{a.freq.title()} pay on {fmt_money(a.salary)}/yr (Ontario, {R['year']} rates)")
        e = res["employer_cost"]
        print(f"  Employer also pays: CPP {fmt_money(e['cpp_match'])}, EI {fmt_money(e['ei_1_4x'])}")
    elif a.cmd == "promotion":
        res = promotion(a.old, a.new, a.freq, a.ytd_gross, a.ytd_cpp, a.ytd_cpp2, a.ytd_ei,
                        a.retro_periods, a.dependants)
        if a.json: print(json.dumps(res, indent=2)); return
        print_cheque(res["before"], f"BEFORE: {fmt_money(a.old)}/yr")
        print_cheque(res["after_next_cheque"], f"AFTER (next cheque): {fmt_money(a.new)}/yr")
        print(f"\n  Change per cheque: gross +{fmt_money(res['delta_gross'])}, net +{fmt_money(res['delta_net'])}")
        if "retro_pay" in res:
            rp = res["retro_pay"]
            print(f"  Retro pay ({rp['periods']} periods): gross {fmt_money(rp['gross'])}, "
                  f"tax {fmt_money(rp['income_tax'])}, CPP {fmt_money(rp['cpp_approx'])}, "
                  f"EI {fmt_money(rp['ei_approx'])}, net ~{fmt_money(rp['net_approx'])}")
    elif a.cmd == "bonus":
        res = bonus_tax(a.salary, a.freq, a.amount, dependants=a.dependants)
        print(json.dumps(res, indent=2) if a.json else
              f"Bonus {fmt_money(res['gross'])}: tax {fmt_money(res['income_tax'])}, "
              f"CPP {fmt_money(res['cpp_approx'])}, EI {fmt_money(res['ei_approx'])}, "
              f"net ~{fmt_money(res['net_approx'])}")
    elif a.cmd == "calendar":
        res = calendar(date.fromisoformat(a.start), a.count, load_company(a.company))
        if a.json: print(json.dumps(res, indent=2)); return
        print(f"\nUpcoming {res['frequency']} pay dates (holiday rule: {res['holiday_rule']})")
        for d in res["pay_dates"]:
            flag = f"  <- moved from {d['scheduled']} ({'; '.join(d['notes']) or 'weekend'})" if d["moved"] else ""
            per = f"  period {d['period']}" if d["period"] else ""
            print(f"  {d['actual_deposit']} ({d['weekday']}){per}{flag}")


if __name__ == "__main__":
    main()
