# services/__init__.py
from .chat_service import manejar_mensaje
from .openai_service import generar_respuesta_gpt  # Nombre correcto en español

# Expone las funciones de servicio públicamente
__all__ = ['manejar_mensaje', 'generar_respuesta_gpt']  # Nombres corregidos