#!/usr/bin/env python3
"""Generate script.js with full i18n for Urumuri site."""
import json
import textwrap

def js_str(s):
    return json.dumps(s, ensure_ascii=False)

# Read part 1 already written - we'll write complete file
HEADER = r'''(function () {
  'use strict';

  const STORAGE_LANG = 'urumuri-language';
  const STORAGE_THEME = 'urumuri-theme';
  const LANGS = ['en', 'fr', 'hi', 'zh', 'rw'];

  const PAGE_MAP = {
    'index.html': 'home', '': 'home',
    'transport.html': 'transport', 'food.html': 'food', 'courier.html': 'courier',
    'merchants.html': 'merchants', 'drivers.html': 'drivers', 'about.html': 'about',
    'contact.html': 'contact', 'safety.html': 'safety', 'reviews.html': 'reviews'
  };

  const getPageKey = () => {
    const page = window.location.pathname.split('/').pop() || 'index.html';
    return PAGE_MAP[page] || 'home';
  };

  const getNested = (obj, path) => {
    if (!obj || !path) return undefined;
    return path.split('.').reduce((acc, key) => (acc && acc[key] !== undefined ? acc[key] : undefined), obj);
  };

  let navToggle, navLinks, themeToggle, themeIcon, languagePicker;

  const ensureHeaderUI = () => {
    const headerInner = document.querySelector('.site-header .header-inner');
    if (!headerInner) return;
    let actions = headerInner.querySelector('.nav-actions');
    if (!actions) {
      actions = document.createElement('div');
      actions.className = 'nav-actions';
      const toggle = headerInner.querySelector('.nav-toggle');
      if (toggle) headerInner.insertBefore(actions, toggle);
      else headerInner.appendChild(actions);
    }
    if (!document.getElementById('themeToggle')) {
      const btn = document.createElement('button');
      btn.className = 'theme-toggle';
      btn.id = 'themeToggle';
      btn.type = 'button';
      btn.setAttribute('aria-label', 'Toggle light and dark mode');
      btn.innerHTML = '<span class="theme-icon">☾</span>';
      actions.appendChild(btn);
    }
    if (!document.getElementById('languagePicker')) {
      const label = document.createElement('label');
      label.className = 'language-picker';
      label.innerHTML = '<span class="sr-only">Choose language</span><select id="languagePicker" aria-label="Choose language"><option value="en">EN</option><option value="fr">FR</option><option value="hi">HI</option><option value="zh">中文</option><option value="rw">KINY</option></select>';
      const themeBtn = actions.querySelector('#themeToggle');
      if (themeBtn) actions.insertBefore(label, themeBtn);
      else actions.appendChild(label);
    }
    navToggle = document.getElementById('navToggle');
    navLinks = document.getElementById('navLinks');
    themeToggle = document.getElementById('themeToggle');
    themeIcon = themeToggle?.querySelector('.theme-icon');
    languagePicker = document.getElementById('languagePicker');
  };

  const applyTheme = (theme) => {
    const resolved = theme === 'dark' ? 'dark' : 'light';
    document.body.dataset.theme = resolved;
    localStorage.setItem(STORAGE_THEME, resolved);
    if (themeIcon) themeIcon.textContent = resolved === 'dark' ? '☀︎' : '☾';
  };

  const applyNav = (t) => {
    document.querySelectorAll('.nav-links a[data-page]').forEach((link) => {
      const key = link.dataset.page;
      if (t.nav[key]) link.textContent = t.nav[key];
    });
    document.querySelectorAll('.nav-links a:not([data-page])').forEach((link) => {
      const href = link.getAttribute('href') || '';
      if (href.includes('#services') && t.nav.offers) link.textContent = t.nav.offers;
      if (href.includes('#how-it-works') && t.nav.howItWorks) link.textContent = t.nav.howItWorks;
      if (href.includes('#contact') && t.nav.contact) link.textContent = t.nav.contact;
    });
  };

  const applyFooter = (t) => {
    const f = t.footer;
    if (!f) return;
    const brandBlock = document.querySelector('.site-footer .footer-grid > div:first-child');
    if (brandBlock) {
      const tagline = brandBlock.querySelector('p');
      if (tagline && f.tagline) tagline.textContent = f.tagline;
    }
    const modernBrand = document.querySelector('.site-footer.modern-footer .footer-brand p');
    if (modernBrand && f.taglineShort) modernBrand.textContent = f.taglineShort;
    const columns = document.querySelectorAll('.site-footer .footer-column');
    columns.forEach((col) => {
      const heading = col.querySelector('.footer-heading');
      const links = col.querySelectorAll('a');
      if (col.querySelector('a[href="reviews.html"]') && f.headings?.reviews) {
        if (heading) heading.textContent = f.headings.reviews;
        if (links[0] && f.links?.leaveReview) links[0].textContent = f.links.leaveReview;
      }
      if (col.querySelector('a[href*="index.html#services"]') && f.headings?.company) {
        if (heading) heading.textContent = f.headings.company;
        if (links[0] && f.links?.offers) links[0].textContent = f.links.offers;
        if (links[1] && f.links?.howItWorks) links[1].textContent = f.links.howItWorks;
        if (links[2] && f.links?.contact) links[2].textContent = f.links.contact;
      }
    });
    const standardCols = document.querySelectorAll('.site-footer:not(.modern-footer) .footer-column');
    if (standardCols.length >= 3 && f.headings) {
      const [legal, company, support] = standardCols;
      legal.querySelector('.footer-heading').textContent = f.headings.legal;
      company.querySelector('.footer-heading').textContent = f.headings.company;
      support.querySelector('.footer-heading').textContent = f.headings.support;
      const legalLinks = legal.querySelectorAll('a');
      [f.links.privacy, f.links.terms, f.links.cookies, f.links.driverTerms, f.links.merchantTerms].forEach((txt, i) => { if (txt && legalLinks[i]) legalLinks[i].textContent = txt; });
      const companyLinks = company.querySelectorAll('a');
      [f.links.about, f.links.drivers, f.links.merchants, f.links.safety, f.links.careers].forEach((txt, i) => { if (txt && companyLinks[i]) companyLinks[i].textContent = txt; });
      const supportLinks = support.querySelectorAll('a');
      [f.links.contact, f.links.business, f.links.faqs, f.links.downloads].forEach((txt, i) => { if (txt && supportLinks[i]) supportLinks[i].textContent = txt; });
    }
    const copyright = document.querySelector('.footer-bottom p');
    if (copyright && f.copyright) copyright.textContent = f.copyright;
  };

  const applySelectorMap = (t, pageKey) => {
    const maps = PAGE_SELECTORS[pageKey];
    if (!maps) return;
    maps.forEach(({ sel, path, attr, html }) => {
      const el = document.querySelector(sel);
      if (!el) return;
      const value = getNested(t, path);
      if (value === undefined) return;
      if (attr) el.setAttribute(attr, value);
      else if (html) el.innerHTML = value;
      else el.textContent = value;
    });
  };

  const applyDataAttributes = (t) => {
    document.querySelectorAll('[data-i18n]').forEach((el) => {
      const value = getNested(t, el.getAttribute('data-i18n'));
      if (typeof value === 'string') el.textContent = value;
    });
    document.querySelectorAll('[data-i18n-stat]').forEach((el) => {
      const stat = getNested(t, 'hero.stats.' + el.getAttribute('data-i18n-stat'));
      if (!stat) return;
      const nodes = el.querySelectorAll('span, p');
      if (nodes[0]) nodes[0].textContent = stat.value;
      if (nodes[1]) nodes[1].textContent = stat.label;
    });
    document.querySelectorAll('[data-i18n-card]').forEach((el) => {
      const card = getNested(t, 'cards.' + el.getAttribute('data-i18n-card'));
      if (!card) return;
      const title = el.querySelector('h3');
      const description = el.querySelector('p');
      const action = el.querySelector('.card-link');
      if (title) title.textContent = card.title;
      if (description) description.textContent = card.description;
      if (action) action.textContent = card.action;
    });
  };

  const applyLanguage = (language) => {
    const lang = LANGS.includes(language) ? language : 'en';
    const t = translations[lang] || translations.en;
    document.documentElement.lang = lang === 'zh' ? 'zh' : lang;
    document.body.dataset.language = lang;
    localStorage.setItem(STORAGE_LANG, lang);
    applyNav(t);
    applyFooter(t);
    applySelectorMap(t, getPageKey());
    applyDataAttributes(t);
    if (languagePicker && languagePicker.value !== lang) languagePicker.value = lang;
    if (themeToggle) themeToggle.setAttribute('aria-label', t.ui?.themeToggle || 'Toggle light and dark mode');
    if (languagePicker) languagePicker.setAttribute('aria-label', t.ui?.languagePicker || 'Choose language');
  };

'''

