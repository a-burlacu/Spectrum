from flask import Flask, request, render_template, redirect, abort, flash, url_for
import requests
from database import *
app = Flask(__name__)

message = ''

@app.route("/main", methods=["GET","POST"])
def main():
    Feed_ID = ''
    Feed_Name = ''
    Provider_ID = ''
    DAI = ''
    AltCon = ''
    AltCon_Version = ''
    _224_Feed = ''
    Notification_Buffer = ''
    global message

    error = None

    if request.args.get('action') == "savefeed":
        Feed_ID = request.form.get("Feed_ID")
        Feed_Name = request.form.get("Feed_Name")
        Provider_ID = request.form.get("Provider_ID")
        DAI = request.form["DAI"]
        AltCon = request.form["AltCon"]
        AltCon_Version = request.form.get("AltCon_Version")
        if AltCon_Version == '' :
            AltCon_Version = 'NULL'

        _224_Feed = request.form.get("_224_Feed")
        if _224_Feed == '':
            _224_Feed = 'NULL'

        Notification_Buffer = request.form.get("Notification_Buffer")
        if Notification_Buffer == '':
            Notification_Buffer = 'NULL'

        if add_feed(Feed_ID, Feed_Name, Provider_ID, DAI, AltCon,AltCon_Version,_224_Feed,Notification_Buffer):
            message = "Successfully Added"
            #return redirect(url_for('main'))
            return redirect(request.referrer)
        else:
            message = "Failed to Add"
            raise internal_error()


    return render_template('input_form.html',
                       Feed_ID=Feed_ID,
                       Feed_Name=Feed_Name,
                       DAI=DAI,
                       AltCon=AltCon,
                       AltCon_Version=AltCon_Version,
                       _224_Feed=_224_Feed,
                       message=message)





@app.route("/view", methods=["GET"])
def view():

    Table_Data =get_feed()

    return render_template('display_form.html',
                           table_data=Table_Data)


# return render_template('display_form.html',
#                        Feed_ID=Feed_ID,
#                        Feed_Name=Feed_Name,
#                        DAI=DAI,
#                        AltCon=AltCon,
#                        AltCon_Version=AltCon_Version,
#                        _224_Feed=_224_Feed,
#                        )



# override Internal Server Error message
@app.errorhandler(500)
def internal_error(error):
    return render_template('Error_500.html'),500

if __name__ == '__main__':
        print('running app...')
        app.run(host='', port='7002')
        print('----app is running-----')


cur.close()