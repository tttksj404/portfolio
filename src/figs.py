"""포트폴리오 사례 문서 그림. 수치는 각 사례 문서가 인용한 원 저장소 결과 파일에서 옮겼다.

실행: python figs.py → out/*.html, 이어서 sh render.sh → out/*.png (assets/<프로젝트>/에 복사)
"""
from figkit import C, card, canvas, hbar_rows, legend, ln, nd, page, pth, tx

# ================================================================ Sentinel-30
# s1. 보안 계층 흐름
n = [
    nd(0, 0, 820, 64, "사기범 발화 (통화 한 턴)", (), "neutral", ts=17),
    nd(0, 96, 820, 78, "하네스", ["합성 입력·동의·데이터 출처 확인 · 음성 복제 요청 거부 · 최대 24턴 · 허용 도구 2개"], "det"),
    nd(0, 206, 395, 96, "① 룰 프리필터", ["제로폭 문자·base64·지시 무시 패턴", "0.021ms · 공격 30건 중 16건 여기서 차단"], "det"),
    nd(425, 206, 395, 96, "② LLM 입력 가드", ["봇을 조종하려는 입력과", "송금을 요구하는 정상 사기 대사를 구분"], "llm"),
    nd(0, 334, 395, 96, "미끼봇 응답 (Qwen3-4B)", ["동기 경로에는 응답 1콜만", "평시 저가 모델 · 위기 턴만 중급 모델"], "llm"),
    nd(425, 334, 395, 96, "③ 출력 가드", ["개인정보 마스킹 · 시스템 프롬프트 누출 차단", "차단해도 할머니 말투로 되물어 위장 유지"], "det"),
    nd(0, 462, 395, 80, "증거 추출·요약 (비동기)", ["계좌·기관 같은 필드를 구조화"], "neutral"),
    nd(425, 462, 395, 80, "운영자 검토", ["사람이 확인하기 전에는 대기(pending)"], "ask"),
]
s = [ln(410, 64, 410, 94), pth("M410 174 L410 190 L197 190 L197 204"),
     ln(395, 254, 423, 254), pth("M622 302 L622 318 L197 318 L197 332"), ln(395, 382, 423, 382),
     pth("M622 430 L622 446 L197 446 L197 460"), ln(395, 502, 423, 502)]
page("s_pipeline", card("미끼봇을 지키는 보안 계층",
                        "모델을 부르기 전에 하네스가 실행 범위를 잠그고, 입력과 출력을 세 단계로 걸러 냅니다.",
                        canvas(820, 544, n, s)))

# s2. 보안 계층 OFF/ON
AB = [("적대적 프롬프트 30건<small>봇 Haiku</small>", 3, 30, 0), ("적대적 프롬프트 30건<small>봇 Sonnet</small>", 1, 30, 0),
      ("간접 주입 15건<small>추출 단계</small>", 1, 15, 0)]
inner = legend([("보안 계층 OFF", C["bad"]), ("보안 계층 ON", C["accent"])])
for lab, off, tot, on in AB:
    inner += (f'<div class="row" style="--lab:230px;--val:120px;margin:12px 0 3px"><div class="lab" style="grid-row:span 2">{lab}</div>'
              f'<div class="track" style="height:24px"><div class="bar" style="width:{off / tot * 100 * 4:.1f}%;background:{C["bad"]}"></div></div>'
              f'<div class="val" style="color:{C["bad"]}">{off}건 <small>{off / tot * 100:.1f}%</small></div></div>'
              f'<div class="row" style="--lab:230px;--val:120px;margin:3px 0 14px"><div class="track" style="height:24px;grid-column:2">'
              f'<div class="bar" style="width:0.6%;background:{C["accent"]}"></div></div><div class="val hl">{on}건</div></div>')
