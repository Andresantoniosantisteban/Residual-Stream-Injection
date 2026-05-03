import json
import numpy as np
from scipy.stats import pearsonr, spearmanr

# --- RUTAS ---
FILE_OLD = r'c:\Users\andre\Desktop\Neural_Identity_Forge\Entendiendo\Estudio_Patrones\DLA_data_sedimentaria\Patrones_DLA\Ley_Darcy\20260502_1150_darcy_resultados.json'
FILE_NEW = r'c:\Users\andre\Desktop\Neural_Identity_Forge\Entendiendo\Estudio_Patrones\DLA_data_sedimentaria\Patrones_DLA\Ley_Darcy\Validacion_predictiva_masiva\20260502_1839_darcy_validacion_masiva.json'

def auditar_fidelidad():
    with open(FILE_OLD, 'r', encoding='utf-8') as f:
        old_data = json.load(f)['sujetos_analizados']
    
    with open(FILE_NEW, 'r', encoding='utf-8') as f:
        new_data = json.load(f)['analisis_por_sujeto']

    # Sujetos a comparar (Normalizando nombres)
    # En el viejo era 'gato_ato', en el nuevo es 'GATO'
    comparativas = [
        ("gato_ato", "GATO"),
        ("perro_ro", "PERRO"),
        ("dinero_ \u0120dinero", "DINERO"), # El espacio en el viejo es importante
        ("manzana_ana", "MANZANA")
    ]

    print("\n--- REPORTE DE FIDELIDAD ESTRUCTURAL (DARCY RAW) ---")
    print(f"{'SUJETO':<15} | {'PEARSON %':<12} | {'SPEARMAN %':<12} | {'ESTADO'}")
    print("-" * 60)

    for old_key, new_key in comparativas:
        try:
            # Si el viejo tiene espacio o algo raro lo buscamos por aproximación si falla
            if old_key not in old_data:
                # Intento buscar por prefijo
                match = [k for k in old_data.keys() if old_key.split("_")[0] in k]
                if match: old_key = match[0]

            h_old = old_data[old_key]['perfil_carga_h']
            h_new = new_data[new_key]['perfil_carga_h']

            # Pearson (Similitud lineal)
            p_corr, _ = pearsonr(h_old, h_new)
            # Spearman (Similitud de escala/rango)
            s_corr, _ = spearmanr(h_old, h_new)

            estado = "✅ IDENTIDAD VALIDADA" if p_corr > 0.90 else "⚠️ DESVÍO DETECTADO"

            print(f"{new_key:<15} | {p_corr*100:>10.2f}% | {s_corr*100:>10.2f}% | {estado}")
        except Exception as e:
            print(f"{new_key:<15} | ERROR: {str(e)}")

if __name__ == "__main__":
    auditar_fidelidad()
