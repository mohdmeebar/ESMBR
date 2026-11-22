"""Builds the Arab Dalla reel (1080x1920, ~60 s) in the look of the shop itself:
ivory plaster facade with carved arches and rosettes, walnut shelving with warm
LED strips inside. Run from this folder: python3 -I build.py ."""
import json, math, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
BRANDS = json.load(open(os.path.join(OUT, "assets/brands/brands.json")))
PROD_DIR = os.path.join(OUT, "assets/products")
os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)
for f in os.listdir(os.path.join(OUT, "compositions")):
    os.remove(os.path.join(OUT, "compositions", f))

CX = 540          # the frame's true centre
PHONE = "+973 33337811"


def products(key):
    return sorted(f for f in os.listdir(PROD_DIR) if f.startswith(key + "-"))


HEAD = """  <style>
    @font-face { font-family: "HF Amiri"; font-weight: 700; src: url("assets/fonts/amiri-700.woff2") format("woff2"); }
    @font-face { font-family: "HF Cairo"; font-weight: 400; src: url("assets/fonts/cairo-400.woff2") format("woff2"); }
    @font-face { font-family: "HF Cairo"; font-weight: 700; src: url("assets/fonts/cairo-700.woff2") format("woff2"); }
    @font-face { font-family: "HF Cairo"; font-weight: 800; src: url("assets/fonts/cairo-800.woff2") format("woff2"); }
    #root { position: absolute; inset: 0; direction: rtl; font-family: "HF Cairo", sans-serif; overflow: hidden; }
    .w { display: inline-block; }
    .blk { position: absolute; left: 156px; width: 768px; text-align: center; }
    .plaster { position: absolute; inset: 0; background-color: #efe6d4;
      background-image:
        radial-gradient(70% 45% at 30% 18%, rgba(255,255,255,0.6), rgba(255,255,255,0) 70%),
        radial-gradient(55% 40% at 78% 72%, rgba(170,145,110,0.16), rgba(170,145,110,0) 70%),
        radial-gradient(130% 85% at 50% 50%, rgba(0,0,0,0) 55%, rgba(95,62,30,0.22) 100%); }
    .walnut { position: absolute; inset: 0; background-color: #5a3622;
      background-image:
        linear-gradient(90deg, rgba(0,0,0,0.38), rgba(0,0,0,0) 16%, rgba(0,0,0,0) 84%, rgba(0,0,0,0.38)),
        repeating-linear-gradient(90deg, rgba(255,215,170,0.035) 0 3px, rgba(0,0,0,0) 3px 11px),
        repeating-linear-gradient(90deg, rgba(0,0,0,0.08) 0 1px, rgba(0,0,0,0) 1px 37px),
        linear-gradient(180deg, #67402a, #4a2c1c); }
    .seam { position: absolute; top: 0; width: 2px; height: 1920px; background: rgba(0,0,0,0.32); box-shadow: 1px 0 0 rgba(255,220,180,0.08); }
    .board { position: absolute; left: 0; width: 1080px; height: 24px;
      background: linear-gradient(180deg, #8d5e3d 0%, #6c432a 30%, #4b2d1c 100%); box-shadow: 0 14px 22px rgba(0,0,0,0.45); }
    .led { position: absolute; left: 30px; width: 1020px; height: 3px; border-radius: 2px; background: #ffe7bb; box-shadow: 0 0 14px 4px rgba(255,214,150,0.75); }
    .glow { position: absolute; left: 0; width: 1080px; background: linear-gradient(180deg, rgba(255,208,140,0.34), rgba(255,208,140,0.07) 70%, rgba(255,208,140,0)); }
    .card { position: absolute; object-fit: cover; border-radius: 14px; border: 5px solid #f7f0e3; box-shadow: 0 18px 26px rgba(0,0,0,0.5); }
    .tag { position: absolute; padding: 2px 16px; border-radius: 8px; background: #f7f0e3; color: #3a2416; text-align: center;
      font-weight: 800; font-size: 28px; line-height: 40px; width: max-content; box-shadow: 0 6px 12px rgba(0,0,0,0.35); }
    .pill { position: absolute; height: 84px; border-radius: 42px; display: flex; align-items: center; justify-content: center; gap: 18px; direction: ltr; }
    .pill span { font-weight: 800; font-size: 44px; line-height: 1; }
    .goldtxt { background: linear-gradient(100deg, #6b4314 0%, #a8732a 30%, #e2b865 50%, #a8732a 70%, #6b4314 100%);
      background-size: 300% 100%; background-position: 0% 50%; -webkit-background-clip: text; background-clip: text; color: transparent; }
    .goldlt { background: linear-gradient(100deg, #c9953f 0%, #f3d690 35%, #fff4d6 50%, #f3d690 65%, #c9953f 100%);
      background-size: 300% 100%; background-position: 0% 50%; -webkit-background-clip: text; background-clip: text; color: transparent; }
  </style>
"""

