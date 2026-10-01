import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';
import { site } from './src/site.config';

// Pages ship no JavaScript unless an island asks for it. React is available for islands only.
export default defineConfig({
  site: site.url,
  trailingSlash: 'always',
  integrations: [react(), sitemap({ filter: (page) => !page.includes('/enquiry-sent/') })],
  vite: { plugins: [tailwindcss()] },
  // Shiki's inline styles break under CSP. Brochure sites rarely show code; use Prism if one does.
  markdown: { syntaxHighlight: false },
  security: {
    // Astro hashes its own inline scripts and styles into a CSP <meta> tag. Anything else must be listed here.
    // Never add 'unsafe-inline'. Inline style="" attributes are blocked, so style with classes.
    csp: {
      algorithm: 'SHA-256',
      scriptDirective: { resources: ["'self'", 'https://static.cloudflareinsights.com'] },
      styleDirective: { resources: ["'self'"] },
    },
  },
});
