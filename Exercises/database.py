import sqlite3

con = sqlite3.connect('feeds.sqlite',check_same_thread=False)
cur = con.cursor()

# cur.execute('''CREATE TABLE feed_info(
#             Feed_ID TEXT(20) PRIMARY KEY)''')
#             # Feed_Name TEXT(25),
#             # Provider_ID TEXT(25),
#             # DAI INTEGER(1),
#             # AltCon_Version TEXT(20),
#             # _224_Feed TEXT(20),
#             # Notification_Buffer INTEGER
#             # )''')

def add_FeedID(feedid):
    while con:
        cur.execute("INSERT INTO feed_info VALUES(:Feed_ID)",{'Feed_ID': feedid})
        con.commit()
        return True

    return False

# cur.execute("DROP TABLE feed_info")

