"""금진 바이브코딩 교안 전용 모형 화면 부품.
- ps_window: Windows PowerShell 창
- cc_window: PowerShell 안에서 실행 중인 Claude Code (환영 상자·대화·권한 질문·입력칸)
- installer: 설치 마법사(Git·Python)
- explorer: 파일 탐색기
- browser: 크롬 주소창 + 페이지
- claude_web: claude.ai 대화 + 오른쪽 미리보기(아티팩트) 패널
- start_search: 시작 메뉴 검색
build(..., extra_css=GJ_CSS + PROGRESS_CSS) 로 스타일을 넘긴다. 진도 기능 스크립트는 PROGRESS_JS를 마지막 페이지에 붙인다.
"""
from lessonkit import E, mk


def _t(line):
    """터미널 한 줄: 문자열이면 이스케이프, ('html', 조각)이면 그대로."""
    if isinstance(line, tuple) and line[0] == "html":
        return line[1]
    return E(line)


def ps_window(lines, title="Windows PowerShell", overlay=""):
    """lines: ['PS C:\\Users\\금대리> cd Desktop', ('html', mk(...)), ...]"""
    body = "\n".join(_t(l) for l in lines)
    return (f'<div class="ps-top"><span class="ps-ico">&gt;_</span><span>{E(title)}</span>'
            f'<span class="ps-ctl">─ ☐ ✕</span></div><pre class="ps-body">{body}</pre>{overlay}')


def ps_prompt(path="C:\\Users\\금대리", cmd="", n=None, cursor=False):
    """프롬프트 한 줄(HTML). n이 있으면 명령 부분에 빨간 번호."""
    c = E(cmd) + ('<span class="cur">▌</span>' if cursor else "")
    c = mk(c, n) if n and cmd else c
    return ("html", f'<span class="pp">PS {E(path)}&gt;</span> {c}')


def cc_window(body_html, title="PowerShell — claude", path="C:\\Users\\금대리\\Desktop\\geumjin-vibe"):
    """Claude Code 실행 화면. body_html은 cc_welcome / cc_user / cc_ai / cc_perm / cc_input 조각을 이어 붙인 것."""
    return (f'<div class="ps-top"><span class="ps-ico">&gt;_</span><span>{E(title)}</span><span class="ps-ctl">─ ☐ ✕</span></div>'
            f'<div class="cc-body"><div class="cc-path">{E(path)}</div>{body_html}</div>')


def cc_welcome(extra=""):
    return (f'<div class="cc-welcome"><b>✻ Welcome to Claude Code!</b><div class="cc-dim">/help for help, /status for your current setup</div>'
            f'<div class="cc-dim">cwd: geumjin-vibe</div>{extra}</div>')


def cc_user(text, n=None):
    h = f'<div class="cc-u">&gt; {E(text)}</div>'
    return mk(h, n, block=True) if n else h


def cc_ai(text, n=None):
    h = f'<div class="cc-a"><span class="cc-dot">●</span> {E(text)}</div>'
    return mk(h, n, block=True) if n else h


def cc_tool(text):
    return f'<div class="cc-tool">⎿ {E(text)}</div>'


def cc_perm(question, options, pick=1, n=None, detail=""):
    """권한 질문 상자. options: ['Yes', 'Yes, and don\'t ask again …', 'No'] / pick: 선택된 줄(1부터)"""
    opts = "".join(f'<div class="{"on" if i == pick else ""}">{"❯" if i == pick else "&nbsp;"} {i}. {E(o)}</div>'
                   for i, o in enumerate(options, 1))
    det = f'<div class="cc-dim">{E(detail)}</div>' if detail else ""
    box = f'<div class="cc-perm"><b>{E(question)}</b>{det}{opts}</div>'
    return mk(box, n, block=True) if n else box


def cc_input(text="", n=None, hint="? for shortcuts"):
    t = E(text) if text else '<span class="cc-dim">Try "이 폴더를 설명해줘"</span>'
    box = f'<div class="cc-in">&gt; {t}<span class="cur">▌</span></div>'
    return (mk(box, n, block=True) if n else box) + f'<div class="cc-hint">{E(hint)}</div>'


