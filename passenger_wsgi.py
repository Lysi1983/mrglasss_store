import sys
import os

# Това е добра практика. Гарантира, че модулите в текущата
# директория (като твоя 'app.py') ще бъдат намерени.
sys.path.insert(0, os.path.dirname(__file__))

# Импортираме Flask обекта 'app' от твоя основен файл 'app.py'
# и го преименуваме на 'application', както очаква Passenger.
from app import app as application

