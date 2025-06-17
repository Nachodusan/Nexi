# test_import.py
import sys
import os
import importlib



def main():
    # 1. Configurar rutas
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, BASE_DIR)
    
    print(f"✅ Directorio actual: {BASE_DIR}")
    print(f"✅ sys.path configurado: {sys.path[0]}")
    
    # 2. Verificar existencia de app_database
    app_db_path = os.path.join(BASE_DIR, "app_database")
    print(f"✅ Existe app_database? {os.path.exists(app_db_path)}")
    print(f"✅ Es directorio? {os.path.isdir(app_db_path)}")
    
    # 3. Listar contenido
    print("\n📂 Contenido de app_database:")
    try:
        for item in os.listdir(app_db_path):
            print(f" - {item}")
    except Exception as e:
        print(f"❌ Error listando contenido: {str(e)}")
    
    # 4. Intentar importar
    print("\n🔍 Intentando importar init_db...")
    try:
        # Intenta importar usando diferentes métodos
        try:
            from database import init_db
            print("✅ Método 1: from app_database import init_db - EXITOSO")
        except ImportError:
            import database
            init_db = database.init_db
            print("✅ Método 2: import app_database - EXITOSO")
        
        # 5. Ejecutar función
        print("\n⚙️ Ejecutando init_db...")
        try:
            init_db()
            print("✅ init_db ejecutada correctamente!")
        except Exception as e:
            print(f"❌ Error ejecutando init_db: {str(e)}")
            
    except Exception as e:
        print(f"❌ Error crítico de importación: {str(e)}")
        print("\n💡 Soluciones posibles:")
        print("1. Verifica que la carpeta 'app_database' existe")
        print("2. Asegúrate que contiene __init__.py")
        print("3. Revisa que crud.py tiene la función init_db")
        print("4. Verifica mayúsculas/minúsculas en nombres")

if __name__ == "__main__":
    main()