def installer(title, heading, body_html, buttons_html, side_color="#1f6feb", logo="⚙"):
    """설치 마법사 창(왼쪽 색 띠 + 본문 + 아래 버튼)."""
    return (f'<div class="win-top"><span class="win-icon" style="background:{side_color}"></span><span class="win-title">{E(title)}</span>'
            f'<span class="ps-ctl" style="color:#5f6368">─ ✕</span></div>'
            f'<div class="ins"><div class="ins-side" style="background:{side_color}">{logo}</div>'
            f'<div class="ins-main"><h4>{E(heading)}</h4>{body_html}</div></div>'
            f'<div class="ins-btns">{buttons_html}</div>')


def wbtn(label, primary=False, n=None):
    b = f'<span class="wbtn{" p" if primary else ""}">{E(label)}</span>'
    return mk(b, n) if n else b


def checkbox(label, on=False, n=None):
    h = f'<div class="wcb"><span class="cb{" on" if on else ""}"></span> {E(label)}</div>'
    return mk(h, n, block=True) if n else h


def explorer(path, items, marks=None, path_mark=None, overlay=""):
    """파일 탐색기. items: [('📁','geumjin-vibe','파일 폴더'), ('📄','index.html','Chrome HTML Document')]
    marks: {이름: 번호}"""
    marks = marks or {}
    rows = []
    for ic, name, kind in items:
        cell = f'<span class="ex-n">{ic} {E(name)}</span>'
        if name in marks:
            cell = mk(cell, marks[name])
        rows.append(f'<tr><td>{cell}</td><td class="ex-k">{E(kind)}</td></tr>')
    p = f'<span class="ex-path">{E(path)}</span>'
    p = mk(p, path_mark) if path_mark else p
    return (f'<div class="win-top"><span class="win-icon" style="background:#f2b200"></span><span class="win-title">파일 탐색기</span></div>'
            f'<div class="ex-bar">← → ↑ {p}</div><div class="ex-wrap"><div class="ex-side">⭐ 즐겨찾기<br>🖥 바탕 화면<br>⬇ 다운로드<br>📄 문서</div>'
            f'<table class="ex-t"><tr><th>이름</th><th>유형</th></tr>{"".join(rows)}</table></div>{overlay}')


def browser(url, page_html, url_mark=None, tab="새 탭"):
    u = f'<span class="br-url">{E(url)}</span>'
    u = mk(u, url_mark) if url_mark else u
    return (f'<div class="br-tabs"><span class="br-tab">{E(tab)}</span></div>'
            f'<div class="br-bar">← → ↻ {u}</div><div class="br-page">{page_html}</div>')


def dept_page(title="관리팀 업무 소개", color="#1d3a7a", items=("월말 결산 지원", "발주·거래 내역 정리", "시스템 간 자료 이관"), button=False):
    """모듈 1·2에서 만드는 '우리 부서 업무 소개' 페이지 모양(예시)."""
    lis = "".join(f"<li>{E(i)}</li>" for i in items)
    btn = '<span class="dp-btn">담당자에게 문의</span>' if button else ""
    return (f'<div class="dp"><div class="dp-h" style="background:{color}">{E(title)}<small>㈜금진</small></div>'
            f'<ul>{lis}</ul>{btn}</div>')


def bar_chart(values, title="호기별 불량률(%)"):
    """values: [('1호기', 2.7), ...] → 간단 막대 그림(HTML)."""
    mx = max(v for _, v in values) or 1
    bars = "".join(f'<div class="bc-r"><span>{E(k)}</span><div class="bc-b" style="width:{v / mx * 100:.0f}%"></div><b>{v}%</b></div>'
                   for k, v in values)
    return f'<div class="bc"><div class="bc-t">{E(title)}</div>{bars}</div>'


