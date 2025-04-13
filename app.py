from flask import Flask, render_template, redirect, url_for, request
import json
import os

app = Flask(__name__)

# Default progress data
DEFAULT_PROGRESS = [
    {"step": "Step 1", "title": "Learn the basics", "solved": 0, "total": 31},
    {"step": "Step 2", "title": "Sorting Techniques", "solved": 0, "total": 7},
    {"step": "Step 3", "title": "Arrays", "solved": 0, "total": 40},
    {"step": "Step 4", "title": "Binary Search", "solved": 0, "total": 32},
    {"step": "Step 5", "title": "Strings", "solved": 0, "total": 15},
]

def get_user_file(name):
    return f"{name.lower()}.json"

def load_progress(name):
    file_path = get_user_file(name)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return DEFAULT_PROGRESS.copy()

def save_progress(name, data):
    with open(get_user_file(name), "w") as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    return render_template("home.html", profiles=["yash", "ashwani"])

@app.route('/<name>', methods=["GET", "POST"])
def profile(name):
    user_data = load_progress(name)
    if request.method == "POST":
        for i in range(len(user_data)):
            key = f"solved_{i}"
            if key in request.form:
                user_data[i]["solved"] = int(request.form[key])
        save_progress(name, user_data)
        return redirect(url_for("profile", name=name))

    return render_template("profile.html", name=name.title(), progress=user_data)

if __name__ == "__main__":
    app.run(debug=True)
