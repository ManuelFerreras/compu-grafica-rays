# 📂 Estructura general

```
ray_project/
├── main.py
├── window.py
├── scene_normal.py
├── scene_cpu.py
├── scene_gpu.py
├── camera.py
├── ray.py
├── hit.py
├── cube.py
├── model.py
├── texture.py
├── material.py
├── graphics.py
├── quad.py
├── raytracer.py
└── shaders/
    ├── sprite.vert
    ├── sprite.frag
    ├── raytracing.vert
    └── raytracing.frag
```

---

# `main.py`

### ¿Qué hace?

Punto de entrada. Crea la ventana, la cámara y carga **una** de las escenas (`normal`, `cpu`, `gpu`).

### Bloques importantes

* **Constante `SCENE_TYPE`**

  ```python
  SCENE_TYPE = "gpu"
  ```

  * Selecciona el modo de evaluación requerido por el profe.
  * Cambiás a `"normal"` o `"cpu"` para probar cada etapa.

* **Creación de ventana y cámara**

  ```python
  win = AppWindow(...)
  cam = Camera()
  ```

  * `AppWindow` encapsula Pyglet + ModernGL.
  * `Camera` mantiene matrices y estado (posición, yaw/pitch).

* **Selector de escena**

  ```python
  if SCENE_TYPE == "normal": from scene_normal import SceneNormal; scene = SceneNormal(cam)
  elif SCENE_TYPE == "cpu":  from scene_cpu import SceneCPU;       scene = SceneCPU(cam)
  elif SCENE_TYPE == "gpu":  from scene_gpu import SceneGPU;       scene = SceneGPU(cam)
  ```

  * **Import diferido**: sólo importamos lo que vamos a usar.
  * Pasamos **la misma** `Camera` a cualquier escena.

* **Seteo & loop**

  ```python
  win.set_scene(scene)
  pyglet.app.run()
  ```

  * `set_scene` configura ModernGL en la escena y llama a `start()`.
  * `pyglet.app.run()` inicia el loop de eventos.

---

# `window.py` (App Window + switch F1/F2/F3)

### ¿Qué hace?

Ventana de Pyglet + contexto ModernGL. Maneja input, resize y hot-swap de escenas.

### Bloques importantes

* **Contexto GL y teclado**

  ```python
  self.ctx = moderngl.create_context()
  self.keys = key.KeyStateHandler()
  self.push_handlers(self.keys)
  ```

  * Crea el contexto **OpenGL**.
  * KeyState para **WASD/QE** continuo.

* **`set_scene(scene)`**

  ```python
  self.scene = scene
  self.scene.ctx = self.ctx
  self.scene.start()
  self.scene.on_resize(self.width, self.height)
  ```

  * Enlaza el **contexto GL** a la escena.
  * **Orden correcto**: `start()` (crea recursos) → `on_resize()` (ajusta viewport y matrices).

* **`_switch_scene(mode)`**

  ```python
  cam = self.scene.camera if (...) else Camera()
  new_scene = SceneNormal/SceneCPU/SceneGPU(cam)
  self.set_scene(new_scene)
  self.set_caption(...)
  ```

  * **Reusa la misma cámara** al cambiar de modo.
  * Cambia el título para que el profe vea el modo activo.

* **`on_draw()`**

  ```python
  self.ctx.clear(*self.clear_color)
  self.scene.render()
  ```

  * Limpia el framebuffer y delega el dibujo a la escena.

* **`update(dt)`**

  ```python
  if (WASD/QE presionadas) and hasattr(camera.move): camera.move(...)
  self.scene.update(dt)
  ```

  * Movimiento de cámara **si la escena lo soporta**.
  * Llama `update` para animaciones.

* **`on_key_press(F1/F2/F3)`**

  * Cambia **en vivo** entre modos de escena.

* **`on_mouse_press/drag`**

  * Normaliza a `u=x/width`, `v=y/height` para raycasting/luz.
  * Botón derecho + drag: `camera.look(dx, -dy)`.

---

# `camera.py`

### ¿Qué hace?

Mantiene FOV, aspecto, matrices **view/projection** e inversa. Mueve y rota la cámara. Genera rayos.

### Funciones y líneas clave

