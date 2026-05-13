# ⚡ DÉMARRAGE ULTRA-RAPIDE

## 30 secondes pour lancer l'application

### Windows
```bash
# 1. Double-cliquez sur : run.bat
# → L'application s'ouvre automatiquement
```

### macOS / Linux
```bash
# 1. Terminal → Allez au dossier
cd /chemin/vers/dossier

# 2. Lancez le script
bash run.sh
# → L'application s'ouvre automatiquement
```

### Tous les systèmes (manuel)
```bash
# 1. Terminal/CMD → Allez au dossier
cd /chemin/vers/dossier

# 2. Installez les dépendances (une seule fois)
pip install -r requirements.txt

# 3. Lancez l'application
streamlit run streamlit_app.py
```

---

## L'application est ouverte ! Maintenant :

### 📋 Onglet 1 : PARAMÈTRES
1. **Entrez 3 lectures de circonférence** (exemple : 10.502, 10.504, 10.501)
   - ✅ L'app valide automatiquement (écart ≤ 3mm)
2. **Remplissez les dimensions** (longueur cylindre, type têtes, etc.)
3. **Entrez le tilt** (inclinaison du réservoir)
4. **Ajoutez corrections** (deadwood, température, pression)

### 📊 Onglet 2 : TABLEAU DE JAUGEAGE
- Tableau complet avec tous les volumes
- Téléchargez en **CSV / Excel / TXT**
- Exportez les données

### 📈 Onglet 3 : COURBES DE CALIBRATION
- Visualisez hauteur vs volume
- Voir décomposition cylindre + têtes
- Sauvegardez les graphiques

### 📖 Onglet 4 : GUIDE COMPLET
- Procédures de mesure détaillées
- Instruments recommandés
- Bonnes pratiques et erreurs courantes

---

## Exemple rapide (2 min)

Copiez-collez ces valeurs d'exemple :

| Champ | Valeur |
|-------|--------|
| 1ère lecture | 10.502 |
| 2e lecture | 10.504 |
| 3e lecture | 10.501 |
| Longueur cylindre | 10.0 |
| Type têtes | Elliptique |
| Longueur têtes | 0.835 |
| Tilt | 1.5 |
| Deadwood | 0.0 |

→ **Résultat : Capacité de ~98,000 litres**

---

## Fichiers fournis

```
📂 Application ISO 12917-1
├── streamlit_app.py          ← Application principale
├── run.bat                   ← Lancement Windows
├── run.sh                    ← Lancement Linux/macOS
├── requirements.txt          ← Dépendances Python
├── test_dependencies.py      ← Vérifier installation
├── README.md                 ← Guide complet
├── QUICK_START.md            ← Cette page
└── EXEMPLE_COMPLET.md        ← Exemple détaillé
```

---

## Dépannage rapide

| Problème | Solution |
|----------|----------|
| **"Command not found"** | Python non installé → [python.org](https://python.org) |
| **"Module not found"** | `pip install -r requirements.txt` |
| **Port 8501 occupé** | `streamlit run streamlit_app.py --server.port 8502` |
| **App ne démarre pas** | `python test_dependencies.py` |

---

## Ressources

📖 **Guide complet** : Lisez `README.md`
🎓 **Exemple détaillé** : Voir `EXEMPLE_COMPLET.md`
📚 **Norme ISO** : [ISO 12917-1:2017](https://www.iso.org)
💬 **Questions** : Onglet 4 de l'app (Guide d'utilisation)

---

**C'est tout ! Vous êtes prêt. 🚀**

