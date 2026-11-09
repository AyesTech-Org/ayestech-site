#!/usr/bin/env python3
"""ayestech.com static site generator.

Every page shares one shell (head, header/nav, footer, CSS, JS) so the
navigation can never drift between pages. Run from anywhere:

    python3 tools/build.py

Output is written next to this folder (repository root), which GitHub
Pages serves as-is. Legal pages under /pdf-reader/ are linked from the
App Store listing of ListenFly - keep their paths stable.
"""
from __future__ import annotations

import datetime as _dt
import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = "https://ayestech.com"
LISTENFLY_SITE = "https://listenfly.ayestech.com"
APP_STORE = "https://apps.apple.com/app/listenfly/id6795153598"
EMAIL = "info@ayestech.com"
PHONE = "+31 642 55 7383"
PHONE_HREF = "tel:+31642557383"
YEAR = _dt.date.today().year

# ---------------------------------------------------------------------------
# Shell
# ---------------------------------------------------------------------------

CSS = r"""
:root{
  --bg:#f6f8fb;--surface:#ffffff;--surface-2:#eef2f7;--text:#0f172a;--muted:#4b5563;--line:#dfe5ee;
  --brand:#0f172a;--accent:#1d4ed8;--accent-strong:#1e40af;--accent-soft:#dbe7ff;--accent-ink:#ffffff;
  --ok:#047857;--radius:18px;--radius-sm:12px;--shadow:0 12px 32px rgba(15,23,42,.08);--shadow-sm:0 2px 8px rgba(15,23,42,.06);
  --max:1120px;--gutter:16px;color-scheme:light dark;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#0b1020;--surface:#121a2e;--surface-2:#182239;--text:#e6eaf2;--muted:#a3adc2;--line:#24304a;
    --brand:#e6eaf2;--accent:#6ea0ff;--accent-strong:#8bb3ff;--accent-soft:#1b2a52;--accent-ink:#0b1020;
    --ok:#34d399;--shadow:0 12px 32px rgba(0,0,0,.35);--shadow-sm:0 2px 8px rgba(0,0,0,.3);
  }
}
:root[data-theme="dark"]{
  --bg:#0b1020;--surface:#121a2e;--surface-2:#182239;--text:#e6eaf2;--muted:#a3adc2;--line:#24304a;
  --brand:#e6eaf2;--accent:#6ea0ff;--accent-strong:#8bb3ff;--accent-soft:#1b2a52;--accent-ink:#0b1020;
  --ok:#34d399;--shadow:0 12px 32px rgba(0,0,0,.35);--shadow-sm:0 2px 8px rgba(0,0,0,.3);
}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.6 "Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;overflow-x:hidden}
img{max-width:100%;height:auto;display:block}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
h1,h2,h3,h4{line-height:1.15;margin:0 0 .5em;letter-spacing:-.02em;color:var(--text)}
h1{font-size:clamp(2rem,5.2vw,3.4rem);font-weight:800}
h2{font-size:clamp(1.6rem,3.4vw,2.25rem);font-weight:800}
h3{font-size:1.15rem;font-weight:700}
p{margin:0 0 1em}
ul{padding-left:1.2em}
.container{width:100%;max-width:var(--max);margin:0 auto;padding:0 var(--gutter)}
.skip{position:absolute;left:-999px;top:8px;background:var(--accent);color:var(--accent-ink);padding:8px 12px;border-radius:8px;z-index:100}
.skip:focus{left:8px}

/* Header */
.site-header{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--bg) 86%,transparent);backdrop-filter:saturate(180%) blur(14px);-webkit-backdrop-filter:saturate(180%) blur(14px);border-bottom:1px solid var(--line)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:16px;height:68px}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:1.15rem;color:var(--text);letter-spacing:-.01em}
.brand:hover{text-decoration:none}
.brand img{width:36px;height:36px;border-radius:9px}
.site-nav{display:flex;align-items:center;gap:6px}
.site-nav a{color:var(--text);font-weight:600;padding:8px 12px;border-radius:10px;font-size:.95rem}
.site-nav a:hover{background:var(--surface-2);text-decoration:none}
.site-nav a[aria-current="page"]{color:var(--accent)}
.site-nav .btn{margin-left:8px}
.nav-toggle{display:none;width:44px;height:44px;border:1px solid var(--line);background:var(--surface);border-radius:12px;cursor:pointer;padding:0;align-items:center;justify-content:center;flex-direction:column;gap:5px}
.nav-toggle span{display:block;width:20px;height:2px;background:var(--text);border-radius:2px;transition:transform .2s,opacity .2s}
.nav-toggle[aria-expanded="true"] span:nth-child(1){transform:translateY(7px) rotate(45deg)}
.nav-toggle[aria-expanded="true"] span:nth-child(2){opacity:0}
.nav-toggle[aria-expanded="true"] span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
@media (max-width: 880px){
  .nav-toggle{display:flex}
  .site-nav{position:absolute;left:0;right:0;top:68px;display:none;flex-direction:column;align-items:stretch;gap:2px;padding:10px var(--gutter) 16px;background:var(--surface);border-bottom:1px solid var(--line);box-shadow:var(--shadow)}
  .site-nav.open{display:flex}
  .site-nav a{padding:13px 12px;font-size:1.05rem}
  .site-nav .btn{margin:8px 0 0;text-align:center}
}

/* Buttons */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:12px 20px;border-radius:12px;font-weight:700;border:1px solid transparent;cursor:pointer;transition:transform .15s,box-shadow .15s,background .15s}
.btn:hover{text-decoration:none;transform:translateY(-1px)}
.btn-primary{background:var(--accent);color:var(--accent-ink)}
.btn-primary:hover{background:var(--accent-strong);box-shadow:var(--shadow-sm)}
.btn-secondary{background:var(--surface);color:var(--text);border-color:var(--line)}
.btn-secondary:hover{background:var(--surface-2)}
.btn-sm{padding:9px 14px;font-size:.92rem}
.btn-row{display:flex;flex-wrap:wrap;gap:12px}

/* Layout blocks */
section{padding:64px 0}
@media (min-width: 880px){section{padding:92px 0}}
.section-head{max-width:720px;margin-bottom:36px}
.eyebrow{display:inline-block;font-size:.78rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin-bottom:12px}
.lead{font-size:1.15rem;color:var(--muted);max-width:60ch}
.grid{display:grid;gap:18px}
.grid-2{grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr))}
.grid-3{grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr))}
.grid-4{grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr))}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:26px;box-shadow:var(--shadow-sm);transition:transform .2s,box-shadow .2s,border-color .2s}
.card:hover{transform:translateY(-3px);box-shadow:var(--shadow);border-color:color-mix(in srgb,var(--accent) 35%,var(--line))}
.card h3{margin-top:14px}
.card p{color:var(--muted);margin-bottom:0}
.card .icon{width:44px;height:44px;border-radius:12px;background:var(--accent-soft);color:var(--accent);display:flex;align-items:center;justify-content:center}
.card .icon svg{width:22px;height:22px}
.card ul{color:var(--muted);margin:12px 0 0;padding-left:1.1em}
.card li{margin:4px 0}
a.card{color:inherit;display:block}
a.card:hover{text-decoration:none}
.card .more{display:inline-block;margin-top:14px;color:var(--accent);font-weight:600}
.muted{color:var(--muted)}
.alt{background:var(--surface-2)}
.tight{padding-top:0}

/* Hero */
.hero{padding:56px 0 48px;position:relative;overflow:hidden}
@media (min-width: 880px){.hero{padding:96px 0 80px}}
.hero::before{content:"";position:absolute;inset:0;background:
  radial-gradient(600px 300px at 10% 0%,color-mix(in srgb,var(--accent) 16%,transparent),transparent 70%),
  radial-gradient(500px 260px at 90% 20%,color-mix(in srgb,var(--accent) 10%,transparent),transparent 70%);pointer-events:none}
.hero .container{position:relative;display:grid;gap:36px;align-items:center}
@media (min-width: 960px){.hero .container{grid-template-columns:1.15fr .85fr}}
.hero h1{margin-bottom:18px}
.hero .lead{font-size:1.2rem;margin-bottom:26px}
.panel{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:22px;box-shadow:var(--shadow)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:14px}
.stat{padding:14px;border-radius:var(--radius-sm);background:var(--surface-2)}
.stat b{display:block;font-size:clamp(1.25rem,4.6vw,1.6rem);font-weight:800;letter-spacing:-.02em;color:var(--text);white-space:nowrap}
.stat span{font-size:.9rem;color:var(--muted)}
.panel .foot{margin:16px 0 0;font-size:.9rem;color:var(--muted)}
.strip{border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:var(--surface);padding:16px 0}
.strip .container{display:flex;flex-wrap:wrap;gap:8px 22px;justify-content:center;font-weight:600;font-size:.92rem;color:var(--muted)}
.strip span::before{content:"";display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--accent);margin-right:8px;vertical-align:middle}

/* Feature rows */
.split{display:grid;gap:28px;align-items:center}
@media (min-width: 900px){.split{grid-template-columns:1fr 1fr;gap:48px}.split.rev > :first-child{order:2}}
.split img{border-radius:var(--radius)}
.checks{list-style:none;padding:0;margin:18px 0 24px}
.checks li{padding-left:30px;position:relative;margin:10px 0;color:var(--text)}
.checks li::before{content:"";position:absolute;left:0;top:5px;width:18px;height:18px;border-radius:50%;background:var(--accent-soft)}
.checks li::after{content:"";position:absolute;left:6px;top:9px;width:6px;height:9px;border:solid var(--accent);border-width:0 2px 2px 0;transform:rotate(45deg)}

/* Steps */
.steps{counter-reset:step}
.step{position:relative;padding-top:8px}
.step .num{font-size:.8rem;font-weight:800;letter-spacing:.12em;color:var(--accent)}
.step h3{margin:6px 0 4px}
.step .sub{font-weight:600;color:var(--text);margin:0 0 6px}

/* Product card */
.product{display:grid;gap:28px;align-items:center;background:var(--surface);border:1px solid var(--line);border-radius:24px;padding:28px;box-shadow:var(--shadow)}
@media (min-width: 900px){.product{grid-template-columns:1fr 1fr;padding:44px}}
.product .app{display:flex;align-items:center;gap:14px;margin-bottom:14px}
.product .app img{width:56px;height:56px;border-radius:14px;box-shadow:var(--shadow-sm)}
.product .app b{font-size:1.25rem}
.product .app span{display:block;color:var(--muted);font-size:.9rem}

/* CTA band */
.cta{background:linear-gradient(135deg,#0f172a,#1e3a8a);color:#fff;border-radius:24px;padding:36px 28px;display:grid;gap:22px;align-items:center}
@media (min-width: 900px){.cta{grid-template-columns:1.3fr .7fr;padding:52px}}
.cta h2,.cta p{color:#fff}
.cta p{color:#c7d2fe}
.cta .btn-primary{background:#fff;color:#0f172a}
.cta .btn-primary:hover{background:#e0e7ff}
.cta .btn-secondary{background:transparent;color:#fff;border-color:rgba(255,255,255,.35)}
.cta .btn-secondary:hover{background:rgba(255,255,255,.08)}
.cta ul{margin:0;padding-left:1.1em;color:#e0e7ff}

/* Page header */
.page-head{padding:52px 0 36px}
@media (min-width: 880px){.page-head{padding:76px 0 48px}}
.page-head h1{margin-bottom:12px}

/* Prose (legal pages) */
.prose{max-width:760px}
.prose h2{font-size:1.35rem;margin-top:2.2em}
.prose h2 .n{display:inline-block;min-width:34px;height:34px;line-height:34px;text-align:center;border-radius:10px;background:var(--accent-soft);color:var(--accent);font-size:.95rem;margin-right:10px;vertical-align:middle}
.prose p,.prose li{color:var(--text)}
.prose .summary{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:var(--radius-sm);padding:18px 20px}
.prose .meta{color:var(--muted);font-size:.95rem}
.toc{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-sm);padding:16px 20px;margin:24px 0}
.toc ol{margin:0;padding-left:1.3em;columns:2;column-gap:28px}
@media (max-width: 640px){.toc ol{columns:1}}
.toc li{margin:4px 0;break-inside:avoid}
.subnav{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 8px}
.subnav a{padding:7px 12px;border:1px solid var(--line);border-radius:999px;background:var(--surface);color:var(--text);font-size:.9rem;font-weight:600}
.subnav a[aria-current="page"]{border-color:var(--accent);color:var(--accent)}
.subnav a:hover{text-decoration:none;background:var(--surface-2)}

/* Contact */
.contact-card dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:10px 18px}
.contact-card dt{font-weight:700}
.contact-card dd{margin:0}

/* Footer */
.site-footer{border-top:1px solid var(--line);background:var(--surface);padding:48px 0 28px;margin-top:40px}
.footer-grid{display:grid;gap:28px;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr))}
.footer-grid h4{font-size:.85rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:12px}
.footer-grid ul{list-style:none;padding:0;margin:0}
.footer-grid li{margin:8px 0}
.footer-grid a{color:var(--text)}
.footer-brand p{color:var(--muted);max-width:34ch}
.footer-bottom{display:flex;flex-wrap:wrap;gap:10px 20px;justify-content:space-between;margin-top:36px;padding-top:20px;border-top:1px solid var(--line);color:var(--muted);font-size:.9rem}

/* Reveal */
@media (prefers-reduced-motion: no-preference){
  .reveal{opacity:0;transform:translateY(14px);transition:opacity .5s ease,transform .5s ease}
  .reveal.in{opacity:1;transform:none}
}
"""

