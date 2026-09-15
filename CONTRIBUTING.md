# Guía de Contribución — SoundMotion

## Propósito

Este documento establece las reglas básicas para trabajar de manera organizada en el desarrollo de **SoundMotion**.

El objetivo es evitar conflictos entre los integrantes, mantener un historial de cambios claro y facilitar la integración del trabajo realizado por el equipo.

---

## Equipo

SoundMotion es desarrollado por:

* Saul
* Isa
* Richard

---

## Ramas

La rama `main` contiene la versión estable del proyecto.

Los cambios nuevos deben desarrollarse en ramas independientes y posteriormente integrarse mediante un Pull Request.

### Formato para nombrar ramas

Las ramas deben utilizar nombres descriptivos que indiquen el propósito del cambio.

Formato:

```text
desarrollo/nombre-de-la-tarea
```

Ejemplos:

```text
desarrollo/organizacion-repositorio
desarrollo/reconocimiento-corporal
desarrollo/procesamiento-movimiento
desarrollo/deteccion-gestos
desarrollo/generacion-sonido
desarrollo/integracion-touchdesigner
```

No se deben realizar cambios directamente sobre `main`.

---

## Commits

Los mensajes de commit deben ser breves, claros y escritos en español.

El mensaje debe explicar qué cambio se realizó.

### Ejemplos

```text
Crear estructura inicial del proyecto
```

```text
Agregar dependencias de Python
```

```text
Organizar código de reconocimiento corporal
```

```text
Implementar cálculo de desplazamiento
```

```text
Agregar detección de gesto de mano
```

```text
Corregir validación de landmarks
```

Se deben evitar mensajes poco descriptivos como:

```text
cambios
arreglos
cosas
prueba
final
final final
```

---

## Pull Requests

Los cambios desarrollados en una rama deben integrarse mediante un Pull Request hacia `main`.

El Pull Request debe explicar:

1. Qué se hizo.
2. Por qué se hizo.
3. Cómo se probó.
4. Si existe alguna consideración importante para integrar los cambios.

Antes de solicitar la revisión, el integrante debe comprobar que su código funciona correctamente.

---

## Revisión de código

Todo Pull Request debe ser revisado por al menos otro integrante del equipo antes de integrarse a `main`.

La revisión debe comprobar principalmente:

* Que el cambio corresponda a la tarea.
* Que el código funcione.
* Que no introduzca errores evidentes.
* Que mantenga la organización del proyecto.
* Que no modifique innecesariamente otras partes del sistema.

---

## Pruebas

Antes de realizar un Pull Request, el integrante debe probar los cambios realizados.

Cuando sea posible, se debe incluir evidencia de las pruebas realizadas, especialmente para funcionalidades relacionadas con:

* Reconocimiento corporal.
* Procesamiento de movimiento.
* Detección de gestos.
* Generación de sonido.
* Comunicación con TouchDesigner.
* Visuales interactivos.

---

## Organización del código

El código debe ubicarse en la carpeta correspondiente a su responsabilidad.

La estructura principal del proyecto seguirá una organización modular:

```text
src/
├── vision/
├── processing/
└── audio/
```

Las nuevas carpetas o módulos deben crearse únicamente cuando exista una necesidad concreta dentro del proyecto.

---

## Documentación

Cuando un cambio introduzca una funcionalidad importante, se debe actualizar la documentación correspondiente.

La documentación debe permitir comprender:

* Qué hace la funcionalidad.
* Cómo utilizarla.
* Qué componentes necesita.
* Cómo se relaciona con el resto del sistema.

---

## Archivos que no deben subirse

No se deben subir al repositorio:

* Entornos virtuales.
* Archivos temporales.
* Configuraciones personales del editor.
* Contraseñas o claves.
* Variables de entorno privadas.
* Archivos generados automáticamente que no sean necesarios para ejecutar el proyecto.

Estas exclusiones deben mantenerse en `.gitignore`.

---

## Flujo de trabajo

El flujo general para realizar cambios será:

```text
Crear/seleccionar tarea
        ↓
Crear rama
        ↓
Desarrollar
        ↓
Probar
        ↓
Commit
        ↓
Push
        ↓
Pull Request
        ↓
Revisión
        ↓
Correcciones (si son necesarias)
        ↓
Merge a main
```

---

## Criterio para considerar una tarea terminada

Una tarea se considera terminada cuando:

* La funcionalidad solicitada está implementada.
* El código fue probado.
* Los cambios fueron enviados mediante Pull Request.
* Otro integrante realizó la revisión.
* El Pull Request fue integrado a `main`.
* La documentación fue actualizada cuando correspondía.
