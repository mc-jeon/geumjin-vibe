"""모듈 3·4 실습용 가상 데이터 생성 (실제 ㈜금진 데이터 아님) + 정답값(src/answers.json).
실행: python src/make_practice_m34.py .
  practice/mes_raw.xlsx            모듈 3 — 8~10월 MES 추출 '원본'(표기 섞임·중복·음수·빈칸 포함)
  practice/mes_clean.xlsx          모듈 3 정답 정제본 = 트랙 B 재료(따라잡기용)
  practice/design_template.md      3-10 설계서 4칸 양식
  practice/tracks/track_a_orders.xlsx      트랙 A 주문·재고 + 품목–호기
  practice/tracks/track_c_conditions.xlsx  트랙 C 제품코드별 작업조건
  practice/tracks/track_d_sales.xlsx       트랙 D 주문 실적 + 바이어 후보
  practice/tracks/track_e_source.xlsx      트랙 E 시스템 A 추출본
  practice/tracks/track_e_target.xlsx      트랙 E 시스템 B 업로드 양식(빈 양식)
9월·10월 행은 mes_sample.xlsx / mes_sample_oct.xlsx 를 그대로 가져온다(정제 후 9월 값이 모듈 1의 2.7·3.7·1.9%와 같아지도록).
교안(m3.py·m4.py)은 answers.json의 값을 읽어 쓰므로, 데이터를 다시 만들면 교안 숫자도 같이 바뀐다.
"""
import json
import random
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "..")
OUT = ROOT / "practice"
TR = OUT / "tracks"
TR.mkdir(parents=True, exist_ok=True)
ANS = {}
NOTE = "교육용 가상 데이터입니다. 실제 ㈜금진의 데이터가 아닙니다."


def save(wb, path, widths=None):
    for ws in wb.worksheets:
        for c in ws[1]:
            c.font = Font(bold=True)
            c.fill = PatternFill("solid", fgColor="E8ECF5")
    if widths:
        for col, w in zip("ABCDEFGHIJKL", widths):
            wb.worksheets[0].column_dimensions[col].width = w
    n = wb.create_sheet("안내")
    n.append([NOTE])
    wb.save(path)


def pct(b, q):
    return round(b / q * 100, 1) if q else 0.0


# ════════════════════ 모듈 3 · MES 원본 ════════════════════
HEAD = ["생산일자", "제품코드", "호기", "생산량(m)", "불량량(m)", "가동시간(분)", "오븐온도(℃)"]
PRODUCTS = ["8299-1", "8299-3", "8299-6", "7510-2", "7510-4", "6120-1", "9034-2", "9034-5", "5588-3"]


def read_rows(name):
    ws = load_workbook(OUT / name)["생산실적"]
    return [list(r) for r in ws.iter_rows(min_row=2, values_only=True)]


rnd = random.Random(20260803)
aug = []
d = date(2026, 8, 3)
while d <= date(2026, 8, 31):
    if d.weekday() < 5 and d != date(2026, 8, 17):          # 8/17 광복절 대체공휴일
        for m in (1, 2, 3):
            qty = rnd.randrange(2400, 4200, 50)
            temp = rnd.randint(182, 198)
            rate = {1: 0.022, 2: 0.031, 3: 0.018}[m] + (0.012 if temp >= 195 else 0) + (0.006 if d.weekday() == 0 else 0)
            aug.append([d.isoformat(), rnd.choice(PRODUCTS), m, qty, round(qty * rate * rnd.uniform(0.8, 1.2)), rnd.randint(400, 470), temp])
    d += timedelta(days=1)
clean = aug + read_rows("mes_sample.xlsx") + read_rows("mes_sample_oct.xlsx")
assert len(clean) == 186, len(clean)

raw = [list(r) for r in clean]
idx = list(range(len(raw)))
rnd.shuffle(idx)
dot, slash, hogi, sharp, comma = idx[:24], idx[24:36], idx[36:51], idx[51:59], idx[59:67]
for i in dot:
    raw[i][0] = raw[i][0].replace("-", ".")