page("s_ab", card("보안 계층을 켜고 끈 공격 성공 수",
                  "같은 공격 코퍼스를 보안 계층 없이(OFF)와 켜고(ON) 넣었습니다. 막대 길이는 25%를 끝으로 그렸습니다.", inner,
                  "정상 사기 대사 15건은 ON에서도 오탐 0건이었습니다. 직접 만든 소규모 코퍼스의 결과이며, 판정기가 입력 가드와 같은 모델 계열이라 독립 검증은 아닙니다."))

# s3. 6개 구성 비교
ORCH = [("T1", "단일 저가 모델 1콜", "가장 싸지만 역할 분리·요약 압축이 없어 긴 통화로 못 늘림", "보조", C["warn"]),
        ("T2", "단일 상위 모델 1콜", "비용 최상위인데 추출 F1·위장 유지는 저가 구성과 같음", "탈락", C["bad"]),
        ("T3", "상위 모델 기획 → 응답 (직렬)", "임계경로 지연 Claude 11.7초 · GPT 39.8초 · Gemini 25초", "탈락", C["bad"]),
        ("T4", "응답 동기 + 상위 모델 기획 비동기", "지연은 회복했지만 기획 비용이 그대로, 품질 이득 없음", "탈락", C["bad"]),
        ("T5", "라우터 + 응답 1콜, 추출·압축은 비동기 저가", "지연 최저 · 비용 최저권 · 추출 F1 1.00", "채택", C["accent"]),
        ("T6", "T5 + 상위 모델 기획 3턴마다", "비용 +144% · 지연 +693ms, 품질 이득 없음", "탈락", C["bad"])]
rows = ""
for t, cfg, why, dec, col in ORCH:
    hl = "background:#F3F9F6;" if dec == "채택" else ""
    rows += (f'<div style="display:grid;grid-template-columns:52px 250px 1fr 64px;gap:12px;align-items:center;padding:11px 10px;border-top:1px solid {C["track"]};{hl}">'
             f'<div style="font-size:19px;font-weight:700;color:{col}">{t}</div><div style="font-size:15.5px;font-weight:700;line-height:1.35">{cfg}</div>'
             f'<div style="font-size:15px;color:{C["ink2"]};line-height:1.4">{why}</div>'
             f'<div style="font-size:14.5px;font-weight:700;color:#fff;background:{col};border-radius:999px;text-align:center;padding:3px 0">{dec}</div></div>')
page("s_orch", card("같은 통화 6턴을 6개 구성으로 비교", "토큰, 비용, 동기 임계경로 지연, 추출 F1을 쟀고 세 모델 계열(Claude·GPT·Gemini)에서 같은 방향이 나왔습니다.",
                    rows, "비용 원화 값은 공시 단가 환산이라 모델 계열끼리 절대값은 비교하지 않았습니다."))

# s4. 첫 재생 지연
X0, PX = 230, 0.066
xm = lambda ms: X0 + ms * PX
s = [ln(xm(g), 26, xm(g), 226, w=1, end=False).replace(C["ink2"], C["track"]) for g in (0, 2000, 4000, 6000, 8000)]
s += [tx(xm(g), 250, f"{g // 1000}초", col=C["muted"], size=14.5) for g in (0, 2000, 4000, 6000, 8000)]
LAT = [(58, "Qwen3-TTS 경로", "전체 버퍼 후 재생", 6775.3, 7238.2, C["bad"]), (160, "CosyVoice3 스트리밍", "첫 청크부터 재생", 2243.55, 2512.5, C["accent"])]
for y, lab, sub, med, p95, col in LAT:
    s.append(f'<rect x="{X0}" y="{y - 20}" width="{med * PX:.1f}" height="40" rx="6" fill="{col}"/>')
    s.append(ln(xm(med), y, xm(p95), y, end=False).replace(C["ink2"], col).replace('stroke-width="2"', 'stroke-width="3"'))
    s.append(f'<line x1="{xm(p95)}" y1="{y - 12}" x2="{xm(p95)}" y2="{y + 12}" stroke="{col}" stroke-width="3"/>')
    s.append(tx(X0 - 14, y - 2, lab, col=C["ink"], size=16, anchor="end", bold=True))
    s.append(tx(X0 - 14, y + 18, sub, col=C["muted"], size=14, anchor="end"))
    s.append(tx(X0, y + 44, f"중앙값 {med:,.0f}ms · p95 {p95:,.0f}ms", col=col, size=15, anchor="start", bold=True))
