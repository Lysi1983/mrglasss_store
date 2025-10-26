from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_minify import Minify
import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configure Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

# Configure Flask-Minify
Minify(app=app, html=True, js=True, cssless=True)

# Configure Flask-Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

app.secret_key = os.getenv('SECRET_KEY')

@app.route('/')
@limiter.limit("20 per minute")
def index():
    return render_template('index.html')

@app.route('/about')
@limiter.limit("20 per minute")
def about():
    return render_template('about.html')

@app.route('/services')
@limiter.limit("20 per minute")
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
@limiter.limit("20 per minute")  # Specific rate limit for the contact form
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        msg = Message(subject=f"Ново съобщение от {name}",
                      sender=email,
                      recipients=['mrglas2025@gmail.com'],
                      body=f"Име: {name}\nИмейл: {email}\n\nСъобщение:\n{message}")
        msg_recipient = Message(subject="Вашето съобщение беше получено",
                     sender=os.getenv('MAIL_USERNAME'),
                     recipients=[email],
                    
                     html=f"""
                     <p>Благодарим ви, че се свързахте с нас! Вашето съобщение беше получено.</p>
                     <p><img src='{url_for('static', filename='css/logo.png', _external=True)}' alt='Mr. Glass Logo' style='max-height: 60px; border-radius: 50%;'></p>
                     """)
        try:
            # Send email
            mail.send(msg)
            mail.send(msg_recipient)
            
            flash('Съобщението беше изпратено успешно!', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            with open('./error.log', 'a') as f:
                f.write(f'Error: {str(e)} on date {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n ')
            flash(f'Възникна грешка при изпращането', 'danger')
            return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/get_images/<folder_name>')
def get_images(folder_name):
    # Construct path relative to the application's static folder
    # Use app.root_path to get the application's root directory
    base_static_path = os.path.join(app.root_path, app.static_folder or 'static')
    image_folder_path = os.path.join(base_static_path, 'images', folder_name)
    image_folder_url_base = f'images/{folder_name}'  # Base for URL generation

    try:
        # Security check: Ensure the resolved path is still within the intended 'static/images' directory
        if not os.path.abspath(image_folder_path).startswith(os.path.abspath(os.path.join(base_static_path, 'images'))):
            app.logger.warning(f"Attempt to access invalid path: {folder_name}")
            return jsonify({"error": "Invalid folder path"}), 400  # Bad Request

        if os.path.isdir(image_folder_path):
            # Supported image formats including WebP
            supported_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.PNG', '.JPG', '.JPEG', '.GIF', '.BMP', '.WEBP')
            images = [f for f in os.listdir(image_folder_path) 
                     if os.path.isfile(os.path.join(image_folder_path, f)) and f.lower().endswith(supported_extensions)]
            # Generate URLs correctly using url_for
            image_urls = [url_for('static', filename=os.path.join(image_folder_url_base, img).replace('\\', '/')) for img in images]
            return jsonify(image_urls)
        else:
            app.logger.info(f"Image folder not found: {folder_name}")
            return jsonify({"error": "Folder not found"}), 404
    except Exception as e:
        app.logger.error(f"Error fetching images for {folder_name}: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', 
                           error_code='404', 
                           error_name='Страницата не е намерена', 
                           error_description='Страницата, която търсите, не съществува или е преместена.'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html',
                           error_code='500',
                           error_name='Грешка в сървъра',
                           error_description='Възникна проблем с нашия сървър. Моля, опитайте отново по-късно.'), 500

@app.errorhandler(403)
def forbidden(e):
    return render_template('error.html',
                           error_code='403',
                           error_name='Достъпът е забранен',
                           error_description='Нямате разрешение за достъп до тази страница.'), 403

@app.errorhandler(400)
def bad_request(e):
    return render_template('error.html',
                           error_code='400',
                           error_name='Невалидна заявка',
                           error_description='Сървърът не може да обработи вашата заявка.'), 400

@app.errorhandler(429)
def too_many_requests(e):
    return render_template('error.html',
                           error_code='429',
                           error_name='Твърде много заявки',
                           error_description='Вие изпратихте твърде много заявки за кратък период от време.'), 429

if __name__ == '__main__':
    # Add basic logging configuration
    import logging
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
