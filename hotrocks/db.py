from datetime import datetime
from sqlmodel import SQLModel, create_engine

from .models import User, Mixes, JobAsphalt, JobOrder, Job

DB_FILE = "db.sqlite3"
engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)


def create_tables():
    SQLModel.metadata.create_all(engine)


def populate_user():
    from werkzeug.security import generate_password_hash
    from sqlmodel import Session

    with Session(engine) as sqlsession:
        userJulian = User(username="Julian", password=generate_password_hash("Julian"))
        userLibby = User(username="Libby", password=generate_password_hash("Libby"))
        sqlsession.add(userJulian)
        sqlsession.add(userLibby)
        sqlsession.commit()

        job1 = Job(
            client="Winslow",
            job_name="Thornhill Stage 1b",
            job_number="22-12-1234",
            crew_manager="Julian",
        )
        job2 = Job(
            client="TDL",
            job_name="Cecil St, Williamstown",
            job_number="22-12-1231",
            crew_manager="Julian",
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


if __name__ == "__main__":
    print("creating tables")
    create_tables()
    print("created tables")
