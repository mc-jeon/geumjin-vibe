"""모듈 5-1 · claude.ai 웹(또는 데스크톱 앱)에서 스킬과 커넥터(MCP).
모듈 5(Claude Code CLI)와 같은 일을 웹 화면에서 한다: 결과물 → 말로 스킬 만들기 → 스킬 올리기 → 스킬로 실행 → 커넥터(MCP)로 노션 연결.

사실 확인(2026-11-13, 공식 도움말):
- 스킬: 설정 > 기능(Capabilities)에서 '코드 실행 및 파일 생성'(새 화면: Create and edit files)을 켠다. 사용자 지정(Customize) > 스킬에서 켜고 끈다.
  직접 만든 스킬은 ZIP(최상위에 스킬 폴더, 폴더 이름 = name)으로 '＋ → 스킬 만들기(Create skill) → 스킬 업로드(Upload a skill)'.
  채팅에서는 명령이 아니라 스킬 이름을 말로 부른다. Anthropic 스킬(엑셀·워드·파워포인트·PDF, skill-creator)이 목록에 있다.
  (support.claude.com/en/articles/12512180, claude.com/docs/skills/how-to)
- 커넥터: 사용자 지정 > 커넥터 > ＋ 로 목록(디렉터리)에서 연결. 채팅 입력창 ＋(또는 /) > 커넥터에서 대화마다 켠다.
  주소로 추가: 추가(Add) > 사용자 지정(Custom) > 웹(Web) → 이름·MCP 주소. 무료 요금제는 사용자 지정 커넥터 1개.
  웹 커넥터는 Anthropic 서버에서 연결하므로 인터넷에 공개된 주소만 된다(내 PC에서 도는 MCP는 안 됨).
  (support.claude.com/en/articles/11176164, /11175166)
문서에 한국어 버튼 이름이 없어 화면 문구는 모형으로 그렸다 — 리허설에서 실제 문구를 확인한다.
"""
from pathlib import Path

from common import catchup, gate, st, teach
from ext import OCT_LINES, OCT_TABLE, OCT_VALUES, SEP_LINES, SEP_VALUES, report_mock
from lessonkit import E, app_window, box, cards, code_block, fig, figs, flow, kbd, mk, prompt, section, table, ui, wrap
from mocks_geumjin import browser, claude_web, progress_bar
from mocks_notion import make_side, nt_page, nt_window

ROOT = Path(__file__).resolve().parent.parent
WEB_SKILL = ROOT / "practice" / "skill_example_web" / "monthly-report" / "SKILL.md"
PC = "실습은 PC의 크롬(또는 Claude 데스크톱 앱)에서 합니다. 휴대폰은 복습용으로 보세요. 그림은 탭하면 크게 볼 수 있습니다."

W51_CSS = r"""
.cz{display:flex;min-height:230px;font-size:12.5px}
.cz-side{width:128px;background:#f6f4ef;border-right:1px solid #e6e2d8;padding:8px}
.cz-side div{padding:5px 8px;border-radius:6px;margin:2px 0;color:#3c4043}
.cz-side div.on{background:#fff;font-weight:700}
.cz-side div.sub{padding-left:20px;color:#5f6368}
.cz-main{flex:1;padding:12px 14px}
.cz-h{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.cz-h b{font-size:14px}
.cz-plus{border:1px solid #d6d9de;border-radius:6px;padding:2px 9px;font-weight:700;background:#fff}
.cz-row{display:flex;justify-content:space-between;align-items:center;border:1px solid #ebe8e0;border-radius:8px;padding:7px 10px;margin:5px 0;background:#fff}
.cz-row small{display:block;color:#8a8f98;font-size:11px}
.cz-tg{width:30px;height:16px;border-radius:9px;background:#c9ccd1;position:relative;flex:none}
.cz-tg::after{content:"";position:absolute;top:2px;left:2px;width:12px;height:12px;border-radius:50%;background:#fff}
.cz-tg.on{background:#c96442}.cz-tg.on::after{left:16px}
.cz-btn{border:1px solid #d6d9de;border-radius:6px;padding:2px 10px;background:#fff;font-size:11.5px}
.cz-btn.p{background:#1d3a7a;color:#fff;border-color:#1d3a7a}
.cz-dd{border:1px solid #d6d9de;border-radius:8px;background:#fff;box-shadow:0 4px 14px rgba(0,0,0,.12);padding:4px;width:170px;margin:4px 0 6px auto}
.cz-dd div{padding:5px 8px;border-radius:5px}.cz-dd div.on{background:#f1efe8;font-weight:700}
.cz-chip{display:inline-block;border:1px solid #d6d9de;border-radius:12px;padding:1px 8px;margin:2px;background:#fff}
"""

