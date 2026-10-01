#!/usr/bin/env python3
"""Generate THIRD_PARTY_NOTICES.md and docs/handover/dependencies.md for a client project.

Run from the client project root after `npm install`:
    python <studio-kit>/skills/studio-kit/scripts/notices.py
Exits 1 (and writes nothing) if any shipped package has a licence the client cannot keep.
Standard library only.
"""
import datetime, glob, json, os, re, subprocess, sys

ROOT = os.getcwd()
PERMISSIVE = {"MIT", "ISC", "BSD-2-Clause", "BSD-3-Clause", "Apache-2.0", "0BSD", "Unlicense", "CC0-1.0",
              "OFL-1.1", "BlueOak-1.0.0", "Python-2.0", "Zlib", "WTFPL"}
ATTRIBUTION_OR_WEAK = {"CC-BY-4.0", "CC-BY-3.0", "MPL-2.0"}           # allowed, but listed under "Check"
FORBIDDEN = re.compile(r"(A?GPL|LGPL|SSPL|BUSL|Commons Clause|CC-BY-NC|CC-BY-SA|UNLICENSED)", re.I)
STUDY_ONLY = {"locomotive-scroll"}                                       # from the studio-kit index
FLAGGED = {"gsap": ("Webflow 'Standard No Charge' licence. Licensed to the client directly by Webflow and "
                    "excluded from the studio's modify / sublicense / transfer grant. Keep every @license header.")}
SHIPS_FROM_DEV = {"daisyui", "tailwindcss", "@tailwindcss/vite"}         # build-time packages whose output ships


def run_npm_ls():
    cmd = ["npm", "ls", "--omit=dev", "--all", "--json", "--long"]
    if os.name == "nt":
        cmd = ["cmd", "/c"] + cmd
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    try:
        return json.loads(r.stdout or "{}")
    except json.JSONDecodeError:
        sys.exit("notices: could not parse `npm ls` output. Run `npm install` first.")


def pkg_dir(name):
    return os.path.join(ROOT, "node_modules", *name.split("/"))


