# Library index (skill reference)

Verified 2026-10-01 against npm, GitHub and each repo's LICENSE file. Pinned versions are the ones verified; check for a newer release at install and re-verify its licence before moving.

**Status:** `fork` = forked under KDVassen (install from npm anyway unless the fork carries studio changes) · `reference` = in the index, not forked · `starter` = used by the Astro starter.
**Use:** `ship` may go into client code · `study-only` must never enter a client repo or the kit.

## Quick lookup: I need X

| Need | First choice | Then |
|---|---|---|
| Scroll reveal / parallax / progress bar | CSS scroll-driven animations (patterns.md) | reveal snippet; then Motion `inView`/`scroll` |
| Page transitions | Native cross-document view transitions | Astro `<ClientRouter />` when state or video must persist |
| Tween, stagger, timeline | Motion | anime.js for timeline-heavy plain JS; GSAP only for premium briefs, with the carve-out |
| Smooth scroll feel | Nothing (native scroll) | Lenis ≥1.3.26, only on request |
| List add/remove/reorder | Same-document view transition | AutoAnimate |
| Animated stat numbers | Number Flow (real numbers only) | — |
| Hero background | CSS animated background (patterns.md) | three.js only for a scoped, separately-priced 3D brief |
| 3D product viewer | <model-viewer>, loaded on interaction | React Three Fiber + drei on a React island |
| Components, zero JS | daisyUI classes on native elements | Basecoat (vanilla JS widgets) |
| Accessible widgets (dialog, tabs, menu) | Native <dialog>/<details>/popover styled with daisyUI | Accessible Astro Components (+~9 KB CSS); Base UI or React Aria on an island; shadcn for a styled kit |
| Marketing flourishes | Magic UI (free, MIT) on an island | Motion Primitives patterns; retrofit reduced motion |
| Icons | Lucide via @lucide/astro or astro-icon | Tabler for gaps; Iconoir for finer strokes |
| Charts (any platform) | Chart.js | ECharts for dashboards/maps; Bklit or visx on React islands |
| Carousel | CSS scroll-snap row (patterns.md 12) | Embla once 9.0 stable ships; Swiper 14 only if the operator approves its index entry |
| Lottie animation | Muted video loop | dotLottie player, lazy-loaded below the fold |

## UI components

> Platform matters most here. daisyUI and Basecoat work everywhere. The React family (shadcn, Base UI, Magic UI) needs React, and costs JavaScript on Astro.

### Basecoat — `fork` · `ship`

- The shadcn/ui look rebuilt in plain HTML, Tailwind and a little vanilla JavaScript.
- **Why:** Gives clients the shadcn design language on WordPress or React-free Astro. Small enough to own outright, and with a single maintainer, a fork protects you if it stalls.
- **Install:** `npm i basecoat-css@1.0.2`
- **Licence:** MIT — Yes. Keep the MIT notice.
- **Reduced motion / a11y:** Manages aria-expanded, aria-selected and keyboard handling. No reduced-motion rules, so add one global rule.
- **Size:** JS 10.8 KB + CSS 21.9 KB gzip for every component; per-component files available. · **Build cost:** Low
- **Links:** https://basecoatui.com · https://github.com/hunvreus/basecoat

### Base UI — `fork` · `ship`

- Unstyled, accessible React primitives from the MUI team. The layer under shadcn.
- **Why:** The primitive layer the React world is converging on. Use it directly for bespoke widgets such as a combobox without fighting a design system.
- **Install:** `npm i @base-ui/react@1.8.0`
- **Licence:** MIT — Yes. Keep the MIT notice.
- **Reduced motion / a11y:** ARIA, keyboard and focus handled. Animation is yours to gate.
- **Size:** Import per component; the whole package is 143.5 KB gzip. · **Build cost:** Low via shadcn, Medium directly
- **Links:** https://base-ui.com · https://github.com/mui/base-ui

### daisyUI — `fork` · `ship`

