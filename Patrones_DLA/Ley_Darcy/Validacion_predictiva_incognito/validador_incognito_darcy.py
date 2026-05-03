import json
import numpy as np
import os
from scipy.stats import pearsonr, spearmanr

BASE_DIR = r'c:\Users\andre\Desktop\Neural_Identity_Forge\Entendiendo\Estudio_Patrones\DLA_data_sedimentaria\Patrones_DLA\Ley_Darcy\Validacion_predictiva_incognito'
TEORICO_PATH = os.path.join(BASE_DIR, '20260502_1920_DARCY_PREDICCION_TEORICA_15.json')
RAW_DIR = r'c:\Users\andre\Desktop\Neural_Identity_Forge\Entendiendo\Estudio_Patrones\DLA_data_sedimentaria\ADN_RAW\que_es'
OUTPUT_RESULTADOS = os.path.join(BASE_DIR, '20260502_1925_RESULTADOS_VALIDACION_INCOGNITO.json')

def ejecutar_validacion_incognito():
    print("--- INICIANDO VALIDACIÓN CRUZADA: REALIDAD VS MULTIVERSO TEÓRICO ---")
    
    with open(TEORICO_PATH, 'r', encoding='utf-8') as f:
        multiverso = json.load(f)
    
    resultados_finales = {
        "timestamp": "2026-05-02 19:25:00",
        "autor": "Andrés Antonio Santisteban Lino",
        "veredicto_global": "",
        "sujetos": {}
    }

    exitos = 0
    # Preparar CSV de Auditoría
    csv_lines = ["Concepto,Escenario_Alto_Pearson,Escenario_Medio_Pearson,Escenario_Bajo_Pearson,Ganador,Precision_Pico"]

    for sujeto, escenarios in multiverso['escenarios'].items():
        # ... (lógica anterior de carga y procesamiento se mantiene igual)
        raw_path = os.path.join(RAW_DIR, f"ADN_RAW_{sujeto.upper()}.json")
        if not os.path.exists(raw_path): continue
        with open(raw_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        h_real = np.zeros(24)
        num_t = len(raw_data['flujo_total'])
        for t_info in raw_data['flujo_total']:
            for capa_info in t_info['capas']:
                h_real[capa_info['capa']] += sum([abs(n['im']) for n in capa_info['flujo']])
        h_real /= num_t

        # 2. Comparar con los 3 Escenarios
        comparativas = {}
        mejor_escenario = ""
        mejor_pearson = -1
        
        for nivel, data_teorica in escenarios.items():
            h_teorica = np.array(data_teorica['curva_teorica'])
            p_corr, _ = pearsonr(h_real[7:], h_teorica[7:])
            s_corr, _ = spearmanr(h_real[7:], h_teorica[7:])
            
            comparativas[nivel] = {
                "pearson_fidelidad": float(p_corr * 100),
                "spearman_fidelidad": float(s_corr * 100),
                "curva_teorica": data_teorica['curva_teorica']
            }
            
            if p_corr > mejor_pearson:
                mejor_pearson = p_corr
                mejor_escenario = nivel
        
        # 3. Veredicto y Yuxtaposición de Auditoría
        resultados_finales["sujetos"][sujeto] = {
            "veredicto": "EXITO" if (mejor_escenario == "MEDIO" and mejor_pearson > 0.95) else "FALLO EN INTENSIDAD",
            "escenario_ganador": mejor_escenario,
            "precision_pico": float(mejor_pearson * 100),
            "AUDITORIA_CURVAS": {
                "teorica_ganadora": comparativas[mejor_escenario]['curva_teorica'],
                "real_empirica": h_real.tolist()
            },
            "DETALLE_MULTIVERSO": comparativas
        }

        # Añadir al CSV
        csv_lines.append(f"{sujeto},{comparativas.get('ALTO',{}).get('pearson_fidelidad',0):.2f},{comparativas.get('MEDIO',{}).get('pearson_fidelidad',0):.2f},{comparativas.get('BAJO',{}).get('pearson_fidelidad',0):.2f},{mejor_escenario},{mejor_pearson*100:.2f}")

    csv_path = OUTPUT_RESULTADOS.replace(".json", ".csv")
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(csv_lines))
        
    with open(OUTPUT_RESULTADOS, 'w', encoding='utf-8') as f:
        json.dump(resultados_finales, f, indent=4)
        
    print(f"Validación finalizada. CSV guardado en: {csv_path}")

if __name__ == "__main__":
    ejecutar_validacion_incognito()
