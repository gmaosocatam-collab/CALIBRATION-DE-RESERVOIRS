# 📊 EXEMPLE COMPLET DE CALIBRATION ISO 12917-1:2017

## Cas d'étude : Réservoir horizontal de stockage pétrolier

### Informations générales

**Date de calibration :** 15 mars 2024
**Client :** Dépôt de ravitaillement XYZ
**Numéro de réservoir :** TANK-001
**Localisation :** Latitude 48.8°N, Longitude 2.3°E
**Conditions météo :** 18°C, HR 55%, sans vent
**Opérateur :** Jean Dupont, Certifié ISO 17025

---

## 1. MESURES DE CIRCONFÉRENCE

### Segment 1 (1/4 de la longueur)

| Lecture | Valeur (m) | Notes |
|---------|-----------|-------|
| 1ère | 10.502 | Mesure initiale |
| 2e | 10.504 | Tension ajustée |
| 3e | 10.501 | Vérification |

**Validation :** ✅ VALIDE
- Écart min-max = 10.504 - 10.501 = 3 mm
- Critère ISO = ≤ 3 mm
- **Moyenne = 10.502 m**

### Segment 2 (3/4 de la longueur)

| Lecture | Valeur (m) | Notes |
|---------|-----------|-------|
| 1ère | 10.505 | Mesure initiale |
| 2e | 10.503 | Répétition |
| 3e | 10.504 | Vérification |

**Validation :** ✅ VALIDE
- Écart min-max = 10.505 - 10.503 = 2 mm
- Critère ISO = ≤ 3 mm
- **Moyenne = 10.504 m**

**Moyenne globale (2 segments) = 10.503 m**

---

## 2. CALCUL DU DIAMÈTRE

```
Formule : D = C / π
D = 10.503 / 3.14159
D = 3.342 m
```

**Diamètre retenu = 3.342 m**

---

## 3. MESURES DE LONGUEUR

### Longueur du cylindre

**Méthode :** Mètre ruban de référence

| Mesure | Longueur (m) | Notes |
|--------|--------------|-------|
| 1ère | 10.001 | De repère à repère |
| 2e | 9.999 | Répétition |
| 3e | 10.000 | Vérification |

**Validation :** ✅ VALIDE (écart 2 mm)
**Longueur retenue = 10.000 m**

### Longueur des têtes elliptiques

**Type :** Elliptique (ratio 2:1 standard)

| Mesure | Longueur (m) | Notes |
|--------|--------------|-------|
| Tête avant | 0.835 | Mesure radiale |
| Tête arrière | 0.836 | Mesure radiale |

**Moyenne = 0.8355 m, arrondie à 0.835 m**
**Longueur retenue par tête = 0.835 m**

---

## 4. MESURE DE L'INCLINAISON (TILT)

### Méthode : Niveau optique

**Équipement :** Niveau optique Leica NAK2 (ISO 10309)
**Opérateur :** Topographe certifié

**Résultats :**

| Point | Hauteur de niveau (m) | Distance horizontale (m) |
|-------|-------|--------|
| Extrémité avant | 2.1500 | - |
| Extrémité arrière | 2.0187 | 10.0000 |

**Calcul de tilt :**
```
Dénivellation = 2.1500 - 2.0187 = 0.1313 m
Tilt (rad) = arctan(0.1313 / 10.0) = arctan(0.01313) = 0.01311 rad
Tilt (°) = 0.01311 × 180 / π = 0.7513° ≈ 0.75°
```

**Tilt retenu = 0.75°**

**Variation de hauteur aux extrémités :**
```
Δh = (L/2) × tan(tilt)
Δh = (10.0/2) × tan(0.75°)
Δh = 5 × 0.01311 = 0.0656 m = 65.6 mm
```

**⚠️ Variation = ±65.6 mm (à prendre en compte pour précision)**

---

## 5. DEADWOOD (ÉQUIPEMENTS INTERNES)

### Inventaire des équipements internes

| Équipement | Description | Volume (m³) | Notes |
|-----------|-----------|-----------|-------|
| Tube de circulation | Ø 50mm, L 9.5m | 0.189 | Acier |
| Tube d'immersion | Ø 25mm, L 10m | 0.049 | Mesure niveau |
| Capteur température | Sonde Pt100 | 0.001 | Négligeable |
| Agitateur | Palettes + axe | 0.012 | Non actif |
| Chicane (1) | Plaque 0.5x0.5m | 0.005 | Tôle d'acier |

**Total deadwood = 0.256 m³ ≈ 0.26 m³**

---

## 6. PARAMÈTRES DE CORRECTION

