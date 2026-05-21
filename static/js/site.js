const observer = new IntersectionObserver(
    (entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("is-visible");
            }
        });
    },
    { threshold: 0.18 }
);

document.querySelectorAll(".pillar-card, .feature-card, .step-card, .pricing-card, .testimonial-card, .hero-card").forEach((item) => {
    item.classList.add("reveal-ready");
    observer.observe(item);
});