s += [ln(xm(5000), 22, xm(5000), 226, "warn", 2.5, dash=True, end=False), tx(xm(5000), 16, "목표 5초", col=C["warn"], size=15, bold=True)]
page("s_latency", card("첫 재생까지 걸린 시간 (원격 L40S, 합성 턴)",
                       "기준은 전체 음성 완료가 아니라 첫 재생 가능 청크입니다. 막대는 중앙값, 선 끝은 p95입니다.",
                       canvas(820, 262, [], s),
                       "Qwen3-TTS 경로는 목표를 넘어 실패로 기록했습니다. LLM 전체 생성은 중앙값 678ms라 병목이 아니었고, TTS를 스트리밍으로 바꿔 다시 쟀습니다. 실제 ASR·전화망 구간은 빠져 있습니다."))

# ================================================================ CCTV 모델 선정
# c1. 판정 흐름
n = [nd(0, 0, 150, 92, "검토된 manifest", ["사람 검토 track"], fs=14.5, ts=16),
     nd(178, 0, 150, 92, "역할별 후보 분리", ["속성 · 검색 · 설명"], "det", fs=14.5, ts=16),
     nd(356, 0, 150, 92, "같은 조건 비교", ["strict ReID", "속성 proxy"], "det", fs=14.5, ts=16),
     nd(534, 0, 286, 92, "증거 결합", ["Top-K 검색 결과 + 속성·시간·공간"], "det", fs=14.5, ts=16),
     nd(534, 132, 286, 76, "충돌하거나 증거가 모자라면", ["review · reject"], "ask", fs=14.5, ts=16),
     nd(0, 132, 506, 150, "승격 게이트 (gate.py)", ["측정 범위 · 독립 identity label · track-heldout 적격성", "사람 검토 · 증거 파일 SHA-256 일치",
                                                 "attribute Macro-F1 0.85 · Rank-1 0.85 · Recall@5 0.95", "false-match rate 0.05 이하"], "wacc", fs=14.5, ts=16, bw=2),
     nd(0, 316, 248, 64, "APPROVED", ["0건"], "neutral", fs=14.5, ts=16),
     nd(258, 316, 248, 64, "NOT_APPROVED", ["하나라도 어긋나면 · 종료 코드 2"], "bad", fs=14.5, ts=16, tcol=C["bad"])]
s = [ln(150, 46, 176, 46), ln(328, 46, 354, 46), ln(506, 46, 532, 46), ln(677, 92, 677, 130), pth("M534 170 L508 170"),
     ln(124, 282, 124, 314), ln(382, 282, 382, 314)]
page("c_flow", card("모델 점수 대신 증거로 승격을 정하는 흐름",
                    "역할마다 후보를 따로 비교하고, 승격은 사람이 표를 읽는 대신 게이트 코드가 증거로 판정합니다.", canvas(820, 382, n, s)))

# c2. strict ReID
RE = [("SOLIDER Top-3 평균", 0.47, 0.78, True), ("SOLIDER Top-5 평균", 0.45, 0.76, False), ("SOLIDER 전체 평균", 0.42, 0.84, False),
      ("SigLIP2", 0.29, 0.64, False), ("CLIP ViT-L/14", 0.21, 0.61, False), ("DINOv2", 0.19, 0.60, False)]
