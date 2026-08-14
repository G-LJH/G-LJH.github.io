(() => {
  const header = document.querySelector(".site-header");
  const reveals = document.querySelectorAll(".reveal");

  const onScroll = () => {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 8);
  };

  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
    );
    reveals.forEach((el, i) => {
      el.style.transitionDelay = `${Math.min(i * 0.04, 0.24)}s`;
      io.observe(el);
    });
  } else {
    reveals.forEach((el) => el.classList.add("is-visible"));
  }

  const menus = Array.from(document.querySelectorAll(".resume-menu"));

  const closeAllMenus = (except) => {
    menus.forEach((menu) => {
      if (menu === except) return;
      const toggle = menu.querySelector(".resume-toggle");
      const panel = menu.querySelector(".resume-panel");
      if (!toggle || !panel) return;
      panel.hidden = true;
      toggle.setAttribute("aria-expanded", "false");
    });
  };

  menus.forEach((menu) => {
    const toggle = menu.querySelector(".resume-toggle");
    const panel = menu.querySelector(".resume-panel");
    if (!toggle || !panel) return;

    toggle.addEventListener("click", (event) => {
      event.stopPropagation();
      const willOpen = panel.hidden;
      closeAllMenus(menu);
      panel.hidden = !willOpen;
      toggle.setAttribute("aria-expanded", willOpen ? "true" : "false");
    });

    panel.addEventListener("click", (event) => {
      event.stopPropagation();
    });
  });

  document.addEventListener("click", () => closeAllMenus());
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeAllMenus();
  });
})();
