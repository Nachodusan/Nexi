# routes/webhook_routes.py

from twilio.twiml.messaging_response import MessagingResponse
import logging
import os
import sys


from flask import Blueprint, request
# Importaciones absolutas corregidas
from database.crud import obtener_datos_usuario, actualizar_historial, verificar_inactividad
from services.chat_service import manejar_mensaje

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route("/webhook", methods=["POST"])
def manejar_chat():
    telefono = request.form.get('From', '').strip()
    mensaje_usuario = request.form.get('Body', '').strip()
    resp = MessagingResponse()
    
    if not telefono:
        logging.error("Número de teléfono no detectado")
        return str(resp.message("⚠️ Error: No se detectó tu número. Por favor reintenta."))
    
    try:
        # Obtener datos del usuario
        datos, estado = obtener_datos_usuario(telefono)
        
        # Registrar mensaje del usuario
        actualizar_historial(telefono, f"Usuario: {mensaje_usuario}")
        
        # Procesar mensaje
        respuesta = manejar_mensaje(
            telefono=telefono,
            mensaje_usuario=mensaje_usuario,
            datos=datos,
            estado=estado
        )
        
        # Registrar respuesta del asistente
        actualizar_historial(telefono, f"Asistente: {respuesta}")
        
        return str(resp.message(respuesta))

    except Exception as e:
        # Manejo detallado de errores
        logging.error(f"Error en manejar_chat: {str(e)}", exc_info=True)
        return str(resp.message("⚠️ Error temporal. Por favor intenta nuevamente."))

@webhook_bp.route("/check-inactividad", methods=["GET"])
def verificar_inactividad_endpoint():
    timeout = config.INACTIVIDAD_MIN * 60
    try:
        # Ejecutar verificación de inactividad
        verificar_inactividad()
        return "Inactividad verificada"
    except Exception as e:
        logging.error(f"Error en verificar_inactividad: {str(e)}", exc_info=True)
        return "Error al verificar inactividad", 500