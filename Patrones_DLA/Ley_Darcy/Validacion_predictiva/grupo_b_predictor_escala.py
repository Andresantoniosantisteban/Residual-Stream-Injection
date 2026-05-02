import json
import numpy as np
import os
from datetime import datetime
from scipy import stats

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ADN_PATH = os.path.join(BASE_DIR, '..', '..', '..', 'ADN_TOTAL_IDENTIDADES.json')

def grupo_b_predictor_barrido_ejecutar():
    """
    BARRIDO DE ESCALA (Damping Sweep)
    Autor: Andrés Antonio Santisteban Lino
    
    Este script realiza un barrido de factores de amortiguamiento (10% a 20%)
    para encontrar el valor exacto que minimiza el error de escala (MAE)
    manteniendo la forma (Pearson).
    """
    
    print(f"[{datetime.now()}] Iniciando Barrido de Escala (10% - 20%)...")
    
    if not os.path.exists(ADN_PATH):
        print(f"Error: No se encuentra ADN_TOTAL_IDENTIDADES.json")
        return

    with open(ADN_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. CÁLCULO DE TOPOGRAFÍA MEDIA
    perfiles_todos = []
    for sub_data in data.values():
        h_sub = np.zeros(24)
        for t in sub_data['analisis_tokens']:
            for n in t['mapa_completo']: h_sub[n['c']] += abs(n['im'])
        perfiles_todos.append(h_sub)
    
    topografia_media = np.mean(perfiles_todos, axis=0)
    topografia_norm = topografia_media / topografia_media.mean()

    # 2. RANGO DE BARRIDO DE PRECISIÓN (Refinado)
    # Rango: 0.90 a 0.98 para encontrar el pico de MAE mínimo
    factores_prueba = np.linspace(0.90, 0.98, 9) 

    
    mejor_factor = 0
    menor_error_global = float('inf')
    resultados_barrido = []

    for f_amort in factores_prueba:
        errores_f = []
        
        for pregunta, contenido in data.items():
            tokens_data = contenido['analisis_tokens']
            for t_info in tokens_data:
                mapa = t_info['mapa_completo']
                h_real = np.zeros(24)
                for n in mapa: h_real[n['c']] += abs(n['im'])
                
                # Calibración
                h_calibracion = h_real[:7]
                slope_ini, _, _, _, _ = stats.linregress(np.arange(7), h_calibracion)
                mu_ini = 1.0 / (np.std(h_calibracion) / np.mean(h_calibracion) + 1e-9)
                
                # Predicción con Amortiguamiento
                h_prediccion = list(h_calibracion)
                for i in range(7, 24):
                    factor_inercia = slope_ini * (mu_ini / 4.0)
                    resistencia_suelo = topografia_norm[i]
                    
                    # Aplicamos el Amortiguamiento (f_amort)
                    proximo_h = (h_prediccion[-1] + factor_inercia) * (resistencia_suelo / topografia_norm[i-1]) * f_amort
                    h_prediccion.append(max(0, proximo_h))
                
                # Calculamos Error Absoluto Medio (Escala)
                error_escala = np.mean(np.abs(h_real[7:] - np.array(h_prediccion[7:])))
                errores_f.append(error_escala)
        
        error_medio_f = np.mean(errores_f)
        resultados_barrido.append({"factor": float(f_amort), "error_mae": float(error_medio_f)})
        
        if error_medio_f < menor_error_global:
            menor_error_global = error_medio_f
            mejor_factor = f_amort

    # 3. GUARDAR RESULTADOS
    output_filename = f"{datetime.now().strftime('%Y%m%d_%H%M')}_darcy_barrido_escala.json"
    with open(os.path.join(BASE_DIR, output_filename), 'w', encoding='utf-8') as f:
        json.dump({
            "mejor_factor_encontrado": float(mejor_factor),
            "porcentaje_decaimiento": float((1 - mejor_factor) * 100),
            "menor_error_mae": float(menor_error_global),
            "detalle_barrido": resultados_barrido
        }, f, indent=4)

    print(f"[{datetime.now()}] Barrido finalizado.")
    print(f"Mejor Factor: {mejor_factor:.2f} (Decaimiento: {(1-mejor_factor)*100:.1f}%)")
    print(f"Resultados en: {output_filename}")

if __name__ == "__main__":
    grupo_b_predictor_barrido_ejecutar()
