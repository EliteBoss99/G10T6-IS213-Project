from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests


app = Flask(__name__)
CORS(app)