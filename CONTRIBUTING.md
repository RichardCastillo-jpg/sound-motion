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

No se deben realizar cambios directamente sobre `main`.

Cada integrante del equipo trabajará desde una rama personal:

- `isa`
- `richard`
- `saul`

Cada integrante debe mantener su rama actualizada con respecto a `main` antes de comenzar una nueva tarea.

Las funcionalidades, correcciones y demás cambios se desarrollan dentro de la rama personal correspondiente.

Las Issues del proyecto indican qué tarea debe realizar cada integrante, qué archivos puede modificar, qué pruebas debe realizar y cuándo puede considerarse terminada.

### Reglas de trabajo con ramas

- Cada integrante trabaja desde su rama personal.
- No se deben realizar cambios directamente en `main`.
- Antes de comenzar una nueva tarea, se debe actualizar la rama personal con los cambios recientes de `main`.
- Cada Issue debe desarrollarse mediante commits independientes y claramente identificables.
- Cuando una tarea esté terminada, se debe crear un Pull Request desde la rama personal hacia `main`.
- El Pull Request debe ser revisado por otro integrante antes de realizar el merge.
- Después de integrar cambios en `main`, los demás integrantes deben actualizar sus ramas personales antes de continuar con tareas que dependan de esos cambios.
- No se deben mezclar cambios de Issues diferentes en un mismo commit.

### Ejemplo

Richard trabaja desde:

`richard`

Isabella trabaja desde:

`isa`

Saul trabaja desde:

`saul`

Si Richard termina una tarea:

`richard → Pull Request → main`

Después de aprobar e integrar ese Pull Request, Isabella y Saul deben actualizar sus ramas personales antes de comenzar tareas que dependan de ese cambio.

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

Los cambios desarrollados en una rama personal deben integrarse mediante un Pull Request hacia `main`.

Cada Pull Request debe indicar:

1. Qué se hizo.
2. Qué Issue resuelve.
3. Cómo se probó.
4. Qué evidencia existe.
5. Si existe alguna consideración importante para integrar los cambios.

Antes de solicitar una revisión, el integrante debe comprobar que su código funciona correctamente.

El Pull Request debe contener únicamente los cambios relacionados con la Issue correspondiente.

---

## Revisión de código

Todo Pull Request debe ser revisado por al menos otro integrante del equipo antes de integrarse a `main`.

La revisión debe comprobar:

- Que el cambio corresponda a la Issue.
- Que el código funcione correctamente.
- Que no introduzca errores evidentes.
- Que mantenga la organización del proyecto.
- Que no modifique innecesariamente otras partes del sistema.
- Que las pruebas indicadas en la Issue hayan sido realizadas.

---

## Pruebas

Antes de realizar un Pull Request, el integrante debe probar los cambios realizados.

Cuando sea posible, se debe incluir evidencia de las pruebas realizadas, especialmente para funcionalidades relacionadas con:

- Captura de cámara.
- Detección de pose.
- Detección de manos.
- Procesamiento de movimiento.
- Detección de gestos.
- Generación de sonido.
- Comunicación entre módulos.
- Comunicación con TouchDesigner.
- Visuales interactivos.

La evidencia puede incluir capturas de pantalla, resultados de consola o grabaciones breves cuando corresponda.

---

## Organización del código

El código debe ubicarse en la carpeta correspondiente a su responsabilidad.

La estructura principal del proyecto seguirá una organización modular:

- `src/vision/` → captura de cámara y detección mediante visión por computador.
- `src/processing/` → representación, procesamiento e interpretación de los datos de movimiento.
- `src/audio/` → generación y control del sonido.
- `src/integration/` → comunicación e integración entre los diferentes módulos.
- `touchdesigner/` → componentes y archivos relacionados con la parte visual en TouchDesigner.
- `tests/` → pruebas del proyecto.
- `docs/` → documentación técnica y evidencia necesaria.

Las nuevas carpetas o módulos deben crearse únicamente cuando exista una necesidad concreta dentro del proyecto.

---

## Documentación

Cuando un cambio introduzca una funcionalidad importante, se debe actualizar la documentación correspondiente.

La documentación debe permitir comprender:

- Qué hace la funcionalidad.
- Cómo utilizarla.
- Qué componentes necesita.
- Cómo se relaciona con el resto del sistema.
- Qué consideraciones existen para probarla o ejecutarla.

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

El flujo general para realizar una tarea será:

**Seleccionar Issue → Actualizar rama personal → Desarrollar → Probar → Commit → Push → Pull Request hacia `main` → Revisión → Correcciones si son necesarias → Merge a `main`**

Cada tarea debe seguir las instrucciones indicadas en su Issue correspondiente.

### Antes de comenzar una nueva tarea

1. Revisar que la Issue esté disponible para trabajar.
2. Verificar sus dependencias.
3. Actualizar `main`.
4. Actualizar la rama personal.
5. Confirmar que no existen cambios pendientes antes de comenzar.

### Durante el desarrollo

- Se deben modificar únicamente los archivos relacionados con la Issue.
- Se deben realizar commits claros y separados por tarea.
- No se deben incluir cambios de otras Issues en el mismo commit.
- No se deben realizar cambios directamente sobre `main`.

### Al terminar una tarea

1. Probar los cambios.
2. Revisar `git status`.
3. Realizar el commit correspondiente.
4. Subir la rama personal.
5. Crear un Pull Request hacia `main`.
6. Relacionar el Pull Request con la Issue.
7. Solicitar revisión de otro integrante.
8. Realizar correcciones si son necesarias.
9. Integrar el cambio en `main`.
10. Actualizar el estado de la Issue en el Project.

---

## Criterio para considerar una tarea terminada

Una tarea se considera terminada cuando:

- La funcionalidad solicitada está implementada o la validación requerida fue realizada.
- El código fue probado.
- Se realizaron las pruebas indicadas en la Issue.
- Se recopiló evidencia cuando correspondía.
- Los cambios fueron enviados mediante Pull Request si existieron modificaciones versionables.
- Otro integrante realizó la revisión cuando hubo Pull Request.
- El Pull Request fue integrado a `main`.
- La documentación fue actualizada cuando correspondía.
- La Issue fue actualizada y marcada como completada.