@echo off
REM Script de lancement rapide pour Windows
REM ISO 12917-1 Calibration App

echo.
echo ========================================
echo    Application ISO 12917-1:2017
echo    Calibration de Reservoirs
echo ========================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERREUR: Python n'est pas installé ou non accessible
    echo.
    echo Veuillez installer Python 3.8+ depuis https://python.org
    echo.
    pause
    exit /b 1
)

REM Vérifier les dépendances
echo Verification des dépendances...
python test_dependencies.py

if %errorlevel% neq 0 (
    echo.
    echo Installation des dépendances...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo.
        echo ERREUR lors de l'installation des dépendances
        pause
        exit /b 1
    )
)

REM Lancer l'application
echo.
echo Lancement de l'application...
echo L'application s'ouvrira dans votre navigateur par défaut
echo Si ce n'est pas le cas, ouvrez manuellement : http://localhost:8501
echo.
echo Appuyez sur CTRL+C pour arreter l'application
echo.

streamlit run streamlit_app.py

pause