def claude_web(messages, preview_html="", input_text="Claude에게 물어보기", marks=None, preview_marks=None, attach_mark=None,
               preview_title="부서 소개 페이지", dd=""):
    """claude.ai 화면. 왼쪽 대화 + (preview_html이 있으면) 오른쪽 미리보기 패널.
    marks={메시지순번: 번호, 'input': 번호, 'send': 번호}, preview_marks={'menu': 번호, 'tab': 번호}"""
    marks = marks or {}
    pm = preview_marks or {}
    msgs = []
    for i, (who, text) in enumerate(messages):
        h = f'<div class="msg {who}">{E(text)}</div>'
        msgs.append(mk(h, marks[i], block=True) if i in marks else h)
    if not messages:
        msgs.append('<div class="hello"><b>✻ 좋은 오후입니다</b>무엇을 도와드릴까요?</div>')
    att = '<span class="cw-att">＋</span>'
    att = mk(att, attach_mark) if attach_mark else att
    inp = f'<span>{E(input_text)}</span>'
    inp = mk(inp, marks["input"]) if "input" in marks else inp
    send = '<span class="send">↑</span>'
    send = mk(send, marks["send"]) if "send" in marks else send
    left = f'<div class="cw-chat chat">{"".join(msgs)}<div class="inbox">{att}{inp}{send}</div></div>'
    right = ""
    if preview_html:
        tabs = '<span class="on">미리보기</span><span>코드</span>'
        tabs = mk(tabs, pm["tab"]) if "tab" in pm else tabs
        menu = '<span class="cw-menu">⋯ ⬇</span>'
        menu = mk(menu, pm["menu"]) if "menu" in pm else menu
        right = (f'<div class="cw-prev"><div class="cw-ph"><b>{E(preview_title)}</b><span class="cw-tabs">{tabs}</span>{menu}{dd}</div>'
                 f'<div class="cw-pb">{preview_html}</div></div>')
    return (f'<div class="win-top"><span class="win-icon" style="background:#c96442"></span><span class="win-title">Claude</span>'
            f'<span class="cw-acct">claude.ai</span></div><div class="cw{" split" if preview_html else ""}">{left}{right}</div>')


def start_search(query, result="Windows PowerShell", sub="앱", marks=None):
    """시작 메뉴 검색 화면. marks={'search':1,'result':2,'open':3}"""
    marks = marks or {}

    def m(k, h):
        return mk(h, marks[k]) if k in marks else h
    return (f'<div class="sm">{m("search", f"<div class=sm-q>🔍 {E(query)}</div>")}'
            f'<div class="sm-b"><div class="sm-l"><div class="sm-h">가장 일치하는 항목</div>'
            f'{m("result", f"<div class=sm-best><span class=ps-ico>&gt;_</span> <b>{E(result)}</b><br><small>{E(sub)}</small></div>")}</div>'
            f'<div class="sm-r"><div class="ps-ico big">&gt;_</div><b>{E(result)}</b><small>{E(sub)}</small>'
            f'{m("open", "<div class=sm-act>▢ 열기</div>")}<div class="sm-act dim">🛡 관리자로 실행</div></div></div></div>')


