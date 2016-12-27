import mongoengine

#mongodb://<dbuser>:<dbpassword>@ds145118.mlab.com:45118/mynotes123

host = "ds145118.mlab.com"
port = 45118
db_name = "mynotes123"
user_name = "admin"
password = "admin"

def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]

def item2json(item):
    import json
    return json.loads(item.to_json())