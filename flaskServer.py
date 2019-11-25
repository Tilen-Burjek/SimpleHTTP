from flask import Flask, jsonify, request, g, Response
import time, datetime

app = Flask(__name__)

req_count = dict()

@app.before_request
def before_request():
    g.start = time.time()

@app.route("/")
def home():
    if request.method == "GET":
        client_id = request.args.get("clientId")
        timestamp = datetime.datetime.fromtimestamp(g.start).strftime('%Y-%m-%d %H:%M:%S')
        if check_attempt_number(g.start, client_id):
            return jsonify({"answer": "OK", "clientId": client_id, "date": timestamp})
        else:
            return Response(jsonify({"answer": "Service Unavailable", "clientId": client_id, "date": timestamp}),
                            status=503, mimetype='application/json')


def check_attempt_number(timestamp, client_id):
    global req_count
    if client_id in req_count:
        if timestamp - req_count[client_id][0] < 5:     
            if req_count[client_id][1] >= 5:
                return False
            else:
                req_count[client_id][1] += 1
                return True
        else:
            req_count[client_id] = [timestamp, 1]
            return True
    else:
        req_count[client_id] = [timestamp, 1]
        return True


if __name__ == "__main__":
    app.run(debug=True)
