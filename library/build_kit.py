"""Generate studio-kit library files from data.py plus the operator's picks (2026-10-01)."""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from data import CATS, L, EXCLUDED

SK = r"C:\Users\vasse\Code Projects\studio-kit"
BY = {e["id"]: e for e in L}
CATNAME = {c[0]: c[1] for c in CATS}

FORK = ["animejs","autoanimate","babylon","basecoat","baseui","bklit","chartjs","daisyui","echarts","lenis",
        "lucide","magicui","motion","number-flow","r3f","reactaria","shadcn","tabler","threejs","visx"]
REF = ["aceternity","astro-icon","astro-router","coss","css-bg","css-scroll","dotlottie","embla","gsap",
       "headlessui","iconoir","locomotive","model-viewer","motionprimitives","radix","reactbits","view-transitions"]
STUDY_ONLY = {"aceternity": "Licence forbids redistributing source files; rebuild effects with Motion.",
              "reactbits": "MIT + Commons Clause forbids sublicensing; cannot enter client repos or the kit.",
              "coss": "Root licence is AGPL; only apps/origin and apps/ui are MIT. Study patterns only.",
              "locomotive": "Pins Lenis 1.3.17, which ignores reduced motion. Use Lenis + CSS scroll-driven animation."}

INSTALL = {
 "animejs": "npm i animejs@4.5.0  # import subpaths: animejs/animation, animejs/utils",
 "autoanimate": "npm i @formkit/auto-animate@0.10.0",
 "babylon": "npm i @babylonjs/core@9.29.0",
 "basecoat": "npm i basecoat-css@1.0.2",
 "baseui": "npm i @base-ui/react@1.8.0",
 "bklit": "npx shadcn@4.21.1 add @bklit/<chart>  # never the stat-card items",
 "chartjs": "npm i chart.js@4.5.1",
 "daisyui": "npm i -D daisyui@5.7.47  # Tailwind v4 plugin: @plugin \"daisyui\";",
 "echarts": "npm i echarts@6.1.0  # import from echarts/core",
 "lenis": "npm i lenis@1.3.26  # pin >=1.3.26 for reduced motion",
 "lucide": "npm i @lucide/astro@1.49.0  # React islands: lucide-react@1.49.0",
 "magicui": "npx shadcn@4.21.1 add @magicui/<component>",
 "motion": "npm i motion@13.5.0",
 "number-flow": "npm i number-flow@0.6.2  # React: @number-flow/react",
 "r3f": "npm i three@0.186.1 @react-three/fiber@9.8.1 @react-three/drei@10.7.9",
 "reactaria": "npm i react-aria-components@1.21.1",
 "shadcn": "npx shadcn@4.21.1 init  # in an Astro project with @astrojs/react",
 "tabler": "npm i @tabler/icons@3.48.0  # SVGs; React: @tabler/icons-react",
 "threejs": "npm i three@0.186.1",
 "visx": "npm i @visx/shape@4.0.0 @visx/scale@4.0.0",
 "astro-icon": "npm i astro-icon@1.2.0 @iconify-json/lucide @iconify-json/tabler",
 "astro-router": "built into astro: import { ClientRouter } from 'astro:transitions'",
 "dotlottie": "npm i @lottiefiles/dotlottie-web@0.80.0  # self-host the WASM",
 "embla": "do not install yet: 8.6.0 fails the 12-month rule and 9.0 is still a release candidate; use the scroll-snap row (patterns.md 12)",
 "gsap": "npm i gsap@3.15.0  # flagged licence: carve out of client sublicensing",
 "headlessui": "npm i @headlessui/react@2.2.10",
 "iconoir": "npm i iconoir@7.12.1",
 "model-viewer": "npm i @google/model-viewer@4.3.1  # load on interaction",
 "motionprimitives": "copy components from motion-primitives.com; runtime: motion@13.5.0",
 "radix": "npm i radix-ui@1.6.7",
 "css-bg": "no install: see references/patterns.md", "css-scroll": "no install: see references/patterns.md",
 "view-transitions": "no install: see references/patterns.md",
 "aceternity": "do not install (study only)", "reactbits": "do not install (study only)",
 "coss": "do not install (study only)", "locomotive": "do not install (study only)",
}
REPO_SLUG = {"r3f": ["pmndrs/react-three-fiber", "pmndrs/drei"]}
STARTER_EXTRA = {
 "id": "a11y-astro", "status": "starter", "note": "Added because the Astro starter uses it (approved in the 2026-10-01 plan). The operator may veto.",
}

def slug(repo): return repo.replace("https://github.com/", "").strip("/")

entries = []
for status, ids in (("fork", FORK), ("reference", REF)):
    for i in ids:
        e = dict(BY[i])
        e["status"] = status
        e["use"] = "study-only" if i in STUDY_ONLY else "ship"
        e["use_note"] = STUDY_ONLY.get(i, "")
        e["install"] = INSTALL[i]
        e["category"] = CATNAME[e["cat"]]
        entries.append(e)
a = dict(BY["a11y-astro"]); a.update(status="starter", use="ship", use_note=STARTER_EXTRA["note"],
                                     install="npm i accessible-astro-components@5.8.0", category=CATNAME["ui"])
entries.append(a)
assert len([e for e in entries if e["status"] == "fork"]) == 20 and len([e for e in entries if e["status"] == "reference"]) == 17

