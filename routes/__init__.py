# routes/__init__.py
from .webhook_routes import webhook_bp  # Importa el Blueprint

# Expone el Blueprint públicamente
__all__ = ['webhook_bp']