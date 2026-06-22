"""
Простой веб-сервер для запуска тестов через веб-интерфейс.
Предоставляет API для запуска тестов и отображения результатов.
"""

import os
import sys
import json
import threading
import webbrowser
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import parse_qs, urlparse
import subprocess

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

PORT = 8080
WEBSITE_DIR = Path(__file__).parent
PROJECT_DIR = Path(__file__).parent.parent

# Глобальное состояние тестов
test_state = {
    'running': False,
    'output': '',
    'errors': '',
    'returncode': None
}


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    """Многопоточный HTTP-сервер"""
    daemon_threads = True


def run_tests_in_background(cmd, cwd):
    """Запуск тестов в отдельном потоке"""
    global test_state
    test_state['running'] = True
    test_state['output'] = ''
    test_state['errors'] = ''
    test_state['returncode'] = None

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=cwd
        )
        test_state['output'] = result.stdout
        test_state['errors'] = result.stderr
        test_state['returncode'] = result.returncode

        # Генерируем Allure-отчёт если есть результаты
        results_dir = PROJECT_DIR / 'results'
        if results_dir.exists() and list(results_dir.glob('*.json')):
            report_dir = PROJECT_DIR / 'allure-report'
            try:
                subprocess.run(
                    f'allure generate "{results_dir}" -o "{report_dir}" --clean',
                    shell=True,
                    capture_output=True,
                    timeout=60
                )
            except:
                pass

    except subprocess.TimeoutExpired:
        test_state['errors'] = 'Таймаут выполнения тестов (300 сек)'
        test_state['returncode'] = -1
    except Exception as e:
        test_state['errors'] = str(e)
        test_state['returncode'] = -1
    finally:
        test_state['running'] = False


class TestServerHandler(SimpleHTTPRequestHandler):
    """Обработчик запросов для веб-сервера тестов"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEBSITE_DIR), **kwargs)

    def do_GET(self):
        """Обработка GET-запросов"""
        parsed = urlparse(self.path)

        if parsed.path == '/api/run-tests':
            self.handle_run_tests(parsed.query)
        elif parsed.path == '/api/test-status':
            self.handle_test_status()
        elif parsed.path == '/api/allure-report':
            self.handle_allure_report()
        elif parsed.path.startswith('/results/'):
            self.serve_results(parsed.path)
        elif parsed.path.startswith('/allure-report/'):
            self.serve_allure_report(parsed.path)
        else:
            super().do_GET()

    def handle_run_tests(self, query_string):
        """Запуск тестов через API (асинхронно)"""
        global test_state

        # Если тесты уже запущены
        if test_state['running']:
            self.send_json({'success': False, 'error': 'Тесты уже выполняются'})
            return

        params = parse_qs(query_string)

        test_type = params.get('type', ['all'])[0]
        verbose = params.get('verbose', ['true'])[0] == 'true'
        allure = params.get('allure', ['true'])[0] == 'true'

        # Формируем команду для запуска тестов
        cmd_parts = [sys.executable, '-m', 'pytest']

        if test_type == 'api':
            cmd_parts.append('tests/api/')
        elif test_type == 'ui':
            cmd_parts.append('tests/ui/')
        elif test_type == 'load':
            cmd_parts.append('tests/load/')
        else:
            cmd_parts.append('tests/')

        if verbose:
            cmd_parts.append('-v')

        if allure:
            results_dir = PROJECT_DIR / 'results'
            results_dir.mkdir(exist_ok=True)
            # Очищаем предыдущие результаты
            for f in results_dir.glob('*'):
                f.unlink()
            cmd_parts.extend(['--alluredir=./results'])

        cmd = ' '.join(cmd_parts)

        # Запускаем в отдельном потоке
        thread = threading.Thread(
            target=run_tests_in_background,
            args=(cmd, str(PROJECT_DIR)),
            daemon=True
        )
        thread.start()

        # Сразу возвращаем ответ что тесты запущены
        response = {'success': True, 'message': 'Тесты запущены'}
        self.send_json(response)

    def handle_test_status(self):
        """Получение статуса и результатов тестов"""
        global test_state

        response = {
            'running': test_state['running'],
            'output': test_state['output'],
            'errors': test_state['errors'],
            'returncode': test_state['returncode']
        }
        self.send_json(response)

    def handle_allure_report(self):
        """Получение URL Allure-отчёта"""
        report_dir = PROJECT_DIR / 'allure-report'

        if report_dir.exists() and (report_dir / 'index.html').exists():
            response = {'success': True, 'report_url': '/allure-report/index.html'}
        else:
            response = {'success': False, 'error': 'Allure-отчёт не сгенерирован. Запустите тесты сначала.'}

        self.send_json(response)

    def serve_allure_report(self, path):
        """Обслуживание файлов Allure-отчёта"""
        report_dir = PROJECT_DIR / 'allure-report'
        file_path = report_dir / path.replace('/allure-report/', '')

        if file_path.exists() and file_path.is_file():
            self.send_response(200)
            content_types = {
                '.html': 'text/html; charset=utf-8',
                '.css': 'text/css; charset=utf-8',
                '.js': 'application/javascript; charset=utf-8',
                '.json': 'application/json',
                '.svg': 'image/svg+xml',
                '.png': 'image/png',
                '.ico': 'image/x-icon'
            }
            self.send_header('Content-type', content_types.get(file_path.suffix, 'application/octet-stream'))
            self.end_headers()
            self.wfile.write(file_path.read_bytes())
        else:
            self.send_error(404, 'File not found')

    def serve_results(self, path):
        """Обслуживание файлов из папки results"""
        results_dir = PROJECT_DIR / 'results'
        file_path = results_dir / path.replace('/results/', '')

        if file_path.exists() and file_path.is_file():
            self.send_response(200)
            content_types = {'.html': 'text/html; charset=utf-8', '.json': 'application/json'}
            self.send_header('Content-type', content_types.get(file_path.suffix, 'application/octet-stream'))
            self.end_headers()
            self.wfile.write(file_path.read_bytes())
        else:
            self.send_error(404, 'File not found')

    def send_json(self, data):
        """Отправка JSON-ответа с CORS-заголовками"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def log_message(self, format, *args):
        """Логирование запросов"""
        print(f"[{self.log_date_time_string()}] {args[0]}")


def run_server():
    """Запуск веб-сервера"""
    server = ThreadingHTTPServer(('localhost', PORT), TestServerHandler)
    print(f"✧ Сервер запущен: http://localhost:{PORT}")
    print(f"◇ Откройте эту ссылку в браузере")
    print(f"◇ Нажмите Ctrl+C для остановки")

    # Автооткрытие браузера
    threading.Timer(1.0, lambda: webbrowser.open(f'http://localhost:{PORT}')).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✧ Сервер остановлен")
        server.shutdown()


if __name__ == '__main__':
    run_server()
