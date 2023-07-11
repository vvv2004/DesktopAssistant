import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Database:
    def __init__(self):
        cred = credentials.Certificate("D:/Development/DesktopAssistant/secure/secure.json")
        app = firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def save_to_database(self, dictionary, collection):
        self.db.collection(collection).set(dictionary)

    def get_from_database(self, collection, identifier):
        reference = self.db.collection(collection).document(identifier)
        doc = reference.get()

        if doc.exists:
            return doc.to_dict()
        else:
            return None

    def get_collection(self, collection):
        docs = self.db.collection(collection).strean()

        return {
            collection: docs
        }

    def delete_from_database(self, collection, identifier):
        self.db.collection(collection).document(identifier).delete()

    def delete_field(self, collection, identifier, field):
        document = self.db.collection(collection).document(identifier)
        document.update({field: firestore.DELETE_FIELD})
