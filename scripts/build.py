"""Generate the profile README's SVG assets (light and dark) and README.md.

Run from the repo root:  python3 scripts/build.py
Images in scripts/src/ are embedded into the SVGs, because GitHub renders
README images as <img>, which can't load anything external.
"""
import base64
import pathlib
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "src"
OUT = ROOT / "assets"
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"

THEMES = {
    "light": dict(bg="#ffffff", fg="#1f2328", muted="#59636e", line="#d1d9e0", subtle="#f6f8fa", link="#0969da",
                  ok="#1a7f37", ok_bg="#dafbe1", wa="#9a6700", wa_bg="#fff8c5", os="#8250df", os_bg="#fbefff",
                  heat=("#9be9a8", "#40c463", "#216e39"), heat_ink=("#1f2328", "#ffffff", "#ffffff")),
    "dark": dict(bg="#0d1117", fg="#e6edf3", muted="#9198a1", line="#3d444d", subtle="#151b23", link="#4493f8",
                 ok="#3fb950", ok_bg="#12261a", wa="#d29922", wa_bg="#2e2410", os="#ab7df8", os_bg="#241a3a",
                 heat=("#0e4429", "#196c2e", "#2ea043"), heat_ink=("#e6edf3", "#ffffff", "#ffffff")),
}

