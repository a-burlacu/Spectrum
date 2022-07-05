from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route("/main", methods=('POST'))
def main():
    if request.args.get('action') == "getnetworks":
        provider = request.form.get("provider")


if __name__ == '__main__':
        print('running app...')
        app.run(host='0.0.0.0', port='7000')
        print('----app is running-----')