GJ_CSS = r"""
.ps-top{display:flex;align-items:center;gap:8px;background:#fff;border-bottom:1px solid #d0d4da;padding:6px 10px;font-size:12.5px}
.ps-ico{display:inline-block;background:#012456;color:#fff;font:700 10px/16px Consolas,monospace;padding:0 4px;border-radius:3px}
.ps-ico.big{font-size:22px;line-height:40px;padding:0 10px;margin:6px auto;display:block;width:max-content}
.ps-ctl{margin-left:auto;color:#5f6368;letter-spacing:6px}
.ps-body{background:#012456;color:#eef3ff;font:12.5px/1.6 Consolas,'D2Coding','Malgun Gothic',monospace;padding:12px 14px;margin:0;min-height:200px;white-space:pre-wrap;word-break:break-all}
.ps-body .pp{color:#f5f5f5}
.ps-body .ok{color:#7ee787}.ps-body .er{color:#ff7b72}.ps-body .dim{color:#9fb3d9}.ps-body .y{color:#ffd866}
.cur{animation:none;color:#c9d1d9}
.cc-body{background:#0d1117;color:#e6edf3;font:12.5px/1.55 Consolas,'D2Coding','Malgun Gothic',monospace;padding:12px 14px;min-height:220px}
.cc-path{color:#8b949e;font-size:11px;margin-bottom:6px}
.cc-welcome{border:1px solid #d97757;border-radius:6px;padding:8px 10px;margin-bottom:10px}
.cc-welcome b{color:#d97757}
.cc-dim{color:#8b949e;font-size:11.5px}
.cc-u{color:#e6edf3;background:#161b22;border-left:3px solid #8b949e;padding:4px 8px;margin:6px 0;white-space:pre-wrap}
.cc-a{margin:6px 0;white-space:pre-wrap}.cc-dot{color:#d97757}
.cc-tool{color:#8b949e;margin:-2px 0 6px 14px;white-space:pre-wrap}
.cc-perm{border:1px solid #d97757;border-radius:6px;padding:8px 10px;margin:8px 0}
.cc-perm b{display:block;margin-bottom:4px}
.cc-perm .on{color:#7ee787}
.cc-in{border:1px solid #6e7681;border-radius:6px;padding:6px 10px;margin-top:10px}
.cc-hint{color:#6e7681;font-size:11px;margin-top:3px}
.cc-body .mk,.ps-body .mk{outline-color:#ff5a52}
.ins{display:flex;min-height:190px}
.ins-side{width:96px;color:#fff;font-size:34px;display:flex;align-items:flex-start;justify-content:center;padding-top:22px}
.ins-main{padding:14px 16px;flex:1}
.ins-main h4{font-size:15px;margin-bottom:8px}
.ins-main p{margin:6px 0;color:#3c4043}
.ins-btns{display:flex;justify-content:flex-end;gap:8px;padding:10px 14px;border-top:1px solid #e0e0e0;background:#f7f7f7}
.wbtn{display:inline-block;border:1px solid #adb5bd;background:#fff;border-radius:4px;padding:4px 16px;font-size:12px}
.wbtn.p{background:#1a73e8;border-color:#1a73e8;color:#fff}
.wcb{margin:8px 0;display:flex;align-items:center;gap:6px}
.ins-big{border:1px solid #c9d1dd;border-radius:6px;padding:10px;margin:8px 0;background:#f8fbff}
.ins-big b{color:#1a4f9c;font-size:14px}
.ex-bar{padding:6px 10px;border-bottom:1px solid #e0e0e0;background:#f8f9fa;color:#5f6368}
.ex-path{background:#fff;border:1px solid #d0d4da;border-radius:4px;padding:2px 10px;color:#202124;display:inline-block;min-width:300px}
.ex-wrap{display:flex;min-height:150px}
.ex-side{width:120px;border-right:1px solid #eee;padding:8px;color:#5f6368;line-height:1.9}
.ex-t{border-collapse:collapse;flex:1;margin:4px 8px}
.ex-t th{text-align:left;color:#5f6368;font-weight:500;border-bottom:1px solid #eee;padding:4px}
.ex-t td{padding:5px 4px}.ex-k{color:#5f6368}
.br-tabs{background:#dee1e6;padding:6px 8px 0}
.br-tab{display:inline-block;background:#fff;border-radius:8px 8px 0 0;padding:4px 14px;font-size:12px}
.br-bar{background:#fff;padding:6px 10px;border-bottom:1px solid #e0e0e0;color:#5f6368}
.br-url{background:#f1f3f4;border-radius:14px;padding:3px 12px;color:#202124;display:inline-block;min-width:330px}
.br-page{padding:14px;background:#f5f6f8;min-height:170px}
.dp{background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.12);max-width:330px;margin:0 auto}
.dp-h{color:#fff;padding:12px 14px;font-weight:800;font-size:15px}
.dp-h small{display:block;font-weight:400;opacity:.8;font-size:11px}
.dp ul{margin:10px 0 10px 28px;line-height:1.8}
.dp-btn{display:block;margin:0 14px 12px;background:#c9a24b;color:#1a1300;text-align:center;border-radius:6px;padding:5px;font-weight:700}
.bc{background:#fff;border-radius:8px;padding:10px 12px;box-shadow:0 1px 4px rgba(0,0,0,.1)}
.bc-t{font-weight:800;margin-bottom:6px}
.bc-r{display:flex;align-items:center;gap:6px;margin:5px 0}
.bc-r span{width:40px}.bc-b{height:14px;background:#1d3a7a;border-radius:3px}
.cw{display:block;min-height:260px;background:#faf9f7}
.cw.split{display:grid;grid-template-columns:1fr 1.15fr}
.cw-chat{min-height:260px}
.cw-acct{margin-left:auto;color:#5f6368;font-size:11px}
.cw-att{font-weight:800;color:#3c4043;padding:0 4px}
.cw-prev{border-left:1px solid #e4e7eb;background:#fff;position:relative}
.cw-ph{display:flex;align-items:center;gap:8px;padding:7px 10px;border-bottom:1px solid #eee;font-size:12px;position:relative}
.cw-tabs span{padding:2px 6px;border-radius:5px;color:#5f6368}.cw-tabs .on{background:#f0eee9;color:#202124}
.cw-menu{margin-left:auto;color:#3c4043;padding:0 4px}
.cw-pb{padding:10px;background:#f5f6f8;min-height:210px}
.sm{background:#202020;color:#fff;border-radius:8px;padding:10px;min-height:230px}
.sm-q{background:#2d2d2d;border:1px solid #555;border-radius:20px;padding:6px 14px;margin-bottom:10px}
.sm-b{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.sm-h{color:#bbb;font-size:11px;margin-bottom:6px}
.sm-best{background:#3a3a3a;border-radius:6px;padding:8px}
.sm-best small{color:#bbb}
.sm-r{background:#2b2b2b;border-radius:6px;padding:10px;text-align:center}
.sm-r small{display:block;color:#bbb;margin-bottom:8px}
.sm-act{text-align:left;padding:5px 8px;border-radius:4px;margin-top:2px}
.sm-act.dim{color:#bbb}
.store{background:#fff;padding:12px}
.store-h{display:flex;gap:10px;align-items:center}
.store-h .lg{width:46px;height:46px;border-radius:8px;background:linear-gradient(135deg,#306998,#ffd43b)}
.char-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px;margin:14px 0}
.char{border:1px solid var(--bd);border-radius:14px;padding:12px;background:#fff;display:flex;gap:10px}
.char .av{flex:0 0 54px;height:54px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:28px}
.char b{display:block;font-size:15px}
.char small{color:var(--tx2);display:block;margin:2px 0 4px}
.char .q{font-size:13.5px;color:#333;display:block}
.term-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px;margin:12px 0}
details.term{border:1px solid var(--bd);border-radius:12px;background:#fff;padding:10px 12px}
details.term summary{cursor:pointer;font-weight:800;list-style:none}
details.term summary::-webkit-details-marker{display:none}
details.term summary small{float:right;color:var(--tx2);font-weight:400;font-size:12px}
details.term[open]{background:#fbfaf6;border-color:var(--gold)}
details.term p{margin:6px 0 0;font-size:14px}
details.term .an{color:var(--gold2)}
details.qa{border:1px dashed var(--bd);border-radius:10px;padding:8px 12px;margin:8px 0;background:#fff}
details.qa summary{cursor:pointer;font-weight:700}
.light{display:inline-block;width:14px;height:14px;border-radius:50%;vertical-align:-2px;margin-right:4px}
.l-g{background:#2e9d5b}.l-y{background:#e0a400}.l-r{background:#d23b2f}
.slot{border:2px dashed #c9d1dd;border-radius:14px;padding:18px;margin:14px 0;color:var(--tx2);background:#fafbfc}
.slot b{color:var(--tx)}
"""

