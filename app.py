from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
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
        try:
            # Send email
            mail.send(msg)
            flash('Съобщението беше изпратено успешно!', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            with open('./error.log', 'a') as f:
                f.write(f'Error: {str(e)} on date {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n ')
            flash(f'Възникна грешка при изпращането', 'danger')
            return redirect(url_for('contact'))

    return render_template('contact.html')

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
    app.run(debug=True)
