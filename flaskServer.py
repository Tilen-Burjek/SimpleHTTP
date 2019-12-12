import threading, time

from flask import Flask, request, g, Response
import time

app = Flask(__name__)

req_count = dict()
req_count_lock = threading.Lock()

@app.before_request
def before_request():
    g.start = time.time()

@app.route("/")
def home():
    """
    Server itself. Handles GET requests and returns respose.
    :return: response
    """
    if request.method == "GET":
        client_id = request.args.get("clientId")
        if check_attempt_number(g.start, client_id):
            return Response("OK", status=200, mimetype='application/json')
        else:
            return Response("Service unavailable", status=503, mimetype='application/json')


def check_attempt_number(timestamp, client_id):
    """
    Manages and attempts to avoid Denial of Service attacks
    :param timestamp: current_req timestamp
    :param client_id: current_req client_id
    :return: True (200 Response) | False (503 Response)
    """
    global req_count
    req_count_lock.acquire()
    try:
        if client_id in req_count:
            if timestamp - req_count[client_id][0] < 5:
                if len(req_count[client_id]) >= 5:
                    return False
                else:
                    req_count[client_id].append(timestamp)
                    return True
            else:
                req_count[client_id] = req_count[client_id][1:]
                req_count[client_id].append(timestamp)
                return True
        else:
            req_count[client_id] = [timestamp]
            return True
    finally:
        req_count_lock.release()


if __name__ == "__main__":
    app.run(debug=True, threaded=True)


# dict[key] = [0,1,2,3]
# dict[key] = [timestamp, requestCoutner]

