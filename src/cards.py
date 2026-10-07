"""포트폴리오 README용 프로젝트 카드와 역량 지도. 880 CSS px로 그려 2배 렌더한다(GitHub 본문 1:1).
휴대폰용(m0N, skill_map_m)은 400 CSS px 세로형으로 따로 그린다. README는 <picture>로 폭 600px 이하에서 이쪽을 보여 준다.

실행: python cards.py → out/*.html, 이어서 sh render.sh → out/*.png (assets/cards/에 복사)
"""
import re
from pathlib import Path

OUT = Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)
C = dict(ink="#16201B", ink2="#39453F", muted="#636E68", rule="#D4DBD5", track="#EEF1EE", accent="#1D6B52", accent_soft="#D3E9DF",
         info="#2C5A86", info_soft="#D9E5F1", warn="#9A6414", warn_soft="#F4E6C8", tan="#B9905A", surface2="#F3F5F1", bad="#AE4237")
CSS = f"""*{{box-sizing:border-box}} html,body{{margin:0;background:#fff}}
body{{font-family:"Malgun Gothic","Apple SD Gothic Neo",sans-serif;color:{C['ink']};-webkit-font-smoothing:antialiased;word-break:keep-all}}
.card{{width:880px;margin:14px;padding:26px 30px 24px;border:1px solid {C['rule']};border-radius:14px;background:#fff;position:relative;overflow:hidden}}
.card.m{{width:400px;padding:20px 20px 16px 30px}}
"""


