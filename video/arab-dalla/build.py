"""Builds the Arab Dalla reel (1080x1920, 30 s). Run: python3 -I build.py ."""
import json, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
BRANDS = json.load(open(os.path.join(OUT, "assets/brands/brands.json")))
os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)
AR = "٠١٢٣٤٥٦٧٨٩"
ar = lambda n: "".join(AR[int(c)] for c in str(n))

HEAD = """  <style>
    @font-face { font-family: "HF Amiri"; font-weight: 700; src: url("assets/fonts/amiri-700.woff2") format("woff2"); }
    @font-face { font-family: "HF Cairo"; font-weight: 400; src: url("assets/fonts/cairo-400.woff2") format("woff2"); }
    @font-face { font-family: "HF Cairo"; font-weight: 700; src: url("assets/fonts/cairo-700.woff2") format("woff2"); }
    @font-face { font-family: "HF Cairo"; font-weight: 800; src: url("assets/fonts/cairo-800.woff2") format("woff2"); }
    #root { position: absolute; inset: 0; direction: rtl; font-family: "HF Cairo", sans-serif; color: #f6ecd6; overflow: hidden; }
    .w { display: inline-block; }
    .goldtxt { background: linear-gradient(100deg, #b8913a 0%, #f6dd94 35%, #fff4cf 50%, #f6dd94 65%, #b8913a 100%);
      background-size: 300% 100%; background-position: 0% 50%; -webkit-background-clip: text; background-clip: text; color: transparent; }
    .dot { position: absolute; border-radius: 50%; background: #e9c97a; }
    .blk { position: absolute; left: 120px; width: 768px; text-align: center; }
  </style>
"""

HELP = """
      const tl = gsap.timeline({ paused: true });
      const wordsIn = (sel, at, gap) => tl.fromTo(sel + " .w", { opacity: 0, filter: "blur(10px)", y: 30 }, { opacity: 1, filter: "blur(0px)", y: 0, duration: 0.35, ease: "power4.out", stagger: gap || 0.1 }, at);
      const lineIn = (sel, at) => tl.fromTo(sel, { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.35, ease: "power3.out" }, at);
      const out = (sel, at, d) => tl.to(sel, { opacity: 0, filter: "blur(10px)", duration: d || 0.25, ease: "power2.in" }, at);
"""


def mulberry32(a):
    def r():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = a
        t = ((t ^ (t >> 15)) * (1 | t)) & 0xFFFFFFFF
        t = (t + (((t ^ (t >> 7)) * (61 | t)) & 0xFFFFFFFF) ^ t) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return r


def dust(prefix, n, seed, dur):
    """Gold dust that drifts upward; markup + finite tweens (a pure function of time)."""
    r = mulberry32(seed)
    html, js = "", ""
    for i in range(n):
        x, y, s, o = r() * 1080, r() * 1920, 3 + r() * 6, 0.25 + r() * 0.5
        dy, dx = 80 + r() * 160, (r() - 0.5) * 60
        html += f'    <div id="{prefix}-d{i}" class="dot" style="left:{x:.0f}px;top:{y:.0f}px;width:{s:.1f}px;height:{s:.1f}px;opacity:{o:.2f};"></div>\n'
        js += f'      tl.fromTo("#{prefix}-d{i}", {{ x: 0, y: 0 }}, {{ x: {dx:.0f}, y: {-dy:.0f}, duration: {dur}, ease: "none" }}, 0);\n'
    return html, js


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


BEAT = 0.6  # 100 BPM grid

# ---------------- 1. hook: the headline is on screen from frame 0 ----------------
d_html, d_js = dust("hk", 36, 11, 4.2)
scene("hook", 4.2, d_html + """
    <div id="hk-glow" data-layout-ignore style="position:absolute;left:-160px;top:420px;width:1400px;height:1000px;background:radial-gradient(closest-side, rgba(212,175,90,0.28), rgba(212,175,90,0));"></div>
    <div id="hk-txt" class="blk" style="top:520px;">
      <div id="hk-l1" class="goldtxt" style="font-family:'HF Amiri',serif;font-weight:700;font-size:270px;line-height:1.2;">جودة</div>
      <div id="hk-l2" style="font-family:'HF Amiri',serif;font-weight:700;font-size:150px;line-height:1.25;color:#f6ecd6;">المنتجات</div>
      <div id="hk-rule" style="width:300px;height:4px;margin:22px auto 0;background:#d4af5a;"></div>
      <div id="hk-sub" style="font-weight:700;font-size:40px;line-height:1.5;margin-top:24px;color:#e9c97a;">من محلات الخليج… إلى ضيافتك</div>
    </div>
""", d_js + """
      tl.fromTo("#hk-l1", { backgroundPosition: "0% 50%" }, { backgroundPosition: "100% 50%", duration: 1.6, ease: "sine.inOut" }, 0.2);
      tl.fromTo("#hk-l1", { scale: 1.06 }, { scale: 1, duration: 0.8, ease: "expo.out" }, 0);
      tl.fromTo("#hk-rule", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "expo.out" }, 0.9);
      lineIn("#hk-sub", 1.5);
      tl.to("#hk-txt", { scale: 2.3, opacity: 0, filter: "blur(14px)", duration: 0.4, ease: "power3.in" }, 3.8);
""")