FOOTER_JS = r'''
  const highlightActiveLink = () => {
    const pageKey = getPageKey();
    document.querySelectorAll('.nav-links a[data-page]').forEach((link) => {
      link.classList.toggle('active', link.dataset.page === pageKey);
    });
    document.querySelectorAll('.site-footer a').forEach((link) => {
      const href = link.getAttribute('href') || '';
      const file = href.split('/').pop().split('#')[0];
      const linkKey = PAGE_MAP[file];
      if (linkKey === pageKey) link.classList.add('active');
    });
  };

  const initScrollAnimations = () => {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) {
      animatedElements.forEach((el) => el.classList.add('animate-in'));
      return;
    }
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-in');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.18, rootMargin: '0px 0px -80px 0px' });
    animatedElements.forEach((el) => observer.observe(el));
  };

  const initHeroParallax = () => {
    const heroVisual = document.querySelector('.hero-visual');
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!heroVisual || prefersReducedMotion) return;
    let ticking = false;
    const update = () => {
      heroVisual.style.transform = 'translate3d(0, ' + (window.scrollY * 0.05) + 'px, 0)';
      ticking = false;
    };
    window.addEventListener('scroll', () => {
      if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
  };

  const initReviewsForm = () => {
    if (getPageKey() !== 'reviews') return;
    const stars = document.querySelectorAll('.star');
    const ratingInput = document.getElementById('rating');
    const ratingLabel = document.getElementById('ratingLabel');
    const form = document.getElementById('reviewForm');
    if (!stars.length || !form) return;

    const getRatingLabels = () => {
      const lang = localStorage.getItem(STORAGE_LANG) || 'en';
      const t = translations[lang] || translations.en;
      return t.pages?.reviews?.form?.ratingLabels || ['Poor', 'Fair', 'Good', 'Very Good', 'Excellent'];
    };

    stars.forEach((star) => {
      star.addEventListener('click', () => {
        const rating = star.getAttribute('data-value');
        ratingInput.value = rating;
        const labels = getRatingLabels();
        ratingLabel.textContent = labels[rating - 1];
        stars.forEach((s) => s.classList.toggle('active', s.getAttribute('data-value') <= rating));
      });
      star.addEventListener('mouseover', () => {
        const hoverValue = star.getAttribute('data-value');
        stars.forEach((s) => {
          s.style.color = s.getAttribute('data-value') <= hoverValue ? 'var(--yellow)' : 'var(--gray-200)';
        });
      });
    });
    const starRating = document.getElementById('starRating');
    if (starRating) {
      starRating.addEventListener('mouseleave', () => {
        stars.forEach((s) => {
          s.style.color = s.classList.contains('active') ? 'var(--yellow)' : 'var(--gray-200)';
        });
      });
    }
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        service: document.getElementById('service').value,
        rating: document.getElementById('rating').value,
        review: document.getElementById('review').value,
        timestamp: new Date().toISOString()
      };
      const reviews = JSON.parse(localStorage.getItem('urumuri_reviews') || '[]');
      reviews.push(formData);
      localStorage.setItem('urumuri_reviews', JSON.stringify(reviews));
      const successMessage = document.getElementById('successMessage');
      if (successMessage) successMessage.style.display = 'block';
      form.reset();
      stars.forEach((s) => s.classList.remove('active'));
      const lang = localStorage.getItem(STORAGE_LANG) || 'en';
      const t = translations[lang] || translations.en;
      if (ratingLabel) ratingLabel.textContent = t.pages?.reviews?.form?.ratingSelect || 'Select rating';
      if (successMessage) successMessage.scrollIntoView({ behavior: 'smooth' });
      setTimeout(() => { window.location.href = 'index.html'; }, 3000);
    });
  };

  const init = () => {
    ensureHeaderUI();
    const storedTheme = localStorage.getItem(STORAGE_THEME);
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    applyTheme(storedTheme || (prefersDark ? 'dark' : 'light'));
    const storedLanguage = localStorage.getItem(STORAGE_LANG) || 'en';
    if (languagePicker) {
      languagePicker.value = storedLanguage;
      languagePicker.addEventListener('change', (e) => applyLanguage(e.target.value));
    }
    applyLanguage(storedLanguage);
    navToggle?.addEventListener('click', () => {
      const expanded = navToggle.getAttribute('aria-expanded') === 'true';
      navToggle.setAttribute('aria-expanded', String(!expanded));
      navLinks?.classList.toggle('active');
    });
    themeToggle?.addEventListener('click', () => {
      applyTheme(document.body.dataset.theme === 'dark' ? 'light' : 'dark');
    });
    highlightActiveLink();
    initScrollAnimations();
    initHeroParallax();
    initReviewsForm();
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
'''

