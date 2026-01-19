@echo off
REM Build script for DHH Modpack Installer (Python/PyInstaller)
REM Creates a portable .exe file using PyInstaller

title DHH Installer Build Script (Python)

echo Building DHH Modpack Installer (Python/PyInstaller)
echo.

REM Check if Python is available
where python >nul 2>nul
if errorlevel 1 goto :python_not_found

REM Display Python version (informational only)
python --version

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>nul
if errorlevel 1 goto :install_pyinstaller

REM Optional: Check if requests is installed (for better networking)
python -c "import requests" >nul 2>nul
if errorlevel 1 goto :install_requests

goto :start_build

:python_not_found
echo Python not found in PATH.
echo Please install Python 3.7+ and add it to your PATH.
echo.
pause
exit /b 1

:install_pyinstaller
echo PyInstaller not found. Installing
python -m pip install pyinstaller
if errorlevel 1 goto :pyinstaller_failed
goto :install_requests

:pyinstaller_failed
echo Failed to install PyInstaller.
echo.
pause
exit /b 1

:install_requests
echo requests library not found. Installing (recommended for better networking)
python -m pip install requests
REM Continue even if requests install fails

:start_build
REM Clean previous build
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

echo.
echo Creating portable .exe with PyInstaller
echo.

REM Build with PyInstaller
echo Running PyInstaller
pyinstaller --onefile --windowed --add-data "update.bat;." --name "DHH-Installer" --icon=NONE --clean installer.py

if errorlevel 1 goto :build_failed

echo.
echo ============================================
echo Build completed successfully!
echo ============================================
echo.
if exist dist\DHH-Installer.exe (
    echo Output: dist\DHH-Installer.exe
    echo.
    echo The installer is ready to use. It's a portable .exe file with all dependencies bundled.
) else (
    echo WARNING: Could not find output executable. Check dist directory.
)

echo.
pause
exit /b 0

:build_failed
echo.
echo ============================================
echo Build failed! Check the error messages above.
echo ============================================
echo.
pause
exit /b 1