HELP = """
      const tl = gsap.timeline({ paused: true });
      const wordsIn = (sel, at, gap) => tl.fromTo(sel + " .w", { opacity: 0, filter: "blur(10px)", y: 30 }, { opacity: 1, filter: "blur(0px)", y: 0, duration: 0.35, ease: "power4.out", stagger: gap || 0.1 }, at);
      const lineIn = (sel, at) => tl.fromTo(sel, { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.35, ease: "power3.out" }, at);
      const out = (sel, at, d) => tl.to(sel, { opacity: 0, filter: "blur(10px)", duration: d || 0.25, ease: "power2.in" }, at);
"""

WA = '<svg width="50" height="50" viewBox="0 0 56 56"><circle cx="28" cy="28" r="28" fill="#2f9e57"/><path d="M28 13c-8.3 0-15 6.1-15 13.7 0 3 1.1 5.8 2.9 8.1L14 42l7.6-2.3c1.9.8 4.1 1.3 6.4 1.3 8.3 0 15-6.1 15-13.7S36.3 13 28 13z" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round"/><path d="M22.5 22.5c.6 3.7 3.6 7.6 8 9.4l2.2-2.2 3 1.4-.4 2.6c-6.8.6-13.8-6.4-13.2-13.2l2.6-.4 1.4 3z" fill="#fff"/></svg>'


def pill(pid, top, dark):
    bg, fg, shadow = ("#4a2c1d", "#f6ecd6", "0 14px 30px rgba(74,44,29,0.35)") if dark else ("#f6ecd6", "#2a1c10", "0 14px 30px rgba(0,0,0,0.45)")
    return (f'    <div id="{pid}" class="pill" style="left:{CX - 290}px;top:{top}px;width:580px;background:{bg};box-shadow:{shadow};">'
            f'{WA}<span style="color:{fg};">{PHONE}</span></div>\n')


def rosette(x, y, size, sid):
    """A carved plaster medallion like the shop's facade: relief = shadow stroke + light stroke."""
    petals = "".join(f'<ellipse cx="0" cy="-27" rx="9" ry="20" transform="rotate({k * 30})"/>' for k in range(12))
    body = f'<circle r="60"/><circle r="51"/>{petals}<circle r="11"/>'
    return (f'    <svg id="{sid}" data-layout-ignore style="position:absolute;left:{x - size // 2}px;top:{y - size // 2}px;" width="{size}" height="{size}" viewBox="-66 -66 132 132">'
            f'<g fill="none" stroke="#fbf6ec" stroke-width="3" transform="translate(-1.5,-1.5)">{body}</g>'
            f'<g fill="none" stroke="#c9b28c" stroke-width="3">{body}</g></svg>\n')


def arch(aid, left, top, w, h):
    """A pointed arch in carved relief, drawn with two strokes so it can be 'carved' on screen."""
    def path(i):
        x0, x1, y1, sp = left + i, left + w - i, top + h, top + i * 1.1
        mid = left + w / 2
        return (f"M {x0} {y1} L {x0} {sp + 0.36 * h} Q {x0} {sp + 0.08 * h} {mid} {sp} "
                f"Q {x1} {sp + 0.08 * h} {x1} {sp + 0.36 * h} L {x1} {y1}")
    paths = ""
    for k, i in enumerate((0, 28)):
        d = path(i)
        paths += (f'<path class="{aid}-l" d="{d}" fill="none" stroke="#fbf6ec" stroke-width="5" transform="translate(-2,-2)"/>'
                  f'<path class="{aid}-l" d="{d}" fill="none" stroke="#c4ab84" stroke-width="5"/>')
    return f'    <svg id="{aid}" data-layout-ignore style="position:absolute;left:0;top:0;" width="1080" height="1920">{paths}</svg>\n'


