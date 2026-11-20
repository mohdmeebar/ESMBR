"""Generates the scene files of the 'reel-how' HyperFrames project (1080x1920, 50 s)."""
import os, sys

OUT = sys.argv[1]
os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)

HEAD = """  <style>
    @font-face { font-family: "HF Amiri"; font-weight: 700; src: url("assets/fonts/amiri-700.woff2") format("woff2"); }
    @font-face { font-family: "HF Cairo"; font-weight: 400; src: url("assets/fonts/cairo-400.woff2") format("woff2"); }
    @font-face { font-family: "HF Cairo"; font-weight: 700; src: url("assets/fonts/cairo-700.woff2") format("woff2"); }
    @font-face { font-family: "HF Cairo"; font-weight: 800; src: url("assets/fonts/cairo-800.woff2") format("woff2"); }
    #root { position: absolute; inset: 0; direction: rtl; font-family: "HF Cairo", sans-serif; color: #23271a; }
    .w { display: inline-block; }
    .head { position: absolute; left: 120px; width: 768px; top: 330px; text-align: center;
      font-family: "HF Amiri", serif; font-weight: 700; font-size: 92px; line-height: 1.3; color: #4a5e2a; }
    .head .g { color: #8a6a1f; }
    .cap { position: absolute; left: 120px; width: 768px; top: 1150px; text-align: center;
      font-weight: 700; font-size: 44px; line-height: 1.4; color: #8a6a1f; }
    .kick { position: absolute; left: 0; width: 1080px; top: 290px; text-align: center; font-weight: 700; font-size: 32px; color: #8a8f7a; }
    .qr { display: block; }
    .card { position: absolute; width: 300px; height: 420px; background: linear-gradient(135deg, #fbf6ea, #efe4c9);
      border: 3px solid #b8913a; border-radius: 10px; box-shadow: 0 18px 40px rgba(40, 45, 25, 0.22); text-align: center; }
    .card::after { content: ""; position: absolute; inset: 8px; border: 1px solid #b8913a; border-radius: 6px; }
    .card .t1 { font-family: "HF Amiri", serif; font-weight: 700; font-size: 58px; color: #b8913a; margin-top: 26px; line-height: 1.2; }
    .card .t2 { font-size: 20px; color: #4a5e2a; }
    .card .nm { font-weight: 800; font-size: 36px; color: #23271a; margin: 6px 0 10px; }
    .card .qr { margin: 0 auto; }
  </style>
"""

QR_JS = """
      function mulberry32(a) { return function () { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
        t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
      function qrSVG(seed, size, color) {
        const N = 25, m = size / N, r = mulberry32(seed); let s = "";
        const inF = (i, j) => (i < 8 && j < 8) || (i > N - 9 && j < 8) || (i < 8 && j > N - 9);
        for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) { const v = r(); if (!inF(i, j) && v > 0.52) s += `<rect x="${(i * m).toFixed(2)}" y="${(j * m).toFixed(2)}" width="${(m + 0.3).toFixed(2)}" height="${(m + 0.3).toFixed(2)}"/>`; }
        const f = (x, y) => `<rect x="${x * m}" y="${y * m}" width="${7 * m}" height="${7 * m}"/><rect x="${(x + 1) * m}" y="${(y + 1) * m}" width="${5 * m}" height="${5 * m}" fill="#fff"/><rect x="${(x + 2) * m}" y="${(y + 2) * m}" width="${3 * m}" height="${3 * m}"/>`;
        return `<svg class="qr" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}"><rect width="${size}" height="${size}" fill="#fff"/><g fill="${color}">${s}${f(0, 0)}${f(N - 7, 0)}${f(0, N - 7)}</g></svg>`;
      }
      document.querySelectorAll("[data-qr]").forEach((el) => { el.innerHTML = qrSVG(+el.dataset.qr, +el.dataset.size, el.dataset.color || "#4a5e2a"); });
"""

HELPERS = """
      const tl = gsap.timeline({ paused: true });
      const wordsIn = (sel, at, gap) => tl.fromTo(sel + " .w", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.22, ease: "power4.out", stagger: gap || 0.08 }, at);
      const lineIn = (sel, at) => tl.fromTo(sel, { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.3, ease: "power3.out" }, at);
      const out = (sel, at, d) => tl.to(sel, { opacity: 0, filter: "blur(10px)", duration: d || 0.25, ease: "power2.in" }, at);
"""


