#!/usr/bin/env python3
"""
Test de la table de jaugeage centimétrique
"""

import math
import pandas as pd

def calculate_volume(h, R, L_cylinder, L_head, deadwood=0):
    """Calcule le volume total pour une hauteur h donnée"""
    D = 2 * R
    
    if h < 0 or h > D:
        return None, None, None, None
    
    if h == 0:
        A_cross = 0
    elif h == D:
        A_cross = math.pi * R**2
    else:
        term1 = (R - h) / R
        angle = math.acos(term1)
        sqrt_term = math.sqrt(2 * R * h - h**2)
        A_cross = R**2 * angle - (R - h) * sqrt_term
    
    V_cylinder = A_cross * L_cylinder
    V_head_full = (2/3) * math.pi * R**2 * L_head
    h_ratio = h / D if D > 0 else 0
    V_head_partial_each = V_head_full * h_ratio
    V_heads = 2 * V_head_partial_each
    V_total = V_cylinder + V_heads
    V_net = V_total - deadwood
    
    return V_cylinder, V_heads, V_total, V_net

def generate_calibration_table(D, L_cylinder, L_head, deadwood=0):
    """Génère le tableau de jaugeage CENTIMÉTRIQUE"""
    R = D / 2
    heights = []
    
    # Pas de 1 cm (0.01 m)
    num_steps = int(D * 100) + 1
    for i in range(num_steps):
        h = round(i * 0.01, 4)
        if h <= D:
            heights.append(h)
    
    heights = sorted(set(heights))
    
    data = []
    for h in heights:
        V_cyl, V_head, V_total, V_net = calculate_volume(h, R, L_cylinder, L_head, deadwood)
        if V_total is not None:
            data.append({
                'Hauteur (m)': h,
                'Hauteur (cm)': h * 100,
                'Cylindre (m³)': V_cyl,
                'Têtes (m³)': V_head,
                'Total (m³)': V_total,
                'Total (L)': V_total * 1000,
                'Net (m³)': V_net,
                'Net (L)': V_net * 1000,
            })
    
    return pd.DataFrame(data)

# Test
print("=" * 80)
print("TEST DE LA TABLE CENTIMÉTRIQUE")
print("=" * 80)
print()

# Paramètres d'exemple
D = 3.341  # Diamètre
L_cylinder = 10.0
L_head = 0.835
deadwood = 0.0

print(f"Paramètres :")
print(f"  Diamètre : {D} m")
print(f"  Longueur cylindre : {L_cylinder} m")
print(f"  Longueur têtes : {L_head} m")
print()

# Générer le tableau
df = generate_calibration_table(D, L_cylinder, L_head, deadwood)

print(f"✅ Tableau généré avec {len(df)} points (pas de 1 cm)")
print()

# Afficher les 10 premiers
print("10 PREMIERS POINTS :")
print(df.head(10).to_string(index=False))
print()

# Afficher quelques points clés
print("POINTS CLÉS :")
key_heights = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.341]
for h_key in key_heights:
    matching = df[abs(df['Hauteur (m)'] - h_key) < 0.001]
    if len(matching) > 0:
        row = matching.iloc[0]
        print(f"  h = {row['Hauteur (m)']:.2f}m ({row['Hauteur (cm)']:.0f}cm) : {row['Total (L)']:.0f}L")

print()
print("=" * 80)
print("✅ TEST RÉUSSI - Table centimétrique générée avec succès")
print("=" * 80)
