"""마무리 모듈(5) · 프로젝트 폴더 구성 → 스킬 만들기·실행 → MCP 개념과 노션 연결 실습.
바이브코딩(모듈 1~4)을 끝낸 뒤 마지막에 진행한다. 모듈 3·4의 결과물에 기대지 않도록 새 프로젝트 폴더(gj-report)에서 시작한다.

사실 확인(2026-11-10, 공식 문서):
- 스킬: .claude/skills/<이름>/SKILL.md (프로젝트) · ~/.claude/skills/<이름>/SKILL.md (개인). /이름 인수 로 실행, description으로 자동 실행도 됨.
  세션 중 추가·수정은 바로 반영되지만, 세션을 시작할 때 skills 폴더가 없었다면 /reload-skills 필요. (code.claude.com/docs/en/skills)
- MCP: claude mcp add --transport http notion https://mcp.notion.com/mcp → Claude Code 안에서 /mcp 로 인증.
  기본 범위는 local(명령을 실행한 폴더에서만). claude mcp list 상태: ✔ Connected / ! Needs authentication.
  (code.claude.com/docs/en/mcp, developers.notion.com/guides/mcp/get-started-with-mcp)
- CLAUDE.md는 200줄 이내 권장, /memory로 불러온 파일 확인. (code.claude.com/docs/en/memory)
문서에 없는 것(= 모형으로 그렸으니 리허설에서 확인): /mcp 메뉴의 정확한 문구, 노션 허용 화면 문구, 노션 도구 권한 창 문구.
정답값: 9월 66행·219,750m·6,135m (1호기 2.7 · 2호기 3.7 · 3호기 1.9 · 전체 2.8%),
        10월 60행·188,600m·5,856m (1호기 2.1 · 2호기 3.1 · 3호기 4.1 · 전체 3.1%) — make_practice*.py 출력과 같아야 한다.
"""
from pathlib import Path

from lessonkit import E, app_window, box, cards, code_block, fig, figs, flow, kbd, mk, prompt, section, step, table, ui, wrap
from mocks_geumjin import (bar_chart, browser, cc_ai, cc_input, cc_perm, cc_tool, cc_user, cc_welcome, cc_window, explorer, passed,
                           progress_bar, ps_prompt, ps_window)
from mocks_notion import make_side, nt_db, nt_page, nt_window

ROOT = Path(__file__).resolve().parent.parent
SKILL_FILE = ROOT / "practice" / "skill_example" / "monthly-report" / "SKILL.md"
PC = "설치와 실습은 PC에서 합니다. 휴대폰은 복습용으로 보세요. 그림은 탭하면 크게 볼 수 있습니다."
DESK = "C:\\Users\\금대리\\Desktop"
PROJ = DESK + "\\gj-report"

EXT_CSS = r"""
.np{margin:0;padding:10px 12px;font:12px/1.6 Consolas,'D2Coding','Malgun Gothic',monospace;white-space:pre-wrap;background:#fff;color:#1f2328;min-height:190px}
.np .fm{color:#8250df}.np .hd{color:#0550ae;font-weight:700}
.tree{background:#fbfaf6;border:1px solid var(--bd);border-radius:12px;padding:12px 14px;font:13.5px/1.75 Consolas,'D2Coding','Malgun Gothic',monospace;white-space:pre-wrap;margin:10px 0}
.tree b{color:#1d3a7a}.tree i{color:var(--tx2);font-style:normal}
.oa{max-width:300px;margin:8px auto;background:#fff;border:1px solid #e3e2e0;border-radius:10px;padding:16px;text-align:center}
.oa .lg{font-size:26px}.oa h4{font-size:14px;margin:8px 0 6px}.oa p{color:#5f6368;font-size:12px;margin:4px 0}
.oa .ws{border:1px solid #e3e2e0;border-radius:6px;padding:5px 8px;margin:8px 0;text-align:left;font-size:12px}
.oa .bt{display:flex;gap:8px;justify-content:center;margin-top:10px}
.oa .b{border:1px solid #c9d1dd;border-radius:6px;padding:4px 14px;font-size:12px;background:#fff}
.oa .b.p{background:#2383e2;border-color:#2383e2;color:#fff}
.nt-pg table.mini{border-collapse:collapse;margin:8px 0;font-size:12px}
.nt-pg table.mini td,.nt-pg table.mini th{border:1px solid #e3e2e0;padding:3px 10px;text-align:left}
.nt-pg table.mini th{background:#f7f6f3}
.rp{background:#f6f1e7;border-radius:8px;padding:10px 12px;color:#1d3a7a}
.rp h5{font-size:13.5px;margin:0 0 2px}.rp small{color:#6b6252}
.rp ol{margin:6px 0 8px 18px;font-size:12px;line-height:1.6}
.rp .bc{background:#fffdf8;box-shadow:none;border:1px solid #e6dcc6}
.rp .bc-b.hot{background:#c96442}
"""


def st(no, title, goal, todo, ok, stuck=None, figure="", extra="", one=False):
    return step(no, title, goal, todo, ok=ok + passed(), stuck=stuck, figure=figure, extra=extra, one=one)


def html_line(h):
    return ("html", h)


def span(cls, text):
    return f'<span class="{cls}">{E(text)}</span>'


def cc(body, title="PowerShell — claude"):
    return cc_window(body, title=title, path=PROJ)


def report_mock(month, values, hot, lines):
    """월간 보고서 결과물 모양(예시). hot = 가장 높은 호기 이름."""
    ch = bar_chart(values).replace('<div class="bc-r"><span>' + hot + '</span><div class="bc-b"',
                                   '<div class="bc-r"><span>' + hot + '</span><div class="bc-b hot"')
    lis = "".join(f"<li>{E(x)}</li>" for x in lines)
    return f'<div class="rp"><h5>㈜금진 월간 생산 보고 · 2026년 {month}월</h5><small>교육용 가상 데이터</small><ol>{lis}</ol>{ch}</div>'


def notepad(body_html, name="SKILL.md"):
    return app_window(f"{name} - 메모장", f'<pre class="np">{body_html}</pre>', icon_color="#3a96dd", menus=["파일", "편집", "보기"])


def notion(body, crumbs, on, sub=None, side_marks=None, min_h=280):
    return nt_window(body, crumbs=crumbs, side_on=on, side_marks=side_marks, min_h=min_h,
                     side_items=make_side("금대리의 워크스페이스", team_pages=(), my_pages=("📄 금진 AI 실습",), db=sub))


def oauth_card(n=None):
    allow = '<span class="b p">액세스 허용</span>'
    return ('<div class="oa"><div class="lg">🔗</div><h4>Claude Code가 Notion 워크스페이스에 연결하려고 합니다</h4>'
            '<p>허용하면 이 워크스페이스에서 내가 볼 수 있는 페이지를 읽고 고칠 수 있습니다.</p>'
            '<div class="ws">🏠 금대리의 워크스페이스 ▾</div>'
            f'<div class="bt"><span class="b">취소</span>{mk(allow, n) if n else allow}</div></div>')


