# Proyecto Parcial Computacion Grafica

**Integrantes:**  
- Manuel Ferreras – 2319258  
- Matías Carbel – 2319266  

---

## Descripción

Proyecto grupal para la materia **Computación Gráfica**.  
Implementa un motor visual en Python con **Pyglet**, **ModernGL**, **NumPy** y **PyGLM**, abarcando desde **Raycasting** hasta **Raytracing por GPU**.  

Incluye una mejora grupal con **luz direccional dinámica** y **cámara libre (WASD + Q/E)**.

---

## Controles

- **W / S / A / D:** mover cámara  
- **Q / E:** subir o bajar  
- **Click derecho:** mover luz  
- **Click derecho + arrastrar:** rotar cámara  
- **Click izquierdo:** seleccionar objetos  
- **ESC:** salir  

---

## Ejecución

```bash
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install pyglet moderngl numpy PyGLM

python main.py
