"""모듈 6(구글 시트 + Apps Script 앱 만들기) 실습 파일 — 가상 데이터(실제 ㈜금진 데이터 아님).
실행: python src/make_practice_m6.py .  →  practice/m6_sheet_app.xlsx
- '생산실적' 탭: 9월 가상 생산실적(practice/mes_sample.xlsx와 같은 66행). 정답값 1호기 2.7 · 2호기 3.7 · 3호기 1.9 · 전체 2.8%
- '설계' 탭: 버튼 설계표의 빈 머리글(6-5에서 클로와 함께 채운다)
- '안내' 탭: 가상 데이터 안내
mes_sample.xlsx를 읽어서 복사하므로, 9월 데이터를 바꾸면 이 스크립트도 다시 돌린다.
"""
import sys
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "..")
OUT = ROOT / "practice"
src = load_workbook(OUT / "mes_sample.xlsx", data_only=True)["생산실적"]
rows = [list(r) for r in src.iter_rows(values_only=True) if r and r[0] is not None]

wb = Workbook()
ws = wb.active
ws.title = "생산실적"
for r in rows:
    ws.append(r)
for c in ws[1]:
    c.font = Font(bold=True)
    c.fill = PatternFill("solid", fgColor="EEF2F8")
for col, w in zip("ABCDEFG", (12, 10, 6, 11, 11, 12, 12)):
    ws.column_dimensions[col].width = w
ws.freeze_panes = "A2"

ds = wb.create_sheet("설계")
ds.append(["순서", "버튼 이름", "누르면 하는 일", "필요한 입력", "결과가 나오는 곳"])
for c in ds[1]:
    c.font = Font(bold=True)
    c.fill = PatternFill("solid", fgColor="FFF4D6")
for col, w in zip("ABCDE", (6, 18, 40, 18, 18)):
    ds.column_dimensions[col].width = w

info = wb.create_sheet("안내")
info.append(["교육용 가상 데이터입니다. 실제 ㈜금진의 데이터가 아닙니다."])
info.append(["생산실적: 2026-09-01 ~ 2026-09-30 평일, 1~3호기 (mes_sample.xlsx와 같음)"])
info.append(["설계: 모듈 6에서 Claude와 함께 버튼 설계표를 채웁니다."])

wb.save(OUT / "m6_sheet_app.xlsx")

data = rows[1:]
for m in (1, 2, 3):
    part = [r for r in data if r[2] == m]
    q, b = sum(r[3] for r in part), sum(r[4] for r in part)
    print(f"{m}호기 {q:,}m · {b:,}m · {b / q * 100:.1f}%")
q, b = sum(r[3] for r in data), sum(r[4] for r in data)
print(f"전체 {len(data)}행 · {q:,}m · {b:,}m · {b / q * 100:.1f}%")
