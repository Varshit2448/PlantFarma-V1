document.addEventListener("DOMContentLoaded", () => {
  const dropzone = document.querySelector(".dropzone input");
  if (dropzone) {
    dropzone.addEventListener("change", () => {
      const name = dropzone.files?.[0]?.name;
      const label = dropzone.closest(".dropzone");
      if (name && label) {
        const strong = label.querySelector("strong");
        if (strong) strong.textContent = name;
      }
    });
  }
});
