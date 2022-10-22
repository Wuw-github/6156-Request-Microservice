from flask import Flask, Response, request, jsonify, make_response, g
import json
from request_resource import RequestDAO

app = Flask(__name__)


def get_request_dao():
    if not hasattr(g, 'dao'):
        g.dao = RequestDAO()
    return g.dao


@app.route("/", methods=["GET"])
def get_student_by_uni():
    dao = get_request_dao()
    result = dao.fetch_all_requests()

    if result:
        rsp = Response(json.dumps(result, default=str), status=200, content_type="app.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011, debug=True)