# ---------------- 2. the shop: Arab Dalla ----------------
d_html, d_js = dust("br", 30, 23, 4.2)
scene("brand", 4.2, d_html + """
    <div id="br-glow" data-layout-ignore style="position:absolute;left:-200px;top:300px;width:1400px;height:900px;background:radial-gradient(closest-side, rgba(212,175,90,0.25), rgba(212,175,90,0));"></div>
    <div id="br-logo" style="position:absolute;left:64px;top:420px;width:880px;height:529px;padding:60px;"><img src="assets/logo-gold.png" alt="" style="display:block;width:760px;height:409px;filter:drop-shadow(0 0 26px rgba(233,201,122,0.35));" /></div>
    <div id="br-t1" class="blk" style="top:960px;font-family:'HF Amiri',serif;font-weight:700;font-size:92px;line-height:1.3;color:#f6ecd6;"><span class="w">متخصصون</span> <span class="w">في</span> <span class="w" style="color:#e9c97a">الضيافة</span></div>
    <div id="br-t2" class="blk" style="top:1110px;font-weight:700;font-size:42px;line-height:1.5;color:#e9c97a;">منتجات مختارة من محلات الخليج</div>
""", d_js + """
      tl.fromTo("#br-logo", { clipPath: "inset(0% 0% 100% 0%)", scale: 0.94, opacity: 1 }, { clipPath: "inset(0% 0% 0% 0%)", scale: 1, duration: 1.1, ease: "power2.inOut" }, 0.1);
      tl.fromTo("#br-glow", { opacity: 0 }, { opacity: 1, duration: 1.0, ease: "power2.out" }, 0.4);
      wordsIn("#br-t1", 1.3, 0.12);
      lineIn("#br-t2", 2.0);
      out("#br-t1, #br-t2", 3.85, 0.25);
      tl.to("#br-logo", { y: -420, scale: 0.5, opacity: 0, duration: 0.4, ease: "power3.in" }, 3.8);
""")

# ---------------- 3. brands, one per beat, with a colour flood ----------------
cards, js = "", ""
n = len(BRANDS)
for i, b in enumerate(BRANDS):
    cards += f'    <img id="fl-c{i}" src="assets/brands/{b["key"]}.jpg" alt="" style="position:absolute;left:224px;top:560px;width:560px;height:560px;border-radius:36px;box-shadow:0 30px 70px rgba(0,0,0,0.45);opacity:0;" />\n'
    t = 0.6 + i * BEAT
    js += f'      tl.set("#fl-bg", {{ backgroundColor: "{b["flood"]}" }}, {t:.2f});\n'
    js += f'      tl.fromTo("#fl-c{i}", {{ opacity: 0, rotationY: -80, scale: 0.82, transformPerspective: 1400 }}, {{ opacity: 1, rotationY: 0, scale: 1, duration: 0.32, ease: "power3.out" }}, {t:.2f});\n'
    js += f'      tl.set("#fl-n", {{ textContent: "{ar(i + 1)} / {ar(n)}" }}, {t:.2f});\n'
    if i < n - 1:
        js += f'      tl.to("#fl-c{i}", {{ rotationY: 80, opacity: 0, scale: 0.9, duration: 0.14, ease: "power2.in" }}, {t + BEAT - 0.14:.2f});\n'
fl_dur = round(0.6 + n * BEAT + 0.6, 2)
scene("flash", fl_dur, f"""
    <div id="fl-bg" data-layout-ignore style="position:absolute;inset:0;background-color:#1a120b;"></div>
    <div id="fl-k" class="blk" style="top:330px;font-family:'HF Amiri',serif;font-weight:700;font-size:84px;line-height:1.3;color:#f6ecd6;text-shadow:0 4px 24px rgba(0,0,0,0.5);"><span class="w">علامات</span> <span class="w" style="color:#ffffff">خليجية</span></div>
    <div id="fl-k2" class="blk" style="top:450px;font-weight:700;font-size:40px;line-height:1.4;color:#ffffff;text-shadow:0 3px 18px rgba(0,0,0,0.5);">في مكان واحد</div>
{cards}    <div id="fl-n" class="blk" style="top:1150px;font-weight:700;font-size:36px;line-height:1.4;color:#f6ecd6;direction:ltr;">١ / {ar(n)}</div>
""", f"""
      tl.fromTo("#fl-bg", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 0);
      wordsIn("#fl-k", 0.05, 0.12);
      lineIn("#fl-k2", 0.3);
      lineIn("#fl-n", 0.6);
{js}      out("#fl-k, #fl-k2, #fl-n", {fl_dur - 0.35:.2f});
      tl.to("#fl-c{n - 1}", {{ scale: 0.35, opacity: 0, y: -40, duration: 0.35, ease: "power3.in" }}, {fl_dur - 0.38:.2f});
""")

