import os
import torch
import json
import string
from transformers import AutoModelForCausalLM, AutoTokenizer

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MODEL_NAME = "Qwen2.5-0.5B-Instruct"
MODEL_PATH = os.path.join(BASE_DIR, "modelos", MODEL_NAME)

def extractor_alfabeto_multilingue(capa=12):
    print(f"--- EXPERIMENTO 82: EXTRACTOR DE ALFABETO MULTILINGÜE ---")
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16)
    model.eval()

    # Alfabeto: a-z + ñ
    letras = list(string.ascii_lowercase) + ["ñ"]
    
    idiomas = {
        "ES": "Repite exactamente la letra '{}'",
        "EN": "Repeat exactly the letter '{}'",
        "ZH": "精确重复字母 '{}'"
    }

    diccionario_alfabeto = {lang: {} for lang in idiomas}

    for lang, template in idiomas.items():
        print(f"Destilando Alfabeto desde idioma: {lang}...")
        
        for letra in letras:
            prompt = template.format(letra)
            pt = tokenizer.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True)
            inputs = tokenizer(pt, return_tensors="pt").to(model.device)
            
            # Localizar el token de la letra
            # Nota: ñ puede ser un token único o multi-token según el tokenizer
            token_ids_letra = tokenizer.encode(letra, add_special_tokens=False)
            
            try:
                # Buscamos la posición del primer token de la letra en la secuencia
                pos = -1
                for j in range(len(inputs.input_ids[0])):
                    if inputs.input_ids[0][j] == token_ids_letra[0]:
                        pos = j
                        break
                
                if pos != -1:
                    with torch.no_grad():
                        out = model(inputs.input_ids, output_hidden_states=True)
                        adn_vector = out.hidden_states[capa][0, pos, :].cpu().float().numpy().tolist()
                        diccionario_alfabeto[lang][letra] = adn_vector
                else:
                    print(f"  Aviso: No se encontró la letra '{letra}' en {lang}")
            except Exception as e:
                print(f"  Error en letra '{letra}' ({lang}): {str(e)}")

    out_path = os.path.join(BASE_DIR, "PIEDRA_ROSETA", "EXPERIMENTOS", "BUSQUEDA_NEURONAL", "ALFABETO_MULTILINGUE_BASE.json")
    with open(out_path, "w") as f:
        json.dump(diccionario_alfabeto, f)
    
    print(f"\n¡Alfabeto Destilado! Diccionario guardado en: {out_path}")

if __name__ == "__main__":
    extractor_alfabeto_multilingue()
