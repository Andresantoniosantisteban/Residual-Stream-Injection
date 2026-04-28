import os
import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_NAME = "Qwen2.5-0.5B-Instruct"
MODEL_PATH = os.path.join(BASE_DIR, "modelos", MODEL_NAME)

def auditoria_numerica_total():
    print(f"--- AUDITORÍA NUMÉRICA TOTAL (0-9) ---")
    
    # 1. Cargar modelo y Alfabeto
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16)
    model.eval()

    alfabeto_path = os.path.join(BASE_DIR, "PIEDRA_ROSETA", "ALFABETO_NUMERICO_PURO.json")
    with open(alfabeto_path, "r") as f:
        alfabeto = json.load(f)
    firmas = {k: torch.tensor(v, dtype=torch.float16).to(model.device) for k, v in alfabeto.items()}

    soberania = 1.8
    resultados = []
    num_base = "0"
    
    print(f"Iniciando pruebas unitarias en Capa 12...")

    for i in range(10):
        num_obj = str(i)
        print(f"  Auditando dígito: '{num_obj}'...")
        
        prompt = f"Repite exactamente '{num_base}'"
        inputs = tokenizer(tokenizer.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True), return_tensors="pt").to(model.device)
        
        token_id_base = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(num_base))[0]
        pos_base = -1
        for j in range(len(inputs.input_ids[0])):
            if inputs.input_ids[0][j] == token_id_base:
                pos_base = j
                break

        if pos_base == -1: continue

        def hook_audit(module, input, output):
            target = output[0] if isinstance(output, tuple) else output
            if target.dim() == 3 and target.shape[1] > pos_base:
                v_base = firmas[num_base]
                v_sint = firmas[num_obj]
                target[0, pos_base, :] = target[0, pos_base, :] - v_base + (v_sint * soberania)
            return output

        handle = model.model.layers[12].register_forward_hook(hook_audit)
        with torch.no_grad():
            out = model.generate(inputs.input_ids, max_new_tokens=5, do_sample=False)
        handle.remove()

        res = tokenizer.decode(out[0], skip_special_tokens=True).split("assistant\n")[-1].strip().replace("'", "").replace('"', "")
        
        exito = num_obj == res
        
        resultados.append({
            "dígito_inyectado": num_obj,
            "capa": 12,
            "respuesta_modelo": res,
            "exito": exito
        })

    # Guardar Informe
    out_path = os.path.join(BASE_DIR, "PIEDRA_ROSETA", "AUDITORIA_NUMERICA_RESULTADOS.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4)

    aciertos = sum([1 for r in resultados if r["exito"]])
    print(f"\n--- AUDITORÍA COMPLETADA ---")
    print(f"Tasa de éxito: {aciertos}/10")
    print(f"Informe guardado en: {out_path}")

if __name__ == "__main__":
    auditoria_numerica_total()
