#!/usr/bin/env python3
"""Generate i18n_data.py and regenerate script.js for the Urumuri static site."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
SCRIPT_JS = ROOT / "script.js"
I18N_DATA = ROOT / "i18n_data.py"
EN_STRINGS_FILE = ROOT / "_en_strings.json"
TRIPLES_FILE = ROOT / "_i18n_triples.json"

KEEP_AS_IS = {
    "Urumuri Transport",
    "Urumuri Food",
    "Urumuri Courier",
    "WhatsApp",
    "© 2026 Urumuri",
    "Kigali Innovation District, Kigali, Rwanda",
    "+250 7XX XXX XXX",
    "your.email@example.com",
    "24/7",
    "200+",
    "7 menu items leading revenue.",
    "Thank you! 🎉",
}

META_EN: dict[str, dict[str, str]] = {
    "home": {
        "title": "Urumuri | Rwanda's Intelligent Mobility Ecosystem",
        "description": "Urumuri is Rwanda's next-generation mobility platform combining transport, food delivery, courier services, merchant intelligence and driver empowerment.",
    },
    "transport": {
        "title": "Urumuri Transport | Premium Passenger Rides",
        "description": "Urumuri Transport is Rwanda's flagship mobility service with electric motorcycles, premium safety gear and student-focused discounts.",
    },
    "food": {
        "title": "Urumuri Food | Restaurant, Grocery and Buy For Me",
        "description": "Urumuri Food brings restaurant meals, groceries, pharmacy essentials and buy-for-me services to your door with premium speed and reliability.",
    },
    "courier": {
        "title": "Urumuri Courier | Professional Package Delivery",
        "description": "Urumuri Courier offers business parcel delivery, document handling, same-day service and secure tracking for professional customers.",
    },
    "merchants": {
        "title": "Urumuri Merchants | Intelligence & Analytics",
        "description": "Urumuri Merchants provides sales analytics, inventory insights and AI-powered recommendations for business growth.",
    },
    "drivers": {
        "title": "Urumuri Drivers | Flexible Income and Professional Growth",
        "description": "Join Urumuri as a driver with flexible income, safety training, electric motorcycles and growth opportunities.",
    },
    "about": {
        "title": "About Urumuri | Mission, Vision and Values",
        "description": "Learn Urumuri's mission, vision and values. A premium African mobility brand focused on innovation, safety, community and sustainability.",
    },
    "contact": {
        "title": "Contact Urumuri | Office, Support and Business Inquiries",
        "description": "Contact Urumuri for support, partnerships, driver applications and merchant inquiries. Find our office location, phone, email and social channels.",
    },
    "safety": {
        "title": "Urumuri Safety | Passenger, Rider and Package Protection",
        "description": "Urumuri Safety explains our commitment to passenger protection, reflective gear, rider training, package protection and future insurance readiness.",
    },
    "reviews": {
        "title": "Leave a Review | Urumuri",
        "description": "Share your Urumuri experience and help us improve transport, food and courier services across Rwanda.",
    },
}

META_FR: dict[str, dict[str, str]] = {
    "home": {"title": "Urumuri | Écosystème de mobilité intelligent du Rwanda", "description": "Urumuri est la plateforme de mobilité nouvelle génération du Rwanda : transport, livraison de repas, coursier, intelligence commerciale et autonomisation des chauffeurs."},
    "transport": {"title": "Urumuri Transport | Courses passagers premium", "description": "Urumuri Transport est le service phare de mobilité du Rwanda avec motos électriques, équipement de sécurité premium et réductions étudiants."},
    "food": {"title": "Urumuri Food | Restaurant, épicerie et achats pour vous", "description": "Urumuri Food livre repas, courses, produits de pharmacie et services d'achat pour vous avec rapidité et fiabilité premium."},
    "courier": {"title": "Urumuri Courier | Livraison professionnelle de colis", "description": "Urumuri Courier offre livraison de colis professionnels, documents, service le jour même et suivi sécurisé."},
    "merchants": {"title": "Urumuri Merchants | Intelligence et analyses", "description": "Urumuri Merchants fournit analyses des ventes, insights d'inventaire et recommandations IA pour la croissance des entreprises."},
    "drivers": {"title": "Urumuri Drivers | Revenus flexibles et croissance professionnelle", "description": "Rejoignez Urumuri comme chauffeur avec revenus flexibles, formation sécurité, motos électriques et opportunités de croissance."},
    "about": {"title": "À propos d'Urumuri | Mission, vision et valeurs", "description": "Découvrez la mission, la vision et les valeurs d'Urumuri. Une marque africaine de mobilité premium axée sur l'innovation, la sécurité et la communauté."},
    "contact": {"title": "Contact Urumuri | Bureau, support et demandes commerciales", "description": "Contactez Urumuri pour le support, les partenariats, les candidatures chauffeurs et les demandes commerçants."},
    "safety": {"title": "Urumuri Safety | Protection passagers, chauffeurs et colis", "description": "Urumuri Safety explique notre engagement pour la protection des passagers, l'équipement réfléchissant, la formation des chauffeurs et la sécurité des colis."},
    "reviews": {"title": "Laisser un avis | Urumuri", "description": "Partagez votre expérience Urumuri et aidez-nous à améliorer transport, nourriture et coursier au Rwanda."},
}

META_ZH: dict[str, dict[str, str]] = {
    "home": {"title": "Urumuri | 卢旺达智能出行生态系统", "description": "Urumuri 是卢旺达新一代出行平台，整合交通、餐饮配送、快递、商户智能和司机赋能。"},
    "transport": {"title": "Urumuri Transport | 高端乘客出行", "description": "Urumuri Transport 是卢旺达旗舰出行服务，提供电动摩托车、高端安全装备和学生优惠。"},
    "food": {"title": "Urumuri Food | 餐厅、杂货与代购", "description": "Urumuri Food 将餐厅餐食、杂货、药品和代购服务快速可靠地送到您家门口。"},
    "courier": {"title": "Urumuri Courier | 专业包裹配送", "description": "Urumuri Courier 提供商务包裹配送、文件处理、当日达和安全追踪。"},
    "merchants": {"title": "Urumuri Merchants | 智能与分析", "description": "Urumuri Merchants 提供销售分析、库存洞察和 AI 驱动的业务增长建议。"},
    "drivers": {"title": "Urumuri Drivers | 灵活收入与职业发展", "description": "加入 Urumuri 成为司机，享受灵活收入、安全培训、电动摩托车和成长机会。"},
    "about": {"title": "关于 Urumuri | 使命、愿景与价值观", "description": "了解 Urumuri 的使命、愿景和价值观。专注于创新、安全、社区和可持续发展的非洲高端出行品牌。"},
    "contact": {"title": "联系 Urumuri | 办公室、支持与商务咨询", "description": "联系 Urumuri 获取支持、合作、司机申请和商户咨询。"},
    "safety": {"title": "Urumuri Safety | 乘客、骑手与包裹保护", "description": "Urumuri Safety 介绍我们对乘客保护、反光装备、骑手培训和包裹安全的承诺。"},
    "reviews": {"title": "留下评价 | Urumuri", "description": "分享您的 Urumuri 体验，帮助我们改进卢旺达的出行、餐饮和快递服务。"},
}

META_RW: dict[str, dict[str, str]] = {
    "home": {"title": "Urumuri | Sisitemu y'ubwikorezi bw'ubwenge mu Rwanda", "description": "Urumuri ni urubuga rw'ubwikorezi rwo mu gihe gishya mu Rwanda ruhuza ubwikorezi, ibiryo, courier, ubwenge bw'abacuruzi n'abashoferi."},
    "transport": {"title": "Urumuri Transport | Ingendo z'abagenzi z'ubunararibonye", "description": "Urumuri Transport ni serivisi y'ubwikorezi y'ibanze mu Rwanda ifite moto z'amashanyarizi, ibikoresho by'umutekano n'igihango ku banyeshuri."},
    "food": {"title": "Urumuri Food | Restaurant, ibyagura n'ugura kuri mwe", "description": "Urumuri Food itanga ibiryo, ibyagura, imiti n'ibikorwa byo kugura kuri mwe mu vitesi n'ukwizera."},
    "courier": {"title": "Urumuri Courier | Kohereza ibipaki by'ubunararibonye", "description": "Urumuri Courier itanga kohereza ibipaki by'ubucuruzi, inyandiko, serivisi y'umunsi umwe n'ukurikirana kw'umutekano."},
    "merchants": {"title": "Urumuri Merchants | Ubwenge n'isesengura", "description": "Urumuri Merchants itanga isesengura ry'igurishwa, ubumenyi bw'ububiko n'inama z'AI zo gukura ubucuruzi."},
    "drivers": {"title": "Urumuri Drivers | Amafaranga yihuse n'iterambere ry'umwuga", "description": "Jya mu itsinda ry'abashoferi ba Urumuri ufite amafaranga yihuse, amahugurwa y'umutekano, moto z'amashanyarizi n'amahirwe yo gukura."},
    "about": {"title": "Ibyerekeye Urumuri | Intego, icyerekezo n'agaciro", "description": "Menya intego, icyerekezo n'agaciro ka Urumuri. Ikirango cy'ubwikorezi cy'ubunararibonye mu Afurika gishingiye ku guhanga udushya, umutekano n'umuryango."},
    "contact": {"title": "Twandikire Urumuri | Ibiro, ubufasha n'ibibazo by'ubucuruzi", "description": "Twandikire Urumuri ku bufasha, ubufatanye, gusaba kuba umushoferi n'ibibazo by'abacuruzi."},
    "safety": {"title": "Urumuri Safety | Kurinda abagenzi, abashoferi n'ibipaki", "description": "Urumuri Safety isobanura umuhamagaro wacu wo kurinda abagenzi, ibikoresho by'umucyo, amahugurwa y'abashoferi n'umutekano w'ibipaki."},
    "reviews": {"title": "Tanga igitekerezo | Urumuri", "description": "Sangiza uburambe bwawe na Urumuri ukadufasha kunoza ubwikorezi, ibiryo na courier mu Rwanda."},
}

META_BY_LANG = {"en": META_EN, "fr": META_FR, "zh": META_ZH, "rw": META_RW}


def extract_en_from_script() -> dict[str, Any]:
    text = SCRIPT_JS.read_text(encoding="utf-8")
    marker = "const translations = "
    start = text.index(marker) + len(marker)
    depth = 0
    for i in range(start, len(text)):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                data = json.loads(text[start : i + 1])
                return data["en"]
    raise ValueError("Could not parse translations block in script.js")


def deep_translate(obj: Any, mapping: dict[str, str]) -> Any:
    if isinstance(obj, dict):
        return {k: deep_translate(v, mapping) for k, v in obj.items()}
    if isinstance(obj, list):
        return [deep_translate(v, mapping) for v in obj]
    if isinstance(obj, str):
        return mapping.get(obj, obj)
    return obj


def ensure_triples() -> None:
    if TRIPLES_FILE.exists():
        return
    build_script = ROOT / "_build_triples.py"
    if not build_script.exists():
        raise SystemExit(f"Missing {TRIPLES_FILE.name} and {build_script.name}")
    import subprocess
    import sys

    subprocess.run([sys.executable, str(build_script)], check=True)


def _load_triples() -> dict[str, dict[str, str]]:
    ensure_triples()
    return json.loads(TRIPLES_FILE.read_text(encoding="utf-8"))


_triples = _load_triples()
FR_MAP: dict[str, str] = _triples["fr"]
ZH_MAP: dict[str, str] = _triples["zh"]
RW_MAP: dict[str, str] = _triples["rw"]


def build_meta(lang: str) -> dict[str, dict[str, str]]:
    return META_BY_LANG[lang]


def build_translations(en: dict[str, Any]) -> dict[str, Any]:
    en = json.loads(json.dumps(en))
    en.setdefault("ui", {})
    en["ui"]["languageOptions"] = {
        "en": "English",
        "fr": "Français",
        "zh": "中文",
        "rw": "Kinyarwanda",
    }
    en["meta"] = META_EN

    translations = {
        "en": en,
        "fr": deep_translate(en, FR_MAP),
        "zh": deep_translate(en, ZH_MAP),
        "rw": deep_translate(en, RW_MAP),
    }
    for lang in ("fr", "zh", "rw"):
        translations[lang]["meta"] = build_meta(lang)
        translations[lang].setdefault("ui", {})["languageOptions"] = en["ui"]["languageOptions"]
    return translations


def flatten_strings(obj: Any, out: set[str] | None = None) -> set[str]:
    out = out or set()
    if isinstance(obj, dict):
        for v in obj.values():
            flatten_strings(v, out)
    elif isinstance(obj, list):
        for v in obj:
            flatten_strings(v, out)
    elif isinstance(obj, str):
        out.add(obj)
    return out


def coverage_stats(en_string_list: list[str], mapping: dict[str, str]) -> tuple[int, int, float]:
    total = len(en_string_list)
    translated = sum(
        1
        for s in en_string_list
        if s in KEEP_AS_IS or mapping.get(s, s) != s
    )
    pct = (translated / total * 100) if total else 100.0
    return translated, total, pct


def write_i18n_data(translations: dict[str, Any]) -> None:
    I18N_DATA.write_text(
        "# Auto-generated by generate_i18n.py\n"
        "TRANSLATIONS = "
        + json.dumps(translations, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )


def _read_build_script_part(name: str) -> str:
    text = (ROOT / "build_script.py").read_text(encoding="utf-8")
    if name == "PAGE_SELECTORS":
        m = re.search(r"PAGE_SELECTORS_JS = '''(.+?)'''", text, re.DOTALL)
        return m.group(1) if m else ""
    if name == "FOOTER":
        m = re.search(r"FOOTER_JS = r'''(.+?)'''", text, re.DOTALL)
        return m.group(1) if m else ""
    raise KeyError(name)


HEADER_JS = r"""(function () {
  'use strict';

  const STORAGE_LANG = 'urumuri-language';
  const STORAGE_THEME = 'urumuri-theme';
  const LANGS = ['en', 'fr', 'zh', 'rw'];

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
      label.innerHTML = '<span class="sr-only">Choose language</span><select id="languagePicker" aria-label="Choose language"><option value="en">English</option><option value="fr">Français</option><option value="zh">中文</option><option value="rw">Kinyarwanda</option></select>';
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
    document.documentElement.lang = lang === 'zh' ? 'zh-CN' : (lang === 'fr' ? 'fr' : (lang === 'rw' ? 'rw' : 'en'));
    document.body.dataset.language = lang;
    localStorage.setItem(STORAGE_LANG, lang);
    applyNav(t);
    applyFooter(t);
    applySelectorMap(t, getPageKey());
    applyDataAttributes(t);
    const pageMeta = t.meta?.[getPageKey()];
    if (pageMeta) {
      if (pageMeta.title) document.title = pageMeta.title;
      const desc = document.querySelector('meta[name="description"]');
      if (desc && pageMeta.description) desc.setAttribute('content', pageMeta.description);
    }
    if (languagePicker && languagePicker.value !== lang) languagePicker.value = lang;
    if (t.ui?.languageOptions && languagePicker) {
      const opts = languagePicker.options;
      ['en', 'fr', 'zh', 'rw'].forEach((code, i) => {
        if (opts[i] && t.ui.languageOptions[code]) opts[i].textContent = t.ui.languageOptions[code];
      });
    }
    if (themeToggle) themeToggle.setAttribute('aria-label', t.ui?.themeToggle || 'Toggle light and dark mode');
    if (languagePicker) languagePicker.setAttribute('aria-label', t.ui?.languagePicker || 'Choose language');
  };

"""


def regenerate_script_js(translations: dict[str, Any]) -> int:
    page_selectors = _read_build_script_part("PAGE_SELECTORS")
    footer_js = _read_build_script_part("FOOTER")
    body = (
        HEADER_JS
        + page_selectors
        + "\n  const translations = "
        + json.dumps(translations, ensure_ascii=False, indent=2)
        + ";\n"
        + footer_js
    )
    SCRIPT_JS.write_text(body, encoding="utf-8")
    return body.count("\n") + (0 if body.endswith("\n") else 1)


def validate_maps(en_strings: set[str]) -> None:
    for name, m in (("fr", FR_MAP), ("zh", ZH_MAP), ("rw", RW_MAP)):
        missing = sorted(en_strings - set(m))
        if missing:
            raise SystemExit(f"{name} map missing {len(missing)} keys, e.g. {missing[:3]}")


def main() -> None:
    en = extract_en_from_script()
    en_string_list = json.loads(EN_STRINGS_FILE.read_text(encoding="utf-8"))
    validate_maps(set(en_string_list))
    translations = build_translations(en)
    write_i18n_data(translations)
    lines = regenerate_script_js(translations)
    print(f"Wrote {I18N_DATA}")
    print(f"Regenerated {SCRIPT_JS} ({lines} lines, {SCRIPT_JS.stat().st_size} bytes)")
    print("Languages: en, fr, zh, rw")
    for lang in ("fr", "zh", "rw"):
        tr, total, pct = coverage_stats(en_string_list, {"fr": FR_MAP, "zh": ZH_MAP, "rw": RW_MAP}[lang])
        print(f"  {lang}: {tr}/{total} translated ({pct:.1f}%)")


if __name__ == "__main__":
    main()
