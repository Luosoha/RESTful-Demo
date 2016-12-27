from flask import Flask
import mlab
from mongoengine import *
from flask_restful import Resource, Api, reqparse
import json

mlab.connect()

class Note(Document):
    title = StringField()
    content = StringField()

# n = Note(title = "First note", content = "Blah blah blah")
# n.save()
#
# for note in Note.objects:
#     print(note.to_json())

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("title", type=str, location="json")
parser.add_argument("content", type=str, location="json")


@app.route('/')
def hello_world():
    return 'Hello World!'


class NoteListRes(Resource):
    def get(self): # GET ALL NOTES
        return mlab.list2json(Note.objects)

    def post(self): # POST NEW NOTE
        args = parser.parse_args()
        title = args["title"]
        content = args["content"]
        new_note = Note(title=title, content=content)
        new_note.save()
        return mlab.item2json(new_note)

class NoteRes(Resource):
    def get(self, note_id):
        all_notes = Note.objects
        found_note = all_notes.with_id(note_id)
        return mlab.item2json(found_note)

    def delete(self, note_id):
        all_notes = Note.objects
        found_note = all_notes.with_id(note_id)
        found_note.delete()
        return {"code": 1, "status": "OK"}, 200

    def put(self, note_id):
        #parse args
        args = parser.parse_args()
        title = args["title"]
        content = args["content"]

        #find note
        all_notes = Note.objects
        found_note = all_notes.with_id(note_id)

        #
        found_note.update(set__title=title, set__content=content)
        return {"code": 1, "status": "OK"}, 200

api.add_resource(NoteListRes, "/api/note")
api.add_resource(NoteRes, "/api/note/<note_id>") #note_id in line 46

if __name__ == '__main__':
    app.run()
