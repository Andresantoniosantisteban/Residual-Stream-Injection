import os
import torch
import json
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MODEL_NAME = "Qwen2.5-0.5B-Instruct"
MODEL_PATH = os.path.join(BASE_DIR, "modelos", MODEL_NAME)

def extractor_idiomatico_formal(capa=12):
    print(f"--- EXPERIMENTO 78: EXTRACTOR IDIOMÁTICO DE ADN (CAPA {capa}) ---")
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16)
    model.eval()

    idiomas = {
        "ES": "Repite exactamente '0'",
        "EN": "Repeat exactly '0'",
        "ZH": "精确重复 '0'"
    }

    diccionario_maestro = {lang: {} for lang in idiomas}

    for lang, prompt in idiomas.items():
        print(f"Destilando ADN del idioma: {lang}...")
        
        pt = tokenizer.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(pt, return_tensors="pt").to(model.device)
        
        # Extraer el vector ADN de todos los números del 0 al 9 en este idioma
        for i in range(10):
            digito = str(i)
            curr_prompt = prompt.replace("'0'", f"'{digito}'")
            curr_pt = tokenizer.apply_chat_template([{"role": "user", "content": curr_prompt}], tokenize=False, add_generation_prompt=True)
            curr_inputs = tokenizer(curr_pt, return_tensors="pt").to(model.device)
            
            # Localizar el token del número
            token_id = tokenizer.convert_tokens_to_ids(digito)
            try:
                pos = (curr_inputs.input_ids[0] == token_id).nonzero(as_tuple=True)[0].tolist()[0]
                
                with torch.no_grad():
                    out = model(curr_inputs.input_ids, output_hidden_states=True)
                    # Extraer el ADN puro de la capa 12
                    adn_vector = out.hidden_states[capa][0, pos, :].cpu().float().numpy().tolist()
                    diccionario_maestro[lang][digito] = adn_vector
            except:
                print(f"  Error extrayendo '{digito}' en {lang}")

    out_path = os.path.join(BASE_DIR, "PIEDRA_ROSETA", "EXPERIMENTOS", "BUSQUEDA_NEURONAL", "DICCIONARIO_MULTILINGUE_BASE.json")
    with open(out_path, "w") as f:
        json.dump(diccionario_maestro, f)
    
    print(f"\n¡Extracción Completada! Diccionario Maestro guardado en: {out_path}")

if __name__ == "__main__":
    extractor_idiomatico_formal()
