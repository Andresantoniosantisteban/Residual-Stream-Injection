import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import os
import numpy as np
from datetime import datetime

# --- CONFIGURACIÓN DE ALTA RESOLUCIÓN ATÓMICA (MODO INCOGNITO) ---
MODEL_ID = "Qwen/Qwen2.5-0.5B"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
RAW_DIR = r'c:\Users\andre\Desktop\Neural_Identity_Forge\Entendiendo\Estudio_Patrones\DLA_data_sedimentaria\ADN_RAW\que_es'
# REDIRECCIÓN: Apuntamos al nuevo protocolo de preguntas incógnito
INPUT_PATH = r'c:\Users\andre\Desktop\Neural_Identity_Forge\Entendiendo\Estudio_Patrones\DLA_data_sedimentaria\Patrones_DLA\Ley_Darcy\Validacion_predictiva_incognito\PROTOCOLO_INCOGNITO_PREGUNTAS.json'
MONITOR_PATH = r"c:\Users\andre\Desktop\Neural_Identity_Forge\Entendiendo\Estudio_Patrones\DLA_data_sedimentaria\Patrones_DLA\Ley_Darcy\Validacion_predictiva_incognito\MONITOR_ESCANEO_INCOGNITO.txt"

def obtener_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def actualizar_monitor(sujeto, token, progreso):
    with open(MONITOR_PATH, 'w', encoding='utf-8') as f:
        f.write(f"--- MONITOR DE ESCANEO INCOGNITO ---\n")
        f.write(f"Último Pulso: {obtener_timestamp()}\n")
        f.write(f"Sujeto Actual: {sujeto.upper()}\n")
        f.write(f"Token: {token}\n")
        f.write(f"Progreso: {progreso}\n")
        f.write(f"Estado: TRABAJANDO...\n")

def ejecutar_escaneo_atomico():
    print(f"[{obtener_timestamp()}] Iniciando Escaneo Incógnito (Alta Resolución)...")
    
    if not os.path.exists(RAW_DIR): os.makedirs(RAW_DIR)
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16).to(DEVICE)

    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        base_preguntas = json.load(f)

    activaciones_temp = {}
    def hook_fn(layer_idx):
        def hook(module, input, output):
            activaciones_temp[layer_idx] = output.detach().cpu()
        return hook

    for i in range(model.config.num_hidden_layers):
        model.model.layers[i].mlp.gate_proj.register_forward_hook(hook_fn(i))

    print(f"[{obtener_timestamp()}] Pre-calculando Topografía de Pesos en GPU...")
    normas_capas = {}
    with torch.no_grad():
        for i in range(model.config.num_hidden_layers):
            weights = model.model.layers[i].mlp.down_proj.weight
            normas_capas[i] = torch.norm(weights, dim=0).cpu().numpy()

    for pregunta, metadata in base_preguntas.items():
        sujeto = metadata['sujeto']
        nombre_archivo = f"ADN_RAW_{sujeto.upper().replace(' ', '_')}.json"
        full_output_path = os.path.join(RAW_DIR, nombre_archivo)
        
        if os.path.exists(full_output_path):
            print(f"[{obtener_timestamp()}] Saltando {sujeto} (Ya existe).")
            continue

        print(f"[{obtener_timestamp()}] Mapeando Identidad: {sujeto.upper()}...")
        
        inputs = tokenizer(pregunta, return_tensors="pt").to(DEVICE)
        tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
        indices_sujeto = list(range(len(tokens)))

        with torch.no_grad():
            model(**inputs)

        datos_tokens = []
        total_tokens = len(indices_sujeto)
        for i_count, t_idx in enumerate(indices_sujeto, 1):
            token_str = tokens[t_idx]
            actualizar_monitor(sujeto, token_str, f"{i_count}/{total_tokens}")
            
            mapa_capas = []
            for i in range(model.config.num_hidden_layers):
                vals = activaciones_temp[i][0, t_idx].to(torch.float32).numpy()
                col_norms = normas_capas[i]
                
                neuronas_capa = []
                impactos = vals * col_norms
                indices_activos = np.where(impactos != 0)[0]
                
                for idx_n in indices_activos:
                    neuronas_capa.append({
                        "i": int(idx_n),
                        "im": round(float(impactos[idx_n]), 6)
                    })
                
                mapa_capas.append({
                    "capa": i,
                    "flujo": neuronas_capa
                })

            datos_tokens.append({
                "t_idx": t_idx,
                "token": token_str,
                "capas": mapa_capas
            })

        identidad_data = {
            "metadata": {
                "sujeto": sujeto,
                "pregunta": pregunta,
                "timestamp": obtener_timestamp(),
                "modelo": MODEL_ID
            },
            "flujo_total": datos_tokens
        }
        
        with open(full_output_path, 'w', encoding='utf-8') as f:
            json.dump(identidad_data, f, indent=2)
            
        print(f"[{obtener_timestamp()}] Archivo atómico guardado: {nombre_archivo}")

    print(f"[{obtener_timestamp()}] Escaneo Incógnito Finalizado.")

if __name__ == "__main__":
    ejecutar_escaneo_atomico()
