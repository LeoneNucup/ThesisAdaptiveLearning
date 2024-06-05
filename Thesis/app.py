import datetime
from flask import Flask, render_template, request, jsonify
import json
from lstm_model import predict_score
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///scores.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("scores", lazy=True))
    date = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, nullable=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        pre_test_score = float(request.form["pre_test_score"])
        current_score = float(request.form["current_score"])

        data = json.dumps({"pre_test": pre_test_score, "current": current_score})

        predicted_score, difficulty_level = predict_score(data)

        # Record the user's score and store it in the database
        score_entry = Score(user_id=1, date=datetime.now(), score=current_score, question_id=1)
        db.session.add(score_entry)
        db.session.commit()

        return render_template("result.html", predicted_score=predicted_score, difficulty_level=difficulty_level)

if __name__ == "__main__":
    app.run(debug=True)