JS = r"""
(function(){
  var toggle=document.querySelector('.nav-toggle'),nav=document.getElementById('site-nav');
  if(toggle&&nav){
    toggle.addEventListener('click',function(){
      var open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',open?'true':'false');
    });
    nav.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');});});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'){nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');}});
    document.addEventListener('click',function(e){if(!nav.contains(e.target)&&!toggle.contains(e.target)){nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');}});
  }
  var path=location.pathname.replace(/index\.html$/,'');
  document.querySelectorAll('.site-nav a').forEach(function(a){
    var href=a.getAttribute('href');
    if(href&&href.indexOf('/')===0&&(href===path||(href!=='/'&&path.indexOf(href)===0))){a.setAttribute('aria-current','page');}
  });
  document.querySelectorAll('.subnav a').forEach(function(a){
    if(a.getAttribute('href')===path){a.setAttribute('aria-current','page');}else{a.removeAttribute('aria-current');}
  });
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(entries){entries.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target);}});},{rootMargin:'0px 0px -8% 0px'});
    document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});
  }else{document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in');});}
})();
"""

NAV_LINKS = [
    ("/services/", "Services"),
    ("/projects/", "Projects"),
    ("/pdf-reader/", "ListenFly"),
    ("/about/", "About"),
]


def shell(*, title: str, description: str, path: str, body: str, extra_head: str = "") -> str:
    nav = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV_LINKS)
    canonical = SITE + path
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="AyesTech">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/og-image.png">
<meta name="theme-color" content="#f6f8fb" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0b1020" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/assets/icon-192.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
<style>{CSS}</style>
{extra_head}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container nav">
    <a class="brand" href="/"><img src="/assets/ayestech-logo.png" alt="" width="36" height="36">AyesTech</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu"><span></span><span></span><span></span></button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      {nav}
      <a class="btn btn-primary btn-sm" href="/contact/">Start a project</a>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="/"><img src="/assets/ayestech-logo.png" alt="" width="36" height="36">AyesTech</a>
        <p>Engineering company delivering AI-integrated hardware, embedded, cloud and mobile products for automotive, medical and industrial teams.</p>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="/services/">Services</a></li>
          <li><a href="/projects/">Projects</a></li>
          <li><a href="/about/">About</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Products</h4>
        <ul>
          <li><a href="{LISTENFLY_SITE}">ListenFly</a></li>
          <li><a href="{APP_STORE}">ListenFly on the App Store</a></li>
          <li><a href="https://taskmanager.ayestech.com/">Task Manager</a></li>
        </ul>
      </div>
      <div>
        <h4>ListenFly legal</h4>
        <ul>
          <li><a href="/pdf-reader/privacy/">Privacy Policy</a></li>
          <li><a href="/pdf-reader/terms/">Terms of Service</a></li>
          <li><a href="/pdf-reader/support/">Support</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{PHONE_HREF}">{PHONE}</a></li>
          <li class="muted">Netherlands · serving Europe, US and Canada</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© {YEAR} AyesTech. All rights reserved.</span>
      <span>ayestech.com</span>
    </div>
  </div>