CATS = [
    dict(id="ai", name="AI tools & MCP servers", line="Products that AI agents use directly over MCP.", cols=2, items=[
        dict(slug="cms", n="Innolope CMS", u="github.com/Innolope/innolope-cms", h="https://github.com/Innolope/innolope-cms", st=[("os", "Open source")],
             d="Headless CMS that agents write to over MCP. Markdown-native and self-hosted.", k=["TypeScript", "MCP", "PostgreSQL"]),
        dict(slug="emilytics", n="Emilytics", u="emilytics.com", h="https://emilytics.com", st=[("ok", "App Store"), ("ok", "Web")],
             d="Google Analytics and Search Console in one place. Ask in plain language or through MCP, with anomaly alerts.", k=["Next.js", "Node", "MCP", "Expo"]),
        dict(slug="apphero", n="AppHero", u="apphero.online", h="https://apphero.online", st=[("ok", "Live")],
             d="Turns raw app captures into store screenshots for every device and language. Agents can drive it over MCP.", k=["Next.js", "MCP", "Rendering"]),
        dict(slug="documenda", n="Documenda", u="documenda.innolope.com", h="https://documenda.innolope.com", st=[("ok", "Live")],
             d="Workspace for contracts and policies: generated with Claude and Gemini, imported from PDF, DOCX and email.", k=["Node", "React", "Claude", "Gemini"]),
    ]),
    dict(id="mobile", name="Mobile apps", line="Expo and React Native apps.", cols=2, items=[
        dict(slug="wowch", n="Wowch", u="wooowch.com", h="https://wooowch.com", st=[("ok", "App Store"), ("ok", "Google Play")],
             d="Vertical video city guide: short reviews of places, filmed by locals and ranked by the community.", k=["Expo", "React Native", "Video", "Firebase"]),
        dict(slug="vibetown", n="Vibetown", u="vibetown.pro", h="https://vibetown.pro", st=[("ok", "App Store"), ("ok", "Web")],
             d="Job marketplace for developers who build with AI. SvelteKit web app, Expo app and a browser extension on one backend.", k=["SvelteKit", "Expo", "Node"]),
        dict(slug="scoop", n="Scoop", u="App Store · Google Play", h="https://apps.apple.com/us/app/scoop-conversation-practice/id6828656782", st=[("ok", "App Store"), ("ok", "Google Play")],
             d="Five-minute practice calls with a tough AI counterpart, then a scorecard of what to say next time.", k=["Expo", "Node", "LLM"]),
        dict(slug="forkie", n="Forkie", u="4kie.com", h="https://4kie.com", st=[("ok", "Web"), ("wa", "App coming")],
             d="1,360 recipes with a photo for every cooking step, produced by an image pipeline. Fridge Mode matches what you have.", k=["Expo", "RevenueCat", "Image pipeline"]),
    ]),
    dict(id="data", name="Data pipelines", line="Raw public data collected, cleaned and turned into products people search.", cols=2, items=[
        dict(slug="tinyworld", n="Tiny World", u="tinyworld.online", h="https://tinyworld.online", st=[("ok", "Live")],
             d="10,000 synthetic US residents built from IPUMS census microdata, with realistic links between income, education and occupation.", k=["Python", "pandas", "NumPy", "IPUMS"], crop="xMinYMid slice"),
        dict(slug="pulse", n="Innolope Pulse", u="innolope.com/pulse", h="https://innolope.com/pulse", st=[("ok", "Live")],
             d="Startup data grouped into generated industry pages, with community voting and its own MCP server.", k=["Next.js", "Express", "MongoDB", "MCP"]),
        dict(slug="techfeed", n="Techfeed", u="techfeed.online", h="https://techfeed.online", st=[("ok", "Live")],
             d="Checks newsrooms every ten minutes, matches keywords in any language and delivers to a feed, email or Telegram.", k=["Next.js", "Node", "Python"]),
    ]),
    dict(id="desktop", name="Desktop apps", line="Native and Electron apps for macOS: screen capture, messaging, menu bar.", cols=2, items=[
        dict(slug="texterry", n="Texterry", u="texterry.com", h="https://texterry.com", st=[("ok", "macOS"), ("ok", "Windows")],
             d="One inbox for Telegram, WhatsApp and Discord, with an AI assistant that reads while you're away and an MCP endpoint.", k=["Electron", "React", "Node", "MCP"]),
        dict(slug="bergman", n="Bergman Memo", u="bergman.digital", h="https://bergman.digital", st=[("wa", "Early access")],
             d="Record your screen, camera and voice, then send a link instead of booking a meeting. Comes with a virtual camera with live filters.", k=["Swift", "ScreenCaptureKit", "AVFoundation", "CMIO"]),
        dict(slug="limitfuel", n="LimitFuel", u="github.com/Innolope/LimitFuel", h="https://github.com/Innolope/LimitFuel", st=[("os", "Open source")],
             d="Menu bar app for Claude and Codex usage limits. Signed and notarized, with Windows and Linux builds.", k=["Swift", "AppKit", "Rust"]),
    ]),
    dict(id="web", name="Web products", line="Consumer sites with search, catalogues and browser extensions.", cols=2, items=[
        dict(slug="jobalto", n="Jobalto", u="jobalto.com", h="https://jobalto.com", st=[("ok", "Live")],
             d="Career map of occupations, salaries, skill gaps, courses and live vacancies, with a psychometric career test.", k=["Node", "MongoDB", "Gemini", "OpenAI"]),
        dict(slug="fragnoir", n="Fragnoir", u="fragnoir.com", h="https://fragnoir.com", st=[("ok", "Web"), ("wa", "App coming")],
             d="Fragrance catalogue built from Open Beauty Facts and Wikidata, with a price-comparison Chrome extension.", k=["Next.js", "MongoDB", "Chrome MV3"]),
    ]),
    dict(id="fintech", name="Fintech & security", line="Production code that moves real money, on web and native.", note="[See my merged pull requests in peanut-ui →](https://github.com/peanutprotocol/peanut-ui/pulls?q=is%3Apr+author%3Ainnolope-dev+is%3Amerged)", cols=1, items=[
        dict(slug="peanut", n="Peanut", u="peanut.me", h="https://peanut.me", st=[("ok", "Live"), ("ok", "Contract engineer")],
             d="Contract engineer since June 2026 on a live payments app for web, iOS and Android: passkey sign-in, step-up auth on card and money-movement routes, biometric-guarded session tokens and JWT revocation.",
             k=["TypeScript", "Next.js", "Capacitor", "WebAuthn"], crop="xMinYMid slice", kpi=[("772", "merged PRs"), ("2", "repos: app + API")]),
    ]),
]

