# Автокликер для Telegram

Этот проект представляет собой автокликер для Telegram, который может работать с несколькими 
устройствами через ADB. Скрипт автоматически взаимодействует с мини-приложением в боте,
выполняя необходимые действия в заданные временные интервалы.

## Требования 
- Python 3.x
- Модули Python: `tkinter`, `time`, `random`, `threading`, `adb_shell`

## Установка
1. Установка Python и необходимые модули: 
```sh 
pip install adb-shell 
```
2. Склонируйте репозиторий:
```sh
git clone https://github.com/
```
3. Подготовьте файлы ключей ADB:
   - Создайте файлы `adbkey` и `adbkey.pub` в корневом каталоге проекта.
   Эти файлы содержат приватный и публичный ключи для подключения к устройствам через ADB.

## Использование
1. Запустите скрипт : 
```sh
python zavod.py
```
2. В интерфейсе вы увидите список устройств с их параметрами.
3. Нажмите кнопку "Запустить", чтобы начать выполнение автокликера.
4. Для остановки автокликера нажмите кнопку "Остановить".

## Настройка
Вы можете настроить список устройств, добавив или изменив элементы в списке `self.devices` 
в классе `AutoClickerApp`.

### Пример:
```python
self.devices = [
    {"host": "192.168.1.184", "port": 5555},
    {"host": "192.168.1.102", "port": 5555},
    # Добавить остальные устройства здесь
]
```

## Генерация параметров
Параметры для каждого устройства генерируются случайным образом:
- delay_min: Минимальная задержка между действиями в секундах.
- delay_max: Максимальная задержка между действиями в секундах.
- start_delay_min: Минимальная задержка перед запуском мини-приложения в минутах.
- start_delay_max: Максимальная задержка перед запуском мини-приложения в минутах.
- work_start: Время начала работы автокликера (в формате HH:MM).
- work_end: Время окончания работы автокликера (в формате HH:MM)