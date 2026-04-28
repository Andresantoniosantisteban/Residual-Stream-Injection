import os
import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_NAME = "Qwen2.5-0.5B-Instruct"
MODEL_PATH = os.path.join(BASE_DIR, "modelos", MODEL_NAME)

def validacion_unitaria():
    print(f"--- VALIDACIÓN UNITARIA DEL ALFABETO (0-9) ---")
    
    # 1. Cargar modelo y Alfabeto
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16)
    model.eval()

    alfabeto_path = os.path.join(BASE_DIR, "EL_MECANISMO_PERFECTO", "ALFABETO_NUMERICO_PURO.json")
    with open(alfabeto_path, "r") as f:
        alfabeto = json.load(f)
    firmas = {k: torch.tensor(v, dtype=torch.float16).to(model.device) for k, v in alfabeto.items()}

    soberania = 1.8
    resultados = []

    # Probaremos inyectar el dígito 'i' sobre el prompt del dígito '0'
    num_orig = "0"
    
    for i in range(10):
        num_sint = str(i)
        print(f"Probando unidad: Inyectando {num_sint} sobre prompt de {num_orig}...")
        
        prompt = f"Repite exactamente '{num_orig}'"
        inputs = tokenizer(tokenizer.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True), return_tensors="pt").to(model.device)
        
        # Localizar el token del número '0'
        token_id_orig = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(num_orig))[0]
        input_ids_list = inputs.input_ids[0].tolist()
        pos_orig = -1
        for j in range(len(input_ids_list)):
            if input_ids_list[j] == token_id_orig:
                pos_orig = j
                break

        if pos_orig == -1:
            print(f"  Error: No se encontró el token {num_orig}")
            continue

        def hook_unid(module, input, output):
            target = output[0] if isinstance(output, tuple) else output
            if target.dim() == 3 and target.shape[1] > pos_orig:
                # v_new = v_actual - firma_0 + (firma_i * soberania)
                v_orig = firmas["0"]
                v_sint = firmas[num_sint]
                target[0, pos_orig, :] = target[0, pos_orig, :] - v_orig + (v_sint * soberania)
            return output

        handle = model.model.layers[12].register_forward_hook(hook_unid)
        with torch.no_grad():
            out = model.generate(inputs.input_ids, max_new_tokens=5, do_sample=False)
        handle.remove()

        res = tokenizer.decode(out[0], skip_special_tokens=True).split("assistant\n")[-1].strip()
        # Limpiar respuesta (quitar comillas si las hay)
        res_limpia = res.replace("'", "").replace('"', "").strip()
        
        exito = num_sint == res_limpia
        print(f"  Resultado: {res} -> {'ÉXITO' if exito else 'FALLO'}")
        resultados.append({"inyectado": num_sint, "respuesta": res, "exito": exito})

    # Guardar resultados
    out_path = os.path.join(BASE_DIR, "EL_MECANISMO_PERFECTO", "RESULTADOS_VALIDACION_UNITARIA.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4)

    aciertos = sum([1 for r in resultados if r["exito"]])
    print(f"\n--- VALIDACIÓN UNITARIA COMPLETADA ---")
    print(f"Aciertos totales: {aciertos}/10")

if __name__ == "__main__":
    validacion_unitaria()