PROGRESS_CSS = r"""
.pass{display:flex;align-items:center;gap:8px;margin-top:10px;padding:9px 12px;border:2px solid var(--ok);border-radius:10px;background:#fff;font-weight:800;color:var(--ok);cursor:pointer;font-size:15px}
.pass input{width:20px;height:20px;accent-color:var(--ok)}
.step.passed .step-h{background:linear-gradient(90deg,#1f6b45,#2f8a5c)}
.step.passed .step-h .no::after{content:" ✓"}
.step.locked .step-b{opacity:.28;max-height:120px;overflow:hidden}
.lock-bar{display:none;align-items:center;gap:10px;padding:10px 18px;background:#f3f5f7;border-top:1px solid var(--bd);font-size:14px;color:var(--tx2)}
.step.locked .lock-bar{display:flex}
.lock-bar button{margin-left:auto;border:1px solid #c9d1dd;background:#fff;border-radius:8px;padding:4px 10px;cursor:pointer;font-size:13px}
.prog{position:sticky;top:64px;z-index:20;background:#fff;border:1px solid var(--bd);border-radius:12px;padding:10px 14px;margin:14px 0;display:flex;align-items:center;gap:12px;flex-wrap:wrap;box-shadow:0 2px 8px rgba(11,31,75,.06)}
.prog .bar{flex:1 1 180px;height:10px;background:#e8ecf2;border-radius:99px;overflow:hidden}
.prog .bar i{display:block;height:100%;width:0;background:var(--ok);transition:width .3s}
.prog b{font-size:14px}
.prog button{border:1px solid #c9d1dd;background:#fff;border-radius:8px;padding:4px 10px;cursor:pointer;font-size:12.5px}
.next-mod{display:none}.next-mod.show{display:block}
@media (max-width:860px){.prog{top:auto;position:relative}}
@media print{.step.locked .step-b{opacity:1;max-height:none}.lock-bar,.prog,.pass{display:none!important}}
"""

