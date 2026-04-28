import os
import json
import numpy as np

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DICCIONARIO_PATH = os.path.join(BASE_DIR, "PIEDRA_ROSETA", "EXPERIMENTOS", "BUSQUEDA_NEURONAL", "DICCIONARIO_MULTILINGUE_BASE.json")

def cos_sim(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def analizar_similitudes():
    print(f"--- EXPERIMENTO 80: ANÁLISIS DE SIMILITUD INTER-IDIOMÁTICA ---")
    
    with open(DICCIONARIO_PATH, "r") as f: diccionario = json.load(f)

    reporte = {}

    print(f"{'Dígito':<8} | {'ES <-> EN':<12} | {'EN <-> ZH':<12} | {'ES <-> ZH':<12}")
    print("-" * 55)

    for i in range(10):
        d = str(i)
        v_es = diccionario["ES"][d]
        v_en = diccionario["EN"][d]
        v_zh = diccionario["ZH"][d]

        sim_es_en = cos_sim(v_es, v_en)
        sim_en_zh = cos_sim(v_en, v_zh)
        sim_es_zh = cos_sim(v_es, v_zh)

        print(f"{d:<8} | {sim_es_en:10.6f} | {sim_en_zh:10.6f} | {sim_es_zh:10.6f}")

        reporte[d] = {
            "es_en": float(sim_es_en),
            "en_zh": float(sim_en_zh),
            "es_zh": float(sim_es_zh),
            "promedio": float((sim_es_en + sim_en_zh + sim_es_zh) / 3)
        }

    out_path = os.path.join(BASE_DIR, "PIEDRA_ROSETA", "EXPERIMENTOS", "BUSQUEDA_NEURONAL", "REPORTE_SIMILITUD_VECTORES.json")
    with open(out_path, "w") as f:
        json.dump(reporte, f, indent=4)
    print(f"\nReporte de Similitud guardado en: {out_path}")

if __name__ == "__main__":
    analizar_similitudes()
