from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Sample data (replace with actual database integration)
courses = [
    {"id": 1, "title": "Introduction to Python", "description": "Learn the basics of Python programming."},
    {"id": 2, "title": "Advanced Python Concepts", "description": "Explore advanced topics in Python."},
]

@app.route('/')
def index():
    return render_template('index.html', courses=courses)

@app.route('/add_course', methods=['POST'])
def add_course():
    new_course = {
        "id": len(courses) + 1,
        "title": request.form['title'],
        "description": request.form['description']
    }
    courses.append(new_course)
    return redirect(url_for('index'))

@app.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    if request.method == 'POST':
        for course in courses:
            if course['id'] == course_id:
                course['title'] = request.form['title']
                course['description'] = request.form['description']
                break
        return redirect(url_for('index'))
    else:
        for course in courses:
            if course['id'] == course_id:
                return render_template('edit_course.html', course=course)

@app.route('/delete_course/<int:course_id>')
def delete_course(course_id):
    global courses
    courses = [course for course in courses if course['id'] != course_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