STATS = [("Products", "28", "shipped"), ("This year", "20", "launches"), ("App Store", "5", "apps shipped"), ("MCP", "5", "servers live"), ("Peanut", "772", "merged PRs")]
PHONES = [("ph_wowch", "Wowch"), ("ph_scoop", "Scoop"), ("ph_emilytics", "Emilytics"), ("ph_vibetown", "Vibetown"), ("ph_forkie", "Forkie")]
CASES = [
    ("Bergman Memo", "long screen recordings that never lose the file",
     "AVAssetWriter throws away the whole file on a single out-of-order timestamp, and a full disk used to fail silently in the middle of a recording.",
     "Every frame passes through a monotonic timeline, mic and system audio are mixed on one sample clock, and a disk guard warns before space runs out.",
     "Swift, ScreenCaptureKit, AVFoundation"),
    ("Tiny World", "synthetic people that look like real census data",
     "Sampling each attribute on its own gives impossible people, such as a teenage surgeon on a high income.",
     "Records are drawn from IPUMS ACS microdata so income, education, age and occupation stay consistent, then checked against a JSON Schema.",
     "Python, pandas, NumPy"),
    ("Peanut", "auth that works the same in a browser and a native app",
     "Passkeys, cookies and keychains all behave differently in a browser, an iOS wrapper and an Android wrapper, and the app moves real money.",
     "Step-up auth on card and money-movement routes, server-side JWT revocation with a per-user token version, and session tokens held in Keychain or Keystore behind biometrics.",
     "TypeScript, Next.js, Capacitor, WebAuthn"),
]


def img(slug):
    return "data:image/webp;base64," + base64.b64encode((SRC / f"{slug}.webp").read_bytes()).decode()


def wrap(text, width):
    lines, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return lines + [cur] if cur else lines


def t(x, y, s, size, fill, weight=400, anchor="start", family=FONT, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{extra}>{escape(s)}</text>')


def pill(x, y, label, kind, c, anchor_right=False):
    w = round(len(label) * 6.3 + 14)
    if anchor_right:
        x -= w
    return (f'<rect x="{x}" y="{y}" width="{w}" height="20" rx="10" fill="{c[kind + "_bg"]}"/>'
            + t(x + w / 2, y + 14, label, 11, c[kind], 600, "middle", MONO)), w


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f'<title>{escape(title)}</title>{body}</svg>\n')


def write(name, theme, content):
    (OUT / f"{name}-{theme}.svg").write_text(content)


# ---------- header: the store listing ----------
HEADER_ALT = ("Slav, founding engineer, remote, open to founding-engineer roles. 28 products shipped, 20 in 2026, "
              "5 apps shipped to the App Store, 5 MCP servers live, 772 merged PRs at Peanut.")


