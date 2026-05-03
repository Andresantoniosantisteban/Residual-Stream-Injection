import json
import os
import glob
import numpy as np
from datetime import datetime

# --- CONFIGURACIÓN DE CUENCA TOTAL ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = r'c:\Users\andre\Desktop\Neural_Identity_Forge\Entendiendo\Estudio_Patrones\DLA_data_sedimentaria\ADN_RAW'
OUTPUT_FILE = os.path.join(BASE_DIR, "20260502_1805_MAPA_CUENCA_TOTAL.json")

def obtener_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def analizar_cuenca_total():
    """
    Analiza la presión media de TODAS las neuronas (16,384 x 24)
    a través de los 30 sujetos RAW para mapear la geografía completa.
    """
    print(f"[{obtener_timestamp()}] Iniciando Mapeo de Cuenca Total (Sin Filtros)...")
    
    archivos = glob.glob(os.path.join(RAW_DIR, "ADN_RAW_*.json"))
    num_sujetos = len(archivos)
    
    # Estructura: matriz[capa][neurona_id] = [suma_im, frecuencia_aparicion]
    # Usamos diccionarios para flexibilidad, pero procesaremos los 16k
    cuenca = {layer: {} for layer in range(24)}

    for i_f, file_path in enumerate(archivos, 1):
        sujeto_name = os.path.basename(file_path).replace("ADN_RAW_", "").replace(".json", "")
        print(f"  [{i_f}/{num_sujetos}] Absorbiendo flujo de {sujeto_name}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for t_info in data['flujo_total']:
            for capa_info in t_info['capas']:
                capa = capa_info['capa']
                for n in capa_info['flujo']:
                    idx = n['i']
                    if idx not in cuenca[capa]:
                        cuenca[capa][idx] = [0.0, 0]
                    
                    cuenca[capa][idx][0] += abs(n['im'])
                    cuenca[capa][idx][1] += 1

    # Procesamiento final para exportar el mapa térmico
    mapa_termico = {layer: [] for layer in range(24)}
    
    print(f"[{obtener_timestamp()}] Consolidando relieve fluvial...")
    for layer in range(24):
        # Ordenamos por ID para mantener la geografía espacial
        ids_ordenados = sorted(cuenca[layer].keys())
        for idx in ids_ordenados:
            suma_im, freq = cuenca[layer][idx]
            mapa_termico[layer].append({
                "i": idx,
                "p": round(suma_im / freq, 6) if freq > 0 else 0, # Presión media
                "f": freq # Persistencia (frecuencia)
            })

    # Metadata de la Cuenca
    resultado = {
        "metadata": {
            "autor": "Andrés Antonio Santisteban Lino",
            "descripcion": "Mapa Geográfico de Presión Total (Sin Filtros)",
            "dimension": "16384 x 24",
            "sujetos": num_sujetos,
            "timestamp": obtener_timestamp()
        },
        "cuenca": mapa_termico
    }

    print(f"[{obtener_timestamp()}] Escribiendo mapa de 400k puntos...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=None) # Sin indentación para ahorrar espacio (archivo grande)

    print(f"[{obtener_timestamp()}] Mapa de Cuenca Total finalizado: {os.path.basename(OUTPUT_FILE)}")

if __name__ == "__main__":
    analizar_cuenca_total()
