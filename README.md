# studio-kit

The studio's toolkit for building client websites: a vetted library index, a hardened Astro starter, a client-repo template, the **site-builder** agent with four helpers, and the forks kept under `github.com/KDVassen`.

Public at github.com/KDVassen/studio-kit. Decisions behind it: knowledge-base files `17-libraries_review-list.md` and `18-studio-kit_builder-2026-10-01.md` (D12, D13).

## What's here

| Path | What |
|---|---|
| `library/INDEX.md` | The library index: 37 picks plus the starter's own dependencies — what each is for, pinned install command, licence, reduced-motion notes |
| `library/index.json` · `data.py` · `build_kit.py` | Index data and its generator (`python library/build_kit.py` after editing `data.py`) |
| `library/research-2026-10-01.md` | The original research, including everything excluded and why |
| `forks.json` | The 21 forks: upstream, licence, and whether the studio has modified them |
| `skills/studio-kit/` | The skill: how to choose and use libraries, patterns, rules, and `notices.py` |
| `agents/` | `site-builder` (the session agent) and its helpers: `design-researcher`, `qa-auditor`, `compliance-auditor`, `library-scout` |
| `starter/` | Astro 7 + Tailwind v4 + daisyUI + React-island support + Cloudflare Worker enquiry form. Every client site starts as a copy |
| `templates/client-site/` | Copied over the starter for each client: `CLAUDE.md`, `.claude/settings.json` (runs the session as site-builder, with permission gates), `PROJECT.md`, handover skeleton |
| `scripts/install.sh` | Links the skill and agents into `~/.claude` |
| `scripts/sync-forks.sh` | Syncs every unmodified fork from upstream and prints a report (run monthly) |

## Install

```bash
bash scripts/install.sh
```

Then start a new Claude Code session so the skill and agents load.

## Start a client site

In the Claude desktop app, open a new session in `Code Projects/Websites/clients/`: its settings start the session as the builder. From a terminal with the `claude` CLI, run:

```bash
claude --agent site-builder
```

It asks for the client and the repository name, confirms before creating anything, then copies `starter/` and `templates/client-site/` into `Code Projects\Websites\clients\<repo>`. From then on, any session opened in that folder runs as site-builder automatically (via its `.claude/settings.json`) and resumes from `PROJECT.md`.

## The rules that matter most

- **Forks are not install sources.** Client builds install from npm with pinned versions. A fork is used only after the studio changes it: tag it, install by tag or commit SHA, and set `"modified": true` in `forks.json` (which stops automatic syncing).
- **Nothing outside the index** goes into a client build without a library-scout check and the operator's approval.
- **GSAP is not forked**, because its licence grants use only. If a client site uses it, the handover documents carve it out of the client's sublicensing rights.
- **Payment, DNS and launch are human-only.** The builder stops at staging.

## Windows Smart App Control

Smart App Control blocks an unsigned native binary that Astro 7 uses for Markdown (`satteri`). Its WebAssembly build is installed once in `C:\Users\vasse\Code Projects\node_modules`, which Node finds from any project under that folder. Nothing in any project's `package.json` changes, and deleting that folder undoes it. On another Windows machine with Smart App Control, run:

```bash
npm i --no-save --no-package-lock --force --prefix "<a parent folder of your projects>" @bruits/satteri-wasm32-wasi@<satteri version>
```