- Pure-CSS component classes for Tailwind. No JavaScript.
- **Why:** Works the same on Astro, Next.js and WordPress, ships zero JavaScript, and gates its own transitions behind reduced motion better than anything else checked. The safest default while your platform is undecided.
- **Install:** `npm i -D daisyui@5.7.47  # Tailwind v4 plugin: @plugin "daisyui";`
- **Licence:** MIT — Yes. Keep the MIT notice in the built CSS or a third-party notices file.
- **Reduced motion / a11y:** 140 reduced-motion guards in its CSS. It styles native elements, so ARIA on tabs and dropdowns comes from your HTML.
- **Size:** CSS only; Tailwind emits just the classes you use. Never ship the full 97.7 KB file. · **Build cost:** Low
- **Links:** https://daisyui.com · https://github.com/saadeghi/daisyui

### Magic UI (free) — `fork` · `ship`

- Copy-paste animated marketing components in React, Tailwind and Motion.
- **Why:** Genuinely MIT hero and landing-page polish that clients notice. Only 5 of 79 components handle reduced motion, so each one needs a retrofit before it meets your bar.
- **Install:** `npx shadcn@4.21.1 add @magicui/<component>`
- **Licence:** MIT — Yes for the free components. Keep Magic UI Pro code out.
- **Reduced motion / a11y:** Wrap the app in MotionConfig reducedMotion="user" and guard canvas effects.
- **Size:** Copy-paste; Motion is the main runtime. · **Build cost:** Low to add, Medium to make compliant
- **Links:** https://magicui.design · https://github.com/magicuidesign/magicui

### React Aria Components — `fork` · `ship`

- Adobe's accessibility-first React hooks and components.
- **Why:** The strongest choice for complex, form-heavy builds: date pickers, comboboxes, multilingual and right-to-left sites. More than a brochure site needs.
- **Install:** `npm i react-aria-components@1.21.1`
- **Licence:** Apache-2.0 — Yes. Ship the Apache text, keep NOTICE.txt, and mark files you change.
- **Reduced motion / a11y:** Tested across devices and assistive tech; 30+ languages.
- **Size:** 267.7 KB gzip whole; tree-shakeable. · **Build cost:** Medium to High
- **Links:** https://react-aria.adobe.com · https://github.com/adobe/react-spectrum

### shadcn/ui — `fork` · `ship`

- A CLI that copies styled React and Tailwind components into your project. Built on Base UI by default since July 2026.
- **Why:** The fastest route to a consistent kit you own on React or Next.js. Private registries let your reusable pieces install into each client repo, which fits your licensing model. Little use on Astro without React islands, none on WordPress.
- **Watch:** class-variance-authority last released 2024-11-26, which fails your 12-month rule. Vendor it or grant an exception.
- **Install:** `npx shadcn@4.21.1 init  # in an Astro project with @astrojs/react`
- **Licence:** MIT — Yes. Copied files carry no header, so add the MIT notice to a third-party notices file. Its class-variance-authority dependency is Apache-2.0.
- **Reduced motion / a11y:** ARIA and keyboard come from Base UI. No reduced-motion handling; add a global rule.
- **Size:** Copy-paste, no runtime package. Runtime: Base UI, class-variance-authority, lucide-react. · **Build cost:** Low on React, Medium on Astro
- **Links:** https://ui.shadcn.com · https://github.com/shadcn-ui/ui

### Aceternity UI (free) — `reference` · `study-only`

- Animated React components served from a website registry, with no public repo.
- **Why:** Good for visual ideas. Its licence forbids redistributing source files, which collides with handing a client their repo. Study the effects and rebuild them with Motion.
- **Use note:** Licence forbids redistributing source files; rebuild effects with Motion.
- **Install:** `do not install (study only)`
- **Licence:** Website licence, not open source — Risky: a client repo containing the source is arguably redistribution.
- **Reduced motion / a11y:** 1 of 12 sampled components handles reduced motion.
- **Size:** Copy-paste; Motion runtime. · **Build cost:** Medium
- **Links:** https://ui.aceternity.com

### Origin UI / coss — `reference` · `study-only`

- Hundreds of copy-paste form and app components, kept as a legacy snapshot inside the coss repo.
- **Why:** A big library of patterns to study. The repo's root licence is AGPL. Only the apps/origin and apps/ui folders are MIT, so copy from those and never fork the whole repo.
- **Use note:** Root licence is AGPL; only apps/origin and apps/ui are MIT. Study patterns only.
- **Install:** `do not install (study only)`
- **Licence:** MIT in two folders; AGPL-3.0 elsewhere — Only code copied from the MIT folders, with the notice.
- **Reduced motion / a11y:** Inherits Radix; reduced motion not verified.
- **Size:** Copy-paste; runtime is a pinned Radix release candidate. · **Build cost:** Low to Medium
- **Links:** https://coss.com/origin · https://github.com/cosscom/coss

