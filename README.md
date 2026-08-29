# SOUNDMOTION 🎵

> "El movimiento humano como instrumento musical."
>
## 📖 Descripción

* **SoundMotion** es una interfaz audiovisual interactiva que permite crear y modificar experiencias musicales mediante movimientos corporales.

* Mediante una cámara y técnicas de visión por computador, el sistema reconoce movimientos de la parte superior del cuerpo, incluyendo manos, dedos, brazos, muñecas y torso, para transformarlos en parámetros musicales y visuales en tiempo real.

* El proyecto busca explorar nuevas formas de interacción humano-computador, donde el cuerpo del usuario se convierte en el medio principal de control, permitiendo crear música sin depender únicamente de instrumentos o dispositivos físicos tradicionales.

* SoundMotion permite generar sonidos mediante movimientos, modificar pistas musicales, controlar efectos de audio y crear visuales interactivos sincronizados con la interacción del usuario.

* La propuesta combina visión por computador, procesamiento multimedia y generación audiovisual para construir una experiencia donde movimiento, sonido e imagen se relacionan en tiempo real.

---

## 🛠 Tecnologías Utilizadas

* **Lenguaje de programación:** Python
* **Visión por computador:** MediaPipe Pose + MediaPipe Hands
* **Procesamiento de imagen:** OpenCV
* **Entorno audiovisual:** TouchDesigner
* **Comunicación multimedia:** OSC / MIDI
* **Control de versiones:** Git + GitHub

---

## 🏗 Arquitectura del Sistema

SoundMotion utiliza una arquitectura modular donde cada componente cumple una función específica dentro del flujo de interacción entre el usuario, el reconocimiento corporal y la experiencia audiovisual.

```
Usuario
  ↓
Cámara
  ↓
Módulo de visión por computador
(MediaPipe Pose + Hands)
  ↓
Procesamiento e interpretación del movimiento
  ↓
Parámetros musicales y visuales
  ↓
TouchDesigner
  ↓
Audio + Visuales interactivos
```

### Componentes principales

| Componente              | Descripción                                                            |
| ----------------------- | ---------------------------------------------------------------------- |
| Captura de movimiento   | Obtiene información del usuario mediante cámara.                       |
| Reconocimiento corporal | Detecta manos, dedos, brazos, muñecas y torso.                         |
| Procesamiento           | Convierte movimientos corporales en valores utilizados por el sistema. |
| Motor audiovisual       | Genera sonidos, efectos y visuales en tiempo real.                     |

---

## ✨ Funcionalidades Principales

### 🎹 Creación Musical

El usuario podrá generar sonidos utilizando movimientos corporales.

Ejemplos:

* Movimiento vertical de la mano → variación de tono.
* Apertura de brazos → modificación de intensidad.
* Velocidad del movimiento → cambio de energía musical.

---

### 🎧 Manipulación de Audio

El usuario podrá cargar una pista musical y modificar diferentes parámetros mediante movimientos:

* Volumen.
* Ritmo.
* Efectos.
* Filtros.
* Intensidad sonora.

---

### 🌌 Visuales Interactivos

Los movimientos del usuario generarán respuestas visuales en tiempo real.

Elementos contemplados:

* Partículas.
* Formas abstractas.
* Animaciones sincronizadas con la música.

---

### 🧏‍♂️ Gestos Especiales

El sistema contará con gestos personalizados como elementos interactivos adicionales.

Ejemplo:

**Mano sobre el pecho → activación del Himno Nacional de Colombia como demostración especial del proyecto.**

---