</footer>
<script>{JS}</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Reusable pieces
# ---------------------------------------------------------------------------

ICONS = {
    "ai": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="3"/><path d="M9 9h6v6H9z"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M7 2v2M17 2v2M7 20v2M17 20v2M2 7h2M2 17h2M20 7h2M20 17h2"/></svg>',
    "chip": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h3l2-4 3 8 2-4h6"/><rect x="2" y="3" width="20" height="18" rx="3"/></svg>',
    "cloud": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7 18a4 4 0 0 1-.6-7.95A6 6 0 0 1 18 9a4.5 4.5 0 0 1-.5 9H7z"/></svg>',
    "board": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="8" cy="12" r="1.6"/><circle cx="16" cy="12" r="1.6"/><path d="M8 5V3M16 5V3M8 21v-2M16 21v-2"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 12l2 2 4-5"/><path d="M12 3l7 3v5c0 5-3.5 8.5-7 10-3.5-1.5-7-5-7-10V6z"/></svg>',
    "team": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.2"/><circle cx="17" cy="9" r="2.4"/><path d="M3 19a6 6 0 0 1 12 0"/><path d="M15 19a4.5 4.5 0 0 1 6 0"/></svg>',
    "car": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 13l2-5h14l2 5v5H3z"/><circle cx="7.5" cy="17" r="1.6"/><circle cx="16.5" cy="17" r="1.6"/><path d="M5 13h14"/></svg>',
    "med": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l2-5 3 10 2-5h7"/></svg>',
    "iot": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="2.5"/><path d="M4 12a8 8 0 0 1 8-8M20 12a8 8 0 0 1-8 8M7.5 7.5a6.4 6.4 0 0 0 0 9M16.5 7.5a6.4 6.4 0 0 1 0 9"/></svg>',
}


def card(icon: str, title: str, text: str, bullets: list[str] | None = None, href: str | None = None, more: str | None = None) -> str:
    items = "".join(f"<li>{b}</li>" for b in bullets or [])
    inner = f'<div class="icon">{ICONS[icon]}</div><h3>{title}</h3><p>{text}</p>' + (f"<ul>{items}</ul>" if items else "") + (f'<span class="more">{more} →</span>' if more else "")
    if href:
        return f'<a class="card reveal" href="{href}">{inner}</a>'
    return f'<div class="card reveal">{inner}</div>'


