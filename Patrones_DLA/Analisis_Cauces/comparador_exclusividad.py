import json
import os
import glob

RAW_DIR = r'c:\Users\andre\Desktop\Neural_Identity_Forge\Entendiendo\Estudio_Patrones\DLA_data_sedimentaria\ADN_RAW'
TOTAL_N = 4864

def analizar_exclusividad(sujeto_a, sujeto_b):
    path_a = os.path.join(RAW_DIR, f"ADN_RAW_{sujeto_a}.json")
    path_b = os.path.join(RAW_DIR, f"ADN_RAW_{sujeto_b}.json")
    
    with open(path_a, 'r', encoding='utf-8') as f: data_a = json.load(f)
    with open(path_b, 'r', encoding='utf-8') as f: data_b = json.load(f)

    print(f"ANÁLISIS DE EXCLUSIVIDAD: {sujeto_a} vs {sujeto_b}")
    print("-" * 60)
    print(f"{'CAPA':<5} | {'DENS. A':<8} | {'DENS. B':<8} | {'SOLAPE':<8} | {'EXCLUS. A':<10}")
    
    for layer in range(24):
        # Extraemos solo los Hubs locales (Top 100 neuronas con más presión por token)
        ids_a = set()
        for t in data_a['flujo_total']:
            for c in t['capas']:
                if c['capa'] == layer:
                    # Ordenamos y tomamos el Top 100 de este token
                    sorted_n = sorted(c['flujo'], key=lambda x: abs(x['im']), reverse=True)
                    for n in sorted_n[:100]: ids_a.add(n['i'])
        
        ids_b = set()
        for t in data_b['flujo_total']:
            for c in t['capas']:
                if c['capa'] == layer:
                    sorted_n = sorted(c['flujo'], key=lambda x: abs(x['im']), reverse=True)
                    for n in sorted_n[:100]: ids_b.add(n['i'])

        
        solape = ids_a.intersection(ids_b)
        exclusivas_a = ids_a - ids_b
        
        dens_a = (len(ids_a) / TOTAL_N) * 100
        dens_b = (len(ids_b) / TOTAL_N) * 100
        perc_solape = (len(solape) / len(ids_a | ids_b)) * 100 if (ids_a | ids_b) else 0
        
        print(f"{layer:<5} | {dens_a:>6.2f}% | {dens_b:>6.2f}% | {perc_solape:>6.2f}% | {len(exclusivas_a):<10}")

if __name__ == "__main__":
    # Comparamos GATO vs DINERO (Conceptos muy distintos)
    analizar_exclusividad("GATO", "DINERO")
