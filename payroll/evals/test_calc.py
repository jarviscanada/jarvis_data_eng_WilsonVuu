"""Regression tests for the payroll calculator. Run: python3 -m pytest evals/ -q

Golden values were hand-checked against the CRA T4127 formulas (2026). Before each
January/July rate update, re-verify a few against CRA's Payroll Deductions Online
Calculator (canada.ca/pdoc) and update this file together with rates-2026.md.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import payroll_calc as pc
from datetime import date


def approx(a, b, tol=0.02):
    return abs(a - b) <= tol


def test_new_hire_50k_biweekly():
    r = pc.paycheque(50_000, "biweekly")
    assert approx(r["gross_pay"], 1923.08)
    assert approx(r["cpp"], 106.41)   # 5.95% x (1923.08 - 3500/26)
    assert approx(r["ei"], 31.35)     # 1.63% x 1923.08
    assert r["cpp2"] == 0
    assert approx(r["income_tax_total"], 241.28, 0.05)
    assert approx(r["net_pay"], 1544.04, 0.05)
    assert r["ontario_breakdown_annual"]["health_premium"] == 600


def test_annual_maximums_respected():
    r = pc.paycheque(150_000, "biweekly", ytd_pi=75_000, ytd_cpp=4_230.45, ytd_ei=1_123.07)
    assert r["cpp"] == 0 and r["ei"] == 0
    assert approx(r["cpp2"], 230.77)


def test_cpp2_cap():
    r = pc.paycheque(300_000, "monthly", ytd_pi=84_000, ytd_cpp=4_230.45, ytd_cpp2=376.00, ytd_ei=1_123.07)
    assert approx(r["cpp2"], 40.00)


def test_promotion_increases_net_less_than_gross():
    r = pc.promotion(50_000, 62_000, "biweekly")
    assert 0 < r["delta_net"] < r["delta_gross"]


def test_low_income_ontario_tax_reduction():
    r = pc.paycheque(20_000, "biweekly")
    assert r["ontario_breakdown_annual"]["tax_reduction"] > 0


def test_ohp_schedule():
    assert pc.ohp(20_000) == 0
    assert pc.ohp(30_000) == 300
    assert pc.ohp(60_000) == 600
    assert pc.ohp(100_000) == 750
    assert pc.ohp(250_000) == 900


def test_holidays_2026():
    h = pc.ontario_holidays(2026)
    assert date(2026, 4, 3) in h       # Good Friday
    assert date(2026, 5, 18) in h      # Victoria Day
    assert date(2026, 10, 12) in h     # Thanksgiving


def test_christmas_paydate_moves_earlier():
    cfg = {"pay_frequency": "biweekly", "anchor_pay_date": "2026-01-09"}
    res = pc.calendar(date(2026, 12, 20), 1, cfg)
    assert res["pay_dates"][0]["actual_deposit"] == "2026-12-24"