X0, PW = 190, 560
xv = lambda v: X0 + v * PW
s = [ln(xv(g), 40, xv(g), 40 + len(RE) * 62, w=1, end=False).replace(C["ink2"], C["track"]) for g in (0, 0.25, 0.5, 0.75, 1.0)]
s += [tx(xv(g), 64 + len(RE) * 62, f"{g:g}", col=C["muted"], size=14) for g in (0, 0.25, 0.5, 0.75, 1.0)]
for i, (lab, r1, r5, best) in enumerate(RE):
    y = 48 + i * 62
    s.append(tx(X0 - 14, y + 26, lab, col=C["ink"], size=15.5, anchor="end", bold=best))
    s.append(f'<rect x="{X0}" y="{y}" width="{r1 * PW:.1f}" height="22" rx="4" fill="{C["info"]}"/>')
    s.append(f'<rect x="{X0}" y="{y + 24}" width="{r5 * PW:.1f}" height="22" rx="4" fill="#9DBBD9"/>')
    s.append(tx(xv(r1) + 8, y + 17, f"{r1:.2f}", col=C["info"], size=14.5, anchor="start", bold=True))
    s.append(tx(xv(r5) + 8, y + 41, f"{r5:.2f}", col=C["ink2"], size=14.5, anchor="start", bold=True))
s += [ln(xv(0.85), 30, xv(0.85), 40 + len(RE) * 62, "warn", 2.5, dash=True, end=False).replace(C["warn"], C["bad"]),
      tx(xv(0.85), 22, "Rank-1 기준 0.85", col=C["bad"], size=14, bold=True, anchor="end"),
      ln(xv(0.95), 30, xv(0.95), 40 + len(RE) * 62, "warn", 2.5, dash=True, end=False),
      tx(xv(0.95) + 4, 22, "Recall@5 0.95", col=C["warn"], size=14, bold=True, anchor="start")]
page("c_reid", card("strict ReID 6개 구성: 모두 승격 기준 미달",
                    "CHIRLA 공개 proxy, 같은 카메라·같은 시퀀스 gallery를 빼고 쟀습니다(query 95개, gallery identity 11개).",
                    legend([("Rank-1", C["info"]), ("Recall@5", "#9DBBD9")]) + canvas(820, 76 + len(RE) * 62, [], s),
                    "가장 높은 SOLIDER Top-3 평균(Rank-1 0.4737)도 기준에 못 미쳐 자동 동일인 매칭은 막고, Top-K 후보 검색에만 쓰기로 했습니다."))

# c3. CLIP 파인튜닝 곡선
EP = [(1, 0.804, 0.779), (2, 0.806, 0.783), (3, 0.799, 0.781), (4, 0.794, 0.768), (5, 0.787, 0.757)]
Wc, Hc, L, R, TOP, BOT = 820, 300, 70, 40, 30, 50
lo, hi = 0.74, 0.87
xe = lambda e: L + (e - 1) * (Wc - L - R) / 4
ye = lambda v: TOP + (1 - (v - lo) / (hi - lo)) * (Hc - TOP - BOT)
s = [f'<line x1="{L}" x2="{Wc - R}" y1="{ye(g):.1f}" y2="{ye(g):.1f}" stroke="{C["track"]}" stroke-width="1.5"/>'
     f'<text x="{L - 10}" y="{ye(g) + 5:.1f}" font-size="14" fill="{C["muted"]}" text-anchor="end">{g:.2f}</text>' for g in (0.76, 0.80, 0.84)]
s += [f'<line x1="{L}" x2="{Wc - R}" y1="{ye(0.85):.1f}" y2="{ye(0.85):.1f}" stroke="{C["bad"]}" stroke-width="2.5" stroke-dasharray="7 5"/>',
      tx(Wc - R, ye(0.85) - 10, "목표 mA 0.85", col=C["bad"], size=15, bold=True, anchor="end"),
      f'<line x1="{xe(2)}" x2="{xe(2)}" y1="{TOP}" y2="{Hc - BOT}" stroke="{C["muted"]}" stroke-width="1.5" stroke-dasharray="3 4"/>',
      tx(xe(2) + 10, ye(0.825), "val 최고 epoch 2 선택", col=C["ink2"], size=14.5, anchor="start")]
