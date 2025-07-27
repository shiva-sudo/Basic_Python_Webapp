from flask import Flask,request, jsonify
from dotenv import load_dotenv
import os
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi



load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client.test
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
collection = db['flask-db']
app = Flask(__name__)



@app.route('/submit', methods = ['POST'])
def submit():
    form_data = dict(request.json)

    collection.insert_one(form_data)

    return "Data submitted successfully"

@app.route('/api')
def view():
    data = collection.find()
    data = list(data)
    for item in data:

        print(item)
        del item['_id'] 
    data = {
        'data' : data
    }

    # return render_template('view.html',data = data)

    return jsonify(data)


if __name__ == '__main__':
    app.run(host ='0.0.0.0',port=5000,debug=True)
   