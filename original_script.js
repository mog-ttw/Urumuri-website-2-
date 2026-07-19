const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');
const sectionLinks = document.querySelectorAll('.nav-links a');
const sections = document.querySelectorAll('main section[id]');

navToggle?.addEventListener('click', () => {
  const isExpanded = navToggle.getAttribute('aria-expanded') === 'true';
  navToggle.setAttribute('aria-expanded', String(!isExpanded));
  navLinks.classList.toggle('active');
});

const updateActiveLink = () => {
  const offset = window.scrollY + window.innerHeight / 2;
  sections.forEach(section => {
    const top = section.offsetTop;
    const bottom = top + section.offsetHeight;
    const id = section.getAttribute('id');
    const link = document.querySelector(`.nav-links a[href='#${id}']`);
    if (!link) return;
    if (offset >= top && offset < bottom) {
      sectionLinks.forEach(item => item.classList.remove('active'));
      link.classList.add('active');
    }
  });
};

window.addEventListener('scroll', updateActiveLink, { passive: true });
updateActiveLink();


const observerOptions = {
  threshold: 0.15,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry, index) => {
    if (entry.isIntersecting) {
      setTimeout(() => {
        entry.target.classList.add('animate-in');
      }, index * 80);
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);


document.querySelectorAll('.feature-card, .step-card, .restaurant-card, .stats-grid div').forEach(el => {
  observer.observe(el);
});


document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('click', function(e) {
    const ripple = document.createElement('span');
    ripple.style.position = 'absolute';
    ripple.style.borderRadius = '50%';
    ripple.style.background = 'rgba(255,255,255,0.6)';
    ripple.style.animation = 'rippleEffect 0.6s ease-out';
    ripple.style.pointerEvents = 'none';
    
    const rect = this.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;
    
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.style.transform = 'scale(0)';
    
    this.appendChild(ripple);
  });
});

// Smooth counter animations 
function animateCounter(element) {
  const text = element.innerText;
  const match = text.match(/^(\d+)(.*)$/);
  if (!match) return;
  const target = parseInt(match[1], 10);
  const suffix = match[2] || '';
  const duration = 1500;
  const increment = target / (duration / 30);
  let current = 0;
  
  const timer = setInterval(() => {
    current += increment;
    if (current >= target) {
      element.innerText = target + suffix;
      clearInterval(timer);
    } else {
      element.innerText = Math.floor(current) + suffix;
    }
  }, 30);
}

const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.querySelectorAll('strong').forEach(stat => {
        if (!stat.dataset.animated) {
          stat.dataset.animated = 'true';
          animateCounter(stat);
        }
      });
      statsObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.stats-grid').forEach(grid => {
  statsObserver.observe(grid);
});

const heroCard = document.querySelector('.hero-card');
if (heroCard) {
  heroCard.addEventListener('mousemove', (e) => {
    const rect = heroCard.getBoundingClientRect();
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const rotateX = (y - centerY) / 15;
    const rotateY = (centerX - x) / 15;
    heroCard.style.transform = `perspective(1200px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-12px) scale(1.02)`;
  });
  
  heroCard.addEventListener('mouseleave', () => {
    heroCard.style.transform = 'translateY(-12px) scale(1.02)';
  });
}

const bikeRiders = document.querySelectorAll('.bike-rider');
const updateBikeScroll = () => {
  const offset = window.scrollY;
  bikeRiders.forEach((bike, index) => {
    const factor = 0.035 + index * 0.012;
    bike.style.transform = `translateY(${offset * factor}px)`;
  });
};
updateBikeScroll();
window.addEventListener('scroll', updateBikeScroll, { passive: true });

const style = document.createElement('style');
style.textContent = `
  @keyframes rippleEffect {
    to {
      transform: scale(4);
      opacity: 0;
    }
  }
  .animate-in {
    animation: slideInUp 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards !important;
  }
`;
document.head.appendChild(style);

