import os
from flask import Flask

# Get the base directory (the directory that contains both the app and web folders)
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__,
            template_folder=os.path.join(basedir, 'web', 'templates'),
            static_folder=os.path.join(basedir, 'web', 'static'))

from app import routes  # Import routes after app is created.
