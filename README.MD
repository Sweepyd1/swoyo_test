# ✨ Тестовое задание для Python стажёра

**Клиент для сервиса отправки SMS** с поддержкой OpenAPI-спецификации и логированием операций.

## 🚀 Быстрый старт

```bash
# 1. Клонировать репозиторий и установить uv
git clone https://github.com/Sweepyd1/swoyo_test
cd swoyo_test
pip install uv

# 2. Установить зависимости
uv sync
source .venv/bin/activate.fish

# 3. Создать файл config.toml на основе example_config.toml с вашими данными

# 4. Запустить mock-сервер (в отдельном терминале)
./prism-cli-linux mock sms-platform.yaml

# 5. Запустить клиент
uv run src/main.py \
  --sender 12345678901 \
  --receiver 09876543210 \
  --text "Hello World"

# 6. Запустить тесты
pytest tests/ -v