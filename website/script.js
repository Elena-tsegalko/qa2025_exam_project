// Конфигурация тестов
const testConfig = {
    api: { enabled: false, options: { get: true, post: true, put: false, delete: false, performance: true } },
    ui: { enabled: false, options: { click: true, display: true, spelling: true, business: true } },
    load: { enabled: false, options: { concurrent: true, stress: false, performance: true } },
    settings: { timeout: 300, verbose: true, allure: true }
};

// AI ответы
const aiResponses = {
    'привет': 'Привет! Я AI-ассистент Елены. Могу рассказать о её навыках, тестах или помочь с выбором тестов.',
    'навыки': 'Елена владеет: Python, Selenium, pytest, Allure, API тестированием, Git. Также знает основы ООП и Page Object Model.',
    'тесты': 'В проекте 107 тестов: 28 API-тестов, 62 UI-теста, 8 нагрузочных тестов.',
    'api': 'API-тесты проверяют GET, POST, PUT, DELETE, PATCH запросы, статус-коды, заголовки и производительность.',
    'ui': 'UI-тесты проверяют кликабельность, отображение, орфографию и бизнес-сценарии на сайте.',
    'нагрузочные': 'Нагрузочные тесты проверяют параллельные запросы, стресс-тесты и стабильность сервера.',
    'команда': 'Для запуска тестов: pytest tests/api/ -v, pytest tests/ui/ -v, pytest tests/load/ -v',
    'помощь': 'Я могу помочь с выбором тестов, объяснить что проверяют тесты, или рассказать о навыках Елены.',
    'кто ты': 'Я AI-ассистент, созданный для помощи в работе с тестами. Задавайте вопросы!'
};

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initTestGroups();
    initSkillBars();
    initCounters();
    initTestCheckboxes();
    checkServerConnection();
});

// Проверка подключения к серверу
async function checkServerConnection() {
    try {
        const response = await fetch('/api/test-status', { signal: AbortSignal.timeout(2000) });
        if (response.ok) {
            addTerminalLine('✧ Сервер подключен', 'success');
        }
    } catch (e) {
        addTerminalLine('', '');
        addTerminalLine('⚠ ВНИМАНИЕ: Вы открыли файл напрямую!', 'error');
        addTerminalLine('', '');
        addTerminalLine('Для работы тестов нужно:', 'warning');
        addTerminalLine('1. Запустите сервер: python website/server.py', 'info');
        addTerminalLine('2. Откройте сайт: http://localhost:8080', 'info');
        addTerminalLine('', '');
    }
}

// Навигация
function initNavigation() {
    const links = document.querySelectorAll('.nav-link');
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
            // Закрыть мобильное меню
            document.querySelector('.nav-links').classList.remove('active');
        });
    });
}

function toggleNav() {
    document.querySelector('.nav-links').classList.toggle('active');
}

// Группы тестов
function initTestGroups() {
    const headers = document.querySelectorAll('.test-group-header');
    headers.forEach(header => {
        header.addEventListener('click', () => {
            const options = header.nextElementSibling;
            options.classList.toggle('active');
        });
    });
}

// Полоски навыков
function initSkillBars() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progress = entry.target.dataset.progress;
                entry.target.style.width = progress + '%';
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('.skill-progress').forEach(bar => observer.observe(bar));
}

// Счётчики
function initCounters() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('.stat-number').forEach(counter => observer.observe(counter));
}

function animateCounter(element) {
    const target = parseInt(element.dataset.count);
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;

    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// Чекбоксы тестов
function initTestCheckboxes() {
    const mainCheckboxes = document.querySelectorAll('.test-checkbox');
    mainCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const group = checkbox.closest('.test-group');
            const options = group.querySelectorAll('.option-checkbox');
            options.forEach(opt => opt.checked = checkbox.checked);
            updateTestConfig();
        });
    });
}

// Обновление конфигурации тестов
function updateTestConfig() {
    testConfig.api.enabled = document.getElementById('api-tests').checked;
    testConfig.api.options.get = document.getElementById('api-get')?.checked || false;
    testConfig.api.options.post = document.getElementById('api-post')?.checked || false;
    testConfig.api.options.put = document.getElementById('api-put')?.checked || false;
    testConfig.api.options.delete = document.getElementById('api-delete')?.checked || false;
    testConfig.api.options.performance = document.getElementById('api-performance')?.checked || false;

    testConfig.ui.enabled = document.getElementById('ui-tests').checked;
    testConfig.ui.options.click = document.getElementById('ui-click')?.checked || false;
    testConfig.ui.options.display = document.getElementById('ui-display')?.checked || false;
    testConfig.ui.options.spelling = document.getElementById('ui-spelling')?.checked || false;
    testConfig.ui.options.business = document.getElementById('ui-business')?.checked || false;

    testConfig.load.enabled = document.getElementById('load-tests').checked;
    testConfig.load.options.concurrent = document.getElementById('load-concurrent')?.checked || false;
    testConfig.load.options.stress = document.getElementById('load-stress')?.checked || false;
    testConfig.load.options.performance = document.getElementById('load-performance')?.checked || false;

    testConfig.settings.timeout = parseInt(document.getElementById('test-timeout')?.value) || 300;
    testConfig.settings.verbose = document.getElementById('test-verbose')?.checked || false;
    testConfig.settings.allure = document.getElementById('test-allure')?.checked || false;
}