def seams():
    return "".join(f'    <div class="seam" style="left:{x}px;"></div>\n' for x in (270, 540, 810))


def shelves(sid, rows, s, top_board, items, tags=None, gap=24, deco=True):
    """Walnut shelving: rows of product cards standing on boards lit by LED strips.
    rows: card counts per row; items: image paths. Labels hang on the shelf edge under
    their card. With deco, empty lit shelves continue above and below, like the shop wall."""
    html, labels, ids = "", "", []
    pitch = s + 50

    def shelf(y, glow_h, gid=None, dim=False):
        op = ' style="opacity:0.5"' if dim else ""
        g = f' id="{gid}"' if gid else ""
        return (f'    <div class="board" style="top:{y}px;"></div>\n'
                f'    <div class="led" style="top:{y + 24}px;{"opacity:0.55;" if dim else ""}"></div>\n'
                f'    <div{g} class="glow" style="top:{y + 26}px;height:{glow_h}px;{"opacity:0.5;" if dim else ""}"></div>\n')

    if deco and top_board - 230 > 0:
        html += shelf(top_board - 230, 200, dim=True)
    y = top_board
    idx = 0
    for r, k in enumerate(rows):
        html += shelf(y, s + 30, f"{sid}-g{r}")
        y_cards = y + 50
        width = k * s + (k - 1) * gap
        x = CX - width // 2
        for j in range(k):
            cid = f"{sid}-c{idx}"
            html += f'    <img id="{cid}" class="card" src="{items[idx]}" alt="" style="left:{x}px;top:{y_cards}px;width:{s}px;height:{s}px;" />\n'
            ids.append(cid)
            if tags and tags[idx]:
                # a label never runs wider than its card: a long name wraps onto a second line
                labels += f'    <div id="{sid}-t{idx}" class="tag" style="top:{y_cards + s - 4}px;left:{x + s // 2}px;max-width:{s}px;transform:translateX(-50%);">{tags[idx]}</div>\n'
            x += s + gap
            idx += 1
        y = y_cards + s
    html += f'    <div class="board" style="top:{y}px;"></div>\n'
    end = y + 24
    if deco:
        yy = max(y + pitch, 1300)
        while yy < 1900:
            html += shelf(yy, pitch - 30, dim=True)
            yy += pitch
    return html + labels, ids, end


def scene(sid, dur, body, script):
    html = f"""<template>
{HEAD}  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920" data-duration="{dur}">
{body}
  </div>
  <script>
    (function () {{
{HELP}
{script}
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
"""
    open(os.path.join(OUT, "compositions", sid + ".html"), "w").write(html)


PLAN = []

# ---------------- 1. hook: plaster facade, a carved arch, the headline from frame 0 ----------------
D = 3.8
scene("hook", D, f"""
    <div class="plaster"></div>
{rosette(90, 170, 150, "hk-r1")}{rosette(990, 170, 150, "hk-r2")}{rosette(90, 1760, 150, "hk-r3")}{rosette(990, 1760, 150, "hk-r4")}{arch("hk-a", CX - 380, 250, 760, 1150)}    <div id="hk-txt" class="blk" style="top:560px;">
      <div id="hk-l1" class="goldtxt" style="font-family:'HF Amiri',serif;font-weight:700;font-size:250px;line-height:1.2;">جودة</div>
      <div id="hk-l2" style="font-family:'HF Amiri',serif;font-weight:700;font-size:140px;line-height:1.25;color:#4a2c1d;">المنتجات</div>
      <div id="hk-rule" style="width:280px;height:4px;margin:22px auto 0;background:#a8732a;"></div>
      <div id="hk-sub" style="font-weight:700;font-size:36px;line-height:1.5;margin-top:24px;color:#6b4a2e;">من المحلات العربية… إلى طاولة ضيافتك</div>
    </div>
""", """
      tl.fromTo(".hk-a-l", { strokeDasharray: 3200, strokeDashoffset: 3200 }, { strokeDashoffset: 0, duration: 1.4, ease: "power2.inOut" }, 0);
      tl.fromTo("#hk-l1", { backgroundPosition: "0% 50%" }, { backgroundPosition: "100% 50%", duration: 1.6, ease: "sine.inOut" }, 0.2);
      tl.fromTo("#hk-l1", { scale: 1.06 }, { scale: 1, duration: 0.8, ease: "expo.out" }, 0);
      tl.fromTo("#hk-rule", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "expo.out" }, 0.8);
      lineIn("#hk-sub", 1.3);
      tl.to("#hk-txt", { scale: 1.6, opacity: 0, filter: "blur(14px)", duration: 0.4, ease: "power3.in" }, 3.4);
""")
PLAN.append(("hook", D))

