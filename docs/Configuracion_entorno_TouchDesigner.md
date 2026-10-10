# Instalación de TouchDesigner y configuración del entorno de visión (MediaPipe)

*Registro del procedimiento de instalación, verificación de dependencias y prueba de comunicación con TouchDesigner*

---

## 1. Instalación de TouchDesigner

Se descargó TouchDesigner en su versión completa (offline installer), con el fin de contar con el programa disponible en caso de no tener conexión a internet durante su uso.

Para poder usar la aplicación, se creó una cuenta de TouchDesigner utilizando un correo personal. Una vez verificada la cuenta por correo electrónico, se inició sesión desde la aplicación ya descargada.

Con la cuenta verificada, TouchDesigner presenta la opción de generar una nueva llave de activación (license key), necesaria para habilitar el uso del software. Al abrir el administrador de llaves (Key Manager), en la pestaña "Create" se debe seleccionar el tipo de licencia disponible —en este caso, la opción no comercial, con vigencia de actualizaciones durante un año— y luego presionar el botón "Create Key". En esa misma ventana se muestran datos del equipo, como el código del sistema y el nombre de la máquina, útiles para identificar en qué computador se generó la licencia.

Se selecciona la opción "Crear llave" y se espera a que el proceso finalice.

Una vez finalizado el proceso de creación de la llave, la aplicación confirma la activación mostrando un mensaje indicando que la llave fue instalada exitosamente y que las funciones de TouchDesigner ya están habilitadas. Desde ese momento, el programa se abre normalmente mostrando su interfaz principal de trabajo (la red de nodos, la paleta de operadores y la barra de tiempo), lista para crear o abrir proyectos.

---

## 2. Instalación de las librerías de Python

Una vez instalado y activado TouchDesigner, se procedió a instalar las librerías de Python necesarias para el prototipo, siguiendo la configuración suministrada por Richard. Las librerías se instalaron directamente sobre el intérprete de Python incluido en TouchDesigner, utilizando PowerShell o CMD de Windows con el siguiente comando:

```
"C:\Program Files\Derivative\TouchDesigner\bin\python.exe" -m pip install mediapipe opencv-python python-osc
```

Para confirmar que las librerías quedaron correctamente instaladas y son accesibles desde el Python de TouchDesigner, se ejecutó una prueba de importación con el siguiente comando:

```
"C:\Program Files\Derivative\TouchDesigner\bin\python.exe" -c "import mediapipe, cv2, pythonosc; print('OK')"
```

Al ejecutar este comando en la terminal, el resultado obtenido fue la palabra "OK" impresa sin ningún mensaje de error. Esto confirma que las tres librerías (mediapipe, opencv-python y python-osc) quedaron instaladas y son accesibles correctamente desde el intérprete de Python que usa TouchDesigner.

---

## 3. Descarga y ubicación de los modelos de MediaPipe

Realizada la verificación anterior, se descargaron los modelos correspondientes de MediaPipe indicados por Richard, disponibles en una tabla dentro de los enlaces suministrados.

Los archivos `.task` descargados deben ubicarse dentro de la misma carpeta donde se encuentra el script, ya que el proyecto está organizado en la ruta `src/vision/`. Por lo tanto, ambos modelos (`.task`) se colocaron dentro de esa carpeta, junto a `script.py`.

---

## 4. Ejecución del script y verificación de la cámara

Con los modelos ya ubicados en `src/vision/`, se ejecutó el siguiente comando para verificar que todo el flujo del prototipo funcionara correctamente:

```
"C:\Program Files\Derivative\TouchDesigner\bin\python.exe" script.py
```

Al ejecutar este comando se abre una ventana llamada "Mi cámara", en la cual se visualiza la transmisión en vivo de la cámara. Sobre la imagen aparecen puntos azules que indican hombro, codo y muñeca, y puntos rojos que indican las articulaciones de las manos. Esto confirma que el script está funcionando correctamente según lo planeado para el prototipo actual.

---

## 5. Comunicación por OSC entre Python y TouchDesigner

OSC (Open Sound Control) es el protocolo que utiliza el script de Python para enviarle en tiempo real, por red (UDP), los datos de pose y manos detectados por MediaPipe a TouchDesigner. Cada mensaje OSC está compuesto por una dirección (por ejemplo `/pose/hombro_izquierdo`), que identifica de qué landmark se trata, y un conjunto de valores (las coordenadas x, y, z de ese punto). Para que la comunicación funcione, tanto el script de Python como el OSC In CHOP de TouchDesigner deben usar exactamente el mismo puerto de red; en este proyecto se utiliza el puerto 9000.

En resumen, el flujo es el siguiente: el script de Python detecta un landmark (por ejemplo, el hombro izquierdo) y arma un mensaje OSC con su dirección correspondiente (`/pose/hombro_izquierdo`) y sus tres valores de coordenadas (`x, y, z`). Ese mensaje viaja por UDP hasta el puerto 9000, donde el OSC In CHOP de TouchDesigner lo recibe y lo convierte automáticamente en canales dentro del programa.

---

## 6. Configuración de TouchDesigner para recibir los datos (OSC In CHOP)

Con el script funcionando, se procedió a configurar TouchDesigner para recibir los datos enviados desde Python. Para ello se creó un nuevo proyecto y se agregó un operador (mediante doble clic o la tecla Tab sobre el lienzo) llamado "OSC In" (Open Sound Control), dentro de la categoría CHOP. Al escribir "oscin" en el buscador de operadores, este aparece listado junto a otros operadores de la misma categoría (como Audio Device In, Audio File In, entre otros), y se selecciona para agregarlo a la red.

Al agregarlo a la red de TouchDesigner, el operador aparece inicialmente como un recuadro verde vacío, sin datos, ya que todavía no ha sido configurado ni está recibiendo ningún mensaje.

A continuación se configura el operador con los siguientes parámetros, visibles en el panel de parámetros al seleccionar el nodo:

- **Active:** On
- **Protocol:** Messaging (UDP)
- **Network Port:** 9000

---

## 7. Verificación de la recepción de datos

Con esta configuración aplicada y el script de Python en ejecución, TouchDesigner comienza a mostrar todos los puntos (landmarks) detectados por la cámara, junto con sus respectivos nombres de canal. Al revisar el listado de canales del OSC In CHOP, se observan entradas como `hand/Left/pulgar_base1`, `hand/Left/pulgar_base2` y `hand/Left/pulgar_base3` —correspondientes a las coordenadas x, y, z de cada landmark de la mano izquierda—, junto con sus valores numéricos actualizándose en tiempo real a medida que se mueve la mano frente a la cámara. Esto confirma que la comunicación entre el script y TouchDesigner funciona correctamente.
