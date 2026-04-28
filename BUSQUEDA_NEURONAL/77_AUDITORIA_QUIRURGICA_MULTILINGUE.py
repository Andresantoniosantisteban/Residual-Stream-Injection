import os
import torch
import json
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MODEL_NAME = "Qwen2.5-0.5B-Instruct"
MODEL_PATH = os.path.join(BASE_DIR, "modelos", MODEL_NAME)
COMPARATIVA_PATH = os.path.join(BASE_DIR, "PIEDRA_ROSETA", "EXPERIMENTOS", "BUSQUEDA_NEURONAL", "COMPARATIVA_IDIOMAS_NUM.json")

def auditoria_quirurgica_multilingue(capa=12, soberania=1.8):
    print(f"--- EXPERIMENTO 77: AUDITORÍA QUIRÚRGICA MULTILINGÜE (Protocolo 49) ---")
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16)
    model.eval()

    with open(COMPARATIVA_PATH, "r") as f: vectores = json.load(f)

    idiomas = {
        "ES": "Repite exactamente '0'",
        "EN": "Repeat exactly '0'",
        "ZH": "精确重复 '0'"
    }

    reporte_final = {lang: {} for lang in idiomas}

    for lang, prompt in idiomas.items():
        print(f"\n--- Interviniendo en {lang} ---")
        
        pt = tokenizer.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(pt, return_tensors="pt").to(model.device)
        token_id_0 = tokenizer.convert_tokens_to_ids("0")
        pos_target = (inputs.input_ids[0] == token_id_0).nonzero(as_tuple=True)[0].tolist()[0]

        # v_base: La identidad del '0' en este idioma específico
        v_base = torch.tensor(vectores[lang]["0"], dtype=torch.float16).to(model.device)

        for i in range(10):
            num_obj = str(i)
            # v_sint: La identidad sintética extraída en ESPAÑOL
            v_sint = torch.tensor(vectores["ES"][num_obj], dtype=torch.float16).to(model.device)

            def hook_quirurgico(module, input, output):
                target = output[0] if isinstance(output, tuple) else output
                # FÓRMULA SAGRADA DEL SCRIPT 49
                # 1. Borramos el original (target - v_base)
                # 2. Inyectamos nuestra voluntad ( + v_sint * soberania)
                target[0, pos_target, :] = target[0, pos_target, :] - v_base + (v_sint * soberania)
                return output

            handle = model.model.layers[capa].register_forward_hook(hook_quirurgico)
            with torch.no_grad():
                out = model.generate(inputs.input_ids, max_new_tokens=5, do_sample=False, use_cache=False)
            handle.remove()

            res = tokenizer.decode(out[0], skip_special_tokens=True).split("assistant\n")[-1].strip()
            print(f"  Inyectando '{num_obj}' (ES) -> IA responde en {lang}: '{res}'")
            reporte_final[lang][num_obj] = res

    out_path = os.path.join(BASE_DIR, "PIEDRA_ROSETA", "EXPERIMENTOS", "BUSQUEDA_NEURONAL", "REPORTE_QUIRURGICO_MULTILINGUE.json")
    with open(out_path, "w") as f:
        json.dump(reporte_final, f, indent=4)
    print(f"\nReporte Quirúrgico guardado en: {out_path}")

if __name__ == "__main__":
    auditoria_quirurgica_multilingue()