# ───────── 프롬프트(교안과 그림에서 같이 씀) ─────────
P_CLAUDE_MD = """이 폴더의 규칙 파일 CLAUDE.md를 만들어줘. 아래 내용을 30줄 이내로 짧게 적어줘.
- 프로젝트: ㈜금진 월간 생산 보고서 만들기 (교육용 가상 데이터)
- 폴더: data = 원본 엑셀(수정·삭제 금지), docs = 설계서·메모, output = 결과물
- 불량률 = 불량량 합계 ÷ 생산량 합계 × 100, 소수 첫째 자리까지
- 설명은 한국어로, 초보자용으로
- 파일을 고치기 전에 계획부터 보여주기"""
P_RULES = "이 폴더에서 네가 지켜야 할 규칙을 3줄로 말해줘."
P_REPORT = """목적: 9월 생산실적을 호기별 불량률 중심으로 한눈에 보는 월간 보고서를 만들고 싶어.
재료: data/mes_sample.xlsx (시트 '생산실적')
결과 모양: output/월간보고_2026-09.html 한 파일. 맨 위 제목 '㈜금진 월간 생산 보고 · 2026년 9월', 호기별 불량률 막대 차트 1개, 그 아래 호기별 생산량·불량량·불량률 표(맨 아래 전체 행)
금지사항: data 폴더의 원본은 수정하지 마. 만들기 전에 계획부터 보여줘."""
P_FIX1 = "제목 바로 아래에 요약 3줄을 넣어줘: ① 전체 생산량과 불량률 ② 불량률이 가장 높은 호기와 수치 ③ 확인이 필요한 점 한 가지."
P_FIX2 = "불량률이 가장 높은 호기의 막대만 주황색으로, 나머지는 남색으로 해줘. 배경은 베이지 톤으로 바꿔줘."
P_FIX3 = "원본과 대조할 수 있게 행 수, 전체 생산량 합계, 전체 불량량 합계를 알려줘."
P_SKILL = """방금 만든 월간 보고서가 마음에 들어. 이 작업 방식을 다음 달에도 그대로 쓸 수 있게 프로젝트 스킬로 만들어줘.
- 위치: .claude/skills/monthly-report/SKILL.md
- name: monthly-report
- description: 언제 이 스킬을 쓰는지 한두 문장으로
- 입력: data 폴더의 엑셀 파일 이름($ARGUMENTS). 연도와 월은 생산일자에서 알아내기
- 내용: 지금까지 정한 순서, 불량률 계산식, 보고서 모양(요약 3줄·차트 색·표), 저장 위치(output/월간보고_연도-월.html), 마친 뒤 대조용 숫자 3개 보고, 원본 수정 금지
만든 뒤에는 스킬 파일에 무엇을 적었는지 초보자용으로 설명해줘."""
P_RUN = "/monthly-report mes_sample_oct.xlsx"
P_TUNE = "monthly-report 스킬에 규칙을 하나 추가해줘: 보고서 맨 아래에 '작성: [관리팀 금대리] · 작성일(오늘 날짜)'을 작은 글씨로 넣는다."
P_READ = "노션에서 '금진 AI 실습' 페이지를 찾아서 무엇이 적혀 있는지 알려줘. 아직 아무것도 바꾸지 마."
P_WRITE = """노션 '금진 AI 실습' 페이지 아래에 '2026년 10월 생산 보고'라는 하위 페이지를 만들고 싶어.
output/월간보고_2026-10.html의 요약 3줄과 호기별 표(호기, 생산량, 불량량, 불량률)를 넣을 거야.
만들기 전에 넣을 내용을 먼저 보여줘."""
P_DB = """노션 '금진 AI 실습' 페이지 아래에 '불량 조치 목록' 데이터베이스를 만들어줘.
속성: 조치 내용(제목), 호기(선택: 1호기·2호기·3호기), 상태(선택: 시작 전·진행 중·완료), 기한(날짜)
아래 3건을 넣어줘.
- 3호기 오븐 온도 센서 점검 / 3호기 / 시작 전 / 2026-11-13
- 2호기 월요일 첫 롤 불량 원인 확인 / 2호기 / 시작 전 / 2026-11-17
- 10월 불량 샘플 사진 정리 / 1호기 / 완료 / 2026-11-10"""
P_DB2 = "'불량 조치 목록'에서 '3호기 오븐 온도 센서 점검'의 상태를 '진행 중'으로 바꿔줘."
P_COMBO = """monthly-report 스킬 맨 끝에 단계를 하나 추가해줘.
보고서를 만든 뒤 "노션에 올릴까요?"라고 묻는다. 내가 그렇다고 하면 노션 '금진 AI 실습' 페이지 아래에 '연도년 월월 생산 보고' 하위 페이지를 만들고 요약 3줄과 호기별 표를 넣는다.
같은 제목의 페이지가 이미 있으면 새로 만들지 말고 나에게 알려준다."""
MCP_ADD = "claude mcp add --transport http notion https://mcp.notion.com/mcp\n"

SEP_VALUES = [("1호기", 2.7), ("2호기", 3.7), ("3호기", 1.9)]
OCT_VALUES = [("1호기", 2.1), ("2호기", 3.1), ("3호기", 4.1)]
SEP_LINES = ["전체 219,750m 생산, 불량률 2.8%", "불량률 최고: 2호기 3.7%", "2호기 월요일 불량 확인 필요"]
OCT_LINES = ["전체 188,600m 생산, 불량률 3.1%", "불량률 최고: 3호기 4.1%", "3호기 오븐 온도 확인 필요"]

DB_COLS = [("조치 내용", "title"), ("호기", "select"), ("상태", "status"), ("기한", "date")]
DB_ROWS = [["3호기 오븐 온도 센서 점검", "3호기", "진행 중", "2026-11-13"],
           ["2호기 월요일 첫 롤 불량 원인 확인", "2호기", "시작 전", "2026-11-17"],
           ["10월 불량 샘플 사진 정리", "1호기", "완료", "2026-11-10"]]

OCT_TABLE = ('<table class="mini"><tr><th>호기</th><th>생산량(m)</th><th>불량량(m)</th><th>불량률</th></tr>'
             "<tr><td>1호기</td><td>64,250</td><td>1,369</td><td>2.1%</td></tr>"
             "<tr><td>2호기</td><td>61,850</td><td>1,941</td><td>3.1%</td></tr>"
             "<tr><td>3호기</td><td>62,500</td><td>2,546</td><td>4.1%</td></tr>"
             "<tr><td><b>전체</b></td><td>188,600</td><td>5,856</td><td>3.1%</td></tr></table>")

