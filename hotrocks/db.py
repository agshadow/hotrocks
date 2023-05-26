from datetime import datetime
from sqlmodel import SQLModel, create_engine, Session, col, select

from .models import (
    User,
    Mixes,
    JobAsphalt,
    JobOrder,
    Job,
    ShiftSummary,
    ShiftSummaryLog,
)

import os

DB_FILE = "db.sqlite3"
engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)


def initialise_db_and_create_tables():
    SQLModel.metadata.create_all(engine)


def populate_user():
    with Session(engine) as sqlsession:
        userAdmin = User(username="Admin", password=os.environ.get("adminPassword"))
        sqlsession.add(userAdmin)
        sqlsession.commit()

        job1 = Job(
            date="2023-05-23",
            shift="night",
            crew="Crew 1",
            crew_manager="Grant",
            asphalt_crew_on_site="7pm",
            special_ppe_requirements="Hard Hat",
            special_instructions="Tack Coat",
            client="Joes Construction",
            job_name="Thornhill Stage 9",
            job_number="22-02-1234",
            location="thornhill rd thornhill",
            map="96 A 12",
            supply_plant="Laverton",
            asphalt="14V 300T on site 9pm",
            trucks="tandem",
            gear="standard gear",
            float="thornhill rd thornhill",
            profiling="Bobcat mill 8pm",
            traffic_control="By Client",
            compaction_testing="None",
        )
        job2 = Job(
            date="2023-05-24",
            shift="day",
            crew="Crew 2",
            crew_manager="Kenny",
            asphalt_crew_on_site="7am",
            special_ppe_requirements="Hard Hat",
            special_instructions="Tack Coat",
            client="Joes Construction",
            job_name="Remington Stage 9",
            job_number="21-02-1236",
            location="Remington rd Remivale",
            map="96 A 12",
            supply_plant="Dandenong",
            asphalt="20SI 550T on site 8am",
            trucks="track and trailer",
            gear="standard gear",
            float="Remington rd Remivale",
            profiling="None",
            traffic_control="By Client",
            compaction_testing="Yes",
        )
        sqlsession.add(job1)
        sqlsession.add(job2)
        sqlsession.commit()
        sqlsession.refresh(job1)
        print("---------\n", job1)
        print("---------\n", job1.id)
        mixes1 = Mixes(mix_type="14N", tonnes="200", job_id=job1.id)
        mixes2 = Mixes(mix_type="20SI", tonnes="400", job_id=job1.id)
        mixes3 = Mixes(mix_type="20SF", tonnes="400", job_id=job1.id)
        mixes4 = Mixes(mix_type="10N", tonnes="350", job_id=job2.id)
        sqlsession.add(mixes1)
        sqlsession.add(mixes2)
        sqlsession.add(mixes3)
        sqlsession.add(mixes4)
        sqlsession.commit()

        # populate job orders
        job_order1 = JobOrder(
            date=datetime(2023, 5, 1),
            crew="Jeff Axiak",
            asphalt_crew_on_site="07:00",
            trucks="Tandem",
            job_id=job1.id,
        )
        job_order2 = JobOrder(
            date=datetime(2023, 5, 5),
            crew="All Ash",
            asphalt_crew_on_site="07:00",
            trucks="Flowcon",
            job_id=job2.id,
        )

        sqlsession.add(job_order1)
        sqlsession.add(job_order2)
        sqlsession.commit()

        job_asphalt1 = JobAsphalt(
            mix_type="14N",
            tonnes="50",
            sequence=3,
            joborder_id=job_order1.id,
        )
        job_asphalt2 = JobAsphalt(
            mix_type="20SI",
            tonnes="100",
            sequence=2,
            joborder_id=job_order1.id,
        )
        job_asphalt3 = JobAsphalt(
            mix_type="20SF",
            tonnes="110",
            sequence=1,
            joborder_id=job_order1.id,
        )
        job_asphalt4 = JobAsphalt(
            mix_type="10N",
            tonnes="300",
            sequence=1,
            joborder_id=job_order2.id,
        )
        sqlsession.add(job_asphalt1)
        sqlsession.add(job_asphalt2)
        sqlsession.add(job_asphalt3)
        sqlsession.add(job_asphalt4)
        sqlsession.commit()

        shiftsummary1 = ShiftSummary(
            date="2023-05-23",
            location="Pound Road",
            shift="Night",
            forecast="Fine 26 deg C",
            scope="Pound Road EB",
        )
        shiftsummarylog1 = ShiftSummaryLog(
            shiftsummaryid=1,
            date=datetime.strptime("24/05/23 19:00", "%d/%m/%y %H:%M"),
            data="Toolbox",
        )
        shiftsummarylog2 = ShiftSummaryLog(
            shiftsummaryid=1,
            date=datetime.strptime("24/05/23 19:15", "%d/%m/%y %H:%M"),
            data="Started Spraying, area was already clean.",
        )
        shiftsummarylog3 = ShiftSummaryLog(
            shiftsummaryid=1,
            date=datetime.strptime("24/05/23 20:15", "%d/%m/%y %H:%M"),
            data="Started Laying",
        )
        sqlsession.add(shiftsummary1)
        sqlsession.add(shiftsummarylog1)
        sqlsession.add(shiftsummarylog2)
        sqlsession.add(shiftsummarylog3)
        sqlsession.commit()


def save_job_record(job):
    with Session(engine) as sqlsession:
        # get job from database by id in form
        statement = select(Job).where(col(Job.id) == job.id)
        stored_job_from_db = sqlsession.exec(statement).first()

        # copy incoming data from form to a dictonary, excluding the ID
        update_data = job.dict(exclude_unset=True, exclude={"id"})

        # copy the updated data into the stored job from the db
        for key, val in update_data.items():
            print("setattr():", key, " : ", val)
            setattr(stored_job_from_db, key, val)

        sqlsession.add(stored_job_from_db)
        sqlsession.commit()
        sqlsession.refresh(stored_job_from_db)
    return stored_job_from_db


def save_log_record(shiftsummarylog):
    with Session(engine) as sqlsession:
        # get job from database by id in form
        statement = select(ShiftSummaryLog).where(
            col(ShiftSummaryLog.id) == shiftsummarylog.id
        )
        result = sqlsession.exec(statement).first()

        # copy incoming data from form to a dictonary, excluding the ID
        update_data = shiftsummarylog.dict(exclude_unset=True, exclude={"id"})

        # copy the updated data into the stored job from the db
        for key, val in update_data.items():
            print("setattr():", key, " : ", val)
            setattr(result, key, val)

        sqlsession.add(result)
        sqlsession.commit()
        sqlsession.refresh(result)
    return result


def add_log(shiftsummarylog):
    with Session(engine) as sqlsession:
        print("Saving new log : \n -------------------------", shiftsummarylog)
        sqlsession.add(shiftsummarylog)
        sqlsession.commit()
        sqlsession.refresh(shiftsummarylog)
        print("saved new log : \n ------------------------- ", shiftsummarylog)
    return shiftsummarylog


if __name__ == "__main__":
    print("creating tables")
    initialise_db_and_create_tables()
    print("created tables")
