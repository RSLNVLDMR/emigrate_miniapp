#!/bin/bash

echo "🚀 Деплой на Vercel..."

# Проверяем, что все изменения закоммичены
if [[ -n $(git status --porcelain) ]]; then
    echo "❌ Есть незакоммиченные изменения. Сначала закоммитьте их:"
    git status
    exit 1
fi

# Пушим на GitHub
echo "📤 Пушим на GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Код успешно запушен на GitHub"
    echo ""
    echo "🌐 Теперь нужно:"
    echo "1. Зайти на https://vercel.com"
    echo "2. Найти проект emigrate_miniapp"
    echo "3. Нажать 'Redeploy' или 'Deploy'"
    echo ""
    echo "🔑 Или добавить переменную окружения OPENAI_API_KEY:"
    echo "   Settings → Environment Variables → OPENAI_API_KEY"
    echo ""
    echo "📱 После деплоя валидация документов будет работать!"
else
    echo "❌ Ошибка при пуше на GitHub"
    exit 1
fi
