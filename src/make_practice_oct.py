"""확장 모듈(스킬 실행 실습)용 가상 MES 데이터 — 2026년 10월분 (실제 ㈜금진 데이터 아님).
실행: python src/make_practice_oct.py .  →  practice/mes_sample_oct.xlsx
9월분(mes_sample.xlsx)과 컬럼·시트 이름이 같고, 불량률 순위만 다르다(10월은 3호기가 가장 높음)
→ 같은 스킬을 새 데이터에 돌렸을 때 결과가 달라지는 것을 눈으로 확인하기 위함.
호기별 불량률(정답값)을 출력한다 — 교안 5-8 '성공하면'에 쓰인다.
9월 파일은 건드리지 않는다(make_practice.py와 분리).
"""
import random
import sys
from datetime import date, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "..") / "practice"
OUT.mkdir(parents=True, exist_ok=True)
random.seed(20261110)

PRODUCTS = ["8299-1", "8299-3", "8299-6", "7510-2", "7510-4", "6120-1", "9034-2", "9034-5", "5588-3"]
BASE_RATE = {1: 0.019, 2: 0.026, 3: 0.039}   # 10월: 3호기에 문제가 생긴 상황(가상)
HOLIDAYS = {date(2026, 10, 5), date(2026, 10, 9)}   # 개천절 대체공휴일, 한글날
HEAD = ["생산일자", "제품코드", "호기", "생산량(m)", "불량량(m)", "가동시간(분)", "오븐온도(℃)"]

rows = []
d = date(2026, 10, 1)
while d <= date(2026, 10, 31):
    if d.weekday() < 5 and d not in HOLIDAYS:
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
note.append(["기간: 2026-10-01 ~ 2026-10-31 평일(공휴일 제외), 1~3호기"])
wb.save(OUT / "mes_sample_oct.xlsx")

print(f"행 수: {len(rows)}")
for m in (1, 2, 3):
    q = sum(r[3] for r in rows if r[2] == m)
    b = sum(r[4] for r in rows if r[2] == m)
    print(f"{m}호기: 생산 {q:,}m · 불량 {b:,}m · 불량률 {b / q * 100:.1f}%")
q = sum(r[3] for r in rows)
b = sum(r[4] for r in rows)
print(f"전체: 생산 {q:,}m · 불량 {b:,}m · 불량률 {b / q * 100:.1f}%")