### Headless UI — `reference` · `ship`

- Tailwind Labs' small set of unstyled, accessible components.
- **Why:** Not much now. shadcn on Base UI covers more, and the Vue package fails your 12-month rule.
- **Install:** `npm i @headlessui/react@2.2.10`
- **Licence:** MIT — Yes. Keep the MIT notice.
- **Reduced motion / a11y:** ARIA and keyboard handled.
- **Size:** 61.5 KB gzip. · **Build cost:** Medium
- **Links:** https://headlessui.com · https://github.com/tailwindlabs/headlessui

### Motion Primitives — `reference` · `ship`

- 33 copy-paste React and Motion animation components.
- **Why:** The cleanest genuinely MIT animation set. Components are small and mostly depend only on Motion, so they are easier to keep fast than Magic UI. None handle reduced motion on their own.
- **Install:** `copy components from motion-primitives.com; runtime: motion@13.5.0`
- **Licence:** MIT — Yes. Keep the MIT notice.
- **Reduced motion / a11y:** 0 of 33 handle reduced motion; MotionConfig reducedMotion="user" is mandatory.
- **Size:** Copy-paste; Motion is the runtime. · **Build cost:** Low to Medium
- **Links:** https://motion-primitives.com · https://github.com/ibelick/motion-primitives

### Radix Primitives — `reference` · `ship`

- Unstyled, accessible React primitives.
- **Why:** Stable and behind a lot of existing code, but shadcn moved its default to Base UI in July 2026. Mostly useful when maintaining Radix-based code.
- **Install:** `npm i radix-ui@1.6.7`
- **Licence:** MIT — Yes. Keep the MIT notice.
- **Reduced motion / a11y:** ARIA, focus and keyboard handled.
- **Size:** Dialog 12.3 KB gzip; tree-shakeable. · **Build cost:** Medium directly
- **Links:** https://www.radix-ui.com/primitives · https://github.com/radix-ui/primitives

### React Bits — `reference` · `study-only`

- 213 animated React components, many of them WebGL.
- **Why:** Visually impressive, but 'MIT + Commons Clause' forbids sublicensing the components, so they cannot go into your reusable kit. Many effects pull in GSAP, three.js or the stale OGL.
- **Use note:** MIT + Commons Clause forbids sublicensing; cannot enter client repos or the kit.
- **Install:** `do not install (study only)`
- **Licence:** MIT + Commons Clause — A finished site, yes. Your reusable kit, no.
- **Reduced motion / a11y:** 68 of 213 handle reduced motion.
- **Size:** Copy-paste; heavy transitive dependencies. · **Build cost:** Medium to High
- **Links:** https://reactbits.dev · https://github.com/DavidHDev/react-bits

### Accessible Astro Components — `starter` · `ship`

- 24 zero-dependency Astro components: skip link, modal, tabs, accordion, form validation, reduced-motion toggle.
- **Why:** Serves your WCAG 2.2 AA floor directly with near-zero JavaScript. A natural accessibility layer under Starwind or daisyUI.
- **Use note:** Added because the Astro starter uses it (approved in the 2026-10-01 plan). The operator may veto.
- **Install:** `npm i accessible-astro-components@5.8.0`
- **Licence:** MIT — Yes. Keep the MIT notice.
- **Reduced motion / a11y:** Built to WCAG and ARIA practice per component; ships a reduced-motion toggle that respects the system setting.
- **Size:** No runtime dependencies. · **Build cost:** Low
- **Links:** https://accessible-astro-starter.incluud.dev/accessible-components/ · https://github.com/incluud/accessible-astro-components

## Animation, scroll and transitions

> Order of preference: CSS first, then the reveal snippet, then one JS library. Podium, your reference site, ships about 608 KB of JavaScript, hides the page behind a loading screen and never checks reduced motion. Copy its ideas, not its weight.

### anime.js v4 — `fork` · `ship`