def cta_band(title: str, text: str, primary=("Start a project", "/contact/"), secondary=("Email us", f"mailto:{EMAIL}"), bullets: list[str] | None = None) -> str:
    items = "".join(f"<li>{b}</li>" for b in bullets or [])
    aside = f'<div><p style="margin-bottom:10px"><strong>What you get in the first week</strong></p><ul>{items}</ul></div>' if items else ""
    return f"""
<section class="tight">
  <div class="container">
    <div class="cta reveal">
      <div>
        <h2>{title}</h2>
        <p>{text}</p>
        <div class="btn-row">
          <a class="btn btn-primary" href="{primary[1]}">{primary[0]}</a>
          <a class="btn btn-secondary" href="{secondary[1]}">{secondary[0]}</a>
        </div>
      </div>
      {aside}
    </div>
  </div>
</section>
"""


FIRST_WEEK = [
    "Architecture and risk snapshot for your current scope",
    "Priority backlog with effort ranges and delivery phases",
    "Recommended team setup and communication cadence",
]

SERVICE_CARDS = [
    ("ai", "Applied AI integration",
     "Speech, vision and language models embedded in real products – on the device where privacy and latency matter, in the cloud where scale matters.",
     ["Model selection and optimisation for constrained hardware", "On-device inference, offline operation, privacy by design", "AI-assisted features in web and mobile applications"]),
    ("chip", "Embedded &amp; connectivity",
     "Firmware, CAN-Bus, automotive Ethernet, secure communication and diagnostics for devices that must run reliably for years.",
     ["Bare-metal and RTOS firmware", "Vehicle networks, OBD-II and diagnostics interfaces", "Secure boot, updates and communication"]),
    ("cloud", "Cloud, web &amp; mobile",
     "Operator dashboards, companion apps and backend systems integrated with field devices and business workflows.",
     ["iOS and Android companion apps", "Web dashboards and APIs", "Telemetry pipelines and remote monitoring"]),
    ("board", "Hardware design &amp; manufacturing",
     "PCB, mechanical enclosure, DFM and supplier coordination for robust production.",
     ["Schematic and layout", "Enclosure design and prototyping", "Design for manufacturing and supplier hand-over"]),
    ("check", "Testing &amp; compliance",
     "Verification planning, traceability and support through certification milestones in regulated industries.",
     ["Requirements and traceability", "Verification and validation planning", "Documentation for certification bodies"]),
    ("team", "Dedicated engineering pods",
     "Cross-functional squads that blend with your internal teams, tools and reporting cadence.",
     ["Monthly capacity with a named lead", "Your backlog, your tooling, your reviews", "Scale up or down at milestone gates"]),
]


def service_grid(detailed: bool) -> str:
    cards = []
    for icon, title, text, bullets in SERVICE_CARDS:
        cards.append(card(icon, title, text, bullets if detailed else None, href=None if detailed else "/services/", more=None if detailed else "Learn more"))
    return f'<div class="grid grid-3">{"".join(cards)}</div>'


PROJECT_CARDS = [
    ("car", "Automotive electronics",
     "AVAS ECU, OBD-II tooling, EV communication modules and diagnostics interfaces.",
     ["Acoustic vehicle alerting (AVAS) control units", "OBD-II and diagnostics tooling", "EV charging and communication modules"]),
    ("med", "Medical devices",
     "Safety-critical electronics and software support for connected healthcare products.",
     ["Device firmware with traceable requirements", "Companion and operator applications", "Support through certification milestones"]),
    ("iot", "Industrial IoT",
     "Telemetry, remote monitoring and control systems built for uptime and security.",
     ["Edge devices and gateways", "Secure telemetry and fleet monitoring", "Dashboards for operations teams"]),
]


def project_grid(detailed: bool) -> str:
    cards = [card(icon, title, text, bullets if detailed else None, href=None if detailed else "/projects/", more=None if detailed else "See project areas") for icon, title, text, bullets in PROJECT_CARDS]
    return f'<div class="grid grid-3">{"".join(cards)}</div>'


PROCESS = [
    ("01", "Discovery", "Requirements &amp; constraints", "Business goals, technical feasibility and risk mapping. A written assessment within 48 hours of receiving your scope."),
    ("02", "Architecture", "System design", "Hardware/software architecture, where AI adds value and where it does not, and a development plan with decision gates."),
    ("03", "Build", "Iterative implementation", "Prototype-to-production with regular demos, validation and a backlog you can see at any time."),
    ("04", "Scale", "Launch &amp; sustain", "Compliance support, hand-over, operations and long-term product evolution."),
]


def process_grid() -> str:
    steps = "".join(f'<div class="step card reveal"><span class="num">{n}</span><h3>{t}</h3><p class="sub">{s}</p><p>{d}</p></div>' for n, t, s, d in PROCESS)
    return f'<div class="grid grid-4 steps">{steps}</div>'


