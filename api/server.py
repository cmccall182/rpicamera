from flask import Flask, request, make_response, current_app, render_template, Response, jsonify, send_file
from flask_cors import CORS, cross_origin
from functools import update_wrapper
from datetime import timedelta
from recipe_scrapers import scrape_me
from get_camera_frame import get_camera_frame
import json
import traceback
import logging

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'AcceptContent-Type'

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator    

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/stream.mjpg', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*', headers=['Content-Type'])
def camera_stream():
    try:
        if (request.method == 'GET'):
            return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=FRAME ')
        else:
            raise Exception('Unhandled')
    except:
        app.logger(traceback.format_exc())


@app.route('/camera', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*', headers=['Content-Type'])
def get_fridge_camera():
    try:
        if (request.method == 'GET'):
            return send_file(get_camera_frame(), mimetype='image/jpg')
        else:
            raise Exception('Unhandled')
    except:
        app.logger(traceback.format_exc())


@app.route('/recipes', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers=['Content-Type'])
def get_recipe():
    try:
        if (request.method == 'POST'):
            scraper = scrape_me(request.get_json())
            ingredients = scraper.ingredients()
            return jsonify(recipe=ingredients)
        else:
            raise Exception('Unhandled')
    except:
        app.logger(traceback.format_exc())

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')