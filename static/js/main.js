(function () {
  'use strict';

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function initScrollReveal() {
    const items = document.querySelectorAll('.reveal');
    if (!items.length) return;

    if (reducedMotion || !('IntersectionObserver' in window)) {
      items.forEach((el) => el.classList.add('is-visible'));
      return;
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });

    items.forEach((el) => observer.observe(el));
  }

  function animateCounter(el) {
    const target = Number(el.dataset.count || 0);
    if (reducedMotion) {
      el.textContent = target.toLocaleString();
      return;
    }

    const duration = 1600;
    const start = performance.now();

    function step(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(target * eased).toLocaleString();
      if (progress < 1) requestAnimationFrame(step);
    }

    requestAnimationFrame(step);
  }

  function initCounters() {
    const counters = document.querySelectorAll('[data-count]');
    if (!counters.length) return;

    if (!('IntersectionObserver' in window)) {
      counters.forEach(animateCounter);
      return;
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    counters.forEach((el) => observer.observe(el));
  }

  function initFormLoading() {
    document.querySelectorAll('form.needs-loading').forEach((form) => {
      form.addEventListener('submit', () => {
        if (!form.checkValidity()) return;
        const button = form.querySelector('button[type="submit"]');
        if (!button) return;
        button.disabled = true;
        const spinner = button.querySelector('.spinner-border');
        if (spinner) spinner.classList.remove('d-none');
      });
    });
  }

  function initAutoDismiss() {
    document.querySelectorAll('.alert.auto-dismiss').forEach((alert) => {
      setTimeout(() => {
        if (window.bootstrap && window.bootstrap.Alert) {
          window.bootstrap.Alert.getOrCreateInstance(alert).close();
        } else {
          alert.remove();
        }
      }, 6000);
    });
  }

  function initActiveNav() {
    const path = window.location.pathname;
    document.querySelectorAll('.site-nav .nav-link').forEach((link) => {
      const href = link.getAttribute('href');
      if (!href) return;
      const isHome = href === '/' || href.match(/^\/(en|vi)\/$/);
      if (isHome ? path === href : path.startsWith(href)) {
        link.classList.add('active');
      }
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    initScrollReveal();
    initCounters();
    initFormLoading();
    initAutoDismiss();
    initActiveNav();
  });
})();
