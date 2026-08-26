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

// --- Contact form (posts to Formspree) ---
// Paste the form id from the Formspree dashboard here. The endpoint it gives
// you looks like https://formspree.io/f/abcdwxyz, and the id is that last part.
// Until this is set, the form refuses to pretend it sent anything and points
// people at the phone instead.
const FORMSPREE_ID = 'xljrqgzd';

const contact = document.querySelector('.contact-form');
if (contact) {
  const status = contact.querySelector('.form-status');
  const button = contact.querySelector('button[type="submit"]');
  const connected = /^[a-zA-Z0-9]{6,}$/.test(FORMSPREE_ID);
  const callInstead = 'Please call 864-520-2020 and we’ll help you right away.';

  if (connected) {
    contact.setAttribute('action', 'https://formspree.io/f/' + FORMSPREE_ID);
    contact.setAttribute('method', 'POST');
  }

  // Reveal the "email your CV" note when someone picks Careers
  const reason = contact.querySelector('#cf-reason');
  const careersNote = contact.querySelector('#cfCareers');
  if (reason && careersNote) {
    const syncCareers = () => { careersNote.hidden = reason.value !== 'Careers'; };
    reason.addEventListener('change', syncCareers);

    // Deep links can preselect a reason, e.g. contact.html?reason=partnerships
    // (used by the Partners page "Talk to us" / "Make a referral" buttons).
    const reasonKey = new URLSearchParams(location.search).get('reason');
    if (reasonKey) {
      const map = {
        'new-patient': 'Becoming a new patient',
        'care': 'Question about my care',
        'insurance': 'Insurance & billing',
        'partnerships': 'Referrals & partnerships',
        'careers': 'Careers',
        'other': 'Something else'
      };
      const want = map[reasonKey.toLowerCase()];
      if (want) {
        const opt = [...reason.options].find(o => o.text === want);
        if (opt) reason.value = opt.value;
      }
    }
    syncCareers();
  }

  contact.addEventListener('submit', (e) => {
    e.preventDefault();

    // the form carries novalidate so we can word the message ourselves
    if (!contact.checkValidity()) {
      status.textContent = 'Please add your name and a valid email so we can reply.';
      const firstInvalid = contact.querySelector(':invalid');
      if (firstInvalid) firstInvalid.focus();
      return;
    }

    if (!connected) {
      status.textContent = 'This form isn’t connected yet. ' + callInstead;
      return;
    }

    const label = button.textContent;
    button.disabled = true;
    button.textContent = 'Sending…';
    status.textContent = '';

    fetch(contact.getAttribute('action'), {
      method: 'POST',
      body: new FormData(contact),
      headers: { Accept: 'application/json' }
    })
      .then((res) => {
        if (!res.ok) throw new Error('Formspree returned ' + res.status);
        contact.reset();
        status.textContent = 'Thank you, your message is on its way. We’ll be in touch soon.';
      })
      .catch(() => {
        status.textContent = 'That didn’t send. ' + callInstead;
      })
      .finally(() => {
        button.disabled = false;
        button.textContent = label;
      });
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

// --- Treatment method details (opens in place, no page change) ---
const txMethods = {
  'medication management': {
    ic: 'spark',
    lead: 'Medication can be a steady part of your care when it is chosen carefully and reviewed often. Your prescriber starts conservatively, explains the trade-offs, and adjusts alongside you.',
    points: [
      'A full review of what you have tried before, what helped, and what did not',
      'A clear explanation of why a medication is suggested, side effects included',
      'Follow-up within the first few weeks to see how it is actually going',
      'Dose changes, switches, or tapering off, whichever fits how you respond'
    ],
    note: '<strong>Worth knowing.</strong> Medication is optional. If you would rather start without it, or come off what you are taking, tell us and we will build the plan around that.'
  },
  'genetic testing': {
    ic: 'book',
    lead: 'A simple cheek swab shows how your body processes certain psychiatric medications. It takes some of the guesswork out, especially if past medications caused side effects or did little.',
    points: [
      'A cheek swab collected during your visit and sent to the lab',
      'Results in about two weeks, walked through with you line by line',
      'A shortlist of medications suited to your metabolism, and ones to approach carefully',
      'Findings kept in your chart to guide future prescribing decisions'
    ],
    note: '<strong>Worth knowing.</strong> Testing informs the decision, it does not make it. Your history and how you actually feel on a medication still carry the most weight.'
  },
  'long-acting injectables (lais)': {
    ic: 'hands',
    lead: 'An injection given every few weeks in place of a daily pill. This helps when remembering a daily dose is the hardest part of staying well.',
    points: [
      'A conversation about whether an injectable suits your diagnosis and routine',
      'Usually a short trial of the oral version first, to check how you tolerate it',
      'Injections given at the office, scheduled so you always know the next date',
      'Steadier medication levels between visits, and fewer daily decisions'
    ],
    note: '<strong>Worth knowing.</strong> These are most often used in bipolar disorder and schizophrenia care. Not every medication comes in an injectable form, so we will go over what is available for you.'
  },
  'diagnostic assessments': {
    ic: 'eye',
    lead: 'A structured evaluation to understand what is actually happening before anyone writes a plan. Symptoms overlap constantly, and the wrong label sends care in the wrong direction.',
    points: [
      'A long first conversation about your history, sleep, focus, mood, and daily life',
      'Standardized screening tools where they add real clarity',
      'A look at medical causes worth ruling out, such as thyroid or sleep problems',
      'Findings explained in plain language, with what they mean for treatment'
    ],
    note: '<strong>Worth knowing.</strong> A diagnosis can shift as we learn more about you. That is a normal part of good care, not a mistake.'
  },
  'substance use disorder care': {
    ic: 'hands',
    lead: 'Care for substance use alongside your mental health treatment, in one place and without judgment. Many people are managing both at once, and treating them separately rarely works.',
    points: [
      'An honest conversation about use, with no lecture attached',
      'Treatment for co-occurring depression, anxiety, or trauma at the same time',
      'Medication support where it is appropriate, plus referrals for higher levels of care',
      'Goals you set, whether that means cutting back or stopping altogether'
    ],
    note: '<strong>Worth knowing.</strong> A return to use is treated as information about the plan, not a reason to lose your place here.'
  },
  'personalized plans': {
    ic: 'spark',
    lead: 'Your plan is built around your life, your psyche, environment, and lifestyle, then revised as things change. Two people with the same diagnosis rarely need the same plan.',
    points: [
      'Goals written in your words rather than clinical shorthand',
      'Care that accounts for work, family, sleep, and what you can realistically sustain',
      'Regular check-ins to keep what is working and change what is not',
      'Coordination with therapists and other clinicians you already see'
    ],
    note: '<strong>Worth knowing.</strong> You can bring anything into the plan, including the approaches you would rather not try.'
  }
};

const txKey = (s) => (s || '').trim().toLowerCase().replace(/\s+/g, ' ');

if (document.querySelector('a[href$="treatments.html#methods"], .method-card')) {
  const modal = document.createElement('div');
  modal.className = 'tx-modal';
  modal.id = 'tx-modal';
  modal.setAttribute('role', 'dialog');
  modal.setAttribute('aria-modal', 'true');
  modal.setAttribute('aria-labelledby', 'tx-modal-title');
  modal.innerHTML =
    '<div class="tx-modal-inner">' +
      '<button class="tx-close" data-tx-close aria-label="Close">×</button>' +
      '<span class="value-ic" data-ic="spark"></span>' +
      '<p class="eyebrow">Treatment method</p>' +
      '<h2 class="tx-modal-title" id="tx-modal-title"></h2>' +
      '<p class="tx-modal-lead"></p>' +
      '<p class="tx-modal-h">What to expect</p>' +
      '<ul class="tx-list"></ul>' +
      '<p class="tx-note"></p>' +
      '<div class="tx-modal-cta">' +
        '<a class="btn btn-primary" href="patients.html#book">Book an initial appointment</a>' +
        '<a class="btn btn-outline" href="assessment.html">Take a free assessment</a>' +
      '</div>' +
    '</div>';
  document.body.appendChild(modal);

  const txIc = modal.querySelector('.value-ic');
  const txTitle = modal.querySelector('.tx-modal-title');
  const txLead = modal.querySelector('.tx-modal-lead');
  const txList = modal.querySelector('.tx-list');
  const txNote = modal.querySelector('.tx-note');
  let txLastFocus = null;

  const closeTx = () => {
    modal.classList.remove('open');
    document.body.style.overflow = '';
    if (txLastFocus) txLastFocus.focus();
  };

  const openTx = (name, trigger) => {
    const data = txMethods[txKey(name)];
    if (!data) return false;
    txLastFocus = trigger || null;
    txIc.setAttribute('data-ic', data.ic);
    txTitle.textContent = name;
    txLead.textContent = data.lead;
    txList.innerHTML = data.points.map(p => '<li>' + p + '</li>').join('');
    txNote.innerHTML = data.note;
    modal.classList.add('open');
    document.body.style.overflow = 'hidden';
    modal.querySelector('.tx-close').focus();
    return true;
  };

  // nav and footer links that used to jump to the treatments page
  document.querySelectorAll('a[href$="treatments.html#methods"]').forEach(link => {
    link.addEventListener('click', (e) => {
      if (openTx(link.textContent, link)) e.preventDefault();
    });
  });

  // the cards in the "How we treat" grid
  document.querySelectorAll('.method-card').forEach(card => {
    const heading = card.querySelector('h3');
    if (!heading || !txMethods[txKey(heading.textContent)]) return;
    card.setAttribute('role', 'button');
    card.setAttribute('tabindex', '0');
    const more = document.createElement('span');
    more.className = 'method-more';
    more.textContent = 'Read more →';
    card.appendChild(more);
    card.addEventListener('click', () => openTx(heading.textContent, card));
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openTx(heading.textContent, card); }
    });
  });

  modal.querySelectorAll('[data-tx-close]').forEach(b => b.addEventListener('click', closeTx));
  modal.addEventListener('click', (e) => { if (e.target === modal) closeTx(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && modal.classList.contains('open')) closeTx(); });
}