def listenfly_product(compact: bool = False) -> str:
    return f"""
<div class="product reveal">
  <div>
    <div class="app"><img src="/assets/listenfly-icon.png" alt="ListenFly app icon" width="56" height="56"><div><b>ListenFly</b><span>iPhone app · built and operated by AyesTech</span></div></div>
    <h3 style="font-size:1.5rem">Your documents, read aloud – with AI voices that run on the phone.</h3>
    <p class="muted">PDFs, e-books, Word files, web articles and scanned pages become natural audio. Hundreds of AI voices in 35 languages run entirely on the device, offline, with no account and no upload of the user's library. ListenFly is our reference for what on-device AI can do on consumer hardware.</p>
    <ul class="checks">
      <li>On-device neural text-to-speech in 35 languages</li>
      <li>Word-by-word highlighting, screen-off listening</li>
      <li>Camera scanning with text recognition</li>
      <li>Privacy by design: no account, documents never leave the phone</li>
    </ul>
    <div class="btn-row">
      <a class="btn btn-primary" href="{LISTENFLY_SITE}">Visit listenfly.ayestech.com</a>
      <a class="btn btn-secondary" href="{APP_STORE}">Download on the App Store</a>
    </div>
  </div>
  <img src="/assets/listenfly-iphone.png" alt="ListenFly on iPhone: narrator selection, reading view with highlighted word, and library" width="1400" height="974" loading="lazy">
</div>
"""


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def page_home() -> str:
    body = f"""
<section class="hero">
  <div class="container">
    <div>
      <span class="eyebrow">Engineering partner for AI-integrated products</span>
      <h1>AI-integrated embedded and web products, built by a compact senior team.</h1>
      <p class="lead">AyesTech designs, builds and launches production-ready hardware, firmware, cloud and mobile systems for automotive, medical and industrial companies – and brings applied AI into them where it creates measurable value, at a cost structure larger agencies cannot match.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="/contact/">Start a project</a>
        <a class="btn btn-secondary" href="/projects/">See project areas</a>
      </div>
    </div>
    <div class="panel reveal">
      <div class="stats">
        <div class="stat"><b>48 h</b><span>Technical assessment of your scope</span></div>
        <div class="stat"><b>7+ yrs</b><span>Average engineering experience</span></div>
        <div class="stat"><b>3 domains</b><span>Automotive, medical, industrial</span></div>
        <div class="stat"><b>EU · US · CA</b><span>Delivery footprint from the Netherlands</span></div>
      </div>
      <p class="foot">One integrated team from hardware to cloud. Milestone-based delivery aligned with your budget gates.</p>
    </div>
  </div>
</section>

<div class="strip"><div class="container">
  <span>Hardware</span><span>Firmware</span><span>Connectivity</span><span>Cloud</span><span>Mobile</span><span>Applied AI</span>
</div></div>

<section>
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">What we do</span>
      <h2>Capabilities structured around outcomes</h2>
      <p class="lead">Faster development, reduced certification risk and products that stay maintainable after launch.</p>
    </div>
    {service_grid(detailed=False)}
  </div>
</section>

<section class="alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Cost structure</span>
      <h2>Senior engineering at a lower cost – by design</h2>
      <p class="lead">Lower cost does not come from junior staff or cutting corners. It comes from how the work is organised.</p>
    </div>
    <div class="grid grid-3">
      {card("team", "Compact team, no layers", "You work directly with the engineers who build your product. No account managers, no hand-offs, no overhead billed back to you.")}
      {card("ai", "AI-assisted engineering workflow", "We apply AI tooling across design, implementation, testing and documentation. Engineering hours go into decisions and verification, not boilerplate.")}
      {card("check", "Milestone-based delivery", "Fixed decision gates aligned with your budget. You review working results before each phase is released.")}
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Products we build and run</span>
      <h2>Proof, not slides</h2>
      <p class="lead">We ship and operate our own products with the same team and the same process we offer to clients.</p>
    </div>
    {listenfly_product()}
  </div>
</section>

<section class="alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Project areas</span>
      <h2>Where we deliver measurable value</h2>
    </div>
    {project_grid(detailed=False)}
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">How we work</span>
      <h2>A delivery process that de-risks execution</h2>
      <p class="lead">Clear milestones and decision gates keep every stakeholder aligned from concept to deployment.</p>
    </div>
    {process_grid()}
  </div>
</section>

{cta_band("Need a reliable partner for your next product?", "Share your roadmap and we will propose a practical implementation plan with team structure, timeline and the key technical decisions – directly usable planning input, not a generic pitch deck.", bullets=FIRST_WEEK)}
"""
    return shell(
        title="AyesTech – AI-integrated embedded, web and mobile product engineering",
        description="AyesTech designs and builds AI-integrated hardware, firmware, cloud and mobile products for automotive, medical and industrial companies. Senior team, milestone-based delivery, lower cost by design.",
        path="/", body=body)


def page_services() -> str:
    body = f"""
<section class="page-head">
  <div class="container">
    <span class="eyebrow">Services</span>
    <h1>From silicon to screen, with applied AI where it pays off</h1>
    <p class="lead">One integrated team covers hardware, embedded software, connectivity, cloud, mobile and AI integration. You get a single point of responsibility instead of three vendors and an integration problem.</p>
  </div>
</section>
<section class="tight">
  <div class="container">
    {service_grid(detailed=True)}
  </div>
</section>
<section class="alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Engagement models</span>
      <h2>Three ways to work with us</h2>
    </div>
    <div class="grid grid-3">
      {card("check", "Technical assessment", "Send us your scope, specification or existing codebase. Within 48 hours you receive an architecture and risk snapshot with effort ranges – free of charge for a first conversation.")}
      {card("board", "Fixed-scope project", "A defined deliverable, a milestone plan with decision gates and a budget you approve before each phase. Suitable for prototypes, feature modules and product launches.")}
      {card("team", "Dedicated engineering pod", "Monthly capacity with a named technical lead that works in your backlog, your tooling and your review process. Scale up or down at milestone gates.")}
    </div>
  </div>
</section>
{cta_band("Tell us what you are building.", "We answer every technical enquiry personally and propose the smallest engagement that answers your question.", bullets=FIRST_WEEK)}
"""
    return shell(
        title="Services – AyesTech",
        description="Applied AI integration, embedded and connectivity, cloud/web/mobile, hardware design, testing and compliance, dedicated engineering pods. Three engagement models.",
        path="/services/", body=body)


def page_projects() -> str:
    body = f"""
<section class="page-head">
  <div class="container">
    <span class="eyebrow">Projects</span>
    <h1>Representative project areas</h1>
    <p class="lead">Domains where we deliver measurable business and operational value – and a product of our own that shows the approach end to end.</p>
  </div>
</section>
<section class="tight">
  <div class="container">
    {project_grid(detailed=True)}
  </div>
</section>
<section class="alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Case study</span>
      <h2>ListenFly: on-device AI at consumer scale</h2>
      <p class="lead">An iPhone app that turns documents into natural speech with neural voices running entirely on the phone – designed, built and operated by AyesTech.</p>
    </div>
    {listenfly_product()}
    <div class="grid grid-3" style="margin-top:18px">
      {card("ai", "The AI challenge", "Run neural text-to-speech for 35 languages and hundreds of voices on a phone, offline, with low latency and battery use acceptable for hours of listening.")}
      {card("chip", "The engineering", "Model packaging and on-device inference, background audio that survives screen-off, camera scanning with text recognition, and a cloud path for premium voices – all behind one calm interface.")}
      {card("check", "The outcome", "Shipped on the App Store with a privacy-by-design architecture: no account, no server-side library, no reading tracking. Operated and updated continuously by the same team.")}
    </div>
  </div>
</section>
{cta_band("Have a product in one of these areas?", "We will tell you honestly whether AI belongs in it, what it will cost, and how to get to a first working version quickly.")}
"""
    return shell(
        title="Projects – AyesTech",
        description="Automotive electronics, medical devices and industrial IoT project areas, plus the ListenFly case study: on-device AI narration on iPhone.",
        path="/projects/", body=body)


