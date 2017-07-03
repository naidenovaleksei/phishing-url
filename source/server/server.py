from flask import Flask
app = Flask(__name__)

from checking import UrlChecker

checker = UrlChecker()
is_valid = False

@app.route('/')
def get_status():
    return 'Phishing-url service. Status: %s' % ('VALID' if is_valid else 'INVALID')
	
@app.route('/check', methods=['POST', 'GET'])
def check():
    from flask import request
    url = request.args.get('url', '')
    return 'url: %s <br> status: %s' % (url, checker.get_status(url))