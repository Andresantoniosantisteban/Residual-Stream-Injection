import json
import numpy as np
import os

BASE_DIR = r'c:\Users\andre\Desktop\Neural_Identity_Forge\Entendiendo\Estudio_Patrones\DLA_data_sedimentaria\Patrones_DLA\Ley_Darcy\Validacion_predictiva_incognito'
ACUIFERO_PATH = os.path.join(BASE_DIR, 'acuifero_estructural.json')
OUTPUT_PATH = os.path.join(BASE_DIR, '20260502_1920_DARCY_PREDICCION_TEORICA_15.json')

def generar_15_escenarios():
    with open(ACUIFERO_PATH, 'r', encoding='utf-8') as f:
        acuifero = json.load(f)
    
    topografia_norm = np.array(acuifero['topografia_norm'])
    
    # Definición de las 5 incógnitas (Nivel Medio)
    incognitas = {
        "LAVA": {"inercia_base": 280, "viscosidad_base": 2.50, "escala_base": 0.89},
        "LOBO": {"inercia_base": 320, "viscosidad_base": 3.00, "escala_base": 0.88},
        "SATÉLITE": {"inercia_base": 290, "viscosidad_base": 2.60, "escala_base": 0.89},
        "JUSTICIA": {"inercia_base": 265, "viscosidad_base": 2.45, "escala_base": 0.90},
        "HONGO": {"inercia_base": 295, "viscosidad_base": 2.75, "escala_base": 0.89}
    }
    
    multiverso = {
        "timestamp": "2026-05-02 19:20:00",
        "autor": "Andrés Antonio Santisteban Lino",
        "protocolo": "Predicción Ciega Tripartita",
        "escenarios": {}
    }
    
    # Simulación inicial (Capas 0-5)
    # Usamos una presión inicial promedio de la fase masiva para el arranque (~1500)
    H_INICIAL = 1500 

    for concepto, params in incognitas.items():
        multiverso["escenarios"][concepto] = {}
        
        for nivel in ["ALTO", "MEDIO", "BAJO"]:
            # Ajuste de parámetros según nivel
            if nivel == "ALTO":
                inercia = params["inercia_base"] * 1.10
                escala = min(1.0, params["escala_base"] + 0.03)
            elif nivel == "BAJO":
                inercia = params["inercia_base"] * 0.90
                escala = params["escala_base"] - 0.03
            else:
                inercia = params["inercia_base"]
                escala = params["escala_base"]
            
            # Generación de la curva teórica (Darcy)
            # Capas 0-5 (Arranque lineal)
            h_teorica = [H_INICIAL + (inercia * i) for i in range(6)]
            
            # Capas 6-23 (Flujo por Acuífero)
            for i in range(6, 24):
                ratio_suelo = topografia_norm[i] / (topografia_norm[i-1] + 1e-9)
                # Aplicamos la Inercia + Resistencia Estructural + Escala de Amortiguamiento
                proximo_h = (h_teorica[-1] + (inercia / 4.0)) * ratio_suelo * escala
                h_teorica.append(max(0, proximo_h))
            
            multiverso["escenarios"][concepto][nivel] = {
                "inercia_aplicada": float(inercia),
                "escala_aplicada": float(escala),
                "curva_teorica": h_teorica
            }
            
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(multiverso, f, indent=4)
    
    print(f"Multiverso de 15 Escenarios Teóricos generado en: {OUTPUT_PATH}")

if __name__ == "__main__":
    generar_15_escenarios()
