"""모듈 3·4에서 같이 쓰는 조각: 단계 카드(+통과 체크), 강사 진행표, 따라잡기·도전 상자, 엑셀·대시보드 모형, 정답값."""
import json
from pathlib import Path

from lessonkit import E, app_window, box, grid, mk, step, table
from mocks_geumjin import passed

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
ANS = json.loads((SRC / "answers.json").read_text(encoding="utf-8"))   # make_practice_m34.py가 만든 정답값
PC = "설치와 실습은 PC에서 합니다. 휴대폰은 복습용으로 보세요. 그림은 탭하면 크게 볼 수 있습니다."
DESK = "C:\\Users\\금대리\\Desktop"
WORK = DESK + "\\geumjin-vibe"
TOOL = DESK + "\\gj-tool"


def n(v):
    """천 단위 쉼표."""
    return f"{v:,}"


def st(no, title, goal, todo, ok, stuck=None, figure="", extra="", one=False):
    return step(no, title, goal, todo, ok=ok + passed(), stuck=stuck, figure=figure, extra=extra, one=one)


def html_line(h):
    return ("html", h)


def span(cls, text):
    return f'<span class="{cls}">{E(text)}</span>'


def teach(rows, note=""):
    """강사 진행표(접힘). rows: [시간, 단계, 강사가 할 일, 넘어가는 신호]"""
    nt = f"<p>{note}</p>" if note else ""
    return ('<details class="teach"><summary>🧑‍🏫 강사 진행표 <small>시간 배분 · 강사가 할 일 · 넘어가는 신호 (누르면 펼쳐집니다)</small></summary>'
            + nt + table(["시간", "단계", "강사가 할 일", "넘어가는 신호"], rows) + "</details>")


def catchup(body):
    return box("warn", "🏃 따라잡기", body)


def more(body):
    return box("info", "💪 한 번 더(도전)", body)


def excel(rows, name, status="", colors=None, marks=None):
    """엑셀 창 모형. status: 아래 상태 표시줄 글자(HTML)."""
    st_ = f'<div class="xl-st">{status}</div>' if status else ""
    return app_window(f"{name} - Excel", grid(rows, colors) + st_, icon_color="#1d6f42", menus=["파일", "홈", "삽입", "데이터", "보기"], marks=marks)


def bars(title, values, hot=None, unit="%", wide=False):
    """막대 묶음(대시보드 모형). values: [(라벨, 값)], hot: 강조할 라벨"""
    mx = max(v for _, v in values) or 1
    rows = "".join(f'<div class="bc-r"><span>{E(k)}</span><div class="bc-b{" hot" if k == hot else ""}" style="width:{v / mx * 100:.0f}%"></div><b>{v}{unit}</b></div>'
                   for k, v in values)
    return f'<div class="bc{" w" if wide else ""}"><div class="bc-t">{E(title)}</div>{rows}</div>'


def numcards(items):
    """숫자 카드 줄. items: [(라벨, 값)]"""
    return '<div class="ncs">' + "".join(f'<div class="nc"><small>{E(a)}</small><b>{E(b)}</b></div>' for a, b in items) + "</div>"


def pills(items, on=None, mark=None):
    """선택 버튼 줄. mark=(라벨, 번호)"""
    out = []
    for it in items:
        h = f'<span class="pl{" on" if it == on else ""}">{E(it)}</span>'
        out.append(mk(h, mark[1]) if mark and mark[0] == it else h)
    return f'<div class="pls">{"".join(out)}</div>'


# ───────── 강사 승인코드로 여는 가림 상자 ─────────
# 교육생 화면에서 미리 안 보이게 가리는 용도다. 내용은 페이지 소스와 공개 저장소에 그대로 있으므로 보안 장치가 아니다.
# 승인코드는 저장소에 적지 않고 SHA-256 값만 둔다. 코드를 바꾸려면 새 코드의 SHA-256 값으로 GATE_HASH를 바꾼다.
GATE_HASH = "de508568abd9f1a5852cbab879f32b03138c4fdae49756fbf2c16fc0138b8d58"


