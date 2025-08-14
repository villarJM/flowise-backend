import os
from dotenv import load_dotenv
from app import create_app

# Cargar variables de entorno
load_dotenv('.env.dev')

app = create_app('development')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5011, debug=True)