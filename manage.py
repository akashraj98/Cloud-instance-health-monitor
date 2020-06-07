# !/usr/bin/env python3

from flask import Flask, json


api = Flask(__name__)

if __name__ == '__main__':
    api.run()