- MIT animation engine: timelines, stagger, scroll-linking, text splitting.
- **Why:** Effectively an MIT-licensed GSAP, with no handover complications. It overlaps heavily with Motion, so pick one house library. You already have a fork, but it is unmodified; npm gives you everything.
- **Install:** `npm i animejs@4.5.0  # import subpaths: animejs/animation, animejs/utils`
- **Licence:** MIT — Yes. Keep the MIT notice.
- **Reduced motion / a11y:** Nothing automatic. Use createScope with a reduced-motion media query.
- **Size:** animate + stagger 14.2 KB gzip; full 42 KB. · **Build cost:** Low to Medium
- **Links:** https://animejs.com · https://github.com/juliangarnier/anime

### AutoAnimate — `fork` · `ship`

- One line to animate items being added, removed or reordered.
- **Why:** Cheap polish for filters, accordions and menus, and it respects reduced motion automatically. Same-page view transitions now do much of this natively.
- **Install:** `npm i @formkit/auto-animate@0.10.0`
- **Licence:** MIT — Yes. Keep the MIT notice.
- **Reduced motion / a11y:** Skips animation under reduced motion by default.
- **Size:** 3.1 KB gzip. · **Build cost:** Low
- **Links:** https://auto-animate.formkit.com · https://github.com/formkit/auto-animate

### Lenis — `fork` · `ship`

- Smooth-scroll layer over native scrolling.
- **Why:** The cheapest route to the 'premium agency' scroll feel. It does not help ordinary business sites, and it intercepts mouse-wheel input, so use it only when a client asks for that feel.
- **Install:** `npm i lenis@1.3.26  # pin >=1.3.26 for reduced motion`
- **Licence:** MIT — Yes. Keep the MIT notice.
- **Reduced motion / a11y:** Only v1.3.26 and later honour reduced motion. Pin at least 1.3.26.
- **Size:** 5.3 KB gzip. · **Build cost:** Low
- **Links:** https://lenis.dev · https://github.com/darkroomengineering/lenis

### Motion — `fork` · `ship`

- Animation library with a framework-free JS API plus React components. Formerly Framer Motion.
- **Why:** The only candidate that is first-class both without React and in React, so one skill set covers every platform you are considering. Tiny subsets: inView 0.4 KB, mini animate 3.8 KB. Use it when CSS cannot do the job.
- **Watch:** Recommended as your one house JavaScript animation library.
- **Install:** `npm i motion@13.5.0`
- **Licence:** MIT — Yes. Keep the MIT notice. Motion+ is a separate paid product.
- **Reduced motion / a11y:** Plain JS has no automatic reduced-motion check; gate with matchMedia. In React set MotionConfig reducedMotion="user".
- **Size:** inView 0.4 KB; animate + stagger + inView + scroll 22.5 KB gzip. · **Build cost:** Low to Medium
- **Links:** https://motion.dev · https://github.com/motiondivision/motion

### Astro view transitions — `reference` · `ship`

- Astro's built-in router: app-like navigation with view transitions and fallbacks.
- **Why:** Podium-style page transitions on Astro with accessibility handled for you. It switches animation off under reduced motion, announces page changes, and can keep a video playing across pages.
- **Watch:** Core if Astro wins.
- **Install:** `built into astro: import { ClientRouter } from 'astro:transitions'`
- **Licence:** MIT — Yes. Keep the MIT notice.
- **Reduced motion / a11y:** Disables view-transition animation under reduced motion and announces route changes.
- **Size:** About 5.6 KB gzip. · **Build cost:** Low to Medium; scripts must re-run on astro:page-load
- **Links:** https://docs.astro.build/en/guides/view-transitions/ · https://github.com/withastro/astro

### CSS scroll-driven animations — `reference` · `ship`

- CSS keyframes driven by scroll position or by an element moving through the viewport. No JavaScript.
- **Why:** Replaces most of what people install ScrollTrigger or AOS for: scrubbed reveals, parallax, progress bars. 0 KB and no main-thread cost. Podium already uses it for its hero parallax.
- **Install:** `no install: see references/patterns.md`
- **Licence:** Web platform — Nothing to retain; it is the client's own CSS.
- **Reduced motion / a11y:** A reduced-motion media query stops it completely. Gate with @supports so Firefox, which lacks it, gets static content.
- **Size:** 0 KB · **Build cost:** Low
- **Links:** https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline

### dotLottie player — `reference` · `ship`