for i in slash:
    y, m, dd = raw[i][0].split("-")
    raw[i][0] = f"{y}/{int(m)}/{int(dd)}"
for i in hogi:
    raw[i][2] = f"{raw[i][2]}호기"
for i in sharp:
    raw[i][2] = f"#{raw[i][2]}"
for i in comma:
    raw[i][3] = f"{raw[i][3]:,}"
# 지워야 하는 행 5개(중복 2 · 음수 2 · 불량량 빈칸 1) — 정상 행 뒤에 끼워 넣는다
junk = {idx[70]: "dup", idx[71]: "dup", idx[72]: "neg", idx[73]: "neg", idx[74]: "blank"}
out = []
for i, r in enumerate(raw):
    out.append(r)
    k = junk.get(i)
    if k == "dup":
        out.append(list(r))
    elif k == "neg":
        c = list(clean[i])
        out.append([r[0], c[1], r[2], -c[3], 0, 0, c[6]])       # 입력 취소(음수) 행
    elif k == "blank":
        c = list(clean[i])
        out.append([r[0], rnd.choice(PRODUCTS), r[2], 1200, None, 150, c[6]])   # 불량량 미입력
wb = Workbook()
ws = wb.active
ws.title = "생산실적"
ws.append(HEAD)
for r in out:
    ws.append(r)
save(wb, OUT / "mes_raw.xlsx", (12, 10, 7, 11, 11, 12, 12))

wb = Workbook()
ws = wb.active
ws.title = "생산실적"
ws.append(HEAD)
for r in clean:
    ws.append(r)
save(wb, OUT / "mes_clean.xlsx", (12, 10, 6, 11, 11, 12, 12))


def agg(rows, key):
    q, b = defaultdict(int), defaultdict(int)
    for r in rows:
        k = key(r)
        q[k] += r[3]
        b[k] += r[4]
    return {str(k): {"q": q[k], "b": b[k], "rate": pct(b[k], q[k])} for k in sorted(q, key=str)}


WD = "월화수목금토일"


def band(t):
    return "190 미만" if t < 190 else ("190~194" if t < 195 else "195 이상")


tq, tb = sum(r[3] for r in clean), sum(r[4] for r in clean)
worst = max(((r[0], r[2], pct(r[4], r[3])) for r in clean), key=lambda x: x[2])
ANS["m3"] = {
    "raw_rows": len(out), "clean_rows": len(clean), "removed": {"중복": 2, "음수": 2, "불량량 빈칸": 1},
    "noise": {"날짜 점 표기": len(dot), "날짜 슬래시 표기": len(slash), "호기 '○호기' 표기": len(hogi), "호기 '#○' 표기": len(sharp), "생산량 쉼표 글자": len(comma)},
    "total": {"q": tq, "b": tb, "rate": pct(tb, tq)},
    "machine": agg(clean, lambda r: r[2]),
    "month": {mo: agg([r for r in clean if r[0][5:7] == mo], lambda r: r[2]) for mo in ("08", "09", "10")},
    "month_total": agg(clean, lambda r: r[0][5:7]),
    "weekday": agg(clean, lambda r: WD[date.fromisoformat(r[0]).weekday()]),
    "band": agg(clean, lambda r: band(r[6])),
    "monday_vs": {"월": pct(sum(r[4] for r in clean if date.fromisoformat(r[0]).weekday() == 0), sum(r[3] for r in clean if date.fromisoformat(r[0]).weekday() == 0)),
                  "그 외": pct(sum(r[4] for r in clean if date.fromisoformat(r[0]).weekday() != 0), sum(r[3] for r in clean if date.fromisoformat(r[0]).weekday() != 0))},
    "machine_weekday": agg(clean, lambda r: f"{r[2]}호기-{WD[date.fromisoformat(r[0]).weekday()]}"),
    "worst_day": {"date": worst[0], "machine": worst[1], "rate": worst[2]},
    "over5": sum(1 for r in clean if r[4] / r[3] >= 0.05),
}
ANS["m3"]["product"] = agg(clean, lambda r: r[1])
_pr = ANS["m3"]["product"]
ANS["m3"]["worst_product"] = max(_pr, key=lambda k: _pr[k]["rate"])
ANS["m3"]["best_product"] = min(_pr, key=lambda k: _pr[k]["rate"])
mw = ANS["m3"]["machine_weekday"]
ANS["m3"]["worst_combo"] = max(mw, key=lambda k: mw[k]["rate"])