* **Constructor**

  ```python
  self.position = vec3(0,1,3); self.target = vec3(0,1,0); self.up = vec3(0,1,0)
  self.yaw = -90.0; self.pitch = 0.0
  self.view = glm.lookAt(self.position, self.target, self.up)
  self.proj = glm.perspective(radians(fov), aspect, near, far)
  self.inv_view = glm.inverse(self.view)
  ```

  * Setup **FPS-like** (mirando -Z).
  * Guardamos la **inversa** para transformar rayos (cámara→mundo).

* **`update_matrices()`**

  ```python
  forward = normalize(vec3(cos(yaw)*cos(pitch), sin(pitch), sin(yaw)*cos(pitch)))
  self.target = self.position + forward
  self.view   = glm.lookAt(self.position, self.target, self.up)
  self.proj   = glm.perspective(...)
  self.inv_view = glm.inverse(self.view)
  ```

  * Recalcula matrices tras mover/rotar.

* **Cielo**

  ```python
  set_sky_colors(top, bottom)
  get_sky_gradient(h)  # interpola entre bottom-top
  ```

  * Para el **fondo** en normal/CPU.

* **`raycast(u,v)`**

  ```python
  x_ndc = 2u-1; y_ndc = 2v-1
  dir_cam = normalize(vec3(x_ndc*aspect*tan(fov/2), y_ndc*tan(fov/2), -1))
  dir_world = normalize(mat3(inv_view) * dir_cam)
  return Ray(position, dir_world)
  ```

  * Convierte **coordenadas de pantalla** en **rayo en mundo**.

* **Movimiento / Mirada**

  ```python
  move(forward_amt, right_amt, up_amt, dt)  # WASD/QE
  look(dyaw, dpitch)                        # mouse
  ```

  * `forward` plano XZ, `right = cross(forward, up)`.

---

# `ray.py`

### ¿Qué hace?

Representa un **rayo** con origen y dirección **normalizada**.

### Bloques importantes

* **Encapsulación**

  ```python
  self.__origin, self.__direction
  @property def origin/direction ...
  ```

  * Mantiene invariante: la dirección siempre está normalizada.

* **Ecuación del rayo**

  ```python
  P(t) = origin + t * direction
  ```

  * Usada conceptualmente en intersecciones.

---

# `hit.py`

### ¿Qué hace?

Define el **resultado** de un hit y las **cajas** (AABB/OBB) para colisiones.

### Clases y líneas clave

* **`HitResult`**

  ```python
  hit: bool; t_near: float; t_far: float
  ```

  * si `hit==True`, `t_near` es la entrada del rayo.

* **`HitBox` (AABB)**

  ```python
  check_hit(origin, direction):
      # método de los Slabs
      for axis in x, y, z:
          if direction[axis] ≈ 0: fuera? → miss
          else: t1, t2 = (min-max - origin)/direction
                tmin = max(tmin, min(t1,t2))
                tmax = min(tmax, max(t1,t2))
      hit = tmax >= max(tmin, 0)
  ```

  * **Slab Method**: intersección con planos paralelos por eje.

* **`HitBoxOBB` (caja orientada)**

  ```python
  # obtener invM del objeto
  oL = invM * origin
  pL = invM * (origin + direction)
  dL = normalize(pL - oL)
  # aplicar Slabs en espacio LOCAL
  ```

  * Transformamos el rayo al **espacio local** → la caja vuelve a ser **AABB**.

---

# `cube.py`

### ¿Qué hace?

Modelo simple + hitbox OBB.

### Bloques importantes

* **Estado transform**

  ```python
  position, rotation(x,y,z), scale
  ```

* **`get_model_matrix()`**

  ```python
  T = translate(position)
  R = rotX * rotY * rotZ
  S = scale(scale)
  M = T * R * S
  ```

  * Orden típico **TRS**.

* **`check_hit(origin, direction)`**

  ```python
  self.hitbox.check_hit(origin, direction)
  ```

  * Delega en **AABB** o **OBB** según la implementación.

---

# `model.py`

### ¿Qué hace?

Abstracción de malla (vértices, layout). Sirve para `Cube`/`Quad` si lo usás para GPU tradicional.

### Bloques importantes

* **`Vertex` / `VertexLayout`**

  * Estructuras para VBO/VAO: posición, normal, uv.

