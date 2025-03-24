// Intersection Observer for section animations
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, {
    threshold: 0.1
});

// Observe all containers
document.querySelectorAll('.container').forEach(container => {
    observer.observe(container);
});

// Sticky navigation effect
window.addEventListener('scroll', () => {
    const nav = document.querySelector('.sticky-top');
    if (window.scrollY > 50) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }
});

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Parallax effect for hero section
window.addEventListener('scroll', () => {
    const heroBg = document.querySelector('.hero-bg');
    const scrolled = window.pageYOffset;
    heroBg.style.transform = `translateY(${scrolled * 0.5}px)`;
}); 