# Guía de Contribución — SoundMotion

## Propósito

Este documento establece las reglas para trabajar de manera organizada en el desarrollo de **SoundMotion**.

El objetivo es mantener un historial de cambios claro, evitar conflictos entre los integrantes y facilitar la revisión e integración del trabajo realizado por el equipo.

---

## Equipo

SoundMotion es desarrollado por:

- Richard
- Isabella
- Saul



---

## Ramas

La rama `main` contiene la versión estable del proyecto.

Los cambios nuevos deben desarrollarse en ramas independientes y posteriormente integrarse mediante un Pull Request.

### Formato para nombrar ramas

Se utilizará el siguiente formato:

`tipo/nombre-de-la-tarea`

Tipos permitidos:

- `feature/` → nueva funcionalidad.
- `fix/` → corrección de errores.
- `docs/` → cambios de documentación.
- `test/` → incorporación o modificación de pruebas.
- `refactor/` → reorganización o mejora del código.

Ejemplos:

- `feature/reconocimiento-corporal`
- `feature/procesamiento-movimiento`
- `feature/deteccion-gestos`
- `feature/generacion-sonido`
- `feature/integracion-touchdesigner`
- `fix/validacion-landmarks`
- `docs/actualizar-readme`

No se deben realizar cambios directamente sobre `main`.

---

## Commits

Todos los integrantes deben utilizar el mismo formato para los mensajes de commit.

### Formato

`tipo: descripción`

La descripción debe ser breve, específica y estar escrita en español.

### Tipos permitidos

| Tipo | Uso |
|---|---|
| `feat` | Agregar una nueva funcionalidad. |
| `fix` | Corregir un error existente. |
| `docs` | Modificar o agregar documentación. |
| `refactor` | Reorganizar o mejorar el código sin cambiar su comportamiento. |
| `test` | Agregar o modificar pruebas. |
| `chore` | Realizar tareas de configuración o mantenimiento del proyecto. |

### Ejemplos

- `feat: agregar detección de manos`
- `feat: implementar cálculo de velocidad`
- `fix: corregir validación de landmarks`
- `docs: actualizar guía de contribución`
- `refactor: separar procesamiento de movimiento`
- `test: agregar pruebas de detección de gestos`
- `chore: configurar dependencias del proyecto`

### Reglas para los commits

Los mensajes de commit deben:

- Utilizar uno de los tipos definidos anteriormente.
- Estar escritos en español.
- Describir específicamente el cambio realizado.
- Ser breves y fáciles de entender.
- Representar un cambio concreto.

Se deben evitar mensajes poco descriptivos como:

- `cambios`
- `arreglos`
- `cosas`
- `prueba`
- `avance`
- `final`
- `final final`

---

## Pull Requests

Los cambios desarrollados en una rama deben integrarse mediante un Pull Request hacia `main`.

Cada Pull Request debe indicar:

1. Qué se hizo.
2. Qué tarea resuelve.
3. Cómo se probó.
4. Si existe alguna consideración importante para integrar los cambios.

Antes de solicitar una revisión, el integrante debe comprobar que su código funciona correctamente.

---

## Revisión de código

Todo Pull Request debe ser revisado por al menos otro integrante del equipo antes de integrarse a `main`.

La revisión debe comprobar:

- Que el cambio corresponda a la tarea.
- Que el código funcione correctamente.
- Que no introduzca errores evidentes.
- Que mantenga la organización del proyecto.
- Que no modifique innecesariamente otras partes del sistema.

---

## Pruebas

Antes de realizar un Pull Request, el integrante debe probar los cambios realizados.

Cuando sea posible, se debe incluir evidencia de las pruebas realizadas, especialmente para funcionalidades relacionadas con:

- Reconocimiento corporal.
- Procesamiento de movimiento.
- Detección de gestos.
- Generación de sonido.
- Comunicación con TouchDesigner.
- Visuales interactivos.

---

## Organización del código

El código debe ubicarse en la carpeta correspondiente a su responsabilidad.

La estructura principal del proyecto seguirá una organización modular:

- `src/vision/` → reconocimiento corporal y procesamiento de cámara.
- `src/processing/` → procesamiento e interpretación del movimiento.
- `src/audio/` → generación y control del sonido.

Las nuevas carpetas o módulos deben crearse únicamente cuando exista una necesidad concreta dentro del proyecto.

---

## Documentación

Cuando un cambio introduzca una funcionalidad importante, se debe actualizar la documentación correspondiente.

La documentación debe permitir comprender:

- Qué hace la funcionalidad.
- Cómo utilizarla.
- Qué componentes necesita.
- Cómo se relaciona con el resto del sistema.

---

## Archivos que no deben subirse

No se deben subir al repositorio:

- Entornos virtuales.
- Archivos temporales.
- Configuraciones personales del editor.
- Contraseñas o claves.
- Variables de entorno privadas.
- Archivos generados automáticamente que no sean necesarios para ejecutar el proyecto.

Estas exclusiones deben mantenerse en `.gitignore`.

---

## Flujo de trabajo

El flujo general para realizar cambios será:

**Seleccionar tarea → Crear rama → Desarrollar → Probar → Commit → Push → Pull Request → Revisión → Correcciones (si son necesarias) → Merge a `main`**

---

## Criterio para considerar una tarea terminada

Una tarea se considera terminada cuando:

- La funcionalidad solicitada está implementada.
- El código fue probado.
- Los cambios fueron enviados mediante Pull Request.
- Otro integrante realizó la revisión.
- El Pull Request fue integrado a `main`.
- La documentación fue actualizada cuando correspondía.
