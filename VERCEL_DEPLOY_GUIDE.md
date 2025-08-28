# 🚨 URGENT: Полный деплой на Vercel

## ⚠️ Проблема
В Vercel отсутствуют файлы валидации документов. Нужен полный передеплой.

## 📋 Что нужно сделать

### 1️⃣ Проверить все файлы в проекте
Убедитесь, что в проекте есть:
- ✅ `api/validate.js` - API функция валидации
- ✅ `templates/validation/rules.json` - правила валидации
- ✅ `vercel.json` - конфигурация Vercel
- ✅ `package.json` - зависимости
- ✅ `index.html` - основной файл с UI

### 2️⃣ Принудительный деплой
1. Зайдите на [https://vercel.com](https://vercel.com)
2. Найдите проект `emigrate_miniapp`
3. **ВАЖНО**: Нажмите **"Redeploy"** (не просто "Deploy")
4. Выберите **"Force Redeploy"** если есть такая опция

### 3️⃣ Проверить логи сборки
После деплоя проверьте:
- Логи сборки на Vercel
- Что все файлы загрузились
- Нет ли ошибок в `api/validate.js`

### 4️⃣ Добавить переменную окружения
**КРИТИЧЕСКИ ВАЖНО!**
```
Settings → Environment Variables
Name: OPENAI_API_KEY
Value: [ВАШ_OPENAI_API_КЛЮЧ]
Environment: Production, Preview, Development
```

## 🔍 Проверка после деплоя

### Тест 1: Проверить API
```bash
curl -X POST https://emigrate-miniapp-five.vercel.app/api/validate \
  -H "Content-Type: application/json" \
  -d '{"docType":"insurance","file":{"dataUrl":"test","filename":"test.png","mime":"image/png"}}'
```

### Тест 2: Проверить UI
1. Откройте [https://emigrate-miniapp-five.vercel.app/](https://emigrate-miniapp-five.vercel.app/)
2. Перейдите в "Страховка"
3. Попробуйте загрузить файл

## 🚨 Если деплой не работает

### Вариант 1: Удалить и создать заново
1. Удалите проект на Vercel
2. Создайте новый, подключив GitHub
3. Добавьте переменную окружения

### Вариант 2: Проверить конфигурацию
1. Убедитесь, что `vercel.json` правильный
2. Проверьте, что `api/validate.js` синтаксически корректен
3. Убедитесь, что все зависимости в `package.json`

## 📱 Результат
После успешного деплоя:
- Валидация страховых документов через OpenAI GPT-4o-mini
- API endpoint `/api/validate` работает
- UI интеграция в модуле страховки
- Автоматическая проверка PDF и изображений

---

**🚨 ВЫПОЛНИТЕ ЭТИ ШАГИ СЕЙЧАС!** 🚨
