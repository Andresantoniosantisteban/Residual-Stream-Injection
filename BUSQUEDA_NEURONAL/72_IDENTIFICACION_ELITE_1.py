import os
import json
import numpy as np

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DICCIONARIO_PATH = os.path.join(BASE_DIR, "PIEDRA_ROSETA", "ALFABETO_NUMERICO_PURO.json")
MAPA_ESTRAT_PATH = os.path.join(BASE_DIR, "PIEDRA_ROSETA", "MAPA_ESTRATIGRAFICO_PROTOCOLO_29.json")
OUT_DIR = os.path.join(BASE_DIR, "PIEDRA_ROSETA", "EXPERIMENTOS", "BUSQUEDA_NEURONAL")

def buscar_culpables_1(top_n=10):
    print(f"--- BUSCANDO CULPABLES NEURONALES DEL NÚMERO '1' ---")
    
    # 1. Cargar el ADN Purificado Estratigráfico
    with open(MAPA_ESTRAT_PATH, "r") as f: data = json.load(f)
    
    informe_elite = {}

    for capa in range(24):
        capa_str = str(capa)
        if capa_str not in data or "identidades_puras" not in data[capa_str]:
            continue
            
        if "1" not in data[capa_str]["identidades_puras"]:
            continue
        
        # El vector de identidad purificada (ADN)
        v_adn = np.array(data[capa_str]["identidades_puras"]["1"])
        
        # Encontrar las dimensiones con mayor peso absoluto
        indices_elite = np.argsort(np.abs(v_adn))[-top_n:][::-1]
        valores_elite = v_adn[indices_elite]
        
        informe_elite[capa_str] = {
            "indices": indices_elite.tolist(),
            "valores": valores_elite.tolist(),
            "magnitud_total": float(np.linalg.norm(v_adn))
        }
        
        print(f"Capa {capa:02d}: Top Neurona {indices_elite[0]} (Valor: {valores_elite[0]:.4f})")

    # Guardar Informe de Élite
    out_path = os.path.join(OUT_DIR, "ELITE_NEURONAL_1.json")
    with open(out_path, "w") as f:
        json.dump(informe_elite, f, indent=4)

    print(f"\n¡Cacería completada! Los culpables del '1' están en: {out_path}")

if __name__ == "__main__":
    buscar_culpables_1()
