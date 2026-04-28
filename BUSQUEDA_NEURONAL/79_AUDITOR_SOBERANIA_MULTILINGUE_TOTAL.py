import os
import torch
import json
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MODEL_NAME = "Qwen2.5-0.5B-Instruct"
MODEL_PATH = os.path.join(BASE_DIR, "modelos", MODEL_NAME)
DICCIONARIO_PATH = os.path.join(BASE_DIR, "PIEDRA_ROSETA", "EXPERIMENTOS", "BUSQUEDA_NEURONAL", "DICCIONARIO_MULTILINGUE_BASE.json")

def auditoria_soberania_multilingue_total(capa=12, soberania=1.8):
    print(f"--- EXPERIMENTO 79: AUDITORÍA DE SOBERANÍA TOTAL (ES/EN/ZH) ---")
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16)
    model.eval()

    with open(DICCIONARIO_PATH, "r") as f: diccionario = json.load(f)

    idiomas = {
        "ES": "Repite exactamente '0'",
        "EN": "Repeat exactly '0'",
        "ZH": "精确重复 '0'"
    }

    reporte_final = []

    for lang, prompt in idiomas.items():
        print(f"\nAuditando Soberanía en: {lang}")
        
        pt = tokenizer.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(pt, return_tensors="pt").to(model.device)
        token_id_0 = tokenizer.convert_tokens_to_ids("0")
        pos_target = (inputs.input_ids[0] == token_id_0).nonzero(as_tuple=True)[0].tolist()[0]

        # v_base: El ADN del '0' nativo de este idioma
        v_base = torch.tensor(diccionario[lang]["0"], dtype=torch.float16).to(model.device)

        for i in range(10):
            digito_obj = str(i)
            # v_sint: El ADN del dígito extraído en ESPAÑOL (Nuestro Clon Universal)
            v_sint = torch.tensor(diccionario["ES"][digito_obj], dtype=torch.float16).to(model.device)

            def hook_quirurgico(module, input, output):
                target = output[0] if isinstance(output, tuple) else output
                # APLICANDO LA FÓRMULA DE ÉXITO DEL SCRIPT 49
                target[0, pos_target, :] = target[0, pos_target, :] - v_base + (v_sint * soberania)
                return output

            handle = model.model.layers[capa].register_forward_hook(hook_quirurgico)
            with torch.no_grad():
                out = model.generate(inputs.input_ids, max_new_tokens=5, do_sample=False, use_cache=False)
            handle.remove()

            # Limpiar la respuesta para obtener solo el dígito
            res_completa = tokenizer.decode(out[0], skip_special_tokens=True).split("assistant\n")[-1].strip()
            # Intentar extraer el número de la respuesta (a veces la IA dice "El número es 8" o similar)
            res_limpia = "".join([c for c in res_completa if c.isdigit()])[:1]

            exito = (res_limpia == digito_obj)
            print(f"  [{lang}] Inyectado: {digito_obj} -> IA responde: '{res_completa}' | Éxito: {exito}")

            reporte_final.append({
                "idioma": lang,
                "dígito_inyectado": digito_obj,
                "capa": capa,
                "respuesta_modelo": res_completa,
                "exito": exito
            })

    out_path = os.path.join(BASE_DIR, "PIEDRA_ROSETA", "EXPERIMENTOS", "BUSQUEDA_NEURONAL", "AUDITORIA_SOBERANIA_TOTAL_RESULTADOS.json")
    with open(out_path, "w") as f:
        json.dump(reporte_final, f, indent=4)
    print(f"\nAuditoría completada. Resultados en: {out_path}")

if __name__ == "__main__":
    auditoria_soberania_multilingue_total()
