"""포트폴리오 그림 공통 부품. KeyFin 문서 그림 생성기(keyfin-ai-coaching/docs/images/src/figures.py)에서 가져왔다."""
import collections
import datetime as dt
from pathlib import Path

OUT = Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)

C = dict(ink="#16201B", ink2="#39453F", muted="#636E68", rule="#D4DBD5", track="#EEF1EE", bg="#FFFFFF",
         accent="#1D6B52", accent_soft="#D3E9DF", grey="#A8B1AB", info="#2C5A86", info_soft="#D9E5F1",
         warn="#9A6414", warn_soft="#F4E6C8", bad="#AE4237", bad_soft="#F4D9D4", tan="#B9905A", surface2="#F3F5F1")

BASE_CSS = f"""
*{{box-sizing:border-box}} html,body{{margin:0;background:#fff}}
body{{font-family:"Malgun Gothic","Apple SD Gothic Neo",sans-serif;color:{C['ink']};-webkit-font-smoothing:antialiased;word-break:keep-all}}
.card{{width:880px;margin:14px;padding:26px 30px 24px;border:1px solid {C['rule']};border-radius:14px;background:#fff}}
h1{{font-size:23px;margin:0 0 7px;font-weight:700;letter-spacing:-0.2px}}
.sub{{font-size:16px;color:{C['muted']};margin:0 0 20px;line-height:1.5}}
.note{{font-size:15px;color:{C['muted']};margin-top:16px;line-height:1.55}}
.legend{{display:flex;flex-wrap:wrap;gap:6px 20px;font-size:15.5px;color:{C['ink2']};margin:0 0 14px}}
.legend span{{white-space:nowrap}} .legend i{{display:inline-block;width:14px;height:14px;border-radius:3px;margin-right:6px;vertical-align:-1px}}
.row{{display:grid;grid-template-columns:var(--lab,190px) 1fr var(--val,110px);align-items:center;gap:12px;margin:11px 0}}
.lab{{font-size:16.5px;color:{C['ink2']};text-align:right;line-height:1.25}}
.lab small{{display:block;font-size:14px;color:{C['muted']}}}
.track{{position:relative;height:28px;background:{C['track']};border-radius:6px;overflow:visible}}
.bar{{position:absolute;left:0;top:0;height:100%;border-radius:6px}}
.val{{font-size:17px;font-weight:700;color:{C['ink']};white-space:nowrap}}
.val small{{font-weight:400;color:{C['muted']};font-size:14.5px}}
.hl{{color:{C['accent']}}}
"""


def page(name, body, extra_css=""):
    html = f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{BASE_CSS}{extra_css}</style></head><body>{body}</body></html>'
    (OUT / f"{name}.html").write_text(html, encoding="utf-8")


def card(title, sub, inner, note=""):
    n = f'<div class="note">{note}</div>' if note else ""
    s = f'<p class="sub">{sub}</p>' if sub else ""
    return f'<div class="card"><h1>{title}</h1>{s}{inner}{n}</div>'


def hbar_rows(rows, vmax, color, lab_w=190, val_w=120, vmin=0.0):
    """rows: (label_html, value, value_text, color_or_None)"""
    out = []
    for lab, v, vt, col in rows:
        w = max(0.0, (v - vmin) / (vmax - vmin)) * 100
        out.append(f'<div class="row" style="--lab:{lab_w}px;--val:{val_w}px"><div class="lab">{lab}</div>'
                   f'<div class="track"><div class="bar" style="width:{w:.2f}%;background:{col or color}"></div></div>'
                   f'<div class="val">{vt}</div></div>')
    return "".join(out)


def legend(items):
    return '<div class="legend">' + "".join(f'<span><i style="background:{c}"></i>{t}</span>' for t, c in items) + "</div>"



