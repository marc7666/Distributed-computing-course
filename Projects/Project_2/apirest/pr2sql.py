import sys
from flask import Flask, redirect, url_for, request, jsonify, Response
import json
# from bson.json_util import dumps
from jsonschema import validate
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import socket
from mysql.connector import Error
import mysql.connector
from mysql.connector import errorcode
import pymongo

global DB
global COLLECTION

app = Flask(__name__)
CORS(app)

home_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "address":  {"type": "string"},
        "description": {"type": "string"},
        "home_ownerid": {"type": "integer"},
    },
    "required": ["name", "address", "description"]
}

home_schema_update = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "address":  {"type": "string"},
        "description": {"type": "string"},
        "home_ownerid": {"type": "integer"},
        "homeid": {"type": "integer"},
    },
    "required": ["home_ownerid", "homeid"]
}

sensor_schema = {
    "type": "object",
    "properties": {
        "sensorID": {"type": "string"},
        "room":  {"type": "string"},
        "homeid":  {"type": "integer"},
    },
    "required": ["sensorID", "room", "homeid"]
}

homeowner_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "password":  {"type": "string"},
    },
    "required": ["name", "password"]
}

bulkImport_schema = {
    "type": "object",
    "properties": {
        "Home_owner": {"type": "array"},
        "Home": {"type": "array"},
        "Sensor": {"type": "array"},
    }
}

"""A_bulkImport_schema = {
    "type": "object",
    "properties": {
        "type": "array",
        "items": [{homeowner_schema},
                  {home_schema},
                  {sensor_schema},
                  ]
    }
}"""


def insert_in_db(sql):
    # insert data into
    try:
        cursor = DB.cursor()
        cursor.execute(sql)
        DB.commit()
        return 1
    except mysql.connector.Error as err:
        print(err)
        return err


def select_from_db(sql):
    # select data from database
    try:
        cursor = DB.cursor()
        cursor.execute(sql)
        # this will extract row headers
        row_headers = [x[0] for x in cursor.description]
        rv = cursor.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json_data
    except mysql.connector.Error as err:
        print(err)
        print(TypeError(err))
        return err


def delete_from_db(sql):
    # delete data from database
    try:
        cursor = DB.cursor()
        cursor.execute(sql)
        DB.commit()
        return 1
    except mysql.connector.Error as err:
        print(err)
        return err


def update_in_db(sql):
    # update data from database
    try:
        cursor = DB.cursor()
        cursor.execute(sql)
        DB.commit()
        return 1
    except mysql.connector.Error as err:
        print(err)
        return err


def swagger():
    # URL for exposing Swagger UI (without trailing '/')
    SWAGGER_URL = '/api/docs'
    # Our API url (can of course be a local resource)
    API_URL = '/static/swagger.json'

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        SWAGGER_URL,
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Practica 2"
        },
    )
    app.register_blueprint(swaggerui_blueprint)

# define POST method to create a new home


