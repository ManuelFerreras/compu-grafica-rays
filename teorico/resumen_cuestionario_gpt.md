# 🧠 Defensa Oral – Ray Project (UCC)

## 🟢 MODELO DE COLOR
Usamos el modelo **RGB (Red, Green, Blue)** con canal alfa (**RGBA**).  
Las pantallas emiten luz, y los píxeles combinan estos tres colores primarios.  
- (1,1,1) → blanco  
- (0,0,0) → negro  
- (1,0,0) → rojo, etc.

👉 En el proyecto, todos los colores (en shaders y texturas) están definidos en RGB.

---

## 🟢 PRIMITIVAS GRÁFICAS
Trabajamos con **triángulos**:
- Un **Quad** se forma con 2 triángulos.  
- Un **Cube**, con 12 (2 por cada cara).  
Los triángulos son la unidad mínima que entiende la GPU.

---

## 🟢 PRODUCTO ESCALAR Y VECTORIAL
- **Producto Escalar:** da un número (float).  
  Se usa para medir ángulos entre vectores o calcular iluminación difusa (`dot(normal, lightDir)`).

- **Producto Vectorial:** da un vector perpendicular a los otros dos.  
  Se usa para calcular **normales** o crear bases ortogonales.

---

## 🟢 COORDENADAS HOMOGÉNEAS
- Puntos → `w = 1` (se afectan por traslaciones).  
- Direcciones → `w = 0` (no se trasladan).  
👉 En nuestro motor, esto se usa en las matrices `model`, `view`, `projection`.

---

## 🟢 MATRICES DE TRANSFORMACIÓN
Usamos **matrices 4x4** para trabajar en 3D con coordenadas homogéneas.

| Matriz | Uso |
|---------|-----|
| **Model** | Posiciona el objeto en la escena. |
| **View** | Define la cámara y su orientación. |
| **Projection** | Crea la perspectiva. |
| **Inverse View** | Convierte rayos de cámara a mundo. |

👉 Ejemplo: al trazar un rayo, lo transformamos con la inversa de la matriz de vista.

---

## 🟢 ESPACIOS DE COORDENADAS
| Espacio | Significado |
|----------|--------------|
| **Objeto** | Local del objeto (centro 0,0,0). |
| **Mundo** | Coordenadas globales compartidas por todos. |
| **Vista** | Coordenadas desde la cámara. |

---

## 🟢 NDC (Normalized Device Coordinates)
Después de proyectar, los puntos se escalan entre **[-1, 1]**.  
Esto permite unificar la escena sin importar el tamaño de pantalla.

---

## 🟢 PERSPECTIVA vs ORTOGRÁFICA
- **Perspectiva:** objetos lejanos se ven más chicos (realista).  
- **Ortográfica:** mantiene tamaño constante (como planos técnicos).  
👉 Usamos **perspectiva** en el Ray Project.

---

## 🟢 BUFFERS Y ORGANIZACIÓN DE DATOS
| Elemento | Función |
|-----------|----------|
| **VBO** | Guarda vértices. |
| **IBO** | Guarda índices (orden de dibujo). |
| **VAO** | Vincula buffers con el shader. |

En `graphics.py`, todo esto se gestiona automáticamente.

---

## 🟢 SHADERS
- **Vertex Shader:** se ejecuta por vértice → transforma posiciones.  
- **Fragment Shader:** se ejecuta por píxel → calcula color final.  
- **Compute Shader:** trabaja en grupos paralelos, no dibuja geometría (lo usamos para el Raytracing GPU).

---

## 🟢 UNIFORMS vs ATRIBUTOS
- **Uniforms:** valores globales iguales para todos los vértices/píxeles (por ejemplo, la luz).  
- **Atributos:** varían por vértice (posición, color, normal).

---

## 🟢 TEXTURAS Y SAMPLER2D
Un **sampler2D** es una textura leída por coordenadas UV.  
En nuestro proyecto, el Quad usa una textura generada por el raytracer.

---

## 🟢 MATRICES EN EL PROYECTO
Aparecen en:
- `Cube.get_model_matrix()`
- `Camera.get_view_matrix()` y `get_projection_matrix()`

---

## 🟢 RAYOS EN EL PROYECTO
Se trazan desde la **posición de la cámara**:
- En **Raycasting:** hacia el mouse.  
- En **Raytracing:** hacia cada píxel.

---

## 🟢 HITBOX
La clase `HitBox` detecta colisiones con el método **Slab**.  
En GPU y CPU, nos dice si el rayo “choca” con un objeto.

---

