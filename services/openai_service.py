import logging
from openai import OpenAI
from config import config

# Inicializar cliente de OpenAI solo si hay API key
client = None
if config.OPENAI_API_KEY:
    try:
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        logging.info("✅ Cliente de OpenAI configurado")
    except Exception as e:
        logging.error(f"❌ Error al configurar OpenAI: {str(e)}")
        client = None
else:
    logging.warning("⚠️ OPENAI_API_KEY no configurada, se usará flujo estructurado")

def generar_respuesta_gpt(telefono: str, mensaje_usuario: str, datos, paso: int) -> str:
    """Genera respuesta usando ChatGPT con contexto"""
    if not client:
        return None
        
    try:
        historial = datos.historial if datos.historial else ""
        
        # Truncar historial si es muy largo
        if len(historial) > config.HISTORIAL_MAX_TOKENS:
            lineas = historial.splitlines()
            keep_initial = int(len(lineas) * 0.3)  # Mantener 30% inicial importante
            historial = "\n".join(lineas[:keep_initial] + lineas[-(len(lineas)-keep_initial):])
        
        # Personalizar prompt con datos existentes
        sistema_personalizado = config.SISTEMA_PROMPT
        if datos.nombre:
            sistema_personalizado += f"\n\nDatos actuales del usuario:\nNombre: {datos.nombre}"
            if paso > 0:
                sistema_personalizado += f"\nEdad: {datos.edad}"
        
        messages = [
            {"role": "system", "content": sistema_personalizado},
            {"role": "user", "content": f"{historial}\nUsuario: {mensaje_usuario}"}
        ]

        if paso >= len(config.PREGUNTAS):
            messages.append({
                "role": "system",
                "content": "IMPORTANTE: Muestra todos los datos recolectados con el formato [CONFIRMACION] y pide confirmación SI/NO"
            })

        response = client.chat.completions.create(
            model=config.MODEL_GPT,
            messages=messages,
            max_tokens=350,
            temperature=0.3
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        logging.error(f"Error en ChatGPT: {str(e)}")
        return None