def header(theme):
    c = THEMES[theme]
    W, P = 880, 24
    b = [f'<rect x="0.5" y="0.5" width="{W-1}" height="H" rx="16" fill="{c["bg"]}" stroke="{c["line"]}"/>']
    b.append('<defs><radialGradient id="g1" cx="30%" cy="25%" r="60%"><stop offset="0" stop-color="#ffd27a"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient>'
             '<radialGradient id="g2" cx="75%" cy="75%" r="60%"><stop offset="0" stop-color="#4493f8"/><stop offset="1" stop-color="#4493f8" stop-opacity="0"/></radialGradient></defs>')
    b.append(f'<rect x="{P}" y="{P}" width="96" height="96" rx="24" fill="#1b1f24"/><rect x="{P}" y="{P}" width="96" height="96" rx="24" fill="url(#g1)"/>'
             f'<rect x="{P}" y="{P}" width="96" height="96" rx="24" fill="url(#g2)"/>' + t(P + 48, P + 63, "S", 44, "#ffffff", 700, "middle"))
    b.append(t(P + 116, P + 34, "Slav", 30, c["fg"], 700))
    b.append(t(P + 116, P + 60, "Founding engineer · web, mobile, macOS, AI", 16, c["muted"]))
    b.append(t(P + 116, P + 84, "Remote · open to founding-engineer roles", 15, c["ok"], 600))
    b.append(f'<rect x="{W-P-104}" y="{P+30}" width="104" height="36" rx="18" fill="#0a84ff"/>' + t(W - P - 52, P + 54, "HIRE", 16, "#ffffff", 700, "middle", extra=' letter-spacing="1"'))
    y = P + 120
    b.append(f'<line x1="{P}" y1="{y}" x2="{W-P}" y2="{y}" stroke="{c["line"]}"/><line x1="{P}" y1="{y+76}" x2="{W-P}" y2="{y+76}" stroke="{c["line"]}"/>')
    cw = (W - 2 * P) / len(STATS)
    for i, (k, v, s) in enumerate(STATS):
        cx = P + cw * i + cw / 2
        b.append(t(cx, y + 20, k.upper(), 10.5, c["muted"], 600, "middle", extra=' letter-spacing="0.6"'))
        b.append(t(cx, y + 46, v, 22, c["fg"], 700, "middle"))
        b.append(t(cx, y + 64, s, 11.5, c["muted"], 400, "middle"))
        if i:
            b.append(f'<line x1="{P+cw*i}" y1="{y+12}" x2="{P+cw*i}" y2="{y+64}" stroke="{c["line"]}"/>')
    y += 96
    ph_h, gap = 330, 18
    ph_w = round(ph_h * 320 / 695)
    total = len(PHONES) * ph_w + (len(PHONES) - 1) * gap
    x0 = (W - total) / 2
    for i, (slug, label) in enumerate(PHONES):
        x = x0 + i * (ph_w + gap)
        b.append(f'<clipPath id="p{i}"><rect x="{x}" y="{y}" width="{ph_w}" height="{ph_h}" rx="20"/></clipPath>'
                 f'<image href="{img(slug)}" x="{x}" y="{y}" width="{ph_w}" height="{ph_h}" preserveAspectRatio="xMidYMin slice" clip-path="url(#p{i})"/>'
                 f'<linearGradient id="s{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></linearGradient>'
                 f'<rect x="{x}" y="{y+ph_h-48}" width="{ph_w}" height="48" fill="url(#s{i})" clip-path="url(#p{i})"/>'
                 f'<rect x="{x+.5}" y="{y+.5}" width="{ph_w-1}" height="{ph_h-1}" rx="20" fill="none" stroke="{c["line"]}"/>'
                 + t(x + 12, y + ph_h - 14, label, 13, "#ffffff", 600))
    H = y + ph_h + P
    body = "".join(b).replace('height="H"', f'height="{H-1}"')
    return svg(W, H, body, HEADER_ALT)


