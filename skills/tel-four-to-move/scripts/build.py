#!/usr/bin/env python3
"""Build the Four to Move wall tracker HTML (one A4 portrait page per matter).

Usage: python3 build.py matters.json out.html
See ../examples/example.json for the input shape.
"""
import base64
import datetime as dt
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
C = dict(purple="#4B2A7B", blue="#2764F0", green="#08A54B", orange="#FF4A14",
         pink="#FF62B6", yellow="#FFD21F", cream="#F6F1E9", ink="#1C1530")
# Page colour order and the text colour that reads on it.
MAINS = [("blue", "#fff"), ("orange", "#fff"), ("green", "#fff"), ("pink", C["ink"])]
# Hero band: 7 x 2 grid. (col, row, colspan, rowspan, kind, colour); kind n = number circle.
LAYOUTS = [
    [(1,1,2,2,"n","purple"),(3,1,1,2,"v","blue"),(4,1,1,1,"c","green"),(4,2,1,1,"c","orange"),(5,1,2,1,"h","blue"),(7,1,1,1,"c","orange"),(5,2,1,1,"c","pink"),(6,2,2,1,"h","yellow")],
    [(1,1,1,1,"c","green"),(2,1,2,1,"h","orange"),(4,1,1,2,"v","blue"),(5,1,1,1,"c","yellow"),(6,1,2,2,"n","purple"),(1,2,2,1,"h","pink"),(3,2,1,1,"c","orange"),(5,2,1,1,"c","orange")],
    [(1,1,1,2,"v","green"),(2,1,1,1,"c","orange"),(2,2,1,1,"c","blue"),(3,1,2,2,"n","purple"),(5,1,2,1,"h","green"),(7,1,1,2,"v","pink"),(5,2,1,1,"c","yellow"),(6,2,1,1,"c","green")],
    [(1,1,2,1,"h","pink"),(3,1,1,1,"c","blue"),(1,2,1,1,"c","yellow"),(2,2,2,1,"h","orange"),(4,1,1,2,"v","pink"),(5,1,2,2,"n","purple"),(7,1,1,1,"c","green"),(7,2,1,1,"c","pink")],
]

WORDS = {1: "one", 2: "two", 3: "three", 4: "four"}

CSS = f"""
@page {{ size:A4 portrait; margin:0; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family:'Poppins', Arial, sans-serif; color:{C['ink']}; background:#fff; }}
.page {{ width:210mm; height:297mm; padding:9mm; display:flex; flex-direction:column; gap:5mm; page-break-after:always; overflow:hidden; background:{C['cream']}; }}
.page:last-child {{ page-break-after:auto; }}
.top {{ display:flex; justify-content:space-between; font-size:8pt; font-weight:600; letter-spacing:.18em; text-transform:uppercase; }}
.shapes {{ display:grid; grid-template-columns:repeat(7,1fr); grid-template-rows:repeat(2,27.4mm); }}
.s {{ border-radius:999px; }}
.s.c {{ aspect-ratio:1; height:100%; justify-self:center; }}
.s.n {{ aspect-ratio:1; height:100%; justify-self:center; display:grid; place-items:center; color:#fff; font-weight:800; font-size:78pt; line-height:1; padding-top:4mm; }}
.name {{ font-weight:800; font-size:38pt; line-height:1.05; letter-spacing:-.02em; margin-top:1mm; }}
.chips {{ display:flex; gap:2.5mm; align-items:center; }}
.chip {{ border-radius:999px; padding:1.6mm 5mm 1.2mm; font-size:11pt; font-weight:600; }}
.chip.no {{ background:{C['ink']}; color:#fff; }}
.lab {{ font-size:7.8pt; font-weight:600; letter-spacing:.16em; text-transform:uppercase; margin-bottom:.8mm; }}
.first {{ border-radius:9mm; padding:5mm 8mm 4mm; }}
.first p {{ font-size:14.5pt; font-weight:600; line-height:1.28; }}
.first .ln {{ border-bottom:.4mm solid currentColor; opacity:.55; height:8mm; }}
.todo {{ display:flex; align-items:center; gap:4mm; height:10.6mm; border-bottom:.35mm solid #D9D0C3; font-size:11.5pt; }}
.ring {{ flex:none; width:7mm; height:7mm; border-radius:50%; border:.8mm solid; }}
.ln {{ border-bottom:.35mm solid #BDB2A3; height:9mm; }}
.grid3 {{ display:grid; grid-template-columns:1fr 1.3fr .8fr; gap:5mm; }}
.filled {{ font-size:12pt; font-weight:600; display:flex; align-items:flex-end; padding-bottom:1mm; }}
.bottom {{ display:flex; justify-content:space-between; align-items:flex-end; margin-top:auto; background:#fff; border-radius:9mm; padding:4mm 6mm; }}
.days, .rag {{ display:flex; gap:2.6mm; }}
.day {{ width:14mm; height:14mm; border-radius:50%; border:.8mm solid; display:grid; place-items:center; font-weight:800; font-size:12pt; }}
.dot {{ width:11mm; height:11mm; border-radius:50%; display:grid; place-items:center; font-weight:800; font-size:9pt; color:#fff; }}
.foot {{ display:flex; justify-content:space-between; font-size:7pt; opacity:.65; }}
"""


