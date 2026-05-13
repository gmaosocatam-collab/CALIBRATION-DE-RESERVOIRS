#!/bin/bash
# Script de lancement rapide pour Linux/macOS
# ISO 12917-1 Calibration App

echo ""
echo "========================================"
echo "   Application ISO 12917-1:2017"
echo "   Calibration de Reservoirs"
echo "========================================"
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "ERREUR: Python 3 n'est pas installé"
    echo ""
    echo "Veuillez installer Python 3.8+ depuis https://python.org"
    echo ""
    exit 1
fi

# Vérifier les dépendances
echo "Verification des dépendances..."
python3 test_dependencies.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Installation des dépendances..."
    pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "ERREUR lors de l'installation des dépendances"
        exit 1
    fi
fi

# Lancer l'application
echo ""
echo "Lancement de l'application..."
echo "L'application s'ouvrira dans votre navigateur par défaut"
echo "Si ce n'est pas le cas, ouvrez manuellement : http://localhost:8501"
echo ""
echo "Appuyez sur CTRL+C pour arreter l'application"
echo ""

streamlit run streamlit_app.py
