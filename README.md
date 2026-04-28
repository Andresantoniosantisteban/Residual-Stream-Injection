Neural Identity Forge: Residual Stream Intervention & The Vector Rosetta Stone
Executive Summary
This repository contains the empirical data and core scripts of independent mechanistic interpretability research conducted on Qwen2.5-0.5B. By reverse-engineering the residual stream, this research maps the exact functional topology of latent feature representation, culminating in the discovery of the "Data Port" at Layer 12
.
The methodology transitions interpretability from passive observation to active "Data Pharmacology," demonstrating a 100% deterministic success rate in synthetic latent representation injection and exposing a critical architectural blind spot in LLM security filters
.
Key Empirical Discoveries
1. Structural Dominance (The Bus and Capsule Theory)
Quantitative analysis of the residual stream vector reveals that 99.65% of the vector energy is permanently dedicated to fixed structural infrastructure ("The Bus")
. The actual raw semantic data ("The Capsule") represents only 0.1% to 12.17% of the signal, peaking at Layer 23
.
2. The Crystallization Point
Entropy mapping across all 24 layers demonstrates an abrupt collapse in data entropy at Layer 20, where token purity instantaneously jumps from 0.02 to 0.36
. This marks the exact architectural threshold where the model cleanses its internal logic for output projection.
3. The Vector Rosetta Stone
By mathematically subtracting the 99% structural noise from the residual stream, the pure, isolated core vectors for digits (0-9) and 52 alphabetic characters (A-Z, a-z) were successfully extracted
. Case similarity analysis proves that uppercase and lowercase characters (e.g., 'A' vs 'a') share 98.4% of their vectorial signature, confirming empirically that the model processes high-level abstract concepts rather than visual or token-specific forms
.
4. Permeable Segmentation Law & Security Bypass
By synthetically injecting these pure signatures back into Layer 12, the model entirely ignores the original prompt context, achieving a 100% deterministic success rate (10/10) in overwriting perception
. Because this synthetic injection occurs mid-stream, it effectively bypasses initial attention-based security constraints. This triggers forced semantic hyper-associations (e.g., reliably hallucinating complex concepts like "Deng Xiaoping" solely from the isolated injection of the 'D' signature)
.
Repository Structure
This repository has been sterilized to include only the core reproducible artifacts of the Layer 12 bypass and the Rosetta Stone extraction:
/Data (Pure Vectors)
ALFABETO_NUMERICO_PURO.json & ALFABETO_LITERARIO_PURO.json: The isolated 896-dimensional coordinate dictionaries for numeric and alphabetic concepts
.
ESTRUCTURA_VS_DATO_RESULTADOS.json: Raw empirical log confirming the 99.65% structural overlap
.
MASTER_PROMPTS.json: The purified baseline control dataset used for all tests
.
/Core_Scripts (Intervention)
24_ESTRUCTURA_VS_DATO.py: Quantifies the Process-to-Data ratio in the residual stream
.
28_EXTRACCION_DEL_IDIOMA_PURO.py: The triple-decomposition script used to isolate the core semantic vector from the structural wrapper
.
30_HACK_DE_REALIDAD_SINTETICA.py: The primary latent injection tool for overwriting model perception at Layer 12
.
36_INDUSTRIALIZACION_ALFABETO.py: Automated pipeline for massive token-DNA extraction
.
Replication and Verification
All findings rely strictly on deterministic execution (temperature: 0.0, do_sample: false) without sampling noise
. The provided JSON datasets and intervention scripts allow for immediate verification of the Layer 12 security bypass and the structural isolation theories.
Note: This research operates outside of traditional academia, applying strict mechanistic interpretability protocols to demonstrate latent space vulnerabilities.


The Organic Organization Theory
This architecture was not explicitly programmed; it organized itself organically through mathematical optimization (finding the path of least resistance to minimize loss).
Layers 0-11 (The Organic Database): Act as chaotic data searchers and feature extractors.
Layers 12-23 (The Output Nozzle): Act as strict formatters and structural processors.
Because this organization is organic rather than perfectly compartmentalized, the network exhibits Permeable Segmentation. This permeability is precisely why synthetic latent injections at Layer 12 organically bleed into the surrounding semantic memory, causing forced hallucinations without breaking the output structure.
Lead Researcher: Andres Santisteban Consolidation Date: April 28, 2026 "The reality of the model is no longer what it reads, but what we inject into its residual stream."

