document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll("a[href^='#']");
    links.forEach((link) => {
        link.addEventListener("click", function (event) {
            const targetId = this.getAttribute("href");
            if (targetId.startsWith("#")) {
                event.preventDefault();
                const target = document.querySelector(targetId);
                if (target) {
                    target.scrollIntoView({ behavior: "smooth", block: "start" });
                }
            }
        });
    });

    const revealItems = document.querySelectorAll(".section, .project-card, .profile-card, .timeline-content");
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                }
            });
        },
        { threshold: 0.15 }
    );

    revealItems.forEach((item) => observer.observe(item));
});