def gate(gid, title, desc, body_html, code_hash=GATE_HASH):
    """승인코드를 넣어야 열리는 상자. 연 상태는 그 브라우저에만 기억된다(localStorage). 같은 코드(해시)의 상자는 함께 열리고 함께 닫힌다.
    닫혀 있는 동안 안의 단계는 진도 계산에서 빠진다(PROGRESS_JS가 .gate.closed 안의 단계를 세지 않음)."""
    return (f'<div class="gate closed" id="gate-{E(gid)}" data-hash="{E(code_hash)}">'
            f'<div class="gate-lock"><div class="gate-t">🔒 {E(title)}</div><p>{desc}</p>'
            '<form class="gate-f"><input type="password" autocomplete="off" placeholder="승인코드" aria-label="승인코드">'
            '<button type="submit">열기</button><span class="gate-msg"></span></form></div>'
            f'<div class="gate-body"><div class="gate-open-bar">🔓 강사 승인으로 열린 부분입니다. <button type="button" class="gate-relock">다시 가리기</button></div>{body_html}</div></div>'
            "<script>(function(){var g=document.getElementById('gate-" + gid + "'),K='gj-gate-'+g.dataset.hash.slice(0,12);"
            "try{if(localStorage.getItem(K)===g.dataset.hash)g.classList.remove('closed');}catch(e){}"
            "var f=g.querySelector('.gate-f'),m=g.querySelector('.gate-msg');"
            "f.onsubmit=function(ev){ev.preventDefault();var v=f.querySelector('input').value.trim();"
            "if(!window.crypto||!crypto.subtle){m.textContent='이 브라우저에서는 열 수 없습니다. 크롬으로 열어 주세요.';return;}"
            "crypto.subtle.digest('SHA-256',new TextEncoder().encode(v)).then(function(b){"
            "var h=Array.prototype.map.call(new Uint8Array(b),function(x){return('0'+x.toString(16)).slice(-2);}).join('');"
            "if(h===g.dataset.hash){try{localStorage.setItem(K,h);}catch(e){}location.reload();}"
            "else{m.textContent='승인코드가 맞지 않습니다.';}});};"
            "g.querySelector('.gate-relock').onclick=function(){try{localStorage.removeItem(K);}catch(e){}location.reload();};"
            "})();</script>")


COMMON_CSS = r""".prompt{padding-right:72px}ol.do>li>.prompt,ol.do>li>.code,ol.do>li>div{margin-top:8px}
.gate-lock{border:2px dashed #b9a46a;background:#fbf7ec;border-radius:14px;padding:18px 20px;margin:18px 0;text-align:center}.gate-t{font-weight:900;font-size:18px;color:#1d3a7a}.gate-lock p{color:var(--tx2);margin:8px 0 12px}.gate-f{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;align-items:center}.gate-f input{border:1px solid #c9c2ad;border-radius:8px;padding:8px 12px;font-size:16px;width:180px}.gate-f button,.gate-relock{border:0;border-radius:8px;padding:8px 16px;background:#1d3a7a;color:#fff;font-weight:700;cursor:pointer}.gate-msg{color:#b3372a;font-size:14px;width:100%}.gate.closed .gate-body{display:none}.gate:not(.closed) .gate-lock{display:none}.gate-open-bar{font-size:13.5px;color:var(--tx2);margin:14px 0 4px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}.gate-relock{padding:4px 10px;font-size:12.5px;background:#8a8f98}

details.teach{border:2px solid #c9a24b;border-radius:14px;background:#fffaf0;padding:10px 14px;margin:14px 0}
details.teach summary{cursor:pointer;font-weight:900;color:#6b4e00;font-size:15.5px}
details.teach summary small{font-weight:500;color:#8a7440;margin-left:6px}
details.teach p{margin:8px 0 4px;font-size:14px;color:#5a4a1c}
details.teach table.t{font-size:13.5px}
details.trk{border:2px solid #1d3a7a;border-radius:14px;background:#fff;margin:12px 0;overflow:hidden}
details.trk>summary{cursor:pointer;list-style:none;padding:12px 16px;background:linear-gradient(90deg,#0b1f4b,#1d3a7a);color:#fff;font-weight:900;font-size:16px}
details.trk>summary::-webkit-details-marker{display:none}
details.trk>summary small{display:block;font-weight:500;opacity:.85;font-size:13px;margin-top:2px}
details.trk>.trk-b{padding:6px 16px 14px}
details.trk h4{margin:16px 0 6px;font-size:15px;color:#1d3a7a}
.xl-st{background:#f3f3f3;border-top:1px solid #d6d6d6;padding:4px 10px;font-size:11.5px;color:#333;text-align:right}
.ncs{display:flex;gap:8px;margin:0 0 8px}
.nc{flex:1;background:#fff;border:1px solid #e3e6ec;border-radius:8px;padding:7px 9px}
.nc small{display:block;color:#5f6368;font-size:10.5px}.nc b{font-size:15px;color:#1d3a7a}
.pls{display:flex;gap:5px;margin:0 0 8px;flex-wrap:wrap}
.pl{border:1px solid #c9d1dd;border-radius:99px;padding:2px 10px;font-size:11.5px;background:#fff}
.pl.on{background:#1d3a7a;border-color:#1d3a7a;color:#fff}
.bc-b.hot{background:#c96442}
.bc+.bc{margin-top:8px}
.bc.w .bc-r span{width:62px}
.tree{background:#fbfaf6;border:1px solid var(--bd);border-radius:12px;padding:12px 14px;font:13.5px/1.75 Consolas,'D2Coding','Malgun Gothic',monospace;white-space:pre-wrap;margin:10px 0;overflow-x:auto}
.tree b{color:#1d3a7a}.tree i{color:var(--tx2);font-style:normal}
"""
