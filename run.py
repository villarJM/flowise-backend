import os
from dotenv import load_dotenv
from app import create_app

# Determinar el entorno de ejecución
env = os.getenv('FLASK_ENV', 'development')

# Cargar variables de entorno según el ambiente
if env == 'production':
    load_dotenv('.env.prod')
elif env == 'testing':
    load_dotenv('.env.test')
else:
    load_dotenv('.env.dev')

app = create_app(env)

if __name__ == '__main__':
    # Configuración dinámica según el entorno
    debug_mode = env != 'production'
    port = int(os.getenv('PORT', 8000))
    host = os.getenv('HOST', '0.0.0.0')
    
    app.run(host=host, port=port, debug=debug_mode)