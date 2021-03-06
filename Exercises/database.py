import sqlite3

con = sqlite3.connect('feeds.sqlite',check_same_thread=False)
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS feed_info(
                Feed_ID TEXT(20) PRIMARY KEY ON CONFLICT ROLLBACK,
                Feed_Name TEXT(25),
                Provider_ID TEXT(25),feed_info
                DAI INTEGER(1),
                AltCon INTEGER (1),
                AltCon_Version TEXT(20),
                _224_Feed TEXT(20),
                Notification_Buffer INTEGER)''')



def add_feed(feedid, feedname, provid, dai, altcon, altconver, _224feed, notifbuff):
    with con:
        cur.execute("INSERT INTO feed_info VALUES(:Feed_ID, :Feed_Name, :Provider_ID, :DAI, "
                    ":AltCon, :AltCon_Version, :_224_Feed, :Notification_Buffer )",
                    {'Feed_ID': feedid, 'Feed_Name': feedname, 'Provider_ID': provid,
                     'DAI': dai, 'AltCon': altcon, 'AltCon_Version': altconver,
                     '_224_Feed':_224feed, 'Notification_Buffer': notifbuff})
    return True





def get_feed():
    with con:
        cur.execute("SELECT * FROM feed_info")
        rows = cur.fetchall()
        return rows






# def get_feed(feedid, feedname, provid, dai, altcon, altconver, _224feed, notifbuff):
#     with con:
#         cur.execute("SELECT * FROM feed_info WHERE(:Feed_ID, :Feed_Name, :Provider_ID, :DAI, "
#                     ":AltCon, :AltCon_Version, :_224_Feed, :Notification_Buffer )",
#                     {'Feed_ID': feedid, 'Feed_Name': feedname, 'Provider_ID': provid,
#                      'DAI': dai, 'AltCon': altcon, 'AltCon_Version': altconver,
#                      '_224_Feed':_224feed, 'Notification_Buffer': notifbuff})
#         return cur.fetchall()






# def primary_key_check(feedid):
#     with con:
#         cur.execute("BEFORE INSERT ON feed_info when")
#             return True
#         else:
#             return False

#cur.execute("DROP TABLE feed_info")

