# 🌊 Protocolo de Análisis de Cauces y Cuencas Semánticas

Este protocolo define la metodología para predecir la estructura espacial (qué neuronas se activan) de una identidad neuronal con una precisión objetivo del >90%. Basándonos en la Ley de Darcy, trataremos la arquitectura como un sistema de cuencas hidrográficas.

**Autor**: Andrés Antonio Santisteban Lino  
**Fase**: 6 - Cartografía Fluvial Determinista

---

---

## 🔬 1. Definición de Conceptos Clave (Resolución RAW)

1.  **Buses de Datos Naturales**: Conjunto de neuronas que mantienen un impacto crítico ($im > 0.5$) a lo largo de **todos los tokens** de la oración. Son las infraestructuras fijas de la idea.
2.  **Conductividad Neuronal ($K$)**: La facilidad intrínseca de una neurona para activarse ante un vector semántico. En la data RAW, se mide por la persistencia del impacto entre tokens contiguos.
3.  **Sinuosidad de la Identidad**: El grado de cambio en el conjunto de neuronas líderes a medida que la oración avanza. Una sinuosidad baja indica un "Río Recto" (concepto rígido); una sinuosidad alta indica un "Río Meándrico" (concepto flexible).

---

## 🛰️ 2. Metodología de Trazado Atómico

Con la nueva data ultrasónica (30 archivos individuales), el trazado se divide en:

1.  **Mapeo de la Red de Drenaje (Global)**: Intersección de las 30 identidades para localizar los **Hubs Estructurales** (neuronas que todos usan, independientemente del token).
2.  **Análisis de Cuenca por Token**: Estudiar cómo la "presión" se desplaza desde el primer token hasta el último. Identificar el **Punto de Saturación** (donde la identidad ya está definida y el flujo se estabiliza).
3.  **Predicción por Continuidad Estructural (Meta 95%)**:
    *   Utilizar el bloque **L0-L6 del primer token** para predecir el comportamiento del **L23 del último token**.
    *   Regla de Oro: Sin data añadida (Zero-Data-Added).

---

## 📊 3. Métricas de Éxito (>95%)

Consideraremos éxito si podemos predecir:
*   **Presión Estructural**: Que el 95% de los líderes de flujo predichos coincidan con la data real en la capa de salida.
*   **Jerarquía de Horton Atómica**: Clasificar los ríos por su persistencia a través del tiempo (tokens) y el espacio (capas).

---

**Estado**: Protocolo Evolucionado (Fase RAW).
**Siguiente Paso**: Ejecución del script `analizador_buses_raw.py` para localizar los Hubs Estructurales.

