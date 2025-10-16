CUESTIONARIO DEL PARCIAL

A continuación se presentan las posibles preguntas que se realicen en el día de la evaluación del proyecto.

El día 16 de octubre tener el proyecto abierto en su computadora (si es grupal, con que uno de los integrantes tenga abierto el proyecto es suficiente). Iré banco por banco evaluando. Deben funcionar los 3 "SCENE_TYPE" (normal, cpu y gpu) del script main. Con esto tienen el práctico aprobado.



Luego haré 5 preguntas (o 10 si es un trabajo grupal, 5 cada uno) que deben responder en el momento, apoyándose en su proyecto y con sus palabras. Con responder bien 3 de las 5 preguntas, aprueban el teórico.

De este listado de preguntas, para cada uno voy a seleccionar 5 para que respondan con sus palabras (dejo ejemplo de respuestas completas):

General de Computación Gráfica:
¿Qué modelo de color utilizamos en nuestro proyecto? ¿Por qué?
R: Utilizamos el modelo RGB (Red, Green, Blue) con canal alfa (RGBA). Lo usamos porque las pantallas emiten luz mediante píxeles que mezclan estos tres colores primarios aditivos. Al sumar los tres componentes al máximo obtenemos blanco (máxima intensidad de luz), y al tenerlos en cero obtenemos negro (ausencia de luz).
¿Qué primitivas gráficas utilizamos en nuestro proyecto?
R: Utilizamos triángulos. Con ellos construimos figuras más complejas como el Quad (2 triángulos) y el Cube (12 triángulos, 2 por cada cara).
¿Para qué se suele utilizar la operación entre vectores: Producto Escalar? ¿Qué tipo de dato devuelve?
R: El Producto Escalar se utiliza para calcular el ángulo entre dos vectores o la proyección de un vector sobre otro. También sirve para determinar qué tan perpendiculares o paralelos son (si el resultado es 0 son perpendiculares, si es 1 o -1 son paralelos). Para analizar la perpendicularidad, ambos vectores deben estar previamente normalizados (longitud unitaria). Devuelve un valor escalar (float).
¿Para qué se suele utilizar la operación entre vectores: Producto Vectorial? ¿Qué tipo de dato devuelve?
R: Se utiliza para crear un vector perpendicular a los dos vectores dados. Es útil para calcular normales de superficies o bases ortonormales. Devuelve un vector con las mismas dimensiones que los vectores originales (en 3D devuelve un vector 3D).
¿Cuál es la coordenada homogénea w para un punto? ¿Por qué?
R: La coordenada homogénea w es 1 para un punto porque los puntos deben verse afectados por las traslaciones (nueva posición). Entonces, como 1 es el neutro de la multiplicación, la traslación se aplica correctamente.
¿Cuál es la coordenada homogénea w para una dirección? ¿Por qué?
R: La coordenada homogénea w es 0 para una dirección porque las direcciones no deben verse afectadas por traslaciones. Entonces, como 0 es el absorbente de la multiplicación, anula la traslación. Básicamente, la dirección “arriba” debe ser siempre la misma, no importa dónde esté posicionado.
¿Qué estructura matemática me permite pasar un vector de un espacio vectorial (por ejemplo, de las coordenadas de la cámara) a otro espacio vectorial (coordenadas de la escena)?
R: La estructura que permite pasar un vector de un espacio vectorial a otro es una matriz de transformación. En nuestro caso usamos matrices 4x4 porque trabajamos con coordenadas homogéneas en 3D.
¿Qué dimensiones (filas y columnas) debe tener una matriz para poder aplicar transformaciones lineales (rotación, traslado, escala) a objetos 3D?
R: Las dimensiones de una matriz de transformación debe ser una matriz de 4x4 (4 filas y 4 columnas) para trabajar con coordenadas homogéneas en 3D.
¿Qué función cumple, en Computación Gráfica, la inversa de una matriz? Dame un ejemplo.
R: La inversa de una matriz deshace o invierte las transformaciones aplicadas. Por ejemplo: si tengo un rayo en el espacio de la cámara y quiero transformarlo al espacio del mundo, multiplico por la inversa de la matriz de vista (base de coordenadas de la Cámara). 
¿A qué hace referencia el "Espacio del Objeto"?
R: Es el sistema de coordenadas local del objeto, donde el origen (0,0,0) está en el centro del objeto y los ejes están alineados con el objeto mismo (antes de aplicarle transformaciones). 
¿A qué hace referencia el "Espacio del Mundo"?
R: Es el sistema de coordenadas global de la escena, donde todos los objetos se posicionan. El origen (0,0,0) es el centro de la escena y sirve como referencia común para todos los objetos.
¿A qué hace referencia el "Espacio de Vista"?
R: Es el sistema de coordenadas relativo a la cámara, donde el origen está en la posición de la cámara y los ejes están orientados según hacia dónde mira la cámara.
¿Dónde está el punto de origen, normalmente, en una pantalla?
R: Depende del sistema. En algunos está en la esquina superior izquierda (como en la mayoría de las interfaces gráficas), en otros en la esquina inferior izquierda (como en OpenGL). Lo importante es conocer la convención que usa la biblioteca que estamos utilizando.
¿Dónde está el punto de origen, normalmente, en un objeto de la escena?
R: En el centro geométrico del objeto (también llamado pivot point).
¿Qué son coordenadas normalizadas NDC?
R: Son coordenadas que van de -1 a 1 en todos los ejes (x, y, z). Se usan después de la proyección para tener un espacio estándar independiente de la resolución de pantalla.
¿Cuál es la principal diferencia entre la proyección en perspectiva y la ortográfica?
R: La proyección perspectiva simula cómo vemos en la realidad: los objetos lejanos se ven más pequeños (proyección tipo cono/pirámide). La proyección ortográfica mantiene el tamaño de los objetos sin importar la distancia (proyección prisma rectangular).
¿Qué son el VBO, IBO y VAO? Describe brevemente la función de cada uno.
R: Son estructuras que conectan los datos del modelo con el shader. 
El VBO (Vertex Buffer Object) almacena los atributos de los vértices (posición, color, normales, UVs). 
El IBO (Index Buffer Object) almacena los índices que indican en qué orden conectar los vértices. 
El VAO (Vertex Array Object) describe cómo están organizados estos datos (tipos de datos) y los vincula con el shader (nombres).
¿Qué indica la normal de un vértice?
R: La normal indica la dirección perpendicular a la superficie en ese vértice. Es decir, “hacia dónde mira”.
¿En qué lenguaje programamos para hacer un shader con OpenGL?
R: Para programar shaders en OpenGL utilizamos el lenguaje GLSL.
¿Qué tipo de unidades recorre el Vertex Shader?
R: El Vertex Shader recorre vértices. Se ejecuta una vez por cada vértice del modelo.
¿Qué tipo de unidades recorre el Fragment Shader?
R: El Fragment Shader recorre fragmentos (píxeles del modelo rasterizado). Se ejecuta una vez por cada píxel que forma parte de la geometría rasterizada.
En el Render Pipeline de la GPU ¿Qué se ejecuta primero, el Vertex o el Fragment shader?
R: En el Render Pipeline primero se ejecuta el Vertex Shader (transforma cada vértice), luego ocurre la rasterización (que convierte la geometría en píxeles), y finalmente se ejecuta el Fragment Shader (calcula el color de cada píxel).
¿El Compute Shader recorre unidades?
R: El Compute Shader no recorre unidades de geometría como los otros shaders. Se ejecuta en grupos de trabajo (work groups) de forma paralela, procesando datos de manera general sin estar atado al Render Pipeline.
¿El Compute Shader se ejecuta en GPU o en CPU?
R: El Compute Shader se ejecuta en la GPU.
¿Cuál es la diferencia entre trabajar con Vertex y Fragment shader o hacerlo con Compute shader?
R: El Vertex-Fragment shader está atado al Render Pipeline: el Vertex shader procesa vértices uno por uno, y el Fragment shader procesa píxeles de esos vértices rasterizados. Están diseñados para dibujar geometría en pantalla y operan objeto por objeto (cada objeto ejecuta un “draw call” con la función vao.render).
El Compute Shader es de propósito general, independiente del Render Pipeline. Puede acceder a datos arbitrarios (como toda la escena a la vez mediante SSBOs) y realizar cálculos que no necesariamente producen geometría. Esto lo hace ideal para raytracing, donde necesitamos que cada píxel "vea" todos los objetos de la escena simultáneamente.
¿Qué es un work group?
R: Work Group es un grupo de hilos de ejecución en un Compute Shader que trabajan en paralelo. Permiten dividir el trabajo total en bloques que se procesan simultáneamente en la GPU.
¿Qué son los Uniforms? ¿En qué se diferencian con los atributos de un vértice?
R: Los uniforms son variables globales que se envían desde la CPU y tienen el mismo valor para todas las ejecuciones del shader (todos los vértices y fragmentos). Los atributos de vértice son específicos de cada vértice y varían entre ellos (como su posición o color individual).
¿Qué son los Sampler2D?
R: Es un tipo de uniform especial que representa una textura 2D. Permite leer colores de una imagen cargada en la memoria de la GPU usando coordenadas UV.
¿Qué es un Ray (rayo) en Computación Gráfica?
R: El rayo en Computación Gráfica es una semirrecta definida por un punto de origen y una dirección. Se usa para simular trayectorias de luz o hacer cálculos de colisiones.

