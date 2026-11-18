"""모듈 6 · 구글 시트 + Apps Script로 나만의 시트 앱 만들기 — Claude in Chrome(크롬 확장) 사이드 패널과 함께.
흐름: 확장 설치·사이드 패널 → 엑셀을 구글 시트로 → 클로에게 시트 읽히기 → 버튼 설계 인터뷰 → Apps Script로 버튼 하나씩(집계 → 표시 → 입력 창) → 검증·저장·공유.

사실 확인(2026-11-18, 공식 도움말):
- Claude in Chrome: Chrome 웹 스토어에서 'Chrome에 추가' → Claude 계정 로그인 → 퍼즐 아이콘에서 고정 → 툴바의 Claude 아이콘으로 사이드 패널.
  유료 요금제(Pro·Max·Ultra·Team·Enterprise)만. 크롬 외 브라우저·모바일 미지원.
  승인 방식(입력창 드롭다운): Manually approve / Automatically approve(기본) / Skip all approvals.
  사이트 권한 창: Allow this action / Always allow actions on this site / Decline. 권한 부여(authorizations)·민감 정보 입력·영구 삭제는 어떤 방식이든 사용자 확인.
  (support.claude.com/en/articles/12012173, /12902446)
- Apps Script 동작(onOpen 메뉴, 그림에 스크립트 할당, HtmlService 대화상자, 첫 실행 권한 승인)은 구글 시트 표준 기능.
정답 예시 코드: practice/m6_appscript/Code.gs · Input.html — 가짜 SpreadsheetApp으로 집계 2.7·3.7·1.9·2.8%, 3% 이상 26행, 입력 검증을 확인했다(실제 구글 시트 리허설 전).
"""
from pathlib import Path

from common import catchup, more, st, teach
from lessonkit import (E, app_window, box, cards, code_block, code_editor, dialog, dropdown, fig, figs, flow, gbtn, google_auth, kbd, mk,
                       prompt, section, sheets_window, sidebar, table, ui, wrap)
from mocks_geumjin import browser, progress_bar

ROOT = Path(__file__).resolve().parent.parent
CODE_GS = ROOT / "practice" / "m6_appscript" / "Code.gs"
INPUT_HTML = ROOT / "practice" / "m6_appscript" / "Input.html"
PC = "실습은 PC의 크롬에서 합니다. 휴대폰은 복습용으로 보세요. 그림은 탭하면 크게 볼 수 있습니다."
TITLE = "금진 생산관리 앱"
TABS = ("생산실적", "설계", "안내")

M6_CSS = r"""
.cp{display:flex;flex-direction:column;height:100%;font-size:11.5px}
.cp .b{border-radius:8px;padding:6px 8px;margin:4px 0;white-space:pre-wrap;line-height:1.5}
.cp .b.u{background:#f1efe8;align-self:flex-end;max-width:92%}
.cp .b.a{background:#fff;border:1px solid #ebe8e0}
.cp .b.a code{display:block;background:#1e1e1e;color:#d4d4d4;border-radius:5px;padding:5px 6px;margin-top:4px;font-size:10.5px;white-space:pre}
.cp .perm{border:1.5px solid #c96442;border-radius:8px;padding:6px 8px;margin:6px 0;background:#fffaf5}
.cp .perm div{border:1px solid #e3ddd2;border-radius:5px;padding:3px 6px;margin-top:4px;background:#fff}
.cp .perm div.on{background:#1d3a7a;color:#fff;border-color:#1d3a7a}
.cp .in{margin-top:auto;border:1px solid #d6d9de;border-radius:8px;padding:6px;color:#8a8f98;background:#fff}
.cp .mode{display:inline-block;border:1px solid #d6d9de;border-radius:10px;padding:1px 7px;margin-top:4px;color:#1d3a7a;background:#fff;font-size:10.5px}
.ws{background:#fff;padding:14px}.ws h4{font-size:16px;margin:0 0 4px}.ws p{color:#5f6368;margin:4px 0}
.ws .add{display:inline-block;background:#1a73e8;color:#fff;border-radius:16px;padding:6px 16px;font-weight:700;margin-top:8px}
.pz{background:#fff;border:1px solid #dadce0;border-radius:8px;box-shadow:0 4px 14px rgba(0,0,0,.15);padding:6px;width:220px;margin:6px 0 0 auto}
.pz div{display:flex;justify-content:space-between;padding:5px 6px;border-radius:5px}
.drw{display:inline-block;background:#1d3a7a;color:#fff;border-radius:8px;padding:6px 14px;font-weight:700;font-size:12px;box-shadow:0 2px 5px rgba(0,0,0,.2)}
.frm{font-size:12px}.frm label{display:block;color:#5f6368;margin-top:5px}.frm span.i{display:block;border:1px solid #ccc;border-radius:4px;padding:3px 6px}
"""

