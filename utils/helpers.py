def ofuscar_datos(texto: str) -> str:
    """Ofusca datos sensibles para protección de privacidad"""
    if not texto:
        return ""
    if texto.isdigit() and len(texto) > 6:
        return f"{texto[:3]}***{texto[-2:]}"
    return f"{texto[:2]}***{texto[-2:]}" if len(texto) > 4 else "***"