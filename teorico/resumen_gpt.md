# 🧠 Defensa Oral – Ray Project (UCC)

## 🔹 ¿Qué es un **rayo (Ray)**?
Es una ecuación paramétrica que describe una línea en el espacio 3D:

\[
P(t) = O + t \cdot D
\]

donde:  
- **O** = origen del rayo  
- **D** = dirección normalizada  
- **t** = distancia a lo largo del rayo  

Se usa para detectar qué objetos son “vistos” desde la cámara o impactados por clics del usuario.

---

## 🔹 ¿Qué es **Raycasting**?
Es el proceso de lanzar rayos desde la cámara o desde el mouse para detectar colisiones.  
Sirve para saber **qué objeto fue clickeado o visible**.  
👉 En nuestro proyecto, el modo *normal* (Raycasting) imprime en consola el nombre del cubo tocado.

---

## 🔹 ¿Qué es **Raytracing**?
Extiende el Raycasting:  
Cada píxel lanza un rayo para calcular su **color** según las intersecciones con objetos y la luz.  

### Versiones:
- **CPU:** el cálculo se hace en Python (más lento, pero exacto).  
- **GPU:** el cálculo se hace dentro del shader GLSL (mucho más rápido, en tiempo real).

---

## 🔹 Diferencia CPU vs GPU

| CPU | GPU |
|------|------|
| Calcula cada rayo secuencialmente | Miles de rayos en paralelo |
| Muy preciso, pero lento | Muy rápido, ideal para render en tiempo real |
| Control total desde Python | Control delegado al shader |

---

## 🔹 ¿Qué es una **AABB**?
**Axis-Aligned Bounding Box**  
Caja delimitadora alineada a los ejes X/Y/Z.  
Se usa para detectar colisiones rápidas: los lados no rotan con el objeto.

---

## 🔹 ¿Y una **OBB**?
**Oriented Bounding Box**  
Caja rotada junto con el objeto.  
Se obtiene aplicando la **inversa de la `model_matrix`** al rayo antes de hacer el test.  
✅ En este proyecto, las colisiones rotan correctamente con los cubos.

---

## 🔹 ¿Qué es el **Slab Method**?
Es el método matemático usado para la intersección **Rayo–Caja**.  
Divide el espacio en planos paralelos (slabs) y calcula:
- `tmin` = entrada del rayo al volumen  
- `tmax` = salida del rayo  

Si `tmin < tmax` → el rayo toca la caja.

---

## 🔹 ¿Qué son las matrices **Model / View / Projection**?

| Matriz | Función |
|---------|----------|
| **Model** | Transforma el objeto desde su espacio local al mundo |
| **View** | Define la posición y orientación de la cámara |
| **Projection** | Aplica la perspectiva (campo visual y profundidad) |
| **Inverse View** | Transforma rayos desde cámara a mundo (para raytracing) |

---

## 🔹 ¿Qué hace el **shader fragment** en modo GPU?
Por cada píxel:
1. Calcula la dirección del rayo.  
2. Intersecta con todos los objetos.  
3. Si hay impacto → calcula el color según la luz (modelo Lambert).  
4. Si no hay impacto → pinta el color del cielo (gradiente).

---

## 🔹 Extensión grupal desarrollada
- **Luz direccional dinámica** (click derecho para moverla).  
- **Cámara libre** (WASD + Q/E) con rotación por mouse.  

Estas mejoras permiten manipular la escena en tiempo real y ver el efecto de la iluminación sobre los objetos.

---

## 🔹 Controles importantes

| Acción | Tecla / Mouse |
|--------|----------------|
| W / S / A / D | mover cámara |
| Q / E | subir o bajar |
| Click derecho | mover la luz |
| Click derecho + arrastrar | rotar cámara |
| Click izquierdo | raycasting (seleccionar cubo) |
| F1 / F2 / F3 | cambiar modo (normal / cpu / gpu) |
| ESC | salir |

---

## 🔹 Frase final para la defensa
> “El proyecto implementa todo el pipeline completo desde Raycasting hasta Raytracing en GPU, con detección de colisiones AABB y OBB, shading Lambertiano y extensiones interactivas de cámara y luz dinámica.”

---

## 🧩 Modo de presentación (según consignas)
- Tener el proyecto abierto el día de la evaluación.  
- Probar los tres modos:
  - **F1:** Normal (Raycasting)  
  - **F2:** CPU (Raytracer software)  
  - **F3:** GPU (Raytracer tiempo real)
- Mostrar la consola con los logs de colisiones.

---

## ✅ Resultado final
Proyecto completo, modular y funcional:
- Cumple con todas las etapas del parcial (1 a 5).  
- Incluye mejora grupal válida.  
- Listo para la entrega y defensa oral.
