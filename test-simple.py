#!/usr/bin/env python3
"""
Простой тестовый скрипт для проверки API валидации
Использует только встроенные модули Python
"""

import json
import urllib.request
import urllib.parse

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
        # Подготавливаем запрос
        url = 'http://localhost:8001/api/validate'
        data = json.dumps(test_data).encode('utf-8')
        
        # Создаем HTTP запрос
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Python-Test-Client'
            },
            method='POST'
        )
        
        # Отправляем запрос
        with urllib.request.urlopen(req, timeout=10) as response:
            print(f"📊 Статус ответа: {response.status}")
            print(f"📋 Заголовки: {dict(response.getheaders())}")
            print("-" * 50)
            
            # Читаем ответ
            result_data = response.read().decode('utf-8')
            result = json.loads(result_data)
            
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
                    
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(f"❌ HTTP ошибка: {e.code}")
            if hasattr(e, 'read'):
                print(f"📝 Текст ошибки: {e.read().decode('utf-8')}")
        else:
            print(f"❌ Ошибка подключения: {e.reason}")
            print("💡 Убедитесь, что API сервер запущен: python3 api/validate.py")
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP ошибка: {e.code}")
        print(f"📝 Текст ошибки: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def test_with_curl():
    """Показывает команду curl для тестирования"""
    print("\n" + "="*50)
    print("🔄 Альтернативный способ тестирования (curl)")
    print("="*50)
    
    curl_command = '''curl -X POST http://localhost:8001/api/validate \\
  -H "Content-Type: application/json" \\
  -d '{
    "docType": "insurance",
    "file": {
      "dataUrl": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
      "filename": "test.png",
      "mime": "image/png"
    }
  }' '''
    
    print("💡 Выполните в терминале:")
    print(curl_command)

if __name__ == "__main__":
    print("🚀 Тестирование API валидации документов")
    print("="*50)
    
    # Основной тест
    test_validation_api()
    
    # Альтернативный способ
    test_with_curl()
    
    print("\n" + "="*50)
    print("✅ Тестирование завершено!")
    print("="*50)
