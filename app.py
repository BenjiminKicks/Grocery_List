#imports
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# My App
app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


# Data Class - Row of data

class my_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self) -> str:
        return f"Item {self.id}"




# Routes to main page
@app.route("/", methods=["POST","GET"])
def index():
    # Add a Item
    if request.method == "POST":
        current_item = request.form['content']
        new_item = my_list(item=current_item)
        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"

     # See all Items
    else:
        items = my_list.query.order_by(my_list.created).all()
        return render_template("index.html", items=items)
        




#Dunner and Debugger
if __name__ in "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)