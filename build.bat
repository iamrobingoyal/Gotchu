@echo off
setlocal

REM Build FileOrganizer.exe from this project folder.
cd /d "%~dp0"

REM Keep build tools isolated from the system Python installation.
if not exist .venv\Scripts\python.exe (
    python -m venv .venv
    if errorlevel 1 (
        echo Could not create the build virtual environment.
        exit /b 1
    )
)

.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo Could not install build requirements.
    exit /b 1
)

REM Remove only artifacts created by previous PyInstaller builds.
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean FileOrganizer.spec
if errorlevel 1 (
    echo.
    echo Build failed. Review the errors above.
    exit /b 1
)

echo.
echo Build complete: dist\FileOrganizer.exe
endlocal