def page(name, body):
    (OUT / f"{name}.html").write_text(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>', encoding="utf-8")


def project_card(name, no, title, line, role, period, kpis, tags, color, soft):
    k = "".join(
        f'<div style="flex:1;background:{soft};border-radius:10px;padding:12px 14px">'
        f'<div style="font-size:24px;font-weight:700;color:{color};line-height:1.15">{v}</div>'
        f'<div style="font-size:14.5px;color:{C["ink2"]};margin-top:5px;line-height:1.4">{t}</div></div>' for v, t in kpis)
    tg = "".join(f'<span style="display:inline-block;font-size:14px;color:{C["ink2"]};border:1px solid {C["rule"]};border-radius:999px;padding:2px 10px;margin:0 6px 6px 0">{t}</span>' for t in tags)
    body = (f'<div class="card" style="padding-left:40px"><div style="position:absolute;left:0;top:0;bottom:0;width:10px;background:{color}"></div>'
            f'<div style="display:flex;align-items:baseline;gap:12px"><span style="font-size:15px;font-weight:700;color:{color}">{no}</span>'
            f'<span style="font-size:25px;font-weight:700">{title}</span></div>'
            f'<div style="font-size:16.5px;color:{C["ink2"]};margin:8px 0 6px;line-height:1.5">{line}</div>'
            f'<div style="font-size:15px;color:{C["muted"]};margin-bottom:16px">{role} · {period}</div>'
            f'<div style="display:flex;gap:10px;margin-bottom:16px">{k}</div><div>{tg}</div></div>')
    page(name, body)


def skill_map(name, projects, skills, marks):
    """marks[(project, skill)] = 2(핵심) / 1(일부)"""
    head = "".join(f'<th style="font-size:14.5px;font-weight:700;color:{C["ink2"]};padding:0 4px 10px;text-align:center;width:{int(560 / len(skills))}px;line-height:1.3">{s}</th>' for s in skills)
    rows = ""
    for p, color in projects:
        cells = ""
        for s in skills:
            m = marks.get((p, s), 0)
            dot = (f'<span style="display:inline-block;width:20px;height:20px;border-radius:50%;background:{color}"></span>' if m == 2 else
                   f'<span style="display:inline-block;width:20px;height:20px;border-radius:50%;border:3px solid {color};box-sizing:border-box"></span>' if m == 1 else
                   f'<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:{C["rule"]}"></span>')
            cells += f'<td style="text-align:center;padding:9px 0;border-top:1px solid {C["track"]}">{dot}</td>'
        rows += (f'<tr><td style="font-size:16px;font-weight:700;padding:9px 12px 9px 0;border-top:1px solid {C["track"]};white-space:nowrap">'
                 f'<span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:{color};margin-right:8px"></span>{p}</td>{cells}</tr>')
    lg = (f'<div style="display:flex;gap:22px;font-size:15px;color:{C["ink2"]};margin-top:14px">'
          f'<span><span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:{C["ink2"]};vertical-align:-2px;margin-right:6px"></span>핵심으로 다룸</span>'
          f'<span><span style="display:inline-block;width:14px;height:14px;border-radius:50%;border:3px solid {C["ink2"]};box-sizing:border-box;vertical-align:-2px;margin-right:6px"></span>일부 다룸</span></div>')
    body = (f'<div class="card"><div style="font-size:23px;font-weight:700;margin-bottom:6px">프로젝트별로 다룬 역량</div>'
            f'<div style="font-size:16px;color:{C["muted"]};margin-bottom:18px">각 사례 문서에 근거 수치와 코드 위치를 적어 두었습니다.</div>'
            f'<table style="border-collapse:collapse;width:100%"><thead><tr><th></th>{head}</tr></thead><tbody>{rows}</tbody></table>{lg}</div>')
    page(name, body)


def project_card_m(name, no, title, line, role, period, kpis, tags, color, soft):
    """휴대폰용 세로 카드: 핵심 수치를 한 줄씩 쌓는다."""
    k = "".join(
        f'<div style="display:flex;align-items:baseline;gap:12px;background:{soft};border-radius:9px;padding:9px 12px;margin-bottom:7px">'
        f'<div style="font-size:21px;font-weight:700;color:{color};white-space:nowrap;min-width:92px">{v}</div>'
        f'<div style="font-size:15px;color:{C["ink2"]};line-height:1.4">{t}</div></div>' for v, t in kpis)
    tg = "".join(f'<span style="display:inline-block;font-size:14px;color:{C["ink2"]};border:1px solid {C["rule"]};border-radius:999px;padding:1px 9px;margin:0 5px 5px 0">{t}</span>' for t in tags)
    body = (f'<div class="card m"><div style="position:absolute;left:0;top:0;bottom:0;width:8px;background:{color}"></div>'
            f'<div style="font-size:14px;font-weight:700;color:{color}">{no}</div>'
            f'<div style="font-size:22px;font-weight:700;line-height:1.3;margin-top:2px">{title}</div>'
            f'<div style="font-size:16px;color:{C["ink2"]};margin:8px 0 6px;line-height:1.5">{line}</div>'
            f'<div style="font-size:14px;color:{C["muted"]};margin-bottom:12px">{role} · {period}</div>'
            f'{k}<div style="margin-top:9px">{tg}</div></div>')
    page(name, body)


def skill_map_m(name, projects, skills, marks):
    """휴대폰용 역량 지도: 프로젝트마다 핵심(채운 칩)·일부(테두리 칩) 역량을 나열한다."""
    rows = ""
    for p, color in projects:
        chips = ""
        for lvl in (2, 1):
            for sk in skills:
                if marks.get((p, sk), 0) == lvl:
                    label = re.sub(r"<br>(?!·)", " ", sk).replace("<br>", "")
                    style = (f"background:{color};color:#fff;border:1.5px solid {color}" if lvl == 2 else
                             f"background:#fff;color:{C['ink2']};border:1.5px solid {color}")
                    chips += f'<span style="display:inline-block;font-size:13.5px;border-radius:999px;padding:2px 10px;margin:0 5px 6px 0;{style}">{label}</span>'
        rows += (f'<div style="padding:10px 0 4px;border-top:1px solid {C["track"]}"><div style="font-size:16px;font-weight:700;margin-bottom:7px">'
                 f'<span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:{color};margin-right:8px"></span>{p}</div>{chips}</div>')
    body = (f'<div class="card m" style="padding-left:20px"><div style="font-size:21px;font-weight:700;margin-bottom:4px">프로젝트별로 다룬 역량</div>'
            f'<div style="font-size:14px;color:{C["muted"]};margin-bottom:12px">채운 칩은 핵심으로 다룬 역량, 테두리 칩은 일부 다룬 역량입니다.</div>{rows}</div>')
    page(name, body)


# ---------------------------------------------------------------- 프로젝트 카드
# (이름, 번호, 제목, 한 줄 소개, 역할, 기간, 핵심 수치 3개, 태그, 색, 옅은 색)
CARDS = [
    ("p01", "01", "KeyFin AI 코칭",
     "봉투 예산 앱의 AI 금융 코치. LLM은 의도만 고르고 금액·확률·기간은 시뮬레이터와 서버 코드가 계산합니다.",
     "팀 프로젝트 · AI 코칭 API 전담", "2026.08 ~ 09",
     [("9.1배", "동시 8건 응답 49.07초 → 5.40초"), ("96.2%", "운영 모델 실측 라우팅 정확도"), ("2,519개", "AI 코칭 테스트 통과")],
     ["Python", "FastAPI", "vLLM", "Qwen3.8-27B FP8", "의도 라우팅", "대규모 검증"], C["accent"], C["accent_soft"]),
    ("p06", "06", "AI 결과 품질 게이트와 운영 설계",
     "AI가 만든 문항의 AI 티를 규칙으로 잡는 검증기와, 생성형 AI를 업무에 붙일 때의 경계·역할·루프 설계 문서입니다.",
     "개인 프로젝트", "2026.05 ~ 08",
     [("11개", "보정한 HARD·SOFT 규칙"), ("10/10", "공식 샘플의 HARD 통과"), ("15개", "운영 구조로 정리한 프로젝트")],
     ["Python", "휴리스틱 검증", "카이제곱", "하네스 설계", "Mermaid"], "#5B5F97", "#E3E4F1"),
    ("p02", "02", "Sentinel-30 보이스피싱 미끼봇",
     "통화를 받아 사기범의 시간을 쓰게 하는 AI 미끼봇. 프롬프트 공격에 무너지지 않는 보안 계층과 음성 실시간성을 실측했습니다.",
     "AI 해커톤 6인 팀 · 법리·보안 트랙", "2026.05 ~ 08",
     [("3 → 0건", "공격 30건 중 성공 (보안 계층 OFF→ON)"), ("0/15건", "정상 통화 오탐 (보안 계층 ON)"), ("6개", "같은 통화로 비교한 구성")],
     ["Python", "프롬프트 공격 방어", "LLM 가드", "Qwen3-4B", "faster-whisper", "CosyVoice3"], C["info"], C["info_soft"]),
    ("p03", "03", "CCTV 후보 모델 선정과 승격 게이트",
     "모델 점수 하나 대신 역할별 후보를 같은 조건으로 비교하고, 승격은 증거를 검사하는 게이트 코드가 정합니다.",
     "AIoT 팀 프로젝트 · AI 모델 선정 담당", "2026.07 ~ 08",
     [("7개", "같은 조건으로 비교한 ReID 구성"), ("0건", "증거 없이 승격된 후보"), ("8,949개", "SHA-256 검증 후 보존한 파일")],
     ["PyTorch", "SOLIDER", "CLIP ViT-L/14", "ReID", "지식 증류", "승격 게이트"], C["warn"], C["warn_soft"]),
    ("p04", "04", "AntHill 주식 판단 트레이닝",
     "AI가 정답을 알려주지 않는 투자 판단 훈련 서비스. 규칙 엔진이 방향을 정하고 LLM은 근거 문장만 씁니다.",
     "개인 중심 · 커밋 156건 중 140건 작성(7월 기준)", "2026.05 ~ 07",
     [("3계층", "규칙이 방향, LLM이 설명, 실패하면 규칙 문장"), ("87.2%", "직접 라벨링 172건 감성 정확도 (보정 표본 포함)"), ("14,473개", "적재한 국내·해외 종목")],
     ["Django 5.2", "DRF", "SimpleJWT", "OpenRouter", "Canvas 2D", "Playwright"], C["tan"], "#F1E6D6"),
    ("p05", "05", "Strategy Arena 백테스트 검증",
     "백테스트 곡선이 성과로 읽히지 않도록 사전등록, 시간순 홀드아웃, 비용, 시행 횟수 보정을 얹은 전략 빌더입니다.",
     "개인 프로젝트", "2026.07 ~ 08",
     [("19개", "후보마다 거치는 검증 게이트"), ("0/4개", "사전등록 후보 중 비용 반영 후 통과"), ("40/40", "데이터 절단 버그 교정 후 정합 종목")],
     ["Python", "Flask", "pandas", "사전등록", "홀드아웃", "DSR"], "#4E6E8E", "#DFE7EF"),
]
for c in CARDS:
    project_card(*c)
    project_card_m("m" + c[0][1:], *c[1:])

PJ = [("KeyFin AI 코칭", C["accent"]), ("Sentinel-30", C["info"]), ("CCTV 모델 선정", C["warn"]), ("AntHill", C["tan"]),
      ("Strategy Arena", "#4E6E8E"), ("AI 품질 게이트", "#5B5F97")]
SK = ["LLM 응용<br>·서빙", "평가·검증<br>설계", "백엔드<br>·API", "데이터 분석<br>·통계", "금융<br>도메인", "비전·음성<br>모델"]
M = {}
for pj, vals in zip([p for p, _ in PJ], [(2, 2, 2, 1, 2, 0), (2, 2, 1, 0, 1, 2), (1, 2, 0, 1, 0, 2), (1, 1, 2, 2, 2, 0), (0, 2, 1, 2, 2, 0), (1, 2, 0, 1, 0, 0)]):
    for sk, v in zip(SK, vals):
        M[(pj, sk)] = v
skill_map("skill_map", PJ, SK, M)
skill_map_m("skill_map_m", PJ, SK, M)
print("html:", len(list(OUT.glob("*.html"))))
