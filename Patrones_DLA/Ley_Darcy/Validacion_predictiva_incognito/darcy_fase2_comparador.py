import json
import numpy as np
import os
from scipy.stats import pearsonr, spearmanr

# ... (rutas se mantienen igual)
BASE_DIR = r'c:\Users\andre\Desktop\Neural_Identity_Forge\Entendiendo\Estudio_Patrones\DLA_data_sedimentaria\Patrones_DLA\Ley_Darcy\Validacion_predictiva_incognito'
PREDICCION_PATH = os.path.join(BASE_DIR, '20260502_1920_DARCY_PREDICCION_TEORICA_15.json')
REALIDAD_PATH = os.path.join(BASE_DIR, '20260502_1935_REALIDAD_CRUDA.json')
OUTPUT_FINAL = os.path.join(BASE_DIR, '20260502_1940_VEREDICTO_FINAL_INCOGNITO.json')

def ejecutar_fase2_comparacion():
    print("--- FASE 2: COMPARACIÓN MATEMÁTICA (PEARSON + SPEARMAN) ---")
    
    with open(PREDICCION_PATH, 'r', encoding='utf-8') as f:
        teoria = json.load(f)
    with open(REALIDAD_PATH, 'r', encoding='utf-8') as f:
        realidad = json.load(f)
        
    informe = {
        "timestamp": "2026-05-02 19:40:00",
        "autor": "Andrés Antonio Santisteban Lino",
        "objetivo": "Validación Ciega de la Ley de Darcy",
        "auditoria_por_sujeto": {}
    }

    for sujeto, datos_reales in realidad['datos_empiricos'].items():
        h_real = np.array(datos_reales['perfil_presion_real'])
        escenarios_teoricos = teoria['escenarios'].get(sujeto, {})
        
        comparativa_sujeto = {
            "realidad_empirica": h_real.tolist(),
            "multiverso_teorico": {}
        }
        
        mejor_escenario = ""
        mejor_pearson = -1
        
        for nivel, data_teorica in escenarios_teoricos.items():
            h_teorica = np.array(data_teorica['curva_teorica'])
            
            p_corr, _ = pearsonr(h_real[7:], h_teorica[7:])
            s_corr, _ = spearmanr(h_real[7:], h_teorica[7:])
            
            comparativa_sujeto["multiverso_teorico"][nivel] = {
                "fidelidad_pearson": float(p_corr * 100),
                "fidelidad_spearman": float(s_corr * 100),
                "curva_teorica": data_teorica['curva_teorica']
            }
            
            if p_corr > mejor_pearson:
                mejor_pearson = p_corr
                mejor_escenario = nivel
        
        comparativa_sujeto["veredicto"] = {
            "escenario_ganador": mejor_escenario,
            "precision_pico": float(mejor_pearson * 100),
            "estatus": "ÉXITO" if (mejor_escenario == "MEDIO" and mejor_pearson > 0.95) else "INTENSIDAD_ALTA"
        }
        
        informe["auditoria_por_sujeto"][sujeto] = comparativa_sujeto
        print(f"Juicio completado para: {sujeto} -> Ganador: {mejor_escenario} ({mejor_pearson*100:.2f}%)")

    with open(OUTPUT_FINAL, 'w', encoding='utf-8') as f:
        json.dump(informe, f, indent=4)
    
    print(f"\nFase 2 completada. Veredicto Final en: {OUTPUT_FINAL}")

if __name__ == "__main__":
    ejecutar_fase2_comparacion()