- Maintained Lottie animation player using a WASM engine.
- **Why:** For illustrated or mascot animations a client already owns as Lottie files. Heavy, so lazy-load below the fold and self-host the WASM. A short muted video is often cheaper.
- **Install:** `npm i @lottiefiles/dotlottie-web@0.80.0  # self-host the WASM`
- **Licence:** MIT — Yes. The animation files are plain data the client keeps.
- **Reduced motion / a11y:** No reduced-motion logic; don't autoplay under reduce.
- **Size:** 13.5 KB JS + 487 KB WASM gzip. · **Build cost:** Medium
- **Links:** https://lottiefiles.com/dotlottie · https://github.com/LottieFiles/dotlottie-web

### Embla Carousel — `reference` · `ship`

- Small, dependency-free carousel engine; you supply markup and styles.
- **Why:** The best carousel when a client insists on one. Push back first: a CSS scroll-snap row needs no JavaScript.
- **Watch:** Stable 8.6.0 (2025-04-04) fails the 12-month rule, and 9.0 has been a release candidate since January 2026. Do not ship a pre-release to a client who owns it. Use the CSS scroll-snap row until 9.0 stable ships (library-scout, 2026-10-01).
- **Install:** `do not install yet: 8.6.0 fails the 12-month rule and 9.0 is still a release candidate; use the scroll-snap row (patterns.md 12)`
- **Licence:** MIT — Yes. Keep the MIT notice.
- **Reduced motion / a11y:** v9 adds an accessibility plugin. Never autoplay without a visible pause control.
- **Size:** 7.4 KB gzip. · **Build cost:** Medium
- **Links:** https://www.embla-carousel.com · https://github.com/davidjerleke/embla-carousel

### GSAP — `reference` · `ship`

- The most capable JS animation platform: timelines, ScrollTrigger, SplitText, Flip, MorphSVG. Every plugin is now free.
- **Why:** The fastest way to build Podium-level work for a rare premium client, and SplitText is the most accessible text splitter available. For ordinary business sites CSS covers most of it, and the licence complicates your handover.
- **Watch:** Not open source. Banned in no-code animation tools that compete with Webflow; Webflow may amend or terminate the terms.
- **Install:** `npm i gsap@3.15.0  # flagged licence: carve out of client sublicensing`
- **Licence:** Webflow 'Standard No Charge' licence — The client holds it directly under Webflow's terms. Your contract must carve GSAP out of the 'modify, sublicense, transfer' clause. Keep every @license header.
- **Reduced motion / a11y:** Nothing automatic; use gsap.matchMedia. ScrollSmoother ignores reduced motion entirely.
- **Size:** Core 27 KB; with ScrollTrigger 44.2 KB gzip. · **Build cost:** Medium
- **Links:** https://gsap.com · https://github.com/greensock/GSAP

### Locomotive Scroll v5 — `reference` · `study-only`

- Lenis plus data-scroll attributes for reveals and parallax.
- **Why:** Lenis plus CSS scroll-driven animation does the same with less code, and v5 locks you to Lenis 1.3.17, which ignores reduced motion.
- **Use note:** Pins Lenis 1.3.17, which ignores reduced motion. Use Lenis + CSS scroll-driven animation.
- **Install:** `do not install (study only)`
- **Licence:** MIT — Yes. Keep both MIT notices.
- **Reduced motion / a11y:** Parallax runs regardless of reduced motion.
- **Size:** 8.6 KB gzip. · **Build cost:** Low to Medium
- **Links:** https://scroll.locomotive.ca · https://github.com/locomotivemtl/locomotive-scroll

### View Transitions API — `reference` · `ship`

- Browser-native animated transitions between page states and between pages.
- **Why:** Two lines of CSS give a static multi-page site page transitions without a router, the job Barba and Swup used to do. Browsers without support just navigate normally.
- **Install:** `no install: see references/patterns.md`
- **Licence:** Web platform — Nothing to retain.
- **Reduced motion / a11y:** Browsers do not switch it off for reduced motion. You add one CSS rule.
- **Size:** 0 KB · **Build cost:** Low for a fade, Medium for shared-element morphs
- **Links:** https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API

## WebGL, 3D and backgrounds

> Most clients should get the CSS background, not WebGL. WebGL is justified for a product buyers want to turn around (model-viewer) or a brand-led hero (Paper Shaders). A custom three.js scene is an estimated 20 to 60 hours, so quote it as a separate line item.