@ app.route('/home', methods=['POST', 'PUT', 'DELETE', 'GET'])
def home():
    if request.method == 'POST':
        # get the data from the body
        data = request.get_json()
        print(data)
        info = json.dumps(data)
        # validate the data
        try:
            validate(instance=data, schema=home_schema)
        except:
            return jsonify({"message": "Invalid data"}), 400
        # insert data to database
        # check if key exists in dictionary
        if 'home_ownerid' not in data:
            home_ownerid = 1
        else:
            home_ownerid = data["home_ownerid"]
        sql = "INSERT INTO Home (name, address, description, home_ownerid) VALUES ('" + \
            data["name"] + "', '" + data["address"] + "', '" + \
            data["description"] + "', '" + str(home_ownerid) + "')"
        res = insert_in_db(sql)
        if res == 1:
            # s'ha de retornar el homeid també
            return jsonify({"message": "Home created " + info}), 201
        else:
            return jsonify({"message": "Error creating home "}), 500

    elif request.method == 'PUT':
        data = request.get_json()
        print(data)
        info = json.dumps(data)
        try:
            validate(instance=data, schema=home_schema_update)
        except:
            return jsonify({"message": "Invalid data"}), 400
        # update data in database
        sql = "UPDATE Home SET "
        if 'name' in data:
            sql = sql + "name = '" + data["name"]+"'"
            if sql != "UPDATE Home SET " and ('address' in data or 'description' in data):
                sql = sql + " , "
        if 'address' in data:
            sql = sql + "address = '" + data["address"]+"'"
            if sql != "UPDATE Home SET " and ('description' in data):
                sql = sql + " , "
        if 'description' in data:
            sql = sql + "description = '" + data["description"]+"'"
        if sql != "UPDATE Home SET ":
            sql = sql + " WHERE homeid = '" + str(data["homeid"]) + \
                "' and home_ownerid = '" + str(data["home_ownerid"]) + "'"
            print(sql)
            res = update_in_db(sql)
            if res == 1:
                return jsonify({"message": "Home updated " + info}), 200
            else:
                return jsonify({"message": "Error updating home " + str(sql)}), 500
        else:
            return jsonify({"message": "Nothing to update"}), 406

    elif request.method == 'DELETE':
        data = request.get_json()
        print(data)
        info = json.dumps(data)
        # delete data from database
        sql = "DELETE FROM Home WHERE homeid = '" + str(data["homeid"]) +\
            "' and home_ownerid = " + str(data["home_ownerid"])+""
        res = delete_from_db(sql)
        if res == 1:
            return jsonify({"message": "Home deleted " + info}), 200
        else:
            return jsonify({"message": "Error deleting home "+ res}), 500

    elif request.method == 'GET':
        req_info = request.args.items()
        criteria_value = "0"
        for arg in req_info:
            criteria_search = arg[0]
            criteria_value = arg[1]
            print(arg[0])
            print(arg[1])
        # criteria_value = request.args.get('name')
        info = json.dumps(criteria_value)
        print(info)
        try:
            if criteria_value == "0":
                # get all homes
                sql = "SELECT * FROM Home"
                result = select_from_db(sql)
                return jsonify(result), 200
            else:
                # get home
                sql = "SELECT * FROM Home WHERE " + criteria_search + \
                    " = '" + criteria_value + "'"
                result = select_from_db(sql)
                return jsonify(result), 200
        except:
            return jsonify(message="Unable to get data " + str(sql)), 500


@ app.route('/home/prts/<criteria>/<value>', methods=['GET'])
def search_partial(criteria, value):
    # get home
    try:
        sql = "SELECT * FROM Home WHERE " + criteria + \
            " LIKE '%" + value + "%'"
        result = select_from_db(sql)
        return jsonify(result), 200
    except:
        return jsonify(message="Unable to get data"), 500


@ app.route('/sensor', methods=['POST', 'DELETE'])
def sensor():
    if request.method == 'POST':
        # get the data from the body
        data = request.get_json()
        print(data)
        info = json.dumps(data)
        try:
            validate(instance=data, schema=sensor_schema)
        except:
            return jsonify({"message": "Invalid data"}), 400
        # insert data to database
        sql = "INSERT INTO Sensor (sensorID, room, homeid) VALUES ('" + \
            data["sensorID"] + "', '" + data["room"] + "', '" + \
            str(data["homeid"]) + "')"
        res = insert_in_db(sql)
        if res == 1:
            return jsonify({"message": "Sensor created " + info}), 201
        else:
            return jsonify({"message": "Error creating sensor " + str(res)}), 500

    elif request.method == 'DELETE':
        req_info = request.args.items()
        criteria_value = "0"
        for arg in req_info:
            criteria_search = arg[0]
            criteria_value = arg[1]
            print(arg[0])
            print(arg[1])
        print(criteria_value)
        info = json.dumps(criteria_value)
        data = request.get_json()
        print(data)
        # delete data from database
        sql = "DELETE FROM Sensor s inner join Home h on s.homeid = h.homeid WHERE s." + criteria_search + \
            " = '" + criteria_value + "' and s.homeid = " + \
            data["homeid"] + "and h.home_ownerid = " + data["home_ownerid"]
        res = delete_from_db(sql)
        if res == 1:
            return jsonify({"message": "Sensor deleted " + info}), 200
        else:
            return jsonify({"message": "Error deleting sensor "}), 500


@ app.route('/home/<homeid>/sensor', methods=['GET'])
def sensorlist(homeid):
    # data = request.args.get('home')
    # info = json.dumps(data)
    # print(info)
    # get sensor from homeid
    sql = "SELECT * FROM Sensor WHERE homeid = " + homeid + ""
    print(sql)
    try:
        result = select_from_db(sql)
        return jsonify(result), 200
    except:
        return jsonify(message="Unable to get data"), 500


