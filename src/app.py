from flask import Flask, Response, request, g, render_template, url_for, redirect, flash
import json
from requestDAO import RequestDAO
from requestBoard import RequestBoard
from response_service import Paginate, Hateoas
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt, verify_jwt_in_request

app = Flask(__name__)
app.secret_key = 'it-is-hard-to-guess'
CORS(app)
jwt = JWTManager(app)



dao = RequestDAO()

WHITE_LIST = {
    "get_all_requests": {"GET"},
    "get_request_by_id": {"GET"},
    }

@app.before_request
def check_user_login():    
    if request.endpoint in WHITE_LIST and request.method in WHITE_LIST[request.endpoint]:
        return
    verify_jwt_in_request()
    user_id = get_jwt()['sub']
    g.user_id = user_id
    print(user_id)


@app.route("/requests", methods=["GET"])
def get_all_requests():

    paginate_param = Paginate.parse_paginate_input_params(request.args)
    
    result = dao.fetch_all_requests_v2(request.args, paginate_param)
    rsp = {}
    Paginate.paginate2(request.path, result, paginate_param, rsp)
    Hateoas.link_request_to_participants_by_id(rsp)
    if rsp['data']:
        rsp = Response(json.dumps(rsp, default=str), status=200, content_type="app.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@app.route("/requests/<request_id>", methods=["GET", "PUT"])
def get_request_by_id(request_id):
    if request.method == "GET":
        rsp = {}
        result = dao.fetch_request_by_id(request_id)
        if result:
            rsp = {'data': [result]}
            Hateoas.link_request_to_participants_by_id(rsp)
            rsp = Response(json.dumps(rsp, default=str), status=200, content_type="app.json")
        else:
            rsp = {"message": "request not found"}, 404

        return rsp

    if g.user_id is None:
        return {"message": "Please log in first..."}, 401
    if request.method == "PUT":
        board = process_form_for_board(request)
        try:
            dao.update_request(request_id, board)
        except e:
            return {"message": "update failed"}, 403
        return {"message": "request updated"}, 200


@app.route("/requests/<request_id>/participants", methods=["GET", "DELETE", "POST"])
def get_participants_by_id(request_id):
    if request.method == "GET":
        rsp = dao.fetch_participants_by_request_id(request_id)
        rsp = {"data": rsp}
        Hateoas.link_participant_to_user_by_id(rsp)
        if rsp:
            rsp = Response(json.dumps(rsp, default=str), status=200, content_type="app.json")
        else:
            rsp = {"message": "Not Found"}, 404

        return rsp

    if g.user_id is None:
        return {"message": "Please log in first..."}, 401

    if request.method == "DELETE":
        try:
            dao.delete_participant(request_id, g.user_id)
        except:
            return {"message": "You have not joined this List yet."}, 403
        return {"message": "You have left"}

    if request.method == "POST":
        try:
            dao.create_participant(request_id, g.user_id)
        except:
            return {"message": "you already joined"}, 403
        return {"message": "successfully joined"}, 200

@app.route("/user/requests", methods=["GET"])
def get_requests_by_user():
    
    if g.user_id is None:
        return {"message": "Please login first..."}, 401

    paginate_param = Paginate.parse_paginate_input_params(request.args)
    result = dao.fetch_request_id_by_participants(g.user_id)
    rsp = {}
    Paginate.paginate2(request.path, result, paginate_param, rsp)
    Hateoas.link_request_id_to_request(rsp)
    if rsp:
        rsp = Response(json.dumps(rsp, default=str), status=200, content_type="app.json")
    else:
        rsp = {"message": "No request found"}
    return rsp


def process_form_for_board(request):
    data = request.form
    launch_date = data['date']
    time = data['time']
    start_location = data['start_location']
    destination = data['destination']
    description = data['description']
    capacity = data['capacity']

    board = RequestBoard(launch_date, time, start_location, destination, description, capacity)
    return board


@app.route('/requests/create', methods=['GET', "POST"])
def add_request():
    if request.method == 'POST':
        if g.user_id is None:
            return {"message": "Please log in first..."}, 401
        board = process_form_for_board(request)
        print(board.start_loc)
        if RequestBoard.checkValidation(board):
            dao.create_request(board, g.user_id)
            # flash('Board created')
            return {"message": "board is created"}, 200
        return {"message": "inputs are not valid"}, 403
    return render_template('requests.html')

@app.route('/login', methods=["POST"])
def dunmmy_login():
    return {"token": "token123456"}

@app.route('/sns_subscribe', methods=["POST"])
def subscribe_sns():
    data = request.get_json()
    return {"message": "received",
    "message": data.get('Message'),
    "subscribeURL": data.get("SubscribeURL")}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011, debug=True)
