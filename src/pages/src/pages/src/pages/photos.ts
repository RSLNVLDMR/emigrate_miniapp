const file = document.getElementById("file") as HTMLInputElement;
const result = document.getElementById("result")!;
document.getElementById("upload")?.addEventListener("click", () => {
  if (!file.files || !file.files[0]) {
    result.textContent = "Выберите файл.";
    return;
  }
  // Заглушка проверки
  setTimeout(() => (result.textContent = "✅ Фото выглядит корректно"), 400);
});
