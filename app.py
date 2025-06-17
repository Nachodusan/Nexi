from flask import Flask
from routes.webhook_routes import webhook_bp
import logging
import sys
from pathlib import Path 
from database.crud import init_db 
from dotenv import load_dotenv
import os

load_dotenv() 
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

sys.path.append(str(Path(__file__).parent))

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Registrar blueprints
app.register_blueprint(webhook_bp)

# Inicializar base de datos
init_db()

if __name__ == "__main__":
    app.run(port=5000, debug=True)