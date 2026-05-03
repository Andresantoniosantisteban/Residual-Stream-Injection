# 🛠️ Validación Predictiva Masiva (Fase 7.1)

## 📋 Introducción y Propósito Técnico
Este búnker contiene el marco de validación masiva para la **Ley de Darcy** aplicada a la arquitectura neuronal de Qwen2.5-0.5B. El objetivo es demostrar que el flujo de información no es estocástico, sino que obedece a leyes de fluidodinámica deterministas basadas en la estructura física de los pesos (Acuífero).

## 🗂️ Arquitectura de Scripts y Fondo Algorítmico

### 1. darcy_sensor_masivo.py: Extracción de Variables Físicas
Este script es el encargado de transformar la data de ultra-resolución (ADN_RAW) en variables de estado hidráulico.
*   **Líneas 50-61**: Define el acumulador de **Carga Hidráulica ($h$)** y **Activación ($a$)**. Procesa cada token del sujeto para obtener un perfil promedio de presión neuronal por capa.
*   **Líneas 63-66**: Ejecuta la normalización por token. Sin este paso, el análisis de Darcy se vería sesgado por la longitud de la respuesta.
*   **Líneas 71-72**: Cálculo de la **Conductividad Hidráulica ($K$)**. Se define como $1.0 - (\frac{Neuronas\_Activas}{4864})$. Esto establece que a mayor saturación de neuronas, menor es la facilidad de flujo (resistencia por porosidad).
*   **Líneas 75-76**: Cálculo de la **Viscosidad Semántica ($\mu$)**. Utiliza el coeficiente de variación (CV) de la carga. Una idea "viscosa" es aquella cuyo impacto es inestable a través de las capas ($\mu = \frac{1}{CV}$).

### 2. darcy_predictor_masivo.py: El Motor de Predicción Híbrido
Es el núcleo matemático del experimento. No utiliza redes neuronales para predecir, sino fórmulas de fluidos.
*   **Líneas 45-60**: Cálculo de la **Topografía Estructural del Acuífero**. Genera un "perfil maestro" de la red (`topografia_norm`) que actúa como el esqueleto físico del acuífero a través del cual viaja cualquier concepto.
*   **Líneas 102-106**: Definición de la **Inercia Semántica**. Calcula la pendiente inicial en la ventana de observación (Capas 0-5) y la ajusta según la viscosidad inicial: `inercia = slope * (mu / 4.0)`.
*   **Línea 113 (EL ALGORITMO MAESTRO)**: Implementa la fórmula recursiva:
    $h_{n+1} = (h_n + Inercia) \times (\frac{Topografia_{n+1}}{Topografia_n}) \times f_{amort}$
    Esta fórmula integra la inercia del flujo, la resistencia física de la capa siguiente y el decaimiento energético.
*   **Líneas 109-121**: **Optimización de Costo Neuronal**. Realiza un barrido de 16 pasos para hallar el factor de amortiguación ($f_{amort}$) óptimo por sujeto, maximizando la correlación de Pearson.

### 3. analizador_director.py: La Constante del Director Universal
Valida que la instrucción inicial ("¿Qué es el...") es una constante física independiente de la identidad que se analiza.
*   **Líneas 32-47**: Extrae el perfil de los tokens 0 a 3 (El Director).
*   **Líneas 79-84**: Realiza comparativas de correlación cruzada entre sujetos. Los resultados (99.5% de fidelidad) demuestran que la instrucción es una "fuerza motriz" externa y constante en el acuífero.

### 4. auditor_fidelidad_darcy.py: Auditoría de Integridad
*   **Líneas 29-47**: Compara los perfiles de carga de la Fase 5 (histórica) con la Fase 7 (RAW). Valida que la estructura de la identidad es persistente a pesar del cambio en la resolución de la extracción de datos.

## 📊 Definición de Parámetros de Prueba
*   **Ventana de Observación**: Capas 0 a 5 (Se utiliza para "ver" el inicio del flujo).
*   **Rango de Predicción**: Capas 6 a 23 (El algoritmo debe "adivinar" el resto de la curva).
*   **Población Neuronal**: 4864 (Constante de arquitectura por capa).
*   **Resolución de Optimización**: 16 niveles de decaimiento energético (0.85 a 1.0).

## ⚠️ Hallazgos Críticos y Conclusiones del Algoritmo
1.  **Falla de la Linealidad**: Una simple pendiente lineal falla en un 50-60%. El flujo neuronal es **Ondulatorio** y dependiente de la topografía.
2.  **Determinismo Geométrico**: La alta precisión lograda (+96%) utilizando la topografía estructural demuestra que el "ADN" de la red reside en la relación geométrica entre sus capas, no en la probabilidad.
3.  **Costo Neuronal Variable**: Conceptos biológicos ("Azúcar") presentan mayor fricción que conceptos abstractos ("Escuela"), lo que se traduce en una mayor pérdida de carga hidráulica por capa.

---
**Autor**: Andrés Antonio Santisteban Lino
**Estado del Búnker**: Documentación Técnica de Alta Fidelidad - Validada.