## 🟢 PYTHON Y LIBRERÍAS
- **Pyglet:** crea ventana, loop y eventos (mouse/teclado).  
- **ModernGL:** maneja shaders, buffers y texturas en OpenGL moderno.

---

## 🟢 MODELO Y MATERIALES
- `Model` → define geometría (vértices, índices, normales, colores).  
- `Material` → conecta shaders con texturas.  
- `Texture` → maneja imágenes y las pasa a bytes con `get_bytes()`.

---

## 🟢 RAYCASTING vs RAYTRACING

| Característica | Raycasting | Raytracing |
|----------------|-------------|------------|
| Objetivo | Detectar colisiones | Simular luz y color |
| Resultado | Booleano / ID de objeto | Color del píxel |
| Ejemplo | Clic en cubo | Renderizado 3D |

👉 En tu proyecto:  
- **F1 → Normal:** Raycasting (detecta cubo).  
- **F2 → CPU:** Raytracing por software.  
- **F3 → GPU:** Raytracing con shaders.

---

## 🟢 QUAD Y ESCENA
El **Quad** es una “pantalla virtual” donde pintamos la textura generada por el Raytracer.  
No es hittable (no colisiona con rayos).

---

## 🟢 SKY COLOR
En CPU: `Camera.set_sky_colors(top, bottom)` define el gradiente del cielo.  
En GPU: se pasa como **uniform vec3** al shader.

---

## 🟢 CPU vs GPU RAYTRACER
- **CPU:** genera `ImageData` con NumPy, píxel por píxel.  
- **GPU:** usa shaders para calcular todos los rayos en paralelo.  
👉 GPU = mucho más rápido y en tiempo real.

---

## 🟢 COMPUTE SHADER Y SSBO
- **Compute Shader:** programa que corre en GPU de forma general.  
- **SSBO (Shader Storage Buffer Object):** buffer para enviar estructuras grandes (matrices, materiales, etc.).  
  Se declaran con `layout(binding=X) buffer`.

El **binding** es más importante que el nombre: define el slot de memoria.

---

## 🟢 VARIABLES CLAVE EN GPU
| Variable | Contenido | Uso |
|-----------|------------|-----|
| `models_f` | Model matrices | Transformar objetos |
| `inv_f` | Inversas de matrices | Transformar rayos |
| `mats_f` | Materiales | Colores y reflectividad |
| `primitives` | Geometrías | Estructura del BVH |

---

## 🟢 BVH (Bounding Volume Hierarchy)
Estructura jerárquica para acelerar colisiones.  
Permite **descartar grupos** de objetos que no están en la trayectoria del rayo.  
👉 Sin BVH, cada rayo debería testear todos los objetos.

---

## 🟢 ILUMINACIÓN
- **Luz Ambiental:** ilumina todo un poco (evita negros absolutos).  
- **Luz Difusa:** depende del ángulo entre luz y superficie (efecto Lambert).  
- **Luz Especular:** genera reflejos brillantes (como en metales o vidrio).  

👉 En tu proyecto, la luz se mueve con click derecho.

---

## 🟢 PATH TRACING (solo teórico)
Es una extensión del Raytracing.  
Cada rayo rebota varias veces (reflexiones y refracciones).  
Más rebotes → más realismo, pero menor rendimiento.  
Nuestro proyecto usa **hasta 3 rebotes**, lo que da equilibrio entre rendimiento y calidad.

---

## 🟢 REFLECTIVIDAD
| Valor | Significado |
|--------|--------------|
| 1.0 | Espejo perfecto (refleja todo) |
| 0.0 | Mate (absorbe toda la luz) |

---

## 🟢 DIFERENCIA AABB vs OBB
| Tipo | Descripción |
|------|--------------|
| **AABB** | Caja alineada a los ejes del mundo. No rota. |
| **OBB** | Caja rotada según el objeto. Más precisa, más costosa. |

En el proyecto, `HitBoxOBB` transforma el rayo al espacio local del objeto.

---

## 🟢 FRASE DE CIERRE (defensa)
> “Nuestro proyecto implementa todo el pipeline de Computación Gráfica, desde el Raycasting hasta el Raytracing en GPU, usando Pyglet y ModernGL. Maneja colisiones AABB y OBB, aplica iluminación difusa y ambiental, y tiene mejoras interactivas con cámara libre y luz dinámica.”

---

## ✅ CONCLUSIÓN
- Domina teoría + práctica.  
- Los tres modos (`normal`, `cpu`, `gpu`) funcionan correctamente.  
- Explicaciones claras, defendibles y conectadas con el código real.
