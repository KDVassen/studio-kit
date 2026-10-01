# [CLIENT NAME] website

Built by the studio from the studio-kit starter: Astro 7, Tailwind v4 + daisyUI, React islands when needed, hosted on Cloudflare Workers with an enquiry form stored in Cloudflare D1.

## Run it

```bash
npm install
cp .dev.vars.example .dev.vars  # local-only secret for the form Worker; git-ignored
npx astro dev --background      # pages only, at http://localhost:4321
```

To test the enquiry form end to end (Worker + local database):

```bash
npm run db:local                 # once: create the local tables
npm run worker:dev               # builds, then serves site + form at http://localhost:8787
```

## Where things are

| Path | What |
|---|---|
| `src/site.config.ts` | **Every client fact**: name, contact, hours, privacy settings, analytics token, navigation |
| `src/styles/global.css` | The client's theme (daisyUI), focus styles, reduced-motion rules, page transitions |
| `src/layouts/Base.astro` | Skip link, landmarks, metadata, the reveal-on-scroll script |
| `src/components/EnquiryForm.astro` | The form. Works with JavaScript off. **Human review gate** |
| `worker/index.ts` | Receives the form: validation, honeypot, timing check, rate limit, retention purge. **Human review gate** |
| `worker/schema.sql` | Database tables |
| `wrangler.jsonc` | Cloudflare settings. The D1 `database_id` is a placeholder until the real database is created |
| `scripts/notices.py` | `npm run notices`: writes THIRD_PARTY_NOTICES.md and the dependency list, and fails on a licence the client can't keep |

## Before the first deploy (operator)

1. Rename the Worker in `wrangler.jsonc`.
2. `npx wrangler d1 create <client>-enquiries`, then paste the returned id into `wrangler.jsonc`.
3. `npx wrangler d1 execute <client>-enquiries --remote --file=worker/schema.sql`
4. `npx wrangler secret put RATE_SALT` (any long random string; it scrambles IP addresses before they are stored). Without it the form refuses every enquiry rather than store weakly protected data.
   The Worker also runs a daily clean-up at 03:00 UTC (cron in `wrangler.jsonc`) that enforces the privacy notice's deletion periods.
5. Decide how the client hears about new enquiries. Nothing sends a notification yet.
6. Review the form and Worker code line by line.

Deploys, D1 changes and secrets all prompt for approval; see `.claude/settings.json`.
