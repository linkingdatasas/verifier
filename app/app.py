# Import flask and template operators
from flask import Flask, render_template, session

import os

# Define the WSGI application object
app = Flask(__name__)

#Conf
app.config['JSON_SORT_KEYS'] = False


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return 'bad request!', 404



# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_ver.controllers import mod_ver

# Register blueprint(s)
app.register_blueprint(mod_ver)



def main():
    """Main entry point of the app."""
    try:

        app.run(host='0.0.0.0', debug=True, port=8008, use_reloader=True,threaded=True)
    except Exception as exc:
        print(exc.message)
    finally:
        # get last entry and insert build appended if not completed
        # Do something here
        pass