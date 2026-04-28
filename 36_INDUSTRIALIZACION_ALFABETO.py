import os
import torch
import json
import string
from transformers import AutoModelForCausalLM, AutoTokenizer

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_NAME = "Qwen2.5-0.5B-Instruct"
MODEL_PATH = os.path.join(BASE_DIR, "modelos", MODEL_NAME)

def industrializar_alfabeto():
    print(f"--- CADENA DE MONTAJE: PIEDRA ROSETA ALFABÉTICA ---")
    
    # 1. Cargar modelo
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16)
    model.eval()

    alfabeto_letras = string.ascii_letters # A-Z y a-z
    firmas_literarias = {}
    errores = []

    print(f"Procesando {len(alfabeto_letras)} caracteres...")

    for letra in alfabeto_letras:
        prompt = f"Repite exactamente '{letra}'"
        messages = [{"role": "user", "content": prompt}]
        pt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(pt, return_tensors="pt").to(model.device)
        
        # Validar Repetición (Control de Calidad)
        with torch.no_grad():
            output_ids = model.generate(inputs.input_ids, max_new_tokens=5, do_sample=False)
            res = tokenizer.decode(output_ids[0], skip_special_tokens=True).split("assistant\n")[-1].strip().replace("'", "").replace('"', "")
            
            if res != letra:
                print(f"  [AVISO] Letra '{letra}' falló control de calidad (Respuesta: {res})")
                errores.append(letra)
                # A pesar del fallo, intentamos extraer la firma si el token existe
            
            # Extraer Firma Vectorial (Capa 12)
            outputs = model(inputs.input_ids, output_hidden_states=True)
            h_layer = outputs.hidden_states[12][0].detach().cpu().float()
            
            # Localizar el token de la letra
            token_ids = tokenizer.tokenize(letra)
            if not token_ids: continue
            token_id = tokenizer.convert_tokens_to_ids(token_ids[0])
            
            pos = -1
            input_ids_list = inputs.input_ids[0].tolist()
            for j in range(len(input_ids_list)):
                if input_ids_list[j] == token_id:
                    pos = j
                    break
            
            if pos != -1:
                v_bus = torch.mean(h_layer, dim=0)
                v_capsula = h_layer[pos] - v_bus
                firmas_literarias[letra] = v_capsula.tolist()
                print(f"  Letra '{letra}': ADN extraído correctamente.")

    # 3. Guardar JSON Maestro
    out_path = os.path.join(BASE_DIR, "EL_MECANISMO_PERFECTO", "ALFABETO_LITERARIO_PURO.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(firmas_literarias, f, indent=4)

    print(f"\n--- INDUSTRIALIZACIÓN COMPLETADA ---")
    print(f"Caracteres procesados: {len(firmas_literarias)}/52")
    print(f"Letras con errores: {len(errores)}")
    print(f"Base de datos guardada en: {out_path}")

if __name__ == "__main__":
    industrializar_alfabeto()
