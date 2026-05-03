import json
import numpy as np
import os

RAW_DIR = r'c:\Users\andre\Desktop\Neural_Identity_Forge\Entendiendo\Estudio_Patrones\DLA_data_sedimentaria\ADN_RAW\que_es'
OUTPUT_REALIDAD = r'c:\Users\andre\Desktop\Neural_Identity_Forge\Entendiendo\Estudio_Patrones\DLA_data_sedimentaria\Patrones_DLA\Ley_Darcy\Validacion_predictiva_incognito\20260502_1935_REALIDAD_CRUDA.json'

SUJETOS_INCOGNITO = ["LAVA", "LOBO", "SATÉLITE", "JUSTICIA", "HONGO"]

def extraer_realidad_cruda():
    print("--- FASE 1: EXTRACCIÓN DE REALIDAD CRUDA ---")
    realidad_total = {
        "timestamp": "2026-05-02 19:35:00",
        "autor": "Andrés Antonio Santisteban Lino",
        "datos_empiricos": {}
    }

    for sujeto in SUJETOS_INCOGNITO:
        path = os.path.join(RAW_DIR, f"ADN_RAW_{sujeto}.json")
        if not os.path.exists(path):
            print(f"Advertencia: No se encontró {sujeto}")
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Promediado de presión por capa a través de todos los tokens
        h_perfil = np.zeros(24)
        num_tokens = len(data['flujo_total'])
        
        for t_info in data['flujo_total']:
            for capa_info in t_info['capas']:
                capa_idx = capa_info['capa']
                impacto = sum([abs(n['im']) for n in capa_info['flujo']])
                h_perfil[capa_idx] += impacto
        
        h_perfil /= num_tokens
        
        realidad_total["datos_empiricos"][sujeto] = {
            "pregunta": data['metadata']['pregunta'],
            "perfil_presion_real": h_perfil.tolist(),
            "num_tokens_analizados": num_tokens
        }
        print(f"Extraída Realidad para: {sujeto}")

    with open(OUTPUT_REALIDAD, 'w', encoding='utf-8') as f:
        json.dump(realidad_total, f, indent=4)
    
    print(f"\nFase 1 completada. Realidad Cruda guardada en: {OUTPUT_REALIDAD}")

if __name__ == "__main__":
    extraer_realidad_cruda()
