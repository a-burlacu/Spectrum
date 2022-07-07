from flask import Flask, request, render_template
import requests
from database import *


app = Flask(__name__)


Feed_ID = ''
Feed_Name = ''
Provider_ID = ''
DAI = ''
AltCon_Version = ''
_224_Feed = ''
Notification_Buffer = ''
message = ''

@app.route("/main", methods=["GET","POST"])
def main():
    global Feed_ID, Feed_Name, Provider_ID, DAI, AltCon_Version,_224_Feed, Notification_Buffer
    global message
    if request.args.get('action') == "savefeed":
        Feed_ID = request.form.get("Feed_ID")
        if add_FeedID(Feed_ID):
            message = "Successfully Added"
        else:
            message = "Failed to Add"


    return render_template('input_form.html', Feed_ID=Feed_ID,message=message)

@app.route("/view", methods=["GET"])
def view():


    return Feed_ID


if __name__ == '__main__':
        print('running app...')
        app.run(host='0.0.0.0', port='7002')
        print('----app is running-----')


cur.close()