# ───────── 요청문 ─────────
PW_REPORT = """첨부한 엑셀은 교육용 가상 생산실적이야.
목적: 9월 생산실적을 호기별 불량률 중심으로 한눈에 보는 월간 보고서를 만들고 싶어.
결과 모양: HTML 한 파일. 맨 위 제목 '㈜금진 월간 생산 보고 · 2026년 9월', 그 아래 요약 3줄, 호기별 불량률 막대 차트 1개(가장 높은 호기만 주황색), 그 아래 호기별 생산량·불량량·불량률 표(맨 아래 전체 행)
불량률 = 불량량 합계 ÷ 생산량 합계 × 100, 소수 첫째 자리까지"""
PW_FIX1 = "배경을 베이지 톤으로 바꿔줘. 이것만 고쳐줘."
PW_FIX2 = "표 아래에 원본과 대조할 숫자(행 수, 전체 생산량 합계, 전체 불량량 합계)를 작은 글씨로 적어줘. 이것만 고쳐줘."
PW_SKILL = """방금 만든 월간 보고서가 마음에 들어. 다음 달에도 엑셀만 첨부하면 똑같이 만들 수 있게, 이 작업 방식을 스킬로 만들어줘.
이름은 monthly-report로 해줘.
claude.ai의 '사용자 지정 > 스킬'에 올릴 수 있게 ZIP 파일로 만들어 주고, 스킬 파일에 무엇을 적었는지 초보자용으로 알려줘."""
PW_ZIP = "스킬을 내려받을 수 있는 ZIP 파일로 만들어줘. ZIP 안에는 monthly-report 폴더가 있고, 그 안에 SKILL.md가 있어야 해."
PW_RUN = "monthly-report 스킬로 첨부한 엑셀의 월간 보고서를 만들어줘."
PW_N_READ = "노션에서 '금진 AI 실습' 페이지를 찾아서 무엇이 적혀 있는지 알려줘. 아직 아무것도 바꾸지 마."
PW_N_WRITE = """방금 만든 10월 보고서의 요약 3줄과 호기별 표(호기, 생산량, 불량량, 불량률)를 노션 '금진 AI 실습' 페이지 아래에 '2026년 10월 생산 보고(웹)'라는 하위 페이지로 올리고 싶어.
만들기 전에 넣을 내용을 먼저 보여줘."""

DL = '<div style="margin-top:8px">{}</div>'


def cz(on, body, side_marks=None):
    """claude.ai '사용자 지정' 화면 모형. on: '스킬' 또는 '커넥터'."""
    sm = side_marks or {}
    items = [("💬 채팅", ""), ("📁 프로젝트", ""), ("🧩 사용자 지정", ""), ("스킬", "sub"), ("커넥터", "sub")]
    side = ""
    for name, cls in items:
        c = (cls + (" on" if name == on else "")).strip()
        h = f'<div class="{c}">{E(name)}</div>'
        side += mk(h, sm[name], block=True) if name in sm else h
    return app_window("Claude — 사용자 지정", f'<div class="cz"><div class="cz-side">{side}</div><div class="cz-main">{body}</div></div>', icon_color="#c96442")


def row(name, desc, on=True, right=None):
    r = right if right is not None else f'<span class="cz-tg{" on" if on else ""}"></span>'
    return f'<div class="cz-row"><span><b>{E(name)}</b><small>{E(desc)}</small></span>{r}</div>'


