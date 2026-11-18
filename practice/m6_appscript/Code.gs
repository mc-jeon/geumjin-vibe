/**
 * 금진 생산관리 앱 — 정답 예시 (모듈 6)
 * 구글 시트의 확장 프로그램 > Apps Script 에 붙여넣어 씁니다. 교육용 가상 데이터용입니다.
 * 버튼 3개: ① 호기별 집계  ② 불량률 높은 행 표시  ③ 실적 입력 창
 * 불량률 = 불량량 합계 ÷ 생산량 합계 × 100, 소수 첫째 자리 (날짜별 평균을 내지 않음)
 */
const DATA_SHEET = '생산실적';
const SUMMARY_SHEET = '집계';
const LIMIT = 3.0; // 불량률 표시 기준(%)

/** 시트를 열 때 위쪽에 '🏭 금진 도구' 메뉴를 만든다. */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('🏭 금진 도구')
    .addItem('① 호기별 집계', 'summarizeByLine')
    .addItem('② 불량률 높은 행 표시', 'highlightHighDefect')
    .addItem('③ 실적 입력 창', 'showInputForm')
    .addToUi();
}

/** 생산실적의 데이터 행(머리글 제외)을 읽는다. 빈 행은 뺀다. */
function readRows_() {
  const sh = SpreadsheetApp.getActive().getSheetByName(DATA_SHEET);
  if (!sh) throw new Error("'" + DATA_SHEET + "' 탭이 없습니다.");
  const values = sh.getDataRange().getValues();
  return values.slice(1).filter(function (r) { return r[0] !== '' && r[2] !== ''; });
}

/** 호기별 합계와 불량률을 계산한다(시트를 건드리지 않는 순수 계산). */
function calcByLine_(rows) {
  const by = {};
  let totalQty = 0, totalBad = 0;
  rows.forEach(function (r) {
    const line = Number(r[2]), qty = Number(r[3]), bad = Number(r[4]);
    if (!by[line]) by[line] = { qty: 0, bad: 0 };
    by[line].qty += qty; by[line].bad += bad;
    totalQty += qty; totalBad += bad;
  });
  const rate = function (b, q) { return q ? Math.round(b / q * 1000) / 10 : 0; };
  const out = Object.keys(by).sort().map(function (k) {
    return [k + '호기', by[k].qty, by[k].bad, rate(by[k].bad, by[k].qty)];
  });
  out.push(['전체', totalQty, totalBad, rate(totalBad, totalQty)]);
  return out;
}

/** ① '집계' 탭을 새로 만들어(있으면 비우고) 호기별 생산량·불량량·불량률을 적는다. */
function summarizeByLine() {
  const rows = readRows_();
  const table = calcByLine_(rows);
  const ss = SpreadsheetApp.getActive();
  const sh = ss.getSheetByName(SUMMARY_SHEET) || ss.insertSheet(SUMMARY_SHEET);
  sh.clear();
  sh.getRange(1, 1, 1, 4).setValues([['호기', '생산량(m)', '불량량(m)', '불량률(%)']]).setFontWeight('bold').setBackground('#eef2f8');
  sh.getRange(2, 1, table.length, 4).setValues(table);
  sh.getRange(2, 2, table.length, 2).setNumberFormat('#,##0');
  sh.getRange(table.length + 1, 1, 1, 4).setFontWeight('bold');
  sh.getRange(table.length + 3, 1).setValue('대조: ' + rows.length + '행 · 계산 시각 ' + new Date().toLocaleString('ko-KR'));
  ss.setActiveSheet(sh);
  ss.toast('호기별 집계를 만들었습니다(' + rows.length + '행).', '🏭 금진 도구');
}

/** ② 행별 불량률이 기준(LIMIT %) 이상인 행을 노란색으로 칠한다. 다시 누르면 새로 칠한다. */
function highlightHighDefect() {
  const sh = SpreadsheetApp.getActive().getSheetByName(DATA_SHEET);
  const values = sh.getDataRange().getValues();
  const n = values.length - 1;
  if (n < 1) return;
  sh.getRange(2, 1, n, values[0].length).setBackground(null);
  let count = 0;
  for (let i = 1; i < values.length; i++) {
    const qty = Number(values[i][3]), bad = Number(values[i][4]);
    if (qty > 0 && bad / qty * 100 >= LIMIT) {
      sh.getRange(i + 1, 1, 1, values[0].length).setBackground('#fff1c2');
      count++;
    }
  }
  SpreadsheetApp.getActive().toast('불량률 ' + LIMIT + '% 이상 ' + count + '행을 표시했습니다.', '🏭 금진 도구');
}

/** ③ 실적 입력 창(Input.html)을 띄운다. */
function showInputForm() {
  const html = HtmlService.createHtmlOutputFromFile('Input').setWidth(360).setHeight(430);
  SpreadsheetApp.getUi().showModalDialog(html, '생산 실적 입력');
}

/** 입력 창에서 받은 값을 확인하고 생산실적 맨 아래에 한 줄 더한다. */
function addEntry(f) {
  const qty = Number(f.qty), bad = Number(f.bad), line = Number(f.line);
  if (!f.date || !f.code) throw new Error('생산일자와 제품코드를 넣어 주세요.');
  if ([1, 2, 3].indexOf(line) < 0) throw new Error('호기는 1, 2, 3 중 하나입니다.');
  if (!(qty > 0)) throw new Error('생산량은 0보다 커야 합니다.');
  if (!(bad >= 0) || bad > qty) throw new Error('불량량은 0 이상, 생산량 이하여야 합니다.');
  SpreadsheetApp.getActive().getSheetByName(DATA_SHEET)
    .appendRow([f.date, f.code, line, qty, bad, Number(f.minutes) || '', Number(f.temp) || '']);
  return '추가했습니다: ' + f.date + ' ' + line + '호기 ' + qty + 'm';
}
