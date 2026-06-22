"""
Telegram-бот для запуска автотестов проекта misshacosmetics.by.

Бот предоставляет следующие команды:
- /start - Приветствие и представление тестировщика
- /help - Список доступных команд
- /run_api_test - Запуск API-тестов
- /run_ui_test - Запуск UI-тестов
- /run_load_test - Запуск нагрузочных тестов
- /run_all_tests - Запуск всех тестов
- /status - Статус последнего запуска
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Загрузка переменных из .env файла
load_dotenv()


# Хранение статуса последнего запуска
last_run_status = {}


async def execute_command(cmd: str, update: Update, timeout: int = 300) -> str:
    """
    Выполнение системной команды с таймаутом.

    Args:
        cmd: Команда для выполнения
        update: Объект Update из Telegram
        timeout: Таймаут в секундах

    Returns:
        Результат выполнения команды
    """
    try:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout)
        output = f"STDOUT:\n{stdout.decode().strip()}" if stdout else ''
        output += f"\nSTDERR:\n{stderr.decode().strip()}" if stderr else ''
        return output.strip()
    except asyncio.TimeoutError:
        return f"Таймаут {timeout} сек"
    except Exception as e:
        return f'Ошибка {str(e)}'


def format_test_results(result: str, test_type: str) -> str:
    """
    Форматирование результатов тестов для отправки в Telegram.

    Args:
        result: Результат выполнения тестов
        test_type: Тип тестов (API/UI/Load)

    Returns:
        Отформатированное сообщение
    """
    # Извлекаем только ошибки и важную информацию
    lines = result.split('\n')
    important_lines = []

    for line in lines:
        if any(keyword in line for keyword in ["FAILED", "ERROR", "PASSED", "passed", "failed", "error"]):
            important_lines.append(line)

    if important_lines:
        return f"📋 Результаты {test_type} тестов:\n\n" + '\n'.join(important_lines[:50])
    else:
        return f"✅ Все {test_type} тесты прошли успешно!"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /start.
    Представляет тестировщика и описывает возможности бота.
    """
    welcome_message = """
🎯 Привет! Я Telegram-бот для запуска автотестов!

👨‍💻 Позволь представиться:
Я - Елена, начинающий тестировщик, который успешно закончил курсы тестирования ПО. 
Научилась создавать и поддерживать автоматизированные тесты для веб-приложений.

🤖 Мои возможности:
━━━━━━━━━━━━━━━━━━━━━━━━

📌 Доступные команды:
• /start - Приветствие и информация обо мне
• /help - Список всех команд
• /run_api_test - Запуск API-тестов
• /run_ui_test - Запуск UI-тестов
• /run_load_test - Запуск нагрузочных тестов
• /run_all_tests - Запуск всех тестов
• /status - Статус последнего запуска

🧪 Типы тестов:

1️⃣ API-тесты:
   • GET, POST, PUT, DELETE, PATCH запросы
   • Проверка статус-кодов
   • Проверка заголовков
   • Проверка времени ответа

2️⃣ UI-тесты:
   • Кликабельность элементов
   • Отображение элементов
   • Проверка орфографии
   • Бизнес-сценарии (10 шт.)

3️⃣ Нагрузочные тесты:
   • Параллельные запросы
   • Стресс-тесты
   • Проверка стабильности

💡 Для запуска используй команды выше!
    """
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /help.
    Выводит список доступных команд.
    """
    help_text = """
📋 Список доступных команд:

🔹 Основные команды:
/start - Приветствие и информация
/help - Этот список команд
/status - Статус последнего запуска

🔹 Запуск тестов:
/run_api_test - API-тесты (GET, POST, PUT, DELETE, PATCH)
/run_ui_test - UI-тесты (кликабельность, отображение, орфография, сценарии)
/run_load_test - Нагрузочные тесты
/run_all_tests - Все тесты сразу

💡 Совет: После запуска тестов результаты отправляются автоматически!
    """
    await update.message.reply_text(help_text)


async def run_api_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /run_api_test.
    Запускает API-тесты и отправляет результаты.
    """
    global last_run_status
    last_run_status["type"] = "API"
    last_run_status["status"] = "running"

    await update.message.reply_text('🚀 Запуск API-тестов...')

    results_dir = Path("./results")
    results_dir.mkdir(exist_ok=True)

    # Очистка предыдущих результатов
    for file in results_dir.glob("*"):
        file.unlink()

    # Запуск тестов
    result = await execute_command(
        'pytest -s -v tests/api/ --alluredir=./results',
        update
    )

    # Форматирование и отправка результатов
    formatted_result = format_test_results(result, "API")
    await update.message.reply_text(formatted_result[:3000])

    last_run_status["status"] = "completed"
    last_run_status["result"] = "success" if "FAILED" not in result else "failed"