def scene(sid, dur, body, script, extra_css=""):
    css = HEAD.replace("  </style>\n", extra_css + "  </style>\n")
    html = f"""<template>
{css}  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920" data-duration="{dur}">
{body}
  </div>
  <script>
    (function () {{
{QR_JS if "data-qr" in body else ""}{HELPERS}
{script}
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
"""
    with open(os.path.join(OUT, "compositions", sid + ".html"), "w") as fh:
        fh.write(html)


# ---------------- s1 hook (0 - 4.5) ----------------
scene("hook", 4.5, """
    <div id="hk-big" style="position:absolute;left:120px;width:768px;top:380px;text-align:center;font-family:'HF Amiri',serif;font-weight:700;font-size:220px;line-height:1.15;color:#4a5e2a;">
      <div id="hk-l1">عندك</div><div id="hk-l2" style="color:#8a6a1f">حفل؟</div>
    </div>
    <div id="hk-sub" style="position:absolute;left:120px;width:768px;top:960px;text-align:center;font-weight:800;font-size:64px;line-height:1.35;color:#23271a;">
      <span class="w">ومئات</span> <span class="w">الضيوف</span> <span class="w">والدعوات؟</span>
    </div>
    <div id="hk-pill" style="position:absolute;left:254px;width:500px;top:1110px;height:96px;border-radius:48px;background:#4a5e2a;color:#f6eedb;text-align:center;font-weight:800;font-size:44px;line-height:96px;">خلّ التنظيم علينا</div>
""", """
      tl.fromTo("#hk-big", { scale: 1.06 }, { scale: 1, duration: 0.6, ease: "expo.out" }, 0);
      wordsIn("#hk-sub", 1.1, 0.12);
      tl.fromTo("#hk-pill", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.7)" }, 2.3);
      out("#hk-big, #hk-sub, #hk-pill", 4.2);
""")

# ---------------- s2 three things (4.5 - 11.5) ----------------
ICON_ENV = '<svg width="64" height="64" viewBox="0 0 64 64"><rect x="6" y="14" width="52" height="36" rx="5" fill="none" stroke="#f6eedb" stroke-width="4"/><path d="M8 17 L32 36 L56 17" fill="none" stroke="#f6eedb" stroke-width="4"/></svg>'
ICON_LOGO = '<svg width="64" height="64" viewBox="0 0 64 64"><path d="M32 6 L54 32 L32 58 L10 32 Z" fill="none" stroke="#f6eedb" stroke-width="4"/><circle cx="32" cy="32" r="8" fill="#e3c47a"/></svg>'
ICON_XLS = '<svg width="64" height="64" viewBox="0 0 64 64"><rect x="8" y="8" width="48" height="48" rx="5" fill="none" stroke="#f6eedb" stroke-width="4"/><path d="M8 24 H56 M8 40 H56 M28 8 V56" stroke="#f6eedb" stroke-width="3"/></svg>'
rows = ""
for i, (ic, t, d) in enumerate([(ICON_ENV, "تصميم الدعوة", "صورة أو ملف تصميم الدعوة"),
                                 (ICON_LOGO, "شعار الحفل", "بصيغة PNG بخلفية شفافة"),
                                 (ICON_XLS, "ملف Excel", "بأسماء وأرقام المدعوين")]):
    y = 580 + i * 200
    rows += f"""
    <div id="it-row{i}" style="position:absolute;left:120px;top:{y}px;width:768px;height:170px;background:#fffdf7;border-radius:28px;box-shadow:0 14px 34px rgba(40,45,25,0.12);">
      <div style="position:absolute;right:28px;top:28px;width:114px;height:114px;border-radius:24px;background:#4a5e2a;display:flex;align-items:center;justify-content:center;">{ic}</div>
      <div style="position:absolute;right:170px;top:30px;font-weight:800;font-size:46px;color:#23271a;line-height:1.3;">{t}</div>
      <div style="position:absolute;right:170px;top:96px;font-weight:400;font-size:32px;color:#6b705c;line-height:1.3;">{d}</div>
      <div style="position:absolute;left:34px;top:50px;width:70px;height:70px;border-radius:35px;border:3px solid #b8913a;color:#b8913a;font-weight:800;font-size:38px;line-height:64px;text-align:center;">{'١٢٣'[i]}</div>
    </div>"""
