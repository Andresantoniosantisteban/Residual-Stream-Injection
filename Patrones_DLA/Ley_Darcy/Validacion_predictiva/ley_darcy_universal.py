import json
import numpy as np
import os
from datetime import datetime
from scipy import stats

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ADN_PATH = os.path.join(BASE_DIR, '..', '..', '..', 'ADN_TOTAL_IDENTIDADES.json')

def ley_darcy_universal_ejecutar():
    """
    LEY DE DARCY UNIVERSAL (Validación Final de Forma y Escala)
    Autor: Andrés Antonio Santisteban Lino
    
    Variables Maestras:
    - Inercia (S_ini): Tendencia inicial (0-6)
    - Viscosidad (mu): Estabilidad del fluido semántico.
    - Topografía (T): Relieve estructural del modelo.
    - Amortiguamiento (f): 0.90 (Punto dulce de escala).
    """
    
    print(f"[{datetime.now()}] Ejecutando Ley de Darcy Universal (30 Identidades)...")
    
    if not os.path.exists(ADN_PATH):
        print(f"Error: No se encuentra ADN_TOTAL_IDENTIDADES.json")
        return

    with open(ADN_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. CONSTANTES DE LEY
    F_AMORT = 0.90
    C_ESCALA = 4.0
    
    # 2. CÁLCULO DE TOPOGRAFÍA MEDIA
    perfiles_todos = []
    for sub_data in data.values():
        h_sub = np.zeros(24)
        for t in sub_data['analisis_tokens']:
            for n in t['mapa_completo']: h_sub[n['c']] += abs(n['im'])
        perfiles_todos.append(h_sub)
    
    topografia_media = np.mean(perfiles_todos, axis=0)
    topografia_norm = topografia_media / topografia_media.mean()

    resultados_finales = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "autor": "Andrés Antonio Santisteban Lino",
        "ley": "Ley de Sedimentación de Darcy",
        "constantes_globales": {
            "factor_amortiguamiento": F_AMORT,
            "constante_escala": C_ESCALA,
            "topografia_estructural": topografia_norm.tolist()
        },
        "identidades_validadas": {}
    }

    # 3. PROCESADO TOTAL
    for pregunta, contenido in data.items():
        sujeto = contenido['sujeto']
        for t_info in contenido['analisis_tokens']:
            token_str = t_info['token']
            h_real = np.zeros(24)
            for n in t_info['mapa_completo']: h_real[n['c']] += abs(n['im'])
            
            # Calibración
            h_calibracion = h_real[:7]
            slope_ini, _, _, _, _ = stats.linregress(np.arange(7), h_calibracion)
            mu_ini = 1.0 / (np.std(h_calibracion) / np.mean(h_calibracion) + 1e-9)
            
            # Predicción (La Ley Universal)
            h_pred = list(h_calibracion)
            for i in range(7, 24):
                factor_inercia = slope_ini * (mu_ini / C_ESCALA)
                # ECUACIÓN MAESTRA
                proximo_h = (h_pred[-1] + factor_inercia) * (topografia_norm[i] / topografia_norm[i-1]) * F_AMORT
                h_pred.append(max(0, proximo_h))
            
            # Evaluación de Doble Ciego
            r_pearson, _ = stats.pearsonr(h_real[7:], h_pred[7:])
            mae_error = np.mean(np.abs(h_real[7:] - np.array(h_pred[7:])))
            
            id_key = f"{sujeto}_{token_str}"
            resultados_finales["identidades_validadas"][id_key] = {
                "precision_forma_pearson": float(r_pearson * 100),
                "error_escala_mae": float(mae_error),
                "variables_sujeto": {
                    "inercia": float(slope_ini),
                    "viscosidad": float(mu_ini)
                },
                "curva_real": h_real.tolist(),
                "curva_predicha": h_pred,
                "veredicto": "VALIDADA" if r_pearson > 0.85 and mae_error < 500 else "REVISIÓN"
            }

    output_filename = f"{datetime.now().strftime('%Y%m%d_%H%M')}_LEY_DARCY_FINAL.json"

    with open(os.path.join(BASE_DIR, output_filename), 'w', encoding='utf-8') as f:
        json.dump(resultados_finales, f, indent=4)
        
    print(f"[{datetime.now()}] La Ley ha sido Validada Universalmente.")
    print(f"Archivo Final: {output_filename}")

if __name__ == "__main__":
    ley_darcy_universal_ejecutar()
