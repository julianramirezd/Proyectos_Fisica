@echo off
::==============================================================================
:: RSIRaman - Instalador para Windows
::==============================================================================
:: Este script instala RSIRaman en Windows 10/11
:: Requiere: Python 3.7+ y pip
::==============================================================================

setlocal enabledelayedexpansion

set INSTALL_DIR=%USERPROFILE%\RSIRaman
set SCRIPT_DIR=%~dp0

echo ==============================================================================
echo   RSIRaman - Instalador para Windows
echo   Reimplementación de RSIScan.exe (Raman Systems)
echo ==============================================================================
echo.

echo [1/5] Verificando Python y pip...
where python >nul 2>&1
if errorlevel 1 (
    echo   ERROR: Python no está instalado o no está en el PATH.
    echo   Descárguelo e instálelo desde https://www.python.org/
    echo   Asegúrese de marcar "Add Python to PATH" durante la instalación.
    pause
    exit /b 1
)
python --version
where pip >nul 2>&1
if errorlevel 1 (
    echo   ERROR: pip no está disponible.
    pause
    exit /b 1
)
echo.

echo [2/5] Copiando archivos a %INSTALL_DIR%...
if exist "%INSTALL_DIR%" (
    echo   El directorio ya existe. Sobrescribiendo...
    rd /s /q "%INSTALL_DIR%"
)
mkdir "%INSTALL_DIR%"
xcopy "%SCRIPT_DIR%RSIRaman\*" "%INSTALL_DIR%\" /E /I /Y
echo   Archivos copiados.
echo.

echo [3/5] Instalando dependencias de Python...
pip install -r "%INSTALL_DIR%\requirements.txt"
if errorlevel 1 (
    echo   ADVERTENCIA: Algunas dependencias no se pudieron instalar.
    echo   Intente ejecutar manualmente: pip install -r "%INSTALL_DIR%\requirements.txt"
)
echo.

echo [4/5] Creando acceso directo en el escritorio...
echo [InternetShortcut] > "%USERPROFILE%\Desktop\RSIRaman.url"
echo URL=file:///%INSTALL_DIR%\main.py >> "%USERPROFILE%\Desktop\RSIRaman.url"
echo IconIndex=0 >> "%USERPROFILE%\Desktop\RSIRaman.url"
echo   Acceso directo creado en el escritorio.
echo.

echo [5/5] Creando script de inicio rápido...
echo @echo off > "%INSTALL_DIR%\RSIRaman.bat"
echo cd /d "%INSTALL_DIR%" >> "%INSTALL_DIR%\RSIRaman.bat"
echo python main.py %%* >> "%INSTALL_DIR%\RSIRaman.bat"
echo   Script creado: %INSTALL_DIR%\RSIRaman.bat
echo.

echo ==============================================================================
echo   ¡Instalación completada!
echo.
echo   Para ejecutar RSIRaman:
echo     1. Doble clic en el acceso directo del escritorio, o
echo     2. Ejecute: %INSTALL_DIR%\RSIRaman.bat
echo     3. O abra una terminal y ejecute: python "%INSTALL_DIR%\main.py"
echo ==============================================================================
pause
