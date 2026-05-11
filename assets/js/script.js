/* Fit.Physio.Katrin — Main JS */

// ── NAV SCROLL ──
const nav = document.querySelector('.nav');
const hamburger = document.querySelector('.nav__hamburger');
const mobileNav = document.querySelector('.nav__mobile');

window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 40);
}, { passive: true });

if (hamburger) {
  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    mobileNav.classList.toggle('open');
    document.body.style.overflow = mobileNav.classList.contains('open') ? 'hidden' : '';
  });
}

document.querySelectorAll('.nav__mobile a').forEach(link => {
  link.addEventListener('click', () => {
    hamburger.classList.remove('open');
    mobileNav.classList.remove('open');
    document.body.style.overflow = '';
  });
});

// ── SCROLL ANIMATIONS ──
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in-view'); } });
}, { threshold: 0.12 });

document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));

// ── COUNTER ANIMATION ──
function animateCounter(el) {
  const target = parseInt(el.dataset.target, 10);
  const suffix = el.dataset.suffix || '';
  let start = 0;
  const duration = 1600;
  const step = (timestamp) => {
    if (!start) start = timestamp;
    const progress = Math.min((timestamp - start) / duration, 1);
    const ease = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.floor(ease * target) + suffix;
    if (progress < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      animateCounter(e.target);
      counterObserver.unobserve(e.target);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('[data-target]').forEach(el => counterObserver.observe(el));

// ── VIDEO MODAL ──
const videoWrap = document.querySelector('.video-wrap');
if (videoWrap) {
  videoWrap.addEventListener('click', () => {
    const modal = document.createElement('div');
    modal.style.cssText = `
      position:fixed;inset:0;z-index:1000;
      background:rgba(0,0,0,0.92);
      display:flex;align-items:center;justify-content:center;
      padding:24px;
    `;
    modal.innerHTML = `
      <div style="position:relative;width:100%;max-width:900px;">
        <button style="position:absolute;top:-44px;right:0;background:none;border:none;color:white;font-size:1.8rem;cursor:pointer;line-height:1;" aria-label="Schließen">✕</button>
        <div style="background:#111;border-radius:16px;aspect-ratio:16/9;display:flex;align-items:center;justify-content:center;color:rgba(255,255,255,0.4);font-size:1rem;overflow:hidden;">
          <!-- Video-URL hier einfügen: ersetze durch deinen iframe/video tag -->
          <p style="text-align:center;padding:40px;">🎬 Dein Video kommt hier her.<br><small>Füge in script.js deinen Video-iframe ein.</small></p>
        </div>
      </div>
    `;
    modal.querySelector('button').addEventListener('click', () => modal.remove());
    modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });
    document.body.appendChild(modal);
  });
}

// ── SMOOTH SCROLL FOR ANCHOR LINKS ──
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