# ---------------- 2. the shop sign: the logo on a recessed plaster panel, as on the storefront ----------------
D = 3.4
scene("brand", D, f"""
    <div class="plaster"></div>
{rosette(120, 1600, 130, "br-r1")}{rosette(960, 1600, 130, "br-r2")}    <div id="br-panel" style="position:absolute;left:{CX - 380}px;top:380px;width:760px;height:440px;border-radius:6px;
      background:#f3ebdc;box-shadow: inset 0 0 0 3px #e2d5bd, inset 6px 6px 14px rgba(120,90,55,0.22), inset -4px -4px 10px rgba(255,255,255,0.8);"></div>
    <div id="br-logo" style="position:absolute;left:{CX - 320}px;top:410px;width:640px;height:380px;padding:30px 20px;"><img src="assets/logo-dark.png" alt="" style="display:block;width:600px;height:323px;" /></div>
    <div id="br-t1" class="blk" style="top:900px;font-family:'HF Amiri',serif;font-weight:700;font-size:92px;line-height:1.3;color:#4a2c1d;"><span class="w">متخصصون</span> <span class="w">في</span> <span class="w" style="color:#8a5a1f">الضيافة</span></div>
    <div id="br-t2" class="blk" style="top:1050px;font-weight:700;font-size:40px;line-height:1.5;color:#6b4a2e;">منتجات مختارة من المحلات العربية</div>
""", """
      tl.fromTo("#br-panel", { opacity: 0, scale: 0.96 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, 0.0);
      tl.fromTo("#br-logo", { clipPath: "inset(0% 0% 100% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.9, ease: "power2.inOut" }, 0.2);
      wordsIn("#br-t1", 1.0, 0.12);
      lineIn("#br-t2", 1.5);
      out("#br-t1, #br-t2", 3.05, 0.25);
      tl.to("#br-panel, #br-logo", { y: -380, opacity: 0, duration: 0.4, ease: "power3.in" }, 3.0);
""")
PLAN.append(("brand", D))

# ---------------- 3. the house brand: Deem by Arab Dalla, on the shop's walnut shelves ----------------
DEEM = [("deem-1.jpg", "الدلة الذهبية"), ("deem-2.jpg", "الدلة الفضية"), ("deem-3.jpg", "دلة الضيوف"),
        ("deem-4.jpg", "سخان الحليب"), ("deem-5.jpg", "بريق الكرك"), ("deem-6.jpg", "صانعة القهوة التركية")]
D = 5.8
sh, ids, bottom = shelves("hr", [3, 3], 230, 470, [f"assets/products/{p}" for p, _ in DEEM], [n for _, n in DEEM], gap=34)
js = ""
for i, cid in enumerate(ids):
    t = 0.55 + i * 0.28
    js += f'      tl.fromTo("#{cid}", {{ opacity: 0, y: 50, scale: 0.82, transformOrigin: "50% 100%" }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(1.5)" }}, {t:.2f});\n'
    if DEEM[i][1]:
        js += f'      tl.fromTo("#hr-t{i}", {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, {t + 0.3:.2f});\n'
scene("hero", D, f"""
    <div class="walnut"></div>
{seams()}    <img id="hr-logo" src="assets/deem-cream.png" alt="" style="position:absolute;left:{CX - 105}px;top:296px;width:210px;height:107px;" />
    <div id="hr-by" class="blk" style="top:402px;font-weight:700;font-size:34px;line-height:1.4;color:#f0cf8a;">من دلة العرب</div>
    <div id="hr-stage" data-layout-allow-overlap style="position:absolute;inset:0;">
{sh}    </div>
{pill("hr-pill", 1150, False)}""", f"""
      tl.fromTo("#hr-logo", {{ opacity: 0, scale: 1.25, filter: "blur(12px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.5, ease: "expo.out" }}, 0.05);
      lineIn("#hr-by", 0.3);
      tl.fromTo("#hr-g0, #hr-g1", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power2.out", stagger: 0.15 }}, 0.2);
{js}      lineIn("#hr-pill", 1.2);
      out("#hr-logo, #hr-by, #hr-pill", {D - 0.32:.2f});
      tl.to("#hr-stage", {{ x: -260, opacity: 0, duration: 0.3, ease: "power2.in" }}, {D - 0.32:.2f});
""")
PLAN.append(("hero", D))

