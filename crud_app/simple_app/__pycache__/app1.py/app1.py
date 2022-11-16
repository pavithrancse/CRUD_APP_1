#required Modules
from flask import Flask , jsonify ,request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import logging
import pandas as pd
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS

#creating instance for app
app=Flask(__name__)

#Mongo Url for connection ---> Edu venunaalu kudukalaaam //online or offline
#app.config['mongodb+srv://parthiban:<pavithran>@cluster0.hcv2bhw.mongodb.net/?retryWrites=true&w=majority']="http://127.0.0.1:5000/"
#mongo =PyMongo(app)
con_string = "mongodb+srv://parthiban:<parthiban>@cluster0.hcv2bhw.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_string)

db = client.get_database('database')

user_collection = pymongo.collection.Collection(db, 'collection') #(<database_name>,"<collection_name>")
print("MongoDB connected Successfully")



#CRUD(Create ,Read ,Update ,Delete) operations inside routes 
@app.route("/add",methods=["POST"]) 

#1.Create Operation
#postman input in body :
# {"name":"Abishaik",
# "age":21
# }
def add_value():
    #Getting Input from User (Postman) in JSON format
    jsonvalue = request.json
    #Picking the data from Variable
    namevalue =jsonvalue["name"]
    agevalue = jsonvalue["age"]

    # If its Correct
    if namevalue and agevalue and request.method=="POST":
        #Query
        id=mongo.db.user.insert({"name":namevalue,"age":agevalue})
        resp =jsonify("Process done")
        resp.status_code =200
        return resp 
    # While Error    
    else:
        return not_found()

#2.Read Operation
@app.route("/show") 
def show():
    #for processing Query
    show = mongo.db.user.find()
    #to get data
    resp =dumps(show)
    return resp

#seperate ID is read by this (#ID is Specific for data in MONGODB)
@app.route("/show/<id>")
def showid(id):
    # here ObjectId() is a Method to call id given as argument in function----Query
    user =mongo.db.user.find_one({"_id":ObjectId(id)})
    resp =dumps(user)
    return resp

#3.Update Operation
#here we can use either "PUT" or "PATCH"
#postman input in body :
# {"name":"Abishaik",
# "age":22
# }
@app.route("/update/<id>",methods=["PUT"])
def updatevalue(id):
    _id = id
    _json =request.json
    _name =_json['name']
    _age =_json['age']
    
    if _name and _age and _id and request.method=="PUT":
        #Query
        user =mongo.db.user.update({"_id":ObjectId(_id['$oid']) if "$oid" in _id else ObjectId(_id)},{"$set":{"name":_name,"age":_age}})
        resp =jsonify(user)
        resp.status_code = 200
        return(resp)
    else:
        return not_found()    

#4.Delete Operation
@app.route("/delete/<id>",methods=["DELETE"])
def deleteval(id):
    #Query
    mongo.db.user.delete_one({"_id":ObjectId(id)})
    resp =jsonify("Deleted Abi")
    resp.status_code =200
    return resp

#In case of some rough errors (EG: if the database is deleted Mnually )
@app.errorhandler(404)
def not_found(error=None):
    message ={
        "status":404,
        "message":"not valid Abi"
    }      
    resp = jsonify(message)
    resp.status_code=404

    return resp


#Implementation of code to run standalone
if __name__=="__main__":
    app.run(debug=True)