// Выбрать/снять все
function selectAllTests() {
    document.querySelectorAll('.test-checkbox, .option-checkbox').forEach(cb => cb.checked = true);
    updateTestConfig();
    addTerminalLine('✧ Все тесты выбраны', 'info');
}

function deselectAllTests() {
    document.querySelectorAll('.test-checkbox, .option-checkbox').forEach(cb => cb.checked = false);
    updateTestConfig();
    addTerminalLine('◇ Все тесты сняты', 'info');
}

// Запуск тестов
async function runTests() {
    updateTestConfig();
    
    const selectedTests = [];
    if (testConfig.api.enabled) selectedTests.push('API');
    if (testConfig.ui.enabled) selectedTests.push('UI');
    if (testConfig.load.enabled) selectedTests.push('Load');

    if (selectedTests.length === 0) {
        addTerminalLine('⚠ Выберите хотя бы один тип тестов', 'warning');
        return;
    }

    addTerminalLine('$ Запуск тестов: ' + selectedTests.join(', '), 'info');
    addTerminalLine('⏳ Подготовка к запуску...', '');

    // Имитация запуска тестов
    for (const testType of selectedTests) {
        await simulateTestRun(testType);
    }

    addTerminalLine('', '');
    addTerminalLine('═══════════════════════════════════════', 'info');
    addTerminalLine('✧ Все тесты завершены! ✧', 'success');
    addTerminalLine('═══════════════════════════════════════', 'info');
}

async function simulateTestRun(testType) {
    addTerminalLine('', '');
    addTerminalLine(`▶ Запуск ${testType}-тестов...`, 'info');

    try {
        // Отправляем запрос на запуск
        const params = new URLSearchParams({
            type: testType.toLowerCase(),
            verbose: testConfig.settings.verbose.toString(),
            allure: testConfig.settings.allure.toString()
        });

        const startResponse = await fetch(`/api/run-tests?${params}`);
        const startData = await startResponse.json();

        if (!startData.success) {
            addTerminalLine(`✗ ${startData.error}`, 'error');
            return;
        }

        addTerminalLine('⏳ Тесты выполняются, ожидайте...', 'info');

        // Опрашиваем статус каждую секунду
        let attempts = 0;
        const maxAttempts = 300;

        while (attempts < maxAttempts) {
            await delay(1000);
            attempts++;

            const statusResponse = await fetch('/api/test-status');
            const status = await statusResponse.json();

            if (!status.running) {
                // Тесты завершились
                if (status.output) {
                    const lines = status.output.split('\n');
                    for (const line of lines) {
                        if (line.includes('PASSED')) {
                            addTerminalLine(`✓ ${line.trim()}`, 'success');
                        } else if (line.includes('FAILED')) {
                            addTerminalLine(`✗ ${line.trim()}`, 'error');
                        } else if (line.includes('ERROR')) {
                            addTerminalLine(`! ${line.trim()}`, 'warning');
                        } else if (line.includes('===')) {
                            addTerminalLine(line.trim(), 'info');
                        }
                    }
                }

                if (status.errors) {
                    addTerminalLine(status.errors, 'error');
                }

                if (status.returncode === 0) {
                    addTerminalLine('✧ Тесты завершены успешно!', 'success');
                } else if (status.returncode !== null) {
                    addTerminalLine(`⚠ Тесты завершены с кодом: ${status.returncode}`, 'warning');
                }

                // Показываем кнопку Allure
                if (testConfig.settings.allure) {
                    showAllureButton();
                }
                return;
            }

            // Показываем что ждём
            if (attempts % 5 === 0) {
                addTerminalLine(`⏳ Ожидание... (${attempts}с)`, '');
            }
        }

        addTerminalLine('✗ Превышен таймаут ожидания', 'error');

    } catch (e) {
        addTerminalLine('⚠ Сервер недоступен, запуск симуляции...', 'warning');
        await simulateTestRunOffline(testType);
    }
}

