(() => {
  const saved = localStorage.getItem("theme");
  const preferredDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  document.documentElement.dataset.theme = saved || (preferredDark ? "dark" : "light");

  window.addEventListener("DOMContentLoaded", () => {
    document.querySelector(".theme-button")?.addEventListener("click", () => {
      const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
      document.documentElement.dataset.theme = next;
      localStorage.setItem("theme", next);
    });
  });
})();