def mk(i, c):
    return (f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')


# ================================================================ 케이스북 그림 큰 글씨판 (cb_*)
NODE_FS = {"det": (C["accent_soft"], C["accent"]), "llm": (C["info_soft"], C["info"]), "neutral": ("#fff", "#A9B4AC"),
           "ask": (C["warn_soft"], C["warn"]), "bad": (C["bad_soft"], C["bad"]), "soft": (C["surface2"], C["rule"]),
           "wacc": ("#fff", C["accent"])}
LC = {"ink": (C["ink2"], "m_ink"), "acc": (C["accent"], "m_acc"), "info": (C["info"], "m_info"), "warn": (C["warn"], "m_warn")}


def nd(x, y, w, h, title, lines=(), kind="neutral", fs=15, ts=17, bw=1.5, align="center", just="center", tcol=None, weight=700):
    fill, stroke = NODE_FS[kind]
    tc = tcol or {"det": C["accent"], "llm": C["info"], "wacc": C["accent"]}.get(kind, C["ink"])
    li = "".join(f'<div style="font-size:{fs}px;color:{C["ink2"]};margin-top:3px;line-height:1.38">{l}</div>' for l in lines)
    t = f'<div style="font-size:{ts}px;font-weight:{weight};color:{tc};line-height:1.3">{title}</div>' if title else ""
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;background:{fill};'
            f'border:{bw}px solid {stroke};border-radius:11px;padding:8px 10px;display:flex;flex-direction:column;'
            f'justify-content:{just};text-align:{align}">{t}{li}</div>')


def zone(x, y, w, h, title, sub, kind):
    fill, stroke = {"det": ("#EEF6F2", C["accent"]), "llm": ("#EEF3F9", C["info"])}[kind]
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;background:{fill};'
            f'border:1.8px dashed {stroke};border-radius:14px;padding:12px 16px"><div style="font-size:17px;font-weight:700;color:{stroke}">{title}</div>'
            f'<div style="font-size:14.5px;color:{C["ink2"]};margin-top:2px">{sub}</div></div>')


def ln(x1, y1, x2, y2, col="ink", w=2, dash=False, start=False, end=True):
    c, m = LC[col]
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{" stroke-dasharray=\"6 5\"" if dash else ""}'
            f'{f" marker-start=\"url(#{m})\"" if start else ""}{f" marker-end=\"url(#{m})\"" if end else ""}/>')


def pth(d, col="ink", w=2, dash=False, end=True):
    c, m = LC[col]
    return (f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}"{" stroke-dasharray=\"6 5\"" if dash else ""}'
            f'{f" marker-end=\"url(#{m})\"" if end else ""}/>')


def tx(x, y, s, col=None, size=15, anchor="middle", bold=False, halo=None):
    halo = (col != "#fff") if halo is None else halo
    h = ' stroke="#fff" stroke-width="5" stroke-linejoin="round" paint-order="stroke"' if halo else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{col or C["ink2"]}" text-anchor="{anchor}" '
            f'font-weight="{700 if bold else 400}" font-family="Malgun Gothic"{h}>{s}</text>')


def canvas(W, H, nodes, svg):
    defs = mk("m_ink", C["ink2"]) + mk("m_acc", C["accent"]) + mk("m_info", C["info"]) + mk("m_warn", C["warn"])
    return (f'<div style="position:relative;width:{W}px;height:{H}px;margin:6px auto 0">{"".join(nodes)}'
            f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0;overflow:visible"><defs>{defs}</defs>{"".join(svg)}</svg></div>')


def stacked(rows, legend_items, total_max, lab_w=170, val_w=130, h=32):
    out = legend(legend_items)
    for lab, vals, vt in rows:
        tot = sum(vals)
        segs = "".join(
            f'<div style="width:{v / tot * 100:.3f}%;background:{c};color:#fff;font-size:15px;font-weight:700;display:flex;'
            f'align-items:center;justify-content:center">{v if v / total_max >= 0.06 else ""}</div>'
            for v, (_, c) in zip(vals, legend_items) if v)
        track = 820 - lab_w - val_w - 24
        out += (f'<div class="row" style="--lab:{lab_w}px;--val:0px;margin:14px 0"><div class="lab">{lab}</div>'
                f'<div style="display:flex;align-items:center;gap:12px"><div style="display:flex;flex:none;height:{h}px;width:{tot / total_max * track:.1f}px;'
                f'border-radius:6px;overflow:hidden">{segs}</div><div class="val" style="font-weight:400;color:{C["ink2"]}">{vt}</div></div><div></div></div>')
    return out