Proyecto:
¿Dónde encontramos matrices de transformación en nuestro proyecto?
R: Cada vez que creamos o utilizamos el espacio vectorial de un objeto de la escena. Por ejemplo: 
En las clases Cube o Quad en el método get_model_matrix
En la clase Camera en el método get_view_matrix y get_projection_matrix
¿Desde dónde se trazan los Rays en nuestro proyecto?
R: En nuestro proyecto, los Rays se trazan desde la posición de la cámara hacia cada píxel de la pantalla (en el caso del raytracing). En raycasting también desde la cámara, pero hacia la posición del mouse.
¿Qué función cumple la clase HitBox?
R: La clase HitBox detecta si un rayo colisiona con el objeto. Es un volumen simplificado (caja) que envuelve al objeto para hacer los cálculos de colisión más eficientes.
¿Cuántos Rays se necesitan para calcular si el mouse está sobre un objeto en pantalla?
R: Para calcular si el mouse está sobre un objeto de pantalla, trazamos un solo Ray. Se lanza un rayo desde la cámara en dirección a la posición del cursor en la escena 3D.
¿Para qué fin utilizamos Pyglet?
R: Usamos Pyglet para crear la ventana de la aplicación, gestionar el ciclo de renderizado (el loop principal) y capturar eventos de entrada como el mouse.
¿Para qué fin utilizamos ModernGL?
R: Usamos ModernGL para simplificar el uso de OpenGL moderno. Es una wrapper de Python que hace más fácil trabajar con shaders, buffers y texturas.
¿Qué atributos tiene un Model en nuestro proyecto?
R: Los atributos que tiene la clase Model en nuestro proyecto son: vertices (posiciones), indices, colors (colores), normals (normales) y texcoords (coordenadas UV).
¿Qué ventaja ofrece separar los atributos de vértices (posiciones, colores, normales) en lugar de tener un único array?
R: Separar los atributos de los vértices permite mayor flexibilidad: podemos tener modelos que solo definen algunos atributos (por ejemplo, solo posición y normales sin colores). También hace el código más legible y permite que el shader consuma solo los atributos que necesita, optimizando la memoria.
¿Qué sucedería si los nombres de los atributos en la clase VertexLayout no coinciden con los del shader?
R: Si los nombres de los atributos en la clase VertexLayout no coinciden con los del shader, éste no recibiría los datos esperados. El atributo quedaría sin vincular y el shader usaría valores por defecto o basura, causando errores visuales o de ejecución.
¿Cómo le pasamos los atributos del Model al Vertex Shader?
R: Los atributos del Model los pasamos al Vertex Shader a través de VBOs (que contienen los datos) organizados en un VAO (que describe cómo leerlos). 
En nuestro proyecto, la clase Graphics se encarga de crear estos buffers y vincularlos con el shader.
¿Qué responsabilidad tiene la clase Material?
R: Relacionar un shader con diferentes texturas.
¿Qué almacena la clase Texture y qué método utiliza para convertir los datos a un formato que OpenGL pueda usar?
R: La clase Texture almacena un ImageData (matriz de numpy con los colores de cada píxel). Usa el método get_bytes() para convertir esa matriz en bytes que OpenGL puede cargar en la GPU.
¿Por qué es importante que los nombres de las texturas (Texture.name) coincidan con los uniforms del Fragment shader?
R: Es importante que los nombres de las texturas (Texture.name) coincidan con los uniforms de nuestro shader para que el shader pueda referenciar correctamente la textura. El nombre actúa como identificador que conecta la textura cargada con el uniform sampler2D declarado en el shader.
¿Cómo le cambio el color a un cubo?
R: Para cambiarle el color a un cubo. Creo o Modifico una Texture con el color deseado, creo, si no existe, un Material que vincule esa textura con un shader, y asigno ese material al cubo cuando lo agrego a la escena.
¿Cómo hago que uno de los cubos se deje de animar?
R: Para que uno de los cubos se deje de animar, al crear la instancia del Cube, le paso el parámetro animated=False.
¿Para qué usamos las coordenadas uv en el Fragment Shader?
R: Las coordenadas uv las utilizamos en el Fragment Shader para mapear una textura sobre la superficie. Las coordenadas UV indican qué píxel de la textura corresponde a cada fragmento que estamos renderizando.
¿Qué pasa visualmente si en el Vertex Shader no multiplicamos la posición de la figura primitiva por la matriz "Mvp" (Model-View-Projection)?
R: Si en el Vertex Shader no multiplicamos la posición del vértice por la matriz “Mvp”, el objeto no se transforma correctamente al espacio de la cámara. Lo más probable es que no se vea en pantalla, o se vea en una posición incorrecta ignorando la perspectiva y la ubicación de la cámara.
¿Qué pasa si deshabilito el Depth Test?
R: Si deshabilito el Depth Test en el proyecto, OpenGL deja de realizar la prueba de profundidad y no detecta qué está “por delante” y qué “por detrás”, por lo que no oculta aquellos fragmentos que son “tapados” por otros.
¿El Vertex-Fragment shader se ejecuta una vez por toda la escena o individualmente para cada objeto?
R: El Vertex-Fragment shader se ejecuta individualmente para cada objeto. Cada objeto tiene su propio draw call (vao.render), y en cada draw call el shader procesa todos los vértices y fragmentos de ese objeto específico.
¿Cuál es la principal diferencia entre Raycasting y Raytracing?
R: La principal diferencia es que Raycasting solo detecta si hay colisión entre el rayo y un objeto (información básica). Raytracing utiliza el Raycasting para además calcular información detallada de la colisión como el color de la superficie, normales, reflexiones, refracciones y sombras para generar imágenes realistas.
¿Cuántos Rays se trazan para renderizar un frame de pantalla? ¿De qué depende la cantidad?
R: Para renderizar un frame de pantalla, se traza un Ray por cada píxel de la pantalla. Depende de la resolución: si la pantalla es 800x600, se trazan 480,000 rayos.
¿Por qué se utiliza un Quad en el proyecto de Raytracing?
R: Utilizamos un Quad en Raytracing porque funciona como una "pantalla virtual" donde se muestra el resultado del raytracing. La textura generada por el raytracer se mapea sobre el Quad para visualizarla.
¿Por qué se utiliza el parámetro hittable en la clase Hit?
R: El parámetro hittable en la clase Hit lo utilizamos para controlar qué objetos deben considerarse en las colisiones del raytracing. Si hittable es False, el rayo ignora ese objeto (útil para el Quad de fondo, que solo sirve para mostrar la imagen y no debe colisionar).
Si al ejecutar el programa el quad se renderiza completamente en rojo, ¿cuál es la causa más probable y cómo se soluciona?
R: Si la pantalla renderiza completamente en rojo, puede ser porque el quad tiene configurada la propiedad “hittable” en True. También puede ser que la cantidad de objetos que hay en escena ocupan todos y cada uno de los píxeles de la pantalla. Se soluciona reduciendo la cantidad de objetos o indicando en la instancia del quad que su propiedad “hittable” es False.
En la escena de CPU ¿Dónde configuramos el color del cielo?
R: En la clase Camera, usando el método set_sky_colors() que define los colores superior e inferior del degradado del cielo.
En raytracing por CPU ¿Dónde realizamos el trazado de rayos? ¿Qué da como resultado?
R: En raytracing por CPU trazamos los rayos en el método trace_ray de la clase RayTracer. Da como resultado un ImageData (matriz numpy) donde cada píxel tiene el color calculado según si el rayo colisionó con un objeto o con el cielo. Este ImageData luego se convierte a bytes y se carga como textura en el Quad.
¿Por qué el raytracing en CPU es más lento que en GPU?
R: El raytracing es más lento en CPU que en GPU porque en CPU los rayos se procesan secuencialmente uno tras otro (un solo núcleo o pocos núcleos). En GPU se usan work groups que procesan miles de rayos en paralelo simultáneamente, aprovechando los miles de núcleos de la GPU.
En la escena de GPU ¿Dónde configuramos el color del cielo? ¿Crees que se puede obtener de los archivos de Python? ¿Cómo se los paso al shader?
R: El color del cielo se configura en el Compute Shader, en la parte del código que se ejecuta cuando el rayo no colisiona con ningún objeto. Sí, se puede obtener de Python: tomamos los colores de la clase Camera en la clase RaytracerGPU y los pasamos al shader como uniforms de tipo vec3.
En raytracing por GPU ¿Dónde realizamos el trazado de rayos? ¿Qué da como resultado?
R: En raytracing por GPU los rayos se trazan en el método main() del Compute Shader. Da como resultado una textura de OpenGL donde cada píxel se escribe directamente en la GPU según si el rayo colisionó con un objeto o con el cielo.
¿Qué diferencia hay entre las clases Raytracer y RaytracerGPU?
R: La diferencia es que:
La clase Raytracer (CPU) ejecuta el algoritmo de trazado de rayos en Python píxel por píxel y genera un ImageData que se pasa a bytes y se guardan en la textura que luego se renderiza en el Quad. Es decir, hace todo el raytracing.
La clase RaytracerGPU prepara y envía los datos (SSBOs) al Compute Shader para que la GPU haga todo el trazado en paralelo. Es decir, prepara los datos que necesita el shader y no ocurre el raytracing en la misma clase, lo delega a la GPU.
¿Por qué usamos un Compute Shader y no el tradicional Vertex-Fragment shader?
R: Usamos Compute Shader para raytracing y no el clásico Vertex-Fragment shader porque necesitamos acceder a información de toda la escena simultáneamente para trazar rayos desde cualquier píxel hacia todos los objetos. El Vertex-Fragment shader está diseñado para procesar un objeto a la vez, mientras que el Compute Shader puede trabajar con toda la escena de forma global y paralela.
¿Cómo se guardan datos complejos para enviar al Compute Shader?
R: Para enviar al Compute Shader datos complejos, se guardan en SSBOs (Shader Storage Buffer Objects), que son buffers que pueden almacenar estructuras de datos complejas (arrays de matrices, vectores, structs, etc.) accesibles desde el shader.
¿Por qué usamos SSBOs?
R: Usamos SSBOs porque necesitamos enviar grandes cantidades de datos estructurados al shader (como las transformaciones de todos los objetos, sus materiales, el BVH, etc.) y los uniforms tradicionales tienen límites de tamaño muy pequeños.
¿Cómo se declara un SSBO en el compute shader?
R: Un SSBO se declara en el shader con la palabra clave "buffer" seguida del layout de binding.
¿Qué importa más: el binding o el nombre de la variable?
R: Importa más el binding que el nombre de la variable. El binding indica la ubicación exacta en memoria donde están los datos. El nombre de la variable es sólo para referencia interna del shader.
¿Qué guarda la variable models_f? ¿Para qué se usa?
R: En la variable models_f se guardan las matrices de transformación modelo (Model matrix) de cada objeto en la escena. Se usa para transformar los objetos de su espacio local al espacio del mundo.
¿Qué guarda la variable inv_f? ¿Para qué se usa?
R: En la variable inv_f se guardan las matrices inversas de transformación de cada objeto. Se usa para transformar los rayos del espacio del mundo al espacio local de cada objeto, facilitando el cálculo de colisiones en las coordenadas originales del objeto.
¿Qué guarda la variable mats_f? ¿Para qué se usa?
R: En la variable mats_f se guarda la información de los materiales de cada objeto (colores y propiedades como reflectividad). Se usa para calcular el color final de los píxeles al renderizar.
¿Qué guarda la variable primitives? ¿Para qué se usa?
R: La variable primitives guarda información de las primitivas geométricas (como los vértices o bounds de los objetos). Se usa para construir y recorrer el BVH al hacer las pruebas de colisión.
En resumidas palabras ¿Para qué usamos el BVH?
R: Usamos el BVH para optimizar las colisiones organizando los objetos en una jerarquía espacial. Permite descartar rápidamente grupos enteros de objetos que no pueden ser alcanzados por un rayo, evitando hacer pruebas de colisión innecesarias (como ver si un rayo que va hacia la derecha colisiona con un objeto que está en la izquierda).
¿Qué efecto visual obtenemos si la luz es completamente perpendicular a la superficie?
R: Una luz completamente perpendicular a la superficie la ilumina al máximo (máxima intensidad), ya que recibe la luz directamente de frente.
¿Qué efecto visual obtenemos si la luz es completamente paralela a la superficie?
R: Una luz completamente paralela a la superficie la deja sin iluminación (solo se ve la luz ambiental), ya que la luz no incide sobre ella sino que pasa de largo.
¿Qué efecto visual añade la luz ambiental?
R: La luz ambiental proporciona iluminación base uniforme a toda la escena. Hace que los objetos sean visibles incluso en zonas sin luz directa, evitando sombras completamente negras.
¿Qué efecto visual añade la luz difusa?
R: La luz difusa crea el efecto de sombreado en las superficies según el ángulo de la luz. Las caras perpendiculares a la luz se ven más claras y las paralelas más oscuras, dando volumen al objeto.
¿Qué efecto visual añade la luz especular?
R: La luz especular crea brillos o reflejos puntuales en las superficies, simulando materiales brillantes o pulidos. Se ve más intenso cuando el ángulo de reflexión coincide con la dirección de la cámara.
¿Cómo obtenemos una escena con sombras más oscuras (o menos suaves)?
R: Para obtener sombras menos suaves, en el método calculateShadow del Compute Shader reducimos el porcentaje de luz que se devuelve cuando el rayo hace hit (está en sombra). Valores más bajos generan sombras más oscuras.