async def run_ui_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /run_ui_test.
    Запускает UI-тесты и отправляет результаты.
    """
    global last_run_status
    last_run_status["type"] = "UI"
    last_run_status["status"] = "running"

    await update.message.reply_text('🚀 Запуск UI-тестов...')

    results_dir = Path("./results")
    results_dir.mkdir(exist_ok=True)

    # Очистка предыдущих результатов
    for file in results_dir.glob("*"):
        file.unlink()

    # Запуск тестов
    result = await execute_command(
        'pytest -s -v tests/ui/ --alluredir=./results',
        update
    )

    # Форматирование и отправка результатов
    formatted_result = format_test_results(result, "UI")
    await update.message.reply_text(formatted_result[:3000])

    last_run_status["status"] = "completed"
    last_run_status["result"] = "success" if "FAILED" not in result else "failed"


async def run_load_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /run_load_test.
    Запускает нагрузочные тесты и отправляет результаты.
    """
    global last_run_status
    last_run_status["type"] = "Load"
    last_run_status["status"] = "running"

    await update.message.reply_text('🚀 Запуск нагрузочных тестов...')

    results_dir = Path("./results")
    results_dir.mkdir(exist_ok=True)

    # Очистка предыдущих результатов
    for file in results_dir.glob("*"):
        file.unlink()

    # Запуск тестов
    result = await execute_command(
        'pytest -s -v tests/load/ --alluredir=./results',
        update
    )

    # Форматирование и отправка результатов
    formatted_result = format_test_results(result, "нагрузочных")
    await update.message.reply_text(formatted_result[:3000])

    last_run_status["status"] = "completed"
    last_run_status["result"] = "success" if "FAILED" not in result else "failed"


async def run_all_tests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /run_all_tests.
    Запускает все тесты и отправляет результаты.
    """
    global last_run_status
    last_run_status["type"] = "All"
    last_run_status["status"] = "running"

    await update.message.reply_text('🚀 Запуск всех тестов...')

    results_dir = Path("./results")
    results_dir.mkdir(exist_ok=True)

    # Очистка предыдущих результатов
    for file in results_dir.glob("*"):
        file.unlink()

    # Запуск всех тестов
    result = await execute_command(
        'pytest -s -v tests/ --alluredir=./results',
        update
    )

    # Форматирование и отправка результатов
    formatted_result = format_test_results(result, "всех")
    await update.message.reply_text(formatted_result[:3000])

    last_run_status["status"] = "completed"
    last_run_status["result"] = "success" if "FAILED" not in result else "failed"


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /status.
    Выводит статус последнего запуска тестов.
    """
    if not last_run_status:
        await update.message.reply_text("ℹ️ Тесты еще не запускались.")
        return

    status_emoji = "⏳" if last_run_status.get("status") == "running" else "✅"
    result_emoji = "✅" if last_run_status.get("result") == "success" else "❌"

    status_text = f"""
📊 Статус последнего запуска:

Тип тестов: {last_run_status.get('type', 'Неизвестно')}
Статус: {status_emoji} {last_run_status.get('status', 'Неизвестно')}
Результат: {result_emoji} {last_run_status.get('result', 'Неизвестно')}
    """
    await update.message.reply_text(status_text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик текстовых сообщений.
    Отвечает на сообщения, которые не являются командами.
    """
    await update.message.reply_text(
        "Используйте /help для просмотра списка доступных команд."
    )


def main() -> None:
    """
    Основная функция запуска бота.
    """
    # Получение токена из переменной окружения
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("Переменная окружения TELEGRAM_BOT_TOKEN не задана")

    # Создание приложения
    application = Application.builder().token(token).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("run_api_test", run_api_test))
    application.add_handler(CommandHandler("run_ui_test", run_ui_test))
    application.add_handler(CommandHandler("run_load_test", run_load_test))
    application.add_handler(CommandHandler("run_all_tests", run_all_tests))
    application.add_handler(CommandHandler("status", status_command))

    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    ))

    # Запуск бота
    print("🤖 Бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