# ---------------- 4. brands intro, on the walnut wall ----------------
D = 1.45
scene("brands-intro", D, f"""
    <div class="walnut"></div>
{seams()}    <div id="bi-t" class="blk" style="top:720px;font-family:'HF Amiri',serif;font-weight:700;font-size:120px;line-height:1.3;color:#f6ecd6;"><span class="w">علامات</span> <span class="w" style="color:#f3d98f">عربية</span></div>
    <div id="bi-led" class="led" style="left:{CX - 200}px;width:400px;top:905px;"></div>
    <div id="bi-s" class="blk" style="top:930px;font-weight:700;font-size:46px;line-height:1.4;color:#f0cf8a;">في مكان واحد</div>
""", """
      wordsIn("#bi-t", 0.05, 0.12);
      tl.fromTo("#bi-led", { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "expo.out" }, 0.1);
      lineIn("#bi-s", 0.15);
      tl.to("#bi-t, #bi-s, #bi-led", { y: -120, opacity: 0, filter: "blur(10px)", duration: 0.25, ease: "power3.in" }, 1.2);
""")
PLAN.append(("brands-intro", D))

# ---------------- 5. one shelf wall per brand: logo plaque, products spread on the shelves, the number ----------------
LAYOUT = {1: ([1], 380, 520), 2: ([2], 340, 560), 3: ([2, 1], 255, 480), 4: ([2, 2], 255, 480), 5: ([3, 2], 235, 480)}
for bi, b in enumerate(BRANDS):
    key = b["key"]
    prods = products(key)
    n = len(prods)
    rows, s, top = LAYOUT[n]
    D = round(2.75 + 0.08 * n, 2)
    sid = "b-" + key
    sh, ids, bottom = shelves(sid, rows, s, top, [f"assets/products/{p}" for p in prods])
    js = ""
    for i, cid in enumerate(ids):
        js += f'      tl.fromTo("#{cid}", {{ opacity: 0, y: 50, scale: 0.82, transformOrigin: "50% 100%" }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.48, ease: "back.out(1.5)" }}, {0.35 + i * 0.1:.2f});\n'
    glows = ", ".join(f"#{sid}-g{r}" for r in range(len(rows)))
    plaque_top = top - 170
    scene(sid, D, f"""
    <div class="walnut"></div>
{seams()}    <div id="{sid}-stage" data-layout-allow-overlap style="position:absolute;inset:0;">
{sh}      <img id="{sid}-logo" src="assets/brands/{key}.jpg" alt="" style="position:absolute;left:{CX - 82}px;top:{plaque_top}px;width:164px;height:164px;border-radius:22px;border:5px solid #f7f0e3;box-shadow:0 14px 28px rgba(0,0,0,0.5);" />
    </div>
{pill(sid + "-pill", 1150, False)}""", f"""
      tl.fromTo("#{sid}-stage", {{ x: 240, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, 0);
      tl.fromTo("#{sid}-logo", {{ rotationY: -85, transformPerspective: 1200 }}, {{ rotationY: 0, duration: 0.4, ease: "power3.out" }}, 0.05);
      tl.fromTo("{glows}", {{ opacity: 0.2 }}, {{ opacity: 1, duration: 0.4, ease: "power2.out" }}, 0.15);
{js}      lineIn("#{sid}-pill", 0.5);
      tl.to("#{sid}-stage", {{ x: -240, opacity: 0, duration: 0.28, ease: "power2.in" }}, {D - 0.3:.2f});
      out("#{sid}-pill", {D - 0.3:.2f});
""")
    PLAN.append((sid, D))

# ---------------- 6. the shop's walnut doors open onto every brand ----------------
D = 4.4
wall_items = [f"assets/brands/{b['key']}.jpg" for b in BRANDS]
sh, ids, bottom = shelves("st", [4, 4, 3], 178, 490, wall_items, gap=18, deco=False)
pops = ""
for i, cid in enumerate(ids):
    pops += f'      tl.fromTo("#{cid}", {{ opacity: 0, y: 30, scale: 0.85, transformOrigin: "50% 100%" }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.6)" }}, {0.9 + i * 0.05:.2f});\n'


