"""모듈 1 실습용 가상 MES 데이터 생성 (실제 ㈜금진 데이터 아님).
실행: python make_practice.py <교안폴더>  →  practice/mes_sample.xlsx, practice/mes_sample.csv
호기별 불량률(정답값)을 출력한다 — 교안 1-9 '성공하면'에 쓰인다.
"""
import csv
import random
import sys
from datetime import date, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "..") / "practice"
OUT.mkdir(parents=True, exist_ok=True)
random.seed(20261109)

PRODUCTS = ["8299-1", "8299-3", "8299-6", "7510-2", "7510-4", "6120-1", "9034-2", "9034-5", "5588-3"]
BASE_RATE = {1: 0.021, 2: 0.034, 3: 0.016}   # 호기별 기본 불량률(가상)
HEAD = ["생산일자", "제품코드", "호기", "생산량(m)", "불량량(m)", "가동시간(분)", "오븐온도(℃)"]

rows = []
d = date(2026, 9, 1)
while d <= date(2026, 9, 30):
    if d.weekday() < 5:                          # 평일만
        for machine in (1, 2, 3):
            qty = random.randrange(2400, 4200, 50)
            temp = random.randint(182, 198)
            rate = BASE_RATE[machine] + (0.012 if temp >= 195 else 0) + (0.006 if d.weekday() == 0 else 0)
            bad = round(qty * rate * random.uniform(0.8, 1.2))
            rows.append([d.isoformat(), random.choice(PRODUCTS), machine, qty, bad, random.randint(400, 470), temp])
    d += timedelta(days=1)

wb = Workbook()
ws = wb.active
ws.title = "생산실적"
ws.append(HEAD)
for c in ws[1]:
    c.font = Font(bold=True)
    c.fill = PatternFill("solid", fgColor="E8ECF5")
for r in rows:
    ws.append(r)
for col, w in zip("ABCDEFG", (12, 10, 6, 11, 11, 12, 12)):
    ws.column_dimensions[col].width = w
note = wb.create_sheet("안내")
note.append(["교육용 가상 데이터입니다. 실제 ㈜금진의 데이터가 아닙니다."])
note.append(["기간: 2026-09-01 ~ 2026-09-30 평일, 1~3호기"])
wb.save(OUT / "mes_sample.xlsx")

with open(OUT / "mes_sample.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(HEAD)
    w.writerows(rows)

print(f"행 수: {len(rows)}")
for m in (1, 2, 3):
    q = sum(r[3] for r in rows if r[2] == m)
    b = sum(r[4] for r in rows if r[2] == m)
    print(f"{m}호기: 생산 {q:,}m · 불량 {b:,}m · 불량률 {b / q * 100:.1f}%")
q = sum(r[3] for r in rows)
b = sum(r[4] for r in rows)
print(f"전체: 생산 {q:,}m · 불량 {b:,}m · 불량률 {b / q * 100:.1f}%")
