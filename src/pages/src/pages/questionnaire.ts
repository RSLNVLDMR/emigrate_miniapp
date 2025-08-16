document.getElementById("continue")?.addEventListener("click", () => {
  // ВАЖНО: «Продолжить» ведёт ТОЛЬКО на чеклист
  location.href = "/";
});
document.getElementById("restart")?.addEventListener("click", () => {
  localStorage.removeItem("questionnaire_answers");
  localStorage.removeItem("questionnaire_progress");
  alert("Анкета сброшена. Начните заново.");
  // если есть отдельная страница для старта — редирект на неё
});

// ✎ Inline-edit (демо: просто алерт с ключом поля)
document.querySelectorAll("[data-edit]").forEach((b) => {
  b.addEventListener("click", () => {
    const key = (b as HTMLElement).getAttribute("data-edit");
    alert("Редактировать поле: " + key);
  });
});