io.open(os.path.join(SK, "library", "index.json"), "w", encoding="utf-8", newline="\n").write(
    json.dumps({"verified": "2026-10-01", "entries": entries}, indent=2, ensure_ascii=False) + "\n")

forks = []
for i in FORK:
    e = BY[i]
    for up in REPO_SLUG.get(i, [slug(e["repo"])]):
        forks.append({"upstream": up, "fork": "KDVassen/" + up.split("/")[1], "library": e["name"],
                      "licence": e["lic"], "modified": False,
                      "note": "Existing fork; sync, don't re-fork." if i == "animejs" else
                              ("Never use code under LICENSE-STUDIO.md (proprietary Studio)." if i == "bklit" else
                               ("Apache-2.0: keep NOTICE, mark changed files." if "Apache" in e["lic"] else ""))})
io.open(os.path.join(SK, "forks.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(forks, indent=2) + "\n")

# Human-readable index (README-style) and the skill's reference copy
def md_index(for_skill):
    out = []; w = out.append
    w("# Library index" if not for_skill else "# Library index (skill reference)")
    w("")
    w("Verified 2026-10-01 against npm, GitHub and each repo's LICENSE file. Pinned versions are the ones verified; check for a newer release at install and re-verify its licence before moving.")
    w("")
    w("**Status:** `fork` = forked under KDVassen (install from npm anyway unless the fork carries studio changes) · `reference` = in the index, not forked · `starter` = used by the Astro starter.")
    w("**Use:** `ship` may go into client code · `study-only` must never enter a client repo or the kit.")
    w("")
    w("## Quick lookup: I need X")
    w("")
    w("| Need | First choice | Then |")
    w("|---|---|---|")
    for need, first, then in [
        ("Scroll reveal / parallax / progress bar", "CSS scroll-driven animations (patterns.md)", "reveal snippet; then Motion `inView`/`scroll`"),
        ("Page transitions", "Native cross-document view transitions", "Astro `<ClientRouter />` when state or video must persist"),
        ("Tween, stagger, timeline", "Motion", "anime.js for timeline-heavy plain JS; GSAP only for premium briefs, with the carve-out"),
        ("Smooth scroll feel", "Nothing (native scroll)", "Lenis ≥1.3.26, only on request"),
        ("List add/remove/reorder", "Same-document view transition", "AutoAnimate"),
        ("Animated stat numbers", "Number Flow (real numbers only)", "—"),
        ("Hero background", "CSS animated background (patterns.md)", "three.js only for a scoped, separately-priced 3D brief"),
        ("3D product viewer", "<model-viewer>, loaded on interaction", "React Three Fiber + drei on a React island"),
        ("Components, zero JS", "daisyUI classes on native elements", "Basecoat (vanilla JS widgets)"),
        ("Accessible widgets (dialog, tabs, menu)", "Native <dialog>/<details>/popover styled with daisyUI", "Accessible Astro Components (+~9 KB CSS); Base UI or React Aria on an island; shadcn for a styled kit"),
        ("Marketing flourishes", "Magic UI (free, MIT) on an island", "Motion Primitives patterns; retrofit reduced motion"),
        ("Icons", "Lucide via @lucide/astro or astro-icon", "Tabler for gaps; Iconoir for finer strokes"),
        ("Charts (any platform)", "Chart.js", "ECharts for dashboards/maps; Bklit or visx on React islands"),
        ("Carousel", "CSS scroll-snap row (patterns.md 12)", "Embla once 9.0 stable ships; Swiper 14 only if the operator approves its index entry"),
        ("Lottie animation", "Muted video loop", "dotLottie player, lazy-loaded below the fold"),
    ]:
        w(f"| {need} | {first} | {then} |")
    w("")
    for cid, title, note in CATS:
        items = [e for e in entries if e["cat"] == cid]
        if not items: continue
        w(f"## {title}"); w(""); w(f"> {note}"); w("")
        for e in items:
            w(f"### {e['name']} — `{e['status']}` · `{e['use']}`")
            w("")
            w(f"- {e['what']}")
            w(f"- **Why:** {e['why']}")
            if e["use_note"]: w(f"- **Use note:** {e['use_note']}")
            if e.get("note"): w(f"- **Watch:** {e['note']}")
            w(f"- **Install:** `{e['install']}`")
            w(f"- **Licence:** {e['lic']} — {e['handover']}")
            w(f"- **Reduced motion / a11y:** {e['a11y']}")
            w(f"- **Size:** {e['size']} · **Build cost:** {e['cost']}")
            w(f"- **Links:** {' · '.join(x for x in (e['url'], e['repo']) if x)}")
            w("")
    w("## Considered and excluded")
    w("")
    w("Do not use these; reasons from the 2026-10-01 research. A library-scout run is needed to revisit any of them.")
    w("")
    for cat, name, reason in EXCLUDED:
        w(f"- **{name}** ({CATNAME[cat]}): {reason}")
    return "\n".join(out) + "\n"

io.open(os.path.join(SK, "library", "INDEX.md"), "w", encoding="utf-8", newline="\n").write(md_index(False))
io.open(os.path.join(SK, "skills", "studio-kit", "references", "library-index.md"), "w", encoding="utf-8", newline="\n").write(md_index(True))
print("entries", len(entries), "| forks.json rows", len(forks))
