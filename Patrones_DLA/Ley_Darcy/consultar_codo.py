import json
import os
import glob

def consultar():
    archivos = glob.glob("*_mapeo_codos_darcy.json")
    if not archivos: return
    ultimo = max(archivos, key=os.path.getctime)
    with open(ultimo, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sujetos = ["CABALLO_OBSTRUIDO", "GATO_FLUIDO"]
    print(f"--- COMPARATIVA DE PRESIÓN EN CAPA 4 (Índice 0) ---")
    
    for s in sujetos:
        capa4 = next((p for p in data['datos'][s] if p['capa'] == 4), None)
        if capa4:
            print(f"\nSUJETO: {s}")
            print(f" - Caudal: {capa4['caudal']}")
            print(f" - Latencia de Capa: {capa4['latencia_codo_ms']:.4f} ms")

if __name__ == "__main__":
    consultar()
