/**
 * GIFT Titanium - Main JavaScript
 * Premium Luxury Brand Interactions
 */

(function() {
  'use strict';

  // ============================================
  // Mobile Navigation Toggle
  // ============================================
  const menuToggle = document.querySelector('.menu-toggle');
  const mobileNav = document.querySelector('.mobile-nav');

  if (menuToggle && mobileNav) {
    menuToggle.addEventListener('click', function() {
      menuToggle.classList.toggle('active');
      mobileNav.classList.toggle('active');
      document.body.style.overflow = mobileNav.classList.contains('active') ? 'hidden' : '';
    });

    // Close mobile nav when clicking on a link
    const mobileNavLinks = mobileNav.querySelectorAll('a');
    mobileNavLinks.forEach(link => {
      link.addEventListener('click', function() {
        menuToggle.classList.remove('active');
        mobileNav.classList.remove('active');
        document.body.style.overflow = '';
      });
    });
  }

  // ============================================
  // Header Scroll Effect (Glass + Blur)
  // ============================================
  const header = document.querySelector('.header');
  
  if (header) {
    let lastScroll = 0;
    
    window.addEventListener('scroll', function() {
      const currentScroll = window.pageYOffset;
      
      if (currentScroll > 80) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
      
      lastScroll = currentScroll;
    });
  }

  // ============================================
  // Scroll to Top Button
  // ============================================
  const scrollTopBtn = document.querySelector('.scroll-top');
  
  if (scrollTopBtn) {
    window.addEventListener('scroll', function() {
      if (window.pageYOffset > 400) {
        scrollTopBtn.classList.add('visible');
      } else {
        scrollTopBtn.classList.remove('visible');
      }
    });
    
    scrollTopBtn.addEventListener('click', function() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  // ============================================
  // Quote Modal
  // ============================================
  const quoteModal = document.getElementById('quote-modal');
  
  // Open modal function (global)
  window.openQuoteModal = function(productName) {
    if (!quoteModal) return;
    quoteModal.classList.add('active');
    document.body.style.overflow = 'hidden';

    const productField = document.getElementById('quote-product');
    if (productField && productName) {
      productField.value = productName;
    }

    const productSelect = quoteModal.querySelector('[name="product_interest"]');
    if (productSelect && productName) {
      const options = Array.from(productSelect.options);
      const match = options.find(opt => productName.toLowerCase().includes(opt.value.toLowerCase()));
      productSelect.value = match ? match.value : '';
    }

    const messageField = quoteModal.querySelector('[name="message"]');
    if (messageField && productName && !messageField.value.trim()) {
      messageField.placeholder = 'Interested in: ' + productName;
    }
  };
  
  // Close modal function (global)
  window.closeQuoteModal = function() {
    if (quoteModal) {
      quoteModal.classList.remove('active');
      document.body.style.overflow = '';
    }
  };
  
  // Close modal on background click
  if (quoteModal) {
    quoteModal.addEventListener('click', function(e) {
      if (e.target === this) {
        closeQuoteModal();
      }
    });
  }
  
  // Close modal on escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && quoteModal && quoteModal.classList.contains('active')) {
      closeQuoteModal();
    }
  });

  // ============================================
  // Smooth Scroll for Anchor Links
  // ============================================
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      
      if (href === '#' || href === '#quote' || href === '#products') return;
      
      const target = document.querySelector(href);
      
      if (target) {
        e.preventDefault();
        
        const headerHeight = document.querySelector('.header')?.offsetHeight || 0;
        const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight;
        
        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

  // ============================================
  // Intersection Observer for Scroll Animations
  // ============================================
  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -50px 0px',
    threshold: 0.1
  };

  const animateOnScroll = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animated');
        animateOnScroll.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Observe all elements with data-animate attribute
  document.querySelectorAll('[data-animate]').forEach(el => {
    animateOnScroll.observe(el);
  });

  // ============================================
  // Product Filter Buttons
  // ============================================
  const filterBtns = document.querySelectorAll('.filter-btn');
  const productItems = document.querySelectorAll('.product-item');

  if (filterBtns.length && productItems.length) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', function() {
        const filter = this.dataset.filter;
        
        // Update active button
        filterBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        
        // Filter products
        productItems.forEach(item => {
          if (filter === 'all' || item.dataset.category === filter) {
            item.style.display = 'block';
            setTimeout(() => {
              item.style.opacity = '1';
              item.style.transform = 'translateY(0)';
            }, 50);
          } else {
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
            setTimeout(() => {
              item.style.display = 'none';
            }, 300);
          }
        });
      });
    });
  }

  // ============================================
  // Contact Form Handling
  // ============================================
  const contactForm = document.querySelector('#contact-form');
  
  if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
      // If it's a FormSubmit form, use async submission
      if (this.action && this.action.includes('formsubmit.co')) {
        e.preventDefault();
        const formData = new FormData(this);
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        
        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;
        
        fetch(this.action, {
          method: 'POST',
          body: formData,
          headers: { 'Accept': 'application/json' }
        })
        .then(response => {
          if (response.ok) {
            showToast('Message sent successfully! We will get back to you within 24 hours.');
            this.reset();
          } else {
            showToast('Something went wrong. Please try again or email us directly.');
          }
        })
        .catch(() => {
          showToast('Network error. Please try again or email us directly.');
        })
        .finally(() => {
          submitBtn.textContent = originalText;
          submitBtn.disabled = false;
        });
        return;
      }
      
      e.preventDefault();
      
      // Get form data
      const formData = new FormData(this);
      const data = Object.fromEntries(formData);
      
      // Basic validation
      const required = ['name', 'email', 'company', 'message'];
      let isValid = true;
      
      required.forEach(field => {
        const input = this.querySelector(`[name="${field}"]`);
        if (input && !input.value.trim()) {
          input.classList.add('error');
          isValid = false;
        } else if (input) {
          input.classList.remove('error');
        }
      });
      
      // Email validation
      const emailInput = this.querySelector('[name="email"]');
      if (emailInput && emailInput.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailInput.value)) {
          emailInput.classList.add('error');
          isValid = false;
        }
      }
      
      if (isValid) {
        // Show success message
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        
        submitBtn.textContent = 'Message Sent! ✓';
        submitBtn.disabled = true;
        
        // Reset form
        this.reset();
        
        showToast('Thank you for your inquiry! We will respond within 24 hours.');
        
        // Reset button
        setTimeout(() => {
          submitBtn.textContent = originalText;
          submitBtn.disabled = false;
        }, 3000);
      }
    });
  }

  // Quote Form in Modal
  const quoteForm = document.querySelector('#quote-form');
  
  if (quoteForm) {
    quoteForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const submitBtn = this.querySelector('button[type="submit"]');
      const originalText = submitBtn.textContent;
      
      submitBtn.textContent = 'Sending...';
      submitBtn.disabled = true;
      
      // If FormSubmit form, use fetch
      if (this.action && this.action.includes('formsubmit.co')) {
        const formData = new FormData(this);
        fetch(this.action, {
          method: 'POST',
          body: formData,
          headers: { 'Accept': 'application/json' }
        })
        .then(response => {
          if (response.ok) {
            showToast('Quote request sent! We will respond within 24 hours.');
            this.reset();
            setTimeout(() => {
              closeQuoteModal();
            }, 1500);
          } else {
            showToast('Something went wrong. Please try again or email us directly.');
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
          }
        })
        .catch(() => {
          showToast('Network error. Please try again or email us directly.');
          submitBtn.textContent = originalText;
          submitBtn.disabled = false;
        });
      } else {
        // Original behavior for non-FormSubmit forms
        showToast('Quote request sent! We will respond within 24 hours.');
        this.reset();
        setTimeout(() => {
          submitBtn.textContent = originalText;
          submitBtn.disabled = false;
          closeQuoteModal();
        }, 2000);
      }
    });
  }

  // ============================================
  // FormSubmit.co Async Form Handling
  // ============================================
  document.querySelectorAll('form[action*="formsubmit.co"]').forEach(form => {
    // Skip if already handled by quote-form or contact-form specific handlers
    if (form.id === 'quote-form' || form.id === 'contact-form') return;
    
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      const formData = new FormData(form);
      const submitBtn = this.querySelector('button[type="submit"], input[type="submit"]');
      const originalText = submitBtn ? submitBtn.textContent : '';
      
      if (submitBtn) {
        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;
      }
      
      fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: { 'Accept': 'application/json' }
      })
      .then(response => {
        if (response.ok) {
          showToast('Message sent successfully! We will get back to you within 24 hours.');
          form.reset();
          const modal = form.closest('.quote-modal');
          if (modal) closeQuoteModal();
        } else {
          showToast('Something went wrong. Please try again or email us directly.');
        }
      })
      .catch(() => {
        showToast('Network error. Please try again or email us directly.');
      })
      .finally(() => {
        if (submitBtn) {
          submitBtn.textContent = originalText;
          submitBtn.disabled = false;
        }
      });
    });
  });

  // ============================================
  // Get Quote Buttons (product pages)
  // ============================================
  document.querySelectorAll('[data-get-quote]').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      openQuoteModal(this.dataset.product || '');
    });
  });

  // ============================================
  // Product Gallery Thumbnails
  // ============================================
  const mainImage = document.getElementById('mainImage');
  const thumbnails = document.querySelectorAll('.product-thumbnail');

  if (mainImage && thumbnails.length) {
    thumbnails.forEach(thumb => {
      thumb.addEventListener('click', function() {
        const fullSrc = this.dataset.fullImage;
        if (!fullSrc) return;
        mainImage.src = fullSrc;
        thumbnails.forEach(t => t.classList.remove('active'));
        this.classList.add('active');
      });
    });
  }

  // ============================================
  // Toast Notification Function
  // ============================================
  function showToast(message) {
    const existing = document.querySelector('.toast-notification');
    if (existing) existing.remove();
    
    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.classList.add('show'), 10);
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  }

  // ============================================
  // Parallax Effect for Hero Section
  // ============================================
  const heroSection = document.querySelector('.hero');
  
  if (heroSection && window.innerWidth > 768) {
    window.addEventListener('scroll', function() {
      const scrolled = window.pageYOffset;
      const heroVisual = heroSection.querySelector('.hero-visual');
      
      if (heroVisual && scrolled < window.innerHeight) {
        heroVisual.style.transform = `translateY(${scrolled * 0.2}px)`;
      }
    });
  }

  // ============================================
  // Add CSS for notification animation
  // ============================================
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideOut {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(100%);
        opacity: 0;
      }
    }
    
    .form-input.error,
    .form-textarea.error {
      border-color: #E74C3C !important;
    }
  `;
  document.head.appendChild(style);

  // ============================================
  // Product Image Hover Effect
  // ============================================
  const productCards = document.querySelectorAll('.product-card');
  
  productCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
    });
  });

  // ============================================
  // Lazy Load Images (if native not supported)
  // ============================================
  if (!('loading' in HTMLImageElement.prototype)) {
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          imageObserver.unobserve(img);
        }
      });
    });
    
    lazyImages.forEach(img => imageObserver.observe(img));
  }

  // ============================================
  // Counter Animation for Stats
  // ============================================
  const statNumbers = document.querySelectorAll('.stat-number');
  
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const text = el.textContent;
        const originalText = text;
        const hasPlus = text.includes('+');
        const hasPercent = text.includes('%');
        const hasRange = text.includes('-');
        
        // Handle special cases
        if (hasRange) {
          // For "15-25" format, just show as is
          counterObserver.unobserve(el);
          return;
        }
        
        const num = parseFloat(text.replace(/[^0-9.]/g, ''));
        
        if (!isNaN(num) && num < 1000) {
          animateCounter(el, 0, num, 1500, hasPlus, hasPercent);
        }
        
        counterObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  statNumbers.forEach(el => counterObserver.observe(el));

  function animateCounter(element, start, end, duration, hasPlus, hasPercent) {
    const startTime = performance.now();
    
    function update(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Easing function
      const easeOutQuart = 1 - Math.pow(1 - progress, 4);
      const current = Math.floor(start + (end - start) * easeOutQuart);
      
      let text = current.toString();
      if (hasPercent) text += '%';
      if (hasPlus && progress === 1) text += '+';
      
      element.textContent = text;
      
      if (progress < 1) {
        requestAnimationFrame(update);
      }
    }
    
    requestAnimationFrame(update);
  }

  // ============================================
  // Initialize on DOM Ready
  // ============================================
  document.addEventListener('DOMContentLoaded', function() {
    // Add loaded class to body for page transitions
    document.body.classList.add('loaded');
  });

})();
