document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector("[data-nav-toggle]");
  const nav = document.querySelector("[data-nav]");
  if (toggle && nav) toggle.addEventListener("click", () => nav.classList.toggle("nav-open"));
  document.querySelectorAll("[data-dismiss]").forEach(btn => btn.addEventListener("click", () => btn.closest(".flash")?.remove()));
  document.querySelectorAll("input[type='number'][max]").forEach(input => input.addEventListener("change", () => {
    const max = Number(input.max || 999);
    if (Number(input.value) > max) input.value = max;
    if (Number(input.value) < 0) input.value = 0;
  }));
});
