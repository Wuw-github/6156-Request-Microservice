from flask import Flask, Response, request, g, render_template, url_for, redirect, flash
import json
from requestDAO import RequestDAO
from requestBoard import RequestBoard

app = Flask(__name__)


@app.route("/")
def index():
    return "hello world"


def get_request_dao():
    if not hasattr(g, 'dao'):
        print("goes here")
        g.dao = RequestDAO()
    return g.dao


@app.route("/requests", methods=["GET"])
def get_all_requests():
    dao = get_request_dao()
    result = dao.fetch_all_requests()

    if result:
        rsp = Response(json.dumps(result, default=str), status=200, content_type="app.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@app.route("/requests/<request_id>", methods=["GET"])
def get_request_by_id(request_id):
    dao = get_request_dao()
    result = dao.fetch_request_by_id(request_id)

    if result:
        rsp = Response(json.dumps(result, default=str), status=200, content_type="app.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@app.route("/requests/<request_id>/participants", methods=["GET"])
def get_participants_by_id(request_id):
    dao = get_request_dao()
    result = dao.fetch_participants_by_request_id(request_id)

    if result:
        rsp = Response(json.dumps(result, default=str), status=200, content_type="app.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@app.route('/requests/create/', methods=['GET', 'POST'])
def add_request():
    if request.method == 'POST':
        launch_date = request.form['date']
        time = request.form['time']
        start_location = request.form['start_location']
        destination = request.form['destination']
        description = request.form['description']
        capacity = request.form['capacity']

        board = RequestBoard(launch_date, time, start_location, destination, description, capacity)
        if RequestBoard.checkValidation(board):
            dao = get_request_dao()
            dao.create_request(board)
            # flash('Board created')
            return redirect(url_for('get_all_requests'))
        return render_template('requests.html')
    return render_template('requests.html')









if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011, debug=True)
