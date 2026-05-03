import json
import os
import numpy as np
from datetime import datetime

# --- CONFIGURACIÓN ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ADN_PATH = os.path.join(BASE_DIR, '..', '..', 'ADN_TOTAL_IDENTIDADES.json')


def identificar_rios_madre():
    """
    ANÁLISIS DE CAUCES MAESTROS (Ríos Madre)
    Identifica las neuronas con persistencia universal (>90% de los sujetos).
    """
    print(f"[{datetime.now()}] Iniciando escaneo de Cauces Maestros...")
    
    if not os.path.exists(ADN_PATH):
        print(f"Error: No se encuentra ADN_TOTAL_IDENTIDADES.json")
        return

    with open(ADN_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    num_sujetos = len(data)
    threshold_universal = int(num_sujetos * 0.9) # Neuronas que aparecen en 27 de 30 sujetos
    
    # Estructura: cauces[capa][neurona_id] = frecuencia
    cauces = {layer: {} for layer in range(24)}
    
    # 1. Conteo de Frecuencia Espacial con Filtro de Intensidad (Presión)
    # Solo contamos la neurona si su impacto (im) está por encima del percentil 80 (el flujo fuerte)
    for sub_data in data.values():
        for t_info in sub_data['analisis_tokens']:
            # Calculamos umbral de intensidad para este token
            impactos = [abs(n['im']) for n in t_info['mapa_completo']]
            umbral_vuelo = np.percentile(impactos, 90) # Solo el Top 10% de presión
            
            for n in t_info['mapa_completo']:
                if abs(n['im']) >= umbral_vuelo:
                    c = n['c']
                    idx = n['i']
                    cauces[c][idx] = cauces[c].get(idx, 0) + 1


    # 2. Filtrado de Ríos Madre (Inmortales)
    rios_madre = {layer: [] for layer in range(24)}
    estadisticas = {layer: {"total_activas": len(cauces[layer]), "inmortales": 0} for layer in range(24)}

    for layer in range(24):
        for idx, freq in cauces[layer].items():
            if freq >= threshold_universal:
                rios_madre[layer].append(idx)
                estadisticas[layer]["inmortales"] += 1

    # 3. Exportación de Resultados
    output_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "autor": "Andrés Antonio Santisteban Lino",
        "metodología": "Filtro de Persistencia Universal (>90%)",
        "sujetos_analizados": num_sujetos,
        "estadisticas_por_capa": estadisticas,
        "mapa_rios_madre": rios_madre
    }

    output_file = os.path.join(BASE_DIR, "20260502_1343_mapa_cauces_maestros.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4)
    
    print(f"[{datetime.now()}] Mapa de Cauces Maestros generado.")
    print(f"Archivo: {os.path.basename(output_file)}")

if __name__ == "__main__":
    identificar_rios_madre()
