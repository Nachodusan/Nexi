import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # Para acceder a raíz
load_dotenv(BASE_DIR / '.env')

# Agregar en config.py
class Tags:
    CONFIRMACION = "[CONFIRMACION]"
    REINICIAR = "[REINICIAR]"
class Config:
    # Configuración de Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    # Validación básica de credenciales
    @property
    def supabase_configured(self):
        return bool(self.SUPABASE_URL and self.SUPABASE_KEY)
    
    # Otras configuraciones
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Tiempo de inactividad (minutos)
    INACTIVIDAD_MIN = int(os.getenv("INACTIVIDAD_MIN", "15"))
    
    # Límites de historial
    HISTORIAL_MAX_LENGTH = int(os.getenv("HISTORIAL_MAX_LENGTH", "10000"))
    HISTORIAL_MAX_TOKENS = int(os.getenv("HISTORIAL_MAX_TOKENS", "1500"))
    
    # Palabras clave para urgencias
    URGENT_KEYWORDS = os.getenv("URGENT_KEYWORDS", "incendio,accidente,sangre,emergencia,herido,desmayo,violencia,robo,asalto").split(",")
    
    # Preguntas en orden
    PREGUNTAS = [
        ("nombre", "👋 Por favor, dime tu nombre completo:"),
        ("edad", "¿Cuántos años tienes?"),
        ("direccion", "📌 Ingresa tu dirección exacta:"),
        ("zona", "📍 ¿En qué zona vives? (Sector, barrio, urbanización, etc.):"),
        ("problema", "❗ Describe el problema que quieres reportar:")
    ]
    
    # OpenAI
    MODEL_GPT = os.getenv("MODEL_GPT", "gpt-4o")
    
    # Prompt del sistema
    SISTEMA_PROMPT = f"""
Eres Nexi, un asistente virtual para reportar problemas comunitarios. 
Debes recolectar estos datos específicos en orden:
{", ".join([campo for campo, _ in PREGUNTAS])}.

Sigue estas reglas:
1. Mantén conversación natural y amigable con emojis apropiados
2. Pide un dato a la vez en el orden especificado
3. Valida respuestas:
   - Para 'edad': debe ser número entre 1-120
   - Para 'dirección': debe incluir calle y número
4. Si el usuario intenta saltar datos, redirige amablemente
5. Al completar todos los datos, muestra resumen y pregunta: 
   "¿Confirmas que esta información es correcta? (SI/NO)"
6. Usa [CONFIRMACION] al inicio cuando muestres el resumen final
7. Para reiniciar: si el usuario dice "reiniciar", usa [REINICIAR]
8. Para reportes urgentes: si detectas palabras como {", ".join(URGENT_KEYWORDS)}, prioriza la respuesta

Ejemplo de flujo:
Usuario: Hola
Tú: 👋 ¡Hola! Soy Nexi, tu asistente para reportes. ¿Podrías decirme tu nombre completo?
Usuario: Juan Pérez
Tú: Gracias Juan. ¿Cuántos años tienes?
... (continúa hasta completar todos los datos) ...
Tú: [CONFIRMACION] 🔍 Confirma tus datos:
Nombre: Juan Pérez
Edad: 35
Dirección: Av. Principal 123
Zona: Centro Norte
Problema: Bache grande en la calle
¿Es correcto? (responde SI/NO)
"""

# Crear instancia de configuración para acceso fácil
config = Config()