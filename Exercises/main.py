from flask import Flask, request, render_template
import requests
from database import *


app = Flask(__name__)


Feed_ID = ''
Feed_Name = ''
Provider_ID = ''
DAI = ''
AltCon = ''
AltCon_Version = ''
_224_Feed = ''
Notification_Buffer = ''
message = ''

@app.route("/main", methods=["GET","POST"])
def main():
    global Feed_ID, Feed_Name, Provider_ID, DAI, AltCon, AltCon_Version,_224_Feed, Notification_Buffer
    global message
    if request.args.get('action') == "savefeed":
        Feed_ID = request.form.get("Feed_ID")
        Feed_Name = request.form.get("Feed_Name")
        Provider_ID = request.form.get("Provider_ID")
        DAI = request.form.get("DAI")
        AltCon = request.form.get("AltCon")

        if add_feedID(Feed_ID, Feed_Name, Provider_ID, DAI, AltCon):
            message = "Successfully Added"
        else:
            message = "Failed to Add"


    return render_template('input_form.html',
                           Feed_ID=Feed_ID,
                           Feed_Name=Feed_Name,

                           message=message)

@app.route("/view", methods=["GET"])
def view():


    return Feed_ID


if __name__ == '__main__':
        print('running app...')
        app.run(host='127.0.0.1', port='7002')
        print('----app is running-----')


cur.close()