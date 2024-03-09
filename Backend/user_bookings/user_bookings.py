
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root@localhost:3306/userbooking"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "userbooking"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.String(64), nullable=False)
    class_id = db.Column(db.Integer, nullable=False)

    def __init__(self, userid, class_id):
        self.userid = userid
        self.class_id = class_id

    def json(self):
        return {
            "id": self.id,
            "userid": self.userid,
            "class_id": self.class_id,
        }

@app.route('/user', methods=['POST'])
def add_Booked_Class():
    try:
        data = request.get_json()
        user_id = data.get('userId')
        selected_fitness_classes = data.get('selectedFitnessClasses')

        print(f"Received data: {data}") 
        if not user_id or not selected_fitness_classes:
            print("Missing required parameters.")
            return jsonify({"code": 400, "message": "Missing required parameters."}), 400

        classes = []
        for class_id in selected_fitness_classes:
            # Save the provided details to the database
            user = User(userid=user_id, class_id=class_id)
            db.session.add(user)
            classes.append(user.json())

            print(f"User details added for class_id {class_id}")

        db.session.commit()

        return jsonify({"message": "User's selected fitness classes updated successfully", "classes": classes}), 200

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"code": 500, "message": f"Internal Server Error: {str(e)}"}), 500




@app.route('/user/bookedClasses/<user_id>', methods=['GET'])
def get_booked_classes(user_id):
    try:
        # Query the database to get all booked classes for the specified user
        booked_classes = User.query.filter_by(userid=user_id).all()

        # Check if there are any booked classes
        if not booked_classes:
            return jsonify({"code": 404, "message": "No booked classes found for the user."}), 404

        # List to store details of booked classes
        booked_classes_details = []

        # Iterate through booked classes and fetch class IDs
        for booked_class in booked_classes:
            class_id = booked_class.class_id

            # Append class ID to the list
            booked_classes_details.append({"class_id": class_id})

        return jsonify({"code": 200, "data": {"booked_classes": booked_classes_details}})

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"code": 500, "message": f"Internal Server Error: {str(e)}"}), 500








if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
