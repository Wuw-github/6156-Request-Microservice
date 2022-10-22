from flask import Flask, request, jsonify, make_response, g
from request_resource import RequestDAO


app = Flask(__name__)



def get_request_dao():
    if not hasattr(g, 'dao'):
        g.dao = RequestDAO()
    return g.dao

