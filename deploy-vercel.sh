#!/bin/bash

echo "🚀 Деплой на Vercel через API..."

# Проверяем, что все изменения закоммичены
if [[ -n $(git status --porcelain) ]]; then
    echo "❌ Есть незакоммиченные изменения. Сначала закоммитьте их:"
    git status
    exit 1
fi

echo "📤 Пушим на GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Код успешно запушен на GitHub"
    echo ""
    echo "🌐 Теперь нужно задеплоить вручную:"
    echo ""
    echo "1️⃣ ЗАЙДИТЕ НА https://vercel.com"
    echo "2️⃣ НАЙДИТЕ ПРОЕКТ emigrate_miniapp"
    echo "3️⃣ НАЖМИТЕ 'Redeploy' или 'Deploy'"
    echo ""
    echo "🔑 ДОБАВЬТЕ ПЕРЕМЕННУЮ ОКРУЖЕНИЯ:"
    echo "   Settings → Environment Variables"
    echo "   Name: OPENAI_API_KEY"
    echo "   Value: [ВАШ_OPENAI_API_КЛЮЧ]"
    echo ""
    echo "📱 ПОСЛЕ ДЕПЛОЯ ВАЛИДАЦИЯ ДОКУМЕНТОВ БУДЕТ РАБОТАТЬ!"
    echo ""
    echo "🔍 Если деплой не сработал, проверьте:"
    echo "   - Правильность vercel.json"
    echo "   - Наличие всех файлов в api/ и templates/"
    echo "   - Переменные окружения"
else
    echo "❌ Ошибка при пуше на GitHub"
    exit 1
fi