for key, col, dy in ((1, C["info"], -14), (2, C["warn"], 26)):
    pts = " ".join(f"{xe(e):.1f},{ye(v[key - 1]):.1f}" for e, *v in EP)
    s.append(f'<polyline fill="none" stroke="{col}" stroke-width="3" points="{pts}"/>')
    for e, *v in EP:
        s.append(f'<circle cx="{xe(e):.1f}" cy="{ye(v[key - 1]):.1f}" r="5.5" fill="#fff" stroke="{col}" stroke-width="3"/>')
        s.append(tx(xe(e) + (12 if e == 1 else 0), ye(v[key - 1]) + dy, f"{v[key - 1]:.3f}", col=col, size=14.5, bold=e == 2, anchor="start" if e == 1 else "middle"))
s += [tx(xe(e), Hc - BOT + 28, f"epoch {e}", col=C["ink2"], size=14.5) for e, *_ in EP]
page("c_clip", card("CLIP ViT-L/14 부분 파인튜닝: epoch 2 이후 하락, 목표 미달",
                    "PA-100K 공식 분할(80k/10k/10k)에서 마지막 2 block만 학습했습니다. 선택은 test가 아니라 val mA로 했습니다.",
                    legend([("val mA", C["info"]), ("test mA", C["warn"])]) + canvas(820, Hc, [], s)))

# ================================================================ Strategy Arena
# a1. 검증 흐름
n = [nd(0, 0, 190, 96, "사전등록", ["후보·파라미터·비용·", "분할을 먼저 동결"], "neutral", fs=14.5, ts=16),
     nd(210, 0, 190, 96, "비용 반영 재생", ["t 종가 신호", "t+1 시가 체결"], "det", fs=14.5, ts=16),
     nd(420, 0, 190, 96, "앞 80%로만 선택", ["후보 고르기는", "앞 구간에서만"], "det", fs=14.5, ts=16),
     nd(630, 0, 190, 96, "뒤 20% 홀드아웃", ["선택된 1개만", "한 번 평가"], "det", fs=14.5, ts=16),
     nd(150, 140, 520, 96, "19개 게이트", ["데이터 검증 · 과최적화 민감도 · 워크포워드 · 비용 후 표본 외", "부트스트랩 · 스트레스 · 낙폭 · 레짐 · BTC 상관 · 누적 시행 수 반영 DSR"], "wacc", fs=14.5, ts=16, bw=2),
     nd(0, 280, 400, 76, "NO_RELIABLE_WINNER", ["못 통과하면 기각 사유를 기록"], "bad", fs=14.5, ts=16, tcol=C["bad"]),
     nd(420, 280, 400, 76, "paper 전진검증 대상", ["실주문 없는 원장으로만, 실거래 아님"], "neutral", fs=14.5, ts=16)]
s = [ln(190, 48, 208, 48), ln(400, 48, 418, 48), ln(610, 48, 628, 48), pth("M725 96 L725 118 L410 118 L410 138"),
     pth("M300 236 L300 254 L200 254 L200 278"), pth("M520 236 L520 254 L620 254 L620 278"),
     tx(250, 270, "아니오", col=C["bad"], size=14.5, bold=True), tx(570, 270, "예", col=C["accent"], size=14.5, bold=True)]
page("a_flow", card("백테스트를 성과로 착각하지 않게 만든 검증 순서",
                    "선택과 평가를 시간순으로 나누고, 비용과 시행 횟수를 반영해야만 다음 단계로 넘어갑니다.", canvas(820, 358, n, s)))

# a2. 후보가 검증을 지나며 남은 수
from figkit import stacked
L3 = [("통과", C["accent"]), ("탈락", C["bad"]), ("판정 불가", C["grey"])]
inner = stacked([("wave1 사전등록<small>후보 15개</small>", [0, 15, 0], "통과 0"),
                 ("심층 검증<small>후보 5개</small>", [1, 2, 2], "통과 1 (F1f)"),
                 ("5x 리플레이<small>후보 4개, 비용 후</small>", [0, 4, 0], "통과 0")], L3, 15, 200, 130, 34)