def esc(s):
    return html.escape(s or "")


def line(value):
    return f'<div class="ln filled">{esc(value)}</div>' if value else '<div class="ln"></div>'


def page(i, total, m, week_label, rule_time):
    main, on = MAINS[i % len(MAINS)]
    col = C[main]
    n = i + 1
    shapes = "".join(
        f'<div class="s {k}" style="grid-column:{c}/span {cs};grid-row:{r}/span {rs};background:{C[clr]}">{n if k == "n" else ""}</div>'
        for c, r, cs, rs, k, clr in LAYOUTS[i % len(LAYOUTS)])
    steps = (m.get("next_moves", []) + [""] * 4)[:4]
    todos = "".join(f'<div class="todo"><span class="ring" style="border-color:{col}"></span><span>{esc(t)}</span></div>' for t in steps)
    days = "".join(f'<div class="day" style="border-color:{col};color:{col}">{d}</div>' for d in "MTWTF")
    done = (m.get("done_means", []) + ["", ""])[:2] if isinstance(m.get("done_means"), list) else [m.get("done_means", ""), ""]
    chip_no = f'<span class="chip no">Matter {esc(m["matter_no"])}</span>' if m.get("matter_no") else ""
    return f"""<section class="page">
<div class="top"><span>Four to move &nbsp;·&nbsp; {week_label}</span><span>{n} / {total}</span></div>
<div class="shapes">{shapes}</div>
<div class="name">{esc(m["name"])}</div>
<div class="chips"><span class="chip" style="background:{col};color:{on}">{esc(m.get("type", "Matter"))}</span>{chip_no}</div>
<div class="first" style="background:{col};color:{on}"><div class="lab">Before {esc(rule_time)} Monday</div><p>{esc(m["first_move"])}</p><div class="ln"></div></div>
<div><div class="lab">Next moves</div>{todos}</div>
<div><div class="lab">Done this week means</div>{line(done[0])}{line(done[1])}</div>
<div class="grid3"><div><div class="lab">Hard deadline</div>{line(m.get("deadline"))}</div><div><div class="lab">Waiting on</div>{line(m.get("waiting_on"))}</div><div><div class="lab">Since</div>{line(m.get("since"))}</div></div>
<div class="bottom"><div><div class="lab">Colour in the day it moves</div><div class="days">{days}</div></div>
<div><div class="lab" style="text-align:right">Friday: circle one</div><div class="rag"><span class="dot" style="background:#E23B2E">R</span><span class="dot" style="background:#F2A20C">A</span><span class="dot" style="background:#08A54B">G</span></div></div></div>
<div class="foot"><span>Nothing new starts until all {WORDS.get(total, total)} have moved.</span><span>Tracey Edmonds Law · Internal · Confidential</span></div>
</section>"""


def main():
    data = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2])
    monday = dt.date.fromisoformat(data["week_start"])
    if monday.weekday() != 0:
        sys.exit(f"week_start {monday} is not a Monday")
    week_label = f"week of {monday.day} {monday.strftime('%B %Y')}"
    matters = data["matters"]
    fonts = "".join(
        f"@font-face{{font-family:'Poppins';font-weight:{w};src:url(data:font/woff2;base64,"
        f"{base64.b64encode((ROOT / 'assets/fonts' / f'p{w}.woff2').read_bytes()).decode()}) format('woff2');}}"
        for w in (400, 600, 800))
    body = "".join(page(i, len(matters), m, week_label, data.get("rule_time", "1pm")) for i, m in enumerate(matters))
    out.write_text(f'<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><title>Four to Move</title>'
                   f'<style>{fonts}{CSS}</style></head><body>{body}</body></html>')
    print(out)


if __name__ == "__main__":
    main()
