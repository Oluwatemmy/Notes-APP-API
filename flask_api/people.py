from flask import abort, make_response
from config import db
from models import Person, person_schema, people_schema

def read_all():
    people = Person.query.all()
    # person_schema = PersonSchema(many=True)
    return people_schema.dump(people)

def create(person):
    new_person = person_schema.load(person, session=db.session)
    db.session.add(new_person)
    db.session.commit()
    return person_schema.dump(new_person), 201

def read_one(person_id):
    person = Person.query.get(person_id)

    if person is not None:
        return person_schema.dump(person)
    else:
        abort(404, f"Person with ID {person_id} not found")

def update(person_id, person):
    existing_peron = Person.query.get(person_id)
    if existing_peron:
        update_person = person_schema.load(person, session=db.session)
        existing_peron.fname = update_person.fname
        existing_peron.lname = update_person.lname
        db.session.merge(existing_peron)
        db.session.commit()
        return person_schema.dump(existing_peron), 201
    else:
        abort(
            404,
            f"Person with ID {person_id} not found"
        )

def delete(person_id):
    existing_peron = Person.query.get(person_id)
    if existing_peron:
        db.session.delete(existing_peron)
        db.session.commit()
        return make_response(f"{person_id} is successfully deleted.", 200)
    else:
        abort(
            404,
            f"Person with ID {person_id} not found"
        )
