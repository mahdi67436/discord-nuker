@echo off
title 🔥 Nuker Script Launcher 🔥
color 0A
cd /d "%~dp0"
setlocal enabledelayedexpansion

:: ----------------------------
:: Spinner Loading Function
:: ----------------------------
set "spinner=|/-\"
set "count=0"

:: ----------------------------
:: Check Python Installation
:: ----------------------------
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python and add it to system PATH.
    pause
    exit /b
)

:: ----------------------------
:: Show Loading Animation
:: ----------------------------
echo.
echo Launching nuker.py...
for /l %%i in (1,1,20) do (
    set /a mod=%%i %% 4
    set "char=!spinner:~%mod%,1!"
    <nul set /p="Loading !char! `."
    timeout /t 1 >nul
)
echo.

:: ----------------------------
:: Run nuker.py
:: ----------------------------
:run_script
python "nuker.py"
set "status=%errorlevel%"

if %status% neq 0 (
    color 0C
    echo.
    echo [ERROR] nuker.py encountered an error! Error Code: %status%
    set /p retry="Do you want to retry? (Y/N) > "
    if /i "!retry!"=="Y" goto run_script
    echo Exiting...
    pause >nul
    exit /b
) else (
    color 0B
    echo.
    echo [SUCCESS] nuker.py ran successfully! ✅
)

:: ----------------------------
:: Finished
:: ----------------------------
echo.
echo Press any key to exit...
pause >nul
exit