def page_about() -> str:
    body = f"""
<section class="page-head">
  <div class="container">
    <span class="eyebrow">About</span>
    <h1>A technology-driven engineering company</h1>
    <p class="lead">AyesTech delivers integrated product development for automotive, medical and industrial teams from the Netherlands, serving clients across Europe, the United States and Canada.</p>
  </div>
</section>
<section class="tight">
  <div class="container">
    <div class="split">
      <div>
        <h2>What we stand for</h2>
        <p class="muted">We are a compact, senior team. Every engagement is run by the engineers who do the work, with transparent communication and outcomes you can measure. Quality and compliance come first; cost discipline comes from organisation, not from compromise.</p>
        <ul class="checks">
          <li>End-to-end ownership from hardware to cloud</li>
          <li>Automotive and medical domain expertise</li>
          <li>Applied AI where it creates value – not as a slogan</li>
          <li>Dedicated contact person for direct day-to-day support</li>
        </ul>
      </div>
      <div class="grid grid-2">
        <div class="stat"><b>7+ yrs</b><span>Average engineering experience</span></div>
        <div class="stat"><b>3 domains</b><span>Automotive, medical, industrial</span></div>
        <div class="stat"><b>Full stack</b><span>Hardware to cloud platforms</span></div>
        <div class="stat"><b>Global</b><span>Europe / US / Canada delivery</span></div>
      </div>
    </div>
  </div>
</section>
<section class="alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Principles</span>
      <h2>How we run engagements</h2>
    </div>
    <div class="grid grid-3">
      {card("check", "Transparent by default", "A backlog you can see, demos at every milestone, and effort ranges before work starts. No surprises at invoice time.")}
      {card("team", "Your team, extended", "We blend with your internal teams, tooling and reporting cadence rather than imposing our own.")}
      {card("ai", "Pragmatic about AI", "We use AI in our own workflow every day and put it into products only where it measurably helps – with privacy and reliability designed in.")}
    </div>
  </div>
</section>
<section>
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Leadership</span>
      <h2>Founder-led</h2>
      <p class="lead">AyesTech is founded and led by Süleyman Eskil, who remains hands-on in architecture and delivery on every engagement. Reach the team directly at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </div>
  </div>
</section>
{cta_band("Let's talk about your roadmap.", "A short call is usually enough to tell whether we are the right partner – and to give you planning input you can use either way.")}
"""
    return shell(
        title="About – AyesTech",
        description="AyesTech is a technology-driven engineering company in the Netherlands delivering AI-integrated product development for automotive, medical and industrial teams across Europe, the US and Canada.",
        path="/about/", body=body)


def page_contact() -> str:
    body = f"""
<section class="page-head">
  <div class="container">
    <span class="eyebrow">Contact</span>
    <h1>Start a project</h1>
    <p class="lead">Send us your scope, a specification or just a description of the problem. You receive a written technical assessment within 48 hours.</p>
  </div>
</section>
<section class="tight">
  <div class="container">
    <div class="split">
      <div class="card contact-card">
        <h3>Reach us directly</h3>
        <dl>
          <dt>Email</dt><dd><a href="mailto:{EMAIL}?subject=Project%20enquiry">{EMAIL}</a></dd>
          <dt>Phone</dt><dd><a href="{PHONE_HREF}">{PHONE}</a></dd>
          <dt>Location</dt><dd>Netherlands · serving Europe, US and Canada</dd>
          <dt>Response</dt><dd>Technical assessment within 48 hours</dd>
        </dl>
        <div class="btn-row" style="margin-top:22px">
          <a class="btn btn-primary" href="mailto:{EMAIL}?subject=Project%20enquiry">Email your scope</a>
          <a class="btn btn-secondary" href="mailto:{EMAIL}?subject=Discovery%20call">Book a discovery call</a>
        </div>
      </div>
      <div>
        <h2>What to include</h2>
        <p class="muted">The more of this we have, the more concrete the assessment:</p>
        <ul class="checks">
          <li>What the product does and who uses it</li>
          <li>Target hardware or platform, if already decided</li>
          <li>Regulatory context (automotive, medical, industrial)</li>
          <li>Existing material: specifications, schematics, code, prototypes</li>
          <li>Timeline, budget range and decision makers</li>
        </ul>
        <p class="muted">Everything you send is treated as confidential. We sign an NDA before reviewing proprietary material if you prefer.</p>
      </div>
    </div>
  </div>
</section>
<section class="alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">ListenFly users</span>
      <h2>Looking for app support?</h2>
      <p class="lead">Questions about the ListenFly app are answered on the <a href="/pdf-reader/support/">support page</a>; the <a href="/pdf-reader/privacy/">privacy policy</a> and <a href="/pdf-reader/terms/">terms of service</a> are published there as well.</p>
    </div>
  </div>
</section>
"""
    return shell(
        title="Contact – AyesTech",
        description="Start a project with AyesTech: send your scope and receive a written technical assessment within 48 hours. info@ayestech.com, Netherlands.",
        path="/contact/", body=body)


def page_listenfly() -> str:
    body = f"""
<section class="page-head">
  <div class="container">
    <span class="eyebrow">Product</span>
    <h1>ListenFly</h1>
    <p class="lead">An iPhone app by AyesTech that reads your documents aloud with natural AI voices running on the phone. The full product site, feature tour and plans are at <a href="{LISTENFLY_SITE}">listenfly.ayestech.com</a>.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="{LISTENFLY_SITE}">Open the ListenFly site</a>
      <a class="btn btn-secondary" href="{APP_STORE}">Download on the App Store</a>
    </div>
  </div>
</section>
<section class="tight">
  <div class="container">
    {listenfly_product()}
  </div>
</section>
<section class="alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">For users</span>
      <h2>Support and legal</h2>
    </div>
    <div class="grid grid-3">
      {card("check", "Support", "Answers to common questions and a direct line to the team.", href="/pdf-reader/support/", more="Open support")}
      {card("check", "Privacy Policy", "How ListenFly handles your data, explained plainly.", href="/pdf-reader/privacy/", more="Read the policy")}
      {card("check", "Terms of Service", "The rules that apply while you use ListenFly.", href="/pdf-reader/terms/", more="Read the terms")}
    </div>
  </div>
</section>
{cta_band("Want this kind of on-device AI in your own product?", "ListenFly is built with the same team and process we offer to clients. Tell us about your use case.")}
"""
    return shell(
        title="ListenFly – AyesTech",
        description="ListenFly by AyesTech: an iPhone app that reads PDFs, e-books, Word files, web articles and scanned pages aloud with on-device AI voices in 35 languages. Product site: listenfly.ayestech.com.",
        path="/pdf-reader/", body=body)


