from flask import Flask, render_template, request, redirect
import os, json
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ================= HOME =================
@app.route("/")
def home():
    return render_template("login.html")


# ================= LOGIN =================
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    if email == "avn_aids2@gmail.com" and password == "12345":
        return redirect("/form")
    else:
        return "Wrong login ❌"


# ================= FORM =================
@app.route("/form")
def form():
    return render_template("form.html")


# ================= GENERATE =================
@app.route("/generate", methods=["POST"])
def generate():
    name = request.form.get("name")

    if not name:
        return "Name is required ❌"

    # ==== PHOTO UPLOAD ====
    photo_file = request.files.get("photo")
    filename = ""

    if photo_file and photo_file.filename != "":
        filename = secure_filename(photo_file.filename)
        photo_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        photo_file.save(photo_path)

    # ==== USER DATA ====
    user = {
        "name": name,
        "about": request.form.get("about"),
        "skills": request.form.get("skills"),
        "projects": request.form.get("projects"),
        "contact": request.form.get("contact"),
        "photo": filename,
        "github": request.form.get("github"),
        "instagram": request.form.get("instagram"),
        "linkedin": request.form.get("linkedin"),
    }

    # ==== SAVE TO data.json ====
    try:
        with open("data.json", "r") as f:
            db = json.load(f)
    except:
        db = {}

    db[name] = user

    with open("data.json", "w") as f:
        json.dump(db, f, indent=4)

    return redirect(f"/portfolio/{name}")


# ================= PORTFOLIO =================
@app.route("/portfolio/<name>")
def portfolio(name):
    try:
        with open("data.json") as f:
            db = json.load(f)
    except:
        return "No data found ❌"

    user = db.get(name)

    if not user:
        return "User not found ❌"

    return render_template("portfolio.html", **user)


# ================= RUN FOR RENDER =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

