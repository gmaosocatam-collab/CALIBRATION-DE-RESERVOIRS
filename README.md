# 🛢️ Application de Calibration ISO 12917-1:2017
## Guide de démarrage complet

---

## 1️⃣ INSTALLATION

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Terminal/Command Prompt

### Étapes d'installation

#### Sur Windows :
```bash
# 1. Ouvrir Command Prompt (cmd.exe)

# 2. Se placer dans le dossier du projet
cd chemin/vers/dossier

# 3. Créer un environnement virtuel (recommandé)
python -m venv venv
venv\Scripts\activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Lancer l'application
streamlit run streamlit_app.py
```

#### Sur macOS/Linux :
```bash
# 1. Ouvrir Terminal

# 2. Se placer dans le dossier du projet
cd chemin/vers/dossier

# 3. Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Lancer l'application
streamlit run streamlit_app.py
```

---

## 2️⃣ LANCEMENT DE L'APPLICATION

Une fois l'installation terminée, lancez simplement :

```bash
streamlit run streamlit_app.py
```

L'application s'ouvrira automatiquement dans votre navigateur par défaut à l'adresse :
```
http://localhost:8501
```

Si ce n'est pas le cas, ouvrez manuellement le lien dans votre navigateur.

---

## 3️⃣ STRUCTURE DE L'APPLICATION

### 📋 Onglet 1 : "Paramètres"
Entre les paramètres de votre réservoir :

1. **Mesures de circonférence**
   - Entrez 3 lectures de circonférence (mètres)
   - L'application valide automatiquement (écart ≤ 3mm selon ISO)
   - Le diamètre est calculé automatiquement

2. **Dimensions du réservoir**
   - Longueur du cylindre (mètres)
   - Type de têtes (Knuckle-dish, Elliptique, Sphérique, Plate)
   - Longueur de chaque tête (mètres)

3. **Inclinaison (Tilt)**
   - Entrez le tilt en degrés
   - La variation de hauteur est calculée automatiquement

4. **Corrections**
   - Température de référence
   - Pression de référence
   - Volume de deadwood

### 📊 Onglet 2 : "Tableau de jaugeage"
Affichage du tableau complet avec :
- Hauteur de liquide (m, cm, mm)
- Volumes du cylindre, des têtes, et total
- Capacités en m³ et litres
- Export possible en CSV, Excel, ou TXT

### 📈 Onglet 3 : "Courbe de calibration"
Visualisation graphique :
- Courbe principale hauteur vs volume
- Décomposition cylindre/têtes
- Comparaison des volumes

### 📖 Onglet 4 : "Guide d'utilisation"
Guide complet avec :
- Procédures de mesure détaillées
- Instruments et précisions
- Bonnes pratiques
- Erreurs courantes
- Fréquence de recalibration

### ℹ️ Onglet 5 : "À propos"
Information sur :
- Norme ISO 12917-1:2017
- À propos de l'application
- Limitations et hypothèses
- Références normatives

---

## 4️⃣ GUIDE PRATIQUE D'UTILISATION

### Scénario complet : Calibrer un réservoir

#### ÉTAPE 1 : Préparer les mesures

**Sur site :**
1. Remplissez le réservoir à capacité normale
2. Attendez 24 heures (stabilisation thermique)
3. Préparez les instruments :
   - Mètre ruban (ISO 4313)
   - Niveau optique ou clinomètre
   - Craie pour marques de référence

#### ÉTAPE 2 : Prendre les mesures

**Circonférence :**
- À 1/4 et 3/4 de la longueur du segment
- Enroulez le mètre perpendiculairement à l'axe
- Prenez 3 lectures → Notes : 10.502m, 10.504m, 10.501m

**Longueur :**
- Cylindre : intersection d'une tête à l'autre = 10.0m
- Têtes : profondeur radiale = 0.835m chacune

**Tilt :**
- Mesurez dénivellation entre extrémités
- Exemple : 1.3m de dénivellation sur 10m = 1.5°