### Babylon.js — `fork` · `ship`

- A full 3D and game engine for the web.
- **Why:** No case for it on small-business sites. Worth knowing it exists.
- **Install:** `npm i @babylonjs/core@9.29.0`
- **Licence:** Apache-2.0 — Yes. Keep the Apache licence.
- **Reduced motion / a11y:** Canvas; nothing automatic.
- **Size:** 1.7 MB gzip whole. · **Build cost:** High
- **Links:** https://www.babylonjs.com · https://github.com/BabylonJS/Babylon.js

### React Three Fiber + drei — `fork` · `ship`

- A React renderer for three.js, plus drei's ready-made helpers.
- **Why:** Only if React wins and a project has a real 3D brief. It then cuts build time well below plain three.js.
- **Install:** `npm i three@0.186.1 @react-three/fiber@9.8.1 @react-three/drei@10.7.9`
- **Licence:** MIT — Yes. Keep both MIT notices.
- **Reduced motion / a11y:** As three.js.
- **Size:** 55.7 KB gzip on top of three.js. · **Build cost:** High
- **Links:** https://docs.pmnd.rs/react-three-fiber · https://github.com/pmndrs/react-three-fiber

### three.js — `fork` · `ship`

- The standard WebGL 3D engine.
- **Why:** Nearly every other 3D option runs on it, so it is worth understanding. A custom scene is rarely justified on a fixed-price site: about 180 KB gzip and weeks of work at your hours.
- **Install:** `npm i three@0.186.1`
- **Licence:** MIT — Yes. Keep the MIT notice.
- **Reduced motion / a11y:** Canvas content is invisible to screen readers; stop the render loop under reduced motion.
- **Size:** 180.6 KB gzip. · **Build cost:** High
- **Links:** https://threejs.org · https://github.com/mrdoob/three.js

### CSS animated background — `reference` · `ship`

- Two to four blurred radial-gradient shapes moved with CSS transforms. No JavaScript.
- **Why:** Gives most clients the 'alive' hero they want for under 1 KB of CSS and about 1 to 2 hours, with no WebGL cost at all. Try this before any shader library.
- **Install:** `no install: see references/patterns.md`
- **Licence:** Your own code — The client owns it outright.
- **Reduced motion / a11y:** Wrap the animation in a no-preference reduced-motion query.
- **Size:** Under 1 KB CSS · **Build cost:** Low
- **Links:** https://developer.mozilla.org/en-US/docs/Web/CSS/@property

### <model-viewer> — `reference` · `ship`

- A web component that shows a 3D product model the visitor can turn around.
- **Why:** The one 3D feature a small business might genuinely need: a product buyers want to inspect. One HTML tag on any platform; most of the cost is preparing the model, not the code.
- **Install:** `npm i @google/model-viewer@4.3.1  # load on interaction`
- **Licence:** Apache-2.0 — Yes. Keep the Apache licence.
- **Reduced motion / a11y:** Its alt text becomes the accessible name. Don't enable auto-rotate.
- **Size:** About 284 KB gzip with three.js; load on click behind a poster image. · **Build cost:** Low to Medium
- **Links:** https://modelviewer.dev · https://github.com/google/model-viewer

## Text effects

> Splitting text into letters breaks screen readers unless the full sentence stays readable. SplitType and Splitting.js fail that test and are excluded.

### Number Flow — `fork` · `ship`

- Animated number transitions: digits roll for stats, prices and counters.
- **Why:** The stats row ('25 years, 1,200 clients') appears on many business sites, and this does it accessibly in about 5 KB. Screen readers hear the final number, not rolling digits.
- **Watch:** Only animate real numbers. A counter invites inventing statistics.
- **Install:** `npm i number-flow@0.6.2  # React: @number-flow/react`
- **Licence:** MIT — Yes. Keep the MIT notice.
- **Reduced motion / a11y:** Respects reduced motion by default and exposes the formatted value as its accessible name.
- **Size:** 5.1 KB gzip. · **Build cost:** Low
- **Links:** https://number-flow.barvian.me · https://github.com/barvian/number-flow

## Icons

> Default to Lucide and fill gaps with Tabler. Both sit on the same 24px grid, so they mix cleanly.

### Lucide — `fork` · `ship`