* **`Model`**

  * Administra buffers, draw call (si hubieras hecho raster tradicional).

> En este proyecto renderizamos por **Raytracing**, así que `Model` es de soporte y para el **Quad**.

---

# `texture.py`

### ¿Qué hace?

Maneja imágenes en **CPU** y su conversión a bytes para la **GPU**.

### Bloques importantes

* **`ImageData(w,h,channels=3)`**

  ```python
  self.pixels = np.zeros((h, w, channels), dtype=np.uint8)
  ```

  * Buffer CPU que llenamos desde el **RayTracer**.

* **`get_bytes()`**

  ```python
  return self.pixels.tobytes(order="C")
  ```

  * Lo sube **Graphics** a una textura OpenGL.

---

# `material.py`

### ¿Qué hace?

Agrupa **shaders** + **texturas** + **uniforms**.
(En este pipeline lo usamos poco porque pintamos con shaders especializados de ray).

---

# `graphics.py`

### ¿Qué hace?

Capa de **ModernGL**: carga shaders, crea **quad fullscreen** y permite actualizar **textura**.

### Bloques importantes

* **`load_program_from_files(vs_path, fs_path)`**

  ```python
  v_src = open(vs).read(); f_src = open(fs).read()
  self.prog = self.ctx.program(vertex_shader=v_src, fragment_shader=f_src)
  ```

  * Compila y linkea **GLSL**.

* **`create_fullscreen_quad()`**

  ```python
  # Vertex buffer con dos triángulos que cubren la pantalla
  in_pos: (-1,-1),(1,-1),(1,1), (-1,-1),(1,1),(-1,1)
  in_uv:  (0,0),(1,0),(1,1), (0,0),(1,1),(0,1)
  self.vao = self.ctx.vertex_array(self.prog, [(vbo, "2f 2f", "in_pos","in_uv")])
  # Crea textura 2D vacía que luego se actualiza
  self.texture = self.ctx.texture((2,2), components=3)
  ```

  * El **quad** es donde mostramos la textura (sea CPU o GPU).

* **`update_texture(w, h, bytes_ )`**

  ```python
  if size cambió -> recrea texture
  texture.write(bytes_)
  ```

  * Sube el **frame** generado por CPU **o** cualquier imagen.

* **`draw()`**

  ```python
  if self.texture in prog: bind(0); set sampler uniform; self.vao.render()
  ```

  * Dibuja el quad con la textura activa.

---

# `quad.py`

### ¿Qué hace?

Ayudante para crear la geometría del **quad** (si lo usás fuera de `Graphics`).

---

# `raytracer.py` (CPU)

### ¿Qué hace?

Genera, por **CPU**, la imagen píxel a píxel (lento pero exacto) y la devuelve como `ImageData`.

### Bloques importantes

* **Constructor**

  ```python
  self.camera = camera
  self.objects = objects
  ```

* **`render(width, height)`**

  ```python
  img = ImageData(width, height, 3)
  for j in range(height):
    for i in range(width):
       u = (i+0.5)/width; v = (j+0.5)/height
       ray = camera.raycast(u,v)
       color = self.trace(ray)
       img.pixels[j,i,:] = (color*255).astype(np.uint8)
  return img
  ```

  * **Muestreo** centro del píxel.
  * **Gamma**: simple/clamp (según versión).

* **`trace(ray)`**

  ```python
  # testea contra todos los objetos
  # si impacta → color rojo (versión mínima) o shading básico
  # si no → color de cielo (camera.get_sky_gradient(dir.y))
  ```

  * Aquí está la **lógica** de colisiones y color (simplificada vs GPU).

---

# `scene_normal.py` (modo **NORMAL**)

### ¿Qué hace?

Renderiza **sólo** un fondo (gradiente) y hace **Raycasting** al click para logs.

### Bloques importantes

* **`start()`**

  ```python
  self.objects = [Cube(...), ...] # para picking
  self.gfx = Graphics(self.ctx)
  self.gfx.load_program_from_files("sprite.vert","sprite.frag")
  self.gfx.create_fullscreen_quad()
  self._upload_sky_texture(w,h)
  ```

  * **No hay** raytracing.

