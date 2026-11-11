# 금진 바이브코딩 교안

㈜금진 임직원 대상 바이브코딩(Claude Code) 실습 교안. 단일 페이지 `index.html`을 Python 스크립트로 생성하고 Cloudflare Workers(정적 자산)로 배포한다.

- 배포 주소: https://geumjin-vibe.edunfuture.workers.dev/
- 배포 방식: `main` 브랜치에 푸시하면 Cloudflare가 자동 배포

## 다른 PC에서 이어서 작업하기

```powershell
git clone https://github.com/mc-jeon/geumjin-vibe.git geumjin-vibe-lesson
cd geumjin-vibe-lesson
python -m pip install -r requirements.txt
python src/build.py .          # → index.html 다시 생성
```

- Python 3.11 이상(작성 환경: 3.13)
- 작업 전 `git pull`, 작업 후 `git add` → `git commit` → `git push`
- Claude Code로 작업할 때는 `CLAUDE.md`에 프로젝트 맥락과 남은 할 일이 정리돼 있다.

## 폴더 구성

| 경로 | 내용 |
|---|---|
| `index.html` | 빌드 결과물(배포되는 교안). 직접 고치지 말고 `src/`를 고친 뒤 빌드 |
| `src/build.py` | 빌드 진입점 · 모듈 1·2 |
| `src/m3.py`, `src/m4.py` | 모듈 3(데이터 정제), 모듈 4(트랙 A~E) |
| `src/ext.py` | 모듈 5(프로젝트 폴더·스킬·MCP 노션) |
| `src/tips.py` | 모델·토큰 꿀팁 탭 |
| `src/common.py` | 모듈 3·4 공통 부품 |
| `src/lessonkit.py`, `src/mocks_*.py`, `src/lesson.css`, `src/lesson_runtime.js` | 페이지 부품·모형 화면·스타일·런타임 |
| `src/make_practice*.py` | 실습용 가상 데이터 생성 (`make_practice_m34.py` → `practice/` + `src/answers.json`) |
| `practice/` | 교육생이 내려받는 실습 파일 |
| `shots/` | 실제 화면 캡처(PNG). 이름 규칙은 `shots/README.md` |
| `_자료목록.json` | 교안에 나오는 실습 자료 목록(검증용) |
| `og_image.jpg`, `src/og*.html` | 카카오톡 미리보기 이미지 |

## 자주 쓰는 명령

```powershell
python src/make_practice_m34.py .   # 모듈 3·4 실습 데이터 + answers.json 다시 만들기(교안 숫자도 바뀜)
python src/build.py .               # 교안 빌드
```

개인정보(교육생 명단 등)는 `.gitignore`로 제외돼 있다. 명단 파일은 저장소에 올리지 않는다.
