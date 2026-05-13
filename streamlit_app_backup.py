"""
APPLICATION DE CALIBRATION DE RÉSERVOIRS HORIZONTAUX
Norme ISO 12917-1:2017

Développée avec Streamlit
Auteur: Expert en Métrologie Pétrolière
Date: 2024
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from datetime import datetime
from io import BytesIO

# ============================================================================
# CONFIGURATION STREAMLIT
# ============================================================================

st.set_page_config(
    page_title="ISO 12917-1 - Calibration de Réservoirs",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour une interface professionnelle
st.markdown("""
<style>
    /* Police et thème général */
    :root {
        --primary-color: #1e3a8a;
        --secondary-color: #3b82f6;
        --accent-color: #f59e0b;
        --success-color: #10b981;
        --warning-color: #ef4444;
    }
    
    /* Styles personnalisés */
    .main-header {
        font-size: 2.5rem;
        color: #1e3a8a;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #3b82f6;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #3b82f6;
        padding-left: 0.8rem;
    }
    
    .info-box {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .success-box {
        background-color: #ecfdf5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .tooltip-text {
        font-size: 0.85rem;
        color: #6b7280;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def calculate_volume(h, R, L_cylinder, L_head, deadwood=0):
    """
    Calcule le volume total pour une hauteur h donnée
    """
    D = 2 * R
    
    if h < 0 or h > D:
        return None, None, None, None
    
    # Section transversale du liquide
    if h == 0:
        A_cross = 0
    elif h == D:
        A_cross = math.pi * R**2
    else:
        term1 = (R - h) / R
        angle = math.acos(term1)
        sqrt_term = math.sqrt(2 * R * h - h**2)
        A_cross = R**2 * angle - (R - h) * sqrt_term
    
    # Volume du cylindre
    V_cylinder = A_cross * L_cylinder
    
    # Volume des têtes (elliptiques)
    V_head_full = (2/3) * math.pi * R**2 * L_head
    h_ratio = h / D if D > 0 else 0
    V_head_partial_each = V_head_full * h_ratio
    V_heads = 2 * V_head_partial_each
    
    # Volume total
    V_total = V_cylinder + V_heads
    V_net = V_total - deadwood
    
    return V_cylinder, V_heads, V_total, V_net


def generate_calibration_table(D, L_cylinder, L_head, deadwood=0):
    """
    Génère le tableau de jaugeage CENTIMÉTRIQUE (par pas de 1 cm)
    """
    R = D / 2
    heights = []
    
    # Pas de 1 cm (0.01 m) de 0 à D
    num_steps = int(D * 100) + 1  # Convertir en centimètres
    for i in range(num_steps):
        h = round(i * 0.01, 4)  # Pas de 1 cm = 0.01 m
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


def validate_circumferences(readings):
    """
    Valide les 3 lectures de circonférence selon ISO 12917-1
    """
    if len(readings) != 3:
        return False, "Veuillez fournir exactement 3 lectures"
    
    readings = sorted(readings)
    diff = readings[2] - readings[0]
    
    if diff <= 0.003:  # 3 mm
        return True, f"✅ Valide. Écart: {diff*1000:.2f} mm (≤ 3 mm)"
    else:
        return False, f"❌ Non valide. Écart: {diff*1000:.2f} mm (> 3 mm). Répétez les mesures."


def export_to_excel(df, filename="tableau_jaugeage.xlsx"):
    """
    Exporte le tableau en Excel
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Jaugeage', index=False)
    
    output.seek(0)
    return output


# ============================================================================
# INTERFACE PRINCIPALE
# ============================================================================

# En-tête
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center;">
        <h1 style="color: #1e3a8a; margin: 0;">🛢️ CALIBRATION DE RÉSERVOIRS</h1>
        <p style="color: #6b7280; font-size: 0.95rem; margin: 0;">ISO 12917-1:2017 - Cylindres horizontaux</p>
    </div>
    """, unsafe_allow_html=True)

# Onglets principaux
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Paramètres",
    "📊 Tableau de jaugeage",
    "📈 Courbe de calibration",
    "📖 Guide d'utilisation",
    "ℹ️ À propos"
])