# ---- Legal pages (text kept verbatim from the published versions) --------

def legal_subnav(current: str) -> str:
    links = [("/pdf-reader/", "ListenFly"), ("/pdf-reader/privacy/", "Privacy Policy"), ("/pdf-reader/terms/", "Terms of Service"), ("/pdf-reader/support/", "Support")]
    return '<div class="subnav">' + "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>' for h, t in links) + "</div>"


def legal_page(*, path: str, eyebrow: str, title: str, tagline: str, meta: str | None, summary: str | None, sections: list[tuple[str, str]], description: str) -> str:
    toc = "".join(f'<li><a href="#s{i}">{t}</a></li>' for i, (t, _) in enumerate(sections, 1))
    body_sections = "".join(f'<h2 id="s{i}"><span class="n">{i}</span>{t}</h2>{c}' for i, (t, c) in enumerate(sections, 1))
    body = f"""
<section class="page-head">
  <div class="container">
    {legal_subnav(path)}
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
    <p class="lead">{tagline}</p>
    {f'<p class="meta">{meta}</p>' if meta else ''}
  </div>
</section>
<section class="tight">
  <div class="container prose">
    {f'<div class="summary">{summary}</div>' if summary else ''}
    <div class="toc"><ol>{toc}</ol></div>
    {body_sections}
    <p class="muted" style="margin-top:3em">ListenFly is a tool for listening to documents you own or are legally entitled to access. Questions: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  </div>
</section>
"""
    return shell(title=f"{title} – ListenFly – AyesTech", description=description, path=path, body=body)


def page_privacy() -> str:
    sections = [
        ("Who we are", f"<p>AyesTech — Süleyman Eskil<br>Contact: <a href=\"mailto:{EMAIL}\">{EMAIL}</a></p>"),
        ("Data that stays on your device", """<p>The following is stored only on your device and is never collected or seen by us:</p>
<ul>
<li>Documents you add (PDF, EPUB, DOCX, text files) and pages you scan with the camera</li>
<li>Text extracted from them, including text recognition (OCR) results</li>
<li>Your reading progress — the page and sentence you stopped at</li>
<li>Your settings (voice, language, speed, theme)</li>
<li>A local diagnostic log used for troubleshooting</li>
</ul>
<p>Deleting the app removes all of it from your device.</p>"""),
        ("Voices, cloud narration and text recognition", """<p>On the free tier, speech is synthesised entirely on your device and no text ever leaves it.</p>
<p><strong>Standard:</strong> narration uses AI voices that run entirely on your device — the text you listen to never leaves it. The voice files are downloaded once from our own storage (Cloudflare R2); these downloads send no document content.</p>
<p><strong>Premium:</strong> when you use HD cloud voices, only the passage about to be spoken is sent over an encrypted connection (HTTPS) to our server, and from there to Google Cloud Text-to-Speech. In this transfer:</p>
<ul>
<li>No name, e-mail, Apple Account or any user identifier is sent.</li>
<li>The text is not logged or stored on our server; it is discarded once the audio is produced.</li>
<li>Neither the text nor the audio is used for advertising, profiling or AI training.</li>
<li>The generated audio is cached briefly on your device only, so replaying does not resend anything.</li>
</ul>
<p><strong>Scanned pages (Standard and Premium):</strong> if you use the cloud text-recognition option for a page that has no text layer, the page image is sent over HTTPS through our server to Google Cloud Vision to extract its text. The same rules apply: no identifier is sent, the image is not stored on our server, and it is never used for advertising, profiling or AI training. The on-device recognition option sends nothing.</p>
<p>To operate the service and prevent abuse, our infrastructure may keep standard technical request records (IP address, timestamp, error details) for a short period. These records never contain your document content.</p>"""),
        ("Advertising (free tier only)", """<p>The free tier shows occasional full-screen ads served by Google AdMob, which may access your device advertising identifier (IDFA) and general device information for ad measurement and personalisation.</p>
<p>If you decline the iOS App Tracking Transparency prompt, your advertising identifier is not used. You can change this any time in Settings › Privacy &amp; Security › Tracking. Any paid subscription removes ads entirely.</p>
<p>AdMob privacy practices: <a href="https://policies.google.com/technologies/partner-sites">policies.google.com/technologies/partner-sites</a></p>"""),
        ("Purchases", "<p>Subscriptions and top-ups are processed by Apple through the App Store. We never see, receive or store your payment details — we only learn whether your subscription is currently valid.</p>"),
        ("Camera and photos", "<p>The camera opens only when you use the “Scan” feature, solely to turn a page into text. The captured image is processed on your device and stays there.</p>"),
        ("Children", "<p>The app is not directed at children under 13 and does not knowingly collect data from them.</p>"),
        ("Your rights", f"<p>Because there is no account and we hold no personal data about you, there is no user record to delete. For any GDPR or KVKK question, write to <a href=\"mailto:{EMAIL}\">{EMAIL}</a>.</p>"),
        ("Changes", "<p>If this policy changes, the effective date above is updated and significant changes are announced in the app.</p>"),
    ]
    return legal_page(
        path="/pdf-reader/privacy/", eyebrow="Privacy policy", title="Privacy Policy",
        tagline="How ListenFly handles your data, explained plainly.",
        meta="Effective: 21 August 2026 · Last updated: 21 August 2026",
        summary="<strong>In short:</strong> ListenFly has no accounts, never uploads your books to our servers, and does not track your reading. Your library, progress and settings stay on your device. Only with Premium HD cloud voices is the text being spoken at that moment sent to our server to generate audio; on Standard and Premium, a scanned page can be sent for cloud text recognition if you choose that option.",
        sections=sections,
        description="ListenFly privacy policy: no accounts, documents stay on your device, what is sent for cloud narration and text recognition, advertising on the free tier, purchases, your rights.")


