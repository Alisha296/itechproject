// Intersection Observer for section animations
document.addEventListener('DOMContentLoaded', function() {
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
        if (nav && window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else if (nav) {
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
    const heroBg = document.querySelector('.hero-bg');
    if (heroBg) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            heroBg.style.transform = `translateY(${scrolled * 0.5}px)`;
        });
    }

    // Filter products functionality
    const categoryFilter = document.getElementById('categoryFilter');
    const priceFilter = document.getElementById('priceFilter');
    const sortFilter = document.getElementById('sortFilter');
    const searchInput = document.getElementById('searchInput');

    function applyFilters() {
        const url = new URL(window.location.href);
        
        // Apply category filter
        if (categoryFilter && categoryFilter.value) {
            url.searchParams.set('category', categoryFilter.value);
        } else {
            url.searchParams.delete('category');
        }
        
        // Apply price filter
        if (priceFilter && priceFilter.value) {
            url.searchParams.set('price', priceFilter.value);
        } else {
            url.searchParams.delete('price');
        }
        
        // Apply sort filter
        if (sortFilter && sortFilter.value) {
            url.searchParams.set('sort', sortFilter.value);
        } else {
            url.searchParams.delete('sort');
        }
        
        // Apply search filter
        if (searchInput && searchInput.value.trim()) {
            url.searchParams.set('search', searchInput.value.trim());
        } else {
            url.searchParams.delete('search');
        }
        
        window.location.href = url.toString();
    }

    // Add event listeners for filters
    if (categoryFilter) categoryFilter.addEventListener('change', applyFilters);
    if (priceFilter) priceFilter.addEventListener('change', applyFilters);
    if (sortFilter) sortFilter.addEventListener('change', applyFilters);
    if (searchInput) {
        const searchButton = searchInput.nextElementSibling;
        if (searchButton) {
            searchButton.addEventListener('click', applyFilters);
        }
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                applyFilters();
            }
        });
    }

    // Initialize filter values from URL
    const urlParams = new URLSearchParams(window.location.search);
    if (categoryFilter && urlParams.has('category')) {
        categoryFilter.value = urlParams.get('category');
    }
    if (priceFilter && urlParams.has('price')) {
        priceFilter.value = urlParams.get('price');
    }
    if (sortFilter && urlParams.has('sort')) {
        sortFilter.value = urlParams.get('sort');
    }
    if (searchInput && urlParams.has('search')) {
        searchInput.value = urlParams.get('search');
    }
}); 