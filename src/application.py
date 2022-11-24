from flask import Flask, Response, request
from datetime import datetime
import json
from columbia_student_resource import ColumbiaStudentResource
from flask_cors import CORS
import requests as req

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)


@app.get("/api/composite/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "F22-composite-Microservice",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result


@app.route("/api/composite/students/<uni>", methods=["GET", "POST", "DELETE"])
def student_by_uni(uni):
    if request.method == "GET":
        result = {'student_info': None, 'student_courses': None, 'student_contact': {'address': None, 'phone': None}}
        req1 = req.get(f'http://18.212.74.63:5011/api/students/{uni}')
        req2 = req.get(f'http://awsome-eb-dev.us-east-1.elasticbeanstalk.com/api/students/{uni}/courses')
        req3 = req.get(f'http://18.212.74.63:5012/api/students/{uni}/addresses')
        req4 = req.get(f'http://18.212.74.63:5012/api/students/{uni}/phones')
        if req1.status_code == 200:
            result['student_info'] = json.loads(req1.content.decode('utf-8'))
        if req2.status_code == 200:
            result['student_courses'] = json.loads(req2.content.decode('utf-8'))
        if req3.status_code == 200:
            result['student_contact']['address'] = json.loads(req3.content.decode('utf-8'))
        if req4.status_code == 200:
            result['student_contact']['phone'] = json.loads(req4.content.decode('utf-8'))

    elif request.method == "DELETE":
        result = {'student_info': False, 'student_courses': False,
                  'student_contact': {'address': False, 'phone': False}}
        req1 = req.delete(f'http://18.212.74.63:5011/api/students/{uni}')
        # req2 = req.delete(f'http://awsome-eb-dev.us-east-1.elasticbeanstalk.com/api/students/{uni}/courses')
        req3 = req.delete(f'http://18.212.74.63:5012/api/students/{uni}/addresses')
        req4 = req.delete(f'http://18.212.74.63:5012/api/students/{uni}/phones')
        if req1.status_code == 200:
            result['student_info'] = True
        if req3.status_code == 200:
            result['student_contact']['address'] = True
        if req4.status_code == 200:
            result['student_contact']['phone'] = True
    else:
        data = request.get_json()
        result = {'student_info': False, 'student_courses': False,
                  'student_contact': {'address': False, 'phone': False}}
        try:
            req1 = req.post(url=f'http://18.212.74.63:5011/api/students/{uni}', data=data['student_info'])
            # req2 = req.delete(f'http://awsome-eb-dev.us-east-1.elasticbeanstalk.com/api/students/{uni}/courses')
            req3 = req.post(url=f'http://18.212.74.63:5012/api/students/{uni}/addresses', data=data['student_contact'][
                'address'])
            req4 = req.post(url=f'http://18.212.74.63:5012/api/students/{uni}/phones', data=data['student_contact'][
                'phone'])
            if req1.status_code == 200:
                result['student_info'] = True
            if req3.status_code == 200:
                result['student_contact']['address'] = True
            if req4.status_code == 200:
                result['student_contact']['phone'] = True
        except Exception as e:
            print(e)
    rsp = Response(json.dumps(result), status=200, content_type="application.json")
    return rsp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5013)

