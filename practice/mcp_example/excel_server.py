"""생산실적 조회 MCP 서버(정답 예시) — 금진 바이브코딩 모듈 5 심화(5-22).

프로젝트 폴더의 data 폴더에 있는 생산실적 엑셀을 읽어 호기별 불량률을 알려준다.
인터넷에 나가지 않고 내 PC 안의 파일만 읽는다. 원본 엑셀은 읽기만 하고 고치지 않는다.

준비:   pip install mcp openpyxl
등록:   claude mcp add mes -- python mcp/excel_server.py   (gj-report 폴더에서)
"""
from pathlib import Path

from openpyxl import load_workbook
from mcp.server.mcpserver import MCPServer

DATA = Path(__file__).resolve().parent.parent / "data"   # gj-report\data
mcp = MCPServer("mes")


def _rows(file: str):
    path = DATA / Path(file).name   # data 폴더 밖의 파일은 열지 않는다
    if not path.exists():
        raise ValueError(f"data 폴더에 {path.name} 파일이 없습니다. list_files로 이름을 확인하세요.")
    ws = load_workbook(path, read_only=True, data_only=True)["생산실적"]
    rows = ws.iter_rows(values_only=True)
    head = next(rows)
    return [dict(zip(head, r)) for r in rows if r and r[0]]


@mcp.tool()
def list_files() -> list[str]:
    """data 폴더에 있는 생산실적 엑셀 파일 이름 목록을 알려준다."""
    return sorted(p.name for p in DATA.glob("*.xlsx"))


@mcp.tool()
def defect_rate(file: str, line: int | None = None) -> dict:
    """생산실적 엑셀 하나로 호기별 생산량·불량량·불량률을 계산한다.

    file: data 폴더의 엑셀 파일 이름(예: mes_sample_oct.xlsx). 몇 월 파일인지 모르면 list_files를 먼저 부른다.
    line: 호기 번호(1·2·3). 비우면 전체 호기와 합계를 모두 돌려준다.
    불량률 = 불량량 합계 ÷ 생산량 합계 × 100, 소수 첫째 자리.
    """
    data = _rows(file)
    result = {"파일": Path(file).name, "행 수": len(data), "호기별": {}}
    for no in sorted({r["호기"] for r in data}):
        if line and no != line:
            continue
        part = [r for r in data if r["호기"] == no]
        made, bad = sum(r["생산량(m)"] for r in part), sum(r["불량량(m)"] for r in part)
        result["호기별"][f"{no}호기"] = {"생산량(m)": made, "불량량(m)": bad, "불량률(%)": round(bad / made * 100, 1)}
    if not line:
        made, bad = sum(r["생산량(m)"] for r in data), sum(r["불량량(m)"] for r in data)
        result["전체"] = {"생산량(m)": made, "불량량(m)": bad, "불량률(%)": round(bad / made * 100, 1)}
    return result


if __name__ == "__main__":
    mcp.run()
