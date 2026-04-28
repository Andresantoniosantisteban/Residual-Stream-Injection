import os
import torch
import json
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_NAME = "Qwen2.5-0.5B-Instruct"
MODEL_PATH = os.path.join(BASE_DIR, "modelos", MODEL_NAME)

def hack_realidad_sintetica():
    print(f"--- INICIANDO HACK DE REALIDAD SINTÉTICA (Tony Stark Mode) ---")
    
    # 1. Cargar modelo y Alfabeto
    print("Cargando modelo...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16)
    model.eval()

    alfabeto_path = os.path.join(BASE_DIR, "EL_MECANISMO_PERFECTO", "ALFABETO_NUMERICO_PURO.json")
    with open(alfabeto_path, "r") as f:
        alfabeto = json.load(f)
    
    # Convertir firmas a tensores
    firmas = {k: torch.tensor(v, dtype=torch.float16).to(model.device) for k, v in alfabeto.items()}

    # 2. Configurar el Experimento
    numero_original = "102938475612"
    numero_sintetico = "777777777777"
    soberania = 1.8 # Factor de amplificación para asegurar la inyección
    
    prompt = f"Repite exactamente '{numero_original}'"
    print(f"Prompt Original (Realidad A): {numero_original}")
    print(f"Objetivo Inyectado (Realidad B): {numero_sintetico}")

    messages = [{"role": "user", "content": prompt}]
    pt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(pt, return_tensors="pt").to(model.device)
    
    # Mapear posiciones de los tokens del número
    tokens_num = tokenizer.tokenize(numero_original)
    token_ids_num = tokenizer.convert_tokens_to_ids(tokens_num)
    input_ids_list = inputs.input_ids[0].tolist()
    
    start_idx = -1
    for i in range(len(input_ids_list) - len(token_ids_num)):
        if input_ids_list[i:i+len(token_ids_num)] == token_ids_num:
            start_idx = i
            break
            
    if start_idx == -1:
        print("Error: No se pudo localizar el número en el prompt.")
        return

    # 3. El Hook de Inyección (Capa 12)
    def hook_hack_realidad(module, input, output):
        target = output[0] if isinstance(output, tuple) else output
        # Solo intervenimos en el Prefill (3D)
        if target.dim() == 3 and target.shape[1] > start_idx:
            print(f"  [SISTEMA] Hackeando Capa 12: Sustituyendo pasajeros...")
            for i in range(len(numero_original)):
                pos = start_idx + i
                char_orig = numero_original[i]
                char_sint = numero_sintetico[i]
                
                # Operación Quirúrgica:
                # v_final = v_actual - firma_original + (firma_sintetica * soberania)
                v_orig = firmas[char_orig]
                v_sint = firmas[char_sint]
                
                target[0, pos, :] = target[0, pos, :] - v_orig + (v_sint * soberania)
        return output

    # Registramos el hook en la Capa 12
    handle = model.model.layers[12].register_forward_hook(hook_hack_realidad)

    # 4. Generación
    print("Generando respuesta con realidad alterada...")
    with torch.no_grad():
        output_ids = model.generate(
            inputs.input_ids,
            max_new_tokens=20,
            do_sample=False
        )

    handle.remove()

    respuesta = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    respuesta_neta = respuesta.split("assistant\n")[-1].strip()

    print(f"\n--- RESULTADO DEL HACK ---")
    print(f"Respuesta del Modelo: {respuesta_neta}")
    
    if "777" in respuesta_neta:
        print(f"\n[ÉXITO TOTAL] ¡HEMOS HACKEADO LA REALIDAD!")
        print(f"El modelo cree que leyó '{numero_sintetico}' a pesar de tener '{numero_original}' en su prompt.")
    else:
        print(f"\n[FALLO] El modelo se resiste. La atención al prompt original es demasiado fuerte.")

if __name__ == "__main__":
    hack_realidad_sintetica()