PROGRESS_JS = r"""
<script>
(function(){
  // 진도 관리: 단계 '통과' 체크 → 다음 단계 열림. 진도는 이 브라우저에만 저장(localStorage).
  var KEY = 'gj-vibe-progress-v1';
  var st = {};
  try { st = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { st = {}; }
  function save(){ try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) {} }
  document.querySelectorAll('.page').forEach(function(page){
    var bar = page.querySelector('.prog');
    if (!bar) return;   // 진도 막대가 있는 탭만 단계 잠금
    var steps = Array.prototype.slice.call(page.querySelectorAll('section.step'));
    var openAll = !!st['__open_' + page.id] || !!navigator.webdriver;   // 자동 점검(브라우저 자동화)에서는 잠금 해제
    steps.forEach(function(s){
      var no = s.id.slice(1);
      if (!s.querySelector('.lock-bar')) {
        var lb = document.createElement('div'); lb.className = 'lock-bar';
        lb.innerHTML = '🔒 앞 단계를 통과하면 열립니다.<button type="button">그래도 열어 보기</button>';
        lb.querySelector('button').onclick = function(){ s.classList.remove('locked'); s.dataset.peek = '1'; };
        s.appendChild(lb);
      }
      var cb = s.querySelector('.pass input');
      if (cb) {
        cb.checked = !!st[no];
        cb.onchange = function(){ st[no] = cb.checked; save(); render(); };
      }
    });
    function render(){
      var done = 0, blocked = false;
      steps.forEach(function(s){
        var no = s.id.slice(1), ok = !!st[no];
        if (ok) done++;
        s.classList.toggle('passed', ok);
        s.classList.toggle('locked', blocked && !openAll && !s.dataset.peek);
        if (!ok) blocked = true;
      });
      if (bar) {
        bar.querySelector('.bar i').style.width = (steps.length ? done / steps.length * 100 : 0) + '%';
        bar.querySelector('.cnt').textContent = done + ' / ' + steps.length + ' 단계 통과';
        bar.querySelector('.all').textContent = openAll ? '단계 잠금 켜기' : '전체 펼치기(복습)';
      }
      var nx = page.querySelector('.next-mod');
      if (nx) nx.classList.toggle('show', done === steps.length || openAll);
      if (typeof fitMocks === 'function') requestAnimationFrame(fitMocks);
    }
    if (bar) {
      bar.querySelector('.all').onclick = function(){ openAll = !openAll; st['__open_' + page.id] = openAll; save(); render(); };
      bar.querySelector('.reset').onclick = function(){
        steps.forEach(function(s){ var no = s.id.slice(1); delete st[no]; var cb = s.querySelector('.pass input'); if (cb) cb.checked = false; delete s.dataset.peek; });
        save(); render();
      };
    }
    render();
  });
})();
</script>
"""