#### ÉTAPE 3 : Entrer les données dans l'application

1. Allez à l'onglet "Paramètres"
2. Entrez les 3 lectures de circonférence
3. Attendez la validation (✅ ou ❌)
4. Remplissez les autres champs
5. Visionnez le résumé en bas

#### ÉTAPE 4 : Générer les documents

1. Allez à l'onglet "Tableau de jaugeage"
2. Téléchargez en CSV/Excel
3. Allez à l'onglet "Courbe de calibration"
4. Sauvegardez les images des courbes

#### ÉTAPE 5 : Archiver

- Conservez les données 7 ans minimum
- Archivez : mesures brutes, tableau, rapport
- Mettez à jour si modification deadwood

---

## 5️⃣ INTERPRÉTATION DES RÉSULTATS

### Validation des mesures

✅ **Valide :**
```
Écart entre 3 lectures ≤ 3 mm
Exemple : 10.502, 10.504, 10.501 m → Écart 3 mm = VALIDE
```

❌ **Non valide :**
```
Écart entre 3 lectures > 3 mm
Exemple : 10.502, 10.504, 10.520 m → Écart 18 mm = INVALIDE
→ Répétez les mesures
```

### Tableau de jaugeage

| Hauteur | Volume total | Litres | Interprétation |
|---------|--------------|--------|---|
| 0.5m | 9.679 m³ | 9,679 L | ~3% de capacité |
| 1.0m | 24.971 m³ | 24,971 L | ~26% de capacité |
| 1.5m | 42.530 m³ | 42,530 L | ~44% de capacité |
| 2.0m | 60.614 m³ | 60,614 L | ~62% de capacité |
| 3.0m | 91.731 m³ | 91,731 L | ~95% de capacité |

### Courbes

- **Courbe linéaire :** Augmentation proportionnelle hauteur/volume
- **Décomposition :** Contribution croissante des têtes pour h > 50%
- **Pente :** Plus raide en bas (fine croissance) qu'au milieu (croissance linéaire)

---

## 6️⃣ PARAMÈTRES COURANTS

### Réservoir type (industrie pétrolière)
```
Diamètre : 2.5 à 4.0 m
Longueur : 5 à 30 m
Tilt : 0.5° à 2.0°
Têtes : Elliptiques (ratio 2:1)
Deadwood : 0.5 à 5.0 m³
```

### Réservoir petit/moyen
```
Exemple : Ravitaillement carburant
Diamètre : 1.5 m
Longueur : 3 m
Tilt : < 0.5°
Têtes : Plate ou Knuckle-dish
Deadwood : 0.1 m³
```

### Réservoir grande capacité
```
Exemple : Stockage pétrolier
Diamètre : 4.0 m
Longueur : 20 m
Tilt : 1.0° à 1.5°
Têtes : Elliptiques
Deadwood : 10 m³
Capacité : ~200,000 L
```

---

## 7️⃣ DÉPANNAGE

### Problème : Application ne lance pas

**Solution :**
1. Vérifiez Python installé : `python --version`
2. Vérifiez dépendances : `pip list`
3. Réinstallez : `pip install -r requirements.txt`
4. Relancez : `streamlit run streamlit_app.py`

### Problème : Validation échoue (écart > 3mm)

**Solution :**
1. Mesures probables sources de décalage :
   - Tension inconsistante du mètre
   - Mal enroulé autour du réservoir
   - Points de mesure mal définis
2. Répétez les mesures 2-3 fois
3. Assurez-vous d'avoir exactement 3 lectures

### Problème : Import Excel échoue

**Solution :**
- Vérifiez openpyxl installé : `pip install openpyxl`
- Relancez l'application

### Problème : Graphiques ne s'affichent pas

**Solution :**
- Actualisez la page (F5)
- Vérifiez matplotlib installé : `pip install matplotlib`

---

## 8️⃣ TIPS & ASTUCES

