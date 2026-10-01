# Patterns

Small, licence-free building blocks. Each one respects reduced motion and keeps content visible if JavaScript fails. The Astro starter already includes the first four.

## 1. Global reduced-motion safety net

Catches CSS transitions and keyframes only. It does **not** stop JavaScript animation libraries; see pattern 7 for those.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: .01ms !important;
    scroll-behavior: auto !important;
  }
}
```

## 2. Reveal on scroll (227 bytes, works in every browser)

Never use on the hero or the LCP element.

```css
@media (prefers-reduced-motion: no-preference) {
  .js [data-reveal] { opacity: 0; transform: translateY(8px); transition: opacity .32s ease-out, transform .32s ease-out; }
  .js [data-reveal].is-visible { opacity: 1; transform: none; }
}
```

```js
// One module script at the end of <body>. The .js class is added here, in the same
// script that reveals things, so a script failure can never leave content hidden.
document.documentElement.classList.add('js');
const io = new IntersectionObserver((entries) => {
  for (const e of entries) if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); }
}, { rootMargin: '0px 0px -10% 0px' });
document.querySelectorAll('[data-reveal]').forEach((el) => io.observe(el));
```

## 3. Page transitions between pages (0 KB)

Chrome/Edge 126+ and Safari 18.2+ animate; other browsers navigate normally.

```css
@view-transition { navigation: auto; }

/* Browsers do not disable view transitions for reduced motion. You must. */
@media (prefers-reduced-motion: reduce) {
  ::view-transition-group(*), ::view-transition-old(*), ::view-transition-new(*) { animation: none !important; }
}
```

Shared-element morph: give the same element on both pages the same unique name, e.g. `style="view-transition-name: project-hero"`. Names must be unique per page.

Use Astro's `<ClientRouter />` instead only when state must survive navigation (a playing video via `transition:persist`). Scripts then re-run on `astro:page-load`, not on load.

## 4. Scroll-driven reveal and progress bar (0 KB)

Firefox lacks `animation-timeline`, so everything sits behind `@supports` and Firefox users get static, visible content.

```css
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    [data-scroll-reveal] {
      animation: sk-reveal linear both;
      animation-timeline: view();
      animation-range: entry 0% cover 30%;
    }
    @keyframes sk-reveal { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: none; } }

    .sk-progress {                                   /* <div class="sk-progress" aria-hidden="true"></div> */
      position: fixed; inset: 0 0 auto 0; height: 3px; z-index: 50;
      background: var(--accent); transform-origin: 0 50%;
      animation: sk-grow linear both; animation-timeline: scroll(root);
    }
    @keyframes sk-grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
  }
}
```

Parallax: give each column a different `translateY` range in its keyframes, same `animation-timeline: view()`.

## 5. Animated hero background without WebGL (< 1 KB)

```html
<div class="sk-bg" aria-hidden="true"><span></span><span></span><span></span></div>
```

```css
.sk-bg { position: absolute; inset: 0; overflow: hidden; z-index: -1; pointer-events: none; }
.sk-bg span { position: absolute; width: 40vmax; aspect-ratio: 1; border-radius: 50%; filter: blur(60px); opacity: .45;
  background: radial-gradient(circle, var(--blob-1), transparent 70%); left: -10%; top: -20%; }
.sk-bg span:nth-child(2) { background: radial-gradient(circle, var(--blob-2), transparent 70%); left: 55%; top: 10%; }
.sk-bg span:nth-child(3) { background: radial-gradient(circle, var(--blob-3), transparent 70%); left: 20%; top: 55%; }
@media (prefers-reduced-motion: no-preference) {
  .sk-bg:not(.is-paused) span { animation: sk-drift 24s ease-in-out infinite alternate; }
  .sk-bg span:nth-child(2) { animation-duration: 30s; animation-direction: alternate-reverse; }
  @keyframes sk-drift { to { transform: translate(10vmax, 6vmax) scale(1.15); } }
}
```

- **WCAG 2.2.2 (Pause, Stop, Hide):** motion that starts automatically and lasts more than 5 seconds needs a way to pause it. Include pattern 6, or limit the drift to one pass of 5 seconds or less.
- Compute text contrast against the **lightest** point the blobs reach, not the base colour.
- `filter: blur` is costly on low-end phones; keep it to three blobs.

## 6. Pause control for ambient motion

```html
<button type="button" class="sk-pause" aria-pressed="false" data-target=".sk-bg">Pause animation</button>
```

```js
for (const b of document.querySelectorAll('.sk-pause')) {
  b.addEventListener('click', () => {
    const on = b.getAttribute('aria-pressed') !== 'true';
    b.setAttribute('aria-pressed', String(on));
    b.textContent = on ? 'Play animation' : 'Pause animation';
    document.querySelector(b.dataset.target)?.classList.toggle('is-paused', on);
  });
}
```

Hide the button under reduced motion (nothing is moving): `@media (prefers-reduced-motion: reduce) { .sk-pause { display: none; } }`.

## 7. JavaScript animation, gated so reduced-motion visitors download nothing

```js
// Astro <script> (bundled module). The import happens only when motion is allowed.
const motionOK = window.matchMedia('(prefers-reduced-motion: no-preference)').matches;
if (motionOK) {
  const { animate, inView, stagger } = await import('motion');
  inView('[data-stagger]', (el) => {
    animate(el.children, { opacity: [0, 1], y: [8, 0] }, { delay: stagger(0.06), duration: 0.32 });
  });
}
```

Never set the hidden start state in CSS for JS-driven animation: if the import fails or motion is reduced, content must already be visible. The same gate applies to anime.js (`createScope({ mediaQueries: { reduceMotion: '(prefers-reduced-motion)' } })`), GSAP (`gsap.matchMedia()`), three.js render loops, Lottie and shader backgrounds.

## 8. Split-text headline that screen readers read as one sentence

```astro
---
const { text } = Astro.props;
const words = text.split(' ');
---
<h1 class="sk-split">
  <span class="vh">{text}</span>
  <span aria-hidden="true">{words.map((w, i) => <span class="w" style={`--i:${i}`}>{w} </span>)}</span>
