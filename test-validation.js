// Тестовый скрипт для проверки API валидации
// Запуск: node test-validation.js

const testValidation = async () => {
  const testData = {
    docType: "insurance",
    file: {
      dataUrl: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
      filename: "test.png",
      mime: "image/png"
    }
  };

  try {
    console.log('Тестируем API валидации...');
    console.log('URL:', 'http://localhost:8000/api/validate');
    console.log('Данные:', JSON.stringify(testData, null, 2));
    
    const response = await fetch('http://localhost:8000/api/validate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(testData)
    });

    console.log('Статус ответа:', response.status);
    console.log('Заголовки:', Object.fromEntries(response.headers.entries()));

    if (response.ok) {
      const result = await response.json();
      console.log('✅ Успешный ответ:');
      console.log(JSON.stringify(result, null, 2));
    } else {
      const errorText = await response.text();
      console.log('❌ Ошибка:');
      console.log(errorText);
    }
  } catch (error) {
    console.log('❌ Ошибка сети:', error.message);
  }
};

// Запускаем тест
testValidation();
