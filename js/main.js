/* ═══════════════════════════════════════
   MAIN JS — KonvertAI
   Nav, mobile menu, reveal, chat, smooth scroll
═══════════════════════════════════════ */

(function () {
  'use strict';

  // ── Nav: scroll effects (blur + hide on scroll down) ──
  var nav = document.getElementById('nav');
  var lastScroll = 0;
  var ticking = false;

  function onScroll() {
    if (ticking) return;
    ticking = true;

    requestAnimationFrame(function () {
      var scrollY = window.scrollY;

      // Add scrolled class for shadow
      if (scrollY > 50) {
        nav.classList.add('scrolled');
      } else {
        nav.classList.remove('scrolled');
      }

      // Hide nav on scroll down, show on scroll up
      if (scrollY > 400) {
        if (scrollY > lastScroll + 10) {
          nav.classList.add('hidden');
        } else if (scrollY < lastScroll - 5) {
          nav.classList.remove('hidden');
        }
      } else {
        nav.classList.remove('hidden');
      }

      lastScroll = scrollY;
      ticking = false;
    });
  }

  window.addEventListener('scroll', onScroll, { passive: true });

  // ── Mobile menu toggle ──
  var toggle = document.querySelector('.nav-toggle');
  var mobileMenu = document.querySelector('.nav-mobile');

  if (toggle && mobileMenu) {
    toggle.addEventListener('click', function () {
      var isOpen = mobileMenu.classList.toggle('open');
      toggle.classList.toggle('active');
      toggle.setAttribute('aria-expanded', isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    // Close on link click
    var mobileLinks = mobileMenu.querySelectorAll('a');
    for (var i = 0; i < mobileLinks.length; i++) {
      mobileLinks[i].addEventListener('click', function () {
        toggle.classList.remove('active');
        mobileMenu.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    }
  }

  // ── Reveal on scroll (IntersectionObserver) ──
  var revealElements = document.querySelectorAll('.r, .r-up, .r-scale');

  if ('IntersectionObserver' in window) {
    var revealObserver = new IntersectionObserver(function (entries) {
      for (var i = 0; i < entries.length; i++) {
        if (entries[i].isIntersecting) {
          entries[i].target.classList.add('v');
          revealObserver.unobserve(entries[i].target);
        }
      }
    }, {
      threshold: 0.08,
      rootMargin: '0px 0px -40px 0px'
    });

    for (var i = 0; i < revealElements.length; i++) {
      revealObserver.observe(revealElements[i]);
    }
  } else {
    // Fallback: show all immediately
    for (var i = 0; i < revealElements.length; i++) {
      revealElements[i].classList.add('v');
    }
  }

  // ── Chat mockup animation ──
  var messages = document.querySelectorAll('.msg');
  var typingIndicator = document.querySelector('.typing-ind');

  function animateChat() {
    var delay = 600;

    for (var i = 0; i < messages.length; i++) {
      (function (msg, d) {
        setTimeout(function () {
          if (msg.classList.contains('in') && typingIndicator) {
            typingIndicator.classList.add('show');
            setTimeout(function () {
              typingIndicator.classList.remove('show');
              msg.classList.add('show');
            }, 800);
          } else {
            msg.classList.add('show');
          }
        }, d);
      })(messages[i], delay);

      delay += messages[i].classList.contains('in') ? 1600 : 1000;
    }
  }

  // Start chat when hero is visible
  var heroSection = document.getElementById('hero');
  if (heroSection && messages.length > 0) {
    var heroObserver = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) {
        setTimeout(animateChat, 500);
        heroObserver.disconnect();
      }
    }, { threshold: 0.3 });

    heroObserver.observe(heroSection);
  }

  // ── Smooth scroll for anchor links ──
  var anchors = document.querySelectorAll('a[href^="#"]');
  for (var i = 0; i < anchors.length; i++) {
    anchors[i].addEventListener('click', function (e) {
      var href = this.getAttribute('href');
      if (href === '#') return;
      var target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  }

  // ── Active nav link highlight ──
  var sections = document.querySelectorAll('section[id]');
  var navLinks = document.querySelectorAll('.nav-links a');

  if (sections.length > 0 && navLinks.length > 0) {
    var sectionObserver = new IntersectionObserver(function (entries) {
      for (var i = 0; i < entries.length; i++) {
        if (entries[i].isIntersecting) {
          var id = entries[i].target.getAttribute('id');
          for (var j = 0; j < navLinks.length; j++) {
            navLinks[j].classList.remove('active');
            if (navLinks[j].getAttribute('href') === '#' + id) {
              navLinks[j].classList.add('active');
            }
          }
        }
      }
    }, {
      threshold: 0.3,
      rootMargin: '-72px 0px -50% 0px'
    });

    for (var i = 0; i < sections.length; i++) {
      sectionObserver.observe(sections[i]);
    }
  }

})();


// ── Lead form handling ──
(function () {
  'use strict';

  var form = document.getElementById('lead-form');
  var success = document.getElementById('form-success');

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var formData = new FormData(form);
      var submitBtn = form.querySelector('.form-submit');

      // Disable button during submission
      submitBtn.disabled = true;
      submitBtn.textContent = 'Enviando...';

      // Send to Formspree (or custom endpoint)
      fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: { 'Accept': 'application/json' }
      })
      .then(function (response) {
        if (response.ok) {
          form.hidden = true;
          success.hidden = false;
        } else {
          // Fallback: redirect to WhatsApp with data
          var nome = formData.get('nome') || '';
          var whatsapp = formData.get('whatsapp') || '';
          var empresa = formData.get('empresa') || '';
          var msg = 'Olá! Quero testar o agente de IA.\nNome: ' + nome + '\nWhatsApp: ' + whatsapp + '\nEmpresa: ' + empresa;
          window.open('https://wa.me/5583999999999?text=' + encodeURIComponent(msg), '_blank');
          form.hidden = true;
          success.hidden = false;
        }
      })
      .catch(function () {
        // Network error: redirect to WhatsApp
        var nome = formData.get('nome') || '';
        var whatsapp = formData.get('whatsapp') || '';
        var empresa = formData.get('empresa') || '';
        var msg = 'Olá! Quero testar o agente de IA.\nNome: ' + nome + '\nWhatsApp: ' + whatsapp + '\nEmpresa: ' + empresa;
        window.open('https://wa.me/5583999999999?text=' + encodeURIComponent(msg), '_blank');
        form.hidden = true;
        success.hidden = false;
      });
    });
  }

  // Phone mask for WhatsApp field
  var phoneInput = document.getElementById('form-whatsapp');
  if (phoneInput) {
    phoneInput.addEventListener('input', function (e) {
      var v = e.target.value.replace(/\D/g, '');
      if (v.length > 11) v = v.slice(0, 11);
      if (v.length > 6) {
        e.target.value = '(' + v.slice(0, 2) + ') ' + v.slice(2, 7) + '-' + v.slice(7);
      } else if (v.length > 2) {
        e.target.value = '(' + v.slice(0, 2) + ') ' + v.slice(2);
      } else if (v.length > 0) {
        e.target.value = '(' + v;
      }
    });
  }
})();