# Load translations from external JSON files we'll embed
import os
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build PAGE_SELECTORS as JS
PAGE_SELECTORS_JS = '''
  const PAGE_SELECTORS = {
    home: [
      { sel: '.hero-home .eyebrow', path: 'pages.home.hero.eyebrow' },
      { sel: '.hero-home h1', path: 'pages.home.hero.headline' },
      { sel: '.hero-home .hero-intro', path: 'pages.home.hero.intro' },
      { sel: '.hero-home .hero-actions .btn-primary', path: 'pages.home.hero.primary' },
      { sel: '.hero-home .hero-actions .btn-secondary', path: 'pages.home.hero.secondary' },
      { sel: '.hero-home .hero-stats > div:nth-child(1) span', path: 'pages.home.hero.stats.one.value' },
      { sel: '.hero-home .hero-stats > div:nth-child(1) p', path: 'pages.home.hero.stats.one.label' },
      { sel: '.hero-home .hero-stats > div:nth-child(2) span', path: 'pages.home.hero.stats.two.value' },
      { sel: '.hero-home .hero-stats > div:nth-child(2) p', path: 'pages.home.hero.stats.two.label' },
      { sel: '.hero-home .hero-stats > div:nth-child(3) span', path: 'pages.home.hero.stats.three.value' },
      { sel: '.hero-home .hero-stats > div:nth-child(3) p', path: 'pages.home.hero.stats.three.label' },
      { sel: '.hero-home .hero-badge', path: 'pages.home.hero.badge' },
      { sel: '.hero-home .media-top', path: 'pages.home.hero.mediaTop' },
      { sel: '.hero-home .media-middle', path: 'pages.home.hero.mediaMiddle' },
      { sel: '.hero-home .media-bottom', path: 'pages.home.hero.mediaBottom' },
      { sel: '.section-highlight .section-header .eyebrow', path: 'pages.home.highlights.eyebrow' },
      { sel: '.section-highlight .section-header h2', path: 'pages.home.highlights.title' },
      { sel: '.section-highlight .cards-grid a:nth-child(1) h3', path: 'cards.transport.title' },
      { sel: '.section-highlight .cards-grid a:nth-child(1) p', path: 'cards.transport.description' },
      { sel: '.section-highlight .cards-grid a:nth-child(1) .card-link', path: 'cards.transport.action' },
      { sel: '.section-highlight .cards-grid a:nth-child(2) h3', path: 'cards.food.title' },
      { sel: '.section-highlight .cards-grid a:nth-child(2) p', path: 'cards.food.description' },
      { sel: '.section-highlight .cards-grid a:nth-child(2) .card-link', path: 'cards.food.action' },
      { sel: '.section-highlight .cards-grid a:nth-child(3) h3', path: 'cards.courier.title' },
      { sel: '.section-highlight .cards-grid a:nth-child(3) p', path: 'cards.courier.description' },
      { sel: '.section-highlight .cards-grid a:nth-child(3) .card-link', path: 'cards.courier.action' },
      { sel: '.section-glass .panel-primary h2', path: 'pages.home.glass.merchantTitle' },
      { sel: '.section-glass .panel-primary p', path: 'pages.home.glass.merchantText' },
      { sel: '.section-glass .panel-secondary h2', path: 'pages.home.glass.driversTitle' },
      { sel: '.section-glass .panel-secondary p', path: 'pages.home.glass.driversText' },
      { sel: '.section-features .section-header .eyebrow', path: 'pages.home.features.eyebrow' },
      { sel: '.section-features .section-header h2', path: 'pages.home.features.title' },
      { sel: '.section-features .feature-grid article:nth-child(1) h3', path: 'pages.home.features.dispatchTitle' },
      { sel: '.section-features .feature-grid article:nth-child(1) p', path: 'pages.home.features.dispatchText' },
      { sel: '.section-features .feature-grid article:nth-child(2) h3', path: 'pages.home.features.pricingTitle' },
      { sel: '.section-features .feature-grid article:nth-child(2) p', path: 'pages.home.features.pricingText' },
      { sel: '.section-features .feature-grid article:nth-child(3) h3', path: 'pages.home.features.merchantTitle' },
      { sel: '.section-features .feature-grid article:nth-child(3) p', path: 'pages.home.features.merchantText' },
      { sel: '.section-features .feature-grid article:nth-child(4) h3', path: 'pages.home.features.communityTitle' },
      { sel: '.section-features .feature-grid article:nth-child(4) p', path: 'pages.home.features.communityText' },
      { sel: '.section-cta .eyebrow', path: 'pages.home.cta.eyebrow' },
      { sel: '.section-cta h2', path: 'pages.home.cta.title' },
      { sel: '.section-cta .cta-panel > div > p:not(.eyebrow)', path: 'pages.home.cta.text' },
      { sel: '.section-cta .btn-primary', path: 'pages.home.cta.button' }
    ],
    transport: [
      { sel: '.hero-secondary .eyebrow', path: 'pages.transport.hero.eyebrow' },
      { sel: '.hero-secondary h1', path: 'pages.transport.hero.headline' },
      { sel: '.hero-secondary .hero-intro', path: 'pages.transport.hero.intro' },
      { sel: '.hero-secondary .hero-actions .btn-primary', path: 'pages.transport.hero.primary' },
      { sel: '.hero-secondary .hero-actions .btn-secondary', path: 'pages.transport.hero.secondary' },
      { sel: '.hero-secondary .hero-badge', path: 'pages.transport.hero.badge' },
      { sel: '.hero-secondary .media-panel', path: 'pages.transport.hero.media' },
      { sel: 'main .section-highlight:nth-of-type(1) .section-header .eyebrow', path: 'pages.transport.safety.eyebrow' },
      { sel: 'main .section-highlight:nth-of-type(1) .section-header h2', path: 'pages.transport.safety.title' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(1) h3', path: 'pages.transport.safety.helmetTitle' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(1) p', path: 'pages.transport.safety.helmetText' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(2) h3', path: 'pages.transport.safety.rainTitle' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(2) p', path: 'pages.transport.safety.rainText' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(3) h3', path: 'pages.transport.safety.reflectiveTitle' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(3) p', path: 'pages.transport.safety.reflectiveText' },
      { sel: 'main .section-glass .glass-panel:nth-child(1) h2', path: 'pages.transport.glass.electricTitle' },
      { sel: 'main .section-glass .glass-panel:nth-child(1) p', path: 'pages.transport.glass.electricText' },
      { sel: 'main .section-glass .glass-panel:nth-child(2) h2', path: 'pages.transport.glass.passengerTitle' },
      { sel: 'main .section-glass .glass-panel:nth-child(2) p', path: 'pages.transport.glass.passengerText' },
      { sel: 'main .section-highlight:nth-of-type(2) .section-header .eyebrow', path: 'pages.transport.student.eyebrow' },
      { sel: 'main .section-highlight:nth-of-type(2) .section-header h2', path: 'pages.transport.student.title' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(1) h3', path: 'pages.transport.student.discountTitle' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(1) p', path: 'pages.transport.student.discountText' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(2) h3', path: 'pages.transport.student.studyTitle' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(2) p', path: 'pages.transport.student.studyText' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(3) h3', path: 'pages.transport.student.youthTitle' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(3) p', path: 'pages.transport.student.youthText' },
      { sel: 'main .section-cta .eyebrow', path: 'pages.transport.cta.eyebrow' },
      { sel: 'main .section-cta h2', path: 'pages.transport.cta.title' },
      { sel: 'main .section-cta .cta-panel > div > p:not(.eyebrow)', path: 'pages.transport.cta.text' },
      { sel: 'main .section-cta .btn-primary', path: 'pages.transport.cta.button' }
    ],
    food: [
      { sel: '.hero-secondary .eyebrow', path: 'pages.food.hero.eyebrow' },
      { sel: '.hero-secondary h1', path: 'pages.food.hero.headline' },
      { sel: '.hero-secondary .hero-intro', path: 'pages.food.hero.intro' },
      { sel: '.hero-secondary .hero-actions .btn-primary', path: 'pages.food.hero.primary' },
      { sel: '.hero-secondary .hero-actions .btn-secondary', path: 'pages.food.hero.secondary' },
      { sel: '.hero-secondary .hero-badge', path: 'pages.food.hero.badge' },
      { sel: '.hero-secondary .media-panel', path: 'pages.food.hero.media' },
      { sel: 'main .section-highlight:nth-of-type(1) .section-header .eyebrow', path: 'pages.food.services.eyebrow' },
      { sel: 'main .section-highlight:nth-of-type(1) .section-header h2', path: 'pages.food.services.title' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(1) h3', path: 'pages.food.services.restaurantTitle' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(1) p', path: 'pages.food.services.restaurantText' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(2) h3', path: 'pages.food.services.groceryTitle' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(2) p', path: 'pages.food.services.groceryText' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(3) h3', path: 'pages.food.services.buyTitle' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(3) p', path: 'pages.food.services.buyText' },
      { sel: 'main .section-glass .glass-panel:nth-child(1) h2', path: 'pages.food.glass.workTitle' },
      { sel: 'main .section-glass .glass-panel:nth-child(1) p', path: 'pages.food.glass.workText' },
      { sel: 'main .section-glass .glass-panel:nth-child(2) h2', path: 'pages.food.glass.homeTitle' },
      { sel: 'main .section-glass .glass-panel:nth-child(2) p', path: 'pages.food.glass.homeText' },
      { sel: 'main .section-highlight:nth-of-type(2) .section-header .eyebrow', path: 'pages.food.support.eyebrow' },
      { sel: 'main .section-highlight:nth-of-type(2) .section-header h2', path: 'pages.food.support.title' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(1) h3', path: 'pages.food.support.fastTitle' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(1) p', path: 'pages.food.support.fastText' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(2) h3', path: 'pages.food.support.secureTitle' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(2) p', path: 'pages.food.support.secureText' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(3) h3', path: 'pages.food.support.smartTitle' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(3) p', path: 'pages.food.support.smartText' },
      { sel: 'main .section-cta .eyebrow', path: 'pages.food.cta.eyebrow' },
      { sel: 'main .section-cta h2', path: 'pages.food.cta.title' },
      { sel: 'main .section-cta .cta-panel > div > p:not(.eyebrow)', path: 'pages.food.cta.text' },
      { sel: 'main .section-cta .btn-primary', path: 'pages.food.cta.button' }
    ],
    courier: [
      { sel: '.hero-secondary .eyebrow', path: 'pages.courier.hero.eyebrow' },
      { sel: '.hero-secondary h1', path: 'pages.courier.hero.headline' },
      { sel: '.hero-secondary .hero-intro', path: 'pages.courier.hero.intro' },
      { sel: '.hero-secondary .hero-actions .btn-primary', path: 'pages.courier.hero.primary' },
      { sel: '.hero-secondary .hero-actions .btn-secondary', path: 'pages.courier.hero.secondary' },
      { sel: '.hero-secondary .hero-badge', path: 'pages.courier.hero.badge' },
      { sel: '.hero-secondary .media-panel', path: 'pages.courier.hero.media' },
      { sel: 'main .section-highlight:nth-of-type(1) .section-header .eyebrow', path: 'pages.courier.services.eyebrow' },
      { sel: 'main .section-highlight:nth-of-type(1) .section-header h2', path: 'pages.courier.services.title' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(1) h3', path: 'pages.courier.services.docTitle' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(1) p', path: 'pages.courier.services.docText' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(2) h3', path: 'pages.courier.services.businessTitle' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(2) p', path: 'pages.courier.services.businessText' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(3) h3', path: 'pages.courier.services.personalTitle' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(3) p', path: 'pages.courier.services.personalText' },
      { sel: 'main .section-glass .glass-panel:nth-child(1) h2', path: 'pages.courier.glass.sameDayTitle' },
      { sel: 'main .section-glass .glass-panel:nth-child(1) p', path: 'pages.courier.glass.sameDayText' },
      { sel: 'main .section-glass .glass-panel:nth-child(2) h2', path: 'pages.courier.glass.trackingTitle' },
      { sel: 'main .section-glass .glass-panel:nth-child(2) p', path: 'pages.courier.glass.trackingText' },
      { sel: 'main .section-highlight:nth-of-type(2) .section-header .eyebrow', path: 'pages.courier.professional.eyebrow' },
      { sel: 'main .section-highlight:nth-of-type(2) .section-header h2', path: 'pages.courier.professional.title' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(1) h3', path: 'pages.courier.professional.protectionTitle' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(1) p', path: 'pages.courier.professional.protectionText' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(2) h3', path: 'pages.courier.professional.trainingTitle' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(2) p', path: 'pages.courier.professional.trainingText' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(3) h3', path: 'pages.courier.professional.workflowTitle' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(3) p', path: 'pages.courier.professional.workflowText' },
      { sel: 'main .section-cta .eyebrow', path: 'pages.courier.cta.eyebrow' },
      { sel: 'main .section-cta h2', path: 'pages.courier.cta.title' },
      { sel: 'main .section-cta .btn-primary', path: 'pages.courier.cta.button' }
    ],
    merchants: [
      { sel: '.hero-secondary .eyebrow', path: 'pages.merchants.hero.eyebrow' },
      { sel: '.hero-secondary h1', path: 'pages.merchants.hero.headline' },
      { sel: '.hero-secondary .hero-intro', path: 'pages.merchants.hero.intro' },
      { sel: '.hero-secondary .hero-actions .btn-primary', path: 'pages.merchants.hero.primary' },
      { sel: '.hero-secondary .hero-actions .btn-secondary', path: 'pages.merchants.hero.secondary' },
      { sel: '.hero-secondary .hero-badge', path: 'pages.merchants.hero.badge' },
      { sel: '.hero-secondary .media-panel', path: 'pages.merchants.hero.media' },
      { sel: 'main .section-highlight:nth-of-type(1) .section-header .eyebrow', path: 'pages.merchants.dashboard.eyebrow' },
      { sel: 'main .section-highlight:nth-of-type(1) .section-header h2', path: 'pages.merchants.dashboard.title' },
      { sel: 'main .section-highlight:nth-of-type(1) .glass-panel:nth-child(1) h3', path: 'pages.merchants.dashboard.salesToday' },
      { sel: 'main .section-highlight:nth-of-type(1) .glass-panel:nth-child(2) h3', path: 'pages.merchants.dashboard.salesWeek' },
      { sel: 'main .section-highlight:nth-of-type(1) .glass-panel:nth-child(3) h3', path: 'pages.merchants.dashboard.salesMonth' },
      { sel: 'main .section-highlight:nth-of-type(1) .glass-panel:nth-child(4) h3', path: 'pages.merchants.dashboard.aov' },
      { sel: 'main .section-highlight:nth-of-type(1) .glass-panel:nth-child(5) h3', path: 'pages.merchants.dashboard.orders' },
      { sel: 'main .section-highlight:nth-of-type(1) .glass-panel:nth-child(6) h3', path: 'pages.merchants.dashboard.bestSellers' },
      { sel: 'main .section-highlight:nth-of-type(1) .glass-panel:nth-child(6) p', path: 'pages.merchants.dashboard.bestSellersText' },
      { sel: 'main .section-glass .glass-panel:nth-child(1) h2', path: 'pages.merchants.glass.revenueTitle' },
      { sel: 'main .section-glass .glass-panel:nth-child(1) p', path: 'pages.merchants.glass.revenueText' },
      { sel: 'main .section-glass .glass-panel:nth-child(2) h2', path: 'pages.merchants.glass.productTitle' },
      { sel: 'main .section-glass .glass-panel:nth-child(2) p', path: 'pages.merchants.glass.productText' },
      { sel: 'main .section-highlight:nth-of-type(2) .section-header .eyebrow', path: 'pages.merchants.intelligence.eyebrow' },
      { sel: 'main .section-highlight:nth-of-type(2) .section-header h2', path: 'pages.merchants.intelligence.title' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(1) h3', path: 'pages.merchants.intelligence.sellsTitle' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(1) p', path: 'pages.merchants.intelligence.sellsText' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(2) h3', path: 'pages.merchants.intelligence.hireTitle' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(2) p', path: 'pages.merchants.intelligence.hireText' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(3) h3', path: 'pages.merchants.intelligence.restockTitle' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(3) p', path: 'pages.merchants.intelligence.restockText' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(4) h3', path: 'pages.merchants.intelligence.revenueTitle' },
      { sel: 'main .section-highlight:nth-of-type(2) article:nth-child(4) p', path: 'pages.merchants.intelligence.revenueText' },
      { sel: 'main .section-glass.animate-on-scroll .eyebrow', path: 'pages.merchants.future.eyebrow' },
      { sel: 'main .section-glass.animate-on-scroll h2', path: 'pages.merchants.future.title' },
      { sel: 'main .section-glass.animate-on-scroll .cta-panel > div > p:not(.eyebrow)', path: 'pages.merchants.future.text' },
      { sel: 'main .section-glass.animate-on-scroll .btn-secondary', path: 'pages.merchants.future.button' },
      { sel: 'main .section-highlight.animate-on-scroll .section-header .eyebrow', path: 'pages.merchants.pricing.eyebrow' },
      { sel: 'main .section-highlight.animate-on-scroll .section-header h2', path: 'pages.merchants.pricing.title' },
      { sel: 'main .section-highlight.animate-on-scroll .section-header > p', path: 'pages.merchants.pricing.text' },
      { sel: 'main .section-highlight.animate-on-scroll article:nth-child(1) h3', path: 'pages.merchants.pricing.trafficTitle' },
      { sel: 'main .section-highlight.animate-on-scroll article:nth-child(1) p', path: 'pages.merchants.pricing.trafficText' },
      { sel: 'main .section-highlight.animate-on-scroll article:nth-child(2) h3', path: 'pages.merchants.pricing.distanceTitle' },
      { sel: 'main .section-highlight.animate-on-scroll article:nth-child(2) p', path: 'pages.merchants.pricing.distanceText' },
      { sel: 'main .section-highlight.animate-on-scroll article:nth-child(3) h3', path: 'pages.merchants.pricing.urgencyTitle' },
      { sel: 'main .section-highlight.animate-on-scroll article:nth-child(3) p', path: 'pages.merchants.pricing.urgencyText' }
    ],
    drivers: [
      { sel: '.hero-secondary .eyebrow', path: 'pages.drivers.hero.eyebrow' },
      { sel: '.hero-secondary h1', path: 'pages.drivers.hero.headline' },
      { sel: '.hero-secondary .hero-intro', path: 'pages.drivers.hero.intro' },
      { sel: '.hero-secondary .hero-actions .btn-primary', path: 'pages.drivers.hero.primary' },
      { sel: '.hero-secondary .hero-actions .btn-secondary', path: 'pages.drivers.hero.secondary' },
      { sel: '.hero-secondary .hero-badge', path: 'pages.drivers.hero.badge' },
      { sel: '.hero-secondary .media-panel', path: 'pages.drivers.hero.media' },
      { sel: 'main .section-highlight .section-header .eyebrow', path: 'pages.drivers.benefits.eyebrow' },
      { sel: 'main .section-highlight .section-header h2', path: 'pages.drivers.benefits.title' },
      { sel: 'main .section-highlight article:nth-child(1) h3', path: 'pages.drivers.benefits.incomeTitle' },
      { sel: 'main .section-highlight article:nth-child(1) p', path: 'pages.drivers.benefits.incomeText' },
      { sel: 'main .section-highlight article:nth-child(2) h3', path: 'pages.drivers.benefits.equipmentTitle' },
      { sel: 'main .section-highlight article:nth-child(2) p', path: 'pages.drivers.benefits.equipmentText' },
      { sel: 'main .section-highlight article:nth-child(3) h3', path: 'pages.drivers.benefits.trainingTitle' },
      { sel: 'main .section-highlight article:nth-child(3) p', path: 'pages.drivers.benefits.trainingText' },
      { sel: 'main .section-highlight article:nth-child(4) h3', path: 'pages.drivers.benefits.growthTitle' },
      { sel: 'main .section-highlight article:nth-child(4) p', path: 'pages.drivers.benefits.growthText' },
      { sel: 'main .section-glass .glass-panel:nth-child(1) h2', path: 'pages.drivers.glass.electricTitle' },
      { sel: 'main .section-glass .glass-panel:nth-child(1) p', path: 'pages.drivers.glass.electricText' },
      { sel: 'main .section-glass .glass-panel:nth-child(2) h2', path: 'pages.drivers.glass.safetyTitle' },
      { sel: 'main .section-glass .glass-panel:nth-child(2) p', path: 'pages.drivers.glass.safetyText' },
      { sel: 'main .section-cta .eyebrow', path: 'pages.drivers.cta.eyebrow' },
      { sel: 'main .section-cta h2', path: 'pages.drivers.cta.title' },
      { sel: 'main .section-cta .btn-primary', path: 'pages.drivers.cta.button' }
    ],
    about: [
      { sel: '.hero-secondary .eyebrow', path: 'pages.about.hero.eyebrow' },
      { sel: '.hero-secondary h1', path: 'pages.about.hero.headline' },
      { sel: '.hero-secondary .hero-intro', path: 'pages.about.hero.intro' },
      { sel: '.hero-secondary .hero-actions .btn-primary', path: 'pages.about.hero.primary' },
      { sel: '.hero-secondary .hero-actions .btn-secondary', path: 'pages.about.hero.secondary' },
      { sel: '.hero-secondary .hero-badge', path: 'pages.about.hero.badge' },
      { sel: '.hero-secondary .media-panel', path: 'pages.about.hero.media' },
      { sel: 'main .section-highlight .glass-panel:nth-child(1) h2', path: 'pages.about.mission.missionTitle' },
      { sel: 'main .section-highlight .glass-panel:nth-child(1) p', path: 'pages.about.mission.missionText' },
      { sel: 'main .section-highlight .glass-panel:nth-child(2) h2', path: 'pages.about.mission.visionTitle' },
      { sel: 'main .section-highlight .glass-panel:nth-child(2) p', path: 'pages.about.mission.visionText' },
      { sel: 'main .section-glass .section-header .eyebrow', path: 'pages.about.values.eyebrow' },
      { sel: 'main .section-glass .section-header h2', path: 'pages.about.values.title' },
      { sel: 'main .section-glass article:nth-child(1) h3', path: 'pages.about.values.innovationTitle' },
      { sel: 'main .section-glass article:nth-child(1) p', path: 'pages.about.values.innovationText' },
      { sel: 'main .section-glass article:nth-child(2) h3', path: 'pages.about.values.safetyTitle' },
      { sel: 'main .section-glass article:nth-child(2) p', path: 'pages.about.values.safetyText' },
      { sel: 'main .section-glass article:nth-child(3) h3', path: 'pages.about.values.communityTitle' },
      { sel: 'main .section-glass article:nth-child(3) p', path: 'pages.about.values.communityText' },
      { sel: 'main .section-glass article:nth-child(4) h3', path: 'pages.about.values.sustainabilityTitle' },
      { sel: 'main .section-glass article:nth-child(4) p', path: 'pages.about.values.sustainabilityText' },
      { sel: 'main .section-highlight.animate-on-scroll .section-header .eyebrow', path: 'pages.about.impact.eyebrow' },
      { sel: 'main .section-highlight.animate-on-scroll .section-header h2', path: 'pages.about.impact.title' },
      { sel: 'main .section-highlight.animate-on-scroll .section-header > p', path: 'pages.about.impact.text' },
      { sel: 'main .section-highlight.animate-on-scroll .service-card:nth-child(1) h3', path: 'pages.about.impact.growthTitle' },
      { sel: 'main .section-highlight.animate-on-scroll .service-card:nth-child(1) p', path: 'pages.about.impact.growthText' },
      { sel: 'main .section-highlight.animate-on-scroll .service-card:nth-child(2) h3', path: 'pages.about.impact.youthTitle' },
      { sel: 'main .section-highlight.animate-on-scroll .service-card:nth-child(2) p', path: 'pages.about.impact.youthText' },
      { sel: 'main .section-highlight.animate-on-scroll .service-card:nth-child(3) h3', path: 'pages.about.impact.smartTitle' },
      { sel: 'main .section-highlight.animate-on-scroll .service-card:nth-child(3) p', path: 'pages.about.impact.smartText' }
    ],
    contact: [
      { sel: '.hero-secondary .eyebrow', path: 'pages.contact.hero.eyebrow' },
      { sel: '.hero-secondary h1', path: 'pages.contact.hero.headline' },
      { sel: '.hero-secondary .hero-intro', path: 'pages.contact.hero.intro' },
      { sel: '.hero-secondary .hero-actions .btn-primary', path: 'pages.contact.hero.primary' },
      { sel: '.hero-secondary .hero-actions .btn-secondary', path: 'pages.contact.hero.secondary' },
      { sel: '.hero-secondary .hero-badge', path: 'pages.contact.hero.badge' },
      { sel: '.hero-secondary .media-panel', path: 'pages.contact.hero.media' },
      { sel: 'main .section-highlight .glass-panel:nth-child(1) h2', path: 'pages.contact.info.officeTitle' },
      { sel: 'main .section-highlight .glass-panel:nth-child(1) p', path: 'pages.contact.info.officeText' },
      { sel: 'main .section-highlight .glass-panel:nth-child(2) h2', path: 'pages.contact.info.phoneTitle' },
      { sel: 'main .section-highlight .glass-panel:nth-child(3) h2', path: 'pages.contact.info.emailTitle' },
      { sel: 'main .section-glass .section-header .eyebrow', path: 'pages.contact.reach.eyebrow' },
      { sel: 'main .section-glass .section-header h2', path: 'pages.contact.reach.title' },
      { sel: 'main .section-glass article:nth-child(1) h3', path: 'pages.contact.reach.businessTitle' },
      { sel: 'main .section-glass article:nth-child(1) p', path: 'pages.contact.reach.businessText' },
      { sel: 'main .section-glass article:nth-child(2) h3', path: 'pages.contact.reach.driverTitle' },
      { sel: 'main .section-glass article:nth-child(2) p', path: 'pages.contact.reach.driverText' },
      { sel: 'main .section-glass article:nth-child(3) h3', path: 'pages.contact.reach.customerTitle' },
      { sel: 'main .section-glass article:nth-child(3) p', path: 'pages.contact.reach.customerText' },
      { sel: 'main .section-glass article:nth-child(4) h3', path: 'pages.contact.reach.pressTitle' },
      { sel: 'main .section-glass article:nth-child(4) p', path: 'pages.contact.reach.pressText' },
      { sel: 'main .section-cta .eyebrow', path: 'pages.contact.cta.eyebrow' },
      { sel: 'main .section-cta h2', path: 'pages.contact.cta.title' },
      { sel: 'main .section-cta .btn-primary', path: 'pages.contact.cta.button' }
    ],
    safety: [
      { sel: '.hero-secondary .eyebrow', path: 'pages.safety.hero.eyebrow' },
      { sel: '.hero-secondary h1', path: 'pages.safety.hero.headline' },
      { sel: '.hero-secondary .hero-intro', path: 'pages.safety.hero.intro' },
      { sel: '.hero-secondary .hero-actions .btn-primary', path: 'pages.safety.hero.primary' },
      { sel: '.hero-secondary .hero-actions .btn-secondary', path: 'pages.safety.hero.secondary' },
      { sel: '.hero-secondary .hero-badge', path: 'pages.safety.hero.badge' },
      { sel: '.hero-secondary .media-panel', path: 'pages.safety.hero.media' },
      { sel: 'main .section-highlight:nth-of-type(1) .section-header .eyebrow', path: 'pages.safety.passenger.eyebrow' },
      { sel: 'main .section-highlight:nth-of-type(1) .section-header h2', path: 'pages.safety.passenger.title' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(1) h3', path: 'pages.safety.passenger.helmetTitle' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(1) p', path: 'pages.safety.passenger.helmetText' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(2) h3', path: 'pages.safety.passenger.reflectiveTitle' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(2) p', path: 'pages.safety.passenger.reflectiveText' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(3) h3', path: 'pages.safety.passenger.visibilityTitle' },
      { sel: 'main .section-highlight:nth-of-type(1) .service-card:nth-child(3) p', path: 'pages.safety.passenger.visibilityText' },
      { sel: 'main .section-glass .glass-panel:nth-child(1) h2', path: 'pages.safety.glass.trainingTitle' },
      { sel: 'main .section-glass .glass-panel:nth-child(1) p', path: 'pages.safety.glass.trainingText' },
      { sel: 'main .section-glass .glass-panel:nth-child(2) h2', path: 'pages.safety.glass.packageTitle' },
      { sel: 'main .section-glass .glass-panel:nth-child(2) p', path: 'pages.safety.glass.packageText' },
      { sel: 'main .section-highlight.animate-on-scroll .section-header .eyebrow', path: 'pages.safety.emergency.eyebrow' },
      { sel: 'main .section-highlight.animate-on-scroll .section-header h2', path: 'pages.safety.emergency.title' },
      { sel: 'main .section-highlight.animate-on-scroll .section-header > p', path: 'pages.safety.emergency.text' },
      { sel: 'main .section-highlight.animate-on-scroll article:nth-child(1) h3', path: 'pages.safety.emergency.supportTitle' },
      { sel: 'main .section-highlight.animate-on-scroll article:nth-child(1) p', path: 'pages.safety.emergency.supportText' },
      { sel: 'main .section-highlight.animate-on-scroll article:nth-child(2) h3', path: 'pages.safety.emergency.careTitle' },
      { sel: 'main .section-highlight.animate-on-scroll article:nth-child(2) p', path: 'pages.safety.emergency.careText' },
      { sel: 'main .section-highlight.animate-on-scroll article:nth-child(3) h3', path: 'pages.safety.emergency.insuranceTitle' },
      { sel: 'main .section-highlight.animate-on-scroll article:nth-child(3) p', path: 'pages.safety.emergency.insuranceText' },
      { sel: 'main .section-cta .eyebrow', path: 'pages.safety.cta.eyebrow' },
      { sel: 'main .section-cta h2', path: 'pages.safety.cta.title' },
      { sel: 'main .section-cta .btn-primary', path: 'pages.safety.cta.button' }
    ],
    reviews: [
      { sel: '.review-header .eyebrow', path: 'pages.reviews.header.eyebrow' },
      { sel: '.review-header h1', path: 'pages.reviews.header.title' },
      { sel: '.review-header p', path: 'pages.reviews.header.subtitle' },
      { sel: '#successMessage h3', path: 'pages.reviews.success.title' },
      { sel: '#successMessage p', path: 'pages.reviews.success.text' },
      { sel: 'label[for="name"]', path: 'pages.reviews.form.name' },
      { sel: '#name', path: 'pages.reviews.form.namePlaceholder', attr: 'placeholder' },
      { sel: 'label[for="email"]', path: 'pages.reviews.form.email' },
      { sel: '#email', path: 'pages.reviews.form.emailPlaceholder', attr: 'placeholder' },
      { sel: 'label[for="phone"]', path: 'pages.reviews.form.phone' },
      { sel: '#phone', path: 'pages.reviews.form.phonePlaceholder', attr: 'placeholder' },
      { sel: 'label[for="service"]', path: 'pages.reviews.form.service' },
      { sel: '#service option[value=""]', path: 'pages.reviews.form.servicePlaceholder' },
      { sel: '#service option[value="food"]', path: 'pages.reviews.form.services.food' },
      { sel: '#service option[value="grocery"]', path: 'pages.reviews.form.services.grocery' },
      { sel: '#service option[value="pharmacy"]', path: 'pages.reviews.form.services.pharmacy' },
      { sel: '#service option[value="courier"]', path: 'pages.reviews.form.services.courier' },
      { sel: '#service option[value="buyformes"]', path: 'pages.reviews.form.services.buyformes' },
      { sel: '#service option[value="other"]', path: 'pages.reviews.form.services.other' },
      { sel: '.form-group:has(#starRating) > label', path: 'pages.reviews.form.rating' },
      { sel: '#review', path: 'pages.reviews.form.reviewPlaceholder', attr: 'placeholder' },
      { sel: 'label[for="review"]', path: 'pages.reviews.form.review' },
      { sel: '.btn-submit', path: 'pages.reviews.form.submit' },
      { sel: '.btn-cancel', path: 'pages.reviews.form.cancel' }
    ]
  };
'''

print("Generator scaffold ready - need translations JSON")