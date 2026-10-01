# PROJECT

> The site-builder agent reads this at the start of every session and updates it whenever the phase changes, a decision is made, or a gate is passed. Dates on everything.

| | |
|---|---|
| Client | [CLIENT NAME] |
| Repository | [REPO NAME] (private) |
| Local folder | [PATH] |
| Started | [DATE] |
| **Current phase** | 0 Kickoff |

## Gates

Tick only with a date. Human-only gates are ticked by the operator.

- [ ] Repository created — operator approved — 
- [ ] Scope and quote sent to client — 
- [ ] Deposit (40%) received — **operator confirms** — 
- [ ] Homepage design signed off **in writing** by the client — 
- [ ] Second payment (40%) received — **operator confirms** — 
- [ ] Enquiry form and Worker reviewed line by line by the operator — 
- [ ] QA clean: qa-auditor and compliance-auditor, no open CONFIRMED findings — 
- [ ] Staging deploy approved by the operator — 
- [ ] Final payment (20%) — **HUMAN ONLY** — 
- [ ] DNS cut-over and launch — **HUMAN ONLY** — 

## Client facts

Business, customers, the one action a visitor should take, contact methods, area, hours. Real facts only.

## Scope

Pages (standard package: up to 5), inclusions, exclusions, revision rounds used (of 2), content due dates.

## Decisions

| Date | Decision | Why |
|---|---|---|

## Open questions

- [ ] **Enquiry delivery:** how does the client hear about a new enquiry? (stored in D1 by default; nothing notifies anyone yet)
- [ ] **Content editing after handover:** how will the client edit their own content?

## Budget exceptions

Decision D14: any page over the 30 KB JavaScript budget (for example a React island) needs the operator's approval, recorded here first.

| Date | Page | What and why | Size (gzip) | Approved by |
|---|---|---|---|---|

## Design

Canvas link, sign-off date, theme tokens and every computed contrast ratio.

## Copied source

Components copied in from registries (shadcn, Magic UI, Bklit…), one per line: `- name — source URL — licence`. `notices.py` lists these in THIRD_PARTY_NOTICES.md.

## Assets register

| Asset | Version / source | Licence | Licence holder |
|---|---|---|---|

## Phase log

| Date | Phase | Event |
|---|---|---|
