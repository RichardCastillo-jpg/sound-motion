# Landmarks utilizados por SoundMotion

Este documento es la referencia del equipo sobre que landmarks de MediaPipe usa SoundMotion, qué índice tiene cada uno y cómo se llama dentro del proyecto.
- La lista de Pose y la lista de Hands son independientes. Un mismo índice puede existir en ambas, pero significa cosas distintas.
- Cada landmark tiene un único nombre en todo el proyecto. Los módulos de `src/` deben usar estos nombres y no inventar alias.
- `izquierdo/a` y `derecho/a` se refieren a la persona que aparece en cámara, que es como MediaPipe define los lados en Pose.
- En Hands, MediaPipe devuelve la etiqueta `Left`/`Right` (handedness) asumiendo que la imagen está en espejo (modo selfie).

---

## 1. Pose (MediaPipe Pose, 33 landmarks disponibles, 8 usados)

Se usan solo brazos y torso, porque SoundMotion trabaja únicamente con la parte superior del cuerpo.

| Índice | Nombre en SoundMotion | Landmark MediaPipe | Lado | Por qué se usa |
|---|---|---|---|---|
| 11 | `hombro_izquierdo` | LEFT_SHOULDER | Izquierdo | Ancla del brazo y referencia del ancho del torso |
| 12 | `hombro_derecho` | RIGHT_SHOULDER | Derecho | Ancla del brazo y referencia del ancho del torso |
| 13 | `codo_izquierdo` | LEFT_ELBOW | Izquierdo | Articulación intermedia para movimiento del brazo |
| 14 | `codo_derecho` | RIGHT_ELBOW | Derecho | Articulación intermedia para movimiento del brazo |
| 15 | `muñeca_izquierda` | LEFT_WRIST | Izquierdo | Extremo del brazo; enlaza la pose con la mano izquierda |
| 16 | `muñeca_derecha` | RIGHT_WRIST | Derecho | Extremo del brazo; enlaza la pose con la mano derecha |
| 23 | `cadera_izquierda` | LEFT_HIP | Izquierdo | Referencia inferior del torso (posición y escala) |
| 24 | `cadera_derecha` | RIGHT_HIP | Derecho | Referencia inferior del torso (posición y escala) |

### Landmarks de Pose descartados

- **Cara (0-10):** fuera del alcance actual.
- **Dedos de Pose (17-22):** son redundantes; los dedos los cubre Hands con mayor precisión.
- **Piernas y pies (25-32):** fuera del alcance (parte superior del cuerpo).

---

## 2. Hands (MediaPipe Hands, 21 landmarks por mano, 21 usados)

Se usan los 21 landmarks de cada mano. Justificación:

- **Posición general de la mano:** muñeca y base de los dedos.
- **Movimiento de dedos:** requiere las articulaciones intermedias, no solo las puntas.
- **Gestos básicos posteriores** (puño, mano abierta, pinza, señalar): dependen de la relación entre articulaciones y puntas.

Recortar a un subconjunto ahorra poco y podría obligar a reindexar después.

Aplica igual a la mano izquierda y a la derecha. Los índices son los mismos; la mano se distingue por la etiqueta de lateralidad, no por el nombre del landmark.

| Índice | Nombre en SoundMotion | Landmark MediaPipe | Dedo | Articulación |
|---|---|---|---|---|
| 0 | `mano_muñeca` | WRIST | Mano | Muñeca (origen de la mano) |
| 1 | `pulgar_cmc` | THUMB_CMC | Pulgar | Base |
| 2 | `pulgar_mcp` | THUMB_MCP | Pulgar | Nudillo |
| 3 | `pulgar_ip` | THUMB_IP | Pulgar | Articulación intermedia |
| 4 | `pulgar_punta` | THUMB_TIP | Pulgar | Punta |
| 5 | `indice_mcp` | INDEX_FINGER_MCP | Índice | Nudillo |
| 6 | `indice_pip` | INDEX_FINGER_PIP | Índice | Articulación proximal |
| 7 | `indice_dip` | INDEX_FINGER_DIP | Índice | Articulación distal |
| 8 | `indice_punta` | INDEX_FINGER_TIP | Índice | Punta |
| 9 | `medio_mcp` | MIDDLE_FINGER_MCP | Medio | Nudillo |
| 10 | `medio_pip` | MIDDLE_FINGER_PIP | Medio | Articulación proximal |
| 11 | `medio_dip` | MIDDLE_FINGER_DIP | Medio | Articulación distal |
| 12 | `medio_punta` | MIDDLE_FINGER_TIP | Medio | Punta |
| 13 | `anular_mcp` | RING_FINGER_MCP | Anular | Nudillo |
| 14 | `anular_pip` | RING_FINGER_PIP | Anular | Articulación proximal |
| 15 | `anular_dip` | RING_FINGER_DIP | Anular | Articulación distal |
| 16 | `anular_punta` | RING_FINGER_TIP | Anular | Punta |
| 17 | `menique_mcp` | PINKY_MCP | Meñique | Nudillo |
| 18 | `menique_pip` | PINKY_PIP | Meñique | Articulación proximal |
| 19 | `menique_dip` | PINKY_DIP | Meñique | Articulación distal |
| 20 | `menique_punta` | PINKY_TIP | Meñique | Punta |

### Patrón de nombres

`<dedo>_<parte>`, con `dedo` en `pulgar | indice | medio | anular | menique` y `parte` en `cmc | mcp | pip | dip | ip | punta`. El pulgar usa `cmc`, `mcp`, `ip` y `punta`; no tiene `pip` ni `dip`.

Los nombres se escriben sin tildes ni eñes (`indice`, `menique`) para evitar problemas en código. La excepción son los nombres de Pose heredados del prototipo (`muñeca_*`).

---

## 3. Muñeca: Pose vs. Hands

La muñeca aparece en ambas listas, pero son landmarks distintos con nombres distintos:

| Origen | Nombre | Índice |
|---|---|---|
| Pose | `muñeca_izquierda` / `muñeca_derecha` | 15 / 16 |
| Hands | `mano_muñeca` | 0 |

Las posiciones son parecidas, pero no idénticas, porque provienen de dos modelos distintos. No deben tratarse como el mismo dato.

---

## 4. Referencia

- MediaPipe Pose Landmarker: https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker
- MediaPipe Hand Landmarker: https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker
