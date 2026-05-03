import json

FILE = r'c:\Users\andre\Desktop\Neural_Identity_Forge\Entendiendo\Estudio_Patrones\DLA_data_sedimentaria\Patrones_DLA\Analisis_Cauces\20260502_1805_MAPA_CUENCA_TOTAL.json'
TOTAL_N = 4864

with open(FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"{'CAPA':<6} | {'ACTIVAS':<10} | {'DENSIDAD':<10} | {'PRESIÓN MEDIA':<15}")
print("-" * 50)

for layer in range(24):
    l_data = data['cuenca'][str(layer)]
    activas = len(l_data)
    densidad = (activas / TOTAL_N) * 100
    presion_media = sum([n['p'] for n in l_data]) / activas if activas > 0 else 0
    
    print(f"{layer:<6} | {activas:<10} | {densidad:>7.2f}% | {presion_media:>13.6f}")
