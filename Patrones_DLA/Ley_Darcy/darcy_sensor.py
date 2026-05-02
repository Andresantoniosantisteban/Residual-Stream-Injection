import json
import numpy as np
import os
from datetime import datetime
from scipy import stats

# --- CONFIGURACIÓN DE RUTAS ---
# El script se ejecuta desde su propia carpeta Ley_Darcy
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# El ADN Total está dos niveles arriba
ADN_PATH = os.path.join(BASE_DIR, '..', '..', 'ADN_TOTAL_IDENTIDADES.json')

def obtener_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M")

def darcy_sensor_ejecutar():
    """
    SENSOR HIDRODINÁMICO: LEY DE DARCY (Fase 5.1)
    
    Este sensor extrae las constantes físicas del flujo semántico:
    1. Carga Hidráulica (h): Intensidad neta por capa.
    2. Conductividad (K): Capacidad de paso del medio poroso (pesos).
    3. Viscosidad (mu): Resistencia interna de la identidad al cambio.
    """
    
    print(f"[{datetime.now()}] Iniciando Sensor Hidrodinámico de Darcy...")
    
    if not os.path.exists(ADN_PATH):
        print(f"Error: No se encuentra el ADN_TOTAL_IDENTIDADES.json en {ADN_PATH}")
        return

    with open(ADN_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # El archivo de resultados llevará el prefijo de timestamp según la regla 0
    timestamp_prefix = obtener_timestamp()
    output_filename = f"{timestamp_prefix}_darcy_resultados.json"
    output_path = os.path.join(BASE_DIR, output_filename)

    resultados_prueba = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hipotesis": "Ley de Darcy: El flujo latente obedece a la resistencia física del medio poroso.",
        "metodología": "Análisis de gradiente de presión y conductividad inter-capa",
        "sujetos_analizados": {}
    }

    for pregunta, contenido in data.items():
        sujeto = contenido['sujeto']
        tokens_data = contenido['analisis_tokens']
        
        for t_info in tokens_data:
            token_str = t_info['token']
            mapa = t_info['mapa_completo']
            
            # Organizamos impactos por capa (24 capas)
            # h_capa: Carga Hidráulica (suma de impactos absolutos)
            # a_capa: Área (conteo de neuronas activas)
            h_capa = np.zeros(24)
            a_capa = np.zeros(24)
            
            for n in mapa:
                capa = n['c']
                impacto = abs(n['im'])
                h_capa[capa] += impacto
                a_capa[capa] += 1
            
            # --- CÁLCULO DE VARIABLES DARCY ---
            
            # 1. Gradiente Hidráulico (dh/dl)
            # Diferencia de carga entre capas consecutivas
            gradientes = np.diff(h_capa) # dh (dl es 1 entre capas)
            
            # 2. Conductividad Hidráulica (K)
            # Estimación: A mayor área activa en una población finita, 
            # menor es la conductividad (suelo saturado/compactado).
            # K = 1 - (Área Activa / Población Total de la Capa)
            # Población total por capa en Qwen2.5-0.5B: 116736 / 24 = 4864
            POBLACION_CAPA = 4864
            conductividades = [1.0 - (a / POBLACION_CAPA) for a in a_capa]
            
            # 3. Viscosidad Semántica (mu)
            # Medida por el coeficiente de variación (CV) de la carga.
            # Una viscosidad alta (Miel) mantiene la carga estable (bajo CV).
            # Una viscosidad baja (Agua) permite fluctuaciones rápidas (alto CV).
            cv_carga = np.std(h_capa) / np.mean(h_capa) if np.mean(h_capa) > 0 else 0
            viscosidad = 1.0 / (cv_carga + 1e-9) # Inversa de la volatilidad
            
            id_key = f"{sujeto}_{token_str}"
            resultados_prueba["sujetos_analizados"][id_key] = {
                "perfil_carga_h": h_capa.tolist(),
                "gradientes_dh": gradientes.tolist(),
                "conductividad_media_k": float(np.mean(conductividades)),
                "viscosidad_semantica_mu": float(viscosidad),
                "capa_max_presion": int(np.argmax(h_capa))
            }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(resultados_prueba, f, indent=4)
        
    print(f"[{datetime.now()}] Experimento finalizado. Resultados en: {output_filename}")

if __name__ == "__main__":
    darcy_sensor_ejecutar()