page("a_funnel", card("검증 단계별로 살아남은 후보 수",
                      "통과한 전략보다 떨어진 전략과 그 이유를 기록하는 데 무게를 뒀습니다.", inner,
                      "5x 리플레이 후보 4개는 비용 후 검증 수익률 하한이 모두 음수(-1.40 ~ -1.50%)라 판정을 NO_RELIABLE_WINNER로 남겼습니다. 어느 수치도 실거래 성과가 아닙니다."))

# ================================================================ AI 품질 도구
# q1. 보정 결과
inner = legend([("HARD 규칙 (하나라도 실패하면 탈락)", C["accent"]), ("SOFT 신호 (품질 점수)", "#5B5F97")])
rows = [("HARD 7개 규칙<small>각각</small>", 10, "10/10", C["accent"]), ("구체 수치", 0, "0/10", "#5B5F97"), ("문서 링크", 0, "0/10", "#5B5F97"),
        ("산업 맥락", 1, "1/10", "#5B5F97"), ("혼동 개념쌍", 2, "2/10", "#5B5F97")]
inner += hbar_rows(rows, 10, C["accent"], 170, 80)
page("q_calib", card("AWS 공식 샘플 10문항으로 규칙 보정",
                     "사람이 쓴 공식 문항이 HARD 규칙에 걸리면 규칙이 과한 것으로 보고 임계값을 고치거나 SOFT로 옮겼습니다.", inner,
                     "공식 샘플의 평균 품질 점수는 8/100이었습니다. AI 티는 없지만 시나리오가 밋밋하다는 뜻이라, 이 신호들은 탈락 기준이 아니라 점수로만 씁니다."))

# q2. 하네스·루프 구조
n = [nd(0, 0, 150, 80, "업무 요청", ["위험·데이터", "등급 분류"], fs=14.5, ts=16),
     nd(168, 0, 150, 80, "하네스", ["권한·도구·", "출력 계약"], "det", fs=14.5, ts=16),
     nd(336, 0, 150, 80, "오케스트레이션", ["검색·작성·", "검토 라우팅"], "det", fs=14.5, ts=16),
     nd(504, 0, 150, 80, "실행 그래프", ["분기·join·", "checkpoint"], "det", fs=14.5, ts=16),
     nd(672, 0, 148, 80, "모델·도구 실행", (), "llm", fs=14.5, ts=16),
     nd(504, 120, 316, 70, "근거·구조·정책 검증", ["승격 기준을 통과했나"], "wacc", fs=14.5, ts=16, bw=2),
     nd(504, 230, 150, 76, "사람 승인", ["후 업무 반영"], "neutral", fs=14.5, ts=16),
     nd(670, 230, 150, 76, "보류·fallback", ["실패 기록"], "bad", fs=14.5, ts=16, tcol=C["bad"]),
     nd(168, 230, 300, 76, "지표·trace·피드백", ["다음 루프의 테스트·규칙·절차로"], "ask", fs=14.5, ts=16)]
s = [ln(150, 40, 166, 40), ln(318, 40, 334, 40), ln(486, 40, 502, 40), ln(654, 40, 670, 40), ln(746, 80, 746, 118),
     pth("M579 190 L579 228"), pth("M745 190 L745 228"), tx(565, 214, "예", col=C["accent"], size=14.5, bold=True, anchor="end"),
     tx(758, 214, "아니오", col=C["bad"], size=14.5, bold=True, anchor="start"), ln(504, 268, 470, 268), pth("M670 296 L660 296 L660 326 L318 326 L318 308"),
     pth("M168 268 L75 268 L75 82")]
