// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('header');
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('nav a');

    // Header scroll effect
    const updateHeader = () => {
        if (window.scrollY > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    };

    // Smooth scroll for anchor links with offset for fixed header
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const headerHeight = header.offsetHeight;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerHeight - 20;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Highlight active nav link based on scroll position
    const highlightNavLink = () => {
        let currentSection = '';

        sections.forEach(section => {
            const sectionTop = section.offsetTop - 150;
            const sectionHeight = section.offsetHeight;

            if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
                currentSection = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentSection}`) {
                link.classList.add('active');
            }
        });
    };

    // Animate elements on scroll
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.capability-card, .project-card, .contact-link, .section-header, .about-content');

        elements.forEach((element, index) => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight * 0.85;

            if (elementPosition < screenPosition) {
                // Stagger animation for cards
                setTimeout(() => {
                    element.classList.add('visible');
                }, index * 50);
            }
        });
    };

    // Set initial styles for animation
    const setupAnimations = () => {
        const elements = document.querySelectorAll('.capability-card, .project-card, .contact-link');

        elements.forEach(element => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        });
    };

    // Add visible class styles
    const addVisibleStyles = () => {
        const style = document.createElement('style');
        style.textContent = `
            .capability-card.visible,
            .project-card.visible,
            .contact-link.visible {
                opacity: 1 !important;
                transform: translateY(0) !important;
            }
        `;
        document.head.appendChild(style);
    };

    // Parallax effect for hero background
    const parallaxHero = () => {
        const hero = document.querySelector('.hero');
        if (hero && window.scrollY < window.innerHeight) {
            const scrolled = window.scrollY;
            hero.style.backgroundPositionY = `${scrolled * 0.3}px`;
        }
    };

    // Initialize
    addVisibleStyles();
    setupAnimations();
    updateHeader();
    highlightNavLink();
    animateOnScroll();

    // Scroll event listeners with throttling
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                updateHeader();
                highlightNavLink();
                animateOnScroll();
                parallaxHero();
                ticking = false;
            });
            ticking = true;
        }
    });

    // Trigger animations after a short delay to ensure page is rendered
    setTimeout(() => {
        animateOnScroll();
    }, 100);
});