def web51_page():
    skills_list = (row("Excel · Word · PowerPoint · PDF", "Anthropic · 파일을 만들 때 자동으로 씀")
                   + mk(row("skill-creator", "Anthropic · 스킬 만들기를 도와줌"), 3, block=True))
    skills_after = (row("monthly-report", "첨부한 생산실적 엑셀로 호기별 불량률 월간 보고서…")
                    + row("skill-creator", "Anthropic · 스킬 만들기를 도와줌") + row("Excel · Word · PowerPoint · PDF", "Anthropic"))
    upload_dd = '<div class="cz-dd">' + mk('<div class="on">⬆ 스킬 업로드</div>', 3, block=True) + "</div>"
    conn_list = (row("Notion", "페이지·데이터베이스 읽기·쓰기", right=mk('<span class="cz-btn p">연결</span>', 3))
                 + row("Google Drive", "문서 찾기·읽기", right='<span class="cz-btn">연결</span>')
                 + row("Slack", "채널 메시지 읽기·보내기", right='<span class="cz-btn">연결</span>'))
    oauth = ('<div style="max-width:300px;margin:6px auto;background:#fff;border:1px solid #e3e2e0;border-radius:10px;padding:14px;text-align:center">'
             '<div style="font-size:22px">🔗</div><b>Claude가 Notion 워크스페이스에 연결하려고 합니다</b>'
             '<div style="border:1px solid #e3e2e0;border-radius:6px;padding:4px 8px;margin:8px 0;text-align:left">🏠 금대리의 워크스페이스 ▾</div>'
             '<span class="cz-btn">취소</span> ' + mk('<span class="cz-btn p">액세스 허용</span>', 3) + "</div>")
    chat_menu = ('<div class="cz-dd" style="margin:0 auto 0 0"><div>📎 파일 추가</div>' + mk('<div class="on">🔌 커넥터 ›</div>', 1, block=True)
                 + '<div style="padding-left:18px">Notion <span class="cz-tg on" style="display:inline-block;vertical-align:middle"></span></div></div>')

    mcp_part = "".join([
        section("2교시 · 커넥터(MCP)로 노션 연결", "약 35분 · 읽기 → 내용 확인 → 쓰기"),
        st("웹-6", "커넥터 = 웹에서 부르는 MCP", "모듈 5에서 배운 MCP를 웹에서는 ‘커넥터’라고 부르고, 무엇이 같고 다른지 압니다.",
           ["아래 비교표를 읽습니다.", "주의 상자 두 개를 읽습니다.", "옆 사람에게 ‘웹 커넥터로는 내 PC의 MCP를 못 붙이는 이유’를 한 문장으로 말해 봅니다."],
           extra=table(["", "Claude Code(모듈 5)", "claude.ai 웹·앱(모듈 5-1)"], [
               ["부르는 이름", "MCP 서버", "커넥터(Connector)"],
               ["추가하는 곳", "PowerShell에서 claude mcp add …", "사용자 지정 > 커넥터 > ＋"],
               ["로그인 허용", "/mcp → Authenticate", "‘연결’ 누르면 노션 허용 화면"],
               ["쓰는 범위", "그 폴더에서만(기본)", "내 계정의 모든 대화. 대화마다 ＋ > 커넥터에서 켜고 끔"],
               ["내 PC에서 도는 MCP(5-21·5-22)", "등록 가능", "불가 — 인터넷에 공개된 주소(https://…)만"]])
           + box("warn", "웹 커넥터는 클라우드에서 연결합니다", "웹 커넥터는 내 PC가 아니라 Anthropic 서버가 바깥 서비스에 연결합니다. 그래서 회사 내부망·VPN 안의 시스템이나 내 PC에서 돌린 MCP는 웹에 붙일 수 없습니다. "
                 "그런 것은 Claude Code(모듈 5)나 데스크톱 앱에서 씁니다.")
           + box("no", "연결하면 권한이 생깁니다", "커넥터를 연결하면 클로가 내가 볼 수 있는 노션 내용을 읽고 고칠 수 있습니다. 실습은 개인 워크스페이스에서 하고, 쓰기 전에는 ‘먼저 보여줘’라고 합니다. 신호등(빨강 금지)은 그대로입니다."),
           ok="‘웹 커넥터는 인터넷에 공개된 서비스만, 내 PC의 MCP는 Claude Code로’라고 말할 수 있으면 통과입니다.", one=True),
        st("웹-7", "노션 커넥터 연결하기", "목록에서 노션 커넥터를 골라 내 노션 계정으로 연결을 허용합니다.",
           ["노션에 <b>금진 AI 실습</b> 페이지가 있는지 확인 — 없으면 5-12대로 만들기(제목 + 한 줄 ‘이 페이지는 Claude MCP 실습용입니다.’)",
            f"claude.ai 왼쪽 {ui('사용자 지정')} → {ui('커넥터')} → {ui('＋')}(커넥터 둘러보기)에서 <b>Notion</b> 찾기",
            f"{ui('연결')}(Connect) → 열린 노션 화면에서 워크스페이스가 내 것인지 확인 → {ui('액세스 허용')}",
            "커넥터 목록의 Notion 옆이 ‘연결됨’인지 확인"],
           ok="사용자 지정 > 커넥터 목록에 <b>Notion — 연결됨</b>이 보입니다.",
           stuck="노션 허용 화면이 안 뜨면 브라우저 팝업 차단을 확인하세요. 회사 계정(Team·Enterprise)은 관리자가 먼저 노션 커넥터를 허용해야 목록에 보입니다. 화면 문구는 버전·언어 설정에 따라 다를 수 있습니다.",
           figure=figs(
               fig("m51-07a", "사용자 지정 > 커넥터 > ＋ → Notion 연결", cz("커넥터", '<div class="cz-h"><b>커넥터 둘러보기</b><span class="cz-plus">＋</span></div>' + conn_list,
                                                                     side_marks={"커넥터": 2})),
               fig("m51-07b", "노션 허용 화면(모형)", browser("https://www.notion.so/…/oauth", oauth, tab="Notion")))),
        st("웹-8", "채팅에서 노션 쓰기 — 읽기 → 쓰기", "웹-5에서 만든 10월 보고서를 노션 하위 페이지로 올립니다. 올리기 전에 내용을 먼저 봅니다.",
           [f"웹-5 대화(10월 보고서)로 돌아가 입력창 왼쪽 {ui('＋')} → {ui('커넥터')} → <b>Notion</b> 켜기",
            f"아래 요청문을 보내고, 노션 도구를 써도 되는지 묻는 창에서 {ui('허용')} — 내가 쓴 한 줄이 그대로 나오는지 확인" + prompt(PW_N_READ),
            "아래 요청문을 보내고, 클로가 보여 준 ‘넣을 내용’에서 숫자 확인(3호기 4.1%) → “좋아, 만들어줘.” → 허용" + prompt(PW_N_WRITE) + prompt("좋아, 만들어줘."),
            "노션에서 ‘금진 AI 실습’ 아래 새 페이지 열어 보기"],
           ok="노션 ‘금진 AI 실습’ 아래에 <b>2026년 10월 생산 보고(웹)</b> 페이지가 생기고, 요약 3줄과 표(전체 188,600m · 5,856m · 3.1%)가 들어 있습니다.",
           stuck="노션을 못 찾는다고 하면 1번에서 Notion을 켰는지 다시 확인하세요(대화마다 켭니다). 허용 창이 계속 뜨는 게 번거로우면 ‘항상 허용’을 고를 수 있지만, 쓰기 도구는 처음에는 매번 확인하는 편이 안전합니다.",
           figure=figs(
               fig("m51-08a", "입력창 ＋ → 커넥터 → Notion 켜기", claude_web([("ai", "10월 월간 보고서를 만들었습니다. 3호기 4.1%가 가장 높습니다.")], input_text="", attach_mark=None)
                   .replace('<div class="inbox">', chat_menu + '<div class="inbox">', 1)),
               fig("m51-08b", "노션에 생긴 하위 페이지", nt_window(
                   nt_page("2026년 10월 생산 보고(웹)", "".join(f"<p>{i}. {E(x)}</p>" for i, x in enumerate(OCT_LINES, 1)) + OCT_TABLE, icon="📄"),
                   crumbs=("금진 AI 실습", "2026년 10월 생산 보고(웹)"), side_on="📄 2026년 10월 생…", min_h=280,
                   side_items=make_side("금대리의 워크스페이스", team_pages=(), my_pages=("📄 금진 AI 실습",), db="📄 2026년 10월 생…")), ))),
        st("웹-9", "(선택) 주소로 커넥터 추가하기 · 정리", "목록에 없는 서비스를 MCP 주소로 추가하는 방법과, 연결을 끊는 방법을 압니다.",
           [f"{ui('사용자 지정')} → {ui('커넥터')} → {ui('추가')} → {ui('사용자 지정')} → {ui('웹')} 메뉴가 있는 것만 확인(오늘은 추가하지 않아도 됩니다)",
            "아래 표에서 ‘주소로 추가’할 때 넣는 것과 지킬 것을 읽기",
            "아래 퇴장 체크 5항목 확인"],
           extra=table(["주소로 추가할 때", "내용"], [
               ["이름", "목록에 보일 이름(예: 사내 생산 시스템)"],
               ["주소", "https:// 로 시작하는 MCP 주소. 서비스 안내 문서나 전산 담당이 알려 줌"],
               ["로그인", "대부분 ‘지금 로그인’ → 그 서비스 화면에서 허용"],
               ["지킬 것", "출처를 모르는 주소는 넣지 않음 · 열쇠(API 키)는 전산 담당 확인 후 · 무료 요금제는 사용자 지정 커넥터 1개"]])
           + table(["#", "퇴장 체크", "확인 방법"], [
               ["1", "파일 기능", "설정 > 기능에서 ‘코드 실행 및 파일 생성’ 켜짐"], ["2", "내 스킬", "사용자 지정 > 스킬에 monthly-report 켜짐"],
               ["3", "스킬 실행", "10월 보고서가 9월과 같은 모양(2.1·3.1·4.1%)"], ["4", "노션 커넥터", "사용자 지정 > 커넥터에 Notion 연결됨"],
               ["5", "노션 결과", "‘2026년 10월 생산 보고(웹)’ 페이지"]])
           + box("info", "연결 끊기", "사용자 지정 > 커넥터에서 Notion을 고르고 ‘연결 해제’를 누릅니다. 노션 쪽 설정의 연결 목록에서도 지울 수 있습니다."),
           ok="퇴장 체크 5항목을 확인했습니다(시간상 건너뛴 단계는 제외).", one=True),
    ])

    return wrap("".join([
        progress_bar("모듈 5-1 진도"),
        section("모듈 5-1 · 웹에서 스킬과 커넥터(MCP)", "약 1시간 30분 · claude.ai 또는 Claude 데스크톱 앱"),
        box("info", "이 모듈은", "모듈 5에서 Claude Code(검은 창)로 한 일을 <b>claude.ai 웹 화면</b>에서 합니다. 설치가 어려운 PC, 평소 웹·앱으로 Claude를 쓰는 사람에게 맞습니다. "
            "같은 일을 두 가지 화면으로 해 보면 ‘스킬은 방법, MCP(커넥터)는 연결’이 더 분명해집니다."),
        flow([("1교시", "결과물 → 말로 스킬 만들기 → 올리기 → 실행"), ("2교시", "커넥터(MCP)로 노션 연결 → 읽기·쓰기")]),
        teach([
            ["0:00 (5분)", "웹-1", "설정 > 기능에서 파일 기능을 켰는지 손 들어 확인. 회사 계정이면 관리자 설정을 미리 확인", "스킬 목록 화면"],
            ["0:05 (15분)", "웹-2", "모듈 1의 1-9와 같은 흐름. 고치기는 한 번에 하나씩", "9월 2.7·3.7·1.9"],
            ["0:20 (10분)", "웹-3", "‘마음에 드니 스킬로 만들어줘’가 핵심. ZIP을 내려받았는지 확인", "monthly-report.zip"],
            ["0:30 (5분)", "웹-4", "업로드 실패는 대부분 ZIP 구조(폴더째 압축). 정답 예시 ZIP으로 대체 가능", "목록에 monthly-report"],
            ["0:35 (10분)", "웹-5", "새 대화에서 스킬 이름만 말로. 9월과 나란히 비교", "10월 2.1·3.1·4.1"],
            ["0:55 (5분)", "웹-6", "(승인코드로 연 뒤) 웹 커넥터는 클라우드에서 연결된다는 점 강조", "한 문장 설명"],
            ["1:00 (10분)", "웹-7", "노션 허용 화면을 강사가 먼저 시연. 워크스페이스 확인", "Notion 연결됨"],
            ["1:10 (15분)", "웹-8", "대화마다 ＋ > 커넥터에서 켜는 것을 놓치기 쉬움. 읽기 → 내용 확인 → 쓰기", "노션에 10월 보고"],
            ["1:25 (5분)", "웹-9", "주소로 추가는 메뉴 위치만. 퇴장 체크", "5항목"],
        ], note="시각에는 교시 사이 쉬는 시간 10분이 들어 있습니다. 2교시(웹-6~웹-9)는 모듈 5처럼 강사 승인코드로 엽니다. 실습 파일 내려받기가 막힌 PC는 강사가 USB나 사내 공유 폴더로 나눠 줍니다."),
        cards([("🧩", "스킬", "<p>사용자 지정 > 스킬. 내 계정의 모든 대화에서 쓰는 작업표준서.</p>"),
               ("🔌", "커넥터(MCP)", "<p>사용자 지정 > 커넥터. 노션 같은 바깥 서비스로 가는 연결.</p>"),
               ("💬", "대화", "<p>입력창 ＋에서 파일 첨부와 커넥터 켜기.</p>")], cols=3),
        catchup("모듈 5를 하지 않았어도 됩니다. 모듈 5를 했다면 개념은 같고 화면만 다릅니다."),

        section("1교시 · 결과물 → 스킬 만들기 → 올리기 → 실행", "약 45분"),
        st("웹-1", "준비 — 파일 기능 켜고 스킬 목록 보기", "웹에서 스킬을 쓰려면 파일 기능이 켜져 있어야 합니다. 켜고, 스킬이 모여 있는 곳을 확인합니다.",
           [f"claude.ai 왼쪽 아래 내 이름 → {ui('설정')} → {ui('기능')}에서 <b>코드 실행 및 파일 생성</b>(새 화면에서는 ‘파일 만들기 및 편집’) 켜기",
            f"왼쪽 사이드바 {ui('사용자 지정')} → {ui('스킬')} 열기",
            "Anthropic이 만든 기본 스킬(엑셀·워드·파워포인트·PDF, <b>skill-creator</b>)을 확인하고, skill-creator가 꺼져 있으면 켜기"],
           ok="사용자 지정 > 스킬 목록에 <b>skill-creator</b>가 켜져 있습니다.",
           stuck="메뉴 이름은 화면 버전과 언어 설정에 따라 다를 수 있습니다(영어 화면: Settings > Capabilities, Customize > Skills). 회사 계정(Team·Enterprise)은 관리자가 조직 설정에서 스킬을 켜야 보입니다.",
           figure=fig("m51-01", "사용자 지정 > 스킬", cz("스킬", '<div class="cz-h"><b>스킬</b><span class="cz-plus">＋</span></div>' + skills_list, side_marks={"스킬": 2}))),
        st("웹-2", "결과물 먼저 — 9월 보고서를 대화로 만들기", "모듈 5처럼 먼저 대화로 만들고 고쳐서 ‘이거다’ 싶은 결과를 얻습니다.",
           [f"새 대화 → 입력창 {ui('＋')} → {ui('파일 추가')} → <b>mes_sample.xlsx</b> 첨부"
            + DL.format('<a class="dl g" href="practice/mes_sample.xlsx" download>📥 mes_sample.xlsx (9월 가상 생산실적)</a>'),
            f"아래 요청문을 붙여넣고 {ui('↑')}" + prompt(PW_REPORT),
            "오른쪽 미리보기에서 불량률 확인",
            "하나씩 고치기 — 첫 번째 요청 → 확인 → 두 번째 요청" + prompt(PW_FIX1) + prompt(PW_FIX2)],
           ok="미리보기 보고서의 불량률이 <b>1호기 2.7% · 2호기 3.7% · 3호기 1.9% · 전체 2.8%</b>이고, 대조 숫자가 <b>66행 · 219,750m · 6,135m</b>입니다.",
           stuck="숫자가 다르면 “합계 불량량 ÷ 합계 생산량으로 다시 계산해줘”라고 보내세요. 엑셀이 첨부되지 않으면 웹-1의 파일 기능이 켜졌는지 확인합니다.",
           figure=fig("m51-02", "첨부 → 요청 → 미리보기", claude_web(
               [("user", "📎 mes_sample.xlsx\n첨부한 엑셀은 교육용 가상 생산실적이야. 목적: 9월 생산실적을…"), ("ai", "9월 월간 보고서를 만들었습니다.")],
               preview_html=report_mock(9, SEP_VALUES, "2호기", SEP_LINES), preview_title="월간보고_2026-09.html", attach_mark=1, marks={0: 2},
               preview_marks={"tab": 3}, input_text=""))),
        st("웹-3", "말로 스킬 만들기 — ‘마음에 드니 스킬로 만들어줘’", "방금의 작업 방법을 같은 대화에서 말 한 번으로 스킬 파일(ZIP)로 받습니다.",
           ["같은 대화에서 아래 요청문 보내기" + prompt(PW_SKILL),
            "클로가 만든 <b>monthly-report.zip</b>을 내려받기(파일 카드의 ⬇) — ZIP 대신 글만 보여 주면 아래 요청문을 보내기" + prompt(PW_ZIP),
            "클로의 설명에서 스킬 이름·언제 쓰는지(설명)·순서·계산식이 들어 있는지 확인하고, 아래 정답 예시와 비교"],
           extra=box("info", "화면에 ‘스킬 저장’ 같은 버튼이 보이면", "클로가 만든 스킬 옆에 바로 내 스킬로 저장하는 버튼이 보이는 화면도 있습니다. 그 버튼을 눌렀다면 웹-4는 목록에 생겼는지 확인만 합니다.")
           + code_block("정답 예시 SKILL.md (웹용 · 내 것과 문장이 달라도 괜찮습니다)", path=WEB_SKILL, cid="c-web-skill", tall=True, wrap=True,
                        download_href="practice/skill_example_web/monthly-report/SKILL.md")
           + catchup('ZIP을 못 받았으면 정답 예시 ZIP을 내려받아 웹-4로 갑니다. <a class="dl" href="practice/skill_example_web/monthly-report.zip" download>📥 monthly-report.zip (정답 예시)</a>'),
           ok="내려받기 폴더에 <b>monthly-report.zip</b>이 있습니다.",
           stuck="skill-creator가 꺼져 있어도 대부분 만들어 줍니다. 잘 안 되면 웹-1에서 skill-creator를 켜고 “skill-creator 스킬을 써서 만들어줘”라고 덧붙입니다.",
           figure=fig("m51-03", "같은 대화에서 ‘스킬로 만들어줘’", claude_web(
               [("user", "방금 만든 월간 보고서가 마음에 들어. … 스킬로 만들어줘. 이름은 monthly-report로 해줘."),
                ("ai", "monthly-report 스킬을 만들었습니다.\n📦 monthly-report.zip  ⬇\n스킬 파일에는 ① 언제 쓰는지 ② 계산식 ③ 보고서 모양 ④ 대조 숫자 보고를 적었습니다.")],
               marks={0: 1, 1: 2}, input_text=""))),
        st("웹-4", "스킬 올리기 — 사용자 지정 > 스킬", "내려받은 ZIP을 내 계정에 스킬로 올리고 켭니다.",
           [f"왼쪽 {ui('사용자 지정')} → {ui('스킬')}",
            f"{ui('＋')} → {ui('스킬 만들기')}(Create skill)",
            f"{ui('스킬 업로드')}(Upload a skill) → 내려받기 폴더의 <b>monthly-report.zip</b> 선택",
            "목록에 <b>monthly-report</b>가 생기고 켜져 있는지 확인"],
           ok="사용자 지정 > 스킬 목록에 <b>monthly-report</b>가 켜져 있습니다.",
           stuck="업로드가 안 되면 대부분 ZIP 모양 문제입니다. ZIP 안에 <b>monthly-report 폴더</b>가 있고 그 안에 SKILL.md가 있어야 합니다(파일만 압축하면 안 됨). 직접 압축할 때는 폴더를 오른쪽 클릭 → ‘압축(ZIP)’ 메뉴로 <b>폴더째</b> 압축합니다. 폴더 이름과 스킬 이름(name)이 같아야 합니다.",
           figure=figs(
               fig("m51-04a", "＋ → 스킬 만들기 → 스킬 업로드", cz("스킬", '<div class="cz-h"><b>스킬</b>' + mk('<span class="cz-plus">＋ 스킬 만들기</span>', 2) + "</div>" + upload_dd + skills_list.replace(' data-n="3"', ' data-n="x"'),
                                                              side_marks={"스킬": 1}).replace('<div class="mk" data-n="x">', "<div>")),
               fig("m51-04b", "목록에 생긴 내 스킬", cz("스킬", '<div class="cz-h"><b>스킬</b><span class="cz-plus">＋</span></div>' + mk(skills_after[:skills_after.index("</div>") + 6], 4, block=True)
                                                    + skills_after[skills_after.index("</div>") + 6:])))),
        st("웹-5", "스킬로 실행 — 10월 데이터", "새 대화에서 설명 없이 ‘스킬 이름 + 파일’만으로 같은 모양의 10월 보고서를 만듭니다.",
           ["새 대화 열기(앞 대화의 기억 없이 스킬만으로 되는지 보려고)",
            f"입력창 {ui('＋')} → {ui('파일 추가')} → <b>mes_sample_oct.xlsx</b> 첨부"
            + DL.format('<a class="dl g" href="practice/mes_sample_oct.xlsx" download>📥 mes_sample_oct.xlsx (10월 가상 생산실적)</a>'),
            "아래 요청문 보내기" + prompt(PW_RUN),
            "9월 보고서와 모양을 나란히 비교"],
           extra=box("info", "CLI(모듈 5)와 다른 점", "웹에는 <code>/monthly-report</code> 같은 명령 대신 <b>스킬 이름을 말로</b> 부릅니다. “10월 월간 보고서 만들어줘”처럼 말해도 설명(description)을 보고 스스로 꺼내 씁니다. "
                     "웹 스킬은 폴더가 아니라 <b>내 계정 전체</b>에 적용됩니다."),
           ok="9월과 <b>같은 모양</b>의 보고서가 나오고 <b>1호기 2.1% · 2호기 3.1% · 3호기 4.1% · 전체 3.1%</b>, 3호기 막대가 주황색입니다. 대조 숫자는 60행 · 188,600m · 5,856m.",
           stuck="스킬을 안 쓰고 제멋대로 만들면 웹-4에서 스킬이 켜져 있는지 확인하고 “monthly-report 스킬을 꼭 써서 다시 만들어줘”라고 보냅니다. 모양이 다르면 웹-3 대화로 돌아가 “스킬에 ○○ 규칙을 추가해서 ZIP으로 다시 만들어줘” → 웹-4에서 다시 올립니다.",
           figure=fig("m51-05", "새 대화 — 스킬 이름 + 파일만으로", claude_web(
               [("user", "📎 mes_sample_oct.xlsx\nmonthly-report 스킬로 첨부한 엑셀의 월간 보고서를 만들어줘."), ("ai", "monthly-report 스킬로 10월 보고서를 만들었습니다.\n대조용: 60행 · 188,600m · 5,856m")],
               preview_html=report_mock(10, OCT_VALUES, "3호기", OCT_LINES), preview_title="월간보고_2026-10.html", attach_mark=2, marks={0: 3}, input_text=""))),

        gate("m51mcp", "커넥터(MCP) 실습(2교시)은 강사가 열어 줍니다",
             "강사가 알려 주는 <b>승인코드</b>를 넣으면 웹-6 ~ 웹-9가 열립니다. 모듈 5에서 이미 열었다면 자동으로 열려 있습니다.", mcp_part),
        '<div class="next-mod">' + box("ok", "모듈 5-1 완료!", "웹에서도 ‘결과물 → 스킬 → 커넥터’ 순서는 같습니다. 반복하는 일은 스킬로, 바깥 서비스는 커넥터로 연결해 보세요.") + "</div>",
    ]), pc_note=PC)
