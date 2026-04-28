import os
import json
import numpy as np

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ALFABETO_PATH = os.path.join(BASE_DIR, "PIEDRA_ROSETA", "EXPERIMENTOS", "BUSQUEDA_NEURONAL", "ALFABETO_MULTILINGUE_BASE.json")

def cos_sim(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def analizar_soberania_eñe():
    print(f"--- EXPERIMENTO 83: ANÁLISIS DE SOBERANÍA DE LA 'Ñ' ---")
    
    with open(ALFABETO_PATH, "r") as f: alfabeto = json.load(f)

    # 1. COMPARAR Ñ ENTRE IDIOMAS
    v_ñ_es = alfabeto["ES"]["ñ"]
    v_ñ_en = alfabeto["EN"]["ñ"]
    v_ñ_zh = alfabeto["ZH"]["ñ"]

    sim_ñ_es_en = cos_sim(v_ñ_es, v_ñ_en)
    sim_ñ_es_zh = cos_sim(v_ñ_es, v_ñ_zh)

    print(f"SIMILITUD DE LA 'Ñ' ENTRE IDIOMAS:")
    print(f"  ES <-> EN: {sim_ñ_es_en*100:.2f}%")
    print(f"  ES <-> ZH: {sim_ñ_es_zh*100:.2f}%")

    # 2. COMPARAR Ñ vs N (EL DUELO DE IDENTIDAD)
    v_n_es = alfabeto["ES"]["n"]
    v_n_en = alfabeto["EN"]["n"]
    v_n_zh = alfabeto["ZH"]["n"]

    print(f"\nDUELO Ñ vs N (¿Las confunde la IA?):")
    print(f"  ESPAÑOL: Similitud Ñ-N = {cos_sim(v_ñ_es, v_n_es)*100:.2f}%")
    print(f"  INGLÉS:  Similitud Ñ-N = {cos_sim(v_ñ_en, v_n_en)*100:.2f}%")
    print(f"  CHINO:   Similitud Ñ-N = {cos_sim(v_ñ_zh, v_n_zh)*100:.2f}%")

    reporte = {
        "soberania_ñ": {
            "es_en": float(sim_ñ_es_en),
            "es_zh": float(sim_ñ_es_zh)
        },
        "confusion_n": {
            "es": float(cos_sim(v_ñ_es, v_n_es)),
            "en": float(cos_sim(v_ñ_en, v_n_en)),
            "zh": float(cos_sim(v_ñ_zh, v_n_zh))
        }
    }

    out_path = os.path.join(BASE_DIR, "PIEDRA_ROSETA", "EXPERIMENTOS", "BUSQUEDA_NEURONAL", "REPORTE_SOBERANIA_EÑE.json")
    with open(out_path, "w") as f:
        json.dump(reporte, f, indent=4)
    print(f"\nReporte de Soberanía guardado en: {out_path}")

if __name__ == "__main__":
    analizar_soberania_eñe()
