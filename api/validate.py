#!/usr/bin/env python3
"""
Python версия API валидации для локального тестирования
Запуск: python3 api/validate.py
"""

import json
import os
import re
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import base64

# Загружаем переменные окружения
def load_env():
    env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'env.local')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

load_env()

# Правила валидации
RULES = {
    "insurance": {
        "displayName": "Ubezpieczenie medyczne",
        "requiredFields": [
            "insurer_name",
            "policy_number", 
            "insured_name",
            "id_number",
            "valid_from",
            "valid_to",
            "coverage_summary",
            "signatures_present"
        ],
        "patterns": {
            "policy_number": r"^[A-Za-z0-9\-/]{4,}$",
            "id_number": r"^[A-Za-z0-9]{5,}$",
            "valid_from": r"^\d{4}-\d{2}-\d{2}$",
            "valid_to": r"^\d{4}-\d{2}-\d{2}$"
        },
        "redFlagHints": [
            "Срок действия истёк или дата окончания раньше даты начала",
            "Отсутствует номер полиса",
            "Нет подписи страхователя/страховщика",
            "Нет ФИО застрахованного или не совпадает с анкетою",
            "Не указаны ключевые покрытия (например, неотложка/стационар)"
        ]
    }
}

def build_extraction_schema(doc_type):
    """Создает схему для извлечения данных"""
    if doc_type == "insurance":
        return {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "insurer_name": {"type": "string"},
                "policy_number": {"type": "string"},
                "insured_name": {"type": "string"},
                "id_number": {"type": "string"},
                "valid_from": {"type": "string"},
                "valid_to": {"type": "string"},
                "coverage_summary": {"type": "string"},
                "signatures_present": {"type": "boolean"},
                "stamp_present": {"type": "boolean"}
            },
            "required": []
        }
    return {"type": "object", "additionalProperties": True, "properties": {}}

def validate_extracted(extracted, cfg):
    """Валидирует извлеченные данные"""
    issues = []
    hints = []

    # Проверка обязательных полей
    for field in cfg.get("requiredFields", []):
        if field not in extracted or (isinstance(extracted[field], str) and not extracted[field].strip()):
            issues.append(f"Отсутствует обязательное поле: {field}")

    # Проверка паттернов
    for field, pattern in cfg.get("patterns", {}).items():
        value = str(extracted.get(field, ""))
        if value and not re.match(pattern, value):
            issues.append(f"Поле {field} не соответствует формату ({pattern})")

    # Дополнительная логика для страховки
    if cfg.get("displayName") == "Ubezpieczenie medyczne":
        try:
            valid_from = datetime.strptime(extracted.get("valid_from", ""), "%Y-%m-%d")
            valid_to = datetime.strptime(extracted.get("valid_to", ""), "%Y-%m-%d")
            
            if valid_to < valid_from:
                issues.append("Дата окончания полиса раньше даты начала")
            
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if valid_to < today:
                issues.append("Срок действия полиса истёк")
                
        except ValueError:
            pass

        coverage = extracted.get("coverage_summary", "")
        if not coverage or len(coverage) < 5:
            hints.append("Покрытия не распознаны: проверьте, что в полисе указаны ключевые разделы")

    hints.extend(cfg.get("redFlagHints", []))
    return issues, hints

def mock_openai_analysis(file_data, doc_type):
    """Имитирует анализ OpenAI (для тестирования)"""
    # В реальном приложении здесь будет вызов OpenAI API
    print(f"Анализируем {doc_type} документ...")
    
    # Имитируем извлеченные данные
    if doc_type == "insurance":
        return {
            "insurer_name": "PZU S.A.",
            "policy_number": "POL-2024-001",
            "insured_name": "Иван Иванов",
            "id_number": "ABC12345",
            "valid_from": "2024-01-01",
            "valid_to": "2024-12-31",
            "coverage_summary": "Медицинское страхование, включая неотложную помощь и стационарное лечение",
            "signatures_present": True,
            "stamp_present": True
        }
    
    return {}

class ValidationHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/validate':
            self.handle_validation()
        else:
            self.send_error(404, "Not Found")

    def handle_validation(self):
        try:
            # Читаем тело запроса
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            doc_type = data.get('docType')
            file_data = data.get('file')

            if not doc_type or not file_data:
                self.send_error(400, "docType and file are required")
                return

            if doc_type not in RULES:
                self.send_error(400, f"Unknown docType: {doc_type}")
                return

            cfg = RULES[doc_type]

            # Имитируем анализ OpenAI
            extracted = mock_openai_analysis(file_data, doc_type)

            # Валидируем данные
            issues, hints = validate_extracted(extracted, cfg)

            # Формируем ответ
            response = {
                "ok": len(issues) == 0,
                "issues": issues,
                "hints": hints,
                "extracted": extracted
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")
            self.send_error(500, f"Server error: {str(e)}")

    def do_OPTIONS(self):
        """Обработка CORS preflight запросов"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        """Логирование запросов"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

def run_server(port=8001):
    """Запускает сервер"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ValidationHandler)
    print(f"🚀 API сервер запущен на http://localhost:{port}")
    print(f"📝 Endpoint: POST http://localhost:{port}/api/validate")
    print(f"🔑 OpenAI API ключ: {'✅ Загружен' if os.getenv('OPENAI_API_KEY') else '❌ Не найден'}")
    print("Нажмите Ctrl+C для остановки")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
