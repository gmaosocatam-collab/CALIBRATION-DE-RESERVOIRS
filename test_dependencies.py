#!/usr/bin/env python3
"""
Script de test des dépendances et vérification basique de la fonctionnalité
"""

import sys
from datetime import datetime

print("=" * 80)
print("VÉRIFICATION DES DÉPENDANCES - Application ISO 12917-1")
print("=" * 80)
print()

# Liste des dépendances
dependencies = [
    'streamlit',
    'pandas',
    'numpy',
    'matplotlib',
    'openpyxl',
    'dateutil'
]

# Test des imports
print(f"⏱️  Test réalisé le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

failed = []
passed = []

for dep in dependencies:
    try:
        if dep == 'dateutil':
            __import__('dateutil.parser')
        else:
            __import__(dep)
        passed.append(dep)
        print(f"✅ {dep:<20} OK")
    except ImportError:
        failed.append(dep)
        print(f"❌ {dep:<20} MANQUANT")

print()
print("=" * 80)

if not failed:
    print("✅ TOUS LES TESTS SONT PASSÉS")
    print()
    print("Vous pouvez maintenant lancer l'application avec :")
    print()
    print("  streamlit run streamlit_app.py")
    print()
    sys.exit(0)
else:
    print(f"❌ {len(failed)} dépendance(s) manquante(s)")
    print()
    print("Pour installer les dépendances manquantes :")
    print()
    print("  pip install -r requirements.txt")
    print()
    print("Ou installez individuellement :")
    for dep in failed:
        if dep == 'dateutil':
            print(f"  pip install python-dateutil")
        else:
            print(f"  pip install {dep}")
    print()
    sys.exit(1)