- A consistent 24px outline icon set, 1,857 icons.
- **Why:** First-party packages for vanilla JS, React, Astro and static SVG, so the same set survives whichever platform wins. Hides decorative icons from screen readers by default. Recommended default.
- **Install:** `npm i @lucide/astro@1.49.0  # React islands: lucide-react@1.49.0`
- **Licence:** ISC, plus MIT for Feather-derived icons — Yes. Keep both notices in a third-party notices file.
- **Reduced motion / a11y:** aria-hidden by default unless you give it a label.
- **Size:** About 0.4 KB per icon in React; 0 KB in Astro. · **Build cost:** Low
- **Links:** https://lucide.dev · https://github.com/lucide-icons/lucide

### Tabler Icons — `fork` · `ship`

- A large MIT icon set, 6,220 icons, outline and filled.
- **Why:** The fallback when Lucide lacks an industry-specific icon. Same 24px, 2px-stroke grid, so the two mix cleanly.
- **Install:** `npm i @tabler/icons@3.48.0  # SVGs; React: @tabler/icons-react`
- **Licence:** MIT — Yes. Keep the MIT notice.
- **Reduced motion / a11y:** Add aria-hidden yourself on decorative icons.
- **Size:** About 0.4 KB per icon. · **Build cost:** Low
- **Links:** https://tabler.io/icons · https://github.com/tabler/tabler-icons

### astro-icon (Iconify) — `reference` · `ship`

- Build-time icon inlining for Astro from 238 icon sets. No client JavaScript.
- **Why:** One component for Lucide, Tabler and others on Astro. The trap: each set carries its own licence, and about 70 of the 238 need attribution, are copyleft or non-commercial. Use an allow-list.
- **Watch:** Core if Astro wins. Avoid @iconify/react, last released 2025-09-15.
- **Install:** `npm i astro-icon@1.2.0 @iconify-json/lucide @iconify-json/tabler`
- **Licence:** MIT (tool); each icon set has its own — Yes for the tool. Record the licence of each set used.
- **Reduced motion / a11y:** Set aria-hidden on decorative icons.
- **Size:** 0 KB client JavaScript. · **Build cost:** Low
- **Links:** https://www.astroicon.dev · https://github.com/natemoo-re/astro-icon

### Iconoir — `reference` · `ship`

- An MIT outline set with a lighter 1.5px stroke, 1,671 icons.
- **Why:** For a client whose brand wants finer lines. Not needed if Lucide and Tabler cover the job.
- **Install:** `npm i iconoir@7.12.1`
- **Licence:** MIT — Yes. Keep the MIT notice.
- **Reduced motion / a11y:** No default aria-hidden.
- **Size:** About 0.6 KB per icon. · **Build cost:** Low
- **Links:** https://iconoir.com · https://github.com/iconoir-icons/iconoir

## Charts

> Brochure sites rarely need charts. The clients that do: solar and energy installers, property, NGOs, consultancies, training providers, tourism and events.

### Bklit UI — `fork` · `ship`

- Polished React chart components on visx and Motion, installed through the shadcn registry.
- **Why:** The best-looking charts here, and the source lands in your repo so you can edit it. But charts have no keyboard access, it installs a visx pre-release, and its stat-card items pull in a paid, non-transferable icon set. Skip those.
- **Install:** `npx shadcn@4.21.1 add @bklit/<chart>  # never the stat-card items`
- **Licence:** MIT (charts); Studio is proprietary — Yes for registry code. Install with the CLI rather than copying from Studio.
- **Reduced motion / a11y:** No keyboard handling at all. Every chart needs a caption and a visually hidden data table.
- **Size:** Per chart unmeasured; Motion and visx at runtime. · **Build cost:** Medium
- **Links:** https://ui.bklit.com · https://github.com/bklit/bklit-ui

### Chart.js — `fork` · `ship`

- Framework-agnostic canvas charts.
- **Why:** The one chart library that works the same on Astro, React and WordPress, so the safe default while the platform is undecided.
- **Watch:** Its last release passes your 12-month rule only until 2026-10-13. Commits are active.
- **Install:** `npm i chart.js@4.5.1`
- **Licence:** MIT — Yes. Keep the MIT notice.
- **Reduced motion / a11y:** Canvas is not accessible by default: add a role, label and fallback table. Set animation off under reduced motion.
- **Size:** 66.8 KB gzip whole; register only what you use. · **Build cost:** Low to Medium
- **Links:** https://www.chartjs.org · https://github.com/chartjs/Chart.js