### 💡 Pour précision maximale :
1. Mesurez 3 fois chaque point
2. Utilisez mètre ruban ISO 4313 Grade A
3. Laissez 24h stabilisation thermique
4. Enregistrez température ambiante
5. Documentez tout (photos, notes)

### 💡 Pour rapidité :
1. Téléchargez le template pré-rempli
2. Utilisez symboles de copie-colle
3. Générez rapports en batch (CSV)

### 💡 Pour conformité :
1. Gardez copie des données brutes 7 ans
2. Signez les rapports (recommandé)
3. Datez toutes les mesures
4. Référencez norme ISO 12917-1:2017

---

## 9️⃣ EXPORTS DISPONIBLES

### Format CSV
- Importable dans Excel, Access, bases de données
- Tableau complet avec toutes les colonnes
- Parfait pour archivage numérique

### Format Excel (.xlsx)
- Pré-formaté avec tableaux
- Cartes de style appliquées
- Prêt pour rapports clients

### Format TXT
- Fichier texte pur
- Lisible partout, pas de dépendances
- Sauvegarde archivale

### Graphiques
- Exportez depuis Streamlit (clic droit → Enregistrer image)
- PNG, SVG disponibles
- Résolution 100 dpi (standard imprimé)

---

## 🔟 SUPPORT ET CONTACT

### Questions sur l'application :
- Consultez l'onglet "Guide d'utilisation"
- Lire les explications en info-bulles (hover sur ?)
- Vérifier "À propos"

### Questions sur ISO 12917-1 :
- Consultez le standard officiel
- Contactez expert métrologie pétrolière
- Vérifiez réglementations nationales

### Bug ou problème technique :
- Notez étapes de reproduction
- Joignez captures d'écran
- Décrivez erreur affichée
- Contactez développeur

---

## 📋 CHECKLIST PRE-MESURE

Avant de mesurer votre réservoir :

- [ ] Réservoir rempli à capacité normale
- [ ] 24h d'attente minimum
- [ ] Mètre ruban vérifié et étalonné
- [ ] Niveau/clinomètre disponible
- [ ] Points de référence marqués
- [ ] Météo stable (pas d'extrêmes)
- [ ] 2 personnes pour sécurité
- [ ] Formulaires prêts
- [ ] Appareil photo pour documentation
- [ ] Application Streamlit lancée et testée

---

## 📋 CHECKLIST POST-MESURE

Après avoir mesuré votre réservoir :

- [ ] Données brutes enregistrées
- [ ] Validation ✅ ou ❌ complétée
- [ ] Tableau de jaugeage généré
- [ ] Courbes de calibration visionnées
- [ ] Exports en CSV/Excel sauvegardés
- [ ] Rapport archivé (copie papier/numérique)
- [ ] Signatures collectées (si requis)
- [ ] Date d'archivage notée
- [ ] Prochaine recalibration planifiée (2-5 ans)
- [ ] Alertes si modification deadwood

---

## 🎓 RESSOURCES PÉDAGOGIQUES

### Comprendre les formules

**Diamètre :**
```
D = Circonférence / π
Exemple : 10.502 / 3.14159 = 3.341 m
```

**Section transversale :**
```
Pour segment de cercle rempli jusqu'à hauteur h :
A = R² × arccos((R-h)/R) - (R-h) × √(2Rh - h²)

Cas limites :
- h = 0 : A = 0 (vide)
- h = D : A = π × R² (plein)
- h = D/2 : A = π × R² / 2 (demi-plein)
```

**Tilt (variation de hauteur) :**
```
La hauteur d'un réservoir incliné varie linéairement :
Δh = (L/2) × tan(tilt)
Exemple : L = 10m, tilt = 1.5° → Δh = 5 × tan(1.5°) = 0.131m = 131 mm

Cela signifie que la hauteur varie de ±131 mm entre les extrémités !
```

---

**Bonne utilisation de l'application ! 🛢️**

Pour questions : Consultez le Guide d'utilisation complet (Onglet 4)