@ app.route('/homeowner', methods=['GET', 'POST'])
def homeowner():
    if request.method == 'GET':
        # get a homeoner
        print("GET")
        data = request.get_json()
        print(data)
        info = json.dumps(data)
        print("GET2")
        try:
            validate(instance=data, schema=homeowner_schema)
        except:
            return jsonify({"message": "Invalid data"}), 400
        # select a homeowner in database
        sql = "SELECT * FROM Home_Owner WHERE name = '" + data["name"] + "'"
        print(sql)
        try:
            result = select_from_db(sql)
            return jsonify(result[0]), 200
        except:
            return jsonify({"message": "Error getting homeowner "}), 500
    elif request.method == 'POST':
        # get the data from the body
        data = request.get_json()
        print(data)
        info = json.dumps(data)
        try:
            validate(instance=data, schema=homeowner_schema)
        except:
            return jsonify({"message": "Invalid data"}), 400
        # insert data to database
        sql = "INSERT INTO Home_Owner (name, password) VALUES ('" + \
            data["name"] + "', '" + data["password"] + "')"
        print(sql)
        if insert_in_db(sql) == 1:
            return jsonify({"message": "Home Owner created " + info}), 201
        else:
            return jsonify({"message": "Error creating home owner "}), 500


@app.route('/homeowner/check/<home_ownerid>', methods=['GET'])
def check_hoid(home_ownerid):
    sql = "SELECT * FROM Home_Owner WHERE home_ownerid = " + str(home_ownerid)
    print(sql)
    try:
        result = select_from_db(sql)
        if result == []:
            return jsonify({"message": "Home Owner not found"}), 404
        else:
            return jsonify({"message": "Home Owner found"}), 200
    except:
        return jsonify(message="Unable to get data"), 500


@ app.route('/homeowner/<home_ownerID>/homes', methods=['GET'])
def list_user_homes(home_ownerID):
    # get all homes from a homeowner
    sql = "SELECT * FROM Home WHERE home_ownerid = '" + home_ownerID + "'"
    try:
        result = select_from_db(sql)
        return jsonify(result), 200
    except:
        return jsonify(message="Unable to get data"), 500


@ app.route('/alldata', methods=['GET','POST'])
def list_all_data():
    if request.method == 'GET':
        # get all homes from a homeowner
        sql = "SELECT * FROM Home_Owner ho left join Home h on ho.home_ownerid = h.home_ownerid left join Sensor s on h.homeid = s.homeid"
        print(sql)
        try:
            result = select_from_db(sql)
            return jsonify(result), 200
        except:
            return jsonify(message="Unable to get data"), 500
    if request.method == 'POST':
        data = request.get_json()
        info = json.dumps(data)
        print(data)
        try:
            if 'home_owner' in data:
                ho = data['home_owner']
                for elem in ho:
                    sql = 'insert into Home_Owner (name, password) values ("'+elem['name']+'","'+elem['password']+'")'
                    print(sql)
                    insert_in_db(sql)
            if 'home' in data:
                h = data['home']
                for elem in h:
                    sql = 'insert into Home (name, address, description, home_ownerid) values ("'+elem['name']+'","'+elem['address']+'","'+elem['description']+'","'+str(elem['home_ownerid'])+')'
                    print(sql)
                    insert_in_db(sql)
            if 'sensor' in data:
                s = data['sensor']
                for elem in s:
                    sql = 'insert into Sensor (sensorID, room, homeid) values ("'+elem['sensorID']+'","'+elem['room']+'",'+str(elem['homeid'])+')'
                    print(sql)
                    insert_in_db(sql)
            return jsonify({"message": "Added Successfully" }), 200
        except:
            return jsonify({"message": "Invalid data"}), 400

@app.route('/sensor/<sensorID>', methods=['GET'])
def get_sensor_temp(sensorID):
    try:
        client = pymongo.MongoClient(
            "mongodb://marc:2022@192.168.10.102:27017/")
        db = client["temperatures"]
        COLLECTION = db["temperatures"]
        print("Connected successfully to the MongoDB")
        result = COLLECTION.find({"sensorID": sensorID})
        return jsonify(result), 200
    except:
        print("Unable to connect with the specified DB")
    # get temperatures from sensor in mongoDB
    try:
        """result = COLLECTION.find({"sensorID": sensorID})"""
        client.close()
        if not result:
            return jsonify({"message": "Sensor not found"}), 404
        else:
            return jsonify(result), 200
    except:
        client.close()
        return jsonify(message="Unable to get data"), 500


if __name__ == '__main__':
    # connect_to_db()
    try:
        DB = mysql.connector.connect(
            host="mysqldb", user="root", password="root", database="pr2")
        print("Connected to database")
    except mysql.connector.Error as err:
        print("Error connecting to database")
        print(err)
    swagger()
    hostname = socket.gethostname()  # Getting the hostname
    IPAddr = socket.gethostbyname(hostname)  # Obtaining the container IP
    # Running the app in the container IP and port 5000
    app.run(host=IPAddr, port=5000, debug=True)
