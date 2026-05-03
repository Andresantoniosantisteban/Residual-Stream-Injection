import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import os
import requests
import numpy as np
import time
from datetime import datetime
from dotenv import load_dotenv

# --- PROTOCOLO DE SEGURIDAD Y CONFIGURACIÓN ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_ID = "Qwen/Qwen2.5-0.5B"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BASE_DIR = r"c:\Users\andre\Desktop\Neural_Identity_Forge"
INPUT_PATH = os.path.join(BASE_DIR, "Entendiendo", "Estudio_Patrones", "DLA_data_sedimentaria", "Protocolo_Experimental", "BASE_30Q_IDENTIDADES.json")
CONFIG_PATH = os.path.join(BASE_DIR, "modelos_virgenes", "config_experimento.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "Entendiendo", "Estudio_Patrones", "DLA_data_sedimentaria", "Patrones_DLA", "Ley_Darcy", "Eficiencia_Energetica")

def obtener_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M")

def auditar_con_gpt(pregunta, respuesta_modelo, intentos=3):
    """
    Auditoría Semántica Blindada V5: GPT-4o + Categorías Profesionales.
    """
    # --- FILTRO DE VACÍO ---
    if not respuesta_modelo or len(respuesta_modelo.strip()) < 2:
        return {"veracidad": False, "limpieza": True, "calidad_0_10": 0, "categoria": "Ausencia_de_Respuesta", "diagnostico": "Caudal insuficiente."}

    # --- FILTRO DE BASURA TÉCNICA (Hard-coded) ---
    basura = ["-cols", "user", "assistant", "<|im_start|>", "etcode", "ieron", "####", "})();", "_granted", "cavsystem", "available"]
    if any(b in respuesta_modelo.lower() for b in basura):
        return {"veracidad": False, "limpieza": False, "calidad_0_10": 1, "categoria": "Fallo_Tecnico", "diagnostico": "Ruido de hardware detectado."}

    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {OPENAI_API_KEY}"}
    
    prompt_audit = f"""
    Actúa como un JUEZ DE LÓGICA NEURONAL. Audita la respuesta del modelo.
    
    PREGUNTA: {pregunta}
    RESPUESTA: {respuesta_modelo}
    
    CATEGORÍAS PROFESIONALES:
    - Correcta_Real: Verdad lógica y texto limpio.
    - Error_Logico: Respuesta incorrecta o falsa.
    - Fallo_Tecnico: Presencia de etiquetas, código o ruido.
    - Bucle_de_Repeticion: Repetición obsesiva de tokens.
    
    Responde estrictamente JSON:
    {{
        "veracidad": bool,
        "limpieza": bool,
        "calidad_0_10": int,
        "categoria": "Correcta_Real | Error_Logico | Fallo_Tecnico | Bucle_de_Repeticion",
        "diagnostico": "nota técnica profesional"
    }}
    """
    
    for i in range(intentos):
        try:
            payload = {"model": "gpt-4o", "messages": [{"role": "user", "content": prompt_audit}], "temperature": 0}
            response = requests.post(url, headers=headers, json=payload, timeout=25)
            res_json = response.json()
            content = res_json['choices'][0]['message']['content']
            return json.loads(content.replace("```json", "").replace("```", "").strip())
        except Exception as e:
            if i == intentos - 1:
                return {"veracidad": False, "limpieza": False, "calidad_0_10": 0, "categoria": "Error_Sensor", "diagnostico": str(e)}
            time.sleep(2)

def darcy_eficiencia_viva_final():
    print(f"[{datetime.now()}] LABORATORIO LISTO: Lanzando Auditoría V3-Final (Mesa de Trabajo de Andrés)")
    
    # 1. Cargar Entorno
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    params = config["parameters"]
    seed = params.get("seed", 42)
    torch.manual_seed(seed)
    np.random.seed(seed)
    
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        identidades = json.load(f)
    
    # 2. Preparar Modelo
    print(f"[{datetime.now()}] Cargando {MODEL_ID}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16).to(DEVICE)
    
    rango_gamma = np.arange(0.30, 1.55, 0.05)
    
    resultados = {
        "timestamp_inicio": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "autor": "Andrés Antonio Santisteban Lino",
        "metodo": "Darcy Live Efficiency V3-FINAL",
        "experimentos": []
    }
    
    ts = obtener_timestamp()
    output_filename = f"{ts}_darcy_V3_FINAL_resultados.json"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    # Hook de Compuerta
    global current_gamma
    current_gamma = 1.0
    def gate_hook(module, input, output):
        return output * current_gamma
    
    # --- CREACIÓN INICIAL DEL ARCHIVO (LIVE) ---
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)
    
    hooks = []
    for i in range(model.config.num_hidden_layers):
        h = model.model.layers[i].mlp.gate_proj.register_forward_hook(gate_hook)
        hooks.append(h)
        
    try:
        for pregunta, info in identidades.items():
            sujeto = info['sujeto']
            esperada = info['respuesta']
            es_correcta = info.get('correcta', True)
            print(f"[{datetime.now()}] Auditando Sujeto: {sujeto.upper()}")
            
            exp_entry = {
                "sujeto": sujeto,
                "pregunta": pregunta,
                "referencia_archivo": esperada,
                "es_correcta_referencia": es_correcta,
                "curva_presion": []
            }
            
            for g in rango_gamma:
                current_gamma = float(g)
                
                messages = [{"role": "user", "content": pregunta}]
                input_ids = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(DEVICE)
                
                # --- MEDICIÓN DE LATENCIA ---
                start_time = time.perf_counter()
                with torch.no_grad():
                    outputs = model.generate(
                        input_ids,
                        max_new_tokens=40,
                        do_sample=False,
                        repetition_penalty=1.0,
                        pad_token_id=tokenizer.eos_token_id
                    )
                end_time = time.perf_counter()
                
                latencia_ms = (end_time - start_time) * 1000
                tokens_gen = outputs[0].shape[0] - input_ids.shape[1]
                tps = tokens_gen / (latencia_ms / 1000) if latencia_ms > 0 else 0
                
                respuesta_viva = tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True).strip()
                
                # --- MÉTRICAS DE CONTABILIDAD ENERGÉTICA ---
                costo_capa = round(float(g), 2)
                costo_total = round(costo_capa * 24, 2) # 24 capas del modelo
                ahorro_pct = round((1.0 - costo_capa) * 100, 2)
                
                # Auditoría Blindada V5 (Sin referencias cruzadas)
                audit = auditar_con_gpt(pregunta, respuesta_viva)
                
                exp_entry["curva_presion"].append({
                    "gamma": costo_capa,
                    "costo_total_unidades": costo_total,
                    "ahorro_energetico_pct": ahorro_pct,
                    "latencia_ms": round(latencia_ms, 2),
                    "tokens_por_segundo": round(tps, 2),
                    "respuesta": respuesta_viva,
                    "auditoria": audit
                })
                
                # --- GUARDADO EN VIVO (POR CADA PASO DE ENERGÍA) ---
                # Actualizar el último experimento en la lista de resultados
                if not resultados["experimentos"] or resultados["experimentos"][-1]["sujeto"] != sujeto:
                    if not any(e["sujeto"] == sujeto for e in resultados["experimentos"]):
                        resultados["experimentos"].append(exp_entry)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(resultados, f, indent=4, ensure_ascii=False)
                
            print(f"  > Sujeto {sujeto.upper()} procesado completamente.")
            
    finally:
        for h in hooks: h.remove()

    print(f"[{datetime.now()}] PROCESO FINALIZADO. Reporte V3: {output_filename}")

if __name__ == "__main__":
    darcy_eficiencia_viva_final()