scene("items", 7, f"""
    <div id="it-head" class="head"><span class="w">أرسل</span> <span class="w">لنا</span> <span class="w g">٣ أشياء</span> <span class="w">فقط</span></div>
{rows}
""", """
      wordsIn("#it-head", 0.15, 0.1);
      [0, 1, 2].forEach((i) => tl.fromTo("#it-row" + i, { opacity: 0, x: 120, filter: "blur(8px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 0.55, ease: "expo.out" }, 0.9 + i * 0.6));
      tl.to("#it-row2", { scale: 1.05, duration: 0.3, ease: "power2.out", yoyo: true, repeat: 1 }, 4.4);
      out("#it-head, #it-row0, #it-row1", 6.2);
      tl.to("#it-row2", { y: -360, scale: 1.0, duration: 0.55, ease: "power3.inOut" }, 6.2);
      tl.to("#it-row2", { opacity: 0, duration: 0.2 }, 6.75);
""")

# ---------------- s3 excel -> personal cards (11.5 - 19.5) ----------------
names = [("سارة أحمد", "+973 3••• ••12"), ("خالد محمد", "+973 3••• ••48"), ("نورة علي", "+973 3••• ••07"),
         ("عبدالله سالم", "+973 3••• ••93"), ("ريم يوسف", "+973 3••• ••61")]
trs = "".join(f"""
        <div id="xc-r{i}" style="display:flex;height:66px;border-top:1px solid #e3e0d4;font-size:30px;line-height:66px;">
          <div style="width:70px;text-align:center;color:#8a8f7a;">{'١٢٣٤٥'[i]}</div>
          <div style="flex:1;font-weight:700;">{n}</div>
          <div style="width:300px;direction:ltr;text-align:left;padding-left:24px;color:#6b705c;">{p}</div>
        </div>""" for i, (n, p) in enumerate(names))
fan = [(-150, 40, -12), (-75, 15, -6), (0, 0, 0), (75, 15, 6), (150, 40, 12)]
cards = ""
for i, (n, _) in enumerate(names):
    dx, dy, rot = fan[i]
    cards += f"""
    <div id="xc-c{i}" class="card" data-layout-allow-overlap style="left:{354 + dx}px;top:{760 + dy}px;z-index:{10 + i};">
      <div class="t1">دعوة</div><div class="t2">نتشرف بدعوتكم لحضور الحفل</div>
      <div class="nm">{n.split()[0]}</div><div data-qr="{11 + i}" data-size="150"></div>
    </div>"""
scene("cards", 8, f"""
    <div id="xc-head" class="head" style="font-size:84px;"><span class="w">دعوة</span> <span class="w g">باسم</span> <span class="w g">كل</span> <span class="w g">ضيف</span></div>
    <div id="xc-sheet" style="position:absolute;left:120px;top:500px;width:768px;transform-origin:50% 0%;background:#fffdf7;border-radius:24px;overflow:hidden;box-shadow:0 14px 34px rgba(40,45,25,0.12);">
      <div style="display:flex;height:70px;background:#4a5e2a;color:#f6eedb;font-weight:800;font-size:30px;line-height:70px;">
        <div style="width:70px;text-align:center;">#</div><div style="flex:1;">الاسم</div><div style="width:300px;padding-left:24px;text-align:left;">رقم الجوال</div>
      </div>{trs}
    </div>
{cards}
    <div id="xc-cap" class="cap" style="top:1235px;">ورمز QR فريد لا يتكرر</div>
""", f"""
      wordsIn("#xc-head", 0.1, 0.08);
      tl.fromTo("#xc-sheet", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }}, 0.05);
      tl.to("#xc-sheet", {{ scale: 0.6, duration: 0.6, ease: "power3.inOut" }}, 1.5);
      const fan = {fan};
      for (let i = 0; i < 5; i++) {{
        const at = 2.0 + i * 0.55;
        tl.fromTo("#xc-r" + i, {{ backgroundColor: "rgba(227,196,122,0)" }}, {{ backgroundColor: "rgba(227,196,122,0.45)", duration: 0.15 }}, at - 0.15);
        tl.to("#xc-r" + i, {{ backgroundColor: "rgba(227,196,122,0)", duration: 0.3 }}, at + 0.35);
        tl.fromTo("#xc-c" + i, {{ opacity: 0, y: -200, scale: 0.3, rotation: 0 }}, {{ opacity: 1, y: 0, scale: 1, rotation: fan[i][2], duration: 0.6, ease: "expo.out" }}, at);
      }}
      lineIn("#xc-cap", 5.0);
      out("#xc-head, #xc-sheet, #xc-cap", 7.5);
      for (let i = 0; i < 5; i++) tl.to("#xc-c" + i, {{ x: -fan[i][0], y: 120, rotation: 0, scale: 0.4, opacity: 0, duration: 0.45, ease: "power3.in" }}, 7.4 + i * 0.03);
""", extra_css="    #xc-sheet > div { padding: 0 6px; }\n")

