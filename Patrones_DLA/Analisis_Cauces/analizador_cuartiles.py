import json
import numpy as np

FILE = r'c:\Users\andre\Desktop\Neural_Identity_Forge\Entendiendo\Estudio_Patrones\DLA_data_sedimentaria\Patrones_DLA\Analisis_Cauces\20260502_1805_MAPA_CUENCA_TOTAL.json'

with open(FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("ANÁLISIS DE PRESIÓN POR CUARTILES (FILTRADO ORGÁNICO)")
print("-" * 65)
print(f"{'CAPA':<5} | {'P. MEDIA':<10} | {'Q3 (75%)':<10} | {'NEURONAS VIVAS (>Q3)':<15}")

for layer in range(24):
    l_data = data['cuenca'][str(layer)]
    presiones = [n['p'] for n in l_data if n['p'] > 0]
    
    if not presiones: continue
    
    p_media = np.mean(presiones)
    q3 = np.percentile(presiones, 75)
    vivas = [p for p in presiones if p >= q3]
    
    print(f"{layer:<5} | {p_media:>8.6f} | {q3:>8.6f} | {len(vivas):<15} (25%)")

print("-" * 65)
print("Nota: Solo el 25% superior (Q4) se considera CAUCE VIVO. El resto es RUIDO ORGÁNICO.")