async function simulateTestRunOffline(testType) {
    const tests = {
        'API': [
            'tests/api/test_api_methods.py::TestApiMethods::test_get_main_page',
            'tests/api/test_api_methods.py::TestApiMethods::test_get_about_page',
            'tests/api/test_api_methods.py::TestApiMethods::test_get_response_time',
            'tests/api/test_api_methods.py::TestApiMethods::test_get_headers',
            'tests/api/test_api_methods.py::TestApiMethods::test_post_contact_form',
            'tests/api/test_api_methods.py::TestApiMethods::test_put_user_data',
            'tests/api/test_api_methods.py::TestApiMethods::test_delete_from_cart',
            'tests/api/test_api_methods.py::TestApiPerformance::test_response_time_main'
        ],
        'UI': [
            'tests/ui/test_clickability.py::TestClickability::test_header_logo_clickable',
            'tests/ui/test_display.py::TestElementDisplay::test_header_logo_displayed',
            'tests/ui/test_spelling.py::TestSpelling::test_title_spelling',
            'tests/ui/test_business_scenarios.py::TestBusinessScenarios::test_search_product_scenario'
        ],
        'Load': [
            'tests/load/test_load.py::TestConcurrentRequests::test_concurrent_get_requests',
            'tests/load/test_load.py::TestLoadOnPages::test_load_main_page',
            'tests/load/test_load.py::TestResponseTime::test_response_time_main'
        ]
    };

    const testList = tests[testType] || [];
    let passed = 0;
    let failed = 0;

    for (const test of testList) {
        await delay(300 + Math.random() * 500);
        
        const success = Math.random() > 0.1;
        if (success) {
            addTerminalLine(`✓ ${test.split('::').pop()}`, 'success');
            passed++;
        } else {
            addTerminalLine(`✗ ${test.split('::').pop()} FAILED`, 'error');
            failed++;
        }
    }

    addTerminalLine('', '');
    addTerminalLine(`📊 Результат: ${passed} passed, ${failed} failed`, failed > 0 ? 'warning' : 'success');
    
    // Показываем кнопку Allure если отчёт сгенерирован
    if (testConfig.settings.allure) {
        showAllureButton();
    }
}

// Allure отчёт
function showAllureButton() {
    const btn = document.getElementById('btn-allure-report');
    if (btn) {
        btn.style.display = 'inline-block';
        addTerminalLine('◈ Allure-отчёт готов. Нажмите "Открыть Allure-отчёт"', 'info');
    }
}

async function openAllureReport() {
    addTerminalLine('$ Открытие Allure-отчёта...', 'info');

    try {
        const response = await fetch('/api/allure-report');
        const data = await response.json();

        if (data.success) {
            addTerminalLine('✧ Открываю настоящий Allure-отчёт...', 'success');
            window.open(data.report_url, '_blank');
        } else {
            addTerminalLine('⚠ ' + data.error, 'warning');
            addTerminalLine('◇ Запустите тесты сначала', 'info');
        }
    } catch (e) {
        addTerminalLine('⚠ Сервер недоступен', 'error');
        addTerminalLine('◇ Запустите: python website/server.py', 'info');
    }
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Терминал
function addTerminalLine(text, type = '') {
    const terminal = document.getElementById('terminal');
    const line = document.createElement('div');
    line.className = 'terminal-line';
    line.innerHTML = `
        <span class="terminal-prompt">$</span>
        <span class="terminal-text ${type}">${text}</span>
    `;
    terminal.appendChild(line);
    terminal.scrollTop = terminal.scrollHeight;
}

function clearTerminal() {
    const terminal = document.getElementById('terminal');
    terminal.innerHTML = `
        <div class="terminal-line">
            <span class="terminal-prompt">$</span>
            <span class="terminal-text">Терминал очищен</span>
        </div>
    `;
}

function handleTerminalInput(event) {
    if (event.key === 'Enter') {
        const input = document.getElementById('terminal-input');
        const command = input.value.trim();
        
        if (command) {
            addTerminalLine(`$ ${command}`, '');
            processCommand(command);
            input.value = '';
        }
    }
}

function processCommand(command) {
    const cmd = command.toLowerCase();
    
    if (cmd === 'help') {
        addTerminalLine('Доступные команды: help, run, list, clear', 'info');
    } else if (cmd === 'run') {
        runTests();
    } else if (cmd === 'list') {
        addTerminalLine('Типы тестов: API (28), UI (62), Load (8)', 'info');
    } else if (cmd === 'clear') {
        clearTerminal();
    } else {
        addTerminalLine(`Команда не найдена: ${command}`, 'error');
    }
}

// AI Бот
function toggleAiBot() {
    document.getElementById('ai-bot').classList.toggle('collapsed');
}

function sendAiMessage() {
    const input = document.getElementById('ai-input');
    const message = input.value.trim();
    
    if (message) {
        addAiMessage(message, 'user');
        input.value = '';
        
        // Генерация ответа
        setTimeout(() => {
            const response = generateAiResponse(message);
            addAiMessage(response, 'bot');
        }, 500);
    }
}

function handleAiInput(event) {
    if (event.key === 'Enter') {
        sendAiMessage();
    }
}

function addAiMessage(text, type) {
    const container = document.getElementById('ai-messages');
    const message = document.createElement('div');
    message.className = `ai-message ai-message-${type}`;
    message.innerHTML = `
        <span class="ai-message-icon">${type === 'bot' ? '◈' : '◇'}</span>
        <div class="ai-message-content">${text}</div>
    `;
    container.appendChild(message);
    container.scrollTop = container.scrollHeight;
}

function generateAiResponse(message) {
    const lowerMessage = message.toLowerCase();
    
    for (const [key, response] of Object.entries(aiResponses)) {
        if (lowerMessage.includes(key)) {
            return response;
        }
    }
    
    return 'Интересный вопрос! Я могу рассказать о навыках Елены, типах тестов или помочь с запуском. Попробуйте спросить "навыки", "тесты" или "помощь".';
}
