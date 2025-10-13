# Mr. Glass Store

Welcome to the Mr. Glass Store project! This repository contains the source code for a web application that showcases various glass products and services.

## Project Structure

```
app.py                 # Main application entry point
error.log              # Log file for errors
monitor.log            # Log file for monitoring
passenger_wsgi.py      # WSGI configuration for Passenger
requirements.txt       # Python dependencies
site_monitor.py        # Monitoring script
wsgi.py                # WSGI configuration

static/                # Static files (CSS, JS, images)
  css/                 # Stylesheets and images
  js/                  # JavaScript files

templates/             # HTML templates
  about.html           # About page
  base.html            # Base template
  contact.html         # Contact page
  error.html           # Error page
  index.html           # Home page
  services.html        # Services page

tmp/                   # Temporary files
  restart.txt          # File to trigger application restart
```

## Requirements

- Python 3.8 or higher
- Flask (see `requirements.txt` for full list of dependencies)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```bash
   cd mrglass_store
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To start the application, run:
```bash
python app.py
```

## crontab

to run site_monitor.py

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