page("q_loop", card("생성형 AI를 업무에 붙이는 운영 구조",
                    "모델 이름보다 먼저 권한, 역할, 검증, 실패의 되먹임을 정합니다. 개인 환경과 프로젝트에서 시험한 방식입니다.", canvas(820, 330, n, s)))

# ================================================================ AntHill
# h1. 판단 엔진과 훈련 루프
n = [nd(0, 0, 190, 84, "뉴스·시세 수집", ["RSS·Naver·Stooq·Yahoo", "다중 폴백"], fs=14.5, ts=16),
     nd(210, 0, 190, 84, "종목 매핑", ["종목 14,473개", "KR + US"], fs=14.5, ts=16),
     nd(420, 0, 190, 84, "감성·키워드", ["사전 기반 감성", "TF-IDF 키워드"], fs=14.5, ts=16),
     nd(630, 0, 190, 84, "규칙 엔진", ["방향 결정", "+ evidence_trace"], "det", fs=14.5, ts=16, bw=2),
     nd(420, 120, 400, 96, "방향 = 감성 0.4 + 기술 신호 0.4 + 키워드 0.2", ["감성과 기술 신호가 크게 엇갈리면 중립", "항목별 값·가중치·기여도·이유를 응답에 공개"], "det", fs=14.5, ts=15.5),
     nd(0, 120, 400, 96, "LLM 코치 (근거 문장만)", ["정해진 방향은 바꾸지 않음 · JSON 검증", "키가 없거나 실패하면 규칙 문장으로 대체"], "llm", fs=14.5, ts=16),
     nd(0, 256, 190, 76, "① 사용자 판단", ["매수·보유·매도 먼저"], "ask", fs=14.5, ts=16),
     nd(210, 256, 190, 76, "② AI 기준선 공개", ["같은 시점의 근거"], "neutral", fs=14.5, ts=16),
     nd(420, 256, 190, 76, "③ 결과 확정", ["기준일 뒤 뉴스는 차단"], "neutral", fs=14.5, ts=16),
     nd(630, 256, 190, 76, "④ 복기", ["실수 4유형 집계", "→ 다음 체크리스트"], "det", fs=14.5, ts=16)]
s = [ln(190, 42, 208, 42), ln(400, 42, 418, 42), ln(610, 42, 628, 42), ln(725, 84, 725, 118), ln(420, 168, 402, 168),
     ln(190, 294, 208, 294), ln(400, 294, 418, 294), ln(610, 294, 628, 294), pth("M725 332 L725 352 L95 352 L95 334", dash=True)]
page("h_engine", card("방향은 규칙이, 설명은 LLM이 맡는 판단 훈련",
                      "같은 케이스를 다시 풀어도 AI 판단이 같아야 학습 신호가 됩니다. 그래서 LLM은 방향을 정하지 않습니다.", canvas(820, 356, n, s)))

# h2. 감성값을 어디까지 쓰나
from figkit import stacked
L4 = [("방향 신호로 사용", C["accent"]), ("판단 보류", C["warn"]), ("시장 맥락으로만", C["info"]), ("개별 종목 점수에서 제외", C["grey"])]
inner = stacked([("뉴스 350건<small>감성값 사용 범위</small>", [60, 57, 163, 70], "")], L4, 350, 190, 80, 40)
inner += hbar_rows([("직접 라벨링 172건<small>전체 정확도</small>", 87.21, "87.2%", C["accent"]), ("방향성 신호만", 97.52, "97.5%", C["accent"])], 100, C["accent"], 190, 80)
page("h_sentiment", card("감성 분석 결과를 그대로 쓰지 않은 이유",
                         "정확도를 올리는 데서 멈추지 않고, 여러 종목·시장 전반 기사는 개별 종목 점수에서 빼는 게이트를 만들었습니다.", inner,
                         "172건에는 사전을 보정할 때 쓴 99건이 들어 있어 독립 검증은 아닙니다. 보정 표본의 100%는 일반화 수치로 쓰지 않았습니다."))