| Paramètre | Valeur | Justification |
|-----------|--------|-------|
| Température de référence | 15°C | Standard ASTM |
| Pression de référence | 101.325 kPa | Pression atm. |
| Coefficient dilatation acier | 0.000012/°C | ISO 1975 |

**Correction thermique (si applicable) :**
- À 15°C (référence) : volume de base
- À 20°C : +0.06% (0.36 m³ pour 60,000 L)
- À 25°C : +0.12% (0.72 m³ pour 60,000 L)

---

## 7. TABLEAU DE JAUGEAGE (EXTRAIT)

| Hauteur (m) | Cylindre (m³) | Têtes (m³) | Total brut (m³) | Deadwood (m³) | Total net (m³) | Litres nets |
|------------|------------|-----------|------------|-----------|-----------|----------|
| 0.0 | 0.000 | 0.000 | 0.000 | 0.26 | -0.26 | -260 |
| 0.5 | 8.715 | 0.147 | 8.862 | 0.26 | 8.602 | 8,602 |
| 1.0 | 22.232 | 0.294 | 22.526 | 0.26 | 22.266 | 22,266 |
| 1.5 | 38.854 | 0.441 | 39.295 | 0.26 | 39.035 | 39,035 |
| 2.0 | 55.347 | 0.588 | 55.935 | 0.26 | 55.675 | 55,675 |
| 2.5 | 71.316 | 0.735 | 72.051 | 0.26 | 71.791 | 71,791 |
| 3.0 | 82.966 | 0.882 | 83.848 | 0.26 | 83.588 | 83,588 |
| 3.342 | 87.467 | 0.964 | 88.431 | 0.26 | 88.171 | 88,171 |

**Capacité totale (net) = 88,171 litres ≈ 88.2 m³**

---

## 8. CONTRÔLE DE QUALITÉ

### Vérifications effectuées

- ✅ Mesures de circonférence : écart ≤ 3 mm (conforme ISO 12917-1)
- ✅ Mesures de longueur : écart ≤ 3 mm (conforme ISO)
- ✅ Tilt mesuré avec théodolite certifié (ISO 10309)
- ✅ Deadwood inventorié et pesé
- ✅ Deux opérateurs pour vérification indépendante
- ✅ Photos documentaires prises
- ✅ Conditions météo stables (sans extrêmes)

### Incertitude estimée

```
Incertitude globale ≈ ±0.5% (typique ISO 12917-1)
Pour capacité de 88,000 L : ±440 L

Sources d'incertitude :
- Mesure de circonférence : ±10 mm (iso)
- Mesure de longueur : ±10 mm
- Tilt : ±0.1°
- Deadwood : ±5%
```

---

## 9. RAPPORT FINAL

### Conclusion

Le réservoir **TANK-001** a été calibré selon la norme **ISO 12917-1:2017** par **méthode manuelle externe**.

**Capacité certifiée (volume net) = 88,171 litres**

### Documents fournis

1. ✅ Tableau de jaugeage complet (CSV, Excel, PDF)
2. ✅ Courbes de calibration (graphiques)
3. ✅ Fiche de données (cette page)
4. ✅ Certificat de calibration (certificat)
5. ✅ Photos documentaires (dossier)

### Validité et maintenance

- **Date de calibration :** 15 mars 2024
- **Prochaine recalibration recommandée :** 15 mars 2026 (2 ans)
- **Reconduction obligatoire si :**
  - Modification du deadwood
  - Déformation visible du réservoir
  - Changement de fondation (> 5 mm)
  - Exigence réglementaire nationale

### Signature

**Opérateur :** Jean Dupont
**Date :** 15 mars 2024
**Signature :** _________________________
**Sceau/Cachet :** [À imprimer]

**Certifié conforme ISO 12917-1:2017**

---

## 10. DONNÉES POUR SAISIE DANS L'APPLICATION

Copiez-collez ces données dans l'application Streamlit :

```
MESURES DE CIRCONFÉRENCE :
1ère lecture : 10.502 m
2e lecture : 10.504 m
3e lecture : 10.501 m
→ Validation : ✅ VALIDE (écart 3 mm)

DIMENSIONS :
Longueur cylindre : 10.0 m
Type de têtes : Elliptique
Longueur de chaque tête : 0.835 m

INCLINAISON :
Tilt : 0.75°

CORRECTIONS :
Température de référence : 15°C
Pression de référence : 101.325 kPa
Deadwood : 0.26 m³
```

**Résultat attendu :**
```
Diamètre : 3.341 m
Capacité totale (net) : ~88,000 L
```

---

**FIN DE L'EXEMPLE**

Vous pouvez maintenant utiliser cet exemple comme cas de test pour l'application Streamlit.

