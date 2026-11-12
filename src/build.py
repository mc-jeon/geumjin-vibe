"""금진 바이브코딩 교안 빌드.
실행: python src/build.py .   → ./index.html
모듈 1·2는 이 파일, 모듈 3은 src/m3.py, 모듈 4는 src/m4.py, 모듈 5(스킬·MCP)는 src/ext.py.
모듈 3·4의 숫자는 src/answers.json(make_practice_m34.py 출력)에서 읽는다.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lessonkit import (E, Page, app_window, box, build, cards, code_block, dropdown, fig, figs, flow, hero, kbd, mk, prompt, section,
                       shot_list_section, step, table, ui, wrap)
from tips import tips_page
from common import COMMON_CSS, teach
from ext import EXT_CSS, ext_page
from m3 import m3_page
from m4 import m4_page
from mocks_notion import NT_CSS
from mocks_geumjin import (DEMO_CSS, GJ_CSS, PROGRESS_CSS, demo, PROGRESS_JS, bar_chart, browser, cc_ai, cc_input, cc_perm, cc_tool, cc_user,
                           cc_welcome, cc_window, checkbox, claude_web, dept_page, explorer, installer, passed, progress_bar,
                           ps_prompt, ps_window, start_search, wbtn)

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
SITE = "https://geumjin-vibe.edunfuture.workers.dev/"
DESK_CSS = """.dk{display:flex;min-height:200px}.dk-side{width:130px;background:#f6f4ef;border-right:1px solid #e6e2d8;padding:8px}.dk-tab{padding:6px 8px;border-radius:6px;margin:3px 0}.dk-tab.on{background:#fff;font-weight:700}.dk-tab.dim{color:#8a8f98}.dk-main{flex:1;padding:14px}.dk-main p{color:#5f6368;margin:6px 0 10px}.dk-in{margin-top:14px;border:1px solid #d6d9de;border-radius:10px;padding:8px 10px;color:#8a8f98}"""
MODE = "claude --permission-mode default"   # 수동 모드로 시작(권한 창이 매번 뜨게) — 최신 버전은 auto 모드가 기본
PC = "설치와 실습은 PC에서 합니다. 휴대폰은 복습용으로 보세요. 그림은 탭하면 크게 볼 수 있습니다."
DESK = "C:\\Users\\금대리\\Desktop"
WORK = DESK + "\\geumjin-vibe"


def st(no, title, goal, todo, ok, stuck=None, figure="", extra="", one=False):
    """단계 카드 + '통과' 체크(다음 단계 열기)."""
    return step(no, title, goal, todo, ok=ok + passed(), stuck=stuck, figure=figure, extra=extra, one=one)


def html_line(h):
    return ("html", h)


def span(cls, text):
    return f'<span class="{cls}">{E(text)}</span>'


# ════════════════════════════ 홈 ════════════════════════════
home = hero("㈜금진 · AI 실무 역량 과정", "말로 만드는<br><em>내 업무 도구</em>",
            "코딩을 몰라도 괜찮습니다. 내 업무를 말로 설명하면 AI 일꾼이 도구를 만들어 줍니다. 4시간짜리 모듈 4개를 단계마다 확인하며 따라가고, 마지막에 스킬과 MCP로 마무리합니다.") + wrap(
    section("이 과정에서 하는 것", "4시간 모듈 4개(16시간) + 마무리 모듈 5")
    + cards([("💡", "모듈 1 · 이해와 웹 체험", "바이브코딩이 무엇인지 알고, 설치 없이 웹에서 첫 페이지를 만듭니다."),
             ("🛠", "모듈 2 · CLI 환경 셋팅", "터미널을 열고 Git·Claude Code·Python을 설치해 내 PC 작업대를 꾸립니다."),
             ("📊", "모듈 3 · 데이터 기본기", "엑셀을 AI에게 읽히고 대시보드를 만든 뒤 원본과 대조합니다."),
             ("🏭", "모듈 4 · 부서별 실전", "부서별 트랙으로 내 업무 도구를 완성하고 공유합니다.")], cols=4)
    + box("info", "🔌 모듈 5 · 프로젝트 폴더, 스킬, MCP(노션)", '내 도구를 만든 뒤 마지막에 합니다. 잘된 작업 방법을 스킬 파일로 굳혀 명령 한 줄로 다시 쓰고, 바깥 도구(노션)를 MCP로 연결합니다. '
          '<a href="#m5" data-go="m5">모듈 5 열기</a>')
    + section("진행 순서")
    + flow([("모듈 1", "이해 + 웹 체험"), ("모듈 2", "CLI 작업대 준비"), ("모듈 3", "데이터 → 대시보드"), ("모듈 4", "부서별 도구 완성"), ("모듈 5", "스킬·MCP로 마무리")])
    + table(["모듈", "시간", "내용", "준비물"], [
        ["모듈 1", "4시간", "바이브코딩 개념·용어, Claude 웹에서 첫 페이지와 차트", "Claude 유료 계정, 크롬"],
        ["모듈 2", "4시간+ (현장 조절)", "PowerShell, Git·Claude Code·Python 설치, 첫 대화, 되돌리기", "노트북(설치 권한), 충전기"],
        ["모듈 3", "4시간", "폴더 틀·규칙 파일(CLAUDE.md), 데이터 읽히기·정제·대시보드·검증, 내 도구 설계서", "모듈 2 완료 PC"],
        ["모듈 4", "4시간", "부서별 트랙 A–E 실습, 검증·공유·시연", "설계서, 마스킹한 부서 데이터(없으면 샘플 데이터)"],
        ["모듈 5", "약 3시간 30분 (+ 심화 선택 약 60분)", "새 프로젝트 폴더(복습), 스킬 만들기·실행, MCP 개념과 노션 연결 실습. 심화: 날씨·엑셀 MCP 직접 만들기", "모듈 3 완료 PC, 노션 계정(무료 가능)"]])
    + section("꼭 지킬 원칙 3가지")
    + box("info", "1. 한 번에 하나씩", "AI에게 여러 가지를 한꺼번에 시키지 않습니다. 하나 바꾸고 확인하고 저장합니다.")
    + box("warn", "2. 결과는 원본과 대조", "AI도 틀릴 수 있습니다. 숫자는 원본 엑셀에서 3개 이상 직접 확인합니다.")
    + box("no", "3. 빨간 데이터는 넣지 않기", "급여·인사평가, 단가·원가, 회사 확인 전의 원청·기술 자료는 AI에 넣지 않습니다. 거래처·연락처는 가린 뒤에 넣습니다.")
    + section("이 교안 쓰는 법", "단계마다 통과 체크")
    + box("ok", "단계 카드", "🎯 목표 → 번호 순서대로 따라 하기 → ✅ 성공하면 → ⚠ 막히면. 글 번호와 그림의 빨간 번호가 같습니다.")
    + box("info", "통과 체크", "내 화면이 '성공하면'과 같으면 초록 체크를 누르세요. 다음 단계가 열리고 위쪽 진도 막대가 올라갑니다. 진도는 내 브라우저에만 저장됩니다. 복습할 때는 '전체 펼치기'를 누르세요.")
    + box("info", "🎬 강사 시연 상자", "보라색 ‘강사 시연’ 상자가 나오면 강사 화면과 같은 순서의 장면·요청문·명령이 들어 있습니다. 강사가 몇 번째 장면인지 짚으며 보고, 요청문과 명령은 복사해서 그대로 따라 할 수 있습니다.")
    + box("info", "🧑‍🏫 강사 진행표", "모듈마다 맨 위에 금색 ‘강사 진행표’가 접혀 있습니다. 시간 배분, 강사가 할 일, 다음 단계로 넘어가는 신호가 들어 있습니다. 강사는 이 표를 보며 시간을 조절합니다.")
    + box("info", "교실 신호", "모니터 위에 초록 카드(통과) 또는 빨강 카드(도움 필요)를 올려 주세요. 빨강 카드를 보면 보조강사가 갑니다.")
    + section("실습 파일")
    + '<a class="dl g" href="practice/mes_sample.xlsx" download>📥 가상 생산실적(엑셀)</a> <a class="dl" href="practice/mes_sample.csv" download>📥 같은 데이터(CSV)</a> '
    + '<a class="dl g" href="practice/mes_sample_oct.xlsx" download>📥 10월 생산실적(엑셀 · 모듈 5)</a>'
    + '<p style="margin-top:10px;color:var(--tx2)">실습 데이터는 모두 교육용 가상 데이터이며 실제 ㈜금진의 데이터가 아닙니다. 그림은 실제 화면을 단순화한 모형입니다.</p>')

# ════════════════════════════ 캐릭터·용어 ════════════════════════════
CHARS = [
    ("🧑‍💼", "#f3e9d2", "금대리 (주인공)", "여러분 자신", "“매주 엑셀 복붙만 2시간인데… 이걸 말로 시킬 수 있다고요?”"),
    ("🧭", "#e3ecfa", "바이브 코치", "강사 · 방향을 잡아 주는 사람", "“코드는 일꾼이 씁니다. 우리는 ‘무엇을, 왜’만 정확히 말하면 돼요.”"),
    ("🤖", "#fde3d6", "클로 (Claude Code 일꾼)", "메인 AI 일꾼 · 주황 작업복", "“수정하기 전에 계획을 먼저 보여드릴게요.”"),
    ("🤖", "#dff3e4", "코덱스 (Codex 일꾼)", "다른 회사의 코딩 일꾼 · 초록 작업복", "“명령창에서 바로 처리합니다.”"),
    ("🤖", "#dde9fb", "안티 (Antigravity 일꾼)", "구글의 일꾼 · 파란 작업복", "“편집기·터미널·브라우저를 오가며 일해요.”"),
    ("👨‍🍳", "#e6e8ee", "터미널 주방장", "터미널(CLI)", "“사진 메뉴판은 없습니다. 글로 쓴 주문서를 주세요.”"),
    ("🌐", "#e7f3fb", "브라우저 통역사", "브라우저와 HTML", "“HTML만 주시면 누구에게나 똑같이 보여드려요.”"),
    ("📸", "#f6e7f3", "세이브 카메라", "Git(저장·되돌리기)", "“찰칵! 지금 상태 저장. 망가지면 여기로 돌아와요.”"),
    ("📌", "#fff1d6", "게시판 관리인", "GitHub와 배포", "“여기 붙이면 주소 하나로 모두 봐요. 단, 비밀은 붙이지 마세요.”"),
    ("📦", "#eee6d8", "재료 상자", "데이터(엑셀·CSV)", "“저를 일꾼에게 주기 전에 기밀 칸은 가려 주세요.”"),
    ("🧰", "#e2f0ea", "공구함", "Python과 pip", "“엑셀 읽는 공구는 여기 있어요. 부품이 없으면 pip 배달원이 가져옵니다.”"),
]

STATIONS = [("1. 클릭과 글", "윈도우는 클릭, 터미널은 글로 시키기"), ("2. AI 일꾼", "AI 코딩 도구는 터미널에 산다"),
            ("3. 파일 형식", "웹의 언어는 HTML"), ("4. 로컬", "내 PC 파일은 공유가 번거롭다"),
            ("5. 배포", "주소(URL) 하나로 공유"), ("6. 무료 게시판", "간단한 건 GitHub 무료"),
            ("7. 정적", "무료는 고정 화면만"), ("8. 동적", "로그인·DB는 서버가 필요")]

CONCEPTS = [
    ("1. 챗봇과 AI 에이전트", "챗봇은 상담 창구입니다. 답은 주지만 엑셀에 옮기는 건 내 몫입니다. 에이전트는 현장에 투입된 작업자입니다. 내 폴더의 파일을 열고, 만들고, 실행하고, 결과를 보고합니다.",
     "엑셀 파일 10개를 합쳐 달라고 했을 때, 챗봇과 에이전트의 결과물은 각각 무엇일까요?"),
    ("2. 필요한 역량이 바뀌었다", "예전에는 용접기를 다루는 기능공(문법 암기)이 필요했습니다. 지금은 도면을 정확히 그리고 완성품을 검수하는 사람(업무 설명과 검증)이 더 중요합니다.",
     "우리 부서 업무를 가장 정확히 설명할 수 있는 사람은 누구일까요? — 바로 나입니다."),
    ("3. 프롬프트는 작업지시서", "작업지시서에 품목·수량·납기가 빠지면 현장이 멈춥니다. 프롬프트도 목적·재료·결과 모양·금지사항 4칸을 채워야 원하는 결과가 나옵니다.", ""),
    ("4. 한 번에 하나씩", "온도·속도·텐션을 한꺼번에 바꾸면 불량이 나도 원인을 모릅니다. AI에게도 수정을 하나씩 시키고, 잘되면 저장합니다.",
     "‘차트 추가하고 색도 바꾸고 필터도 넣어줘’를 세 번의 요청으로 나눠 보세요."),
    ("5. 환각과 검증", "초품 검사처럼, 첫 롤을 뜯어보지 않고 양산에 들어가지 않습니다. AI 결과도 원본 엑셀과 숫자 3개를 대조한 뒤 씁니다.",
     "AI가 ‘합계 12,250m’라고 했습니다. 어떻게 확인할까요?"),
    ("6. 되돌리기는 안전장치", "세이브 카메라로 작업할 때마다 사진을 찍어 둡니다. AI가 잘 되던 걸 망가뜨려도 사진 찍은 시점으로 돌아갑니다.", ""),
    ("7. 데이터 신호등", "초록은 바로 넣어도 됩니다(거래처명 없는 MES 가동·불량). 노랑은 가린 뒤 넣습니다(거래처 주문, 담당자 연락처). 빨강은 넣지 않습니다(급여·인사평가, 단가·원가, 원청 시스템 자료).",
     "내 업무 자료 3개를 신호등 색으로 분류해 보세요."),
]

TERMS = [  # 용어, 뜻, 금진 비유, 단계
    ("바이브코딩", "말로 설명하면 AI가 코드를 짜는 개발 방식", "반장이 작업지시서를 주면 숙련공이 설비를 돌리는 것", "1-1"),
    ("AI 에이전트", "답만 하지 않고 파일을 읽고 만들고 실행까지 하는 AI", "상담 창구가 아니라 현장에 투입되는 작업자", "1-1"),
    ("프롬프트(요청문)", "AI에게 주는 지시문. 이 교안에서는 ‘요청문’이라고 부름", "작업지시서", "1-6"),
    ("환각", "AI가 그럴듯하지만 틀린 내용을 말하는 것", "확인 안 하고 올린 ‘완료’ 보고", "1-1"),
    ("GUI", "버튼을 눌러 쓰는 화면", "터치패널로 설비 조작", "1-2"),
    ("터미널(CLI)", "글로 명령하는 화면", "설비에 수치를 직접 입력하는 설정 모드", "1-2"),
    ("HTML", "브라우저가 읽는 웹 문서의 언어", "어느 현장에서나 통하는 표준 규격 문서", "1-2"),
    ("CSV / 엑셀", "표 형태의 데이터 파일", "MES에서 뽑은 생산실적표", "1-2"),
    ("로컬 / 클라우드", "내 PC에 있는 것 / 인터넷 서버에 있는 것", "내 서랍 / 천안 물류센터 공용 창고", "1-2"),
    ("배포", "만든 것을 주소(URL)로 누구나 볼 수 있게 올리는 것", "완성품을 출하해 거래처가 받게 하는 것", "1-2"),
    ("정적 / 동적", "누구에게나 같은 화면 / 사용자마다 달라지는 화면", "인쇄된 카탈로그 / 주문받아 만드는 맞춤 생산", "1-2"),
    ("GitHub / 저장소(레포지토리)", "Git 이력을 인터넷에 보관하는 서비스 / 프로젝트 보관함", "본사 문서보관실과 그 안의 파일철", "1-2"),
    ("맥락(컨텍스트)", "AI가 지금 기억하고 있는 대화와 자료", "교대 때 넘기는 인수인계 노트", "2-15"),
    ("마스킹", "민감한 값을 코드로 바꿔 가리는 것", "거래처명을 C001처럼 바꾸기", "1-4"),
    ("API 키", "프로그램이 AI를 불러 쓸 때 내는 유료 출입증", "사내 출입카드 — 잃어버리면 남이 내 돈으로 씀", "참고"),
    ("아티팩트(미리보기)", "웹 Claude가 만든 결과물을 대화창 옆에 바로 보여주는 창", "시생산품을 바로 뜯어보는 검사대", "1-6"),
    ("폴더(프로젝트)", "AI 일꾼이 일하는 작업 공간", "일꾼에게 내준 작업대 하나", "1-10"),
    ("현재 위치(경로)", "터미널이 지금 있는 폴더. PS C:\\Users\\이름> 으로 표시", "배치도의 ‘현재 위치’ 표시", "2-2"),
    ("cd / dir", "폴더 이동 / 폴더 안 목록 보기", "다른 라인으로 가기 / 라인 설비 둘러보기", "2-3"),
    ("설치 / PATH", "프로그램을 깔고 어디 있는지 등록하는 것", "새 설비를 들여놓고 배치도에 위치를 적는 것", "2-7"),
    ("Python", "Claude Code가 엑셀을 읽고 계산할 때 쓰는 도구. 우리는 설치만 하고 코드는 일꾼이 씀", "일꾼 공구함의 ‘엑셀 읽는 공구’", "2-10"),
    ("pip / 패키지", "Python에 기능 묶음(패키지)을 내려받아 더하는 도구. 예: pandas, openpyxl", "공구함에 부품을 채워 주는 배달원", "2-12"),
    ("권한 요청", "Claude Code가 파일을 바꾸거나 명령을 실행하기 전에 허락을 묻는 창", "작업 전 반장 결재", "2-14"),
    ("수동 모드 / 자동 모드", "매번 허락을 묻는 방식(manual) / 안전하다고 판단한 일은 묻지 않고 하는 방식(auto). 이 과정은 수동 모드로 진행", "결재 후 작업 / 위임 전결", "2-14"),
    ("슬래시 명령", "/help, /clear처럼 Claude Code 안에서 쓰는 짧은 명령", "설비의 단축 버튼", "2-15"),
    ("토큰", "AI가 읽고 쓰는 글자 조각의 양. 사용량을 세는 단위", "일꾼의 연료 — 긴 대화·큰 파일일수록 많이 듦", "💡 탭"),
    ("모델(Fable·Opus·Sonnet·Haiku)", "같은 Claude 안에서 능력과 비용이 다른 등급. /model로 바꿈", "기술 고문 · 설계 반장 · 숙련 기능공 · 빠른 보조", "💡 탭"),
    ("Git / 커밋", "파일의 변경 이력을 저장하는 도구 / 저장 시점 하나", "변경점 관리대장과 그 한 줄", "2-20"),
    ("CLAUDE.md", "작업 폴더에 두는 규칙 파일. Claude Code가 매번 먼저 읽음", "현장 안전수칙 게시물", "3-3"),
    ("정제", "표기를 통일하고 쓸 수 없는 행을 빼서 계산할 수 있는 데이터로 만드는 것", "입고 검사 — 불량 원자재를 걸러 내기", "3-5"),
    ("대시보드", "여러 숫자를 차트와 카드로 한 화면에 모은 것", "현장 현황판", "3-6"),
    ("설계서", "무엇을 만들지 목적·데이터·화면·금지사항 4칸으로 적은 글", "도면", "3-10"),
    (".claude 폴더", "프로젝트 폴더 안의 Claude Code 전용 폴더. 스킬·설정이 들어 있음", "일꾼 전용 서랍", "5-2"),
    ("GitHub Pages", "GitHub 저장소의 HTML을 인터넷 주소로 보여 주는 무료 기능", "회사 게시판에 완성품 사진 붙이기", "4-6"),
    ("스킬(Skill)", "잘된 작업 방법을 적어 둔 파일(SKILL.md). /이름 으로 다시 실행", "작업표준서", "5-7"),
    ("MCP", "AI 일꾼이 노션 같은 바깥 프로그램과 연결되는 표준 규격", "협력사 출입증과 전용 통로(표준 커넥터)", "5-11"),
    ("API", "프로그램끼리 정보를 주고받는 출입구. 사이트가 열어 두면 MCP를 직접 만들어 연결할 수 있음", "거래처 전용 납품 창구", "5-20"),
    ("OAuth(허용 로그인)", "비밀번호를 넘기지 않고, 해당 서비스 화면에서 ‘연결 허용’만 해 주는 로그인 방식", "방문증 발급 — 열쇠는 주지 않음", "5-14"),
]

QUIZ = [
    ("Q1. 답만 하지 않고 내 폴더의 파일을 직접 만들고 실행까지 하는 AI를 무엇이라고 하나요?", "AI 에이전트 — 현장에 투입되는 작업자"),
    ("Q2. 브라우저가 읽는 웹 문서의 언어는?", "HTML — 누구 PC에나 있는 브라우저로 똑같이 보입니다"),
    ("Q3. 만든 것을 주소 하나로 누구나 볼 수 있게 올리는 것을 무엇이라고 하나요?", "배포"),
    ("Q4. 거래처명을 C001처럼 바꿔 가리는 것을 무엇이라고 하나요?", "마스킹"),
    ("Q5. AI가 그럴듯하지만 틀린 내용을 말하는 것은? 그리고 막는 방법은?", "환각 — 원본과 숫자 3개 이상 대조하기"),
]

char_html = '<div class="char-grid">' + "".join(
    f'<div class="char"><div class="av" style="background:{bg}">{ic}</div><div><b>{E(n)}</b><small>{E(r)}</small><span class="q">{E(q)}</span></div></div>'
    for ic, bg, n, r, q in CHARS) + "</div>"
N_TERMS_M1 = sum(1 for t in TERMS if t[3].startswith("1-"))
term_html = '<div class="term-grid">' + "".join(
    f'<details class="term"><summary>{E(t)} <small>{E(s)}</small></summary><p>{E(m)}</p><p class="an">🏭 {E(a)}</p></details>'
    for t, m, a, s in TERMS) + "</div>"
concept_html = "".join(
    box("info", c, E(d) + (f"<br><b>생각해 보기</b> {E(q)}" if q else "")) for c, d, q in CONCEPTS)
quiz_html = "".join(f'<details class="qa"><summary>{E(q)}</summary><p>정답: {E(a)}</p></details>' for q, a in QUIZ)

glossary = wrap(
    section("등장인물", "교안 전체에 나오는 캐릭터")
    + "<p>교안은 ‘금대리가 AI 일꾼에게 일을 시켜 내 도구를 얻는 이야기’로 이어집니다. AI 도구는 제품 로고 없이 작업복 색으로만 구분합니다.</p>"
    + char_html
    + section("개념 지도: 8개 정거장", "터미널에서 배포까지")
    + flow(STATIONS[:4]) + flow(STATIONS[4:])
    + section("개념 비유 7가지", "벽지 공장 현장에 빗대어")
    + concept_html
    + prompt("[나쁜 예]\n생산 대시보드 만들어줘.\n\n[좋은 예]\n목적: 호기별 주간 불량률을 한눈에 보고 싶어.\n재료: 이 폴더의 mes_sample.xlsx (컬럼: 생산일자, 호기, 생산량(m), 불량량(m))\n결과 모양: 호기 1~3별 불량률 막대차트 1개 + 주차 선택 필터, index.html 한 파일\n금지사항: 원본 엑셀은 수정하지 마. 수정 전에 계획부터 보여줘.")
    + section(f"용어 카드 {len(TERMS)}개", "누르면 뜻과 비유가 펼쳐집니다")
    + term_html
    + section("용어 퀴즈", "5문항 중 4개 이상 맞히면 통과")
    + quiz_html)

# ════════════════════════════ 모듈 1 ════════════════════════════
dept_v1 = dept_page()
dept_v2 = dept_page(color="#a7801f", items=("월말 결산 지원", "발주·거래 내역 정리", "시스템 간 자료 이관", "월간 보고서 작성"), button=True)
chart = bar_chart([("1호기", 2.7), ("2호기", 3.7), ("3호기", 1.9)])

P16 = """우리 [관리팀] 업무를 소개하는 웹 페이지를 HTML 한 파일로 만들어줘.
- 위쪽에 부서 이름과 '㈜금진'
- 주요 업무 3가지를 목록으로: [월말 결산 지원], [발주·거래 내역 정리], [시스템 간 자료 이관]
- 깔끔한 남색 계열 디자인"""
P19 = """첨부한 엑셀은 교육용 가상 생산실적이야.
호기별 불량률을 막대 차트로 보여주는 웹 페이지를 HTML 한 파일로 만들어줘.
- 불량률 = 호기별 불량량(m) 합계 ÷ 생산량(m) 합계 × 100, 소수 첫째 자리까지
- 차트 아래에 호기별 생산량·불량량·불량률 표"""

m1 = wrap(
    progress_bar("모듈 1 진도")
    + section("모듈 1 · 바이브코딩 이해와 웹에서 첫 코딩", "4시간 · 설치 없음")
    + flow([("1교시", "바이브코딩이란"), ("2교시", "개념 지도·용어·신호등"), ("3교시", "웹에서 첫 페이지"), ("4교시", "데이터 넣기·웹의 한계")])
    + teach([
        ["0:00 (30분)", "1교시 설명", "한 문장 메시지로 시작. 5개 블록(정의·배경·체험·이점·한계)을 질문으로 풀어 감. 등장인물 소개", "—"],
        ["0:30 (20분)", "1-1", "라이브 시연 12분(가상 MES → 대시보드, 장면 6개). 수정은 장면 4·5로 나눠 ‘한 번에 하나씩’을 보여 줌. 끝에 “제가 코드를 썼나요?” 질문. 포스트잇 5분", "포스트잇 전원 제출"],
        ["1:00 (20분)", "1-2", "캐릭터·용어 탭의 8개 정거장을 칠판에 그리며 설명. 짝에게 ‘배포’ 설명시키기", "짝 설명 완료"],
        ["1:20 (15분)", "1-3", "용어 카드 훑기 → 퀴즈 5문항 → 정답 공개", "4문항 이상"],
        ["1:35 (15분)", "1-4", "신호등 표를 금진 예시로 설명. 헷갈리는 자료는 ‘노랑’으로 보고 강사에게 묻게 함", "자료 3개 분류"],
        ["2:00 (10분)", "1-5", "로그인 확인. 안 되는 사람은 보조강사가 지원", "전원 새 대화 화면"],
        ["2:10 (15분)", "1-6", "요청문의 [ ]를 부서에 맞게 고치게 함. 첫 페이지가 뜨면 박수", "미리보기에 페이지"],
        ["2:25 (15분)", "1-7", "‘한 번에 하나씩’을 세 번 반복. 한꺼번에 시킨 사람의 화면을 예로 보여 줌", "수정 3회"],
        ["2:40 (10분)", "1-8", "내려받은 파일을 주소창 file:/// 로 확인시킴", "내 PC에서 열림"],
        ["3:00 (20분)", "1-9", "초록 데이터만 넣는다는 점을 다시 말하고, 숫자 2.7·3.7·1.9를 함께 확인", "차트 숫자 일치"],
        ["3:20 (10분)", "1-10", "웹의 불편함을 교육생 입으로 말하게 하고 CLI로 넘어가는 이유로 연결", "빈칸 4개"],
        ["3:30 (10분)", "1-11", "점검 4항목을 한 명씩 확인하고 문제 있는 PC를 기록 → 전산 담당에 전달", "점검 결과 수합"],
        ["3:40 (15분)", "1-12", "앱 설치는 시간이 남는 사람부터. 못 한 사람은 모듈 2 전까지 과제", "(선택)"],
    ], note="시각에는 교시 사이 쉬는 시간 10분이 들어 있습니다. 1-1 시연이 길어지면 장면 5(색 바꾸기)는 말로만 설명하고 넘어갑니다. 1-5에서 로그인이 안 되는 사람은 보조강사가 맡고 강사는 1-6으로 넘어갑니다. 1-12는 모듈 2의 따라잡기 경로를 위한 준비라, 시간이 없으면 과제로 돌립니다.")
    # ── 1교시 ──
    + section("1교시 · 바이브코딩이란", "약 50분")
    + box("info", "한 문장으로", "코드를 배우는 게 아니라, <b>내 업무를 말로 설명해서 도구를 얻는 법</b>을 배웁니다.")
    + "<h3>1. 바이브코딩은 정확히 무엇인가</h3><ul class='plain'>"
      "<li><b>정의</b> — 만들고 싶은 것을 일상 언어로 설명하면 AI가 코드를 작성·실행·수정합니다. 사람은 결과를 보고 “여기는 이렇게 바꿔줘”라고 방향을 잡습니다.</li>"
      "<li><b>용어의 유래</b> — 2025년 2월 안드레이 카파시(전 테슬라 AI 총괄, OpenAI 창립 멤버)가 “코드는 잊고 분위기(vibe)에 몸을 맡긴다”고 표현한 데서 시작됐습니다.</li>"
      "<li><b>오해 바로잡기</b> — 대충 만드는 것이 아닙니다. 무엇을·왜·어떤 순서로 하는지 아는 업무 담당자가 가장 잘할 수 있는 방식입니다.</li></ul>"
    + "<h3>2. 왜 지금인가</h3><ul class='plain'>"
      "<li>답만 하던 챗봇에서, 내 PC의 파일을 읽고 만들고 실행까지 하는 ‘AI 에이전트’(클로·코덱스·안티) 시대로 넘어왔습니다.</li>"
      "<li>“개발팀에 요청 → 일정 대기 → 외주”였던 작은 업무 도구를, 현업 담당자가 반나절에 직접 만들 수 있습니다.</li>"
      "<li>필요한 역량이 ‘문법 암기’에서 ‘업무를 정확히 설명하는 힘, 결과를 검증하는 눈’으로 바뀌었습니다.</li></ul>"
    + "<h3>3. 이 과정에서 직접 체험하는 것</h3>"
    + cards([("💬", "말 한마디로 페이지", "모듈 1·2"), ("📊", "엑셀 → 차트·표", "모듈 1·3"), ("🔁", "대화로 고쳐 나가기", "전 모듈"),
             ("🔗", "링크 하나로 공유", "모듈 4"), ("📸", "틀리면 되돌리기", "모듈 2~")], cols=3)
    + "<h3>4. 앞으로 업무에 무엇이 좋아지나</h3>"
    + table(["이점", "금진 업무에서의 모습(예시)"], [
        ["반복업무 자동화", "매주 손으로 합치던 엑셀 보고서를 버튼 하나로 생성"],
        ["내 업무에 딱 맞는 도구", "시중 솔루션 대신 우리 부서 양식·용어 그대로 만든 현황판"],
        ["아이디어 검증 속도", "기획서 대신 작동하는 시제품으로 회의·보고"],
        ["부서 간 소통", "링크 하나로 같은 데이터를 보는 공용 화면"],
        ["비용·의존도 감소", "간단한 도구는 외주 없이 내부에서 해결"]])
    + "<h3>5. 한계와 안전 수칙</h3>"
    + box("warn", "AI는 틀릴 수 있습니다", "계산 결과는 원본과 대조하는 습관을 들입니다.")
    + box("no", "공개 배포 금지 자료", "개인정보·기밀 데이터는 외부 공개 배포(GitHub Pages)에 올리지 않습니다.")
    + box("info", "삭제·배포는 확인 후", "AI에게 바로 맡기지 말고 변경 내용을 먼저 확인합니다.")
    + st("1-1", "강사 시연 보고 한 줄 적기", "AI 일꾼이 10분 만에 도구를 만드는 장면을 보고, 내가 맡기고 싶은 일을 정합니다.",
         [f"아래 {ui('🎬 강사 시연')} 상자를 열어 두고 강사 화면을 봅니다.",
          "강사가 지금 몇 번째 장면인지 상자에서 짚으며 따라갑니다. 요청문은 상자에 있는 그대로입니다.",
          "(선택) claude.ai에 로그인돼 있다면 mes_sample.xlsx를 첨부하고 같은 요청문을 붙여넣어 함께 해 봅니다.",
          "포스트잇에 “AI 일꾼에게 가장 먼저 맡기고 싶은 일” 1줄을 적어 칠판에 붙입니다."],
         extra=demo("가상 MES 데이터 → 10분 대시보드",
                    "강사는 모듈 2에서 배울 화면(PowerShell + Claude Code)으로 시연합니다. 지금은 화면 흐름만 따라오면 됩니다. "
                    "데이터는 홈 탭의 가상 생산실적(mes_sample.xlsx)과 같습니다.",
                    [{"do": "빈 작업 폴더 <code>demo</code>에 mes_sample.xlsx를 넣고 <code>claude</code>를 실행합니다.",
                      "see": "Claude Code 시작 화면과 입력칸(&gt;)이 보입니다."},
                     {"do": "데이터를 먼저 읽힙니다 — 고치지 말고 설명만 하라고 합니다.",
                      "say": "이 폴더의 엑셀 파일을 열어서 어떤 컬럼이 있고, 이상해 보이는 값은 몇 개인지 초보자용으로 설명해줘. 아직 수정하지 마.",
                      "see": "컬럼 7개(생산일자·제품코드·호기·생산량·불량량·가동시간·오븐온도), 66행, 9월 평일 1~3호기라는 설명이 나옵니다."},
                     {"do": "대시보드를 만들어 달라고 합니다. 권한 창이 뜨면 <b>1. Yes</b>를 고릅니다.",
                      "say": "호기별 불량률(불량량÷생산량)을 막대 차트로 보여주는 index.html을 만들어줘.\n이상한 값은 계산에서 빼고, 뺀 건수는 화면 아래에 표시해줘. 원본 엑셀은 수정하지 마.",
                      "see": "폴더에 index.html이 생기고, 크롬에서 열면 <b>1호기 2.7% · 2호기 3.7% · 3호기 1.9%</b> 막대가 보입니다."},
                     {"do": "대화로 고칩니다 — 먼저 기능 하나만 더합니다.",
                      "say": "요일별로도 볼 수 있게 선택 버튼을 추가해줘.",
                      "see": "크롬을 새로고침하면 차트 위에 요일 버튼이 생깁니다. 눌러 보고 되는 것을 확인한 뒤 다음 요청으로 갑니다."},
                     {"do": "확인했으면 색 하나만 바꿉니다 — 한 번에 하나씩.",
                      "say": "금진 느낌이 나도록 베이지와 남색 톤으로 바꿔줘.",
                      "see": "크롬을 새로고침하면 색만 바뀌고, 방금 넣은 요일 버튼은 그대로 있습니다."},
                     {"do": "강사가 묻습니다: “제가 코드를 한 줄이라도 썼나요?”", "see": "답은 ‘아니요’. 말로 설명하고 결과를 확인했을 뿐입니다."}],
                    follow="같은 흐름을 <b>1-9</b>(웹에서 엑셀 → 차트)와 <b>모듈 3</b>(CLI로 데이터 → 대시보드)에서 직접 합니다."),
         ok="시연 장면 6개를 따라갔고, 포스트잇이 칠판에 붙어 있으면 통과입니다. 포스트잇은 모듈 3(3-10)에서 설계서를 쓸 때 다시 봅니다.",
         figure=figs(
             fig("m1-01a", "시연 장면 2 — 데이터 읽히기", cc_window(
                 cc_welcome(cwd="demo") + cc_user("이 폴더의 엑셀 파일을 열어서 어떤 컬럼이 있고, 이상해 보이는 값은 몇 개인지 설명해줘. 아직 수정하지 마.")
                 + cc_ai("mes_sample.xlsx — 66행, 컬럼 7개\n생산일자 · 제품코드 · 호기 · 생산량(m) · 불량량(m) · 가동시간(분) · 오븐온도(℃)\n이상해 보이는 값: 없음",),
                 path="C:\\Users\\강사\\Desktop\\demo")),
             fig("m1-01b", "시연 장면 3 — 권한 창에서 1. Yes", cc_window(
                 cc_user("호기별 불량률을 막대 차트로 보여주는 index.html을 만들어줘…")
                 + cc_perm("Do you want to create index.html?", ["Yes", "Yes, allow all edits during this session", "No"])
                 + cc_tool("Write(index.html) — 차트 + 호기별 표"), path="C:\\Users\\강사\\Desktop\\demo")),
             fig("m1-01c", "시연 장면 3 결과 — 크롬에서 연 대시보드", browser(
                 "file:///C:/Users/강사/Desktop/demo/index.html", chart, tab="호기별 불량률"))))
    # ── 2교시 ──
    + section("2교시 · 개념 지도, 용어, 데이터 신호등", "약 50분")
    + st("1-2", "개념 지도 8개 정거장", "터미널에서 배포까지 큰 그림을 캐릭터로 이해합니다.",
         [f"{ui('캐릭터·용어')} 탭의 ‘개념 지도’를 엽니다.", "강사 설명을 들으며 정거장 1~8을 차례로 짚습니다.",
          "옆 사람에게 ‘배포’가 무엇인지 한 문장으로 설명해 봅니다."],
         ok="‘HTML 파일을 주소 하나로 공유하는 것이 배포’라고 말할 수 있으면 통과입니다.",
         extra=flow(STATIONS[:4]) + flow(STATIONS[4:]), one=True)
    + st("1-3", "용어 카드와 퀴즈", f"앞으로 계속 나올 용어 {N_TERMS_M1}개를 익힙니다.",
         [f"{ui('캐릭터·용어')} 탭의 용어 카드를 눌러 뜻과 비유를 봅니다(1-1~1-10 표시 카드).", "아래 퀴즈 5문항을 풉니다.", "정답을 펼쳐 확인합니다."],
         ok="5문항 중 4개 이상 맞히면 통과입니다.", extra=quiz_html, one=True)
    + st("1-4", "데이터 신호등", "AI에 넣어도 되는 자료와 안 되는 자료를 구분합니다.",
         ["아래 신호등 표를 읽습니다.", "내 업무 자료 3개를 떠올립니다.", "자료마다 초록·노랑·빨강 중 하나를 정해 메모합니다."],
         ok="3개 모두 색을 정했고, 노랑은 무엇을 가릴지까지 말할 수 있으면 통과입니다.",
         extra=table(["신호", "뜻", "금진 예시"], [
             ['<span class="light l-g"></span>초록', "바로 넣어도 됨", "거래처명 없는 MES 가동·불량 데이터, 공개 카탈로그 문구"],
             ['<span class="light l-y"></span>노랑', "가린(마스킹) 뒤 넣기", "거래처 주문 내역(거래처명 → C001), 담당자 연락처"],
             ['<span class="light l-r"></span>빨강', "넣지 않음", "급여·인사평가, 단가 협상·원가 분석, 회사 확인 전의 원청 시스템 자료와 기술 자료(작업조건·배합 등)"]], raw=True), one=True)
    # ── 3교시 ──
    + section("3교시 · 웹에서 첫 코딩", "약 50분 · claude.ai")
    + st("1-5", "Claude 웹 열기", "설치 없이 브라우저에서 Claude를 엽니다.",
         [f"크롬 주소창에 {ui('claude.ai')} 입력 후 {kbd('Enter')}", "회사에서 안내한 계정으로 로그인", "가운데 입력창이 있는 새 대화 화면을 확인"],
         ok="‘무엇을 도와드릴까요?’ 같은 인사말과 입력창이 보입니다.",
         stuck="로그인 메일이 오지 않으면 스팸함을 확인하세요. 회사 보안 정책으로 접속이 막히면 강사에게 알려 주세요.",
         figure=fig("m1-05", "claude.ai 새 대화 화면", claude_web([], marks={"input": 3})))
    + st("1-6", "말 한마디로 첫 웹 페이지", "요청문(프롬프트) 하나로 부서 소개 페이지를 만들고 바로 미리 봅니다.",
         [f"아래 요청문의 {ui('복사')} → [ ] 부분을 우리 부서에 맞게 고치기" + prompt(P16), f"입력창에 붙여넣고 {ui('↑')}(보내기)",
          "오른쪽에 열린 미리보기 창에서 페이지 확인"],
         ok="오른쪽 창에 부서 이름과 업무 3가지가 적힌 페이지가 보입니다. 모양은 사람마다 달라도 괜찮습니다.",
         stuck="오른쪽 창이 안 열리고 코드만 보이면 “방금 코드를 미리보기로 보여줘”라고 보내세요.",
         figure=fig("m1-06", "요청 → 오른쪽 미리보기", claude_web(
             [("user", "우리 관리팀 업무를 소개하는 웹 페이지를 HTML 한 파일로 만들어줘…"), ("ai", "부서 소개 페이지를 만들었습니다.")],
             preview_html=dept_v1, marks={0: 2}, preview_marks={"tab": 3}, input_text="")))
    + st("1-7", "대화로 고치기 — 한 번에 하나씩", "수정 요청을 하나씩 보내며 결과가 바뀌는 것을 확인합니다.",
         ["첫 번째 요청을 보내고 미리보기가 바뀐 것 확인" + prompt("제목 배경색을 금색 계열로 바꿔줘."),
          "두 번째 요청을 보내고 확인" + prompt("주요 업무에 '[월간 보고서 작성]'을 하나 더 추가해줘."),
          "세 번째 요청을 보내고 버튼 눌러 보기" + prompt("맨 아래에 '담당자에게 문의' 버튼을 넣어줘. 누르면 '준비 중입니다' 안내가 뜨게 해줘.")],
         ok="제목 색·업무 4개·버튼까지 3번의 수정이 모두 반영됐습니다.",
         stuck="한 번에 여러 개를 보냈더니 엉뚱하게 바뀌었다면 “방금 수정은 취소하고 이전 버전으로 돌려줘”라고 보내세요.",
         figure=fig("m1-07", "수정 3번이 반영된 미리보기", claude_web(
             [("user", "제목 배경색을 금색 계열로 바꿔줘."), ("ai", "바꿨습니다."), ("user", "업무 하나 더 추가해줘."), ("ai", "추가했습니다."),
              ("user", "문의 버튼을 넣어줘."), ("ai", "버튼을 넣었습니다.")],
             preview_html=dept_v2, marks={0: 1, 2: 2, 4: 3}, input_text="")))
    + st("1-8", "파일로 받아 내 PC에서 열기", "만든 페이지를 HTML 파일로 받아 브라우저로 열어 봅니다.",
         [f"미리보기 창 오른쪽 위 {ui('⋯')}(또는 {ui('⬇')}) 클릭", f"{ui('다운로드')} 클릭", f"파일 탐색기 {ui('다운로드')} 폴더에서 받은 .html 파일 더블클릭",
          "크롬 주소창이 file:/// 로 시작하는지 확인"],
         ok="인터넷 주소가 아닌 내 PC 파일(file:///…)로 같은 페이지가 열립니다. ‘HTML = 브라우저가 읽는 문서’를 확인한 것입니다.",
         stuck="다운로드 메뉴 위치는 화면 버전에 따라 다를 수 있습니다. 못 찾으면 코드 탭의 복사 버튼으로 복사해 메모장에 붙이고 ‘이름.html’로 저장해도 됩니다.",
         figure=figs(
             fig("m1-08a", "미리보기 메뉴 → 다운로드", claude_web([("user", "문의 버튼을 넣어줘."), ("ai", "버튼을 넣었습니다.")],
                                                           preview_html=dept_v2, preview_marks={"menu": 1}, input_text="",
                                                           dd=dropdown(["복사", ("다운로드", 2)], align="right", width=110))),
             fig("m1-08b", "다운로드 폴더 → 더블클릭", explorer("C:\\Users\\금대리\\Downloads",
                                                         [("🌐", "부서_소개.html", "Chrome HTML Document"), ("📊", "mes_sample.xlsx", "Microsoft Excel 워크시트")],
                                                         marks={"부서_소개.html": 3})),
             fig("m1-08c", "내 PC 파일로 열린 페이지", browser("file:///C:/Users/금대리/Downloads/부서_소개.html", dept_v2, url_mark=4, tab="관리팀 업무 소개"))))
    # ── 4교시 ──
    + section("4교시 · 데이터 넣어 보기와 웹의 한계", "약 55분")
    + st("1-9", "엑셀을 넣어 차트 만들기", "초록 등급 가상 데이터로 호기별 불량률 차트를 만듭니다.",
         ['홈 탭 또는 아래 버튼으로 <b>mes_sample.xlsx</b> 내려받기' + '<div style="margin-top:8px"><a class="dl g" href="practice/mes_sample.xlsx" download>📥 mes_sample.xlsx (가상 생산실적 66행)</a></div>', f"입력창 왼쪽 {ui('＋')} → {ui('파일 또는 사진 추가')}(Add files or photos) → mes_sample.xlsx 선택",
          f"아래 요청문을 붙여넣고 {ui('↑')}" + prompt(P19), "미리보기의 차트와 표 확인"],
         ok="불량률이 <b>1호기 2.7% · 2호기 3.7% · 3호기 1.9%</b>로 나옵니다(전체 2.8%). 2호기 막대가 가장 깁니다.",
         stuck="숫자가 조금 다르면 날짜별 평균을 낸 경우입니다. “합계 불량량 ÷ 합계 생산량으로 다시 계산해줘”라고 보내세요. 엑셀이 올라가지 않으면 설정 → 기능에서 ‘코드 실행 및 파일 생성’을 켜거나, 홈 탭의 CSV 파일을 올립니다.",
         figure=fig("m1-09", "파일 첨부 → 요청 → 차트", claude_web(
             [("user", "📎 mes_sample.xlsx\n첨부한 엑셀은 교육용 가상 생산실적이야. 호기별 불량률을…"), ("ai", "호기별 불량률 차트를 만들었습니다.")],
             preview_html=chart, preview_title="호기별 불량률", attach_mark=2, marks={0: 3}, preview_marks={"tab": 4}, input_text="")))
    + st("1-10", "웹의 한계", "웹이 불편한 점을 직접 적어 보고, 왜 CLI로 넘어가는지 이해합니다.",
         ["아래 비교표의 빈칸(웹 쪽)을 내 경험으로 채웁니다.", "답 보기를 펼쳐 비교합니다.", "모듈 2에서 쓸 CLI 쪽 설명을 읽습니다."],
         extra=table(["비교", "웹 Claude (오늘 해 본 것)", "Claude Code CLI (모듈 2부터)"], [
             ["파일 넣기", "(빈칸)", "내 폴더의 파일을 일꾼이 직접 엽니다"],
             ["결과 저장", "(빈칸)", "내 폴더에 바로 파일이 생깁니다"],
             ["여러 파일 관리", "(빈칸)", "폴더 하나를 작업대로 통째로 씁니다"],
             ["되돌리기", "(빈칸)", "세이브 카메라(Git)로 시점별 복원"]])
         + '<details class="qa"><summary>답 보기(웹 쪽 예시)</summary><p>매번 파일을 올려야 함 · 결과를 매번 내려받아야 함 · 파일이 여러 개면 관리가 어려움 · 대화 기록 외에 저장 시점이 없음</p></details>'
         + box("info", "그래서", "일꾼을 내 PC 작업대(폴더)로 부르는 것이 CLI입니다. 터미널 주방장에게 글로 주문하면 클로가 내 폴더에서 바로 일합니다."),
         ok="웹 쪽 빈칸 4개를 채웠으면 통과입니다.", one=True)
    + st("1-11", "모듈 2 준비 점검", "다음 모듈에서 설치가 막히지 않도록 미리 확인합니다.",
         ["Claude 유료 구독이 켜져 있는지 확인(설정 → 요금제)", "노트북에 프로그램 설치 권한이 있는지 확인(관리자 문의)",
          "Windows 업데이트가 밀려 있지 않은지 확인", "다음 시간에 노트북과 충전기 지참"],
         ok="4개 항목을 강사에게 ‘이상 없음’ 또는 ‘문제 있음’으로 알렸습니다.",
         stuck="회사 보안 프로그램이 설치를 막을 수 있습니다. 문제가 있으면 모듈 2 전에 전산 담당에게 요청해 주세요.", one=True)
    + st("1-12", "Claude 데스크톱 앱 설치 (CLI의 짝꿍)", "PC에 Claude 앱을 설치해, 웹 대신 앱으로 쓰고 Claude Code(Code 탭)도 미리 열어 봅니다.",
         [f"아래 {ui('⬇ Windows용 Claude 앱 내려받기')} 버튼 클릭 → 설치 파일 다운로드가 바로 시작됩니다"
          + '<div style="margin-top:8px"><a class="dl g" href="https://claude.ai/api/desktop/win32/x64/setup/latest/redirect">⬇ Windows용 Claude 앱 내려받기 (64비트)</a> '
            '<a class="dl" href="https://claude.com/ko/download" target="_blank" rel="noopener">🌐 공식 다운로드 페이지 열기</a></div>',
          "브라우저 아래(또는 오른쪽 위) 다운로드 목록에서 받은 설치 파일 실행 → 설치가 끝나면 앱이 자동으로 열림",
          "웹(claude.ai)과 같은 계정으로 로그인",
          f"앱 화면에서 {ui('Code')} 탭을 눌러 Claude Code 화면이 열리는지 확인"],
         extra=box("info", "앱과 CLI는 어떤 관계인가요?",
               "같은 Claude Code를 두 가지 방식으로 씁니다. <b>CLI</b>(모듈 2에서 설치)는 PowerShell에서 글로 쓰고, <b>데스크톱 앱의 Code 탭</b>은 화면을 보며 씁니다. "
               "이 과정은 CLI로 진행하고, 모듈 2에서 CLI 설치가 막히면 앱의 Code 탭이 <b>따라잡기 경로</b>가 됩니다. CLI는 앱이 없어도 따로 설치할 수 있습니다."),
         ok="데스크톱 앱이 열리고 로그인돼 있으며, Code 탭을 누르면 작업 폴더를 고르는 화면이 나옵니다.",
         stuck="첫 번째 버튼으로 다운로드가 시작되지 않으면 ‘공식 다운로드 페이지 열기’에서 Windows용 버튼을 누르세요. ARM 노트북(일부 서피스 등)은 페이지에서 ARM64용을 고릅니다. 회사 PC에서 설치가 막히면 1-11처럼 전산 담당에게 요청합니다.",
         figure=fig("m1-12", "Claude 데스크톱 앱 — Code 탭", app_window(
             "Claude",
             '<div class="dk"><div class="dk-side"><div class="dk-tab">💬 채팅</div>' + mk('<div class="dk-tab on">⌨ Code</div>', 4, block=True)
             + '<div class="dk-tab dim">🕘 최근 항목</div></div><div class="dk-main"><b>Claude Code</b><p>작업할 폴더를 고르면 이 폴더에서 Claude가 파일을 읽고 만듭니다.</p>'
             '<span class="mbtn p">📁 폴더 선택</span><div class="dk-in">무엇을 만들까요?</div></div></div>', icon_color="#c96442")))
    + '<div class="next-mod">' + box("ok", "모듈 1 완료!", '수고하셨습니다. 다음은 <a href="#m2" data-go="m2">모듈 2 · CLI 환경 셋팅</a>입니다.') + "</div>",
    pc_note=PC)

# ════════════════════════════ 모듈 2 ════════════════════════════
PATH3 = '''$newPath = $env:USERPROFILE + "\\.local\\bin"
[Environment]::SetEnvironmentVariable("PATH", [Environment]::GetEnvironmentVariable("PATH","User") + ";" + $newPath, "User")
$env:Path += ";" + $newPath
'''
PS_HEAD = ["Windows PowerShell", "Copyright (C) Microsoft Corporation. All rights reserved.", ""]

m2 = wrap(
    progress_bar("모듈 2 진도")
    + section("모듈 2 · CLI 환경 셋팅", "4시간+ · 현장 진도에 따라 조절")
    + box("info", "오늘의 작업대", "터미널(PowerShell)에 공구 3종 — <b>Git</b>(세이브 카메라) · <b>Claude Code</b>(클로) · <b>Python</b>(엑셀 읽는 공구) — 을 갖추고, 내 폴더에서 첫 결과물을 만듭니다. 명령은 <b>한 줄씩</b> 치고, 성공 화면을 확인한 뒤 다음으로 갑니다.")
    + flow([("1교시", "터미널 첫걸음"), ("2교시", "공구 3종 설치"), ("3교시", "로그인·첫 대화"), ("4교시", "첫 결과물·되돌리기")])
    + teach([
        ["0:00 (10분)", "입장 체크", "1-11 점검 결과 확인. 설치 권한이 없는 PC는 보조강사와 먼저 해결", "전원 PowerShell 열 준비"],
        ["0:10 (35분)", "2-1 ~ 2-5", "명령을 한 줄씩 같이 침. 2-4에서 일부러 오타를 내 ‘빨간 글자는 안내문’을 체험시킴", "바탕화면에 geumjin-vibe"],
        ["0:55 (15분)", "2-6", "설치 공식(확인 → 설치 → PATH → 다시 확인)을 칠판에 적음", "git 버전 표시"],
        ["1:10 (25분)", "2-7 ~ 2-9", "설치가 느린 PC를 기다리는 동안 PATH 비유(배치도) 설명. 창을 새로 열었는지 확인", "claude 버전 표시"],
        ["1:35 (25분)", "2-10 ~ 2-12", "Store 안내가 뜨는 화면을 먼저 보여 주고, PATH 체크를 전원 손으로 가리키게 함", "python·pip 버전 표시"],
        ["2:10 (25분)", "2-13 ~ 2-14", "로그인은 브라우저에서. 전원 아래 줄이 manual mode on인지 확인. 권한 창 세 줄을 소리 내어 읽게 함", "시작 화면 + manual mode on"],
        ["2:35 (20분)", "2-15 ~ 2-16", "첫 질문 → /help → /clear → /exit → claude -c 를 한 흐름으로", "이전 대화 이어짐"],
        ["3:05 (10분)", "2-17", "모듈 1과 같은 요청이 ‘내 폴더에 파일로’ 생기는 차이를 강조", "index.html 열림"],
        ["3:15 (10분)", "2-18", "요청문 4종 중 ‘계획 먼저’를 가장 길게. 오류 붙여넣기 틀은 메모만", "아이콘 수정 반영"],
        ["3:25 (10분)", "2-19", "권한 창의 명령을 읽고 허락하는 연습", "‘준비됐다’ 답"],
        ["3:35 (20분)", "2-20", "망가뜨린 직후 강사 시연(git status·diff) → 되돌리기 → git log. 이름·이메일 설정 질문이 나오는 PC를 보조강사가 돕게 함", "제목이 원래대로"],
        ["3:55 (15분+)", "2-21", "8항목 체크. 남은 사람은 클리닉으로 개별 지원", "8개 체크"],
    ], note="시각에는 교시 사이 쉬는 시간 10분이 들어 있습니다. 단계가 21개라 4시간을 10분쯤 넘깁니다(2-21 클리닉). 막히기 쉬운 설치(2-7~2-9)·로그인(2-13~2-14)·되돌리기(2-20)에 시간을 더 주고, 따라 치기만 하는 2-1~2-5·2-17·2-18을 줄였습니다. 그래도 밀리면 2-18은 설명·계획 먼저 2개만 하고, 2-20(되돌리기)과 2-21(퇴장 체크)은 꼭 합니다. 20분 이상 막힌 사람은 데스크톱 앱 Code 탭(따라잡기)으로 먼저 진행시킵니다.")
    # ── 1교시 ──
    + section("1교시 · 터미널 첫걸음 (설치 전)", "약 45분")
    + st("2-1", "PowerShell 열기", "터미널 주방장을 불러냅니다.",
         [f"{kbd('Windows')} 키 또는 시작 버튼 누르기", "‘PowerShell’ 입력", f"{ui('Windows PowerShell')} → {ui('열기')}"],
         ok="파란(또는 검은) 창에 <code>PS C:\\Users\\내이름&gt;</code>이 보입니다.",
         stuck="‘관리자로 실행’은 누르지 마세요. 실수로 열었다면 창을 닫고 다시 여세요.",
         figure=fig("m2-01", "시작 → PowerShell 검색 → 열기", start_search("PowerShell", marks={"search": 2, "result": 3}))
         )
    + st("2-2", "터미널 화면 읽기", "맨 아래 줄이 ‘지금 내가 있는 폴더’라는 것을 압니다.",
         ["맨 아래 줄 <code>PS C:\\Users\\내이름&gt;</code>을 찾습니다.", f"파일 탐색기를 열고 {ui('사용자')} → 내 이름 폴더로 가서 주소창을 봅니다.",
          "두 곳이 같은 폴더라는 것을 확인합니다."],
         ok="‘터미널은 지금 내 사용자 폴더에 있다’고 말로 설명할 수 있습니다.",
         figure=figs(fig("m2-02a", "PowerShell 현재 위치", ps_window(PS_HEAD + [html_line(mk('<span class="pp">PS C:\\Users\\금대리&gt;</span><span class="cur">▌</span>', 1))])),
                     fig("m2-02b", "탐색기 주소창 — 같은 폴더", explorer("C:\\Users\\금대리", [("📁", "Desktop", "파일 폴더"), ("📁", "Documents", "파일 폴더"), ("📁", "Downloads", "파일 폴더")],
                                                                path_mark=2))))
    + st("2-3", "폴더 이동 연습", "글로 폴더를 오가는 법을 익힙니다.",
         [f"<code>cd Desktop</code> 입력 → {kbd('Enter')}" + code_block("연습 명령", text="cd Desktop\ndir\ncd ..\n", cid="c-cd"), f"<code>dir</code> 입력 → {kbd('Enter')} (바탕화면 목록)", f"<code>cd ..</code> 입력 → {kbd('Enter')} (한 칸 위로)",
          f"<code>cd De</code>까지 치고 {kbd('Tab')} → 자동 완성 확인", f"{kbd('↑')} 키로 이전 명령 불러오기"],
         ok="<code>cd Desktop</code> 후 맨 아래 줄이 <code>…\\Desktop&gt;</code>로 바뀌고, <code>dir</code>에 바탕화면 파일 목록이 나옵니다.",
         stuck="‘경로를 찾을 수 없습니다’가 나오면 바탕화면이 OneDrive에 있는 PC입니다. <code>cd ([Environment]::GetFolderPath('Desktop'))</code>를 복사해 쓰세요.",
         figure=fig("m2-03", "cd → dir → cd ..", ps_window([
             ps_prompt(cmd="cd Desktop", n=1), ps_prompt(path="C:\\Users\\금대리\\Desktop", cmd="dir", n=2),
             "", "    디렉터리: C:\\Users\\금대리\\Desktop", "", "Mode     LastWriteTime      Length Name", "----     -------------      ------ ----",
             "d----    2026-11-09 09:10        회의자료", "-a---    2026-11-02 17:40  20512 주간보고.xlsx", "",
             ps_prompt(path="C:\\Users\\금대리\\Desktop", cmd="cd ..", n=3), ps_prompt(cursor=True)])))
    + st("2-4", "터미널 조작 습관", "붙여넣기·멈추기·화면 지우기, 그리고 빨간 글자에 놀라지 않기를 익힙니다.",
         [f"위 연습 명령을 복사해 {kbd('Ctrl', 'V')} 또는 마우스 오른쪽 클릭으로 붙여넣기", f"명령이 멈추지 않으면 {kbd('Ctrl', 'C')}",
          "<code>cls</code>로 화면 지우기", "일부러 <code>dri</code>(오타)를 쳐서 빨간 글자 보기"],
         ok="빨간 글자가 나와도 아무것도 고장 나지 않았다는 것을 확인했습니다. 빨간 글자는 ‘그런 명령은 없어요’라는 안내문입니다.",
         figure=fig("m2-04", "빨간 글자 = 안내문", ps_window([
             ps_prompt(cmd="dri"),
             html_line(mk('<span class="er">dri : \'dri\' 용어가 cmdlet, 함수, 스크립트 파일 또는 실행할 수 있는 프로그램 이름으로 인식되지 않습니다.</span>', 4)),
             "", ps_prompt(cmd="cls", n=3)])))
    + st("2-5", "작업 폴더 만들기", "앞으로 AI 일꾼이 일할 작업대(폴더)를 만듭니다.",
         ["<code>cd Desktop</code>으로 바탕화면 이동" + code_block("작업 폴더 만들기", text="cd Desktop\nmkdir geumjin-vibe\n", cid="c-mkdir"),
          "<code>mkdir geumjin-vibe</code> 입력", "파일 탐색기 바탕화면에 같은 폴더가 생겼는지 확인"],
         extra=box("warn", "폴더 이름 규칙", "작업 폴더 이름은 영문 소문자와 - 만 씁니다. 폴더 이름의 한글·띄어쓰기는 명령을 칠 때 오류가 나기 쉽습니다. 폴더 안의 파일 이름은 한글이어도 됩니다.")
         + box("info", "바탕화면이 OneDrive에 있는 PC", "<code>cd Desktop</code>이 안 되는 PC는 앞으로도 계속 안 됩니다. 이 교안에서 <code>cd Desktop</code>이 나올 때마다 <code>cd ([Environment]::GetFolderPath('Desktop'))</code>로 바꿔 치세요(부록 오류표에도 있습니다)."),
         ok="탐색기 바탕화면에 <b>geumjin-vibe</b> 폴더가 보입니다. 글로 만든 폴더가 클릭 화면에도 똑같이 생겼습니다.",
         figure=figs(fig("m2-05a", "mkdir로 폴더 만들기", ps_window([ps_prompt(path=DESK, cmd="mkdir geumjin-vibe", n=2), "",
                                                              "Mode     LastWriteTime      Length Name", "d----    2026-11-09 10:05        geumjin-vibe", "",
                                                              ps_prompt(path=DESK, cursor=True)])),
                     fig("m2-05b", "탐색기에서도 확인", explorer(DESK, [("📁", "geumjin-vibe", "파일 폴더"), ("📁", "회의자료", "파일 폴더"), ("📊", "주간보고.xlsx", "Microsoft Excel 워크시트")],
                                                         marks={"geumjin-vibe": 3}))))
    # ── 2교시 ──
    + section("2교시 · 공구 3종 설치", "약 65분 · 한 줄씩, 성공 화면 확인 후 다음")
    + box("info", "설치 공식", "세 공구 모두 같은 순서입니다 — <b>확인 → 설치 → (PATH 등록) → 다시 확인</b>. 두 번째부터는 순서를 스스로 말해 보세요.")
    + st("2-6", "Git 확인·설치 (세이브 카메라)", "되돌리기 도구 Git을 설치합니다. 2-20과 모듈 3·4의 ‘저장’에 꼭 필요합니다.",
         ["<code>git --version</code> 입력" + code_block("Git 확인", text="git --version\n", cid="c-git"), "버전이 나오면 2-7로. ‘인식되지 않습니다’가 나오면 git-scm.com에서 Windows용 설치 파일 받기",
          f"설치 화면은 바꾸지 말고 {ui('Next')}를 계속 → {ui('Install')} → {ui('Finish')}", "PowerShell을 닫고 다시 열어 1번 다시 실행"],
         ok="<code>git version 2.xx.x.windows.1</code>처럼 버전 번호가 나옵니다.",
         stuck="설치 중 선택지가 많아 보여도 전부 기본값이면 됩니다. 이미 깔려 있으면 설치를 건너뜁니다.",
         figure=figs(fig("m2-06a", "git --version", ps_window([ps_prompt(cmd="git --version", n=1), html_line(span("ok", "git version 2.51.0.windows.1")), "", ps_prompt(cursor=True)])),
                     fig("m2-06b", "Git 설치 — 기본값으로 Next", installer("Git 2.xx Setup", "Select Components",
                                                                       "<p>설치할 구성 요소를 고르는 화면입니다. 아무것도 바꾸지 않습니다.</p>"
                                                                       + checkbox("Windows Explorer integration", True) + checkbox("Git LFS (Large File Support)", True),
                                                                       wbtn("Back") + wbtn("Next", True, 3) + wbtn("Cancel"), side_color="#f05133", logo="◆"))))
    + st("2-7", "Claude Code 설치 (클로 부르기)", "설치 명령 한 줄로 클로를 내 PC에 들입니다.",
         ["아래 명령 복사" + code_block("Claude Code 설치", text="irm https://claude.ai/install.ps1 | iex\n", cid="c-install"),
          "PowerShell에 붙여넣고 Enter", "설치가 끝날 때까지 기다리기(1~3분)"],
         ok="‘설치 완료(successfully installed)’ 문구와 설치 위치(…\\.local\\bin\\claude.exe)가 나옵니다.",
         stuck="빨간 글자로 접속 오류가 나오면 회사 네트워크가 막은 경우입니다. 강사에게 알려 주세요.",
         figure=fig("m2-07", "설치 명령 실행", ps_window([ps_prompt(cmd="irm https://claude.ai/install.ps1 | iex", n=2),
                                                    html_line(span("dim", "Setting up Claude Code...")),
                                                    html_line(span("ok", "✔ Claude Code successfully installed!")),
                                                    html_line(span("dim", "  Location: C:\\Users\\금대리\\.local\\bin\\claude.exe")), "", ps_prompt(cursor=True)])))
    + st("2-8", "PATH 등록 (배치도에 위치 적기)", "터미널이 claude 프로그램 위치를 찾을 수 있게 등록합니다.",
         ["아래 3줄을 한꺼번에 복사" + code_block("PATH 등록 3줄", text=PATH3, cid="c-path"), "PowerShell에 붙여넣고 Enter", "PowerShell 창을 닫고 새로 열기"],
         extra=box("info", "왜 하나요?", "설치만으로는 터미널이 새 설비 위치를 모를 때가 있습니다. 배치도에 ‘클로는 여기 있음’이라고 적는 단계입니다."),
         ok="아무 메시지 없이 다음 줄로 넘어가면 정상입니다. 창을 다시 열었는지 꼭 확인하세요.",
         figure=fig("m2-08", "PATH 3줄 붙여넣기", ps_window([html_line(mk('<span class="pp">PS C:\\Users\\금대리&gt;</span> $newPath = $env:USERPROFILE + "\\.local\\bin"<br>'
                                                                     '<span class="pp">PS C:\\Users\\금대리&gt;</span> [Environment]::SetEnvironmentVariable("PATH", …)<br>'
                                                                     '<span class="pp">PS C:\\Users\\금대리&gt;</span> $env:Path += ";" + $newPath', 2)), ps_prompt(cursor=True)])))
    + st("2-9", "Claude Code 확인", "클로가 제자리에 있는지 확인합니다.",
         ["새 PowerShell에서 <code>claude --version</code> 입력" + code_block("확인", text="claude --version\n", cid="c-ccver")],
         ok="<code>2.x.x (Claude Code)</code>처럼 버전 번호가 나옵니다.",
         stuck="‘인식되지 않습니다’가 나오면 2-8을 다시 하고 창을 새로 여세요. 그래도 안 되면 부록의 ‘자주 보는 오류’ 표를 보세요.",
         figure=fig("m2-09", "claude --version", ps_window([ps_prompt(cmd="claude --version", n=1), html_line(span("ok", "2.1.x (Claude Code)")), "", ps_prompt(cursor=True)])))
    + st("2-10", "Python 확인 (공구함 열어 보기)", "엑셀 읽는 공구 Python이 있는지 봅니다.",
         ["<code>python --version</code> 입력" + code_block("Python 확인", text="python --version\n", cid="c-py"), "버전이 나오면 2-12로 건너뜀", "아래처럼 ‘Microsoft Store’ 안내가 나오거나 Store 창이 뜨면 → 창을 닫고 2-11로"],
         extra=box("warn", "가짜 바로가기 주의", "Windows에는 ‘python’이라는 이름의 가짜 바로가기가 들어 있어서, 설치가 안 된 상태로 치면 Store로 안내합니다. Store에서 설치하지 말고 2-11로 가세요."),
         ok="버전이 나오거나(설치됨), Store 안내가 나왔습니다(설치 필요). 둘 다 정상 확인입니다.",
         figure=fig("m2-10", "설치 안 된 상태의 안내문", ps_window([ps_prompt(cmd="python --version", n=1),
                                                          html_line(mk('<span class="y">Python was not found; run without arguments to install from the Microsoft Store, or disable this shortcut from Settings &gt; Apps &gt; Advanced app settings &gt; App execution aliases.</span>', 3)),
                                                          "", ps_prompt(cursor=True)])))
    + st("2-11", "Python 설치 — PATH 체크가 핵심", "python.org 설치 파일로 Python을 설치합니다.",
         [f"크롬에서 {ui('python.org/downloads/windows')} 열기 → Python 3.13.x의 {ui('Windows installer (64-bit)')} 받기",
          "받은 설치 파일 실행",
          f"첫 화면 맨 아래 {ui('Add python.exe to PATH')} <b>체크</b>",
          f"{ui('Install Now')} 클릭 → 완료되면 {ui('Close')}"],
         ok="‘Setup was successful’ 화면이 나옵니다.",
         stuck="다운로드 페이지가 ‘Python install manager’를 먼저 권하면, 아래 목록에서 Python 3.13.x의 Windows installer (64-bit)를 고르세요. PATH 체크를 빠뜨렸으면 설치 파일을 다시 실행해 Modify로 고칩니다.",
         figure=fig("m2-11", "설치 첫 화면 — PATH 체크 후 Install Now", installer(
             "Python 3.13.x (64-bit) Setup", "Install Python 3.13.x (64-bit)",
             "<p>Select Install Now to install Python with default settings, or choose Customize to enable or disable features.</p>"
             + mk('<div class="ins-big"><b>→ Install Now</b><br><small>C:\\Users\\금대리\\AppData\\Local\\Programs\\Python\\Python313</small></div>', 4, block=True)
             + '<div class="ins-big" style="background:#fff"><b>→ Customize installation</b></div>'
             + checkbox("Use admin privileges when installing py.exe", True) + checkbox("Add python.exe to PATH", True, n=3),
             wbtn("Cancel"), side_color="#306998", logo="🐍")))
    + st("2-12", "Python 확인 (공구·배달원)", "Python과 부품 배달원 pip이 준비됐는지 확인합니다.",
         ["PowerShell을 닫고 새로 열기", "<code>python --version</code>" + code_block("Python·pip 확인", text="python --version\npip --version\n", cid="c-pyver"),
          "<code>pip --version</code>"],
         ok="<code>Python 3.13.x</code>와 <code>pip 2x.x from … (python 3.13)</code>이 나옵니다.",
         stuck="여전히 Store 안내가 나오면 PATH 체크가 빠진 것입니다(2-11 막히면 참고). pip만 안 되면 <code>python -m pip --version</code>으로 확인하세요.",
         figure=fig("m2-12", "python · pip 버전", ps_window([ps_prompt(cmd="python --version", n=2), html_line(span("ok", "Python 3.13.x")),
                                                       ps_prompt(cmd="pip --version", n=3), html_line(span("ok", "pip 25.2 from C:\\Users\\금대리\\…\\pip (python 3.13)")), "", ps_prompt(cursor=True)])))
    # ── 3교시 ──
    + section("3교시 · 로그인과 첫 대화", "약 45분")
    + st("2-13", "첫 실행과 로그인", "작업 폴더에서 클로를 처음 깨우고 내 계정으로 로그인합니다.",
         ["<code>cd Desktop\\geumjin-vibe</code>로 작업 폴더 이동" + code_block("작업 폴더에서 실행", text="cd Desktop\\geumjin-vibe\n" + MODE + "\n", cid="c-run"),
          f"<code>{MODE}</code> 입력(위 상자에서 복사)",
          f"글자 색 테마는 첫 번째(Dark mode) 그대로 {kbd('Enter')}",
          f"로그인 방식에서 {ui('Claude account with subscription')} 선택 → 열린 브라우저에서 로그인·승인 → 터미널로 돌아와 {kbd('Enter')}"],
         extra=box("info", "왜 명령이 긴가요?", "최신 Claude Code는 <b>자동(auto) 모드</b>로 시작해, 안전하다고 판단한 일은 묻지 않고 합니다. 이 과정에서는 무엇을 하려는지 읽고 허락하는 연습을 위해 <b>수동 모드</b>로 시작합니다. "
               "<code>--permission-mode default</code>가 ‘매번 물어봐’라는 뜻입니다."),
         ok="버전·모델 이름·작업 폴더가 적힌 시작 화면과 아래 입력칸(&gt;)이 보입니다. 맨 아래 줄에 <b>⏸ manual mode on</b>이 있으면 수동 모드입니다.",
         stuck="브라우저가 자동으로 안 열리면 <kbd>c</kbd> 키를 눌러 주소를 복사해(또는 터미널에 나온 긴 주소를 직접 복사해) 크롬에 붙여넣으세요. 화면 문구와 로그인 선택지 수는 버전에 따라 조금 다릅니다.",
         figure=figs(fig("m2-13a", "작업 폴더에서 claude 실행", ps_window([ps_prompt(cmd="cd Desktop\\geumjin-vibe", n=1), ps_prompt(path=WORK, cmd=MODE, n=2)])),
                     fig("m2-13b", "로그인 방식 고르기", cc_window(cc_welcome() + cc_perm("Select login method:", ["Claude account with subscription", "Anthropic Console account"], n=4)))))
    + st("2-14", "폴더 신뢰와 권한 창 읽기", "클로가 ‘해도 돼요?’라고 묻는 창을 읽고 고르는 법을 익힙니다.",
         [f"‘이 폴더를 믿나요?’ 질문에 {ui('Yes, proceed')} 선택 → {kbd('Enter')}",
          f"입력칸 아래 줄이 <b>⏸ manual mode on</b>인지 확인 — <b>⏵⏵ auto mode on</b>이면 {kbd('Shift', 'Tab')}을 한 번 눌러 바꾸기",
          "앞으로 파일을 만들거나 명령을 실행할 때 나오는 권한 창의 세 줄을 읽기",
          f"고르는 법: {kbd('↑')}{kbd('↓')}로 옮기고 {kbd('Enter')} (또는 번호 키)"],
         extra=table(["선택지", "뜻", "언제"], [["1. Yes", "이번 한 번만 허락", "처음에는 항상 이것"],
                                              ["2. Yes, … don't ask again", "이번 작업 동안 같은 일은 묻지 않음", "익숙해진 뒤"],
                                              ["3. No", "거절하고 다르게 하라고 말하기", "이상한 명령일 때"]]),
         ok="아래 줄에 ⏸ manual mode on이 보이고, 질문 상자를 읽고 스스로 1번을 골랐습니다.",
         figure=figs(fig("m2-14a", "폴더 신뢰 확인", cc_window(cc_perm("Do you trust the files in this folder?", ["Yes, proceed", "No, exit"], n=1,
                                                                    detail="C:\\Users\\금대리\\Desktop\\geumjin-vibe"))),
                     fig("m2-14b", "권한 창(예: 파일 만들기)", cc_window(cc_welcome() + cc_ai("index.html 파일을 만들겠습니다.")
                                                                + cc_perm("Do you want to create index.html?", ["Yes", "Yes, allow all edits during this session", "No, and tell Claude what to do differently"], n=3)
                                                                + '<div class="cc-hint">⏸ manual mode on (shift+tab to cycle)</div>'))))
    + st("2-15", "첫 질문과 슬래시 명령", "클로에게 말을 걸고 기본 명령을 써 봅니다.",
         ["입력칸에 아래 질문을 붙여넣고 Enter" + prompt("너는 무엇을 해 줄 수 있어? 초보자용으로 5줄만 설명해줘."), "<code>/help</code> 입력 → 도움말 훑어보기", "<code>/model sonnet</code> 입력 → 실습용 주력 모델로 바꾸기",
          "<code>/clear</code>로 대화를 비운 뒤, 같은 질문을 한 번 더 보내기"],
         extra=table(["명령", "뜻"], [["/help", "도움말"], ["/clear", "대화 맥락 정리(새로 시작)"], ["/exit", "Claude Code 종료"], ["/login", "다시 로그인"],
                                 ["/model", "모델 바꾸기(Opus·Sonnet·Haiku 등)"], ["/usage", "내 요금제 사용량 확인"]])
         + box("info", "모델 고르기와 토큰 아끼기", '설치 직후 기본 모델은 가장 비싼 축인 Opus입니다. 실습은 Sonnet으로 충분해서 <code>/model sonnet</code>으로 바꿔 둡니다. 어떤 일에 어떤 모델이 좋은지는 <a href="#tips" data-go="tips">💡 모델·토큰 꿀팁</a> 탭에 정리했습니다.'),
         ok="클로가 한국어로 5줄 정도 답하고, <code>/clear</code> 뒤에 다시 물어도 답이 나옵니다.",
         figure=fig("m2-15", "첫 질문", cc_window(cc_welcome() + cc_user("너는 무엇을 해 줄 수 있어? 초보자용으로 5줄만 설명해줘.", n=1)
                                               + cc_ai("1. 이 폴더의 파일을 읽고 설명해요.\n2. 새 파일(웹 페이지 등)을 만들어요.\n3. 엑셀 데이터를 정리·계산해요.\n4. 오류가 나면 원인을 찾아 고쳐요.\n5. 바꾸기 전에 항상 허락을 물어요.")
                                               + cc_input("/help", n=2))))
    + st("2-16", "나갔다 다시 들어오기", "종료해도 대화를 이어갈 수 있다는 것을 확인합니다.",
         ["<code>/exit</code>로 종료", "PowerShell에서 <code>claude -c</code> 입력", "방금 대화가 이어지는지 확인"],
         extra=box("info", "다시 들어오면 모드 확인", "다시 들어왔을 때 아래 줄이 auto mode on이면 Shift+Tab을 한 번 눌러 manual mode on으로 바꿉니다.")
         + table(["명령", "언제"], [["claude", "새 대화 시작"], ["claude -c", "최근 대화 이어서"], ["claude -r", "지난 대화 골라서 열기"], ["claude update", "업데이트"]]),
         ok="<code>claude -c</code>로 다시 들어가면 이전 질문과 답이 보입니다.",
         stuck="로그인이 풀렸다는 안내가 나오면 <code>/login</code>을 입력하세요.",
         figure=fig("m2-16", "/exit → claude -c", ps_window([html_line('<span class="dim">&gt; /exit</span>'), ps_prompt(path=WORK, cmd="claude -c", n=2),
                                                      html_line(span("dim", "(이전 대화를 불러옵니다…)"))])))
    # ── 4교시 ──
    + section("4교시 · CLI로 첫 결과물, 공구 점검, 안전장치", "약 65분")
    + st("2-17", "부서 소개 페이지를 CLI로 다시", "모듈 1과 같은 요청을 CLI로 해서, 파일이 내 폴더에 바로 생기는 것을 봅니다.",
         ["아래 요청문을 붙여넣고 Enter" + prompt("우리 [관리팀] 업무를 소개하는 웹 페이지를 index.html 파일로 만들어줘.\n위쪽에 부서 이름과 ㈜금진, 주요 업무 3가지를 목록으로, 남색 계열 디자인."),
          "권한 창에서 1. Yes", f"탐색기 geumjin-vibe 폴더에 {ui('index.html')}이 생겼는지 확인",
          "index.html 더블클릭으로 크롬에서 열기"],
         ok="다운로드 없이 내 작업 폴더에 index.html이 생기고, 더블클릭하면 페이지가 열립니다.",
         figure=figs(fig("m2-17a", "요청 → 권한 창", cc_window(cc_user("우리 관리팀 업무를 소개하는 웹 페이지를 index.html 파일로 만들어줘…", n=1)
                                                          + cc_perm("Do you want to create index.html?", ["Yes", "Yes, allow all edits during this session", "No"], n=2))),
                     fig("m2-17b", "내 폴더에 바로 생긴 파일", explorer(WORK, [("🌐", "index.html", "Chrome HTML Document")], marks={"index.html": 3})),
                     fig("m2-17c", "크롬에서 열기", browser("file:///C:/Users/금대리/Desktop/geumjin-vibe/index.html", dept_v1, url_mark=4, tab="관리팀 업무 소개"))))
    + st("2-18", "요청문 4종 써 보기", "설명·계획 먼저·작게 수정·오류 붙여넣기 요청을 한 번씩 씁니다.",
         ["설명 요청 보내기" + prompt("방금 만든 index.html이 어떻게 구성됐는지 초보자용으로 설명해줘."),
          "계획 먼저 요청 보내기(파일이 바뀌지 않는 것 확인)" + prompt("아직 파일은 수정하지 말고, 주요 업무 옆에 아이콘을 넣는 계획만 먼저 알려줘."),
          "작게 수정 요청 보내기 → 권한 창 1. Yes → 크롬 새로고침" + prompt("좋아. 계획대로 하되 가장 작은 수정부터 하고, 무엇이 바뀌었는지 알려줘."),
          "오류 붙여넣기 틀을 메모해 두기" + prompt("아래 오류가 났어. 바로 고치지 말고 원인과 해결 순서를 먼저 설명해줘.\n[오류 메시지 붙여넣기]")],
         ok="파일을 바꾸지 않는 요청 2번(설명·계획)과 수정 1번을 해 봤고, 아이콘 수정이 크롬 새로고침 후 페이지에 보입니다.",
         figure=fig("m2-18", "계획 먼저 → 작게 수정", cc_window(cc_user("아직 파일은 수정하지 말고, 아이콘을 넣는 계획만 먼저 알려줘.", n=2)
                                                         + cc_ai("계획: ① 업무 목록 앞에 아이콘 추가 ② 색은 그대로 유지\n바뀔 파일: index.html")
                                                         + cc_user("좋아. 계획대로 하되 가장 작은 수정부터 해줘.", n=3)
                                                         + cc_tool("Update(index.html) — 3줄 수정"))))
    + st("2-19", "공구 점검과 없는 도구 대처", "엑셀을 읽을 부품을 확인하고, 없으면 설치 방법을 물어 허락하는 법을 익힙니다.",
         ["아래 요청문을 붙여넣고 Enter" + prompt("엑셀 파일(.xlsx)을 읽을 준비가 됐는지 확인해줘. 필요한 도구가 없으면 무엇이 없는지와 설치 방법을 초보자용으로 알려줘. 설치 명령은 내가 확인하고 허락할게."),
          "‘필요한 부품(pandas, openpyxl)이 없다’는 답을 읽기",
          f"권한 창에 나온 명령이 <code>pip install pandas openpyxl</code>인지 확인 → {ui('1. Yes')}", "설치 후 ‘준비됐다’는 답 확인"],
         extra=box("info", "앞으로도 이렇게", "낯선 도구가 필요하다는 말이 나오면 겁내지 말고 같은 방식으로 묻습니다: “무엇이 없는지, 설치 방법을 초보자용으로 알려줘.” 명령을 읽고 이상하지 않을 때만 허락합니다."),
         ok="pandas·openpyxl 설치 후 클로가 ‘엑셀을 읽을 준비가 됐다’고 답합니다.",
         stuck="이미 설치돼 있다는 답이 나오면 그대로 통과입니다. 설치가 네트워크 오류로 실패하면 강사에게 알려 주세요.",
         figure=fig("m2-19", "부품 확인 → 설치 허락", cc_window(cc_user("엑셀 파일(.xlsx)을 읽을 준비가 됐는지 확인해줘…", n=1)
                                                       + cc_ai("pandas, openpyxl이 설치되어 있지 않습니다. 엑셀을 읽으려면 두 부품이 필요합니다.", n=2)
                                                       + cc_perm("Bash command", ["Yes", "Yes, and don't ask again for pip install commands", "No"], n=3, detail="pip install pandas openpyxl"))))
    + st("2-20", "세이브 카메라 — 저장하고 되돌리기", "망가져도 돌아올 수 있다는 것을 직접 확인합니다.",
         ["저장 시작 요청 보내기 → 권한 창 1. Yes" + prompt("이 폴더를 git으로 저장 시작하고, 지금 상태를 '첫 저장'이라는 이름으로 저장해줘."),
          "일부러 망가뜨리는 수정 요청 → 크롬 새로고침으로 확인" + prompt("제목 글자를 엄청 크게, 빨간색으로 바꿔줘."),
          "(강사와 함께) 두 번째 PowerShell 창에서 <code>git status</code>, <code>git diff</code>로 바뀐 내용 보기 — 아래 강사 시연 상자",
          "되돌리기 요청 → 크롬 새로고침으로 원래대로 돌아왔는지 확인" + prompt("방금 바꾼 거 마음에 안 들어. 마지막 저장 상태로 되돌려줘.")],
         extra=demo("세이브 카메라 속을 들여다보기 (git status · diff · log)",
                "클로가 뒤에서 한 저장·되돌리기를 명령으로 직접 확인합니다. Claude Code 창은 그대로 두고 <b>PowerShell 창을 하나 더</b> 열어 강사와 같이 칩니다.",
                [{"do": "새 PowerShell 창을 열고 작업 폴더로 이동합니다.", "cmd": ("c-demo-cd", "cd Desktop\\geumjin-vibe\n"),
                  "see": "맨 아래 줄이 <code>…\\geumjin-vibe&gt;</code>로 바뀝니다."},
                 {"do": "망가뜨리는 수정(빨간 큰 제목)을 한 직후, 무엇이 바뀌었는지 봅니다.", "cmd": ("c-demo-status", "git status\n"),
                  "see": "<code>modified: index.html</code> — 저장 이후 index.html이 바뀌었다는 뜻입니다."},
                 {"do": "어떻게 바뀌었는지 봅니다. 화면이 멈추면 <kbd>q</kbd>를 눌러 빠져나옵니다.", "cmd": ("c-demo-diff", "git diff\n"),
                  "see": "<span style='color:#b3372a'>빨간 − 줄</span>은 지워진 원래 내용, <span style='color:#1f8452'>초록 + 줄</span>은 새로 들어간 내용입니다."},
                 {"do": "되돌리기를 마친 뒤 저장 기록을 봅니다.", "cmd": ("c-demo-log", "git status\ngit log --oneline\n"),
                  "see": "<code>nothing to commit, working tree clean</code>(깨끗함)과 <code>첫 저장</code> 기록 1줄이 보입니다."}],
                follow="명령은 화면을 보기만 하는 것이라 아무것도 바꾸지 않습니다. 안전하게 같이 쳐 보세요. 첫 줄의 브랜치 이름은 master 또는 main으로 나오며 둘 다 정상입니다."),
         ok="빨간 큰 제목이 원래 제목으로 돌아왔습니다. ‘코드 수정하다 기존 것이 날아가도 되돌릴 수 있다’를 확인했습니다.",
         stuck="‘이름·이메일 설정이 필요하다’고 하면 “이름은 [금대리], 이메일은 [회사 메일]로 이 폴더에만 설정해줘”라고 보내세요.",
         figure=figs(fig("m2-20", "저장 → 망가뜨리기 → 되돌리기", cc_window(cc_user("이 폴더를 git으로 저장 시작하고 '첫 저장'으로 저장해줘.", n=1)
                                                             + cc_tool("git init · git commit -m \"첫 저장\"")
                                                             + cc_user("제목 글자를 엄청 크게, 빨간색으로 바꿔줘.", n=2)
                                                             + cc_user("마지막 저장 상태로 되돌려줘.", n=4)
                                                             + cc_tool("git restore index.html — 첫 저장 상태로 복원"))),
                     fig("m2-20b", "강사 시연 — 두 번째 PowerShell에서 git 보기", ps_window([
                         ps_prompt(path=WORK, cmd="git status"), "On branch master", "Changes not staged for commit:",
                         html_line(span("er", "        modified:   index.html")), "",
                         ps_prompt(path=WORK, cmd="git diff"),
                         html_line(span("er", '-  <h1 style="color:#fff">관리팀 업무 소개</h1>')),
                         html_line(span("ok", '+  <h1 style="color:red;font-size:64px">관리팀 업무 소개</h1>')), "",
                         ps_prompt(path=WORK, cmd="git log --oneline"), html_line(span("y", "a1b2c3d 첫 저장"))], title="Windows PowerShell — 두 번째 창"))))
    + st("2-21", "클리닉과 퇴장 체크", "모듈 3으로 가기 전에 작업대가 다 갖춰졌는지 확인합니다.",
         ["아래 8개 항목을 하나씩 확인", "안 되는 항목이 있으면 빨강 카드 → 보조강사와 해결", "모두 되면 초록 카드"],
         extra=table(["#", "확인 항목", "확인 방법"], [
             ["1", "Git", "git --version"], ["2", "Claude Code", "claude --version"], ["3", "Python", "python --version"],
             ["4", "로그인", "claude 실행 시 시작 화면과 입력칸"], ["5", "작업 폴더", "바탕화면 geumjin-vibe"], ["6", "index.html", "더블클릭하면 열림"],
             ["7", "엑셀 읽기 준비", "2-19에서 ‘준비됐다’"], ["8", "저장 1회 이상(‘첫 저장’)", "클로에게 “저장 기록 보여줘”"]]),
         ok="8개 모두 확인했습니다. 모듈 3에서 이 작업대 그대로 데이터를 다룹니다.",
         stuck="20분 이상 막히면 ‘따라잡기 경로’로 Claude 데스크톱 앱의 Code 탭에서 나머지를 먼저 하고, 클리닉 시간에 CLI를 마저 잡습니다. 앱이 아직 없으면 1-12부터 합니다.", one=True)
    + '<div class="next-mod">' + box("ok", "모듈 2 완료!", '작업대가 준비됐습니다. 다음은 <a href="#m3" data-go="m3">모듈 3 · 데이터 기본기와 내 도구 설계</a>입니다.') + "</div>",
    pc_note=PC)


# ════════════════════════════ 부록 ════════════════════════════
ap = wrap(
    section("부록", "막힐 때·되돌릴 때·지킬 것")
    + "<h3>자주 보는 오류</h3>"
    + table(["화면에 나온 것", "원인", "해결"], [
        ["'claude' 용어가 … 인식되지 않습니다", "PATH 미등록 또는 창을 새로 안 엶", "2-8 다시 → PowerShell 닫고 새로 열기"],
        ["Python was not found; … Microsoft Store …", "Python 미설치 또는 PATH 체크 누락", "2-11 설치(PATH 체크) 또는 설치 파일 다시 실행 → Modify"],
        ["'pip' 용어가 … 인식되지 않습니다", "PATH 문제", "python -m pip --version 으로 대신 확인"],
        ["경로를 찾을 수 없습니다(cd Desktop)", "바탕화면이 OneDrive에 있음", "cd ([Environment]::GetFolderPath('Desktop'))"],
        ["… 스크립트를 실행할 수 없습니다(실행 정책)", "PC 보안 정책", "강사에게 알리기 → 필요 시 전산 담당 요청"],
        ["로그인 브라우저가 열리지 않음", "기본 브라우저 설정", "터미널에 나온 주소를 복사해 크롬에 붙여넣기"],
        ["한글 사용자 폴더에서 오류", "경로에 한글 포함", "작업 폴더를 C:\\work 처럼 영문 경로에 만들기"],
        ["응답이 이상하게 길어짐·엉뚱함", "대화 맥락이 꼬임", "/clear 후 다시 요청"],
        ["작업을 멈추고 싶음", "—", "Esc(클로 작업 중단) 또는 Ctrl+C"],
        ["권한 창이 안 뜨고 바로 실행됨", "자동(auto) 모드로 시작됨", "아래 줄이 manual mode on이 될 때까지 Shift+Tab. 다음부터는 claude --permission-mode default 로 시작"],
        ["내려받은 파일 이름에 (1)이 붙음", "같은 이름의 파일을 전에 받은 적이 있음", "F2로 이름에서 ‘ (1)’을 지우거나, 먼저 받은 파일을 사용"],
        ["/monthly-report 가 ‘알 수 없는 명령’", "스킬 폴더를 아직 못 읽음 또는 위치가 다름", "/reload-skills → 그래도 안 되면 /exit 후 claude 다시 실행. 위치는 .claude\\skills\\이름\\SKILL.md"],
        ["스킬 결과 모양이 매번 다름", "스킬 본문에 규칙이 빠짐", "“스킬에 ○○ 규칙을 추가해줘”로 보완(5-10)"],
        ["claude mcp list 에 Needs authentication", "아직 노션 로그인 허용 전", "claude 실행 → /mcp → notion → Authenticate(5-14)"],
        ["claude mcp list 에 Failed to connect", "네트워크가 mcp.notion.com 차단 또는 주소 오타", "강사에게 알리기 · claude mcp remove notion 후 다시 추가"],
        ["노션 페이지를 못 찾음", "다른 워크스페이스로 허용함", "/mcp → notion → 다시 인증하고 워크스페이스 확인"],
        ["No module named 'mcp.server.fastmcp'", "MCP 부품 2.x에서 이름이 바뀜(FastMCP → MCPServer)", "“설치된 mcp 버전에 맞게 고쳐줘”(5-21)"],
        ["직접 만든 MCP가 npm·node를 요구함", "요청문에 언어를 안 정해 Node.js로 만듦", "“Python으로 다시 만들어줘”(5-21)"],
        ["날씨 MCP가 403 또는 ‘연결하지 못했습니다’", "회사 네트워크가 날씨 사이트를 막음", "강사에게 알리기 · 사내망에서 api.open-meteo.com 허용 요청"]])
    + "<h3>되돌리기</h3>"
    + box("info", "클로에게 말로", "“마지막 저장 상태로 되돌려줘” · “저장 기록 보여줘” · “두 번 전 저장으로 돌아가줘”")
    + box("warn", "삭제·배포는 직접 확인", "파일 삭제, git push, 배포는 클로에게 바로 맡기지 말고 무엇이 바뀌는지 먼저 확인합니다.")
    + "<h3>다음에 혼자 고칠 때 쓸 요청문</h3>"
    + prompt("이 폴더가 무엇을 하는 프로젝트인지, 파일마다 역할을 초보자용으로 설명해줘. 아직 수정하지 마.")
    + prompt("[바꾸고 싶은 것]을 하고 싶어. 아직 파일은 수정하지 말고, 어떤 파일을 어떻게 바꿀지 계획만 알려줘.")
    + prompt("좋아. 계획대로 하되 가장 작은 수정부터 하고, 무엇이 바뀌었는지 알려줘. 잘 되면 '[이름]'으로 저장해줘.")
    + prompt("아래 오류가 났어. 바로 고치지 말고 원인과 해결 순서를 먼저 설명해줘.\n[오류 메시지 붙여넣기]")
    + prompt("[값]이 엑셀로는 [A]인데 화면에는 [B]로 나와. 계산 과정을 한 줄씩 보여줘.")
    + prompt("방금 바꾼 거 마음에 안 들어. 마지막 저장 상태로 되돌려줘.")
    + "<h3>AI에 넣기 전 체크리스트</h3>"
    + table(["확인", "내용"], [["□", "이 자료는 신호등 무슨 색인가요? (초록·노랑·빨강)"], ["□", "노랑이면 거래처명·연락처를 가렸는가?"],
                              ["□", "빨강(급여·인사·단가·원가·원청 자료)이 섞여 있지 않은가?"], ["□", "결과 숫자를 원본과 3개 이상 대조했는가?"]])
    + "<h3>강사 준비 체크리스트</h3>"
    + table(["언제", "할 일", "관련 단계"], [
        ["1주 전", "교육생 Claude 유료 구독 확정·계정 안내(사전 안내문 카톡 공지)", "1-5, 2-13"],
        ["1주 전", "노트북 설치 권한·보안 프로그램·사내망(claude.ai, github.com, python.org, pip) 접속 확인", "1-11, 2-6~2-12"],
        ["1주 전", "트랙 배정(기술개발 5명을 B 3명·C 2명으로) 확정. 실데이터 수령일과 마스킹 담당자 지정. 원청 자료를 AI에 넣어도 되는 범위 확인", "3-10, 모듈 4"],
        ["1주 전", "교육생 노션 계정 안내(개인 이메일 무료 가입, 실습용 워크스페이스) · 사내망에서 notion.com, mcp.notion.com 접속 확인", "5-12~5-14"],
        ["1주 전", "(심화를 할 때) 사내망에서 api.open-meteo.com, geocoding-api.open-meteo.com, pypi.org(pip 설치) 접속 확인", "5-21, 5-22"],
        ["3일 전", "강사 PC에서 모듈 1·2 전 단계 리허설 → 화면 문구가 다르면 교안 수정, 실제 캡처를 shots/에 저장", "전체"],
        ["3일 전", "1-1 라이브 시연용 demo 폴더 + 백업 완성본 준비(가상 MES 데이터)", "1-1"],
        ["3일 전", "강사 PC에서 모듈 3 전 단계와 모듈 4 트랙 A~E 요청문 리허설 — 트랙 카드의 ‘성공하면’ 숫자와 같은지 확인하고 트랙별 완성본을 백업으로 준비", "모듈 3·4"],
        ["3일 전", "강사 PC에서 모듈 5 리허설 — /memory·/mcp 메뉴, 노션 허용 화면, 노션 도구 권한 창 문구를 확인하고 캡처 교체", "5-3, 5-14, 5-15"],
        ["3일 전", "(심화를 할 때) 강사 Windows PC에서 5-21·5-22 요청문 리허설 — 클로가 만든 MCP가 Connected인지, 3호기 4.1%가 나오는지 확인", "5-21, 5-22"],
        ["3일 전", "(선택) 캐릭터 이미지 11장 준비 — 없으면 이모지 그대로 진행", "캐릭터·용어"],
        ["당일", "포스트잇, 초록·빨강 신호 카드, 보조강사 1명 배치(모듈 2)", "1-1, 모듈 2"],
        ["당일", "사내 공유 폴더 위치 안내(4-6). GitHub Pages 시연용 계정과 샘플 버전 준비", "4-6"]])
    + shot_list_section()
    + PROGRESS_JS)

pages = [Page("home", "", "홈", home), Page("terms", "★", "캐릭터·용어", glossary), Page("m1", "1", "모듈 1", m1), Page("m2", "2", "모듈 2", m2),
         Page("m3", "3", "모듈 3", m3_page()), Page("m4", "4", "모듈 4", m4_page()), Page("m5", "5", "모듈 5", ext_page()), Page("tips", "💡", "모델·토큰", tips_page()), Page("ap", "+", "부록", ap)]
build(OUT / "index.html", pages, title="금진 바이브코딩 · 말로 만드는 내 업무 도구",
      description="㈜금진 임직원을 위한 바이브코딩 실습 교안 — 개념 이해, Claude Code CLI 환경 셋팅, 스킬·MCP(노션)까지 단계별로 따라 합니다.",
      brand=("GJ", "말로 만드는 내 업무 도구", "㈜금진 바이브코딩"), site_url=SITE, og_image="og_image.jpg",
      extra_css=GJ_CSS + PROGRESS_CSS + DEMO_CSS + DESK_CSS + NT_CSS + EXT_CSS + COMMON_CSS + "ul.plain{margin:6px 0 12px 22px;line-height:1.75}h3{margin:16px 0 8px}.wrap :not(pre)>code{font-family:Consolas,'D2Coding','Malgun Gothic','Apple SD Gothic Neo',sans-serif;font-size:.95em}")
print("wrote", OUT / "index.html")
