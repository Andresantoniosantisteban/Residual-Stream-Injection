import json
import numpy as np
import os
import glob
from datetime import datetime

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Directorio de los 30 búnkeres atómicos (Inferencia)
QUE_ES_DIR = r'c:\Users\andre\Desktop\Neural_Identity_Forge\Entendiendo\Estudio_Patrones\DLA_data_sedimentaria\ADN_RAW\que_es'

def obtener_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M")

def darcy_sensor_masivo_ejecutar():
    """
    SENSOR HIDRODINÁMICO MASIVO: LEY DE DARCY (Fase 7.1)
    Validación Predictiva sobre data RAW atómica.
    """
    
    print(f"[{datetime.now()}] Iniciando Validación Masiva de Darcy...")
    
    archivos = glob.glob(os.path.join(QUE_ES_DIR, "ADN_RAW_*.json"))
    if not archivos:
        print(f"Error: No se encontraron búnkeres en {QUE_ES_DIR}")
        return

    timestamp_prefix = obtener_timestamp()
    output_filename = f"{timestamp_prefix}_darcy_validacion_masiva.json"
    output_path = os.path.join(BASE_DIR, output_filename)

    resultados_validacion = {
        "metadata": {
            "autor": "Andrés Antonio Santisteban Lino",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fase": "7.1 - Validación Predictiva Masiva",
            "archivos_analizados": len(archivos)
        },
        "analisis_por_sujeto": {}
    }

    for i_f, file_path in enumerate(archivos, 1):
        sujeto_raw = os.path.basename(file_path).replace("ADN_RAW_", "").replace(".json", "")
        print(f"  [{i_f}/{len(archivos)}] Procesando {sujeto_raw}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Variables de Darcy para el sujeto (acumulado de todos los tokens)
        h_total = np.zeros(24)
        a_total = np.zeros(24)
        
        # Iteramos por cada token del búnker
        for t_info in data['flujo_total']:
            for capa_info in t_info['capas']:
                capa = capa_info['capa']
                for n in capa_info['flujo']:
                    impacto = abs(n['im'])
                    h_total[capa] += impacto
                    a_total[capa] += 1
        
        # --- CÁLCULO DE VARIABLES DARCY (Promediado por Token) ---
        num_tokens = len(data['flujo_total'])
        h_medio = h_total / num_tokens
        a_medio = a_total / num_tokens
        
        # 1. Gradiente Hidráulico (dh/dl)
        gradientes = np.diff(h_medio)
        
        # 2. Conductividad Hidráulica (K)
        POBLACION_CAPA = 4864
        conductividades = [1.0 - (a / POBLACION_CAPA) for a in a_medio]
        
        # 3. Viscosidad Semántica (mu)
        cv_carga = np.std(h_medio) / np.mean(h_medio) if np.mean(h_medio) > 0 else 0
        viscosidad = 1.0 / (cv_carga + 1e-9)
        
        resultados_validacion["analisis_por_sujeto"][sujeto_raw] = {
            "conductividad_k": round(float(np.mean(conductividades)), 6),
            "viscosidad_mu": round(float(viscosidad), 6),
            "capa_max_presion": int(np.argmax(h_medio)),
            "perfil_carga_h": h_medio.tolist()
        }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(resultados_validacion, f, indent=4)
        
    print(f"[{datetime.now()}] Validación Masiva finalizada. Resultados en: {output_filename}")

if __name__ == "__main__":
    darcy_sensor_masivo_ejecutar()
