import sys
import os


sys.path.insert(0, os.path.dirname(__file__))


from app import app as application


application.secret_key = os.getenv('SECRET_KEY', 'some_secret_key')

if __name__ == "__main__":
    
    application.run(host='0.0.0.0', port=1022)

