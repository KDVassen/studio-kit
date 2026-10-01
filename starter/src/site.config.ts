// Every client fact lives here. Components never hard-code a name, contact detail, price or date.
// Values in [SQUARE BRACKETS] are visible placeholders: replace them, never invent them.

export const site = {
  name: '[CLIENT NAME]',
  legalName: '[LEGAL NAME]',
  tagline: '[ONE-LINE PROMISE]',
  description: '[ONE-SENTENCE DESCRIPTION FOR SEARCH RESULTS]',
  // Reserved .invalid domain until the client's real domain is known.
  url: 'https://example.invalid',
  // schema.org type for structured data, e.g. 'Electrician', 'BeautySalon', 'ProfessionalService'.
  businessType: 'LocalBusiness',
  // Social share image path in /public (1200×630). Empty = no og:image tag.
  ogImage: '',
  address: '[BUSINESS ADDRESS]',
  area: '[AREA SERVED]',
  hours: '[HOURS]',

  contact: {
    // Digits only with country code, e.g. 27821234567. Leave '' until supplied: no link is rendered.
    whatsapp: '',
    whatsappDisplay: '[WHATSAPP]',
    email: '',
    emailDisplay: '[EMAIL]',
  },

  privacy: {
    infoOfficer: '[INFORMATION OFFICER NAME AND EMAIL]',
    // Single source of truth: the privacy page states it and the Worker's daily purge enforces it.
    retentionMonths: 12,
    responseTime: '[RESPONSE TIME]',
    // Vendors that receive personal information offshore (POPIA s18 / s72). Keep in step with what is deployed.
    offshoreVendors: ['Cloudflare, Inc. (hosting, form storage, privacy-first analytics)'],
  },

  analytics: {
    // Cloudflare Web Analytics token. Empty = no beacon is loaded at all.
    cloudflareToken: '',
  },

  nav: [
    { href: '/#services', label: 'Services' },
    { href: '/#about', label: 'About' },
    { href: '/#faq', label: 'Questions' },
    { href: '/#contact', label: 'Contact' },
  ],
} as const;