* **`_upload_sky_texture(w,h)`**

  ```python
  rows[j] = camera.get_sky_gradient(v) * 255
  self.gfx.update_texture(w, h, img.get_bytes())
  ```

  * Genera el **gradiente** en CPU y lo sube a GPU.

* **`on_resize()`**

  ```python
  self._tex_w = max(320, width//2)
  self._upload_sky_texture(...)
  ```

  * Regenera el fondo a resolución proporcional.

* **`on_mouse_click()`**

  ```python
  ray = camera.raycast(u, v)
  for obj in objects: res = obj.check_hit(...)
  print("[Hit] Nombre" or "[Miss]")
  ```

  * Demuestra **Raycasting**.

---

# `scene_cpu.py` (modo **CPU**)

### ¿Qué hace?

Usa `RayTracer` para generar una imagen en **baja resolución interna** y la sube como textura al quad. Refresca cada ~0.15 s o cuando rota un cubo.

### Bloques importantes

* **Estado**

  ```python
  render_scale=0.33
  _render_dt=0.15
  _needs_redraw=True
  ```

  * Baja resolución para **rendir**.
  * Limita el **refresco** para no recalcular cada frame.

* **`start()`**

  ```python
  self.objects = [...]
  self._raytracer = RayTracer(self.camera, self.objects)
  self.gfx = Graphics(self.ctx); self.gfx.load_program_from_files("sprite.vert","sprite.frag")
  self.gfx.create_fullscreen_quad()
  self._resize_internal(...); self._render_to_texture()
  ```

  * Crea todo y **renderiza** el primer frame.

* **`update(dt)`**

  ```python
  rotate cube B; self._needs_redraw = True
  if _needs_redraw and _acc >= _render_dt: _render_to_texture()
  ```

  * Re-render **cuando hace falta**.

* **`_render_to_texture()`**

  ```python
  img = self._raytracer.render(self.fb_width, self.fb_height)
  self.gfx.update_texture(...)
  ```

  * Pinta el resultado del **RayTracer** en el quad.

---

# `scene_gpu.py` (modo **GPU**)

### ¿Qué hace?

Dibuja el quad fullscreen y corre un **fragment shader** que **raytracea**: para cada píxel, genera el rayo, intersecta OBBs y sombrea.

### Bloques importantes

* **`start()`**

  ```python
  self.objects = [Cube(...), ...]
  self.gfx = Graphics(self.ctx)
  self.gfx.load_program_from_files("raytracing.vert","raytracing.frag")
  self.gfx.create_fullscreen_quad()
  ```

  * Carga shader **de raytracing**.

* **Uniforms en `render()`**

  ```python
  prog["u_cam_pos"].value = (cam.pos.x, cam.pos.y, cam.pos.z)
  prog["u_fov_y"].value   = cam.fov_deg
  prog["u_aspect"].value  = cam.aspect
  prog["u_inv_view"].write(mat4_to_bytes(camera.inv_view))
  prog["u_sky_top/bottom"].value = ...
  prog["u_light_dir"].value = normalize(-0.5,1,-0.7)
  ```

  * Pasa **cámara**, **cielo** y **luz**.

* **Modelos y colores como **arrays**:**

  ```python
  prog["u_num_objs"].value = num
  prog["u_model"].write( concat(16 mat4 en bytes) )
  prog["u_color"].write( concat(16 vec4 en bytes) )
  ```

  * **Subimos el array completo** (evita `KeyError: 'u_model[0]'`/`u_color[0]` con algunos drivers).

* **`on_mouse_click()`**

  * Mantiene **picking** por CPU (para logs), independiente del shader.

---

# `shaders/sprite.vert` y `sprite.frag`

### ¿Qué hacen?

Shader mínimo para dibujar una **textura 2D** (fondo normal / resultado CPU) en un quad fullscreen.

* **Vertex**: pasa posiciones y UV al fragment.
* **Fragment**: samplea la textura y la muestra.

---

# `shaders/raytracing.vert`

### ¿Qué hace?

Sólo **pasa las UV** y emite `gl_Position` para el quad.

```glsl
layout(location=0) in vec2 in_pos;   // -1..1
layout(location=1) in vec2 in_uv;    // 0..1
out vec2 v_uv;
v_uv = in_uv; gl_Position = vec4(in_pos,0,1);
```

---

# `shaders/raytracing.frag`

### ¿Qué hace?