def door(did, side):
    panels = ""
    for k, (t, h) in enumerate(((140, 520), (720, 520), (1300, 480))):
        panels += (f'<div style="position:absolute;left:70px;top:{t}px;width:400px;height:{h}px;border-radius:10px;'
                   f'box-shadow: inset 0 0 0 8px #3a1f14, inset 0 0 0 12px #7a4a30, inset 6px 8px 18px rgba(0,0,0,0.45);">'
                   f'<div style="position:absolute;left:70px;top:{int(h * 0.12)}px;width:260px;height:{int(h * 0.76)}px;border-radius:50%;'
                   f'box-shadow: inset 0 0 0 6px #3a1f14, inset 0 0 0 10px #7a4a30, inset 4px 6px 12px rgba(0,0,0,0.4);"></div></div>')
    handle_x = 500 if side == "l" else 22
    origin = "0% 50%" if side == "l" else "100% 50%"
    left = 0 if side == "l" else 540
    return (f'      <div id="{did}" style="position:absolute;left:{left}px;top:0;width:540px;height:1920px;transform-origin:{origin};'
            f'background-color:#4a2619;background-image:repeating-linear-gradient(90deg, rgba(255,210,170,0.04) 0 3px, rgba(0,0,0,0) 3px 12px),'
            f'linear-gradient(180deg,#5a2f1e,#3e2015);box-shadow: inset 0 0 0 10px #351a10;">{panels}'
            f'<div style="position:absolute;left:{handle_x}px;top:900px;width:18px;height:120px;border-radius:9px;background:linear-gradient(90deg,#8a6a2a,#e6c77a,#8a6a2a);"></div></div>\n')


scene("store", D, f"""
    <div id="st-wall" style="position:absolute;inset:0;">
      <div class="walnut"></div>
{seams()}{sh}    </div>
    <div id="st-light" data-layout-ignore style="position:absolute;inset:0;background:radial-gradient(60% 45% at 50% 50%, rgba(255,214,150,0.35), rgba(255,214,150,0));"></div>
    <div id="st-t" class="blk" style="top:300px;font-family:'HF Amiri',serif;font-weight:700;font-size:100px;line-height:1.3;color:#f6ecd6;text-shadow:0 4px 20px rgba(0,0,0,0.5);"><span class="w">تحت</span> <span class="w">سقف</span> <span class="w" style="color:#f3d98f">واحد</span></div>
    <div id="st-s" class="blk" style="top:428px;font-weight:700;font-size:38px;line-height:1.4;color:#f0cf8a;">منتجات من أكثر من دولة عربية</div>
    <div id="st-doors" data-layout-ignore style="position:absolute;inset:0;perspective:1800px;">
{door("st-dl", "l")}{door("st-dr", "r")}    </div>
""", pops + """
      tl.fromTo("#st-dl", { rotationY: 0 }, { rotationY: -100, duration: 1.2, ease: "power2.inOut" }, 0.25);
      tl.fromTo("#st-dr", { rotationY: 0 }, { rotationY: 100, duration: 1.2, ease: "power2.inOut" }, 0.25);
      tl.to("#st-doors", { opacity: 0, duration: 0.3, ease: "power1.in" }, 1.2);
      tl.fromTo("#st-light", { opacity: 1 }, { opacity: 0.35, duration: 1.0, ease: "power2.out" }, 0.6);
      tl.fromTo("#st-g0, #st-g1, #st-g2", { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.out", stagger: 0.15 }, 0.7);
      wordsIn("#st-t", 1.3, 0.12);
      lineIn("#st-s", 1.7);
      out("#st-t, #st-s", 4.05);
      tl.to("#st-wall", { scale: 1.25, opacity: 0, filter: "blur(10px)", duration: 0.4, ease: "power3.in" }, 4.0);
""")
PLAN.append(("store", D))

