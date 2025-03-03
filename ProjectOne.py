# IPython log file
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

class ShelterDatabase:
    def __init__(
        self,
        user='aacuser',
        password='SNHU1234',
        host='nv-desktop-services.apporto.com',
        port=34847,
        db='aac',
        collection='shelters'
    ):
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (user, password, host, port))
        self.database = self.client[db]
        self.collection = self.database[collection]
        
    def create(self, data):
        assert data is not None, "Creation data is required"
        return self.collection.insert_one(data)

    def read(self, filter={}):
        return list(self.collection.find(filter))

    def update(self, data, rec_num=None, id=None):
        assert rec_num is not None or id is not None, "Rec number or id are required"
        if rec_num is not None:
            return self.collection.update_one({"rec_num": rec_num}, {"$set": data})
        else:
            return self.collection.update_one({"_id": ObjectId(id)}, {"$set": data})
         
    def delete(self, rec_num=None, id=None):
        assert rec_num is not None or id is not None, "Rec number or id are required"
        if rec_num is not None:
            return self.collection.delete_one({"rec_num": rec_num})
        else:
            return self.collection.delete_one({"_id": ObjectId(id)})
    
    def close_connection(self):
        self.client.close()

if __name__ == "__main__":
    db = ShelterDatabase()
    
    new_dog = {
        "rec_num": 10001,
        "age_upon_outcome": "5 Months",
        "animal_id": "A123456",
        "animal_type": "Dog",
        "breed": "Golden Retriever Mix",
        "color": "Golden",
        "date_of_birth": "2024-02-02",
        "datetime": "2024-02-02 12:30:00",
        "monthyear": "2024-02-02T12:30:00",
        "name": "Sir Dog",
        "outcome_subtype": "",
        "outcome_type": "Adoption",
        "sex_upon_outcome": "Male",
        "location_lat": 42.882673,
        "location_long": -71.573689,
        "age_upon_outcome_in_weeks": 52
    }

    inserted_dog = db.create(new_dog)
    id = inserted_dog.inserted_id
    print(f"Created Id: {id}")

    retrieved = db.read({"rec_num": new_dog["rec_num"]})
    print("\nAnimals retrieved:\n")
    for animal in retrieved:
        animal["_id"] = str(animal["_id"])
        print(json.dumps(animal, indent=2))


    updated_dog = db.update(id=id, data={"name": "Sir Doggydog"})
    verified = db.read({"_id": id})[0]
    verified["_id"] = str(verified["_id"])
    print("\nUpdated dog:\n")
    print(json.dumps(verified, indent=2))

    deleted = db.delete(id=id)
    print(f"\nDeleted count: {deleted.deleted_count}")

    db.close_connection()
    
