from dataclasses import dataclass

from typing import Tuple

@dataclass
class UserData:
    nombre: str
    edad: str
    direccion: str
    zona: str
    problema: str
    historial: str
    urgente: bool

@dataclass
class UserState:
    telefono: str
    timestamp_ultimo_mensaje: float
    paso: int
    mensaje_inactividad_enviado: bool