def header_m(theme):
    """Phone version: fewer, larger elements, so it stays readable at ~350px."""
    c = THEMES[theme]
    W, P = 440, 20
    b = [f'<rect x="0.5" y="0.5" width="{W-1}" height="H" rx="16" fill="{c["bg"]}" stroke="{c["line"]}"/>',
         '<defs><radialGradient id="g1" cx="30%" cy="25%" r="60%"><stop offset="0" stop-color="#ffd27a"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient>'
         '<radialGradient id="g2" cx="75%" cy="75%" r="60%"><stop offset="0" stop-color="#4493f8"/><stop offset="1" stop-color="#4493f8" stop-opacity="0"/></radialGradient></defs>',
         f'<rect x="{P}" y="{P}" width="76" height="76" rx="19" fill="#1b1f24"/><rect x="{P}" y="{P}" width="76" height="76" rx="19" fill="url(#g1)"/>'
         f'<rect x="{P}" y="{P}" width="76" height="76" rx="19" fill="url(#g2)"/>' + t(P + 38, P + 51, "S", 36, "#ffffff", 700, "middle"),
         t(P + 92, P + 30, "Slav", 28, c["fg"], 700),
         t(P + 92, P + 54, "Founding engineer", 17, c["muted"]),
         t(P + 92, P + 76, "Remote · open to roles", 16, c["ok"], 600)]
    y = P + 96
    b.append(f'<line x1="{P}" y1="{y}" x2="{W-P}" y2="{y}" stroke="{c["line"]}"/>')
    stats = [STATS[0], STATS[2], STATS[4]]
    cw = (W - 2 * P) / 3
    for i, (k, v, s) in enumerate(stats):
        cx = P + cw * i + cw / 2
        b.append(t(cx, y + 36, v, 26, c["fg"], 700, "middle") + t(cx, y + 58, s, 14, c["muted"], 400, "middle"))
    y += 76
    ph = PHONES[:3]
    gap = 12
    ph_w = (W - 2 * P - 2 * gap) / 3
    ph_h = round(ph_w * 695 / 320)
    for i, (slug, label) in enumerate(ph):
        x = P + i * (ph_w + gap)
        b.append(f'<clipPath id="p{i}"><rect x="{x}" y="{y}" width="{ph_w}" height="{ph_h}" rx="16"/></clipPath>'
                 f'<image href="{img(slug)}" x="{x}" y="{y}" width="{ph_w}" height="{ph_h}" preserveAspectRatio="xMidYMin slice" clip-path="url(#p{i})"/>'
                 f'<rect x="{x+.5}" y="{y+.5}" width="{ph_w-1}" height="{ph_h-1}" rx="16" fill="none" stroke="{c["line"]}"/>')
    H = y + ph_h + P
    return svg(W, H, "".join(b).replace('height="H"', f'height="{H-1}"'), HEADER_ALT)


def card_m(p, theme, W=220):
    """Phone version of a card: picture, name and one status, large enough to read at half a phone width."""
    c = THEMES[theme]
    img_h = round(W * 0.55)
    b = [f'<clipPath id="c"><rect width="{W}" height="HH" rx="10"/></clipPath>',
         f'<g clip-path="url(#c)"><rect width="{W}" height="HH" fill="{c["bg"]}"/>'
         f'<image href="{img(p["slug"])}" x="0" y="0" width="{W}" height="{img_h}" preserveAspectRatio="{p.get("crop", "xMidYMin slice")}"/>'
         f'<line x1="0" y1="{img_h}" x2="{W}" y2="{img_h}" stroke="{c["line"]}"/></g>']
    y = img_h + 30
    b.append(t(12, y, p["n"], 20, c["fg"], 700))
    kind, label = p["st"][0]
    y += 12
    w = round(len(label) * 9 + 18)
    b.append(f'<rect x="12" y="{y}" width="{w}" height="26" rx="13" fill="{c[kind + "_bg"]}"/>' + t(12 + w / 2, y + 18, label, 14, c[kind], 600, "middle"))
    H = y + 26 + 14
    b.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="none" stroke="{c["line"]}"/>')
    return svg(W, H, "".join(b).replace('height="HH"', f'height="{H}"'), f'{p["n"]}: {p["d"]}')


# ---------- project cards ----------
def card(p, theme, W, lines_max, compact):
    c = THEMES[theme]
    img_h = round(W * 0.55)
    pad = 16
    fs = 13 if compact else 13.5
    chars = int((W - 2 * pad) / (fs * 0.52))
    desc = wrap(p["d"], chars)
    b = [f'<clipPath id="c"><rect x="0" y="0" width="{W}" height="HH" rx="12"/></clipPath>',
         f'<g clip-path="url(#c)"><rect width="{W}" height="HH" fill="{c["bg"]}"/>',
         f'<image href="{img(p["slug"])}" x="0" y="0" width="{W}" height="{img_h}" preserveAspectRatio="xMidYMin slice"/>',
         f'<line x1="0" y1="{img_h}" x2="{W}" y2="{img_h}" stroke="{c["line"]}"/></g>']
    y = img_h + 30
    b.append(t(pad, y, p["n"], 17, c["fg"], 700))
    px = W - pad
    for kind, label in reversed(p["st"]):
        s, w = pill(px, y - 15, label, kind, c, anchor_right=True)
        b.append(s)
        px -= w + 5
    y += 8
    for ln in desc:
        y += 19
        b.append(t(pad, y, ln, fs, c["muted"]))
    y += 19 * (lines_max - len(desc))
    y += 14
    x = pad
    for chip in p["k"]:
        w = round(len(chip) * 6.7 + 12)
        if x + w > W - pad:
            break
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="21" rx="4" fill="{c["subtle"]}" stroke="{c["line"]}"/>' + t(x + 6, y + 14.5, chip, 11, c["muted"], 400, family=MONO))
        x += w + 5
    y += 21 + 22
    b.append(t(pad, y, p["u"], 12, c["link"], 400, family=MONO))
    H = y + 16
    b.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{c["line"]}"/>')
    return svg(W, H, "".join(b).replace('height="HH"', f'height="{H}"'), f'{p["n"]}: {p["d"]} {" / ".join(l for _, l in p["st"])}.')


