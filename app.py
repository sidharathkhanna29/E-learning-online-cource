'''
@Author: Sidharath Khanna, Dhruvin Lad, Jagjeet Kaur Randhawa, Harshil Patel, Rohit Verma -->
@Date: 30/03/2024
@Version: 1.0.0.0
@Program: Controller for Pythonic Information System for E-Learning App by  Team GPT Masters
'''
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo, MongoClient

app = Flask(__name__)


#initialize the Flask app 
app = Flask("myapp")    # connect and create a db named as mydb
app.config["MONGO_URI"] = "mongodb://localhost:27017/course_db" #initializing the client for mongodb
mongo = PyMongo(app) # Creating  the course collection
courses_collection = mongo.db.courses # Accessing the courses collection in the database

# client = MongoClient('mongodb://localhost:27017/')
# db = client['course_db']
# courses_collection = db['courses']

# Sample data ( to be replaced with actual database integration)
courses = [
    {"id": 1, "title": "Introduction to Python", "description": "Learn the basics of Python programming."},
    {"id": 2, "title": "Advanced Python Concepts", "description": "Explore advanced topics in Python."},
]

# courses_collection.insert_many(courses)

# Route to display the index page with a list of courses
@app.route('/')
def index():
    if request.method == 'POST':
        data = request.form
        print('Form Data Received',data)
    return render_template('index.html', courses=courses)

# Route to handle adding a new course
@app.route('/add_course', methods=['POST'])
def add_course():
    # Create a new course dictionary using form data
    new_course = {
        "id": len(courses) + 1,         # Generating a unique ID for the new course
        "title": request.form['title'],
        "description": request.form['description']
    }
    # Adding the new course to the courses list
    courses.append(new_course)
    # Adding it into DB 
    data = request.form
    courses_collection.insert_one(new_course)
    # courses_collection.insert_one({'title': data['title']}, {'description' : data['description']})
    # Redirecting to the index page after adding the course
    return redirect(url_for('index'))

# Route to handle editing an existing course
@app.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    # Checking if the form is submitted with updated course information
    if request.method == 'POST':
        # Updating the course details in the courses list
        for course in courses:
            if course['id'] == course_id:
                course['title'] = request.form['title']
                course['description'] = request.form['description']
                
                # courses_collection.update_many( {"title": course['title']}, {'description' : course['description']})
                result = courses_collection.insert_one({'title': course['title']}, {'description' : course['description']})

                # if result.modified_count == 1:
                #     print({'message': 'Course updated successfully'})
                # else:
                #     print({'message': 'Course not found'})

                break
        # Redirecting to the index page after editing the course
        return redirect(url_for('index'))
    else:
        # Displaying the edit course form with pre-filled data
        for course in courses:
            if course['id'] == course_id:
                return render_template('edit_course.html', course=course)

# Route to handle deleting a course
@app.route('/delete_course/<int:course_id>')
def delete_course(course_id):
    global courses
    # Removing the course with the specified ID from the courses list
    courses = [course for course in courses if course['id'] != course_id]
    # Redirecting to the index page after deleting the course
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
