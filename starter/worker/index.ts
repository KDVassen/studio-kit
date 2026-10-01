// HUMAN REVIEW GATE (client-build rule 11): this Worker stores personal information.
// Show every change to the operator line by line before deploying.
//
// Static files are served by Cloudflare's asset layer before this code runs; only
// requests that match no file (here: POST /api/enquiry) reach the Worker.
//
// Defences, strongest first: same-origin check, atomic per-sender rate limit, honeypot.
// The elapsed-time check is a weak extra signal: it only flags enquiries as suspect, never drops them.

import { site } from '../src/site.config';

interface Env {
  ASSETS: Fetcher;
  DB: D1Database;
  RATE_SALT?: string; // secret: `npx wrangler secret put RATE_SALT`; locally in .dev.vars
}

type Fields = { name: string; email: string; business: string; message: string };

const MAX_BODY = 20_000;           // bytes
const MIN_ELAPSED_MS = 3_000;      // a person can't read and fill the form faster than this
const RATE_WINDOW_MS = 600_000;    // 10 minutes
const RATE_MAX = 5;                // enquiries per window per sender
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const RETENTION_MS = Math.round(site.privacy.retentionMonths * 30.4375) * 86_400_000;
const FORM_TYPES = ['application/x-www-form-urlencoded', 'multipart/form-data'];
const SECURITY_HEADERS = {
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Content-Security-Policy': "default-src 'none'; style-src 'unsafe-inline'; frame-ancestors 'none'; form-action 'self'; base-uri 'none'",
  'Cache-Control': 'no-store',
};

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    if (url.pathname === '/api/enquiry') {
      if (request.method !== 'POST') {
        return new Response('Method not allowed', { status: 405, headers: { Allow: 'POST', ...SECURITY_HEADERS } });
      }
      try {
        return await handleEnquiry(request, env);
      } catch (err) {
        console.error('enquiry failed', err instanceof Error ? err.message : 'unknown error'); // server-side only
        return reply(request, 500, { ok: false }, page('Something went wrong',
          '<p>Your enquiry did not send. Please try again in a moment, or use WhatsApp or email instead.</p>'));
      }
    }
    return env.ASSETS.fetch(request);
  },

  // Daily housekeeping (cron in wrangler.jsonc), so the privacy notice's deletion promises hold
  // even on a site that receives no enquiries.
  async scheduled(_controller: ScheduledController, env: Env): Promise<void> {
    const now = Date.now();
    await env.DB.batch([
      env.DB.prepare('DELETE FROM rate_events WHERE ts < ?1').bind(now - 86_400_000),
      env.DB.prepare('DELETE FROM enquiries WHERE kept = 0 AND created_at < ?1').bind(now - RETENTION_MS),
    ]);
  },
} satisfies ExportedHandler<Env>;