# ════════════════════ 트랙 A · 주문·재고 ════════════════════
rnd = random.Random(1116)
BASE = date(2026, 11, 16)
SERIES = {"8299": "실크", "7510": "합지", "6120": "방염", "9034": "실크", "5588": "합지"}
codes = [f"{p}-{i}" for p in SERIES for i in range(1, 5)]
a_rows, mat = [], []
for c in codes:
    order = rnd.randrange(3000, 16000, 500)
    gj, ca, safe = rnd.randrange(0, 9000, 500), rnd.randrange(0, 6000, 500), rnd.choice([1000, 1500, 2000])
    due = BASE + timedelta(days=rnd.choice([1, 2, 3, 4, 7, 8, 9, 10, 14, 15, 18]))
    a_rows.append([c, SERIES[c[:4]], order, gj, ca, safe, due.isoformat()])
    ok = [m for m in (1, 2, 3) if rnd.random() < 0.6] or [rnd.choice([1, 2, 3])]
    mat.append([c] + ["O" if m in ok else "" for m in (1, 2, 3)])
wb = Workbook()
ws = wb.active
ws.title = "주문재고"
ws.append(["품목코드", "품목계열", "주문량(m)", "금진재고(m)", "천안재고(m)", "안전재고(m)", "납기일"])
for r in a_rows:
    ws.append(r)
w2 = wb.create_sheet("품목호기")
w2.append(["품목코드", "1호기", "2호기", "3호기"])
for r in mat:
    w2.append(r)
save(wb, TR / "track_a_orders.xlsx", (11, 10, 11, 12, 12, 12, 12))


def a_calc(r):
    need = max(0, r[2] + r[5] - r[3] - r[4])
    days = (date.fromisoformat(r[6]) - BASE).days
    lv = "생산 불필요" if need == 0 else ("긴급" if days <= 3 else ("주의" if days <= 7 else "여유"))
    return need, days, lv


ac = [(r[0],) + a_calc(r) for r in a_rows]
urgent = sorted([x for x in ac if x[3] == "긴급"], key=lambda x: (x[2], -x[1]))
ANS["A"] = {"base": BASE.isoformat(), "items": len(a_rows), "need_items": sum(1 for x in ac if x[1] > 0), "need_total": sum(x[1] for x in ac),
            "levels": {lv: sum(1 for x in ac if x[3] == lv) for lv in ("긴급", "주의", "여유", "생산 불필요")},
            "urgent_first": {"code": urgent[0][0], "need": urgent[0][1], "days": urgent[0][2]} if urgent else None,
            "sample": {"code": ac[0][0], "need": ac[0][1], "level": ac[0][3]},
            "m2_need": sum(x[1] for x, m in zip(ac, mat) if m[2] == "O")}

# ════════════════════ 트랙 C · 작업조건 ════════════════════
rnd = random.Random(2027)
NAMES = {"8299": "실크 플레인", "7510": "합지 스트라이프", "6120": "방염 스톤", "9034": "실크 린넨", "5588": "합지 플라워"}
c_rows = []
for c in codes + ["8299-6", "7510-5"]:
    c_rows.append([c, f"{NAMES[c[:4]]} {c[-1]}", rnd.choice([1, 2, 3]), rnd.randrange(195, 216, 5), rnd.randint(182, 198),
                   rnd.randrange(80, 141, 10), rnd.randrange(90, 181, 10), rnd.randrange(18, 36, 2),
                   f"E-{rnd.randint(101, 140)}", f"P-{rnd.randint(201, 260)}"])
wb = Workbook()
ws = wb.active
ws.title = "작업조건"
CH = ["제품코드", "제품명", "호기", "발포온도(℃)", "오븐온도(℃)", "텐션(N)", "코팅량(g/㎡)", "설정속도(m/min)", "엠보롤", "인쇄롤"]
ws.append(CH)
for r in c_rows:
    ws.append(r)
