document.addEventListener("DOMContentLoaded", function () {
    let elements = document.querySelectorAll(".fade-in");
    
    function fadeInOnScroll() {
        elements.forEach((el) => {
            let rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight) {
                el.style.opacity = 1;
                el.style.transform = "translateY(0)";
            }
        });
    }

    fadeInOnScroll();
    window.addEventListener("scroll", fadeInOnScroll);
});