def page_terms() -> str:
    sections = [
        ("Acceptance", "<p>By downloading and using ListenFly, you agree to these Terms of Service. If you do not agree, please do not use the app.</p>"),
        ("Purpose of the app", "<p>ListenFly is a tool for listening to documents you own or are legally entitled to access. The app hosts and distributes no copyrighted content — you are responsible for the rights to the documents you add.</p>"),
        ("Subscriptions and purchases", """<ul>
<li>Standard and Premium subscriptions and top-up packages are purchased through your App Store account.</li>
<li>Subscriptions renew automatically. Payment is charged to your Apple Account on confirmation of purchase.</li>
<li>Unless cancelled at least 24 hours before the end of the current period, the subscription renews at the same price.</li>
<li>Manage or cancel anytime in Settings › (your name) › Subscriptions.</li>
<li>One-time top-ups (30 min / 1h / 2h / 5h) are consumable, non-refundable and do not renew.</li>
<li>Refund requests are handled by Apple at <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>.</li>
<li>On-device voice listening is always unlimited and free on every tier.</li>
</ul>"""),
        ("Acceptable use", """<p>While using the app, you agree not to:</p>
<ul>
<li>Add copyrighted content you do not own or have no right to access</li>
<li>Attempt to reverse-engineer the app or abuse the service (e.g. automated or excessive requests)</li>
<li>Use the app for any unlawful purpose</li>
</ul>"""),
        ("Intellectual property", "<p>The app itself, its design and source code belong to AyesTech. Any documents and content you add to your library always remain yours — we claim no rights over them.</p>"),
        ("Disclaimer of warranty", "<p>The app is provided “as is”. No warranty, express or implied, is given that it will be uninterrupted or error-free; in particular, the accuracy of cloud-based text recognition (OCR) and narration depends on third-party services (Apple Vision, Google Cloud Text-to-Speech).</p>"),
        ("Limitation of liability", "<p>To the extent permitted by applicable law, AyesTech is not liable for any indirect, incidental or consequential damages arising from use of the app.</p>"),
        ("Suspension and termination", "<p>If we determine that you have violated these terms, we may suspend or terminate your access to server-side services (cloud narration). On-device (free) use is unaffected by such a restriction, since it runs entirely on your device.</p>"),
        ("Governing law", "<p>These terms are governed by the laws of the Republic of Türkiye. Apple’s standard Licensed Application End User License Agreement also applies to in-app purchases made through the App Store: <a href=\"https://www.apple.com/legal/internet-services/itunes/dev/stdeula/\">apple.com/legal/internet-services/itunes/dev/stdeula</a>.</p>"),
        ("Changes", "<p>If these terms change, the effective date above is updated and significant changes are announced in the app.</p>"),
        ("Contact", f"<p>Questions: <a href=\"mailto:{EMAIL}\">{EMAIL}</a></p>"),
    ]
    return legal_page(
        path="/pdf-reader/terms/", eyebrow="Terms of service", title="Terms of Service",
        tagline="The rules that apply while you use ListenFly — kept plain.",
        meta="Effective: 21 August 2026 · Last updated: 21 August 2026",
        summary=None, sections=sections,
        description="ListenFly terms of service: acceptance, purpose, subscriptions and purchases, acceptable use, intellectual property, warranty, liability, governing law.")


def page_support() -> str:
    sections = [
        ("Which file types can it read?", "<p>PDF, EPUB, DOCX and plain text files. You can also scan paper pages with the camera, paste a web link, or paste text from the clipboard.</p>"),
        ("Why is a scanned page or image-based PDF slow to open?", "<p>Those documents contain no embedded text, so each page goes through on-device text recognition (OCR). The first pass can take a few seconds; results are cached, so later openings are instant.</p>"),
        ("Playback stops when the screen turns off.", "<p>It should keep playing with the screen off. If it stops, check that the app is not restricted under Settings › ListenFly and that Low Power Mode is off.</p>"),
        ("What is the difference between the free and paid tiers?", "<p>The free tier uses your device’s built-in voice: unlimited, works offline, shows occasional ads. Standard unlocks natural AI voices that run on your device in 35 languages, with unlimited listening and no ads. Premium adds HD cloud voices in every language with a weekly/monthly allowance and no ads. If your allowance runs out, keep listening with the on-device voice for free, or buy a one-time top-up.</p>"),
        ("How do I cancel my subscription?", "<p>On your iPhone go to Settings › (your name) › Subscriptions and select ListenFly. Cancellation takes effect at the end of the current period. Subscriptions are managed by Apple; for refunds use <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>.</p>"),
        ("My subscription doesn’t show up on my new phone.", "<p>Use Settings › Subscription › Restore Purchases inside the app, and make sure you are signed in with the Apple Account you purchased with.</p>"),
        ("Are my books uploaded to the cloud?", "<p>No. Your documents stay on your device. Only while using Premium HD cloud voices is the passage being read sent for narration, with no identifier attached; Standard voices run on your device. See the <a href=\"/pdf-reader/privacy/\">Privacy Policy</a> for details.</p>"),
    ]
    return legal_page(
        path="/pdf-reader/support/", eyebrow="Support", title="Support",
        tagline="Find quick answers, or write to us directly.",
        meta=None,
        summary=f"<strong>Write to us:</strong> <a href=\"mailto:{EMAIL}\">{EMAIL}</a><br>We usually reply within 1–2 business days. When reporting a problem, telling us your iPhone model, iOS version and document type helps us fix it faster.",
        sections=sections,
        description="ListenFly support: file types, scanned PDFs, background playback, free vs paid tiers, cancelling or restoring a subscription, privacy of your documents.")


def page_404() -> str:
    body = """
<section class="page-head">
  <div class="container">
    <span class="eyebrow">404</span>
    <h1>This page does not exist</h1>
    <p class="lead">The address may have changed. Use the menu, or go back to the home page.</p>
    <div class="btn-row"><a class="btn btn-primary" href="/">Home</a><a class="btn btn-secondary" href="/contact/">Contact</a></div>
  </div>
</section>
"""
    return shell(title="Page not found – AyesTech", description="Page not found.", path="/404.html", body=body)


PAGES = {
    "index.html": page_home,
    "services/index.html": page_services,
    "projects/index.html": page_projects,
    "about/index.html": page_about,
    "contact/index.html": page_contact,
    "pdf-reader/index.html": page_listenfly,
    "pdf-reader/privacy/index.html": page_privacy,
    "pdf-reader/terms/index.html": page_terms,
    "pdf-reader/support/index.html": page_support,
    "404.html": page_404,
}


def write_sitemap() -> None:
    urls = ["/", "/services/", "/projects/", "/about/", "/contact/", "/pdf-reader/", "/pdf-reader/privacy/", "/pdf-reader/terms/", "/pdf-reader/support/"]
    today = _dt.date.today().isoformat()
    items = "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}</urlset>\n', encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")


def main() -> None:
    for rel, fn in PAGES.items():
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(fn(), encoding="utf-8")
        print("wrote", rel)
    write_sitemap()
    print("wrote sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
