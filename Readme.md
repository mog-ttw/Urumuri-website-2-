# Urumuri — Rwanda's Intelligent Mobility Ecosystem

A multi-page marketing website for **Urumuri**, a next-generation mobility platform serving Kigali and nearby districts in Rwanda. The site covers transport, food delivery, courier services, merchant tools, driver programs, safety, and contact — built with pure HTML, CSS, and JavaScript.

---

## Quick start (for presenting)

### Option 1 — Launch script (recommended)

```bash
cd /Users/Daniel/Desktop/Urumuri
chmod +x present.sh
./present.sh
```

This starts a local server and opens the homepage in your default browser.

### Option 2 — Manual

```bash
cd /Users/Daniel/Desktop/Urumuri
python3 -m http.server 8765
```

Then open [http://localhost:8765/index.html](http://localhost:8765/index.html) in your browser.

> **Tip:** Use full-screen mode (`F11` on Windows/Linux, `Ctrl+Cmd+F` on Mac) and zoom to 100% before you present.

---

## Site map

| Page | File | What to show |
|------|------|--------------|
| Home | `index.html` | Brand story, three core services, stats, ecosystem overview |
| Transport | `transport.html` | Electric rides, safety gear, student discounts |
| Food | `food.html` | Restaurant & grocery delivery |
| Courier | `courier.html` | Package delivery, same-day options |
| Merchants | `merchants.html` | Business analytics and partnership tools |
| Drivers | `drivers.html` | Driver recruitment, training, electric fleet |
| About | `about.html` | Mission, vision, values |
| Safety | `safety.html` | Safety standards and emergency support |
| Contact | `contact.html` | Office, phone, email, WhatsApp |
| Reviews | `reviews.html` | Customer review form |

---

## Key features to demo live

1. **Homepage hero** — headline, stats (24/7, 200+ fleet, trusted across Kigali), and animated service panels.
2. **Service cards** — click through Transport, Food, and Courier pages.
3. **Dark / light mode** — toggle in the top-right header (moon/sun icon).
4. **Language switcher** — English, Français, 中文, Kinyarwanda (auto-injected by `script.js`).
5. **Scroll animations** — scroll down on any page to show staggered card entrances.
6. **Mobile layout** — resize the browser or use DevTools device mode to show the hamburger menu.
7. **Contact & social** — WhatsApp link, Instagram, X, Facebook in the footer.

---

## Brand & design

| Element | Value |
|---------|-------|
| Primary navy | `#0B1F3A` |
| Royal blue | `#1f4f92` |
| Gold accent | `#ffd700` / `#D4AF37` |
| Headings font | Bricolage Grotesque |
| Body font | DM Sans |
| Style | Human, playful motion — bounce entrances, slight card tilt, no heavy glass/AI effects |

---

## Tech stack

- **HTML5** — semantic, multi-page structure
- **CSS3** — custom properties, responsive grid, scroll/hover animations
- **JavaScript (vanilla)** — navigation, theme toggle, i18n, scroll observer, parallax, review form
- **No build step** — open or serve the folder directly

---

## Project structure

```
Urumuri/
├── index.html              # Homepage
├── transport.html          # Transport service page
├── food.html               # Food delivery page
├── courier.html            # Courier service page
├── merchants.html          # Merchant partnerships
├── drivers.html            # Driver program
├── about.html              # Mission, vision, values
├── safety.html             # Safety information
├── contact.html            # Contact details
├── reviews.html            # Customer review form
├── styles.css              # Global styles and animations
├── script.js               # Interactivity, i18n, theme
├── translations.json       # Translation strings
├── present.sh              # One-command demo launcher
├── PRESENTATION-SCRIPT.md  # Verbal walkthrough script
└── Readme.md               # This file
```

---

## Presentation checklist

Before you go live:

- [ ] Run `./present.sh` and confirm the site loads
- [ ] Test dark mode toggle
- [ ] Switch language once to show i18n works
- [ ] Have Transport, About, and Contact pages ready to click
- [ ] Close unrelated browser tabs
- [ ] Turn off notifications / Do Not Disturb
- [ ] Read through `PRESENTATION-SCRIPT.md` once

---

## Contact (from the site)

- **Phone:** +250 788 246 777
- **Email:** info@urumuri.rw
- **Office:** Kigali Innovation District, Kigali, Rwanda
- **WhatsApp:** [+250 788 246 777](https://api.whatsapp.com/send/?phone=%2B250788246777)

---

## License

© 2026 Urumuri. All rights reserved.