Exclusivas de conceptos vistos en el apartado para Proyecto en Grupo:
¿Qué diferencia principal hay entre un Hitbox AABB (Axis Aligned Bounding Box) y uno OBB (Object Oriented Bounding Box)?
R: La diferencia entre AABB y OBB es que el AABB es una caja alineada a los ejes del mundo (no rota con el objeto), mientras que OBB es una caja orientada que sigue las rotaciones del objeto (se alinea con los ejes locales del objeto). OBB es más precisa pero más costosa de calcular.
¿Qué función cumple la clase HitBoxOBB?
R: La función que cumple la clase HitBoxOBB es la de detectar colisiones entre un rayo y el objeto usando una caja orientada que se ajusta mejor a la forma rotada del objeto. Transforma el rayo al espacio local del objeto para hacer la colisión más precisa.
¿Cuál es la principal diferencia entre Raytracing y Pathtracing?
R: La diferencia es que Pathtracing extiende el raytracing al simular múltiples rebotes de luz. Cuando un rayo colisiona con una superficie, puede generar nuevos rayos (reflejados o refractados) que continúan trazándose recursivamente, obteniendo efectos de iluminación global más realistas.
¿Cuál es la diferencia visual que agrega Pathtracing a la escena?
R: La diferencia visual es la de ver reflexiones y refracciones realistas. Los objetos con reflectividad reflejan otros objetos de la escena en su superficie, y se pueden ver efectos como espejos, metales brillantes o vidrio.
¿Cuántos rebotes de luz utilizamos en nuestro proyecto?
R: En nuestro proyecto usamos un máximo de 3 rebotes. Es un balance entre realismo visual (más rebotes = más realista) y rendimiento (cada rebote multiplica el costo computacional).
¿Qué significa una reflectividad de 1.0?
R: Una reflectividad de 1.0 significa que la superficie refleja completamente la luz sin absorberla, comportándose como un espejo perfecto. Todo el rayo se refleja en la dirección especular.
¿Qué significa una reflectividad de 0.0?
R: Una reflectividad de 0.0 significa que la superficie absorbe toda la luz sin reflejarla, comportándose como un material completamente mate. No se generan rayos reflejados.