**Aquí vive el raytracer en GPU**. Para cada píxel:

1. Genera rayo en cámara.
2. Lo transforma a mundo.
3. Intersecta con todos los objetos (OBB → inv(M)*rayo).
4. Si impacta: calcula **Lambert** (difuso + ambiente).
5. Si no: usa **cielo**.

### Uniforms importantes

```glsl
uniform vec3  u_cam_pos;
uniform float u_fov_y, u_aspect;
uniform mat4  u_inv_view;

uniform vec3 u_sky_top, u_sky_bottom;

const int MAX_OBJECTS=16;
uniform int  u_num_objs;
uniform mat4 u_model[MAX_OBJECTS];
uniform vec4 u_color[MAX_OBJECTS];

uniform vec3 u_light_dir;
```

* **Array de mat4/vec4** subidos como **bloques** desde Python.

### Generación del rayo

```glsl
float tanHalf = tan(radians(u_fov_y)*0.5);
float x = 2*v_uv.x-1, y = 2*v_uv.y-1;
vec3 dir_cam = normalize(vec3(x*u_aspect*tanHalf, y*tanHalf, -1));
vec3 dir_world = normalize(mat3(u_inv_view)*dir_cam);
vec3 origin_world = u_cam_pos;
```

### Intersección con OBB (vía local)

```glsl
mat4 M = u_model[i], invM = inverse(M);
vec3 oL = (invM * vec4(origin_world,1)).xyz;
vec3 dL = normalize((invM * vec4(origin_world+dir_world,1)).xyz - oL);
float tNear = slabIntersectAABB(oL, dL, vec3(-0.5), vec3(0.5), tFar);
```

### Slab Method (núcleo)

```glsl
// por eje X/Y/Z: acumula tmin/tmax; si tmin>tmax → miss
```

### Sombreado Lambert

```glsl
// normal por cara en local (compara Hit con ±0.5 por eje)
vec3 nL = (±1,0,0) o (0,±1,0) o (0,0,±1)
vec3 nW = normalize(mat3(M) * nL)
float diff = max(dot(nW, normalize(u_light_dir)), 0.0)
vec3 col = base * (0.25 + 0.75 * diff) // 25% ambiente
```

### Cielo

```glsl
vec3 sky = mix(u_sky_bottom, u_sky_top, clamp(dir_world.y*0.5+0.5, 0,1));
```

---

# 🧪 ¿Cómo justificar/demostrar cada parte en un oral?

* **Rayos**: abrir `ray.py` → `Ray(origin, direction)` normalizada.
* **Raycasting**: F1 (normal), click → consola imprime el cubo (`scene_normal.py::on_mouse_click`).
* **CPU**: F2 (cpu), mover la cámara o rotar cubo → ver refresco cada ~0.15 s; explicar `raytracer.py::render`.
* **GPU**: F3 (gpu), mover cámara y ver sombreado en tiempo real; mostrar `u_model` y `u_color` subidos como **arrays**.
* **OBB**: en shader, rayo transformado por `inverse(model)` → Slab en local.
* **Matrices**: `camera.inv_view` enviado a shader para pasar de cámara a mundo.
* **Iluminación**: Lambert (difuso) + 25% ambiente en fragment.
* **Switch de escenas**: F1/F2/F3 en `window.py::on_key_press` — el profe lo ve en vivo.

---

# 🧷 Frases cortas para cerrar cada tema (estilo defensa)

* **Ray**: “Es una recta paramétrica; con `t` medimos distancias.”
* **Raycasting**: “Lanzo 1 rayo por click para saber qué objeto toqué.”
* **Raytracing**: “Lanzo 1 rayo por píxel para decidir el color.”
* **CPU vs GPU**: “En GPU paralelizo el cálculo por píxel; en CPU es secuencial.”
* **AABB/OBB**: “Si transformo el rayo con `inverse(model)`, el OBB se vuelve AABB local.”
* **Slab**: “Ajusto `tmin/tmax` por eje; si `tmin>tmax`, no hubo intersección.”
* **Matrices**: “Model ubica el objeto; View mira; Projection da perspectiva; Inverse View sirve para transformar rayos.”
* **Shader**: “El fragment calcula el rayo, intersecta y sombrea; si no pega, cielo.”