def wide_card(p, theme):
    c = THEMES[theme]
    W, H, iw, pad = 880, 300, 440, 22
    b = [f'<clipPath id="c"><rect width="{W}" height="{H}" rx="12"/></clipPath>',
         f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{c["bg"]}"/>'
         f'<image href="{img(p["slug"])}" x="0" y="0" width="{iw}" height="{H}" preserveAspectRatio="{p.get("crop", "xMidYMin slice")}"/>'
         f'<line x1="{iw}" y1="0" x2="{iw}" y2="{H}" stroke="{c["line"]}"/></g>']
    x, y = iw + pad, 44
    b.append(t(x, y, p["n"], 22, c["fg"], 700))
    px = W - pad
    for kind, label in reversed(p["st"]):
        s, w = pill(px, y - 16, label, kind, c, anchor_right=True)
        b.append(s)
        px -= w + 5
    y += 6
    for ln in wrap(p["d"], 56):
        y += 20
        b.append(t(x, y, ln, 14, c["muted"]))
    y += 40
    kx = x
    if not p.get("kpi"):
        y -= 40
    for v, l in p.get("kpi", []):
        b.append(t(kx, y, v, 26, c["fg"], 700) + t(kx, y + 18, l, 12, c["muted"]))
        kx += 150
    y += 40
    cx = x
    for chip in p["k"]:
        w = round(len(chip) * 6.7 + 12)
        b.append(f'<rect x="{cx}" y="{y}" width="{w}" height="21" rx="4" fill="{c["subtle"]}" stroke="{c["line"]}"/>' + t(cx + 6, y + 14.5, chip, 11, c["muted"], 400, family=MONO))
        cx += w + 5
    b.append(t(x, H - 20, p["u"], 12, c["link"], 400, family=MONO))
    b.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{c["line"]}"/>')
    return svg(W, H, "".join(b), f'{p["n"]}: {p["d"]}')


def button(label, theme, primary):
    c = THEMES[theme]
    w = round(len(label) * 8.2 + 34)
    fill, ink, stroke = ("#1f883d" if theme == "light" else "#238636", "#ffffff", "none") if primary else (c["subtle"], c["fg"], c["line"])
    return svg(w, 36, f'<rect x=".5" y=".5" width="{w-1}" height="35" rx="7" fill="{fill}" stroke="{stroke}"/>' + t(w / 2, 23, label, 14, ink, 600, "middle"), label)


PHONE = "(max-width: 600px)"


def pic(name, alt, width=None, href=None, phone=False):
    wa = f' width="{width}"' if width else ""
    m = (f'<source media="{PHONE} and (prefers-color-scheme: dark)" srcset="assets/{name}-m-dark.svg">'
         f'<source media="{PHONE}" srcset="assets/{name}-m-light.svg">') if phone else ""
    p = (f'<picture>{m}<source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">'
         f'<img src="assets/{name}-light.svg" alt="{escape(alt)}"{wa}></picture>')
    return f'<a href="{href}">{p}</a>' if href else p