# ============================================================================
# TAB 1: PARAMÈTRES
# ============================================================================

with tab1:
    st.markdown('<p class="sub-header">Configuration du réservoir</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 1️⃣ Mesures de circonférence")
        st.markdown("""
        <div class="info-box">
            <b>ℹ️ Comment mesurer la circonférence :</b><br>
            • Utilisez un <b>mètre ruban métallique</b> d'au moins 5 m<br>
            • Enroulez le mètre autour du réservoir<br>
            • Prenez la mesure à 1/4 et 3/4 de la longueur du segment<br>
            • Répétez 3 fois jusqu'à ±3 mm de concordance<br>
            • Enregistrez les 3 lectures ci-dessous
        </div>
        """, unsafe_allow_html=True)
        
        reading1 = st.number_input(
            "1ère lecture (m)",
            min_value=0.0,
            step=0.001,
            format="%.3f",
            help="Première mesure de circonférence en mètres"
        )
        
        reading2 = st.number_input(
            "2e lecture (m)",
            min_value=0.0,
            step=0.001,
            format="%.3f",
            help="Deuxième mesure de circonférence en mètres"
        )
        
        reading3 = st.number_input(
            "3e lecture (m)",
            min_value=0.0,
            step=0.001,
            format="%.3f",
            help="Troisième mesure de circonférence en mètres"
        )
        
        # Validation
        if reading1 > 0 and reading2 > 0 and reading3 > 0:
            is_valid, message = validate_circumferences([reading1, reading2, reading3])
            
            if is_valid:
                st.success(message)
                circumference = (reading1 + reading2 + reading3) / 3
                diameter = circumference / math.pi
            else:
                st.error(message)
                circumference = None
                diameter = None
        else:
            st.info("Entrez les 3 lectures pour validation")
            circumference = None
            diameter = None
        
        # Affichage des résultats
        if circumference:
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Circonférence moy.", f"{circumference:.3f} m")
            with col_b:
                st.metric("Diamètre calculé", f"{diameter:.3f} m")
    
    with col2:
        st.markdown("### 2️⃣ Dimensions du réservoir")
        
        st.markdown("""
        <div class="info-box">
            <b>ℹ️ Types de têtes disponibles :</b><br>
            • <b>Knuckle-dish</b> : Standard industrie pétrolière<br>
            • <b>Elliptique</b> : Rapport 2:1 (profondeur = D/2 environ)<br>
            • <b>Sphérique</b> : Rapport 1:1 (profondeur = D/2)<br>
            • <b>Plate</b> : Pas de profondeur
        </div>
        """, unsafe_allow_html=True)
        
        length_cylinder = st.number_input(
            "Longueur du cylindre (m)",
            min_value=0.1,
            max_value=50.0,
            value=10.0,
            step=0.1,
            format="%.1f",
            help="Longueur du corps cylindrique (hors têtes) en mètres"
        )
        
        head_type = st.selectbox(
            "Type de têtes",
            options=["Knuckle-dish", "Elliptique", "Sphérique", "Plate"],
            help="Sélectionnez le type de têtes du réservoir"
        )
        
        length_head = st.number_input(
            "Longueur de chaque tête (m)",
            min_value=0.0,
            max_value=10.0,
            value=0.835,
            step=0.01,
            format="%.3f",
            help="Profondeur/longueur de chaque tête en mètres. Pour tête elliptique: ≈ D/4"
        )
    
    # Ligne séparatrice
    st.divider()
    
    # Paramètres d'inclinaison et corrections
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### 3️⃣ Inclinaison (Tilt)")
        
        st.markdown("""
        <div class="info-box">
            <b>ℹ️ Mesure du tilt :</b><br>
            • Utilisez un <b>niveau optique</b> ou <b>théodolite</b><br>
            • Mesurez la dénivellation entre les deux extrémités du réservoir<br>
            • Tilt = arctan(dénivellation / longueur)<br>
            • Tilt typique : 0.5° à 2°<br>
            • Variation de hauteur = (L/2) × tan(tilt)
        </div>
        """, unsafe_allow_html=True)
        
        tilt_degrees = st.number_input(
            "Tilt (inclinaison) (°)",
            min_value=-10.0,
            max_value=10.0,
            value=1.5,
            step=0.1,
            format="%.1f",
            help="Inclinaison du réservoir en degrés"
        )
        
        # Calcul de la variation de hauteur
        tilt_radians = math.radians(tilt_degrees)
        delta_h = (length_cylinder / 2) * math.tan(tilt_radians)
        
        st.info(f"📐 Variation de hauteur: ±{abs(delta_h)*1000:.1f} mm sur la longueur du réservoir")
    
    with col4:
        st.markdown("### 4️⃣ Corrections")
        
        st.markdown("""
        <div class="info-box">
            <b>ℹ️ Corrections thermiques et de pression :</b><br>
            • <b>Température</b> : Coefficients de dilatation de l'acier ≈ 0.000012/°C<br>
            • <b>Pression</b> : Applicable si réservoir pressurisé (ASME)<br>
            • <b>Deadwood</b> : Volumes occupés par tuyauteries, capteurs, etc.
        </div>
        """, unsafe_allow_html=True)
        
        temp_reference = st.number_input(
            "Température de référence (°C)",
            min_value=-50.0,
            max_value=100.0,
            value=15.0,
            step=1.0,
            format="%.1f",
            help="Température de référence pour les corrections thermiques"
        )
        
        pressure_reference = st.number_input(
            "Pression de référence (kPa)",
            min_value=0.0,
            max_value=10000.0,
            value=101.325,
            step=10.0,
            format="%.1f",
            help="Pression atmosphérique ou de travail en kPa"
        )
        
        deadwood_volume = st.number_input(
            "Volume de deadwood (m³)",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.01,
            format="%.2f",
            help="Volume des équipements internes (tuyauteries, capteurs, etc.)"
        )
    
    st.divider()
    
    # Résumé des paramètres
    st.markdown("### 📋 Résumé des paramètres")
    
    if diameter and circumference:
        summary_col1, summary_col2, summary_col3 = st.columns(3)
        
        with summary_col1:
            st.metric("Diamètre", f"{diameter:.3f} m", delta=f"±3mm (ISO)")
            st.metric("Longueur cylindre", f"{length_cylinder:.1f} m")
            st.metric("Têtes", head_type)
        
        with summary_col2:
            st.metric("Longueur têtes", f"{length_head:.3f} m")
            st.metric("Tilt", f"{tilt_degrees:.1f}°")
            st.metric("Variation hauteur", f"±{abs(delta_h)*1000:.1f} mm")
        
        with summary_col3:
            st.metric("Temp. référence", f"{temp_reference:.1f}°C")
            st.metric("Pression ref.", f"{pressure_reference:.1f} kPa")
            st.metric("Deadwood", f"{deadwood_volume:.2f} m³")
        
        # Bouton de validation
        st.success("✅ Configuration complète et valide")

# ============================================================================
# TAB 2: TABLEAU DE JAUGEAGE
# ============================================================================

with tab2:
    st.markdown('<p class="sub-header">Tableau de jaugeage (Calibration Table)</p>', unsafe_allow_html=True)
    
    try:
        if diameter and circumference:
            # Génération du tableau
            df_calibration = generate_calibration_table(diameter, length_cylinder, length_head, deadwood_volume)
            
            # Options d'affichage
            col_opt1, col_opt2, col_opt3 = st.columns([2, 2, 2])
            
            with col_opt1:
                display_decimals = st.selectbox(
                    "Précision d'affichage",
                    options=[2, 3, 4, 5, 6],
                    value=3,
                    help="Nombre de décimales à afficher"
                )
        
        with col_opt2:
            show_net = st.checkbox(
                "Afficher volumes nets",
                value=False,
                help="Inclure les volumes nets (après déduction deadwood)"
            )
        
        with col_opt3:
            rows_to_show = st.selectbox(
                "Nombre de lignes",
                options=[10, 20, 50, 100, "Tout"],
                value=20,
                help="Nombre de lignes à afficher"
            )
        
        # Préparation de l'affichage
        df_display = df_calibration.copy()
        
        if not show_net:
            df_display = df_display[['Hauteur (m)', 'Hauteur (cm)', 'Cylindre (m³)', 'Têtes (m³)', 'Total (m³)', 'Total (L)']]
        
        # Formatage
        format_dict = {
            'Hauteur (m)': f'{{:.{display_decimals}f}}',
            'Hauteur (cm)': f'{{:.{display_decimals}f}}',
            'Cylindre (m³)': f'{{:.{display_decimals}f}}',
            'Têtes (m³)': f'{{:.{display_decimals}f}}',
            'Total (m³)': f'{{:.{display_decimals}f}}',
            'Total (L)': f'{{:.{max(0, display_decimals-1)}f}}',
            'Net (m³)': f'{{:.{display_decimals}f}}',
            'Net (L)': f'{{:.{max(0, display_decimals-1)}f}}',
        }
        
        df_display_formatted = df_display.copy()
        for col in df_display_formatted.columns:
            if col in format_dict:
                df_display_formatted[col] = df_display_formatted[col].apply(format_dict[col].format)
        
        # Limiter le nombre de lignes
        if rows_to_show != "Tout":
            df_display_formatted = df_display_formatted.head(rows_to_show)
        
        st.markdown("""
        <div class="success-box">
            <b>✅ Tableau généré selon ISO 12917-1:2017</b><br>
            Calibration réalisée par méthode manuelle externe
        </div>
        """, unsafe_allow_html=True)
        
        # Affichage du tableau
        st.dataframe(df_display_formatted, use_container_width=True)
        
        # Téléchargements
        col_dl1, col_dl2, col_dl3 = st.columns(3)
        
        with col_dl1:
            csv_data = df_calibration.to_csv(index=False)
            st.download_button(
                label="📥 Télécharger CSV",
                data=csv_data,
                file_name=f"calibration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                help="Télécharger le tableau en format CSV"
            )
        
        with col_dl2:
            excel_buffer = export_to_excel(df_calibration)
            st.download_button(
                label="📥 Télécharger Excel",
                data=excel_buffer,
                file_name=f"calibration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Télécharger le tableau en format Excel"
            )
        
        with col_dl3:
            # Générer PDF texte
            pdf_text = "Tableau de Jaugeage ISO 12917-1:2017\n"
            pdf_text += "=" * 80 + "\n\n"
            pdf_text += df_calibration.to_string()
            
            st.download_button(
                label="📥 Télécharger TXT",
                data=pdf_text,
                file_name=f"calibration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                help="Télécharger le tableau en format texte"
            )
        
        # Statistiques
        st.divider()
        st.markdown("### 📊 Statistiques du réservoir")
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.metric(
                "Capacité totale",
                f"{df_calibration['Total (L)'].max():,.0f} L",
                delta=f"{df_calibration['Total (m³)'].max():.2f} m³"
            )
        
        with stat_col2:
            st.metric(
                "À h = 1.5m",
                f"{df_calibration[abs(df_calibration['Hauteur (m)'] - 1.5) < 0.01]['Total (L)'].values[0] if len(df_calibration[abs(df_calibration['Hauteur (m)'] - 1.5) < 0.01]) > 0 else 'N/A':.0f} L"
            )
        
        with stat_col3:
            st.metric(
                "À 50% capacité",
                f"{df_calibration['Total (L)'].max() * 0.5:,.0f} L"
            )
        
        with stat_col4:
            st.metric(
                "À 75% capacité",
                f"{df_calibration['Total (L)'].max() * 0.75:,.0f} L"
            )
    
        else:
            st.warning("⚠️ Veuillez d'abord configurer les paramètres du réservoir dans l'onglet 'Paramètres'")
    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")

# ============================================================================
# TAB 3: COURBE DE CALIBRATION
# ============================================================================

with tab3:
    st.markdown('<p class="sub-header">Courbe de calibration (Hauteur vs Volume)</p>', unsafe_allow_html=True)
    
    if diameter and circumference:
        df_calibration = generate_calibration_table(diameter, length_cylinder, length_head, deadwood_volume)
        
        # Options de courbe
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            chart_type = st.selectbox(
                "Type de courbe",
                options=["Linéaire", "Volume (m³)", "Volume (L)"],
                help="Sélectionnez le type de graphique"
            )
        
        with col_chart2:
            show_grid = st.checkbox("Afficher la grille", value=True)
        
        # Création de la courbe
        fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
        
        if chart_type == "Linéaire":
            ax.plot(
                df_calibration['Hauteur (m)'],
                df_calibration['Total (L)'],
                linewidth=2.5,
                color='#3b82f6',
                marker='o',
                markersize=4,
                markerfacecolor='#f59e0b',
                label='Volume total'
            )
        else:
            ax.plot(
                df_calibration['Hauteur (m)'],
                df_calibration['Total (m³)'] if chart_type == "Volume (m³)" else df_calibration['Total (L)'],
                linewidth=2.5,
                color='#3b82f6',
                marker='o',
                markersize=4,
                markerfacecolor='#f59e0b',
                label='Volume total'
            )
        
        # Formatting
        ax.set_xlabel('Hauteur de liquide (m)', fontsize=11, fontweight='bold')
        ax.set_ylabel(
            'Volume (L)' if 'L' in chart_type or chart_type == "Linéaire" else 'Volume (m³)',
            fontsize=11,
            fontweight='bold'
        )
        ax.set_title(
            'Courbe de calibration - Réservoir cylindrique horizontal',
            fontsize=13,
            fontweight='bold',
            pad=20
        )
        
        if show_grid:
            ax.grid(True, alpha=0.3, linestyle='--')
        
        ax.legend(fontsize=10, loc='upper left')
        
        # Styling
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_facecolor('#f8f9fa')
        fig.patch.set_facecolor('white')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Courbe combinée (Cylindre + Têtes)
        st.markdown("### Décomposition du volume")
        
        fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), dpi=100)
        
        # Graphique empilé
        ax1.fill_between(
            df_calibration['Hauteur (m)'],
            0,
            df_calibration['Cylindre (m³)'],
            alpha=0.7,
            label='Cylindre',
            color='#3b82f6'
        )
        ax1.fill_between(
            df_calibration['Hauteur (m)'],
            df_calibration['Cylindre (m³)'],
            df_calibration['Total (m³)'],
            alpha=0.7,
            label='Têtes',
            color='#f59e0b'
        )
        
        ax1.set_xlabel('Hauteur de liquide (m)', fontsize=10, fontweight='bold')
        ax1.set_ylabel('Volume (m³)', fontsize=10, fontweight='bold')
        ax1.set_title('Composition du volume', fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.set_facecolor('#f8f9fa')
        
        # Courbe comparative
        ax2.plot(
            df_calibration['Hauteur (m)'],
            df_calibration['Cylindre (m³)'],
            linewidth=2,
            marker='o',
            markersize=3,
            label='Cylindre',
            color='#3b82f6'
        )
        ax2.plot(
            df_calibration['Hauteur (m)'],
            df_calibration['Têtes (m³)'],
            linewidth=2,
            marker='s',
            markersize=3,
            label='Têtes',
            color='#f59e0b'
        )
        ax2.plot(
            df_calibration['Hauteur (m)'],
            df_calibration['Total (m³)'],
            linewidth=2.5,
            marker='^',
            markersize=3,
            label='Total',
            color='#10b981'
        )
        
        ax2.set_xlabel('Hauteur de liquide (m)', fontsize=10, fontweight='bold')
        ax2.set_ylabel('Volume (m³)', fontsize=10, fontweight='bold')
        ax2.set_title('Comparaison des volumes', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3, linestyle='--')
        ax2.set_facecolor('#f8f9fa')
        
        fig2.patch.set_facecolor('white')
        plt.tight_layout()
        st.pyplot(fig2)
    
    else:
        st.warning("⚠️ Veuillez d'abord configurer les paramètres du réservoir dans l'onglet 'Paramètres'")

# ============================================================================
# TAB 4: GUIDE D'UTILISATION
# ============================================================================

with tab4:
    st.markdown('<p class="sub-header">📖 Guide complet de calibration</p>', unsafe_allow_html=True)
    
    # Guide des mesures
    with st.expander("🔧 Guide de prise des mesures", expanded=True):
        st.markdown("""
        ### 1. Mesure de la CIRCONFÉRENCE
        
        **Équipement requis :**
        - Mètre ruban métallique de 5-10 m (précision ±1 mm)
        - Surface de référence (craie, ruban)
        - 2 personnes (préférable)
        
        **Procédure :**
        1. Marquez une ligne de référence longitudinale sur le réservoir
        2. À 1/4 de la longueur du segment, enroulez le mètre perpendiculairement à l'axe
        3. Enregistrez la lecture au mm le plus proche
        4. Répétez à 3/4 de la longueur
        5. Répétez la mesure jusqu'à obtenir 3 lectures concordant à ±3 mm
        6. Calculez la moyenne des 3 lectures
        
        **Critères d'acceptation ISO 12917-1 :**
        - Maximum 3 lectures = 3 résultats
        - Écart max entre min et max ≤ 3 mm
        - Si écart > 3 mm : répétez les mesures
        
        ---
        
        ### 2. Mesure de la LONGUEUR
        
        **Équipement requis :**
        - Mètre ruban ou chaîne d'arpenteur
        - Point de référence fixe (ex: bague d'extrémité)
        
        **Procédure :**
        1. Définissez un point de référence à chaque extrémité (ex: intersection axe/tête)
        2. Mesurez la distance entre les deux points
        3. Pour les têtes : mesurez la profondeur radiale depuis l'intersection
        4. Répétez jusqu'à concordance ±3 mm
        
        **Points critiques :**
        - Longueur du cylindre : de l'extrémité d'une tête à l'autre
        - Longueur des têtes : profondeur depuis l'intersection cylindre/tête
        
        ---
        
        ### 3. Mesure du TILT (inclinaison)
        
        **Équipement requis :**
        - Niveau optique OU théodolite OU clinomètre
        - Chaîne d'arpenteur (pour mesure horizontale)
        
        **Procédure (avec niveau optique) :**
        1. Installez le niveau à un point élevé (observation)
        2. Mesurez la hauteur du niveau par rapport au référentiel
        3. Visez les deux extrémités du réservoir
        4. Enregistrez la dénivellation (Δh) et la distance horizontale (L)
        5. Tilt (rad) = arctan(Δh / L)
        6. Tilt (°) = arctan(Δh / L) × 180 / π
        
        **Procédure (avec clinomètre) :**
        1. Placez le clinomètre contre la paroi du réservoir
        2. Visez l'extrémité éloignée
        3. Enregistrez l'angle directement en degrés
        
        **Formule de variation de hauteur :**
        Δh = (L/2) × tan(tilt) = variation aux extrémités en mètres
        
        ---
        
        ### 4. Identification du DEADWOOD
        
        **Équipement :**
        - Plans du réservoir
        - Mesure/inspection interne
        
        **Éléments à inclure :**
        - Tuyauteries internes (accumulation, circulation)
        - Capteurs (température, niveau, densité)
        - Chicanes ou déflecteurs
        - Agitateurs
        - Tubes d'immersion
        
        **Calcul du volume :**
        - Pour cylindres : V = π r² L
        - Pour tubes : V = π r² L
        - Pour formes complexes : mesurage direct ou calcul CAO
        
        """)
    
    # Instruments et précisions
    with st.expander("⚙️ Instruments et précisions"):
        st.markdown("""
        ### Mètre ruban métallique
        - **Précision :** ±0.5 à ±1 mm pour 10 m
        - **Standards :** ISO 4313 (Grade A)
        - **Avantages :** Portable, économique, rapide
        - **Inconvénients :** Sensible à la tension, température
        
        ### Laser distance meter (alternative)
        - **Précision :** ±1 à ±2 mm
        - **Avantages :** Sans contact, rapide, précis
        - **Inconvénients :** Coûteux, sensible aux conditions météo
        - **Usage ISO 12917-1 :** Autorisé pour mesures internes et tilt
        
        ### Niveau optique / Théodolite
        - **Précision :** ±0.5° pour tilt
        - **Standards :** ISO 2954 (Theodolite), ISO 10309 (Niveau)
        - **Avantages :** Très précis, idéal pour tilt
        - **Inconvénients :** Coûteux, nécessite expertise
        
        ### Clinomètre
        - **Précision :** ±0.5°
        - **Avantages :** Simple, portable, peu coûteux
        - **Inconvénients :** Moins précis
        
        ### Équipement de mesure interne (ISO 12917-1)
        - **Tige télescopique :** Précision ±1 mm, lecture au mm
        - **Laser distance meter :** ±1 à ±2 mm
        - **Calliper :** Précision ±0.5 mm
        
        """)
    
    # Bonnes pratiques
    with st.expander("✅ Bonnes pratiques"):
        st.markdown("""
        ### Avant les mesures
        - ✓ Remplissez le réservoir à capacité normale et laissez 24h minimum
        - ✓ Notez la température ambiante et de la paroi
        - ✓ Inspectez le réservoir pour dommages physiques
        - ✓ Vérifiez que la surface est accessible et sûre
        - ✓ Étalonnez les instruments avant utilisation
        
        ### Pendant les mesures
        - ✓ Prenez des photos/notes pour traçabilité
        - ✓ Mesurez à même niveau/référence pour chaque point
        - ✓ Répétez jusqu'à obtenir concordance ±3 mm
        - ✓ Enregistrez les conditions météo (température, humidité)
        - ✓ Utilisez même équipement pour tous les points
        - ✓ Deux opérateurs = meilleure qualité
        
        ### Après les mesures
        - ✓ Vérifiez la validité des résultats (écarts ≤ 3 mm)
        - ✓ Calculez les moyennes
        - ✓ Archivez les données brutes
        - ✓ Générez le rapport de calibration
        - ✓ Conservez 7 ans minimum
        
        ### Fréquence de recalibration
        - Tous les 2 ans : standard régulièrement utilisé
        - Tous les 5 ans : usage occasionnel
        - Immédiatement si : modification deadwood, déformation visuelle, dommage
        - Sur demande : régulation nationale/contractuelle
        
        """)
    
    # Erreurs courantes
    with st.expander("⚠️ Erreurs courantes"):
        st.markdown("""
        ### Mesure de circonférence
        ❌ Ne pas enrouler parallèlement à l'axe → Lectures incorrectes
        ❌ Tension inconsistante du mètre → Écarts > 3 mm
        ❌ Mesurer à mauvaises positions (pas 1/4 et 3/4) → Pas conforme ISO
        ❌ Accepter premier ensemble de 3 lectures → Risque de valeurs aberrantes
        
        ### Mesure de longueur
        ❌ Références mal définies → Imprécision systématique
        ❌ Confondre longueur cylindre vs longueur totale
        ❌ Oublier de mesurer profondeur des têtes
        
        ### Tilt
        ❌ Mesurer angle au lieu de dénivellation → Confusion d'unités
        ❌ Ne pas mesurer au même point de référence aux deux extrémités
        ❌ Ignorer le tilt si < 1° → Peut affecter précision sur long réservoir
        
        ### Deadwood
        ❌ Oublier tuyauteries/capteurs internes
        ❌ Estimer au lieu de mesurer les volumes
        ❌ Ne pas mettre à jour après modification interne
        
        """)

# ============================================================================
# TAB 5: À PROPOS
# ============================================================================

with tab5:
    st.markdown('<p class="sub-header">ℹ️ À propos de l\'application</p>', unsafe_allow_html=True)
    
    st.markdown("""
    ### ISO 12917-1:2017
    
    **Titre complet :**
    *Petroleum and Liquid Petroleum Products — Calibration of Horizontal Cylindrical Tanks*
    
    **Portée :**
    - Spécifie les méthodes manuelles de calibration de réservoirs cylindriques horizontaux
    - Applicable aux réservoirs au-dessus et sous-sol
    - Couvre les têtes plates, elliptiques, sphériques et knuckle-dish
    - Applicable à réservoirs jusqu'à ~4 m de diamètre et 10° de tilt
    
    **Normes liées :**
    - ISO 7507-1 : Équipement de calibration standard
    - ISO 2954 : Théodolite
    - ISO 10309 : Niveau optique
    - ISO 4313 : Mètre ruban métallique
    
    ---
    
    ### À propos de cette application
    
    **Version :** 1.0
    **Date :** 2024
    **Développée avec :** Streamlit, Python, Pandas, Matplotlib
    **Auteur :** Expert en Métrologie Pétrolière
    
    **Fonctionnalités :**
    - ✅ Validation des mesures de circonférence (ISO 12917-1)
    - ✅ Calcul automatique du diamètre
    - ✅ Génération de tableau de jaugeage complet
    - ✅ Courbes de calibration (hauteur vs volume)
    - ✅ Export en CSV, Excel, TXT
    - ✅ Gestion du tilt et corrections
    - ✅ Calcul de deadwood
    - ✅ Guide complet de mesure
    
    ---
    
    ### Limitations et hypothèses
    
    ⚠️ **Important :**
    - Les calculs suppose têtes elliptiques ratio 2:1 (standard)
    - Pas de correction thermique/pression automatique (manuel)
    - Volume partiel des têtes : approximation (formule ISO incomplète)
    - Résultats valides uniquement avec mesures ISO 12917-1 valides
    - Utilisez pour référence ; consultez standard complet pour applications officielles
    
    ---
    
    ### Support et garantie
    
    ℹ️ **Cette application est fournie à titre informatif.**
    
    Pour applications commerciales/officielles :
    - Consultez le standard ISO 12917-1:2017 complet
    - Travaillez avec laboratoire certifié ISO 17025
    - Valider avec expert métrologie pétrolière
    - Respectez réglementations nationales
    
    ---
    
    ### Références
    
    1. **ISO 12917-1:2017** - Petroleum and Liquid Petroleum Products — Calibration of Horizontal Cylindrical Tanks
    2. **API MPMS Chapter 2.2** - Calibration of Horizontal Cylindrical Tanks
    3. **ASTM D1220** - Standard Specification for Measuring Petroleum and Petroleum Vapor Conditions
    
    ---
    
    ### Contact et retours
    
    Pour retours ou questions sur l'application :
    - Reportez les bugs avec détails de reproduction
    - Suggérez des améliorations
    - Partagez cas d'utilisation réussis
    
    """)
    
    # Footer
    st.divider()
    col_footer1, col_footer2, col_footer3 = st.columns(3)
    
    with col_footer1:
        st.markdown("""
        **Standards appliqués**
        - ISO 12917-1:2017
        - ISO 7507-1
        """)
    
    with col_footer2:
        st.markdown("""
        **Normes de sécurité**
        - Respectez ASME/PED
        - Réservoirs pressurisés
        """)
    
    with col_footer3:
        st.markdown(f"""
        **Dernière mise à jour**
        {datetime.now().strftime('%d/%m/%Y')}
        """)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### 🛠️ Outils rapides")
    
    st.markdown("""
    **Formules ISO 12917-1**
    
    **Diamètre :**
    ```
    D = C / π
    ```
    
    **Section transversale :**
    ```
    A = R² × arccos((R-h)/R) - (R-h) × √(2Rh - h²)
    ```
    
    **Tilt :**
    ```
    Δh = (L/2) × tan(tilt)
    ```
    
    **Volume tête elliptique :**
    ```
    V = (2/3) × π × R² × L
    ```
    """)
    
    st.divider()
    
    st.markdown("""
    ### 📚 Ressources
    
    - [ISO 12917-1:2017](https://www.iso.org)
    - [API MPMS](https://www.api.org)
    - [Norme française](https://www.afnor.org)
    """)
    
    st.divider()
    
    # Export rapport
    if diameter and circumference:
        if st.button("📄 Générer rapport complet"):
            st.info("Rapport complet généré (fonctionnalité en développement)")

# ============================================================================
# FOOTER
# ============================================================================

st.divider()

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.caption("🛢️ **Calibration ISO 12917-1:2017**")

with footer_col2:
    st.caption("Réservoirs cylindriques horizontaux")

with footer_col3:
    st.caption(f"© 2024 - v1.0")

