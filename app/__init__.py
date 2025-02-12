from flask import Flask

app = Flask(__name__,
            template_folder="../web/templates",
            static_folder="../web/static")

from app import routes  # Import routes after app is created.