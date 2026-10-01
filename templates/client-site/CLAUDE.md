# CLAUDE.md — [CLIENT NAME] website

This repository is one client's website, built by the studio from studio-kit. Sessions here run as the **site-builder** agent (set in `.claude/settings.json`).

**Read first:** `PROJECT.md` (where this project stands), then the preloaded `studio-kit` skill and its `references/rules.md`.

## Stack

- **Astro** (decision D12): pages ship no JavaScript unless an island asks for it. **React islands** only where a component needs React.
- Tailwind v4 + daisyUI for styling; the client's theme lives in `src/styles/global.css`.
- Every client fact lives in `src/site.config.ts`. Components never hard-code names, contact details, prices or dates.
- Hosting: **Cloudflare Workers with static assets**. The enquiry form posts to `worker/index.ts`, which stores enquiries in **D1** and purges old data daily.
- **Content Security Policy is on:** no inline `style=""` attributes and no `'unsafe-inline'`. A React island costs about 68 KB of runtime, which needs the operator's budget exception.

## Hard rules (full list: studio-kit `references/rules.md`)

1. **Never** touch DNS, the registrar, production hosting, billing or credentials. Payment, DNS cut-over and launch are the operator's alone.
2. **Ask first** before: pushing, creating a repo or PR, any deploy (staging included), creating or changing a remote D1 database or secret, spending credits, or adding a library that is not in the studio-kit index.
3. **No secrets in git.** `.env*` and `.dev.vars` are git-ignored and must stay that way.
4. **No client customer data in the repo**, ever.
5. **Human review gate:** any change to `src/components/EnquiryForm.astro` or `worker/` is shown to the operator line by line before deploying.
6. **Nothing fabricated:** no invented reviews, client names, logos, statistics or prices. Use `[PLACEHOLDER]` and ask.
7. **WCAG 2.2 AA** and the performance budget (TBT ≤ 150 ms, CLS ≤ 0.02, LCP ≤ 2.0 s, JS ≤ 30 KB gzip per page) must pass before handover.
8. Every dependency's licence must let the client keep it. Run `npm run notices` before every staging deploy and at handover.

## Astro development

- Start the dev server in the background: `npx astro dev --background`; manage it with `npx astro dev stop | status | logs`.
- Full Worker + form test locally: `npm run db:local` once, then `npm run worker:dev`.
- Docs: https://docs.astro.build (routing, components, framework islands, content collections, styling).

## Windows note (this studio's machine)

Windows Smart App Control blocks an unsigned native file Astro 7 uses for Markdown. A WebAssembly fallback is installed once in `C:\Users\vasse\Code Projects\node_modules`, which every project under `Code Projects` picks up. If Astro reports "Cannot find native binding" for `satteri`, reinstall it there:
`npm i --no-save --no-package-lock --force --prefix "C:/Users/vasse/Code Projects" @bruits/satteri-wasm32-wasi@<satteri version>`