async function handleEnquiry(request: Request, env: Env): Promise<Response> {
  // Only this site's own pages may submit.
  const origin = request.headers.get('Origin');
  const fetchSite = request.headers.get('Sec-Fetch-Site');
  if ((origin && origin !== new URL(request.url).origin) || fetchSite === 'cross-site') {
    return new Response('Forbidden', { status: 403, headers: SECURITY_HEADERS });
  }

  const type = (request.headers.get('content-type') ?? '').split(';')[0].trim().toLowerCase();
  if (!FORM_TYPES.includes(type)) return new Response('Unsupported media type', { status: 415, headers: SECURITY_HEADERS });
  const length = request.headers.get('content-length');
  if (length === null) return new Response('Length required', { status: 411, headers: SECURITY_HEADERS });
  if (Number(length) > MAX_BODY) return new Response('Too large', { status: 413, headers: SECURITY_HEADERS });

  if (!env.RATE_SALT) {
    // Fail closed: without the secret, stored IP hashes could be reversed.
    console.error('RATE_SALT secret is not set');
    return reply(request, 500, { ok: false }, page('Something went wrong',
      '<p>Your enquiry did not send. Please use WhatsApp or email instead.</p>'));
  }

  const form = await request.formData();
  const get = (k: string) => { const v = form.get(k); return typeof v === 'string' ? v.trim() : ''; };

  // Honeypot: bots get a normal-looking success and nothing is stored. Counted, never with personal data.
  if (get('hp_x7')) { console.log('enquiry: honeypot tripped'); return success(request); }

  const fields: Fields = {
    name: get('name').slice(0, 100),
    email: get('email').slice(0, 254),
    business: get('business').slice(0, 120),
    message: get('message').slice(0, 2000),
  };
  const errors = validate(fields);
  if (Object.keys(errors).length) {
    const list = Object.values(errors).map((e) => `<li>${escapeHtml(e)}</li>`).join('');
    return reply(request, 422, { ok: false, errors }, page('Please check the form',
      `<ul>${list}</ul><p>Use your browser's back button to fix these; your answers should still be there.</p>`));
  }

  // Elapsed time is measured by the visitor's own browser clock, so device clock errors can't skew it.
  // Missing (JavaScript off) is normal. Too fast is only a hint: the enquiry is kept, flagged suspect.
  const elapsed = Number(get('elapsed'));
  const suspect = get('elapsed') !== '' && Number.isFinite(elapsed) && elapsed < MIN_ELAPSED_MS ? 1 : 0;

  const now = Date.now();
  const sender = await sha256(`${senderKey(request.headers.get('CF-Connecting-IP') ?? 'unknown')}|${new Date(now).toISOString().slice(0, 10)}|${env.RATE_SALT}`);

  // Atomic: the rate-event row is inserted only if the sender is under the limit, so parallel requests can't slip past.
  const gate = await env.DB
    .prepare('INSERT INTO rate_events (hash, ts) SELECT ?1, ?2 WHERE (SELECT COUNT(*) FROM rate_events WHERE hash = ?1 AND ts > ?3) < ?4')
    .bind(sender, now, now - RATE_WINDOW_MS, RATE_MAX)
    .run();
  if (gate.meta.changes !== 1) {
    return reply(request, 429, { ok: false }, page('Too many messages',
      '<p>Please wait a few minutes and try again, or use WhatsApp or email instead.</p>'));
  }

  await env.DB
    .prepare('INSERT INTO enquiries (created_at, name, email, business, message, suspect) VALUES (?1, ?2, ?3, ?4, ?5, ?6)')
    .bind(now, fields.name, fields.email, fields.business || null, fields.message, suspect)
    .run();
  return success(request);
}

function validate(f: Fields): Record<string, string> {
  const errors: Record<string, string> = {};
  if (!f.name) errors.name = 'Add your name.';
  if (!f.email) errors.email = 'Add an email address so we can reply.';
  else if (!EMAIL_RE.test(f.email)) errors.email = 'Enter an email address like name@example.com.';
  if (f.message.length < 10) errors.message = 'Tell us a little about what you need (at least 10 characters).';
  return errors;
}

// IPv6 visitors are limited per /64 network (one household or device), so rotating addresses inside it doesn't help.
function senderKey(ip: string): string {
  if (!ip.includes(':')) return ip;
  const [head, tail = ''] = ip.split('::');
  const h = head ? head.split(':') : [];
  const t = tail ? tail.split(':') : [];
  const full = ip.includes('::') ? [...h, ...Array(8 - h.length - t.length).fill('0'), ...t] : h;
  return full.slice(0, 4).map((x) => x.toLowerCase().replace(/^0+(?=.)/, '')).join(':') + '::/64';
}

function wantsJson(request: Request): boolean {
  return (request.headers.get('accept') ?? '').includes('application/json');
}

function success(request: Request): Response {
  if (wantsJson(request)) return Response.json({ ok: true }, { headers: SECURITY_HEADERS });
  return new Response(null, { status: 303, headers: { Location: new URL('/enquiry-sent/', request.url).toString(), ...SECURITY_HEADERS } });
}

function reply(request: Request, status: number, json: unknown, html: string): Response {
  if (wantsJson(request)) return Response.json(json, { status, headers: SECURITY_HEADERS });
  return new Response(html, { status, headers: { 'Content-Type': 'text/html; charset=utf-8', ...SECURITY_HEADERS } });
}

function page(title: string, body: string): string {
  return `<!doctype html><html lang="en-ZA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>${escapeHtml(title)}</title><style>body{font:18px/1.6 system-ui,sans-serif;color:#15171A;background:#FAF9F7;max-width:40rem;margin:4rem auto;padding:0 1rem}a{color:#0B6B73;text-decoration:underline}</style></head><body><main><h1>${escapeHtml(title)}</h1>${body}<p><a href="/#contact">Back to the contact form</a></p></main></body></html>`;
}

function escapeHtml(s: string): string {
  return s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!);
}

async function sha256(text: string): Promise<string> {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
}
