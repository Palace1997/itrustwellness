/* iTrust Wellness — interactions */

// --- Mobile nav toggle ---
const header = document.querySelector('.site-header');
const toggle = document.querySelector('.nav-toggle');

toggle.addEventListener('click', () => {
  const open = header.classList.toggle('open');
  toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
});

// close the mobile menu after tapping a nav link
document.querySelectorAll('.main-nav a').forEach(link => {
  link.addEventListener('click', () => {
    header.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
  });
});

// --- Contact form (front-end stub) ---
const contact = document.querySelector('.contact-form');
if (contact) {
  contact.addEventListener('submit', (e) => {
    e.preventDefault();
    const status = contact.querySelector('.form-status');
    contact.reset();
    if (status) status.textContent = 'Thank you for reaching out — we’ll be in touch soon.';
  });
}

// --- Payment options modal ---
const payModal = document.getElementById('pay-modal');
if (payModal) {
  const openPay = () => { payModal.classList.add('open'); document.body.style.overflow = 'hidden'; };
  const closePay = () => { payModal.classList.remove('open'); document.body.style.overflow = ''; };
  document.querySelectorAll('[data-open-pay]').forEach(b => b.addEventListener('click', openPay));
  payModal.querySelectorAll('[data-close-pay]').forEach(b => b.addEventListener('click', closePay));
  payModal.addEventListener('click', (e) => { if (e.target === payModal) closePay(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && payModal.classList.contains('open')) closePay(); });
}

// --- Newsletter (front-end stub) ---
const news = document.querySelector('.newsletter');
if (news) {
  news.addEventListener('submit', () => {
    const input = news.querySelector('input');
    if (input.value) {
      input.value = '';
      input.placeholder = 'Thank you — you’re subscribed!';
    }
  });
}