def demo(title, intro, scenes, follow=""):
    """강사 시연 상자. 수강생이 강사 화면과 같은 순서로 보고 따라 할 수 있게 장면별로 보여준다.
    scenes: [{'do': 강사가 하는 일(HTML), 'say': 붙여넣는 요청문(복사 카드) 또는 None, 'cmd': (cid, 명령 텍스트) 또는 None,
              'see': 화면에 나오는 것(HTML)}]"""
    from lessonkit import code_block, prompt
    lis = []
    for i, s in enumerate(scenes, 1):
        say = prompt(s["say"]) if s.get("say") else ""
        cmd = code_block("따라 칠 명령", text=s["cmd"][1], cid=s["cmd"][0]) if s.get("cmd") else ""
        see = f'<div class="demo-see">👀 화면: {s["see"]}</div>' if s.get("see") else ""
        lis.append(f'<li><span class="demo-n">장면 {i}</span><div class="demo-do">{s["do"]}</div>{say}{cmd}{see}</li>')
    fol = f'<div class="demo-follow">🙋 따라 하기 · {follow}</div>' if follow else ""
    return (f'<div class="demo"><div class="demo-h">🎬 강사 시연 <b>{E(title)}</b><small>강사 화면과 같은 순서로 보세요</small></div>'
            f'<p class="demo-intro">{intro}</p><ol class="demo-s">{"".join(lis)}</ol>{fol}</div>')


DEMO_CSS = r"""
.demo{border:2px solid #7c5cff;background:#f7f4ff;border-radius:14px;padding:12px 14px;margin:12px 0}
.demo-h{font-size:15px;color:#4b2fc0;font-weight:900;display:flex;flex-wrap:wrap;align-items:baseline;gap:6px}
.demo-h b{color:#1b1440}.demo-h small{color:#6d62a8;font-weight:600;font-size:12.5px}
.demo-intro{margin:6px 0 4px;font-size:14px;color:#3d3566}
.demo-s{list-style:none;margin:6px 0 0;padding:0;counter-reset:none}
.demo-s>li{background:#fff;border:1px solid #e2dbff;border-radius:10px;padding:9px 11px;margin:8px 0}
.demo-n{display:inline-block;background:#7c5cff;color:#fff;font-weight:800;font-size:12px;border-radius:6px;padding:1px 8px;margin-bottom:4px}
.demo-do{font-size:14.5px}
.demo-see{margin-top:6px;font-size:13.5px;color:#3d3566;background:#f3f0ff;border-radius:8px;padding:6px 9px}
.demo-follow{margin-top:8px;padding:8px 11px;border-radius:10px;background:#fff6dc;font-size:14px}
.demo .prompt,.demo .code{margin-top:6px}
"""


def progress_bar(label):
    """탭 위쪽 진도 막대(진도 스크립트가 채움)."""
    return (f'<div class="prog"><b>📍 {E(label)}</b><div class="bar"><i></i></div><span class="cnt">0 / 0 단계 통과</span>'
            f'<button type="button" class="all">전체 펼치기(복습)</button><button type="button" class="reset">처음부터</button></div>')


def passed(text="내 화면도 이렇게 나왔어요 — 통과"):
    """'성공하면' 아래 통과 체크(다음 단계 열기)."""
    return f'<label class="pass"><input type="checkbox"> {E(text)}</label>'
