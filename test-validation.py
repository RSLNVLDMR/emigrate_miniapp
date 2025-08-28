#!/usr/bin/env python3
"""
Python тестовый скрипт для проверки API валидации
Запуск: python3 test-validation.py
"""

import requests
import json

def test_validation_api():
    """Тестирует API валидации"""
    
    # Тестовые данные
    test_data = {
        "docType": "insurance",
        "file": {
            "dataUrl": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
            "filename": "test.png",
            "mime": "image/png"
        }
    }
    
    print("🧪 Тестируем API валидации...")
    print(f"📡 URL: http://localhost:8001/api/validate")
    print(f"📋 Данные: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
    print("-" * 50)
    
    try:
        # Отправляем POST запрос
        response = requests.post(
            'http://localhost:8001/api/validate',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"📊 Статус ответа: {response.status_code}")
        print(f"📋 Заголовки: {dict(response.headers)}")
        print("-" * 50)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Успешный ответ:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # Анализируем результат
            if result.get('ok'):
                print("\n🎉 Документ прошел валидацию!")
            else:
                print(f"\n⚠️ Найдено проблем: {len(result.get('issues', []))}")
                print(f"💡 Рекомендаций: {len(result.get('hints', []))}")
            
            if result.get('extracted'):
                print("\n📄 Извлеченные данные:")
                extracted = result['extracted']
                for key, value in extracted.items():
                    print(f"  {key}: {value}")
                    
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(f"📝 Текст ошибки: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к серверу")
        print("💡 Убедитесь, что API сервер запущен: python3 api/validate.py")
    except requests.exceptions.Timeout:
        print("❌ Таймаут запроса")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def test_with_real_file():
    """Тестирует с реальным файлом (опционально)"""
    print("\n" + "="*50)
    print("📁 Тест с реальным файлом")
    print("="*50)
    
    # Здесь можно добавить тест с реальным файлом
    print("💡 Для теста с реальным файлом:")
    print("1. Запустите API сервер: python3 api/validate.py")
    print("2. Откройте приложение: http://localhost:8000")
    print("3. Перейдите в раздел 'Страховка'")
    print("4. Загрузите файл страхового полиса")
    print("5. Нажмите 'Проверить с AI'")

if __name__ == "__main__":
    print("🚀 Тестирование API валидации документов")
    print("="*50)
    
    # Основной тест
    test_validation_api()
    
    # Дополнительная информация
    test_with_real_file()
    
    print("\n" + "="*50)
    print("✅ Тестирование завершено!")
    print("="*50)