# ───────── 요청문(사이드 패널에 붙여넣기) ─────────
P64 = "지금 열려 있는 구글 시트의 '생산실적' 탭을 보고, 어떤 열이 있고 데이터가 몇 행인지, 호기별 불량률이 대략 어떤지 초보자용으로 설명해줘. 아직 아무것도 바꾸지 마."
P65A = """이 시트로 나만의 생산관리 앱을 만들고 싶어. 시트 위에 버튼(메뉴)을 몇 개 달 거야.
어떤 버튼이 있으면 좋을지 나에게 한 번에 하나씩 질문해서 같이 정해줘. 질문은 5개 이내로 하고, 아직 아무것도 만들지 마."""
P65B = "정한 내용을 '설계' 탭의 표(순서 | 버튼 이름 | 누르면 하는 일 | 필요한 입력 | 결과가 나오는 곳)에 한 줄에 버튼 하나씩 적어줘. 다른 탭은 건드리지 마."
P66 = "Apps Script가 무엇인지, 오늘 만들 버튼이 시트·메뉴·코드와 어떻게 연결되는지 초보자용으로 5줄로 설명해줘."
P67 = """'설계' 탭 1번 버튼(호기별 집계)을 Apps Script로 만들고 싶어.
- 시트를 열면 위쪽에 '🏭 금진 도구' 메뉴가 생기고, 그 안에 '① 호기별 집계'가 있게
- 누르면 '집계' 탭을 만들어(있으면 비우고) 호기, 생산량(m), 불량량(m), 불량률(%)과 맨 아래 전체 행을 적게
- 불량률 = 불량량 합계 ÷ 생산량 합계 × 100, 소수 첫째 자리. 생산실적 탭은 고치지 마
- Code.gs에 붙여넣을 코드 전체를 한 번에 보여줘. 내가 복사해서 붙여넣을게. 실행할 함수 이름도 알려줘."""
P68ERR = """실행했더니 아래 오류가 났어. 바로 고치지 말고 원인과 고칠 곳을 먼저 설명해줘.
[실행 로그의 빨간 오류를 그대로 붙여넣기]"""
P69 = "시트 위에 '집계' 버튼 그림을 넣고, 누르면 방금 만든 호기별 집계 함수가 실행되게 연결하는 방법을 한 단계씩 알려줘. 한 단계가 끝나면 내가 '다음'이라고 할게."
P610 = """2번 버튼(불량률 높은 행 표시)을 추가해줘.
- '🏭 금진 도구' 메뉴에 '② 불량률 높은 행 표시'를 더하고
- 생산실적 탭에서 행별 불량률(불량량 ÷ 생산량 × 100)이 3% 이상인 행을 연한 노란색으로 칠하게. 다시 누르면 지우고 새로 칠하게
- 1번 버튼은 그대로 두고, Code.gs 전체 코드를 다시 보여줘(통째로 바꿔 붙여넣을게)"""
P611 = """3번 버튼(실적 입력 창)을 추가해줘.
- 메뉴에 '③ 실적 입력 창'을 더하고, 누르면 작은 창이 떠서 생산일자·제품코드·호기·생산량·불량량(가동시간·오븐온도는 선택)을 넣게
- '추가하기'를 누르면 생산실적 맨 아래에 한 줄 더하고, 호기가 1~3이 아니거나 불량량이 생산량보다 크면 막고 이유를 보여줘
- 필요한 파일(Code.gs 전체, 새 HTML 파일의 이름과 내용)을 하나씩 보여주고, 어디에 붙여넣는지 알려줘"""
P613 = """이 시트 앱을 내 실제 업무에 맞게 바꾸고 싶어. 내 업무는 [예: 주간 주문 마감 집계]야.
어떤 버튼 3개가 있으면 좋을지 설계표(순서 | 버튼 이름 | 누르면 하는 일 | 필요한 입력 | 결과가 나오는 곳)로 제안만 해줘. 아직 만들지 마."""

SHEET_ROWS = [["생산일자", "제품코드", "호기", "생산량(m)", "불량량(m)", "가동시간(분)", "오븐온도(℃)"],
              ["2026-09-01", "8299-6", "1", "2950", "62", "454", "183"],
              ["2026-09-01", "7510-4", "2", "3300", "131", "441", "196"],
              ["2026-09-01", "9034-2", "3", "2600", "47", "463", "188"],
              ["2026-09-02", "5588-3", "1", "3850", "92", "407", "191"],
              ["…", "", "", "", "", "", ""]]
DESIGN_ROWS = [["순서", "버튼 이름", "누르면 하는 일", "필요한 입력", "결과가 나오는 곳"],
               ["1", "호기별 집계", "호기별 생산량·불량량·불량률(합계끼리 나눔)", "없음", "'집계' 탭"],
               ["2", "불량률 높은 행 표시", "행별 불량률 3% 이상인 행을 노랗게", "기준 3%", "생산실적 탭 색"],
               ["3", "실적 입력 창", "창에 입력 → 맨 아래 한 줄 추가, 틀린 값은 막기", "날짜·코드·호기·생산량·불량량", "생산실적 맨 아래"]]
SUM_ROWS = [["호기", "생산량(m)", "불량량(m)", "불량률(%)"], ["1호기", "69,150", "1,887", "2.7"], ["2호기", "75,450", "2,799", "3.7"],
            ["3호기", "75,150", "1,449", "1.9"], ["전체", "219,750", "6,135", "2.8"], ["", "", "", ""], ["대조: 66행", "", "", ""]]
CODE_HEAD = ["function onOpen() {", "  SpreadsheetApp.getUi()", "    .createMenu('🏭 금진 도구')", "    .addItem('① 호기별 집계', 'summarizeByLine')",
             "    .addToUi();", "}", "", "function summarizeByLine() {", "  // 생산실적 → 호기별 합계 → '집계' 탭", "  …", "}"]


def cpanel(msgs, marks=None, perm=None, perm_mark=None, mode="수동 승인", mode_mark=None, input_text="Claude에게 요청하기"):
    """크롬 사이드 패널의 Claude 모형. msgs=[('u'|'a', 텍스트 또는 ('code', 코드))], perm=권한 질문 문구."""
    marks = marks or {}
    out = []
    for i, (who, t) in enumerate(msgs):
        body = (E(t[0]) + f"<code>{E(t[1])}</code>") if isinstance(t, tuple) else E(t)
        h = f'<div class="b {who}">{body}</div>'
        out.append(mk(h, marks[i], block=True) if i in marks else h)
    if perm:
        p = (f'<div class="perm"><b>권한이 필요합니다</b><br>{E(perm)}<div class="on">이 작업만 허용</div>'
             '<div>이 사이트에서 항상 허용</div><div>거절</div></div>')
        out.append(mk(p, perm_mark, block=True) if perm_mark else p)
    md = f'<span class="mode">⏸ {E(mode)} ▾</span>'
    md = mk(md, mode_mark) if mode_mark else md
    out.append(f'<div class="in">{E(input_text)}<br>{md}</div>')
    return sidebar("✻ Claude", f'<div class="cp">{"".join(out)}</div>')