def split(items):
    """Two-column grid; an odd one out (the first item) gets a full-width card."""
    return (items[:1], items[1:]) if len(items) % 2 else ([], items)


def anchor(name):
    return "".join(ch for ch in name.lower().replace(" ", "-") if ch.isalnum() or ch == "-")


def main():
    OUT.mkdir(exist_ok=True)
    for f in OUT.glob("*.svg"):
        f.unlink()
    for th in THEMES:
        write("header", th, header(th))
        write("header-m", th, header_m(th))
        write("btn-contact", th, button("✉ Email me about a role", th, True))
        write("btn-linkedin", th, button("LinkedIn", th, False))
        for cat in CATS:
            wide, grid = split(cat["items"])
            for p in cat["items"]:
                write(f'card-{p["slug"]}-m', th, card_m(p, th, 440 if p in wide else 220))
            for p in wide:
                write(f'card-{p["slug"]}', th, wide_card(p, th))
            if not grid:
                continue
            W = 432
            chars = int((W - 32) / (13.5 * 0.52))
            lm = max(len(wrap(p["d"], chars)) for p in grid)
            for p in grid:
                write(f'card-{p["slug"]}', th, card(p, th, W, lm, False))

    contact = "mailto:sf@innolope.com"
    linkedin = "https://www.linkedin.com/in/slavikfokin/"
    md = []
    md.append(f'<a href="{contact}">{pic("header", HEADER_ALT, phone=True)}</a>\n')
    md.append("## I take a product from empty repo to the App Store, then keep it running.\n")
    md.append("Looking for a **founding or first-engineer role** on a small, fully remote team that ships fast. "
              "I've built mobile apps, AI tools with MCP servers, data pipelines and desktop apps, "
              "and I handle security and payments work on a live fintech product.\n")
    md.append(pic("btn-contact", "Email me about a role: sf@innolope.com", href=contact) + "&nbsp;" + pic("btn-linkedin", "LinkedIn", href=linkedin) + "\n")
    md.append("### Hard parts\n")
    for name, sub, prob, sol, stack in CASES:
        md.append(f"<details open><summary><b>{name}</b>: {sub}</summary>\n\n"
                  f"**Problem.** {prob}\n\n**Solution.** {sol}\n\n**Stack.** {stack}\n\n</details>\n")
    md.append("### Projects by area\n")
    md.append(" · ".join(f'[{c["name"]}](#{anchor(c["name"])}) ({len(c["items"])})' for c in CATS) + "\n")
    for cat in CATS:
        md.append(f'### {cat["name"]}\n')
        md.append(f'{cat["line"]}\n')
        wide, grid = split(cat["items"])
        if cat.get("note"):
            md.append(cat["note"] + "\n")
        rows = [[pic(f'card-{p["slug"]}', f'{p["n"]}: {p["d"]}', "98.4%", p["h"], phone=True)] for p in wide]
        cards = [pic(f'card-{p["slug"]}', f'{p["n"]}: {p["d"]}', "49%", p["h"], phone=True) for p in grid]
        rows += [cards[i:i + 2] for i in range(0, len(cards), 2)]
        md.append('<p align="left">\n' + "\n".join(" ".join(r) + "<br>" for r in rows) + "\n</p>\n")
    md.append("---\n")
    md.append("**Hiring your first engineers?** Small team, remote, lots of ownership: that's the job I'm looking for.\n")
    md.append(pic("btn-contact", "Email me about a role: sf@innolope.com", href=contact) + "&nbsp;" + pic("btn-linkedin", "LinkedIn", href=linkedin) + "\n")
    md.append("sf@innolope.com · [linkedin.com/in/slavikfokin](https://www.linkedin.com/in/slavikfokin/)\n")
    (ROOT / "README.md").write_text("\n".join(md))
    sizes = sum(f.stat().st_size for f in OUT.glob("*.svg"))
    print(f"{len(list(OUT.glob('*.svg')))} SVGs, {sizes // 1024} KB")


if __name__ == "__main__":
    main()
