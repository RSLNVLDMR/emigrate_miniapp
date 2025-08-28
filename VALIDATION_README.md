# API Валидации Документов

## Описание

Система валидации документов через OpenAI GPT-4o-mini для проверки страховых полисов.

## Файлы

- `package.json` - зависимости проекта
- `env.example` - шаблон для OpenAI API ключа
- `vercel.json` - конфигурация Vercel с API функциями
- `templates/validation/rules.json` - правила валидации
- `api/validate.js` - serverless функция валидации
- `index.html` - обновлен с UI для валидации

## Установка

1. Скопируйте `env.example` в `.env` и добавьте ваш OpenAI API ключ
2. Установите зависимости: `npm install`
3. Деплой на Vercel

## Тестирование

### Локальное тестирование

```bash
# Установка зависимостей
npm install

# Запуск локального сервера
python3 -m http.server 8000
```

### Тест API

```bash
curl -X POST http://localhost:8000/api/validate \
  -H "Content-Type: application/json" \
  -d '{
    "docType": "insurance",
    "file": { 
      "dataUrl": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==", 
      "filename": "test.png", 
      "mime": "image/png" 
    }
  }'
```

### Тест через UI

1. Откройте http://localhost:8000
2. Перейдите в раздел "Страховка"
3. Загрузите файл страхового полиса
4. Нажмите "Проверить с AI"

## Структура ответа

```json
{
  "ok": true|false,
  "issues": ["список проблем"],
  "hints": ["рекомендации"],
  "extracted": {
    "insurer_name": "название страховой",
    "policy_number": "номер полиса",
    "insured_name": "имя застрахованного",
    "id_number": "номер документа",
    "valid_from": "2024-01-01",
    "valid_to": "2024-12-31",
    "coverage_summary": "описание покрытия",
    "signatures_present": true,
    "stamp_present": true
  }
}
```

## Поддерживаемые форматы

- **PDF** - с текстовым слоем (извлекается текст)
- **Изображения** - JPG, PNG, WebP (анализ через GPT-4o-mini Vision)

## Правила валидации

- Обязательные поля: insurer_name, policy_number, insured_name, id_number, valid_from, valid_to, coverage_summary, signatures_present
- Проверка форматов: номер полиса, ID, даты
- Логика дат: дата окончания > даты начала, полис не истек
- Проверка покрытий: наличие ключевых разделов

## Расширение

Для добавления новых типов документов:

1. Добавьте правила в `templates/validation/rules.json`
2. Обновите `buildExtractionSchema()` в `api/validate.js`
3. Добавьте UI в `index.html`