def sheet(rows=SHEET_ROWS, active="생산실적", tabs=TABS, overlay="", extra_menus=(), colors=None, marks=None, dd_for=None, tab_marks=None):
    return sheets_window(rows, title=TITLE, tabs=tabs, active=active, overlay=overlay, extra_menus=extra_menus, colors=colors,
                         marks=marks, dd_for=dd_for, tab_marks=tab_marks)


def m6_page():
    store = browser("https://chromewebstore.google.com/…/claude", '<div class="ws"><h4>✻ Claude</h4><p>제공: Anthropic · 브라우저에서 Claude와 함께 일하기</p>'
                    + mk('<span class="add">Chrome에 추가</span>', 2) + "</div>", tab="Chrome 웹 스토어")
    pin = app_window("Chrome", '<div style="text-align:right;color:#5f6368">🧩 ⋮</div><div class="pz"><b>확장 프로그램</b>'
                     + mk('<div><span>✻ Claude</span><span>📌</span></div>', 4, block=True) + "</div>", icon_color="#4285f4")
    auth_need = dialog("승인 필요", "이 스크립트를 실행하려면 승인이 필요합니다.", gbtn("취소") + mk(gbtn("권한 검토", primary=True), 3))
    drawing = ('<div style="padding:10px"><span class="drw">📊 집계</span></div>')
    assign = dialog("스크립트 할당", '<p>할당할 스크립트</p><div style="border-bottom:1px solid #1a73e8;padding:3px 0">summarizeByLine</div>',
                    gbtn("취소") + mk(gbtn("확인", primary=True), 4))
    form = dialog("생산 실적 입력", '<div class="frm"><label>생산일자</label><span class="i">2026-09-30</span><label>제품코드</label><span class="i">8299-6</span>'
                  '<label>호기 · 생산량(m) · 불량량(m)</label><span class="i">2 · 3000 · 90</span>'
                  '<div style="margin-top:6px;color:#1f8452">추가했습니다: 2026-09-30 2호기 3000m</div></div>', mk(gbtn("추가하기", primary=True), 3))
    hl = {i: "#fff1c2" for i in (2,)}

    return wrap("".join([
        progress_bar("모듈 6 진도"),
        section("모듈 6 · 구글 시트로 나만의 업무 앱 — 크롬 속 Claude와 함께", "4시간 · 크롬 + 구글 시트 + Apps Script"),
        box("info", "이 모듈에서 얻는 것", "엑셀 같은 표를 <b>내가 원하는 버튼으로 다루는 나만의 시트 앱</b>을 만듭니다. 크롬 오른쪽에 Claude를 띄워 두고(사이드 패널), "
            "시트를 같이 보면서 <b>① 무엇을 할 버튼인지 묻고 답하며 설계 → ② 버튼 하나씩 만들기 → ③ 눌러 보고 확인</b>을 반복합니다. 코드는 클로가 쓰고, 나는 설계하고 확인합니다."),
        flow([("1교시", "크롬 속 Claude · 시트 준비"), ("2교시", "버튼 설계 인터뷰"), ("3교시", "첫 버튼(집계) · 진짜 버튼 달기"), ("4교시", "버튼 더하기 · 검증 · 공유")]),
        teach([
            ["0:00 (15분)", "6-1", "설치는 미리 과제로 내 두면 좋음. 유료 요금제 계정인지 먼저 확인(무료는 사용 불가)", "툴바에 Claude 아이콘"],
            ["0:15 (10분)", "6-2", "승인 방식을 ‘수동 승인’으로 맞추게 함. 권한 창 세 줄을 소리 내어 읽기", "수동 승인 표시"],
            ["0:25 (10분)", "6-3", "가져오기 위치 ‘스프레드시트 바꾸기’를 강조. 회사 구글 계정 정책으로 막히면 개인 계정", "생산실적 66행"],
            ["0:35 (15분)", "6-4", "“아직 아무것도 바꾸지 마”가 왜 필요한지 다시 짚음", "66행 · 7열 답"],
            ["1:00 (30분)", "6-5", "버튼 설계 인터뷰. 클로 질문에 내 말로 답하게 함. 설계표 3줄이 핵심 산출물", "설계 탭 3줄"],
            ["1:30 (15분)", "6-6", "확장 프로그램 > Apps Script. ‘시트 = 화면, Apps Script = 버튼 뒤의 일꾼’ 비유", "빈 편집기"],
            ["1:55 (15분)", "6-7", "코드는 전체 선택 후 통째로 바꿔 붙여넣기. 저장 아이콘 확인", "저장됨"],
            ["2:10 (20분)", "6-8", "권한 승인 화면은 강사가 먼저 시연. ‘확인되지 않은 앱’은 내가 만든 스크립트라 뜨는 정상 화면", "2.7·3.7·1.9·2.8"],
            ["2:30 (15분)", "6-9", "그림 버튼 → 스크립트 할당. 클로가 한 단계씩 안내하게 함", "버튼 눌러 집계"],
            ["2:55 (15분)", "6-10", "버튼 하나 → 저장 → 실행 → 확인 리듬", "26행 노란색"],
            ["3:10 (25분)", "6-11", "HTML 파일 추가가 낯선 부분. 테스트로 넣은 행은 지우게 함", "입력 창으로 1행 추가"],
            ["3:35 (15분)", "6-12", "엑셀과 숫자 대조, 버전 이름 붙이기, 공유 범위", "대조 3칸 일치"],
            ["3:50 (10분)", "6-13", "내 업무용 버튼 3개 설계 제안 받기 → 발표 1명", "설계 제안"],
        ], note="시각에는 교시 사이 쉬는 시간 10분이 들어 있습니다. 6-11이 밀리면 정답 예시 코드를 붙여넣어 결과만 확인합니다. 준비물: 크롬, Claude 유료 요금제 계정, 구글 계정(회사 계정이면 Apps Script·외부 앱 승인이 허용되는지 미리 확인)."),
        cards([("🧩", "Claude in Chrome", "<p>크롬 확장 프로그램. 오른쪽 사이드 패널에서 지금 보는 화면을 같이 보며 일함.</p>"),
               ("📊", "구글 시트", "<p>앱의 화면과 데이터. 엑셀 파일을 가져와 씀.</p>"),
               ("⚙", "Apps Script", "<p>시트의 버튼 뒤에서 일하는 코드. 클로가 쓰고 나는 붙여넣고 확인.</p>")], cols=3),
        box("warn", "이 모듈의 약속 3가지", "① 승인 방식은 <b>수동 승인</b>으로 — 클로가 무엇을 하려는지 읽고 허락합니다. ② <b>구글 권한 승인 화면은 내가 직접</b> 누릅니다(클로에게 맡기지 않음). "
            "③ 실습은 <b>가상 데이터</b>로. 실데이터는 신호등 확인 후, 노랑은 가린 뒤에 씁니다."),

        # ── 1교시 ──
        section("1교시 · 크롬 속 Claude와 실습 시트 준비", "약 50분"),
        st("6-1", "Claude in Chrome 설치하고 고정하기", "크롬에 Claude 확장 프로그램을 설치하고, 툴바에서 바로 누를 수 있게 고정합니다.",
           [f"크롬에서 Chrome 웹 스토어를 열고 <b>Claude</b>(제공: Anthropic)를 찾기 — 아래 버튼으로 공식 소개 페이지를 열어도 됩니다"
            + '<div style="margin-top:8px"><a class="dl" href="https://claude.com/claude-in-chrome" target="_blank" rel="noopener">🌐 Claude in Chrome 공식 페이지</a></div>',
            f"{ui('Chrome에 추가')} → {ui('확장 프로그램 추가')}",
            "Claude 계정으로 로그인(웹 claude.ai와 같은 계정)",
            f"주소창 오른쪽 {ui('🧩')}(확장 프로그램) → Claude 옆 {ui('📌')}(고정) 누르기"],
           ok="크롬 툴바에 <b>Claude 아이콘</b>이 보입니다.",
           stuck="Claude in Chrome은 <b>유료 요금제(Pro·Max·Team·Enterprise)</b>에서만 됩니다. 무료 계정이면 강사에게 알려 주세요. 크롬이 아닌 브라우저(엣지 등)와 휴대폰에서는 안 됩니다. 회사 계정은 관리자가 막아 두었을 수 있습니다.",
           figure=figs(fig("m6-01a", "Chrome 웹 스토어 — Chrome에 추가", store), fig("m6-01b", "🧩 → Claude 고정", pin))),
        st("6-2", "사이드 패널 열고 승인 방식 정하기", "크롬 오른쪽에 Claude를 띄우고, 클로가 화면을 조작하기 전에 매번 묻도록 맞춥니다.",
           [f"툴바의 {ui('Claude 아이콘')}을 눌러 오른쪽에 사이드 패널 열기",
            f"입력창 아래 승인 방식 드롭다운에서 <b>수동 승인</b>(Manually approve) 고르기",
            "아래 표로 권한 창 선택지 세 가지를 읽기"],
           extra=table(["승인 방식", "뜻", "이 수업에서"], [
               ["수동 승인 (Manually approve)", "클릭·입력 하나하나 전에 묻는다", "<b>이것으로</b> — CLI의 manual mode와 같음"],
               ["자동 승인 (Automatically approve)", "안전 검사를 하며 알아서 진행(처음 기본값)", "익숙해진 뒤"],
               ["승인 모두 건너뛰기 (Skip all approvals)", "묻지도, 검사하지도 않음", "쓰지 않음"]], raw=True)
           + table(["권한 창 선택지", "뜻"], [["이 작업만 허용", "이번 한 번만"], ["이 사이트에서 항상 허용", "구글 시트에서는 계속 허락(익숙해진 뒤)"], ["거절", "하지 마"]])
           + box("info", "어떤 방식이든 꼭 묻는 것", "권한 부여(구글 로그인 허용 같은 것), 민감한 정보 입력, 영구 삭제는 승인 방식과 상관없이 Claude가 먼저 묻습니다. 결제·계정 만들기는 아예 하지 않습니다."),
           ok="사이드 패널이 열려 있고, 입력창 아래가 <b>수동 승인</b>입니다.",
           stuck="메뉴 이름은 버전·언어에 따라 영어로 보일 수 있습니다. 승인 방식 드롭다운이 안 보이면 사이드 패널 오른쪽 위 ⋮ 메뉴를 확인하세요.",
           figure=fig("m6-02", "오른쪽 사이드 패널 · 수동 승인", sheet(overlay=cpanel([("a", "안녕하세요. 지금 보고 있는 화면에서 무엇을 도와드릴까요?")], mode_mark=2)))),
        st("6-3", "실습 엑셀을 구글 시트로 가져오기", "가상 생산실적 엑셀을 구글 시트로 만들어 앱의 바탕으로 씁니다.",
           ["아래 버튼으로 <b>m6_sheet_app.xlsx</b> 내려받기"
            + '<div style="margin-top:8px"><a class="dl g" href="practice/m6_sheet_app.xlsx" download>📥 m6_sheet_app.xlsx (생산실적 66행 · 설계 탭)</a></div>',
            f"크롬 새 탭 주소창에 <code>sheets.new</code> 입력 → 빈 시트가 열림",
            f"{ui('파일')} → {ui('가져오기')} → {ui('업로드')} → 내려받은 파일 선택 → 가져오기 위치 <b>스프레드시트 바꾸기</b> → {ui('데이터 가져오기')}",
            f"왼쪽 위 제목을 <b>{TITLE}</b>으로 바꾸기"],
           ok="아래 탭에 <b>생산실적 · 설계 · 안내</b>가 있고, 생산실적 탭에 머리글 + <b>66행</b>이 있습니다.",
           stuck="‘새 스프레드시트 만들기’를 고르면 다른 파일로 열립니다. 그 파일을 쓰면 됩니다. 구글 드라이브에 엑셀을 그냥 올려 열면 엑셀 모드라 Apps Script가 안 보입니다 — 그때는 파일 → ‘Google 스프레드시트로 저장’을 합니다.",
           figure=fig("m6-03", "파일 → 가져오기 → 업로드", sheet(dd_for=("파일", dropdown(["새로 만들기", "열기", ("가져오기", 3), "-", "사본 만들기", "다운로드"])), marks={"파일": 3}))),
        st("6-4", "클로에게 시트 읽히기 — 아직 바꾸지 않기", "클로가 지금 열린 시트를 제대로 보고 있는지, 고치지 않고 설명만 듣습니다.",
           ["시트 탭이 앞에 보이는 상태에서, 사이드 패널 입력창에 아래 요청문 보내기" + prompt(P64),
            f"화면을 읽어도 되는지 묻는 권한 창이 뜨면 {ui('이 작업만 허용')}",
            "답에서 열 7개, 66행, 호기별 불량률(2호기가 가장 높음)을 확인"],
           ok="클로가 <b>열 7개 · 데이터 66행</b>을 말하고, 2호기 불량률이 가장 높다고 답합니다. 시트는 그대로입니다.",
           stuck="행 수를 다르게 말하면 “스크롤해서 마지막 행 번호까지 확인해줘”라고 보내세요. 클로는 화면을 보며 읽기 때문에, 큰 표는 조금씩 다르게 셀 수 있습니다 — 정확한 숫자는 6-8에서 코드로 계산합니다.",
           figure=fig("m6-04", "시트를 보고 설명만", sheet(overlay=cpanel([("u", P64), ("a", "‘생산실적’ 탭: 열 7개(생산일자·제품코드·호기·생산량·불량량·가동시간·오븐온도), 데이터 66행입니다.\n호기별로 보면 2호기 불량률이 가장 높아 보입니다.\n아무것도 바꾸지 않았습니다.")],
                                                                    marks={0: 1}, perm=None)))),

        # ── 2교시 ──
        section("2교시 · 버튼 설계 인터뷰", "약 45분 · 만들기 전에 묻고 답하기"),
        st("6-5", "클로와 버튼 설계하기 — 하나씩 묻고 답하기", "어떤 버튼을 만들지 클로의 질문에 답하며 정하고, ‘설계’ 탭에 표로 남깁니다.",
           ["아래 요청문을 보내고, 클로의 질문에 <b>내 말로</b> 하나씩 답하기(누가 쓰는지, 자주 하는 일, 결과를 어디서 보고 싶은지)" + prompt(P65A),
            "질문이 끝나면 클로가 정리한 버튼 목록을 읽고, 빼거나 바꿀 것을 말하기 — 오늘 실습은 아래 ‘설계 예시’ 3개로 맞추기",
            f"{ui('설계')} 탭을 연 뒤 아래 요청문 보내기 → 권한 창에서 무엇을 적으려는지 읽고 {ui('이 작업만 허용')}" + prompt(P65B),
            "설계 탭에 3줄이 생겼는지 확인"],
           extra=table(DESIGN_ROWS[0], DESIGN_ROWS[1:])
           + box("info", "왜 설계부터 하나요?", "버튼을 먼저 만들면 ‘이게 아닌데’가 반복됩니다. 무엇을 누르면 무슨 일이 생기고 결과가 어디에 나오는지를 먼저 표로 정하면, 클로에게 하나씩 정확히 시킬 수 있습니다(모듈 3의 설계서와 같은 생각)."),
           ok="‘설계’ 탭에 버튼 <b>3줄</b>(호기별 집계 · 불량률 높은 행 표시 · 실적 입력 창)이 적혀 있습니다.",
           stuck="클로가 질문 없이 바로 만들려 하면 권한 창에서 ‘거절’하고 “만들지 말고 질문만 해줘”라고 보내세요. 시트에 직접 적는 게 잘 안 되면 클로가 보여 준 표를 직접 붙여넣어도 됩니다.",
           figure=figs(
               fig("m6-05a", "질문에 하나씩 답하기", sheet(overlay=cpanel([("u", "이 시트로 나만의 생산관리 앱을 만들고 싶어. … 한 번에 하나씩 질문해서 같이 정해줘."),
                                                                         ("a", "질문 1/5: 이 앱은 누가, 언제 쓰나요?"), ("u", "생산팀이 매일 아침 회의 전에 봐요."),
                                                                         ("a", "질문 2/5: 매일 손으로 하는 일 중 가장 귀찮은 것은?")], marks={1: 1, 2: 1}))),
               fig("m6-05b", "‘설계’ 탭에 적힌 버튼 3개", sheet(rows=DESIGN_ROWS, active="설계", tab_marks={"설계": 3}, colors={0: "#fff4d6"})))),
        st("6-6", "Apps Script 편집기 열기", "버튼 뒤에서 일할 코드를 넣을 곳(Apps Script 편집기)을 열고 역할을 이해합니다.",
           [f"시트 메뉴 {ui('확장 프로그램')} → {ui('Apps Script')} → 새 탭에 편집기가 열림",
            f"왼쪽 위 ‘제목 없는 프로젝트’를 눌러 <b>{TITLE}</b>으로 이름 바꾸기",
            "사이드 패널에 아래 요청문을 보내 Apps Script가 무엇인지 듣기" + prompt(P66)],
           extra=table(["", "하는 일", "비유"], [["구글 시트", "데이터와 화면", "현장 현황판"], ["Apps Script", "버튼을 누르면 실행되는 코드", "현황판 뒤의 작업자"],
                                              ["메뉴·버튼", "코드를 부르는 손잡이", "작업 지시 버튼"], ["Claude(사이드 패널)", "코드를 쓰고 방법을 알려 줌", "옆자리 선배"]]),
           ok=f"Apps Script 편집기가 열리고, 프로젝트 이름이 <b>{TITLE}</b>입니다. Code.gs에 <code>function myFunction() {{}}</code>이 보입니다.",
           stuck="‘확장 프로그램’ 메뉴에 Apps Script가 없으면 회사 구글 계정에서 막아 둔 것입니다. 개인 구글 계정으로 6-3부터 다시 합니다. 엑셀 모드(.xlsx 표시)라면 6-3의 ‘Google 스프레드시트로 저장’을 먼저 합니다.",
           figure=figs(
               fig("m6-06a", "확장 프로그램 → Apps Script", sheet(dd_for=("확장 프로그램", dropdown(["부가기능", "매크로", ("Apps Script", 1)])), marks={"확장 프로그램": 1})),
               fig("m6-06b", "빈 편집기 — 프로젝트 이름 바꾸기", code_editor(["function myFunction() {", "", "}"], project=TITLE, marks={"project": 2})))),

        # ── 3교시 ──
        section("3교시 · 첫 버튼 — 호기별 집계", "약 55분 · 받기 → 붙여넣기 → 저장 → 실행 → 확인"),
        st("6-7", "1번 버튼 코드 받아 붙여넣기", "설계표 1번(호기별 집계)을 클로에게 부탁해 코드를 받고, 편집기에 붙여넣어 저장합니다.",
           ["시트 탭으로 돌아와 사이드 패널에 아래 요청문 보내기" + prompt(P67),
            "클로가 보여 준 코드 상자의 <b>복사</b> 누르기 → 함수 이름(예: summarizeByLine) 메모",
            f"Apps Script 탭으로 가서 Code.gs 안을 클릭 → {kbd('Ctrl', 'A')}(전체 선택) → {kbd('Ctrl', 'V')}(붙여넣기)",
            f"{ui('💾')}(프로젝트 저장) 또는 {kbd('Ctrl', 'S')}"],
           extra=box("info", "통째로 바꿔 붙여넣기", "부분만 찾아 고치면 괄호 하나가 빠져 오류가 나기 쉽습니다. 이 수업에서는 늘 <b>전체 코드를 다시 받아 통째로 바꿉니다</b>.")
           + box("ok", "(선택) 클로가 직접 넣게 하기", "“Apps Script 탭의 Code.gs를 방금 코드로 바꾸고 저장해줘”라고 하면 클로가 화면을 조작해 직접 넣습니다. 수동 승인으로 한 단계씩 지켜보고, 저장 뒤에는 코드 첫 줄·마지막 줄이 맞는지 직접 확인합니다. 편집기가 괄호를 자동으로 덧붙여 코드가 깨지면 복사·붙여넣기로 돌아옵니다."),
           ok="Code.gs에 <code>onOpen</code>과 집계 함수가 들어가 있고, 저장 표시(파일 이름 옆 점 없음)가 됐습니다.",
           stuck="급하면 정답 예시를 쓰세요 — 6-12 아래 ‘정답 예시 코드’의 Code.gs를 복사해 붙여넣습니다(버튼 3개가 모두 들어 있어 6-10·6-11 결과도 같이 나옵니다).",
           figure=figs(
               fig("m6-07a", "사이드 패널에서 코드 받기", sheet(overlay=cpanel([("u", "'설계' 탭 1번 버튼(호기별 집계)을 Apps Script로 만들고 싶어. …"),
                                                                           ("a", ("Code.gs에 붙여넣을 코드입니다. 실행할 함수: summarizeByLine", "function onOpen() {\n  SpreadsheetApp.getUi()\n    .createMenu('🏭 금진 도구')…\n}\nfunction summarizeByLine() { … }  [복사]"))],
                                                                          marks={0: 1, 1: 2}))),
               fig("m6-07b", "전체 선택 → 붙여넣기 → 저장", code_editor(CODE_HEAD, project=TITLE, fn="onOpen", marks={"save": 4})))),
        st("6-8", "실행하고 권한 승인하기 — 내가 직접", "집계 함수를 처음 실행하며 구글 권한을 승인하고, 결과 숫자를 확인합니다.",
           [f"편집기 위쪽 함수 선택에서 집계 함수(예: <b>summarizeByLine</b>) 고르기 → {ui('▷ 실행')}",
            f"‘승인 필요’ 창 → {ui('권한 검토')} → 내 구글 계정 선택",
            f"‘Google에서 확인하지 않은 앱’ 화면 → {ui('고급')} → {ui(TITLE + '(으)로 이동(안전하지 않음)')} → 권한 확인 후 {ui('허용')}(또는 모두 선택 → 계속)",
            "실행 로그에 ‘실행 완료’가 뜨면 시트 탭으로 가서 <b>집계</b> 탭 확인",
            "시트 탭을 새로고침(F5) → 위쪽 메뉴에 <b>🏭 금진 도구</b>가 생겼는지 확인"],
           extra=box("warn", "권한 승인은 내가 직접 누릅니다", "‘확인하지 않은 앱’은 <b>내가 방금 만든 스크립트</b>라서 뜨는 정상 화면입니다. 그래도 무엇을 허락하는지(이 스프레드시트 보기·수정 등) 읽고 직접 누릅니다. 클로에게 이 화면을 맡기지 않습니다."),
           ok="‘집계’ 탭에 <b>1호기 2.7 · 2호기 3.7 · 3호기 1.9 · 전체 2.8(%)</b>, 전체 생산량 <b>219,750</b> · 불량량 <b>6,135</b>가 나오고, 시트 위에 <b>🏭 금진 도구</b> 메뉴가 보입니다.",
           stuck="빨간 오류가 나면 실행 로그의 오류를 그대로 복사해 아래 요청문의 [ ]에 붙여 사이드 패널로 보냅니다." + prompt(P68ERR) + " “… 탭을 찾을 수 없습니다”는 탭 이름이 ‘생산실적’과 다를 때입니다. 회사 계정에서 ‘이 앱은 차단됨’이 나오면 관리자 정책이라 개인 구글 계정으로 합니다.",
           figure=figs(
               fig("m6-08a", "함수 고르고 ▷ 실행", code_editor(CODE_HEAD, project=TITLE, fn="summarizeByLine", marks={"fn": 1, "run": 1}, log=[("알림", "실행이 시작됨"), ("알림", "실행이 완료됨")])),
               fig("m6-08b", "승인 필요 → 권한 검토", sheet(overlay=auth_need)),
               fig("m6-08c", "확인하지 않은 앱 → 고급 → 이동", google_auth("unverified", app_name=TITLE).replace('data-n="1"', 'data-n="3"').replace('data-n="2"', 'data-n="3"')),
               fig("m6-08d", "결과 — 집계 탭과 새 메뉴", sheet(rows=SUM_ROWS, active="집계", tabs=("생산실적", "설계", "안내", "집계"), extra_menus=("🏭 금진 도구",),
                                                       marks={"🏭 금진 도구": 5}, tab_marks={"집계": 4}, colors={0: "#eef2f8", 4: "#f6f1e7"})))),
        st("6-9", "시트 위에 진짜 버튼 달기", "메뉴 말고, 시트 위에 누르는 버튼(그림)을 놓고 집계 함수를 연결합니다.",
           ["사이드 패널에 아래 요청문을 보내고, 클로의 안내를 한 단계씩 따라 하기" + prompt(P69),
            f"{ui('삽입')} → {ui('그림')} → 도형으로 둥근 사각형을 그리고 ‘📊 집계’라고 적기 → {ui('저장 후 닫기')}",
            f"시트에 생긴 그림을 클릭 → 오른쪽 위 {ui('⋮')} → {ui('스크립트 할당')}",
            f"함수 이름 <b>summarizeByLine</b>(클로가 알려 준 이름, 괄호 없이) 입력 → {ui('확인')} → 그림 밖을 클릭한 뒤 버튼 누르기"],
           ok="시트 위의 <b>📊 집계</b> 버튼을 누르면 ‘집계’ 탭이 새로 계산됩니다(오른쪽 아래에 ‘호기별 집계를 만들었습니다’ 알림).",
           stuck="버튼을 누르면 그림이 선택만 되고 실행이 안 되면, 그림 밖을 한 번 클릭한 뒤 다시 누릅니다. ‘스크립트 함수를 찾을 수 없음’은 함수 이름 오타 — 괄호 () 없이 정확히 씁니다.",
           figure=figs(
               fig("m6-09a", "그림 버튼 → ⋮ → 스크립트 할당", sheet(overlay='<div style="position:absolute;right:12px;top:110px">' + mk('<span class="drw">📊 집계 ⋮</span>', 3) + "</div>")),
               fig("m6-09b", "함수 이름 넣기", sheet(overlay=assign)))),

        # ── 4교시 ──
        section("4교시 · 버튼 더하기, 검증, 공유", "약 60분 · 버튼 하나 → 저장 → 실행 → 확인"),
        st("6-10", "2번 버튼 — 불량률 높은 행 표시", "설계표 2번 버튼을 더합니다. 1번이 망가지지 않게 ‘전체 코드 다시 받기’로 합니다.",
           ["시트 탭의 사이드 패널에 아래 요청문 보내기" + prompt(P610),
            "새 코드를 복사 → Apps Script의 Code.gs 전체 선택 → 붙여넣기 → 저장",
            "시트 새로고침 → 🏭 금진 도구 → ② 불량률 높은 행 표시 (처음이면 권한 승인을 한 번 더)",
            "노란 행 몇 개가 생겼는지 확인하고, ① 호기별 집계도 여전히 되는지 눌러 보기"],
           ok="생산실적 탭에서 불량률 3% 이상인 <b>26행</b>이 연한 노란색이 되고, ① 호기별 집계도 그대로 됩니다.",
           stuck="1번 버튼이 사라졌다면 새 코드에 1번이 빠진 것입니다. “1번 버튼 코드가 빠졌어. 1·2번이 다 들어간 전체 코드를 다시 줘”라고 보내세요. 행 수가 다르면 “3% 이상인 행이 몇 개인지 세는 방법을 알려줘”로 확인합니다.",
           figure=fig("m6-10", "불량률 3% 이상 행이 노랗게", sheet(extra_menus=("🏭 금진 도구",), colors={2: "#fff1c2"}, marks={"🏭 금진 도구": 3}))),
        st("6-11", "3번 버튼 — 실적 입력 창", "작은 입력 창을 띄워 실적을 넣는 버튼을 만듭니다. 틀린 값은 창이 막아 줍니다.",
           ["사이드 패널에 아래 요청문 보내기" + prompt(P611),
            f"Code.gs는 통째로 바꿔 붙여넣기 → Apps Script 왼쪽 {ui('파일 ＋')} → {ui('HTML')} → 클로가 알려 준 이름(예: Input) → 받은 HTML을 붙여넣기 → 저장",
            "시트 새로고침 → 🏭 금진 도구 → ③ 실적 입력 창 → 시험으로 한 줄 넣기(예: 2026-09-30 · 8299-6 · 2호기 · 3000 · 90)",
            "일부러 틀린 값(호기 4, 불량량 > 생산량)을 넣어 막히는지 확인 → 시험으로 넣은 행은 생산실적 맨 아래에서 지우기"],
           ok="입력 창으로 넣은 행이 생산실적 맨 아래에 생기고, 틀린 값은 <b>이유와 함께 막힙니다</b>. 시험 행을 지운 뒤 ① 집계를 누르면 다시 2.7·3.7·1.9입니다.",
           stuck="‘Input을 찾을 수 없음’은 HTML 파일 이름이 코드와 다를 때입니다(대소문자까지 같게). 창이 비어 보이면 HTML 파일을 저장했는지 확인하세요.",
           figure=fig("m6-11", "③ 실적 입력 창", sheet(extra_menus=("🏭 금진 도구",), overlay=form))),
        st("6-12", "검증 · 버전 이름 · 공유", "앱의 숫자를 원본과 대조하고, 잘된 상태에 이름을 붙여 두고, 공유할 때 지킬 것을 압니다.",
           ["대조: 처음 내려받은 엑셀에서 생산량·불량량 열 합계(219,750 · 6,135)와 66행을 확인해 ‘집계’ 탭과 비교",
            f"시트 {ui('파일')} → {ui('버전 기록')} → {ui('현재 버전 이름 지정')} → ‘버튼 3개 완성’",
            "아래 공유 체크를 읽기"],
           extra=table(["공유 체크", "내용"], [
               ["누구와", "편집 권한을 준 사람은 코드까지 볼 수 있고 고칠 수 있음. 보기만 할 사람에게는 ‘뷰어’로"],
               ["사본을 줄 때", "파일 → 사본 만들기를 하면 Apps Script도 함께 복사됨. 받는 사람은 처음 실행할 때 권한 승인을 다시 함"],
               ["데이터", "실데이터를 넣는다면 신호등 확인 · 거래처·연락처는 가린 뒤. 단가·원가는 넣지 않음"],
               ["되돌리기", "망가지면 파일 → 버전 기록에서 ‘버튼 3개 완성’으로 복원"]])
           + '<details class="qa"><summary>정답 예시 코드 (Code.gs · Input.html) — 막혔을 때만</summary>'
           + code_block("정답 예시 Code.gs", path=CODE_GS, cid="c-m6-code", tall=True, download_href="practice/m6_appscript/Code.gs")
           + code_block("정답 예시 Input.html (파일 ＋ → HTML → 이름 Input)", path=INPUT_HTML, cid="c-m6-html", tall=True, download_href="practice/m6_appscript/Input.html")
           + "</details>",
           ok="집계 탭의 숫자(66행 · 219,750 · 6,135 · 2.8%)가 원본 엑셀과 같고, 버전 기록에 ‘버튼 3개 완성’이 있습니다.",
           stuck="숫자가 다르면 6-11에서 넣은 시험 행이 남아 있는지 확인하세요. 버전 기록 메뉴 이름은 화면에 따라 ‘버전 기록 보기’일 수 있습니다."),
        st("6-13", "정리 — 내 업무용 시트 앱 설계해 보기", "오늘 방법을 내 업무에 옮길 수 있게, 내 업무용 버튼 3개를 설계 제안으로 받아 봅니다.",
           ["아래 퇴장 체크 6항목 확인",
            "사이드 패널에 아래 요청문의 [ ]를 내 업무로 바꿔 보내기 — 제안만 받기" + prompt(P613),
            "가장 먼저 만들고 싶은 버튼 1개를 포스트잇에 적기"],
           extra=table(["#", "퇴장 체크", "확인 방법"], [
               ["1", "크롬 속 Claude", "툴바 아이콘 · 수동 승인"], ["2", "시트", f"‘{TITLE}’에 생산실적·설계·집계 탭"],
               ["3", "설계표", "설계 탭 3줄"], ["4", "버튼 3개", "🏭 금진 도구 ①②③ + 시트 위 📊 집계 버튼"],
               ["5", "검증", "2.7·3.7·1.9·2.8% · 219,750 · 6,135"], ["6", "버전", "‘버튼 3개 완성’"]])
           + more("버튼을 하나 더 설계해 직접 만들어 보세요. 예: ‘이번 주 요약’ 버튼 — 최근 5일치만 골라 호기별 불량률을 집계 탭 옆에 적기."),
           ok="퇴장 체크 6항목을 확인했고, 내 업무용 버튼 3개 설계 제안을 받았습니다.", one=True),
        '<div class="next-mod">' + box("ok", "모듈 6 완료!", "표는 시트에, 버튼은 Apps Script에, 설계와 코드는 옆자리 Claude와 함께. 내 업무의 반복 작업을 버튼 하나로 바꿔 보세요.") + "</div>",
    ]), pc_note=PC)