# ---------------- s4 whatsapp (19.5 - 27.5) ----------------
chat_rows = ""
cn = ["سارة أحمد", "خالد محمد", "نورة علي", "عبدالله سالم", "ريم يوسف", "يوسف حسن"]
for i, n in enumerate(cn):
    chat_rows += f"""
        <div id="wa-r{i}" style="position:absolute;left:0;right:0;top:{150 + i * 90}px;height:90px;border-bottom:1px solid #ece8dc;">
          <div style="position:absolute;right:22px;top:16px;width:60px;height:60px;border-radius:30px;background:{['#d9e3c4','#efe2c2','#dfe8c8','#e8dcc0'][i % 4]};color:#4a5e2a;font-weight:800;font-size:28px;line-height:60px;text-align:center;">{n[0]}</div>
          <div style="position:absolute;right:98px;top:12px;font-weight:800;font-size:26px;">{n}</div>
          <div style="position:absolute;right:98px;top:50px;font-size:22px;color:#6b705c;">بطاقة دعوتك للحفل</div>
          <div id="wa-t{i}" style="position:absolute;left:22px;top:30px;font-weight:800;font-size:26px;color:#8a8f7a;direction:ltr;">✓</div>
          <div id="wa-tt{i}" style="position:absolute;left:22px;top:30px;font-weight:800;font-size:26px;color:#2f9be0;direction:ltr;">✓✓</div>
        </div>"""
scene("whatsapp", 8, f"""
    <div id="wa-head" class="head" style="font-size:76px;"><span class="w">تُرسل</span> <span class="w">تلقائياً</span> <span class="w g">عبر</span> <span class="w g">واتساب</span></div>
    <div id="wa-phone" style="position:absolute;left:294px;top:520px;width:420px;height:720px;border-radius:56px;background:#1c1d1f;box-shadow:0 30px 60px rgba(30,35,20,0.35);">
      <div style="position:absolute;inset:12px;border-radius:46px;overflow:hidden;background:#fffdf7;">
        <div style="position:absolute;left:0;right:0;top:0;height:140px;background:#4a5e2a;color:#fff;text-align:center;">
          <div style="font-weight:800;font-size:30px;padding-top:56px;">دعوات الحفل</div>
          <div id="wa-count" style="font-size:24px;opacity:0.85;">قائمة المدعوين</div>
        </div>{chat_rows}
      </div>
    </div>
    <div id="wa-done" style="position:absolute;left:214px;top:345px;width:580px;height:96px;border-radius:48px;background:#4a5e2a;color:#f6eedb;text-align:center;font-weight:800;font-size:38px;line-height:96px;box-shadow:0 14px 30px rgba(40,45,25,0.25);">✓ وصلت لكل المدعوين</div>
""", """
      wordsIn("#wa-head", 0.1, 0.08);
      tl.fromTo("#wa-phone", { opacity: 0, y: 160, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.7, ease: "expo.out" }, 0.0);
      for (let i = 0; i < 6; i++) {
        const at = 0.9 + i * 0.45;
        tl.fromTo("#wa-r" + i, { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, at);
        tl.fromTo("#wa-t" + i, { opacity: 0 }, { opacity: 1, duration: 0.1 }, at + 0.3);
        tl.fromTo("#wa-t" + i, { opacity: 1 }, { opacity: 0, duration: 0.1, immediateRender: false }, at + 0.75);
        tl.fromTo("#wa-tt" + i, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)" }, at + 0.75);
      }
      out("#wa-head", 4.35, 0.2);
      tl.fromTo("#wa-done", { opacity: 0, scale: 0.7, y: 20 }, { opacity: 1, scale: 1, y: 0, duration: 0.45, ease: "back.out(1.7)" }, 4.6);
      out("#wa-done", 7.6);
      tl.to("#wa-phone", { x: -700, rotation: -8, opacity: 0, duration: 0.4, ease: "power3.in" }, 7.55);
""")

# ---------------- scanner helper ----------------
def scanner(prefix, qr_seed, label):
    return f"""
    <div id="{prefix}-dev" style="position:absolute;left:214px;top:560px;width:580px;height:600px;border-radius:44px;background:#1c1d1f;box-shadow:0 30px 60px rgba(30,35,20,0.35);">
      <div id="{prefix}-view" style="position:absolute;inset:14px;border-radius:32px;overflow:hidden;background:#2a2c22;">
        <div style="position:absolute;left:131px;top:90px;padding:14px;background:#fff;border-radius:10px;"><div data-qr="{qr_seed}" data-size="260" data-color="#23271a"></div></div>
        <div style="position:absolute;left:0;right:0;top:430px;text-align:center;color:#d8d5c8;font-size:30px;">{label}</div>
        <div style="position:absolute;left:105px;top:64px;width:342px;height:342px;">
          <div style="position:absolute;left:0;top:0;width:60px;height:60px;border-left:8px solid #e3c47a;border-top:8px solid #e3c47a;"></div>
          <div style="position:absolute;right:0;top:0;width:60px;height:60px;border-right:8px solid #e3c47a;border-top:8px solid #e3c47a;"></div>
          <div style="position:absolute;left:0;bottom:0;width:60px;height:60px;border-left:8px solid #e3c47a;border-bottom:8px solid #e3c47a;"></div>
          <div style="position:absolute;right:0;bottom:0;width:60px;height:60px;border-right:8px solid #e3c47a;border-bottom:8px solid #e3c47a;"></div>
          <div id="{prefix}-line" style="position:absolute;left:10px;right:10px;top:0;height:6px;background:#3fdc6a;box-shadow:0 0 24px 8px rgba(63,220,106,0.55);"></div>
        </div>
      </div>
    </div>"""

# ---------------- s5 door welcome (27.5 - 35.5) ----------------
scene("door", 8, f"""
    <div id="dr-head" class="head" style="font-size:84px;"><span class="w">امسح</span> <span class="w">الرمز</span><br /><span class="w g">عند</span> <span class="w g">المدخل</span></div>
{scanner("dr", 11, "رمز دعوة الضيف")}
    <div id="dr-ok" data-layout-allow-occlusion data-layout-allow-overlap style="position:absolute;left:228px;top:574px;width:552px;height:572px;border-radius:32px;background:linear-gradient(#5f7a32,#4a5e2a);text-align:center;color:#fff;">
      <svg style="margin-top:70px" width="190" height="190" viewBox="0 0 190 190"><circle id="dr-ring" cx="95" cy="95" r="80" fill="none" stroke="#fff" stroke-width="12" stroke-dasharray="503" stroke-dashoffset="503" transform="rotate(-90 95 95)"/><path id="dr-tick" d="M55 98 L83 126 L136 70" fill="none" stroke="#fff" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="130" stroke-dashoffset="130"/></svg>
      <div id="dr-hi" style="font-weight:700;font-size:40px;margin-top:22px;">أهلاً بك</div>
      <div id="dr-name" style="font-family:'HF Amiri',serif;font-weight:700;font-size:92px;color:#f0d896;line-height:1.3;">سارة أحمد</div>
    </div>
    <div id="dr-cap" class="cap" style="top:1185px;">ترحيب باسم كل ضيف</div>
    <div id="dr-chip" style="position:absolute;left:174px;top:1185px;width:660px;height:84px;border-radius:42px;background:#fffdf7;box-shadow:0 12px 28px rgba(40,45,25,0.15);text-align:center;font-weight:700;font-size:32px;line-height:84px;color:#23271a;"><span style="color:#3fae5a">✓</span> أُضيفت سارة إلى قائمة الحضور</div>
""", """
      wordsIn("#dr-head", 0.1, 0.08);
      tl.fromTo("#dr-dev", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.6, ease: "expo.out" }, 0.0);
      tl.fromTo("#dr-line", { y: 0 }, { y: 330, duration: 0.75, ease: "sine.inOut", yoyo: true, repeat: 1 }, 0.9);
      tl.fromTo("#dr-ok", { opacity: 0, clipPath: "circle(0% at 50% 45%)" }, { opacity: 1, clipPath: "circle(80% at 50% 45%)", duration: 0.45, ease: "power3.out" }, 2.45);
      tl.to("#dr-ring", { strokeDashoffset: 0, duration: 0.5, ease: "power3.out" }, 2.6);
      tl.to("#dr-tick", { strokeDashoffset: 0, duration: 0.35, ease: "power2.out" }, 2.95);
      lineIn("#dr-hi", 3.15);
      tl.fromTo("#dr-name", { opacity: 0, filter: "blur(8px)", scale: 1.15 }, { opacity: 1, filter: "blur(0px)", scale: 1, duration: 0.4, ease: "expo.out" }, 3.35);
      lineIn("#dr-cap", 3.8);
      out("#dr-cap", 5.3, 0.2);
      tl.fromTo("#dr-chip", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, 5.5);
      out("#dr-head, #dr-chip, #dr-ok, #dr-dev", 7.65);
""")

