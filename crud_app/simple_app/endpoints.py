import logging

from flask_pymongo import pymongo
from flask import jsonify, request
import pandas as pd

con_string = "mongodb+srv://parthiban:parthiban@cluster0.hcv2bhw.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_string)

db = client.get_database('User')

user_collection = pymongo.collection.Collection(db, 'user') #(<database_name>,"<collection_name>")
print("MongoDB connected Successfully")


def project_api_routes(endpoints):
    @endpoints.route('/hello', methods=['GET'])
    def hello():
        res = 'Hello world'
        print("Hello world")
        return res

    @endpoints.route('/register-user', methods=['POST'])
    def register_user():
        resp = {}
        try:
            req_body = request.json
            # resp['hello'] = hello_world
            # req_body = req_body.to_dict()
            user_collection.insert_one(req_body)            
            print("User Data Stored Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Stored Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp


   

    @endpoints.route('/read-users',methods=['GET'])
    def read_users():
        resp = {}
        try:
            users = user_collection.find({})
            print(users)
            users = list(users)
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Retrieved Successfully from the Database."
            }
            output = [{'Name' : user['name'], 'Email' : user['email']} for user in users]   #list comprehension
            resp['data'] = output
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp

    @endpoints.route('/update-users',methods=['PUT'])
    def update_users():
        resp = {}
        try:
            req_body = request.json
            # req_body = req_body.to_dict()
            user_collection.update_one({"id":req_body['id']}, {"$set": req_body['updated_user_body']})
            print("User Data Updated Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Updated Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp    

    @endpoints.route('/delete',methods=['DELETE'])
    def delete():
        resp = {}
        try:
            delete_id = request.args.get('delete_id')
            user_collection.delete_one({"id":delete_id})
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Deleted Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp
    
    @endpoints.route('/file_upload',methods=['POST'])
    def file_upload():
        resp = {}
        try:
            req = request.form
            file = request.files.get('file')
            df = pd.read_csv(file)
            print(df)
            print(df.head)
            print(df.columns())
            status = {
                "statusCode":"200",
                "statusMessage":"File uploaded Successfully."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp


    return endpoints