save(wb, TR / "track_c_conditions.xlsx", (10, 18, 6, 12, 12, 9, 13, 15, 9, 9))
look = next(r for r in c_rows if r[0] == "8299-3")
fast = max(c_rows, key=lambda r: r[7])
ANS["C"] = {"items": len(c_rows), "lookup": dict(zip(CH, look)), "m2_count": sum(1 for r in c_rows if r[2] == 2),
            "by_machine": {str(m): sum(1 for r in c_rows if r[2] == m) for m in (1, 2, 3)},
            "fastest": {"code": fast[0], "speed": fast[7], "tie": sum(1 for r in c_rows if r[7] == fast[7])},
            "prefix_7510": sum(1 for r in c_rows if r[0].startswith("7510"))}

# ════════════════════ 트랙 D · 주문 실적 + 바이어 후보 ════════════════════
rnd = random.Random(2750)
CUST = [(f"C{n:03d}", "내수", "한국") for n in range(1, 9)] + [("C009", "수출", "베트남"), ("C010", "수출", "인도네시아"), ("C011", "수출", "아랍에미리트"), ("C012", "수출", "폴란드")]
SER = ["실크", "합지", "방염"]
d_rows = []
for mo in range(1, 11):
    for cu, kind, nat in CUST:
        for s in SER:
            if rnd.random() < (0.45 if kind == "내수" else 0.4):
                base = {"실크": 9000, "합지": 6000, "방염": 3500}[s] * (0.6 if kind == "수출" else 1)
                d_rows.append([f"2026-{mo:02d}", s, cu, kind, nat, int(round(base * rnd.uniform(0.5, 1.6), -2))])
STAT = ["접촉 전", "메일 발송", "회신", "샘플 발송"]
NAT2 = ["베트남", "인도네시아", "아랍에미리트", "폴란드", "태국", "사우디아라비아", "튀르키예"]
buyers = [[f"B{n:03d}", rnd.choice(NAT2), rnd.choice(["인테리어 자재 유통", "건설사 구매", "벽지 수입상"]), rnd.choice(SER), rnd.choice(STAT),
           (date(2026, 9, 1) + timedelta(days=rnd.randint(0, 65))).isoformat()] for n in range(1, 16)]
for b in buyers:
    if b[4] == "접촉 전":
        b[5] = ""
wb = Workbook()
ws = wb.active
ws.title = "주문실적"
ws.append(["주문월", "품목계열", "거래처코드", "구분", "국가", "주문량(m)"])
for r in d_rows:
    ws.append(r)
w2 = wb.create_sheet("바이어후보")
w2.append(["후보코드", "국가", "업종", "관심계열", "상태", "최근접촉일"])
for r in buyers:
    w2.append(r)
save(wb, TR / "track_d_sales.xlsx", (10, 10, 11, 8, 14, 11))
dq = sum(r[5] for r in d_rows)
ex = sum(r[5] for r in d_rows if r[3] == "수출")
by_s = {s: sum(r[5] for r in d_rows if r[1] == s) for s in SER}
by_n = {n: sum(r[5] for r in d_rows if r[4] == n) for n in {r[4] for r in d_rows if r[3] == "수출"}}
ANS["D"] = {"rows": len(d_rows), "total": dq, "oct_total": sum(r[5] for r in d_rows if r[0] == "2026-10"), "sep_total": sum(r[5] for r in d_rows if r[0] == "2026-09"),
            "export_share": pct(ex, dq), "export_total": ex, "by_series": by_s, "top_series": max(by_s, key=by_s.get),
            "top_export_nation": max(by_n, key=by_n.get), "top_export_qty": max(by_n.values()),
            "buyers": len(buyers), "buyer_status": {s: sum(1 for b in buyers if b[4] == s) for s in STAT}}

