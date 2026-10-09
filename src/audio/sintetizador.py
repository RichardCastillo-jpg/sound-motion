"""
Sintetizador de acordes de SoundMotion.

Recibe las frecuencias de un acorde (por ejemplo las que entrega
ControlAcordes.obtener_frecuencias()) y las convierte en sonido.
No contiene lógica musical: solo genera y reproduce audio.
"""

import numpy as np

FRECUENCIA_MUESTREO = 44100  # muestras por segundo
DURACION = 1.5            # segundos que suena cada acorde
VOLUMEN = 2          # entre 0.0 y 1.0, para evitar saturación
ATAQUE = 0.02                # segundos de subida, evita el "clic" inicial


def generar_onda(frecuencias, duracion=DURACION, volumen=VOLUMEN,
                 frecuencia_muestreo=FRECUENCIA_MUESTREO):
    """
    Genera la onda de un acorde sumando una onda senoidal por cada
    frecuencia, con un ataque corto y una caída suave.

    Retorna un arreglo de numpy (float32) listo para reproducir.
    """
    cantidad = int(duracion * frecuencia_muestreo)
    t = np.arange(cantidad) / frecuencia_muestreo

    onda = np.zeros(cantidad)
    for frecuencia in frecuencias:
        onda += np.sin(2 * np.pi * frecuencia * t)

    if len(frecuencias) > 0:
        onda /= len(frecuencias)  # normaliza para que no sature

    # Envolvente: subida rápida y caída exponencial.
    muestras_ataque = max(1, int(ATAQUE * frecuencia_muestreo))
    envolvente = np.exp(-2.5 * t)
    envolvente[:muestras_ataque] *= np.linspace(0, 1, muestras_ataque)

    return (onda * envolvente * volumen).astype(np.float32)


class Sintetizador:
    """Reproduce acordes sin bloquear el programa principal."""

    def __init__(self):
        self._audio_disponible = True

    def reproducir_acorde(self, frecuencias):
        """
        Reproduce el acorde indicado. Si había uno sonando, lo reemplaza.
        No bloquea: retorna de inmediato mientras el sonido se reproduce.

        Si el audio no está disponible (por ejemplo, sin dispositivo de
        salida) avisa una sola vez y el resto del sistema sigue funcionando.
        """
        if not frecuencias or not self._audio_disponible:
            return

        try:
            # Se importa aquí para que el módulo pueda cargarse (y
            # generar_onda probarse) en equipos sin dispositivo de audio.
            import sounddevice as sd

            sd.play(generar_onda(frecuencias), FRECUENCIA_MUESTREO)
        except Exception as error:
            self._audio_disponible = False
            print(f"[Sintetizador] No se pudo reproducir audio: {error}")

    def detener(self):
        """Detiene cualquier sonido en reproducción."""
        if not self._audio_disponible:
            return

        try:
            import sounddevice as sd

            sd.stop()
        except Exception:
            pass