# ---------------- s6 duplicate (35.5 - 41.5) ----------------
scene("dup", 6, f"""
    <div id="dp-head" class="head" style="font-size:84px;"><span class="w">حماية</span> <span class="w g">من</span> <span class="w g">التكرار</span></div>
{scanner("dp", 11, "صورة منسوخة من نفس الرمز")}
    <div id="dp-no" data-layout-allow-occlusion data-layout-allow-overlap style="position:absolute;left:228px;top:574px;width:552px;height:572px;border-radius:32px;background:linear-gradient(#b23a32,#8f2721);text-align:center;color:#fff;">
      <svg style="margin-top:80px" width="180" height="180" viewBox="0 0 180 180"><circle cx="90" cy="90" r="76" fill="none" stroke="#fff" stroke-width="12"/><path id="dp-x" d="M62 62 L118 118 M118 62 L62 118" fill="none" stroke="#fff" stroke-width="13" stroke-linecap="round"/></svg>
      <div style="font-weight:800;font-size:64px;margin-top:20px;">مسح مكرر!</div>
      <div style="font-size:32px;opacity:0.9;margin-top:6px;">هذا الرمز مستخدم مسبقاً</div>
    </div>
    <div id="dp-cap" class="cap" style="top:1185px;">لا يمكن مسح الكود أكثر من مرة</div>
""", """
      wordsIn("#dp-head", 0.1, 0.08);
      tl.fromTo("#dp-dev", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.5, ease: "expo.out" }, 0.0);
      tl.fromTo("#dp-line", { y: 0 }, { y: 330, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 1 }, 0.7);
      tl.fromTo("#dp-no", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power3.out" }, 2.0);
      tl.fromTo("#dp-no", { x: 0 }, { keyframes: [{ x: -22 }, { x: 18 }, { x: -12 }, { x: 8 }, { x: 0 }], duration: 0.45, ease: "none" }, 2.2);
      lineIn("#dp-cap", 2.7);
      out("#dp-head, #dp-cap, #dp-no, #dp-dev", 5.7);
""")

# ---------------- s7 live list (41.5 - 47) ----------------
live = ""
for i, (n, tm) in enumerate([("سارة أحمد", "٨:٠٢ م"), ("خالد محمد", "٨:٠٥ م"), ("نورة علي", "٨:٠٩ م"), ("عبدالله سالم", "٨:١٤ م")]):
    live += f"""
        <div id="lv-r{i}" style="position:absolute;left:30px;right:30px;top:{400 + i * 82}px;height:70px;border-radius:18px;background:#f4efe3;">
          <div style="position:absolute;right:22px;top:14px;font-weight:800;font-size:30px;">{n}</div>
          <div style="position:absolute;left:22px;top:12px;height:46px;padding:0 18px;border-radius:23px;background:#3fae5a;color:#fff;font-weight:700;font-size:24px;line-height:46px;">✓ حضر · {tm}</div>
        </div>"""
scene("live", 5.5, f"""
    <div id="lv-head" class="head" style="font-size:84px;"><span class="w">حضور</span> <span class="w g">يتحدّث</span> <span class="w g">لحظياً</span></div>
    <div id="lv-card" style="position:absolute;left:120px;top:500px;width:768px;height:740px;border-radius:36px;background:#fffdf7;box-shadow:0 20px 44px rgba(40,45,25,0.15);">
      <svg style="position:absolute;left:244px;top:40px" width="280" height="280" viewBox="0 0 280 280">
        <circle cx="140" cy="140" r="115" fill="none" stroke="#ece8dc" stroke-width="26"/>
        <circle id="lv-arc" cx="140" cy="140" r="115" fill="none" stroke="#4a5e2a" stroke-width="26" stroke-linecap="round" stroke-dasharray="722.6" stroke-dashoffset="722.6" transform="rotate(-90 140 140)"/>
      </svg>
      <div id="lv-pct" style="position:absolute;left:244px;width:280px;top:125px;text-align:center;font-weight:800;font-size:76px;color:#4a5e2a;line-height:1;">٠٪</div>
      <div style="position:absolute;left:244px;width:280px;top:215px;text-align:center;font-size:26px;color:#6b705c;">نسبة الحضور</div>
      <div style="position:absolute;left:0;right:0;top:345px;text-align:center;font-size:28px;color:#8a8f7a;">أرقام توضيحية</div>
{live}
    </div>
""", """
      wordsIn("#lv-head", 0.1, 0.08);
      tl.fromTo("#lv-card", { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, 0.0);
      const pct = { v: 0 }, el = document.getElementById("lv-pct");
      const arabic = (n) => String(n).replace(/[0-9]/g, (d) => "٠١٢٣٤٥٦٧٨٩"[d]);
      tl.fromTo(pct, { v: 0 }, { v: 86, duration: 2.6, ease: "power2.out", onUpdate: () => { el.textContent = arabic(Math.round(pct.v)) + "٪"; } }, 0.6);
      tl.fromTo("#lv-arc", { strokeDashoffset: 722.6 }, { strokeDashoffset: 722.6 * (1 - 0.86), duration: 2.6, ease: "power2.out" }, 0.6);
      for (let i = 0; i < 4; i++) tl.fromTo("#lv-r" + i, { opacity: 0, x: 80 }, { opacity: 1, x: 0, duration: 0.4, ease: "expo.out" }, 0.9 + i * 0.5);
      out("#lv-head, #lv-card", 5.25);
""")

# ---------------- s8 end (47 - 50) ----------------
scene("end", 3, """
    <img id="en-icon" src="assets/app-icon.png" alt="" style="position:absolute;left:424px;top:430px;width:160px;height:160px;border-radius:36px;box-shadow:0 14px 40px rgba(40,45,25,0.25);" />
    <div id="en-title" class="head" style="top:640px;font-size:120px;"><span class="w">إدارة</span> <span class="w">ضيوف</span> <span class="w g">الحفل</span></div>
    <div id="en-sub" style="position:absolute;left:120px;width:768px;top:990px;text-align:center;font-weight:700;font-size:40px;line-height:1.5;color:#6b705c;">دعوات · واتساب · QR · حضور لحظي</div>
    <div id="en-rule" style="position:absolute;left:424px;top:1090px;width:160px;height:4px;background:#b8913a;"></div>
""", """
      tl.fromTo("#en-icon", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.6)" }, 0.05);
      wordsIn("#en-title", 0.3, 0.1);
      lineIn("#en-sub", 0.75);
      tl.fromTo("#en-rule", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "expo.out" }, 0.9);
""")

# ---------------- index ----------------
plan = [("hook", 0, 4.5), ("items", 4.5, 7), ("cards", 11.5, 8), ("whatsapp", 19.5, 8),
        ("door", 27.5, 8), ("dup", 35.5, 6), ("live", 41.5, 5.5), ("end", 47, 3)]
hosts = "\n".join(
    f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{st}" data-duration="{du}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>'
    for sid, st, du in plan)
index = f"""<!doctype html>
<html lang="ar">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden;
        background-color: #f4efe3;
        background-image: radial-gradient(rgba(74, 94, 42, 0.09) 3px, transparent 3.5px), radial-gradient(rgba(184, 145, 58, 0.08) 3px, transparent 3.5px);
        background-size: 60px 60px, 60px 60px; background-position: 0 0, 30px 30px; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="50" data-width="1080" data-height="1920">
{hosts}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
with open(os.path.join(OUT, "index.html"), "w") as fh:
    fh.write(index)
print("ok")
