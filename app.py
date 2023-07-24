import time

from flask import Flask, render_template, request, redirect, url_for, g
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy import event

from schemas import StudentSchema
from models import db, Group, Student

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


@app.before_request
def before_request():
    g.start_time = time.time()


@app.after_request
def after_request(response):
    total_time = time.time() - g.start_time
    print(f"Время выполнения запроса {total_time:.6f} секунд")
    return response


def log_db_queries(app):
    @event.listens_for(db.engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        # Выводим запросы к базе данных в консоль
        print("Executing query: %s", statement)


with app.app_context():
    log_db_queries(app)


@app.route("/", methods=["GET"])
def home():
    return {"status": "ok"}


@app.route("/groups")
def show_groups():
    return render_template("groups.html", groups=Group.query.all())


@app.route("/students/<int:group_id>")
def show_students(group_id):
    return render_template(
        "students.html",
        students=Student.query.filter_by(group_id=group_id).all(),
        group=Group.query.get(group_id))


@app.route("/create_group", methods=["GET", "POST"])
def create_group():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]

        new_group = Group(name=name, description=description)
        db.session.add(new_group)
        db.session.commit()
        return redirect(url_for("show_groups"))
    else:
        return render_template("create_group.html")


@app.route("/create_student", methods=["GET", "POST"])
def create_student():
    if request.method == "POST":
        data = request.form
        schema = StudentSchema()

        try:
            result = schema.load(data)
        except ValidationError as error:
            return render_template("create_student.html", errors=error.messages, data=data)

        new_student = Student(
            first_name=result["first_name"],
            last_name=result["last_name"],
            birth_date=result["birth_date"],
            group_id=result["group_id"]
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for("show_groups"))
    else:
        return render_template("create_student.html", groups=Group.query.all())


if __name__ == "__main__":
    app.run(debug=True)
