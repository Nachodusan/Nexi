import logging
from database.crud import guardar_dato, resetear_datos, marcar_chat_finalizado
from config import config
from utils.helpers import ofuscar_datos
# services/__init__.py
from .chat_service import manejar_mensaje
from .openai_service import generar_respuesta_gpt  # Nombre correcto en español

# Expone las funciones de servicio públicamente
__all__ = ['manejar_mensaje', 'generar_respuesta_gpt']  # Nombres corregidos

def manejar_mensaje(telefono: str, mensaje_usuario: str, datos, estado) -> str:
    """Maneja un mensaje usando IA o flujo estructurado"""
    # Primero intentar con OpenAI si está configurado
    respuesta_gpt = generar_respuesta_gpt(telefono, mensaje_usuario, datos, estado.paso)
    
    if respuesta_gpt:
        # Manejar casos especiales de OpenAI
        if "[CONFIRMACION]" in respuesta_gpt:
            # Guardar paso de confirmación
            guardar_dato(telefono, "paso", len(config.PREGUNTAS) + 1)
            # Limpiar el tag y añadir instrucciones
            return respuesta_gpt.replace("[CONFIRMACION]", "").strip() + "\n\nResponde con:\n- *SI* para confirmar\n- *NO* para corregir"
            
        if "[REINICIAR]" in respuesta_gpt:
            resetear_datos(telefono)
            return respuesta_gpt.replace("[REINICIAR]", "").strip() + "\n\n" + config.PREGUNTAS[0][1]
            
        return respuesta_gpt
    
    # Si OpenAI no está disponible o falló, usar flujo estructurado
    return flujo_estructurado(telefono, mensaje_usuario, datos, estado.paso)

def flujo_estructurado(telefono: str, mensaje_usuario: str, datos, paso: int) -> str:
    """Flujo de respaldo sin ChatGPT con validaciones mejoradas"""
    mensaje = mensaje_usuario.lower()
    
    # Comandos globales
    if mensaje in ['reiniciar', 'empezar de nuevo', 'reinicio']:
        resetear_datos(telefono)
        return "♻️ Conversación reiniciada. " + config.PREGUNTAS[0][1]
        
    if mensaje in ['salir', 'cancelar']:
        marcar_chat_finalizado(telefono)
        return "✅ Conversación finalizada. ¡Gracias!"
    
    # Determinar paso actual
    if paso is None or paso < 0:
        paso = 0
        
    # Si estamos en confirmación
    if paso >= len(config.PREGUNTAS):
        if mensaje in ['si', 'sí']:
            marcar_chat_finalizado(telefono)
            return "✅ Reporte registrado. ¡Gracias!"
        elif mensaje == 'no':
            resetear_datos(telefono)
            return "♻️ Comenzaremos de nuevo. " + config.PREGUNTAS[0][1]
        else:
            return "⚠️ Por favor responde SI o NO"
    
    # Validaciones específicas
    campo_actual, pregunta = config.PREGUNTAS[paso]
    mensaje_error = ""
    
    if campo_actual == "edad":
        if not mensaje.isdigit() or not (1 <= int(mensaje) <= 120):
            mensaje_error = "⚠️ Edad inválida. Debe ser un número entre 1 y 120"
    
    elif campo_actual == "direccion":
        if len(mensaje_usuario) < 10 or not any(char.isdigit() for char in mensaje_usuario):
            mensaje_error = "⚠️ Dirección incompleta. Debe incluir calle y número"
    
    if mensaje_error:
        return mensaje_error
    
    # Guardar dato y avanzar
    guardar_dato(telefono, campo_actual, mensaje_usuario)
    
    # Verificar urgencia para problemas
    if campo_actual == "problema":
        es_urgente = any(keyword in mensaje_usuario.lower() for keyword in config.URGENT_KEYWORDS)
        guardar_dato(telefono, "urgente", es_urgente)
        if es_urgente:
            logging.warning(f"🚨 REPORTE URGENTE de {ofuscar_datos(telefono)}: {mensaje_usuario}")
    
    nuevo_paso = paso + 1
    guardar_dato(telefono, "paso", nuevo_paso)
    
    # Determinar siguiente mensaje
    if nuevo_paso < len(config.PREGUNTAS):
        return config.PREGUNTAS[nuevo_paso][1]
    else:
        # Mostrar confirmación
        confirmacion = "\n".join([
            f"Nombre: {datos.nombre}",
            f"Edad: {datos.edad}",
            f"Dirección: {datos.direccion}",
            f"Zona: {datos.zona}",
            f"Problema: {datos.problema}"
        ])
        return f"📋 Confirma tus datos:\n{confirmacion}\n\n¿Es correcto? (responde SI/NO)"