# ════════════════════ 트랙 E · 양식 변환 ════════════════════
rnd = random.Random(505)
DEPT = {"관리팀": "D10", "생산팀": "D20", "기술개발": "D30", "전략": "D40"}
ITEM = ["OF-1001", "OF-1002", "MT-2001", "MT-2002", "MT-2003", "PK-3001", "PK-3002"]
e_rows, e_ok = [], []
for n in range(45):
    dt = date(2026, 10, 1) + timedelta(days=rnd.randint(0, 29))
    cust = rnd.randint(1, 15)
    qty = rnd.randrange(50, 3000, 50)
    dep = rnd.choice(list(DEPT))
    it = rnd.choice(ITEM)
    d_txt = rnd.choice([dt.isoformat(), dt.strftime("%Y.%m.%d"), dt.strftime("%Y%m%d")])
    c_txt = rnd.choice([f"C{cust:03d}", f"c{cust:03d}", f" C{cust:03d}", f"C-{cust:03d}"])
    q_val = rnd.choice([qty, f"{qty:,}", f"{qty} EA"])
    miss = "거래처" if n in (4, 13, 22, 37) else ("수량" if n in (9, 18, 30) else "")
    e_rows.append([d_txt, "" if miss == "거래처" else c_txt, it, "" if miss == "수량" else q_val, dep, rnd.choice(["", "", "긴급", "분할 입고"])])
    if not miss:
        e_ok.append([dt.strftime("%Y%m%d"), f"C{cust:03d}", it, qty, DEPT[dep]])
wb = Workbook()
ws = wb.active
ws.title = "A시스템_추출"
ws.append(["발주일자", "거래처", "품목코드", "수량", "요청부서", "비고"])
for r in e_rows:
    ws.append(r)
save(wb, TR / "track_e_source.xlsx", (12, 10, 10, 10, 10, 12))
wb = Workbook()
ws = wb.active
ws.title = "B시스템_업로드"
ws.append(["전표일자", "거래처코드", "품목코드", "수량", "부서코드"])
w2 = wb.create_sheet("작성규칙")
for r in [["열", "규칙"], ["전표일자", "숫자 8자리 YYYYMMDD (예: 20261005)"], ["거래처코드", "대문자 C + 숫자 3자리 (예: C007). 공백·하이픈 없음"],
          ["품목코드", "원본 그대로"], ["수량", "정수(쉼표·단위 없음)"], ["부서코드", "관리팀 D10 · 생산팀 D20 · 기술개발 D30 · 전략 D40"]]:
    w2.append(r)
save(wb, TR / "track_e_target.xlsx", (12, 12, 10, 8, 10))
ANS["E"] = {"source_rows": len(e_rows), "ok_rows": len(e_ok), "missing": {"거래처": 4, "수량": 3}, "qty_sum": sum(r[3] for r in e_ok),
            "first": e_ok[0], "dept_count": {v: sum(1 for r in e_ok if r[4] == v) for v in DEPT.values()}}

# ════════════════════ 설계서 4칸 양식 ════════════════════
(OUT / "design_template.md").write_text("""# 내 도구 설계서 (4칸)

> 트랙: (A 생산 / B 기술개발① / C 기술개발② / D 전략 / E 관리)   작성자:

## 1. 목적 — 누가, 언제, 무엇을 보려고 쓰나요?
(예: 생산팀 과장이 매주 월요일 아침, 이번 주에 무엇을 얼마나 먼저 만들어야 하는지 본다.)

## 2. 데이터 — 어떤 파일의 어떤 열을 쓰나요?
- 파일 위치와 이름:
- 쓰는 열:
- 계산식(있으면):
- 신호등: (초록 / 노랑 — 무엇을 가렸는지)

## 3. 화면 — 처음 열면 무엇이 보이나요?
- 첫 화면(표 1개 또는 숫자 카드 1개):
- 나중에 더할 기능 2~3개:

## 4. 금지사항 — 하면 안 되는 것
- 원본 파일은 수정하지 않는다.
- (넣지 않는 데이터, 공개하면 안 되는 것 등)
""", encoding="utf-8", newline="\n")

(ROOT / "src" / "answers.json").write_text(json.dumps(ANS, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps(ANS, ensure_ascii=False, indent=1))
