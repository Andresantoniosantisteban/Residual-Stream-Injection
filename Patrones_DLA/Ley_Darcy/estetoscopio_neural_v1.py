import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import time
import json
import pandas as pd
from datetime import datetime

# Protocolo Andrés: Nomenclatura con marca de tiempo
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M")

# Configuración de Hardware
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_PATH = "Qwen/Qwen2.5-0.5B"

print(f"Cargando Estetoscopio de Alta Resolución en {DEVICE}...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH).to(DEVICE)

# Almacén de mediciones
mediciones_raw = []

def stethoscope_hook(layer_idx):
    def hook(module, input, output):
        torch.cuda.synchronize() # Sincronización para latencia real de GPU
        timestamp = time.perf_counter()
        caudal = torch.norm(output, p=2).item()
        
        mediciones_raw.append({
            "capa": layer_idx,
            "caudal": round(caudal, 4),
            "timestamp": timestamp
        })
    return hook

# Instalar Sensores
hooks = []
for i in range(model.config.num_hidden_layers):
    h = model.model.layers[i].mlp.gate_proj.register_forward_hook(stethoscope_hook(i))
    hooks.append(h)

def escanear_sujeto(nombre, pregunta):
    global mediciones_raw
    mediciones_raw = []
    
    print(f"Escaneando {nombre}...")
    inputs = tokenizer(pregunta, return_tensors="pt").to(DEVICE)
    
    with torch.no_grad():
        model.generate(**inputs, max_new_tokens=1, do_sample=False)
        torch.cuda.synchronize()

    df = pd.DataFrame(mediciones_raw)
    df['latencia_codo_ms'] = df['timestamp'].diff() * 1000
    df.at[0, 'latencia_codo_ms'] = 0 
    return df

# Ejecución de Mapeo
sujetos = [
    {"nombre": "GATO_FLUIDO", "pregunta": "¿Cuántas patas tiene un gato?"},
    {"nombre": "CABALLO_OBSTRUIDO", "pregunta": "¿Cuántas patas tiene un caballo?"},
    {"nombre": "ARBOL_OBSTRUIDO", "pregunta": "¿Qué es un árbol?"}
]

dict_resultados = {}
writer = pd.ExcelWriter(f"{TIMESTAMP}_mapeo_codos_darcy.xlsx", engine='openpyxl')

for s in sujetos:
    df = escanear_sujeto(s['nombre'], s['pregunta'])
    dict_resultados[s['nombre']] = df.to_dict(orient='records')
    df.to_excel(writer, sheet_name=s['nombre'], index=False)
    print(f" - {s['nombre']} completado.")

# Guardar Resultados
writer.close()
with open(f"{TIMESTAMP}_mapeo_codos_darcy.json", "w", encoding='utf-8') as f:
    json.dump({
        "timestamp": TIMESTAMP,
        "autor": "Andrés Antonio Santisteban Lino",
        "metodo": "Estetoscopio Neural V1",
        "datos": dict_resultados
    }, f, indent=4, ensure_ascii=False)

# Limpieza
for h in hooks:
    h.remove()

print(f"\nReportes generados exitosamente:")
print(f" - {TIMESTAMP}_mapeo_codos_darcy.json")
print(f" - {TIMESTAMP}_mapeo_codos_darcy.xlsx")