# ---------------- 4. the 3D ring of every brand ----------------
R, CW = 520, 300
faces = ""
for i, b in enumerate(BRANDS):
    ang = i * 360 / n
    faces += f'        <img src="assets/brands/{b["key"]}.jpg" alt="" style="position:absolute;left:{-CW // 2}px;top:{-CW // 2}px;width:{CW}px;height:{CW}px;border-radius:26px;backface-visibility:hidden;box-shadow:0 20px 40px rgba(0,0,0,0.4);transform:rotateY({ang:.2f}deg) translateZ({R}px);" />\n'
d_html, d_js = dust("rg", 24, 37, 4.8)
scene("ring", 4.8, d_html + f"""
    <div id="rg-t" class="blk" style="top:330px;font-family:'HF Amiri',serif;font-weight:700;font-size:96px;line-height:1.3;color:#f6ecd6;"><span class="w">تحت</span> <span class="w">سقف</span> <span class="w" style="color:#f3d98f">واحد</span></div>
    <div id="rg-s" class="blk" style="top:470px;font-weight:700;font-size:42px;line-height:1.4;color:#e9c97a;">منتجات من أكثر من دولة خليجية</div>
    <div id="rg-stage" data-layout-allow-overflow data-layout-ignore style="position:absolute;left:0;top:0;width:1080px;height:1920px;perspective:1700px;perspective-origin:504px 960px;">
      <div id="rg-ring" style="position:absolute;left:504px;top:960px;width:0;height:0;transform-style:preserve-3d;">
{faces}      </div>
    </div>
""", d_js + """
      wordsIn("#rg-t", 0.05, 0.1);
      lineIn("#rg-s", 0.45);
      tl.fromTo("#rg-ring", { rotationX: -6, rotationY: 40, scale: 0.55, opacity: 0 }, { rotationX: -6, rotationY: -20, scale: 1, opacity: 1, duration: 1.0, ease: "power3.out" }, 0.0);
      tl.to("#rg-ring", { rotationY: -300, duration: 3.4, ease: "none" }, 1.0);
      out("#rg-t, #rg-s", 4.45);
      tl.to("#rg-stage", { scale: 1.7, opacity: 0, filter: "blur(12px)", duration: 0.4, ease: "power3.in" }, 4.4);
""")

# ---------------- 5. quality: the wall of brands + the headline ----------------
tiles = ""
order = [b["key"] for b in BRANDS]
order.insert(4, "__dalla")
for i, key in enumerate(order[:12]):
    c, r = i % 3, i // 3
    x, y = 30 + c * 324, 330 + r * 324
    if key == "__dalla":
        tiles += f'    <div id="ql-t{i}" style="position:absolute;left:{x}px;top:{y}px;width:300px;height:300px;border-radius:28px;background:#2a1c10;border:2px solid #b8913a;"><img src="assets/logo-gold.png" alt="" style="position:absolute;left:20px;top:96px;width:260px;height:140px;" /></div>\n'
    else:
        tiles += f'    <img id="ql-t{i}" src="assets/brands/{key}.jpg" alt="" style="position:absolute;left:{x}px;top:{y}px;width:300px;height:300px;border-radius:28px;" />\n'