# ---------------- 7. quality: a lit headline on the walnut wall ----------------
D = 3.8
scene("quality", D, f"""
    <div class="walnut"></div>
{seams()}    <div id="ql-spot" data-layout-ignore style="position:absolute;inset:0;background:radial-gradient(55% 32% at 50% 44%, rgba(255,214,150,0.32), rgba(255,214,150,0));"></div>
    <div id="ql-txt" class="blk" style="top:560px;">
      <div id="ql-l1" class="goldlt" style="font-family:'HF Amiri',serif;font-weight:700;font-size:230px;line-height:1.2;">جودة</div>
      <div id="ql-l2" style="font-family:'HF Amiri',serif;font-weight:700;font-size:130px;line-height:1.25;color:#f6ecd6;">المنتجات</div>
      <div id="ql-led" class="led" style="position:relative;left:auto;margin:26px auto 0;width:320px;"></div>
      <div id="ql-sub" style="font-weight:700;font-size:46px;line-height:1.5;margin-top:26px;color:#f0cf8a;">مختارة بعناية لضيافتك</div>
    </div>
""", """
      tl.fromTo("#ql-spot", { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "power2.out" }, 0.0);
      tl.fromTo("#ql-l1", { opacity: 0, scale: 1.35, filter: "blur(14px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.5, ease: "expo.out" }, 0.1);
      tl.fromTo("#ql-l1", { backgroundPosition: "0% 50%" }, { backgroundPosition: "100% 50%", duration: 1.6, ease: "sine.inOut" }, 0.5);
      tl.fromTo("#ql-l2", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }, 0.35);
      tl.fromTo("#ql-led", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "expo.out" }, 0.7);
      lineIn("#ql-sub", 1.0);
      out("#ql-txt", 3.45);
      tl.to("#ql-spot", { opacity: 0, duration: 0.35 }, 3.45);
""")
PLAN.append(("quality", D))

# ---------------- 8. end card: the storefront sign on plaster, and the number ----------------
D = 4.4
scene("end", D, f"""
    <div class="plaster"></div>
{rosette(120, 210, 140, "en-r1")}{rosette(960, 210, 140, "en-r2")}{rosette(120, 1700, 140, "en-r3")}{rosette(960, 1700, 140, "en-r4")}    <div id="en-panel" style="position:absolute;left:{CX - 360}px;top:340px;width:720px;height:420px;border-radius:6px;
      background:#f3ebdc;box-shadow: inset 0 0 0 3px #e2d5bd, inset 6px 6px 14px rgba(120,90,55,0.22), inset -4px -4px 10px rgba(255,255,255,0.8);"></div>
    <div id="en-logo" style="position:absolute;left:{CX - 300}px;top:370px;width:600px;height:360px;padding:30px 20px;"><img src="assets/logo-dark.png" alt="" style="display:block;width:560px;height:301px;" /></div>
    <div id="en-t" class="blk" style="top:820px;font-family:'HF Amiri',serif;font-weight:700;font-size:84px;line-height:1.3;color:#4a2c1d;"><span class="w">جودة</span> <span class="w">تليق</span> <span class="w" style="color:#8a5a1f">بضيافتك</span></div>
    <div id="en-s" class="blk" style="top:960px;font-weight:700;font-size:40px;line-height:1.4;color:#6b4a2e;">للطلب والاستفسار</div>
{pill("en-pill", 1050, True)}""", """
      tl.fromTo("#en-panel", { opacity: 0, scale: 0.96 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, 0.0);
      tl.fromTo("#en-logo", { clipPath: "inset(0% 0% 100% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.9, ease: "power2.inOut" }, 0.15);
      wordsIn("#en-t", 0.7, 0.12);
      lineIn("#en-s", 1.2);
      tl.fromTo("#en-pill", { opacity: 0, y: 40, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(1.6)" }, 1.4);
""")
PLAN.append(("end", D))

# ---------------- index ----------------
t, hosts = 0.0, ""
for sid, du in PLAN:
    hosts += f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{t:.2f}" data-duration="{du}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>\n'
    t += du
TOTAL = round(t, 2)
music = os.path.exists(os.path.join(OUT, "assets/music.mp3"))
audio = f'      <audio id="bgm" src="assets/music.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="0.9" data-fade-in="0.3" data-fade-out="1.8"></audio>\n' if music else ""
open(os.path.join(OUT, "index.html"), "w").write(f"""<!doctype html>
<html lang="ar">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #4a2c1c; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{hosts}{audio}    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("total", TOTAL, "music", music, "scenes", len(PLAN))
