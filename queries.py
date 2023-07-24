from datetime import date

from sqlalchemy import func, Integer

from models import Group, Student


def get_all_groups():
    return Group.query.all()


def get_all_groups_with_students():
    return db.session.query(Group).join(Student).all()
    #return Group.query.options(db.joinedload(Group.students)).all()


def get_group_by_id():
    return Group.query.filter_by(id=1).first()


def get_groups_by_name():
    return Group.query.filter_by(name="Hall Group").all()


def get_groups_by_name_substring():
    return Group.query.filter(
        Group.name.ilike(f"%ams%")
    ).all()


def get_groups_name_startswith():
    return Group.query.filter(
        Group.name.startswith(f"Scott")
    ).all()

    # db.session.query(Group).filter(Group.name.startswith(substring)).all()


def get_groups_with_students_ending_with_a():
    return Group.query.filter(
        Group.students.any(Student.first_name.like("%a"))
    ).all()


def get_students_ending_with_a():
    return Student.query.join(Group).filter(Student.first_name.like("%a")).all()


def get_female_students():
    return Student.query.filter_by(male=False).all()


def get_female_student_named_meghan():
    return Student.query.filter_by(male=False, first_name="Meghan").first()


def get_students_by_names():
    return Student.query.filter(Student.first_name.in_(["Meghan", "Ann"])).all()


def get_students_by_names_older_than_18():
    today = date.today()
    eighteen_years_ago = today.replace(year=today.year - 18)
    return Student.query.filter(
        Student.first_name.in_(["Meghan", "Ann"]),
        Student.birth_date <= eighteen_years_ago
    ).all()


def get_students_by_names_younger_than_18_or_older_than_65():
    today = date.today()
    eighteen_years_ago = today.replace(year=today.year - 18)
    sixty_five_years_ago = today.replace(year=today.year - 65)
    return Student.query.filter(
        Student.first_name.in_(["Meghan", "Ann"]),
        db.or_(Student.birth_date >= eighteen_years_ago, Student.birth_date <= sixty_five_years_ago)
    ).all()


def get_student_multi_filter():
    today = date.today()
    return db.session.query(Student).filter(
        ((Student.first_name == 'Roma') & (today.year - Student.birth_date.year < 18)) |
        ((Student.first_name == 'Pavel') & (today.year - Student.birth_date.year > 67) & Student.male)
    ).all()


def get_groups_with_count_of_students():
    return db.session.query(Group, func.count(Student.id)).outerjoin(Student.group).group_by(Group).all()


def get_groups_with_count_of_students_and_male_students():
    return db.session.query(
        Group,
        func.count(Student.id).label('total_students'),
        func.sum(func.cast(Student.male, Integer)).label('male_students')
    ).outerjoin(Student.group).group_by(Group).all()


def get_some_fields():
    return db.session.query(Group.id, Group.name).all()


def select_groups_with_gte_5_students():
    return db.session.query(Group).outerjoin(Group.students).group_by(Group).having(func.count(Student.id) > 5).all()


def func():
    ideas_to_delete = Idea.query.filter(Idea.participants.contains("John Doe")).all()
    for idea in ideas_to_delete:
        db.session.delete(idea)
    db.session.commit()

    update_query = update(Idea).where(Idea.type == 'креативная').values(type='инновационная')

    # Выполняем SQL-запрос
    db.session.execute(update_query)
    db.session.commit()


if __name__ == "__main__":
    from app import db, app

    with app.app_context():
        result = get_groups_with_count_of_students_and_male_students()
        print(result)

