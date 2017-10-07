import os
import datetime
import sqlite3

CLOUD_PATH = u'/home/medcloud/webapps/ownphp70/data/Osama/files/Medical College/'
DB_PATH = '/home/medcloud/cloud_index/'

def index():
    now = datetime.datetime.today()
    timestamp = now.strftime('%Y%m%d%H')
    db_filename = "medcloud_index-%s.sqlite" % timestamp
    db_conn = sqlite3.connect(DB_PATH + db_filename, check_same_thread=False)

    db_conn.execute('CREATE TABLE files(path TEXT, filename TEXT)')
    for path, folders, filenames in os.walk(CLOUD_PATH):
        for filename in filenames:
            relative_path = path.lstrip(CLOUD_PATH)
            db_conn.execute(u'INSERT INTO files VALUES (?, ?)', (relative_path, filename))
    db_conn.commit()

def search_index(term):
    now = datetime.datetime.today()
    timestamp = now.strftime('%Y%m%d%H')
    db_filename = "medcloud_index-%s.sqlite" % timestamp
    db_conn = sqlite3.connect(DB_PATH + db_filename, check_same_thread=False)
    raw_term_list = term.split()
    term_list = [u'%' + term + u'%' for term in raw_term_list]
    search_condition = u'SELECT * FROM files WHERE filename LIKE ?'
    term_number = len(term_list)
    if term_number > 1:
        for i in range(term_number - 1):
            search_condition += ' AND filename LIKE ?'

    results = db_conn.execute(search_condition, term_list)

    return results.fetchall()

if __name__ == '__main__':
    index()