</h1>
```

```css
@media (prefers-reduced-motion: no-preference) {
  .sk-split .w { display: inline-block; animation: sk-rise .45s ease-out both; animation-delay: calc(var(--i) * 60ms); }
  /* Transform only, no opacity: a headline is usually the LCP element, and an element
     starting at opacity 0 is not counted as painted, which delays LCP. */
  @keyframes sk-rise { from { transform: translateY(.35em); } }
}
```

`.vh` is the visually-hidden utility in the starter's global CSS.

## 9. Astro islands

```astro
---
import Pricing from '../components/Pricing.astro';          // static: 0 KB JS
import Booking from '../islands/Booking.tsx';                // React island
import Faq from '../components/Faq.astro';                   // native <details>
---
<Pricing />
<Faq />
<Booking client:visible />   <!-- hydrates only when scrolled into view -->
```

After adding an island, build and check that page's JS against the 30 KB gzip budget.

## 10. 3D model, loaded only on request

```astro
<figure class="sk-3d">
  <img src="/products/chair-poster.webp" width="800" height="600" alt="Oak dining chair, front three-quarter view">
  <button type="button" data-load-3d="/products/chair.glb" data-alt="Oak dining chair, rotatable 3D model">View in 3D</button>
</figure>
<script>
  for (const b of document.querySelectorAll('[data-load-3d]')) {
    b.addEventListener('click', async () => {
      await import('@google/model-viewer');
      const mv = document.createElement('model-viewer');
      mv.setAttribute('src', b.dataset.load3d);
      mv.setAttribute('alt', b.dataset.alt);
      mv.setAttribute('camera-controls', '');
      b.closest('figure').replaceChildren(mv);
      mv.focus();
    }, { once: true });
  }
</script>
```

No `auto-rotate`: it is motion the visitor did not ask for.

## 11. Enquiry form

Use the starter's form (`starter/src/components/EnquiryForm.astro` + `starter/worker/`). It already does server-side validation, a honeypot, rate limiting, the POPIA s18 notice at the form, and works with JavaScript off. Any change to it touches personal data and is a **human line-by-line review gate** (client-build rule 11).

## 12. Carousel without a library: a scroll-snap row

The default for galleries, testimonials and "recent work". Native touch swipe in about 96% of browsers, keyboard-scrollable, nothing to license or upgrade. A library only for looping, thumbnails or effects this cannot do: Swiper 14 (in the index; about 25 KB, build your own pause button), or Embla once 9.0 is stable.

```astro
<section class="sk-snap" aria-labelledby="work-h">
  <h2 id="work-h">Recent work</h2>
  <div class="sk-snap__track" tabindex="0" role="region" aria-label="Recent work, scrollable">
    <ul role="list">
      <li><figure><img src="/work/1.webp" width="800" height="600" alt="[Describe the image]" loading="lazy"><figcaption>[Caption]</figcaption></figure></li>
      <!-- more <li> -->
    </ul>
  </div>
  <div class="sk-snap__controls" hidden>
    <button type="button" class="btn" data-snap="prev">Previous</button>
    <button type="button" class="btn" data-snap="next">Next</button>
  </div>
</section>
```

```css
.sk-snap__track { overflow-x: auto; scroll-snap-type: x mandatory; overscroll-behavior-x: contain; }
.sk-snap__track ul { display: grid; grid-auto-flow: column; grid-auto-columns: min(85%, 24rem); gap: 1rem; margin: 0; padding: 0 0 .75rem; }
.sk-snap__track li { scroll-snap-align: start; }
@media (prefers-reduced-motion: no-preference) { .sk-snap__track { scroll-behavior: smooth; } }
/* Keep the scrollbar visible: it tells people the row scrolls. */
```

```js
// Buttons are progressive enhancement: hidden until this runs, so no-JS visitors never see dead controls.
for (const root of document.querySelectorAll('.sk-snap')) {
  const track = root.querySelector('.sk-snap__track');
  const controls = root.querySelector('.sk-snap__controls');
  const prev = root.querySelector('[data-snap="prev"]');
  const next = root.querySelector('[data-snap="next"]');
  const step = () => track.querySelector('li')?.getBoundingClientRect().width ?? track.clientWidth;
  const update = () => {
    prev.disabled = track.scrollLeft <= 1;
    next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 1;
  };
  prev.addEventListener('click', () => track.scrollBy({ left: -step() }));   // CSS scroll-behavior decides smooth vs instant
  next.addEventListener('click', () => track.scrollBy({ left: step() }));
  track.addEventListener('scroll', update, { passive: true });
  controls.hidden = false;
  update();
}
```

**Auto-advance: avoid.** Ask the client whether they really need it; without it there is nothing to pause and WCAG 2.2.2 does not apply. If it is a firm requirement, write it per project: start only inside the `prefers-reduced-motion: no-preference` gate, advance no faster than every 5 seconds, stop on hover, focus, pointer down and hidden tab, and include pattern 6's visible pause button. Have qa-auditor check it.
