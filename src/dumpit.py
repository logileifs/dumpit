from flask import Flask
#import config as cfg

app = Flask(__name__)


@app.route('/')
def index():
	return 'hello again =)'
