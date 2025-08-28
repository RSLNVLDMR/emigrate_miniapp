#!/bin/bash

echo "🚀 Простой деплой на Vercel"
echo "================================"

# Проверяем статус
if [[ -n $(git status --porcelain) ]]; then
    echo "❌ Есть незакоммиченные изменения:"
    git status
    echo ""
    echo "💡 Сначала закоммитьте изменения:"
    echo "   git add . && git commit -m 'your message'"
    exit 1
fi

echo "✅ Все изменения закоммичены"
echo "📤 Пушим на GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Код успешно запушен на GitHub!"
    echo ""
    echo "🌐 ТЕПЕРЬ ЗАДЕПЛОЙТЕ ВРУЧНУЮ:"
    echo ""
    echo "1️⃣ Зайдите на https://vercel.com"
    echo "2️⃣ Найдите проект emigrate_miniapp"
    echo "3️⃣ Нажмите 'Redeploy' или 'Deploy'"
    echo ""
    echo "🔑 ОБЯЗАТЕЛЬНО ДОБАВЬТЕ ПЕРЕМЕННУЮ:"
    echo "   Settings → Environment Variables"
    echo "   OPENAI_API_KEY = ваш_ключ"
    echo ""
    echo "📱 После деплоя валидация документов заработает!"
else
    echo "❌ Ошибка при пуше"
    exit 1
fi