TREE = ('<div class="tree"><b>gj-report\\</b>              <i>← 프로젝트 폴더 = 일꾼에게 내준 작업대 하나</i>\n'
        '├─ <b>CLAUDE.md</b>            <i>← 규칙 파일. 클로가 매번 가장 먼저 읽음 (5-3에서 만듦)</i>\n'
        '├─ <b>.claude\\</b>             <i>← 클로 전용 서랍</i>\n'
        '│   └─ <b>skills\\</b>          <i>← 스킬(작업표준서) 보관함 (5-7에서 생김)</i>\n'
        '│       └─ monthly-report\\SKILL.md\n'
        '├─ <b>data\\</b>                <i>← 원본 재료. 수정·삭제 금지</i>\n'
        '├─ <b>docs\\</b>                <i>← 설계서·메모</i>\n'
        '└─ <b>output\\</b>              <i>← 결과물이 쌓이는 곳</i></div>')

SKILL_FM = '<span class="fm">---\nname: monthly-report\ndescription: data 폴더의 생산실적 엑셀로 호기별 불량률\n  월간 보고서(HTML)를 만든다. …\n---</span>'
SKILL_NP = ('\n'
            '<span class="hd"># 월간 생산 보고서 만들기</span>\n\n<span class="hd">## 입력</span>\n- 엑셀 파일 이름: $ARGUMENTS\n\n'
            '<span class="hd">## 순서</span>\n1. data/ 폴더에서 엑셀을 읽는다. 원본은 수정하지 않는다.\n2. 생산일자에서 연·월을 알아낸다.\n3. 호기별 불량률 = 불량량 합계 ÷ 생산량 합계 × 100 …')


