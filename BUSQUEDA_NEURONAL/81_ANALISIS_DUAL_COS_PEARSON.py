import os
import json
import numpy as np
from scipy.stats import pearsonr

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DICCIONARIO_PATH = os.path.join(BASE_DIR, "PIEDRA_ROSETA", "EXPERIMENTOS", "BUSQUEDA_NEURONAL", "DICCIONARIO_MULTILINGUE_BASE.json")

def cos_sim(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def analizar_dual():
    print(f"--- EXPERIMENTO 81: ANÁLISIS DUAL (COSENO VS PEARSON) ---")
    
    with open(DICCIONARIO_PATH, "r") as f: diccionario = json.load(f)

    print(f"{'Dígito':<8} | {'Coseno ES-EN':<12} | {'Pearson ES-EN':<12} | {'Diferencia':<10}")
    print("-" * 55)

    reporte_dual = {}

    for i in range(10):
        d = str(i)
        v_es = np.array(diccionario["ES"][d])
        v_en = np.array(diccionario["EN"][d])

        c = cos_sim(v_es, v_en)
        p, _ = pearsonr(v_es, v_en)

        diff = abs(c - p)
        
        print(f"{d:<8} | {c*100:9.2f}% | {p*100:9.2f}% | {diff*100:8.2f}%")

        reporte_dual[d] = {
            "coseno_pct": float(c * 100),
            "pearson_pct": float(p * 100),
            "diferencia_pct": float(diff * 100)
        }

    out_path = os.path.join(BASE_DIR, "PIEDRA_ROSETA", "EXPERIMENTOS", "BUSQUEDA_NEURONAL", "REPORTE_COMPARATIVA_COS_PEARSON.json")
    with open(out_path, "w") as f:
        json.dump(reporte_dual, f, indent=4)
    print(f"\nReporte Dual guardado en: {out_path}")

if __name__ == "__main__":
    analizar_dual()