### Apache ECharts — `fork` · `ship`

- A heavyweight chart and map library.
- **Why:** Strongest for dashboards and maps, with the best built-in screen-reader description, which is off by default. Overkill for brochure sites.
- **Install:** `npm i echarts@6.1.0  # import from echarts/core`
- **Licence:** Apache-2.0 — Yes. Keep the licence and third-party notices.
- **Reduced motion / a11y:** Turn on its aria option for auto-generated descriptions and colour-blind patterns.
- **Size:** 359 KB gzip whole; tree-shakeable via echarts/core. · **Build cost:** Medium
- **Links:** https://echarts.apache.org · https://github.com/apache/echarts

### visx — `fork` · `ship`

- Airbnb's low-level D3 and React chart primitives.
- **Why:** The foundation under Bklit. Building charts from primitives costs too many hours for fixed-price work.
- **Install:** `npm i @visx/shape@4.0.0 @visx/scale@4.0.0`
- **Licence:** MIT — Yes. Keep the MIT notice.
- **Reduced motion / a11y:** None built in.
- **Size:** Modular; a shape module is 10.5 KB gzip. · **Build cost:** High
- **Links:** https://airbnb.io/visx · https://github.com/airbnb/visx

## Considered and excluded

Do not use these; reasons from the 2026-10-01 research. A library-scout run is needed to revisit any of them.

- **Pico CSS** (UI components): No release since 2025-03-15. Otherwise ideal for simple sites, so re-check when it ships.
- **Kadence Blocks, GenerateBlocks** (UI components): GPL. Derivative work must also be GPL, which collides with keeping your reusable pieces under your own licence.
- **Animate UI** (UI components): 'MIT + Commons Clause', not genuinely MIT; no activity since 2025-12-31.
- **Shoelace** (UI components): Superseded by Web Awesome; last release 2025-03-11.
- **Paid tiers** (UI components): Magic UI Pro, Aceternity Pro, Starwind Pro, React Bits Pro, Flowbite Pro, Web Awesome Pro, Tailwind Plus. Usually per-developer licences you cannot hand to a client.
- **Barba.js** (Animation, scroll and transitions): No release since 2024-08-12. Swup and native view transitions replace it.
- **lottie-web** (Animation, scroll and transitions): Last release 2025-05-21. Use the dotLottie player.
- **Rive** (Animation, scroll and transitions): Free exports carry a Rive splash screen; removing it needs a paid seat, and the client can only edit in Rive's editor.
- **Theatre.js** (Animation, scroll and transitions): Stalled since 2024, and its editor is AGPL.
- **Splide** (Animation, scroll and transitions): No release since 2022.
- **AOS** (Animation, scroll and transitions): Unmaintained since 2018. The reveal snippet does the same in 227 bytes.
- **ScrollReveal** (Animation, scroll and transitions): GPL plus a paid commercial licence, and unmaintained.
- **Typed.js, TypeIt** (Animation, scroll and transitions): Typed.js moved to GPL-3.0 in v3.0.0 (2026-01-24); TypeIt is GPL with a paid commercial licence.
- **OGL** (WebGL, 3D and backgrounds): No release since 2025-01-27 and no LICENSE file. Study it, don't ship it.
- **curtains.js** (WebGL, 3D and backgrounds): Unmaintained; its successor targets WebGPU, which is not yet available in every major browser.
- **Spline** (WebGL, 3D and backgrounds): Proprietary runtime; free exports are watermarked, and the client needs a Spline account to edit.
- **SplitType** (Text effects): No release since 2023, and no screen-reader handling.
- **Splitting.js** (Text effects): No release since 2024-05-31, and no screen-reader handling. Its CSS-variable pattern is worth studying.
- **Motion+ text components** (Text effects): Paid ($399 one-time). Number Flow and GSAP cover the same ground free.
- **Phosphor Icons** (Icons): No npm release since 2025-05-22. Copying its MIT SVG files in directly sidesteps the rule.
- **Heroicons** (Icons): Last release 2024-11-18. Same workaround: copy the MIT SVGs.
- **uPlot** (Charts): Last release 2025-03-14.
- **Observable Plot** (Charts): Last release 2025-02-14.
