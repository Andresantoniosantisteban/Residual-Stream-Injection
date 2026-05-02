# 🌊 Protocolo de Investigación: Ley de Darcy en la Red Neuronal

Este documento establece la base teórica y experimental para aplicar la **Ley de Darcy** ($Q = -K \cdot A \cdot \frac{dh}{dl}$) al flujo de información en el modelo Qwen2.5-0.5B. El objetivo es determinar si la "Identidad" se comporta como un fluido físico atravesando un medio poroso.

---

## 📐 1. El Gradiente Hidráulico ($dh/dl$) - La Pendiente Semántica

En geología, es la pérdida de energía potencial por unidad de longitud. En nuestra red:
*   **Carga Hidráulica ($h$)**: Definida como la **Intensidad de Activación Neta** (suma de magnitudes de impacto) de un concepto en una capa específica.
*   **Longitud ($l$)**: La distancia física entre capas (incrementos de 1 en la profundidad del modelo).
*   **El Gradiente**: Representa la **tasa de disipación de energía**. 
    *   Un gradiente alto indica que la red está haciendo un gran "esfuerzo" por filtrar o transformar la idea. 
    *   Un gradiente bajo indica que la idea fluye sin resistencia, sugiriendo una ruta de procesamiento altamente eficiente.

---

## 🪨 2. Conductividad Hidráulica ($K$) - La Propiedad del Suelo (Pesos)

La conductividad depende de la facilidad con la que el medio permite el paso del fluido.
*   **El Sedimento de Datos**: Durante el pre-entrenamiento, los datos se "sedimentan" en los pesos del modelo. 
*   **Saturación del Suelo**: Consideraremos que las neuronas con alta densidad de activación actúan como **"suelos compactados"** (baja conductividad), mientras que las zonas de "Hiatos" o silencio actúan como **"canales de drenaje"** (alta conductividad).
*   **Hipótesis de Clumping**: Si el entrenamiento ha unido segmentos de datos de forma muy densa, la conductividad será baja, forzando al fluido (la activación) a buscar caminos alternativos o a aumentar su presión.

---

## 🍯 3. Viscosidad Semántica ($\mu$) - La Resistencia del Fluido

Esta es la propiedad intrínseca de la "idea" misma, independiente del suelo que atraviese.
*   **Definición**: La resistencia interna al flujo.
*   **Experimento de Comparación**:
    *   **Viscosidad Baja (Agua)**: Conceptos como "Sol" o "Fuego". Son ideas primarias, energéticas y rápidas de procesar. Esperamos que su flujo sea directo y su dispersión fractal sea limpia.
    *   **Viscosidad Alta (Aceite/Miel)**: Conceptos complejos o abstractos. Tienen más "cuerpo" semántico y se resisten a la transformación, "pegándose" a las capas y requiriendo más profundidad para cristalizar.
*   **Interacción de Fluidos**: Al igual que el agua y el aceite no se mezclan, conceptos con viscosidades muy diferentes deberían mostrar **fronteras de exclusión** más marcadas en el espacio latente.

---

## 🔬 Metodología de Ataque

Para validar estos tres puntos, realizaremos las siguientes mediciones sobre el archivo `ADN_TOTAL_IDENTIDADES.json`:

1.  **Cálculo de Caudal ($Q$)**: Suma total de activación transmitida entre la Capa $N$ y la Capa $N+1$.
2.  **Mapeo de Resistencia ($R = 1/K$)**: Identificar las capas que bloquean el flujo y causan "embalses" de presión semántica.
3.  **Test de Viscosidad Comparada**: Contrastar los perfiles de flujo de "Gato" vs "Sol" para ver si la "densidad" del concepto altera la velocidad de sedimentación.

---
**Autor**: Neural Identity Forge - Investigación de Geología Neuronal
**Fecha**: 2026-05-02
**Estatus**: Protocolo de Fase 5.1 (Pendiente de Ejecución)
