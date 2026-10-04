@echo off
setlocal
cd /d "%~dp0"

call build.bat
if errorlevel 1 exit /b 1

set "ISCC_PATH="
for %%I in (ISCC.exe) do set "ISCC_PATH=%%~$PATH:I"
if not defined ISCC_PATH if exist "%ProgramFiles(x86)%\Inno Setup 7\ISCC.exe" set "ISCC_PATH=%ProgramFiles(x86)%\Inno Setup 7\ISCC.exe"
if not defined ISCC_PATH if exist "%ProgramFiles%\Inno Setup 7\ISCC.exe" set "ISCC_PATH=%ProgramFiles%\Inno Setup 7\ISCC.exe"
if not defined ISCC_PATH if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC_PATH=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not defined ISCC_PATH if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC_PATH=%ProgramFiles%\Inno Setup 6\ISCC.exe"

if not defined ISCC_PATH (
    echo Inno Setup 6 or 7 is required to build the installer.
    echo Install it from https://jrsoftware.org/isdl.php, then run this script again.
    exit /b 1
)

"%ISCC_PATH%" installer.iss
if errorlevel 1 exit /b 1
echo Installer complete: installer\FileOrganizer_Setup.exe
endlocal