def ext_page():
    return wrap("".join([
        progress_bar("모듈 5 진도"),
        section("모듈 5 · 프로젝트 폴더, 스킬, MCP(노션)", "약 3시간 30분 · 바이브코딩을 마친 뒤 마지막에"),
        box("info", "이 모듈에서 얻는 것",
            "지금까지는 매번 말로 설명했습니다. 이제 <b>규칙은 폴더에</b>(CLAUDE.md), <b>잘된 방법은 스킬 파일에</b>, "
            "<b>바깥 도구는 MCP로</b> 연결해서, 다음 달에는 명령 한 줄로 같은 일을 끝냅니다."),
        flow([("1교시", "프로젝트 폴더 구성"), ("2교시", "결과물 → 스킬 파일 → 스킬로 실행"), ("3교시", "MCP 개념·노션 연결"), ("4교시", "노션 실습·스킬과 합치기")]),
        cards([("📌", "CLAUDE.md", "<p>현장 안전수칙 게시물. 이 폴더에서 항상 지킬 규칙.</p>"),
               ("📋", "스킬", "<p>작업표준서. 잘된 작업 방법을 파일로 굳혀 <code>/이름</code>으로 다시 실행.</p>"),
               ("🔌", "MCP", "<p>외부 시스템 출입증과 전용 통로. 클로가 노션 같은 바깥 도구를 직접 읽고 씀.</p>")], cols=3),

        # ── 1교시 ──
        section("1교시 · 프로젝트 폴더 구성", "약 40분"),
        st("5-1", "새 프로젝트 폴더 만들기", "새 일을 시작할 때마다 쓰는 폴더 틀(data·docs·output)을 만듭니다.",
           ["PowerShell을 새로 열고 아래 명령을 복사해 붙여넣기", "아래 버튼으로 실습 파일 2개 내려받기",
            f"탐색기 {ui('다운로드')} 폴더의 두 엑셀을 바탕화면 {ui('gj-report')} → {ui('data')} 폴더로 옮기기",
            "PowerShell에서 <code>dir data</code>로 두 파일이 보이는지 확인"],
           extra=code_block("프로젝트 폴더 만들기", text="cd Desktop\nmkdir gj-report\ncd gj-report\nmkdir data, docs, output\n", cid="c-proj")
           + '<a class="dl g" href="practice/mes_sample.xlsx" download>📥 9월 생산실적 mes_sample.xlsx</a> '
             '<a class="dl g" href="practice/mes_sample_oct.xlsx" download>📥 10월 생산실적 mes_sample_oct.xlsx</a>'
           + box("info", "왜 새 폴더인가요?", "프로젝트(일) 하나에 폴더 하나입니다. 클로는 <b>지금 열린 폴더 안</b>만 자기 작업대로 보기 때문에, 일이 다르면 폴더도 나눕니다."),
           ok="<code>dir data</code>에 <b>mes_sample.xlsx</b>와 <b>mes_sample_oct.xlsx</b> 두 파일이 나옵니다.",
           stuck="‘경로를 찾을 수 없습니다’가 나오면 바탕화면이 OneDrive에 있는 PC입니다. 첫 줄을 <code>cd ([Environment]::GetFolderPath('Desktop'))</code>로 바꾸세요.",
           figure=figs(
               fig("m5-01a", "폴더 틀 만들기", ps_window([
                   ps_prompt(path=DESK, cmd="mkdir gj-report", n=1), ps_prompt(path=DESK, cmd="cd gj-report"),
                   ps_prompt(path=PROJ, cmd="mkdir data, docs, output"), "",
                   "Mode     LastWriteTime      Length Name", "d----    2026-11-10 13:05        data",
                   "d----    2026-11-10 13:05        docs", "d----    2026-11-10 13:05        output", "",
                   ps_prompt(path=PROJ, cursor=True)])),
               fig("m5-01b", "data 폴더에 엑셀 2개 옮기기", explorer(PROJ + "\\data", [
                   ("📊", "mes_sample.xlsx", "Microsoft Excel 워크시트"), ("📊", "mes_sample_oct.xlsx", "Microsoft Excel 워크시트")],
                   path_mark=3)))),
        st("5-2", "프로젝트 폴더 지도 읽기", "폴더 안의 각 자리가 무슨 역할인지 압니다.",
           ["아래 폴더 지도를 위에서 아래로 읽습니다.", "표에서 ‘누가 만드나’ 칸을 확인합니다.", "옆 사람에게 CLAUDE.md와 스킬의 차이를 한 문장으로 설명해 봅니다."],
           extra=TREE + table(["자리", "무엇을 두나", "누가 만드나", "금진 비유"], [
               ["CLAUDE.md", "이 폴더에서 항상 지킬 규칙(200줄 이내로 짧게)", "클로에게 말로 시킴", "현장 안전수칙 게시물"],
               [".claude\\skills\\", "스킬 파일(SKILL.md) — 반복하는 작업 방법", "클로에게 말로 시킴", "작업표준서 철"],
               [".claude\\settings.json", "허락해 둔 명령 같은 설정. 직접 고칠 일은 거의 없음", "클로가 자동으로", "설비 설정값"],
               ["data\\", "원본 엑셀·CSV. 수정 금지", "내가 넣음", "입고된 원자재"],
               ["docs\\", "설계서, 정한 규칙, 메모", "클로 + 나", "작업 일지"],
               ["output\\", "보고서·대시보드 같은 결과물", "클로가 만듦", "완성품 적치대"]])
           + box("info", "한 문장 정리", "<b>CLAUDE.md</b>는 ‘항상 지킬 것’, <b>스킬</b>은 ‘이 일을 할 때의 순서’입니다. 규칙은 짧게, 순서는 스킬로 뺍니다."),
           ok="‘CLAUDE.md는 항상 읽는 규칙, 스킬은 부를 때 쓰는 작업 방법’이라고 말할 수 있으면 통과입니다.", one=True),
        st("5-3", "CLAUDE.md 만들기", "이 프로젝트의 규칙을 파일로 적어 두어, 매번 다시 설명하지 않게 합니다.",
           [f"PowerShell(gj-report 폴더)에서 <code>claude</code> 입력 → 폴더 신뢰 질문에 {ui('Yes, proceed')}",
            "아래 요청문을 붙여넣고 Enter", f"권한 창에서 만들 파일이 <b>CLAUDE.md</b>인지 확인 → {ui('1. Yes')}",
            f"<code>/memory</code> 입력 → 목록에 CLAUDE.md가 있는지 확인 → {kbd('Esc')}"],
           extra=prompt(P_CLAUDE_MD)
           + box("info", "이미 파일이 많은 폴더라면", "<code>/init</code>을 입력하면 클로가 폴더를 훑어보고 CLAUDE.md 초안을 만들어 줍니다. 오늘처럼 빈 폴더에서는 직접 불러 주는 편이 정확합니다."),
           ok="탐색기 gj-report 폴더에 <b>CLAUDE.md</b>가 생겼고, <code>/memory</code> 목록에도 보입니다.",
           stuck="<code>/memory</code> 화면 모양은 버전에 따라 다릅니다. 목록에 CLAUDE.md 줄만 보이면 됩니다.",
           figure=figs(
               fig("m5-03a", "요청 → 권한 창", cc(cc_welcome(cwd="gj-report") + cc_user("이 폴더의 규칙 파일 CLAUDE.md를 만들어줘. 아래 내용을 30줄 이내로…", n=2)
                                            + cc_perm("Do you want to create CLAUDE.md?", ["Yes", "Yes, allow all edits during this session", "No"], n=3))),
               fig("m5-03b", "/memory — 불러온 규칙 파일 확인", cc(cc_input("/memory", n=4)
                                                          + '<div class="cc-perm"><b>Memory</b><div class="on">❯ 1. Project memory &nbsp; ./CLAUDE.md</div>'
                                                            '<div>&nbsp; 2. User memory &nbsp; ~/.claude/CLAUDE.md</div></div>')))),
        st("5-4", "규칙이 먹히는지 확인", "새 대화에서도 클로가 규칙을 알고 있는지 확인합니다.",
           ["<code>/clear</code>로 대화를 비우기", "아래 질문을 붙여넣고 Enter", "답에 ‘data 원본 수정 금지’와 ‘불량률 계산식’이 들어 있는지 확인"],
           extra=prompt(P_RULES),
           ok="방금 설명하지 않았는데도 클로가 <b>data 수정 금지 · 합계끼리 나누는 계산식 · 계획 먼저</b> 같은 규칙을 말합니다. CLAUDE.md를 읽은 것입니다.",
           stuck="규칙을 모른다고 하면 <code>/exit</code> 후 gj-report 폴더에서 <code>claude</code>를 다시 실행하세요. 다른 폴더에서 실행하면 그 폴더의 규칙만 읽습니다.",
           figure=fig("m5-04", "/clear 뒤에도 규칙을 안다", cc(cc_user("/clear", n=1) + cc_user(P_RULES, n=2)
                                                      + cc_ai("1. data 폴더의 원본 엑셀은 수정·삭제하지 않습니다.\n2. 불량률은 불량량 합계 ÷ 생산량 합계 × 100, 소수 첫째 자리까지.\n3. 파일을 고치기 전에 계획부터 보여드리고, 한국어로 쉽게 설명합니다.")))),

        # ── 2교시 ──
        section("2교시 · 결과물 만들기 → 스킬 파일로 굳히기 → 스킬로 실행", "약 60분"),
        box("info", "스킬은 언제 만드나요?", "<b>결과물이 마음에 들었을 때</b>입니다. 먼저 대화로 만들고 고쳐서 ‘이거다’ 싶은 결과를 얻은 다음, 그 방법을 파일로 굳힙니다. 아직 마음에 안 드는 방법을 굳히면 매번 마음에 안 드는 결과가 나옵니다."),
        flow([("① 만들기", "대화로 9월 보고서"), ("② 고치기", "마음에 들 때까지"), ("③ 굳히기", "스킬 파일로 저장"), ("④ 다시 쓰기", "/monthly-report 로 10월 보고서")]),
        st("5-5", "9월 월간 보고서 만들기", "작업지시서 4칸으로 첫 결과물을 만듭니다.",
           ["아래 요청문을 붙여넣고 Enter", f"클로가 보여 준 계획을 읽고 “좋아, 진행해줘” 보내기 → 권한 창 {ui('1. Yes')}",
            f"탐색기 {ui('output')} 폴더의 <b>월간보고_2026-09.html</b> 더블클릭"],
           extra=prompt(P_REPORT),
           ok="크롬에 보고서가 열리고 불량률이 <b>1호기 2.7% · 2호기 3.7% · 3호기 1.9% · 전체 2.8%</b>로 나옵니다.",
           stuck="‘pandas(또는 openpyxl)가 없다’고 하면 2-19처럼 설치 명령을 읽고 허락합니다. 숫자가 다르면 “합계 불량량 ÷ 합계 생산량으로 다시 계산해줘”라고 보내세요.",
           figure=figs(
               fig("m5-05a", "작업지시서 → 계획 → 허락", cc(cc_user("목적: 9월 생산실적을 호기별 불량률 중심으로…", n=1)
                                                   + cc_ai("계획: ① data/mes_sample.xlsx 읽기(수정 없음) ② 호기별 합계·불량률 계산 ③ output/월간보고_2026-09.html 작성")
                                                   + cc_user("좋아, 진행해줘", n=2) + cc_tool("Write(output/월간보고_2026-09.html)"))),
               fig("m5-05b", "output 폴더에 생긴 보고서", explorer(PROJ + "\\output", [("🌐", "월간보고_2026-09.html", "Chrome HTML Document")],
                                                         marks={"월간보고_2026-09.html": 3})))),
        st("5-6", "마음에 들 때까지 고치기", "한 번에 하나씩 고쳐 ‘이대로 매달 받고 싶은’ 보고서로 만듭니다.",
           ["첫 번째 요청(요약 3줄) 보내기 → 크롬 새로고침", "두 번째 요청(색) 보내기 → 크롬 새로고침", "세 번째 요청(대조 숫자) 보내기",
            "data 폴더의 mes_sample.xlsx를 엑셀로 열어 숫자 3개를 직접 확인"],
           extra=prompt(P_FIX1) + prompt(P_FIX2) + prompt(P_FIX3)
           + box("warn", "원본과 대조", "행 수 <b>66</b> · 전체 생산량 <b>219,750m</b> · 전체 불량량 <b>6,135m</b>. 엑셀에서 D열·E열을 선택하면 오른쪽 아래에 합계가 보입니다."),
           ok="요약 3줄이 있고, 2호기 막대만 주황색이며, 대조 숫자 3개가 엑셀과 같습니다. 이 모양이 마음에 들면 통과입니다.",
           stuck="마음에 안 드는 곳이 더 있으면 지금 더 고치세요. 스킬은 ‘지금 이 모양’을 그대로 기억합니다.",
           figure=fig("m5-06", "고친 뒤의 9월 보고서(예시)", browser("file:///C:/Users/금대리/Desktop/gj-report/output/월간보고_2026-09.html",
                                                          report_mock(9, SEP_VALUES, "2호기", SEP_LINES), tab="월간 생산 보고"))),
        st("5-7", "스킬 파일로 만들기", "방금의 작업 방법을 CLI 창에서 말 한 번으로 스킬 파일(SKILL.md)로 저장합니다.",
           ["Claude Code 입력칸에 아래 요청문을 붙여넣고 Enter",
            f"권한 창의 파일 위치가 <code>.claude\\skills\\monthly-report\\SKILL.md</code>인지 확인 → {ui('1. Yes')}",
            "<code>/reload-skills</code> 입력 → Enter (새로 생긴 스킬 폴더를 읽게 함)",
            "입력칸에 <code>/mon</code>까지만 쳐서 목록에 <b>/monthly-report</b>가 보이는지 확인"],
           extra=prompt(P_SKILL)
           + box("info", "왜 /reload-skills 인가요?", "스킬 파일을 고치는 것은 바로 반영됩니다. 다만 Claude Code를 켤 때 <code>.claude\\skills</code> 폴더가 아예 없었다면 한 번 다시 읽게 해야 합니다. "
                 "목록에 안 보이면 <code>/exit</code> 후 <code>claude</code>를 다시 실행해도 됩니다."),
           ok="탐색기 gj-report\\.claude\\skills\\monthly-report 폴더에 <b>SKILL.md</b>가 있고, <code>/mon</code>을 치면 <b>/monthly-report</b>가 목록에 뜹니다.",
           stuck="파일이 다른 위치(예: 폴더 맨 위)에 만들어졌다면 “.claude/skills/monthly-report/SKILL.md 로 옮겨줘”라고 보내세요. 폴더 이름은 영문 소문자와 -만 씁니다.",
           figure=figs(
               fig("m5-07a", "스킬로 만들어 달라는 요청 → 권한 창", cc(cc_user("방금 만든 월간 보고서가 마음에 들어. 이 작업 방식을 … 프로젝트 스킬로 만들어줘.", n=1)
                                                         + cc_perm("Do you want to create SKILL.md?", ["Yes", "Yes, allow all edits during this session", "No"], n=2,
                                                                   detail=".claude\\skills\\monthly-report\\SKILL.md"))),
               fig("m5-07b", "/mon 까지 치면 스킬이 목록에", cc(cc_user("/reload-skills", n=3) + cc_input("/mon", n=4, hint="/monthly-report   data 폴더의 생산실적 엑셀로 호기별 불량률 월간 보고서(HTML)를 만든다…"))))),
        st("5-8", "스킬 파일 열어 읽기", "스킬이 마법이 아니라 ‘글로 쓴 작업표준서’라는 것을 눈으로 확인합니다.",
           ["PowerShell 창을 하나 더 열고 아래 명령을 붙여넣기(메모장이 열림)",
            "맨 위 <code>---</code> 사이의 <b>name</b>과 <b>description</b> 찾기",
            "그 아래 본문에서 계산식과 저장 위치가 적힌 줄 찾기",
            "아래 ‘정답 예시’와 비교하고 메모장 닫기(저장하지 않음)"],
           extra=code_block("스킬 파일 열기", text="cd Desktop\\gj-report\nnotepad .claude\\skills\\monthly-report\\SKILL.md\n", cid="c-np")
           + table(["부분", "뜻", "잘 쓰는 법"], [
               ["name", "스킬 이름. /이름 으로 부름", "영문 소문자와 -"],
               ["description", "언제 쓰는 스킬인지. 클로가 이 글을 보고 스스로 꺼내 쓰기도 함", "“~라고 할 때 사용한다”처럼 상황을 적기"],
               ["$ARGUMENTS", "/이름 뒤에 적은 말이 들어오는 자리", "파일 이름처럼 매번 바뀌는 것"],
               ["본문", "순서·계산식·모양·금지사항", "신입에게 주는 작업표준서처럼 구체적으로"]])
           + code_block("정답 예시 SKILL.md (내 것과 문장이 달라도 괜찮습니다)", path=SKILL_FILE, cid="c-skill", tall=True, wrap=True,
                        download_href="practice/skill_example/monthly-report/SKILL.md"),
           ok="내 SKILL.md에 name·description이 있고, 본문에 <b>불량률 계산식</b>과 <b>output 저장 위치</b>가 적혀 있습니다.",
           stuck="계산식이나 저장 위치가 빠졌다면 Claude Code 창에서 “스킬에 ○○ 규칙을 추가해줘”라고 보내세요. 급하면 정답 예시를 내려받아 같은 위치에 덮어써도 됩니다.",
           figure=fig("m5-08", "메모장으로 연 SKILL.md", notepad(
               mk(SKILL_FM, 2, block=True) + SKILL_NP.replace("3. 호기별 불량률 = 불량량 합계 ÷ 생산량 합계 × 100 …", mk("3. 호기별 불량률 = 불량량 합계 ÷ 생산량 합계 × 100 …", 3))))),
        st("5-9", "스킬로 실행하기 — 10월 데이터", "설명 없이 명령 한 줄로 10월 보고서를 만듭니다.",
           ["Claude Code 창에서 <code>/clear</code> (앞 대화를 지워도 되는지 확인하기 위해)", "아래 한 줄을 붙여넣고 Enter",
            f"권한 창이 나오면 내용을 읽고 {ui('1. Yes')}", f"{ui('output')} 폴더의 <b>월간보고_2026-10.html</b> 더블클릭"],
           extra=prompt(P_RUN)
           + box("ok", "말로 불러도 됩니다", "“10월 월간 보고서 만들어줘”처럼 말하면 클로가 description을 보고 이 스킬을 스스로 꺼내 씁니다. 확실하게 하려면 <code>/monthly-report 파일이름</code>이 가장 정확합니다."),
           ok="9월과 <b>같은 모양</b>의 보고서가 나오고, 숫자는 <b>1호기 2.1% · 2호기 3.1% · 3호기 4.1% · 전체 3.1%</b>입니다. 이번에는 <b>3호기</b> 막대가 주황색입니다. 대조 숫자는 60행 · 188,600m · 5,856m.",
           stuck="‘알 수 없는 명령’이라고 하면 <code>/reload-skills</code> 후 다시 하거나, <code>/exit</code> → <code>claude</code>로 다시 들어옵니다. 모양이 9월과 다르면 5-8로 돌아가 스킬에 빠진 규칙을 추가합니다.",
           figure=figs(
               fig("m5-09a", "명령 한 줄로 실행", cc(cc_user("/clear", n=1) + cc_user(P_RUN, n=2) + cc_tool("Skill(monthly-report) — data/mes_sample_oct.xlsx")
                                             + cc_ai("output/월간보고_2026-10.html 을 만들었습니다.\n대조용: 60행 · 생산량 188,600m · 불량량 5,856m\n엑셀에서 이 3개를 직접 확인해 주세요."))),
               fig("m5-09b", "10월 보고서 — 같은 모양, 다른 결과", browser("file:///C:/Users/금대리/Desktop/gj-report/output/월간보고_2026-10.html",
                                                              report_mock(10, OCT_VALUES, "3호기", OCT_LINES), tab="월간 생산 보고")))),
        st("5-10", "스킬 다듬기와 보관 위치", "스킬도 말로 고칠 수 있고, 어디에 두느냐에 따라 쓰이는 범위가 달라진다는 것을 압니다.",
           ["아래 요청문의 [ ]를 내 부서·이름으로 고쳐 보내기 → 권한 창 1. Yes", "<code>/monthly-report mes_sample_oct.xlsx</code> 다시 실행(덮어쓸지 물으면 ‘응’)",
            "크롬 새로고침 → 맨 아래 작성자 줄 확인", "아래 표에서 프로젝트 스킬과 개인 스킬의 차이 읽기"],
           extra=prompt(P_TUNE)
           + table(["종류", "두는 곳", "쓰이는 범위", "이럴 때"], [
               ["프로젝트 스킬", "프로젝트폴더\\.claude\\skills\\이름\\SKILL.md", "이 폴더에서만. 폴더를 공유하면 동료도 같이 씀", "이 업무 전용 방법(오늘 만든 것)"],
               ["개인 스킬", "C:\\Users\\내이름\\.claude\\skills\\이름\\SKILL.md", "내 PC의 모든 폴더", "어디서나 쓰는 내 습관(예: 회의록 5줄 요약)"]])
           + box("info", "동료에게 나누기", "<code>monthly-report</code> 폴더를 통째로 복사해 동료의 <code>.claude\\skills\\</code>에 넣으면 됩니다. 스킬 파일에 개인정보·기밀 숫자를 적지 않았는지 먼저 확인하세요."),
           ok="10월 보고서 맨 아래에 ‘작성: 관리팀 금대리 · 작성일’ 줄이 생겼습니다. 스킬을 고치면 다음 실행부터 바로 반영됩니다.",
           figure=fig("m5-10", "스킬 고치기 → 다시 실행", cc(cc_user("monthly-report 스킬에 규칙을 하나 추가해줘: 보고서 맨 아래에 '작성: 관리팀 금대리 · 작성일'…", n=1)
                                                    + cc_tool("Update(.claude\\skills\\monthly-report\\SKILL.md) — 1줄 추가")
                                                    + cc_user(P_RUN, n=2) + cc_ai("같은 이름의 파일이 있습니다. 덮어쓸까요?")))),

        # ── 3교시 ──
        section("3교시 · MCP 개념과 노션 연결", "약 45분"),
        st("5-11", "MCP가 무엇인지 이해하기", "클로가 내 폴더 밖의 도구(노션)를 쓰려면 무엇이 필요한지 압니다.",
           ["아래 설명과 그림(흐름)을 읽습니다.", "표에서 CLAUDE.md · 스킬 · MCP의 차이를 확인합니다.", "생각해 보기 질문에 답하고 정답을 펼쳐 봅니다."],
           extra=box("info", "한 문장으로", "<b>MCP(Model Context Protocol)</b>는 AI 일꾼이 바깥 프로그램과 이야기하는 <b>표준 연결 규격</b>입니다. "
                     "설비마다 케이블이 달랐다면 일일이 변환기를 만들어야 하지만, 규격이 하나면 꽂기만 하면 됩니다.")
           + flow([("클로", "내 PC의 일꾼"), ("MCP", "표준 커넥터 + 출입증"), ("노션", "바깥 도구의 페이지·데이터베이스")])
           + table(["", "CLAUDE.md", "스킬", "MCP"], [
               ["무엇", "항상 지킬 규칙", "일하는 방법(순서)", "바깥 도구로 가는 연결"],
               ["금진 비유", "안전수칙 게시물", "작업표준서", "협력사 출입증과 전용 통로"],
               ["없으면", "매번 규칙을 다시 설명", "매번 방법을 다시 설명", "결과를 내가 복사해 노션에 붙여넣기"],
               ["만드는 법", "말로 시킴(5-3)", "말로 시킴(5-7)", "명령 한 줄 + 로그인 허용(5-13, 5-14)"]])
           + box("warn", "연결하면 권한이 생깁니다", "MCP로 연결하면 클로는 <b>내가 볼 수 있는 노션 내용을 읽고 고칠 수</b> 있습니다. 그래서 ① 실습은 개인(실습용) 워크스페이스에서 "
                 "② 쓰기 전에는 내용을 먼저 보여 달라고 하고 ③ 데이터 신호등(빨강 금지)은 그대로 지킵니다. 회사 워크스페이스 연결은 관리자 확인 후에 합니다.")
           + '<details class="qa"><summary>생각해 보기: “매달 보고서를 같은 모양으로 만든다”와 “보고서를 노션에 올린다”는 각각 무엇으로 해결하나요?</summary>'
             "<p>같은 모양으로 만든다 → 스킬(방법). 노션에 올린다 → MCP(연결). 둘을 합치면 ‘만들고 올리기’까지 한 번에 됩니다(5-18).</p></details>",
           ok="‘스킬은 방법, MCP는 연결’이라고 말할 수 있으면 통과입니다.", one=True),
        st("5-12", "노션에 실습 페이지 준비", "클로가 찾아갈 목적지 페이지를 노션에 만들어 둡니다.",
           [f"크롬에서 {ui('notion.com')} 열고 로그인(계정이 없으면 개인 이메일로 무료 가입)", f"왼쪽 사이드바 {ui('개인 페이지')} 옆 {ui('＋')} 클릭",
            "제목에 <b>금진 AI 실습</b> 입력", "본문에 한 줄 입력: <b>이 페이지는 Claude Code MCP 실습용입니다.</b>"],
           ok="사이드바에 <b>금진 AI 실습</b> 페이지가 보이고 본문에 한 줄이 적혀 있습니다.",
           stuck="화면 이름은 버전에 따라 ‘새 페이지’ 또는 ‘페이지 추가’일 수 있습니다. 노션 무료 요금제로 충분합니다. 다른 사람 워크스페이스에 ‘게스트’로만 들어가 있으면 연결이 안 되니 내 워크스페이스에서 만드세요.",
           figure=fig("m5-12", "노션 새 페이지 — 제목과 한 줄", notion(
               nt_page("금진 AI 실습", mk("<p>이 페이지는 Claude Code MCP 실습용입니다.</p>", 4, block=True), icon="📄", title_mark=3),
               crumbs=("금진 AI 실습",), on="📄 금진 AI 실습", side_marks={"＋개인 페이지": 2}))),
        st("5-13", "노션 MCP 추가하기", "명령 한 줄로 노션으로 가는 통로를 등록합니다.",
           ["Claude Code 창에서 <code>/exit</code>로 나오기(PowerShell은 gj-report 폴더 그대로)", "아래 명령을 복사해 붙여넣고 Enter", "<code>claude mcp list</code> 입력"],
           extra=code_block("노션 MCP 추가", text=MCP_ADD, cid="c-mcp") + code_block("등록 확인", text="claude mcp list\n", cid="c-mcplist")
           + box("info", "명령 읽는 법", "<code>claude mcp add</code>(통로 추가) · <code>--transport http</code>(인터넷 주소로 연결) · <code>notion</code>(내가 붙인 이름) · 마지막은 노션이 공식으로 제공하는 MCP 주소입니다. "
                 "기본 설정에서는 <b>이 명령을 실행한 폴더(gj-report)에서만</b> 연결됩니다."),
           ok="<code>claude mcp list</code>에 <b>notion</b> 줄이 보이고 끝에 <b>Needs authentication</b>(인증 필요)이라고 나옵니다. 아직 로그인 전이라 정상입니다.",
           stuck="‘Failed to connect’가 나오면 회사 네트워크가 mcp.notion.com을 막은 경우입니다. 강사에게 알려 주세요. 주소를 잘못 넣었다면 <code>claude mcp remove notion</code> 후 다시 추가합니다.",
           figure=fig("m5-13", "추가 → 목록 확인", ps_window([
               ps_prompt(path=PROJ, cmd=MCP_ADD.strip(), n=2),
               html_line(span("dim", "Added HTTP MCP server notion with URL: https://mcp.notion.com/mcp to local config")), "",
               ps_prompt(path=PROJ, cmd="claude mcp list", n=3), html_line(span("dim", "Checking MCP server health...")),
               html_line("notion: https://mcp.notion.com/mcp (HTTP) - " + span("y", "! Needs authentication")), "", ps_prompt(path=PROJ, cursor=True)]))),
        st("5-14", "노션 로그인으로 허용하기", "브라우저에서 내 노션 계정으로 ‘연결해도 좋다’고 허용합니다.",
           ["<code>claude</code> 실행", "<code>/mcp</code> 입력 → Enter", f"목록에서 {ui('notion')} 선택 → {ui('Authenticate')}(인증) 선택 → 브라우저가 열림",
            f"브라우저에서 워크스페이스가 내 것인지 확인 → {ui('액세스 허용')}(또는 Allow access)", "터미널로 돌아와 <code>/mcp</code>에서 notion이 <b>connected</b>인지 확인"],
           extra=box("info", "비밀번호는 클로에게 가지 않습니다", "로그인은 노션 화면에서 직접 합니다. 클로는 ‘허용됨’이라는 출입증만 받습니다. 이 방식을 OAuth(오어스)라고 합니다."),
           ok="<code>/mcp</code> 목록의 notion 옆에 <b>✔ connected</b>가 보입니다.",
           stuck="브라우저가 안 열리면 터미널에 나온 주소를 복사해 크롬에 붙여넣으세요. 메뉴 문구는 버전에 따라 다를 수 있습니다 — ‘Authenticate’ 또는 ‘Login’처럼 인증을 뜻하는 항목을 고릅니다.",
           figure=figs(
               fig("m5-14a", "/mcp → notion → Authenticate", cc(cc_input("/mcp", n=2)
                                                               + cc_perm("Notion MCP Server", ["Authenticate", "Disable"], n=3, detail="Status: ! needs authentication"))),
               fig("m5-14b", "브라우저 — 노션 허용 화면(모형)", browser("https://www.notion.so/…/oauth", oauth_card(4), tab="Notion")))),

        # ── 4교시 ──
        section("4교시 · 노션 실습과 스킬·MCP 합치기", "약 50분 · 읽기 → 쓰기 → 고치기 순서"),
        box("info", "안전한 순서", "바깥 도구는 항상 <b>읽기 → 내용 확인 → 쓰기</b> 순서로 합니다. 쓰기 전에 “넣을 내용을 먼저 보여줘”를 습관으로 만드세요."),
        st("5-15", "읽기 — 노션 페이지 찾아 읽기", "클로가 노션에 실제로 닿는지 가장 안전한 ‘읽기’로 확인합니다.",
           ["아래 요청문을 붙여넣고 Enter", "권한 창에 <b>notion</b> 도구 이름이 보이는지 읽기", f"{ui('1. Yes')} 선택"],
           extra=prompt(P_READ)
           + box("info", "권한 창이 달라졌습니다", "이번에는 파일이 아니라 <b>노션 도구</b>(예: notion-search)를 써도 되는지 묻습니다. 무엇을 하려는지 읽고 허락하는 것은 똑같습니다."),
           ok="클로가 <b>“이 페이지는 Claude Code MCP 실습용입니다.”</b>라고 내가 쓴 문장을 그대로 알려 줍니다.",
           stuck="페이지를 못 찾으면 5-14에서 다른 워크스페이스를 골랐을 수 있습니다. <code>/mcp</code> → notion에서 다시 인증(Re-authenticate)하고 워크스페이스를 확인하세요.",
           figure=fig("m5-15", "노션 도구 사용 허락", cc(cc_user(P_READ, n=1)
                                                 + cc_perm("Do you want to use this tool?", ["Yes", "Yes, and don't ask again for this tool", "No"], n=3,
                                                           detail="notion - notion-search (MCP)  query: \"금진 AI 실습\"")))),
        st("5-16", "쓰기 — 10월 보고를 노션 페이지로", "보고서 요약을 노션 하위 페이지로 올립니다. 올리기 전에 내용을 먼저 봅니다.",
           ["아래 요청문을 붙여넣고 Enter", "클로가 보여 준 ‘넣을 내용’에서 숫자 확인(3호기 4.1%)", f"“좋아, 만들어줘” 보내기 → 권한 창 {ui('1. Yes')}",
            "크롬의 노션에서 ‘금진 AI 실습’ 아래 새 페이지 열어 보기"],
           extra=prompt(P_WRITE) + prompt("좋아, 만들어줘."),
           ok="노션 ‘금진 AI 실습’ 아래에 <b>2026년 10월 생산 보고</b> 페이지가 생기고, 요약 3줄과 표(전체 188,600m · 5,856m · 3.1%)가 들어 있습니다.",
           stuck="노션 화면에 안 보이면 새로고침(F5)하세요. 표 대신 글머리 목록으로 들어갔다면 “표로 바꿔줘”라고 보내면 됩니다.",
           figure=figs(
               fig("m5-16a", "내용 먼저 보기 → 만들기", cc(cc_user("노션 '금진 AI 실습' 페이지 아래에 '2026년 10월 생산 보고'라는 하위 페이지를…", n=1)
                                                  + cc_ai("넣을 내용입니다.\n요약: 전체 188,600m 생산, 불량률 3.1% / 최고 3호기 4.1% / 3호기 오븐 온도 확인 필요\n표: 1호기 2.1% · 2호기 3.1% · 3호기 4.1% · 전체 3.1%", n=2)
                                                  + cc_user("좋아, 만들어줘.", n=3))),
               fig("m5-16b", "노션에 생긴 하위 페이지", notion(
                   nt_page("2026년 10월 생산 보고", "<p>① 전체 188,600m 생산, 불량률 3.1%</p><p>② 불량률 최고: 3호기 4.1%</p><p>③ 3호기 오븐 온도 확인 필요</p>" + OCT_TABLE, icon="📄"),
                   crumbs=("금진 AI 실습", "2026년 10월 생산 보고"), on="📄 2026년 10월 생…", sub="📄 2026년 10월 생…", min_h=300)))),
        st("5-17", "데이터베이스 만들고 고치기", "노션 데이터베이스(표)를 말로 만들고, 한 건의 상태를 말로 바꿉니다.",
           ["첫 번째 요청문 보내기 → 권한 창 1. Yes", "노션에서 ‘불량 조치 목록’에 3건이 들어왔는지 확인", "두 번째 요청문 보내기 → 권한 창 1. Yes",
            "노션에서 첫 줄의 상태가 ‘진행 중’으로 바뀌었는지 확인"],
           extra=prompt(P_DB) + prompt(P_DB2),
           ok="‘불량 조치 목록’에 <b>3건</b>이 있고, ‘3호기 오븐 온도 센서 점검’의 상태가 <b>진행 중</b>입니다. 노션을 한 번도 클릭하지 않고 만들고 고쳤습니다.",
           stuck="데이터베이스를 만들 수 없다고 하면 “같은 내용을 ‘금진 AI 실습’ 페이지에 표로 넣어줘”로 바꿔 진행하세요. 속성 이름이 조금 다르게 만들어져도 3건과 상태 변경만 맞으면 통과입니다.",
           figure=fig("m5-17", "노션 — 불량 조치 목록(상태 변경 후)", notion(
               '<div style="padding:0 12px">' + nt_db(DB_COLS, DB_ROWS, name="불량 조치 목록", widths=[142, 50, 70, 98], plus_col=False, new_btn=False) + "</div>",
               crumbs=("금진 AI 실습", "불량 조치 목록"), on="🗂 불량 조치 목록", sub="🗂 불량 조치 목록", min_h=260))),
        st("5-18", "스킬 + MCP 합치기 — 만들고 올리기까지 한 번에", "스킬(방법)에 MCP(연결)를 넣어, 보고서 작성부터 노션 등록까지 명령 한 줄로 끝냅니다.",
           ["아래 요청문으로 스킬에 마지막 단계 추가 → 권한 창 1. Yes", "<code>/monthly-report mes_sample.xlsx</code> 실행(9월 파일 덮어쓰기는 ‘응’)",
            "“노션에 올릴까요?”라고 물으면 ‘응’ → 권한 창 1. Yes", "노션에서 <b>2026년 9월 생산 보고</b> 페이지 확인"],
           extra=prompt(P_COMBO) + prompt("/monthly-report mes_sample.xlsx")
           + box("ok", "오늘의 완성형", "<b>CLAUDE.md</b>(규칙) + <b>스킬</b>(방법) + <b>MCP</b>(연결). 다음 달에는 data 폴더에 새 엑셀을 넣고 <code>/monthly-report 파일이름</code> 한 줄이면 됩니다."),
           ok="노션 ‘금진 AI 실습’ 아래에 <b>2026년 9월 생산 보고</b>가 생기고 표에 <b>2호기 3.7%</b>, 전체 2.8%가 들어 있습니다.",
           stuck="묻지 않고 바로 올리려 하면 권한 창에서 3. No를 고르고 “올리기 전에 먼저 물어봐”라고 보낸 뒤 스킬에도 그 규칙을 적게 하세요.",
           figure=fig("m5-18", "명령 한 줄 → 보고서 → 노션", cc(cc_user("/monthly-report mes_sample.xlsx", n=2) + cc_tool("Skill(monthly-report) — data/mes_sample.xlsx")
                                                      + cc_ai("output/월간보고_2026-09.html 을 만들었습니다. 노션에 올릴까요?")
                                                      + cc_user("응", n=3) + cc_tool("notion - notion-create-pages (MCP) — 2026년 9월 생산 보고")))),
        st("5-19", "정리와 퇴장 체크", "연결을 관리하는 법을 알고, 오늘 만든 것을 점검합니다.",
           ["아래 6개 항목을 하나씩 확인", "연결 끊는 법 표를 읽어 두기(오늘은 끊지 않아도 됩니다)", "내 업무에서 스킬로 만들 반복 작업 1개를 포스트잇에 적기"],
           extra=table(["#", "확인 항목", "확인 방법"], [
               ["1", "프로젝트 폴더 틀", "gj-report 안에 data · docs · output"], ["2", "CLAUDE.md", "/memory 목록에 보임"],
               ["3", "스킬 파일", ".claude\\skills\\monthly-report\\SKILL.md"], ["4", "스킬 실행", "output에 9월·10월 보고서 2개"],
               ["5", "노션 연결", "/mcp 에서 notion connected"], ["6", "노션 결과", "생산 보고 페이지 2개 + 불량 조치 목록 3건"]])
           + table(["하고 싶은 것", "방법"], [
               ["연결 상태 보기", "claude mcp list 또는 Claude Code 안에서 /mcp"],
               ["이 PC에서 연결 지우기", "claude mcp remove notion"],
               ["노션 쪽에서 허용 취소", "노션 설정 → 연결(Connections)에서 Claude Code 연결 해제"],
               ["다른 폴더에서도 쓰기", "추가할 때 --scope user 를 붙임(익숙해진 뒤)"]])
           + box("no", "연결해도 신호등은 그대로", "노션에 올리는 것도 ‘AI에 넣는 것’과 같습니다. 빨강 자료(급여·인사·단가·원가·원청 자료)는 올리지 않고, 공유 범위가 넓은 페이지에는 노랑 자료도 가린 뒤 올립니다."),
           ok="6개 항목을 모두 확인했고, 스킬로 만들 내 업무 1개를 적었습니다.", one=True),
        '<div class="next-mod">' + box("ok", "모듈 5 완료!", "규칙은 폴더에, 방법은 스킬에, 바깥 도구는 MCP로. 이제 내 업무의 반복 작업을 하나씩 스킬로 옮겨 보세요.") + "</div>",
    ]), pc_note=PC)
