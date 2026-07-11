@echo off
title Zodiac Optimizer - Build
echo ============================================
echo   Zodiac Optimizer - EXE Build
echo ============================================
echo.

REM Abhaengigkeiten installieren
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

echo.
echo Baue ZodiacOptimizer.exe ...
echo.

REM --uac-admin sorgt dafuer, dass die EXE automatisch Adminrechte anfordert
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --uac-admin ^
    --name ZodiacOptimizer ^
    --collect-all customtkinter ^
    main.py

echo.
if exist dist\ZodiacOptimizer.exe (
    echo ============================================
    echo   Fertig! Die EXE liegt hier:
    echo   dist\ZodiacOptimizer.exe
    echo ============================================
) else (
    echo   BUILD FEHLGESCHLAGEN - siehe Ausgabe oben.
)
echo.
pause
