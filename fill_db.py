import random
from faker import Faker

from models import Group, Student

fake = Faker()


def generate_random_groups_and_students(num_groups, max_students_per_group):
    groups = []
    students = []

    for _ in range(num_groups):
        group = Group(
            name=fake.company(),
            description=fake.text(),
        )
        groups.append(group)
        num_students = random.randint(1, max_students_per_group)
        for _ in range(num_students):
            student = Student(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=22),
                male=random.choice([True, False]),
                group=group,
            )
            students.append(student)

    return groups, students


if __name__ == "__main__":
    from app import db, app

    num_groups = 10
    max_students_per_group = 20

    groups, students = generate_random_groups_and_students(num_groups, max_students_per_group)
    with app.app_context():
        with db.session.begin():
            for group in groups:
                db.session.add(group)

            for student in students:
                db.session.add(student)

    print("Random groups and students generated and added to the database.")
