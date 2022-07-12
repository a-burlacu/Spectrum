import sqlite3

con = sqlite3.connect('feeds.sqlite',check_same_thread=False)
cur = con.cursor()


# cur.execute('''CREATE TABLE IF NOT EXISTS feed_info(
#                 Feed_ID TEXT(20) PRIMARY KEY ,
#                 Feed_Name TEXT(25),
#                 Provider_ID TEXT(25),
#                 DAI INTEGER(1),
#                 AltCon INTEGER (1),
#                 AltCon_Version TEXT(20),
#                 _224_Feed TEXT(20),
#                 Notification_Buffer INTEGER)''')

cur.execute('''CREATE TABLE IF NOT EXISTS feed_info(
                Feed_ID TEXT(20) PRIMARY KEY ,
                Feed_Name TEXT(25),
                Provider_ID TEXT(25),
                DAI INTEGER(1),
                AltCon INTEGER (1))''')

# def add_feedID(feedid, feedname, provid, dai, altcon, altconver, _224feed, notifbuff ):
#     while con:
#         cur.execute("INSERT INTO feed_info VALUES(:Feed_ID, :Feed_Name)",
#                     {'Feed_ID': feedid, 'Feed_Name': feedname, 'Provider_ID': provid,
#                      'DAI': dai, 'AltCon': altcon, 'AltCon_Version': altconver,
#                      '_224_Feed': _224feed, 'Notification_Buffer': notifbuff})
#         con.commit()
#         return True
#
#     return False

def add_feedID(feedid, feedname, provid, dai, altcon):
    while con:
        cur.execute("INSERT INTO feed_info VALUES(:Feed_ID, :Feed_Name, :Provider_ID, :DAI, :AltCon)",
                    {'Feed_ID': feedid, 'Feed_Name': feedname, 'Provider_ID': provid,
                     'DAI': dai, 'AltCon': altcon })
        con.commit()
        return True

    return False


#cur.execute("DROP TABLE feed_info")

