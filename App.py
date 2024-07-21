from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri)
db_name = "data"
database = client[db_name]
collection_name = 'users'
new_collection = database[collection_name]

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=["GET"])
def login():
    return render_template("form.html")

@app.route("/verify", methods=["POST"])
def verify():
    option = request.form.get("option")
    if option == "1":
        return redirect("/insertForm")
    elif option == "2":
        return redirect("/updateForm")
    elif option == "3":
        return redirect("/deleteForm")
    elif option == "4":
        return redirect("/findForm")
    else:
        return "INVALID"

@app.route("/insertForm")
def insertForm():
    return render_template("insert.html")

@app.route('/insert', methods=["POST"])
def insert():
    name = request.form.get("name")
    age = request.form.get("age")
    department = request.form.get("department")
    section = request.form.get("section")
    phone = request.form.get("phone")
    email = request.form.get("email")
    
    print(f"Received data: Name={name}, Age={age}, Department={department}, Section={section}, Phone={phone}, Email={email}")
    
    data = {
        "name": name,
        "age": age,
        "department": department,
        "section": section,
        "phone": phone,
        "email": email
    }
    
    new_collection.insert_one(data)
    return redirect("/success")

@app.route("/updateForm")
def updateForm():
    return render_template("update.html")

@app.route('/update', methods=["POST"])
def update():
    name = request.form.get("name")
    age = request.form.get("age")
    department = request.form.get("department")
    section = request.form.get("section")
    phone = request.form.get("phone")
    email = request.form.get("email")
    
    update_data = {}
    if age:
        update_data["age"] = age
    if department:
        update_data["department"] = department
    if section:
        update_data["section"] = section
    if phone:
        update_data["phone"] = phone
    if email:
        update_data["email"] = email
    
    result = new_collection.update_one({"name": name}, {"$set": update_data})
    
    if result.matched_count > 0:
        return redirect("/success")
    else:
        return "No record found to update."

@app.route("/deleteForm")
def deleteForm():
    return render_template("delete.html")

@app.route('/delete', methods=["POST"])
def delete():
    name = request.form.get("name")
    
    result = new_collection.delete_one({"name": name})
    
    if result.deleted_count > 0:
        return redirect("/success")
    else:
        return "No record found to delete."

@app.route("/findForm")
def findForm():
    return render_template("find.html")

@app.route('/find', methods=["POST"])
def find():
    name = request.form.get("name")
    result = new_collection.find_one({"name": name})
    
    if result:
        print(result)
        details = f"Name: {result.get('name')}<br>" \
                  f"Age: {result.get('age')}<br>" \
                  f"Department: {result.get('department')}<br>" \
                  f"Section: {result.get('section')}<br>" \
                  f"Phone: {result.get('phone')}<br>" \
                  f"Email: {result.get('email')}"
        return f"Yes, Details:<br>{details}"
    else:
        return "No record found in the database."

@app.route("/success")
def success():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Success</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h1>SUCCESS</h1>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