def read_pkg(path):
    try:
        with open(os.path.join(path, "package.json"), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def licence_of(meta):
    lic = meta.get("license")
    if isinstance(lic, dict):
        lic = lic.get("type")
    if not lic and isinstance(meta.get("licenses"), list) and meta["licenses"]:
        lic = " OR ".join(str(x.get("type", "")) for x in meta["licenses"])
    return (lic or "UNKNOWN").strip()


def judge(name, lic):
    """Return (verdict, reason): verdict is ok | check | flagged | fail."""
    if name in STUDY_ONLY:
        return "fail", "study-only in the studio-kit index"
    if name in FLAGGED:
        return "flagged", FLAGGED[name]
    expr = lic.strip("() ")
    alts = [a.strip("() ") for a in re.split(r"\s+OR\s+", expr)] if " OR " in expr else [expr]
    best = "fail"
    for alt in alts:
        parts = [p.strip("() ") for p in re.split(r"\s+AND\s+", alt)]
        if any(FORBIDDEN.search(p) for p in parts):
            v = "fail"
        elif all(p in PERMISSIVE for p in parts):
            v = "ok"
        elif all(p in PERMISSIVE or p in ATTRIBUTION_OR_WEAK for p in parts):
            v = "check"
        else:
            v = "fail"
        if v == "ok":
            return "ok", ""
        if v == "check":
            best = "check"
    if best == "check":
        return "check", f"{lic}: attribution or file-level copyleft; keep notices and source of changed files"
    return "fail", f"{lic}: not a licence the client can keep, or not recognised. Review by hand."


def licence_texts(path):
    out = []
    for pattern in ("LICEN[CS]E*", "licen[cs]e*", "COPYING*", "NOTICE*", "notice*"):
        for f in sorted(glob.glob(os.path.join(path, pattern))):
            if os.path.isfile(f) and f not in [x[0] for x in out]:
                try:
                    with open(f, encoding="utf-8", errors="replace") as fh:
                        out.append((f, fh.read().strip()))
                except OSError:
                    pass
    return out


def collect():
    tree = run_npm_ls()
    found = {}

    def walk(deps):
        for name, info in (deps or {}).items():
            ver = info.get("version")
            if not ver or (name, ver) in found:
                continue
            path = info.get("path") or pkg_dir(name)
            meta = read_pkg(path) or info
            found[(name, ver)] = {"name": name, "version": ver, "path": path,
                                  "licence": licence_of(meta), "author": str(meta.get("author", ""))[:120]}
            walk(info.get("dependencies"))

    walk(tree.get("dependencies"))
    root = read_pkg(ROOT)
    for name in (root.get("devDependencies") or {}):
        if name in SHIPS_FROM_DEV:
            path = pkg_dir(name)
            meta = read_pkg(path)
            if meta.get("version"):
                found.setdefault((name, meta["version"]), {"name": name, "version": meta["version"], "path": path,
                                                          "licence": licence_of(meta), "author": str(meta.get("author", ""))[:120]})
    allow = set(((root.get("studioKit") or {}).get("noticesAllow")) or [])
    return root, sorted(found.values(), key=lambda p: (p["name"].lower(), p["version"])), allow


def copied_source():
    path = os.path.join(ROOT, "PROJECT.md")
    if not os.path.exists(path):
        return []
    lines, inside = [], False
    for line in open(path, encoding="utf-8"):
        if line.startswith("## "):
            inside = line.strip().lower() == "## copied source"
            continue
        if inside and line.strip().startswith("- "):
            lines.append(line.strip()[2:])
    return lines


def main():
    if not os.path.exists(os.path.join(ROOT, "package.json")):
        sys.exit("notices: run this from a project root containing package.json")
    root, pkgs, allow = collect()
    results = []
    for p in pkgs:
        verdict, reason = judge(p["name"], p["licence"])
        if verdict == "fail" and p["name"] in allow:
            verdict, reason = "check", f"{p['licence']}: allowed by studioKit.noticesAllow in package.json (operator decision)"
        results.append((p, verdict, reason))

    fails = [(p, r) for p, v, r in results if v == "fail"]
    if fails:
        print("notices: FAILED. These packages cannot ship to a client as-is:\n")
        for p, r in fails:
            print(f"  - {p['name']}@{p['version']}: {r}")
        print("\nRemove them, replace them, or (after the operator approves) add the name to "
              "package.json → studioKit.noticesAllow.")
        sys.exit(1)

    today = datetime.date.today().isoformat()
    n = []
    n.append("# Third-party notices\n")
    n.append(f"Generated {today} by studio-kit `notices.py`. Lists every third-party package shipped with this site, "
             "its licence, and the licence text the package provides.\n")
    flagged = [(p, r) for p, v, r in results if v in ("flagged", "check")]
    if flagged:
        n.append("## Read first\n")
        for p, r in flagged:
            n.append(f"- **{p['name']}@{p['version']}**: {r}")
        n.append("")
    n.append("## Packages\n")
    n.append("| Package | Version | Licence |")
    n.append("|---|---|---|")
    for p, v, r in results:
        n.append(f"| {p['name']} | {p['version']} | {p['licence']} |")
    n.append("")
    cs = copied_source()
    n.append("## Copied source\n")
    n.append("Code copied into this project from component registries (it carries no headers of its own):\n")
    n.extend([f"- {c}" for c in cs] or ["- None recorded. List copied components under `## Copied source` in PROJECT.md."])
    n.append("")
    n.append("## Fonts, icons and images\n")
    n.append("Add each asset by hand: name, version, licence, licence holder.\n")
    n.append("## Licence texts\n")
    for p, v, r in results:
        texts = licence_texts(p["path"])
        n.append(f"### {p['name']}@{p['version']} — {p['licence']}\n")
        if not texts:
            n.append("_No licence file in the package. Licence declared in package.json only._\n")
        for f, t in texts:
            n.append(f"`{os.path.basename(f)}`\n\n```text\n{t}\n```\n")
    with open(os.path.join(ROOT, "THIRD_PARTY_NOTICES.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(n) + "\n")

    d = [f"# Dependencies\n", f"Generated {today} by studio-kit `notices.py`, for the handover pack.\n",
         "## Direct dependencies\n", "| Package | Range in package.json | Installed | Licence |", "|---|---|---|---|"]
    installed = {p["name"]: p for p in pkgs}
    for section in ("dependencies", "devDependencies"):
        for name, rng in sorted((root.get(section) or {}).items()):
            meta = installed.get(name) or {"version": read_pkg(pkg_dir(name)).get("version", "?"),
                                           "licence": licence_of(read_pkg(pkg_dir(name)))}
            d.append(f"| {name}{' (dev)' if section == 'devDependencies' else ''} | {rng} | {meta['version']} | {meta['licence']} |")
    d.append(f"\nShipped packages including transitive: **{len(pkgs)}**. Full list and licence texts: `THIRD_PARTY_NOTICES.md`.\n")
    os.makedirs(os.path.join(ROOT, "docs", "handover"), exist_ok=True)
    with open(os.path.join(ROOT, "docs", "handover", "dependencies.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(d) + "\n")

    print(f"notices: OK - {len(pkgs)} shipped packages, {len(flagged)} to read first. "
          "Wrote THIRD_PARTY_NOTICES.md and docs/handover/dependencies.md")


if __name__ == "__main__":
    main()
