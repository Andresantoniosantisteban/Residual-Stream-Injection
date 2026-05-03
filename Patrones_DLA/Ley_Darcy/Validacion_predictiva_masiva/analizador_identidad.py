import json
import numpy as np
import os
import glob
from datetime import datetime
from scipy.stats import pearsonr, spearmanr

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUE_ES_DIR = r'c:\Users\andre\Desktop\Neural_Identity_Forge\Entendiendo\Estudio_Patrones\DLA_data_sedimentaria\ADN_RAW\que_es'

def obtener_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M")

def analizador_identidad_ejecutar():
    """
    ANALIZADOR DE IDENTIDAD: El Concepto
    Compara el token del sujeto entre todos los búnkeres para ver la divergencia semántica.
    """
    print(f"[{datetime.now()}] Iniciando Análisis de Identidad Pura...")
    
    archivos = glob.glob(os.path.join(QUE_ES_DIR, "ADN_RAW_*.json"))
    if not archivos:
        print("Error: No hay archivos en que_es")
        return

    # Usaremos GATO como patrón de referencia (Concepto Real)
    ref_path = os.path.join(QUE_ES_DIR, "ADN_RAW_GATO.json")
    with open(ref_path, 'r', encoding='utf-8') as f:
        ref_data = json.load(f)
    
    # Extraer H y Densidad de la Identidad de GATO (Tokens 4 en adelante)
    h_ref = np.zeros(24)
    d_ref = np.zeros(24)
    start_token = 4
    
    tokens_identidad = ref_data['flujo_total'][start_token:]
    num_t = len(tokens_identidad) if len(tokens_identidad) > 0 else 1
    
    for t_info in tokens_identidad:
        for capa_info in t_info['capas']:
            capa = capa_info['capa']
            impacto = sum([abs(n['im']) for n in capa_info['flujo']])
            h_ref[capa] += impacto
            d_ref[capa] += len(capa_info['flujo'])

    h_ref /= num_t
    d_ref = (d_ref / num_t) / 4864 * 100

    output_filename = f"{obtener_timestamp()}_analizador_identidad_resultados.json"
    output_path = os.path.join(BASE_DIR, output_filename)

    resultados = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "autor": "Andrés Antonio Santisteban Lino",
        "metodo": "Comparativa de Identidad (Sujeto) - Tokens 4-Fin",
        "sujetos_analizados": {}
    }

    for file_path in archivos:
        sujeto = os.path.basename(file_path).replace("ADN_RAW_", "").replace(".json", "")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        h_actual = np.zeros(24)
        d_actual = np.zeros(24)
        
        tokens_act = data['flujo_total'][start_token:]
        num_act = len(tokens_act) if len(tokens_act) > 0 else 1
        
        for t_info in tokens_act:
            for capa_info in t_info['capas']:
                capa = capa_info['capa']
                impacto = sum([abs(n['im']) for n in capa_info['flujo']])
                h_actual[capa] += impacto
                d_actual[capa] += len(capa_info['flujo'])

        h_actual /= num_act
        d_actual = (d_actual / num_act) / 4864 * 100

        # Correlaciones
        p_corr, _ = pearsonr(h_ref, h_actual)
        s_corr, _ = spearmanr(h_ref, h_actual)

        resultados["sujetos_analizados"][sujeto] = {
            "correlacion_pearson": float(p_corr * 100),
            "correlacion_spearman": float(s_corr * 100),
            "camino_densidad": d_actual.tolist(),
            "curva_referencia_gato": h_ref.tolist(),
            "curva_actual": h_actual.tolist()
        }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=4)
    
    print(f"Análisis finalizado: {output_filename}")

if __name__ == "__main__":
    analizador_identidad_ejecutar()
