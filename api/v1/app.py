#!/usr/bin/python3
from flask import Flask, make_response, jsonify
from flask_cors import CORS
import models
from api.v1.views import app_views

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    models.storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001', threaded=True)
