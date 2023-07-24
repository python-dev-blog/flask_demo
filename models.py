from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    students = db.relationship("Student", backref='group', lazy=True)

    def __repr__(self):
        return f"<Group {self.name}>"


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date)
    male = db.Column(db.Boolean, nullable=False, default=True)

    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))

    def __repr__(self):
        return f"<Student {self.first_name} {self.last_name}>"
