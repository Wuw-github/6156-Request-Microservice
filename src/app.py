from flask import Flask, Response, request, g, render_template, url_for, redirect, flash
import json
from requestDAO import RequestDAO
from requestBoard import RequestBoard
from response_service import Paginate, Hateoas

app = Flask(__name__)


def get_request_dao():
    if not hasattr(g, 'dao'):
        g.dao = RequestDAO()
    return g.dao


def check_user_login():
    if not hasattr(g, 'user_id'):
        g.user_id = 1


@app.route("/requests", methods=["GET"])
def get_all_requests():
    dao = get_request_dao()
    result = dao.fetch_all_requests(request.args)

    rsp = {}
    Paginate.paginate(request.path, result, request.args, rsp)
    Hateoas.link_request_to_participants_by_id(rsp)
    if rsp['data']:
        rsp = Response(json.dumps(rsp, default=str), status=200, content_type="app.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@app.route("/requests/<request_id>", methods=["GET", "PUT", "DELETE"])
def get_request_by_id(request_id):
    dao = get_request_dao()
    if request.method == "GET":
        rsp = {}
        result = dao.fetch_request_by_id(request_id)
        Paginate.paginate(request.path, [result], request.args, rsp)
        Hateoas.link_request_to_participants_by_id(rsp)
        if rsp['data']:
            rsp = Response(json.dumps(rsp, default=str), status=200, content_type="app.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        return rsp

    check_user_login()
    if request.method == "PUT":
        board = process_form_for_board(request.form)
        dao.update_request(request_id, board)
        return redirect(url_for('get_all_requests', request_id=request_id))

    if request.method == "DELETE":
        dao.delete_participant(request_id, g.user_id)

        return redirect(url_for(get_all_requests))


@app.route("/requests/<request_id>/participants", methods=["GET", "DELETE", "POST"])
def get_participants_by_id(request_id):
    check_user_login()
    if request.method == "GET":
        dao = get_request_dao()
        result = dao.fetch_participants_by_request_id(request_id)

        rsp = {}
        Paginate.paginate(request.path, result, request.args, rsp)
        Hateoas.link_participant_to_user_by_id(rsp)
        if rsp['data']:
            rsp = Response(json.dumps(rsp, default=str), status=200, content_type="app.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        return rsp

    if request.method == "DELETE":
        dao = get_request_dao()
        dao.delete_participant(request_id, g.user_id)
        return redirect(url_for("get_all_requests"))

    if request.method == "POST":
        check_user_login()
        dao = get_request_dao()
        dao.create_participant(request_id, g.user_id)
        return redirect(url_for('get_participants_by_id', request_id=request_id))


def process_form_for_board(form):
    launch_date = request.form['date']
    time = request.form['time']
    start_location = request.form['start_location']
    destination = request.form['destination']
    description = request.form['description']
    capacity = request.form['capacity']

    board = RequestBoard(launch_date, time, start_location, destination, description, capacity)
    return board


@app.route('/requests/create/', methods=['GET', "POST"])
def add_request():
    check_user_login()
    if request.method == 'POST':
        board = process_form_for_board(request.form)
        if RequestBoard.checkValidation(board):
            dao = get_request_dao()
            dao.create_request(board, g.user_id)
            # flash('Board created')
            return redirect(url_for('get_all_requests'))
        return redirect(url_for('add_request'))
    return render_template('requests.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011, debug=True)