scene("quality", 4.8, f"""
    <div id="ql-wall" data-layout-ignore style="position:absolute;inset:0;">
{tiles}    </div>
    <div id="ql-dim" data-layout-ignore style="position:absolute;inset:0;background:radial-gradient(closest-side at 50% 45%, rgba(18,12,7,0.92), rgba(18,12,7,0.72));"></div>
    <div id="ql-txt" class="blk" style="top:560px;">
      <div id="ql-l1" class="goldtxt" style="font-family:'HF Amiri',serif;font-weight:700;font-size:230px;line-height:1.2;">جودة</div>
      <div id="ql-l2" style="font-family:'HF Amiri',serif;font-weight:700;font-size:130px;line-height:1.25;color:#f6ecd6;">المنتجات</div>
      <div id="ql-rule" style="width:300px;height:4px;margin:22px auto 0;background:#d4af5a;"></div>
      <div id="ql-sub" style="font-weight:700;font-size:46px;line-height:1.5;margin-top:22px;color:#e9c97a;">مختارة بعناية لضيافتك</div>
    </div>
""", """
      for (let i = 0; i < 12; i++) {
        const c = i % 3, r = Math.floor(i / 3), dist = Math.abs(c - 1) + Math.abs(r - 1.5);
        tl.fromTo("#ql-t" + i, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.6)" }, 0.05 + dist * 0.12);
      }
      tl.fromTo("#ql-dim", { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power2.out" }, 0.9);
      tl.fromTo("#ql-l1", { opacity: 0, scale: 1.4, filter: "blur(14px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.5, ease: "expo.out" }, 1.1);
      tl.fromTo("#ql-l1", { backgroundPosition: "0% 50%" }, { backgroundPosition: "100% 50%", duration: 1.6, ease: "sine.inOut" }, 1.5);
      tl.fromTo("#ql-l2", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }, 1.35);
      tl.fromTo("#ql-rule", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "expo.out" }, 1.7);
      lineIn("#ql-sub", 2.0);
      out("#ql-txt", 4.45);
      tl.to("#ql-wall", { scale: 1.15, opacity: 0, duration: 0.4, ease: "power2.in" }, 4.4);
""")

# ---------------- 6. end card ----------------
d_html, d_js = dust("en", 30, 51, 4.8)
CHAT = '<svg width="56" height="56" viewBox="0 0 56 56"><circle cx="28" cy="28" r="28" fill="#2f9e57"/><path d="M28 13c-8.3 0-15 6.1-15 13.7 0 3 1.1 5.8 2.9 8.1L14 42l7.6-2.3c1.9.8 4.1 1.3 6.4 1.3 8.3 0 15-6.1 15-13.7S36.3 13 28 13z" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round"/><path d="M22.5 22.5c.6 3.7 3.6 7.6 8 9.4l2.2-2.2 3 1.4-.4 2.6c-6.8.6-13.8-6.4-13.2-13.2l2.6-.4 1.4 3z" fill="#fff"/></svg>'
scene("end", 4.8, d_html + f"""
    <div id="en-glow" data-layout-ignore style="position:absolute;left:-200px;top:260px;width:1400px;height:900px;background:radial-gradient(closest-side, rgba(212,175,90,0.25), rgba(212,175,90,0));"></div>
    <div id="en-logo" style="position:absolute;left:114px;top:340px;width:780px;height:475px;padding:60px;"><img src="assets/logo-gold.png" alt="" style="display:block;width:660px;height:355px;filter:drop-shadow(0 0 26px rgba(233,201,122,0.35));" /></div>
    <div id="en-t" class="blk" style="top:820px;font-family:'HF Amiri',serif;font-weight:700;font-size:84px;line-height:1.3;color:#f6ecd6;"><span class="w">جودة</span> <span class="w">تليق</span> <span class="w" style="color:#f3d98f">بضيافتك</span></div>
    <div id="en-s" class="blk" style="top:960px;font-weight:700;font-size:40px;line-height:1.4;color:#e9c97a;">للطلب والاستفسار</div>
    <div id="en-pill" style="position:absolute;left:174px;top:1050px;width:660px;height:110px;border-radius:55px;background:#f6ecd6;display:flex;align-items:center;justify-content:center;gap:22px;direction:ltr;box-shadow:0 18px 40px rgba(0,0,0,0.35);">
      {CHAT}<span style="font-weight:800;font-size:52px;color:#2a1c10;line-height:1;">+973 33337811</span>
    </div>
""", d_js + """
      tl.fromTo("#en-logo", { clipPath: "inset(0% 0% 100% 0%)", scale: 0.94 }, { clipPath: "inset(0% 0% 0% 0%)", scale: 1, duration: 0.9, ease: "power2.inOut" }, 0.05);
      wordsIn("#en-t", 0.7, 0.12);
      lineIn("#en-s", 1.2);
      tl.fromTo("#en-pill", { opacity: 0, y: 40, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(1.6)" }, 1.4);
""")

# ---------------- index ----------------
plan = [("hook", 4.2), ("brand", 4.2), ("flash", fl_dur), ("ring", 4.8), ("quality", 4.8), ("end", 4.8)]
t, hosts = 0.0, ""
for sid, du in plan:
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
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden;
        background: radial-gradient(120% 70% at 50% 42%, #33230f 0%, #1a120b 55%, #0f0a06 100%); }}
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
print("total", TOTAL, "music", music)
