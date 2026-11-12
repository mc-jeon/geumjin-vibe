"""날씨 MCP 서버(정답 예시) — 금진 바이브코딩 모듈 5 심화(5-21).

열쇠(API 키)가 필요 없는 공개 날씨 서비스 Open-Meteo(api.open-meteo.com)에서
지금 날씨를 가져온다. Claude Code에 등록하면 "천안 공장 지금 습도 알려줘"처럼 말로 부를 수 있다.

준비:   pip install mcp
등록:   claude mcp add weather -- python mcp/weather_server.py   (gj-report 폴더에서)
"""
import json
import urllib.parse
import urllib.request

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("weather")


@mcp.tool()
def current_weather(latitude: float, longitude: float, place: str = "") -> dict:
    """지금 날씨(기온·습도·강수량·풍속)를 알려준다.

    사용자가 도시 이름만 말하면 그 도시의 위도·경도를 직접 넣어서 부른다.
    예: 천안 36.81, 127.11 / 서울 37.57, 126.98 / 일산 37.66, 126.77
    place에는 사용자가 말한 장소 이름을 그대로 넣는다(결과 표시용).
    """
    query = urllib.parse.urlencode({
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
        "timezone": "Asia/Seoul",
    })
    with urllib.request.urlopen("https://api.open-meteo.com/v1/forecast?" + query, timeout=15) as res:
        now = json.load(res)["current"]
    return {
        "장소": place or f"{latitude}, {longitude}",
        "기준시각": now["time"],
        "기온(℃)": now["temperature_2m"],
        "습도(%)": now["relative_humidity_2m"],
        "강수량(mm)": now["precipitation"],
        "풍속(km/h)": now["wind_speed_10m"],
        "출처": "Open-Meteo (api.open-meteo.com)",
    }


if __name__ == "__main__":
    mcp.run()
