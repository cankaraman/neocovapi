# from services import db_service
from faker import Faker

fake = Faker()


def generate_fake_patients(num: int) -> list():
    patients = list()
    for _ in range(num):
        patients.append(__generate_fake_patient())

    return patients


def __generate_fake_patient():
    first_name = fake.first_name()
    last_name = fake.last_name()
    updated = fake.date_time_this_year(before_now=True, after_now=False)
    return {'firstName': first_name, 'lastName': last_name,
            'updated': updated, 'entryDate': updated}


if __name__ == '__main__':
    patients = generate_fake_patients(3)
    print(patients)
