@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

:: Проверяем venv и создаем его если папки venv нет
if not exist "venv\" (
    python -m venv venv
    call venv\Scripts\activate.bat
    if exist "requirements.txt" pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

:: Проверяем существует ли config.txt
set "CONFIG=config.txt"

if not exist "%CONFIG%" (
    echo config.txt is no exists.

    set /p "nickname=Enter nickname: "

    echo !nickname!>"%CONFIG%"

    echo config.txt is created.
    echo Your nickname: !nickname!
)

:: Запуск
python main.py
pause