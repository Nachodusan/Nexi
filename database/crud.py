from supabase import create_client, Client
import time
import logging
from typing import Optional, Tuple
from .models import UserData, UserState
from config import config


# Cliente Supabase global
_supabase_client = None

def get_supabase() -> Client:
    global _supabase_client
    if _supabase_client is None:
        if not config.SUPABASE_URL or not config.SUPABASE_KEY:
            error_msg = (
                "ERROR: Las variables SUPABASE_URL y SUPABASE_KEY no están configuradas.\n"
                "Asegúrate de tener un archivo .env con:\n"
                "- SUPABASE_URL=...\n"
                "- SUPABASE_KEY=..."
            )
            logging.error(error_msg)
            raise RuntimeError(error_msg)
        _supabase_client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
        logging.info("✅ Cliente de Supabase inicializado")
    return _supabase_client

def init_db():
    """Inicializa la conexión y verifica la tabla usuarios"""
    print("✅ init_db ejecutándose!")
    try:
        supabase = get_supabase()
        response = supabase.table("usuarios").select("*").limit(1).execute()
        if response.data:
            logging.info("✅ Tabla 'usuarios' verificada en Supabase")
        else:
            logging.warning("⚠️ La tabla 'usuarios' está vacía o no existe")
    except Exception as e:
        logging.error(f"❌ Error al verificar tabla: {str(e)}")
        raise RuntimeError("Error de conexión con Supabase. Verifica tus credenciales y conectividad.")

def obtener_datos_usuario(telefono: str) -> Optional[Tuple[dict, Optional[str]]]:
    supabase = get_supabase()
    try:
        response = supabase.table("usuarios").select("*").eq("telefono", telefono).maybe_single().execute()
        if response and hasattr(response, 'data') and response.data:
            data = response.data
            return data, data.get("estado", None)
        else:
            logging.info(f"No se encontró usuario con teléfono: {telefono}")
            return None, None

    except Exception as e:
        logging.error(f"Error al obtener datos usuario {telefono}: {e}")
        return None, None


def actualizar_historial(telefono: str, nuevo_historial: str) -> bool:
    supabase = get_supabase()
    try:
        response = supabase.table("usuarios").update({"historial": nuevo_historial}).eq("telefono", telefono).execute()
        return response.status_code == 200
    except Exception as e:
        logging.error(f"Error al actualizar historial para {telefono}: {e}")
        return False

def verificar_inactividad(telefono: str, timeout_segundos: int) -> bool:
    supabase = get_supabase()
    try:
        response = supabase.table("usuarios").select("timestamp_ultimo_mensaje").eq("telefono", telefono).maybe_single().execute()
        if not response or not response.data or "timestamp_ultimo_mensaje" not in response.data:
            logging.warning(f"No se encontró timestamp para {telefono}")
            return True
        ultimo = response.data["timestamp_ultimo_mensaje"]
        return (int(time.time()) - int(ultimo)) > timeout_segundos
    except Exception as e:
        logging.error(f"Error al verificar inactividad {telefono}: {e}")
        return True

def guardar_dato(telefono: str, campo: str, valor) -> bool:
    supabase = get_supabase()
    try:
        response = supabase.table("usuarios").update({campo: valor}).eq("telefono", telefono).execute()
        return response.status_code == 200
    except Exception as e:
        logging.error(f"Error al guardar dato '{campo}' para {telefono}: {e}")
        return False

def resetear_datos(telefono: str) -> bool:
    supabase = get_supabase()
    try:
        response = supabase.table("usuarios").update({
            "historial": "",
            "paso": 0,
            "chat_finalizado": False
        }).eq("telefono", telefono).execute()
        return response.status_code == 200
    except Exception as e:
        logging.error(f"Error al resetear datos para {telefono}: {e}")
        return False

def marcar_chat_finalizado(telefono: str) -> bool:
    supabase = get_supabase()
    try:
        response = supabase.table("usuarios").update({
            "chat_finalizado": True
        }).eq("telefono", telefono).execute()
        return response.status_code == 200
    except Exception as e:
        logging.error(f"Error al finalizar chat para {telefono}: {e}")
        return False
