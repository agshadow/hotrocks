from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    # first_name: str
    # last_name: str
    # email: str = Field(sa_column=Column("email", String, unique=True))


"""
class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client: str = Field(index=True)
    job_name: str = Field(index=True)
    job_number: Optional[str] = Field(index=True)
    location: Optional[str]
    map: Optional[str]
    crew_manager: str
    profiling: Optional[str]
"""


class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: Optional[date]
    shift: Optional[str]
    crew: Optional[str]
    crew_manager: str
    asphalt_crew_on_site: Optional[str]
    special_ppe_requirements: Optional[str]
    special_instructions: Optional[str]
    client: str = Field(index=True)
    job_name: str = Field(index=True)
    job_number: Optional[str] = Field(index=True)
    location: Optional[str]
    map: Optional[str]
    supply_plant: Optional[str]
    asphalt: Optional[str]
    job_id: Optional[str]
    trucks: Optional[str]
    gear: Optional[str]
    float: Optional[str]
    profiling: Optional[str]
    traffic_control: Optional[str]
    compaction_testing: Optional[str]


class Mixes(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    mix_type: Optional[str]
    tonnes: Optional[str]
    job_id: Optional[int] = Field(default=None, foreign_key="job.id")


class JobOrder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: Optional[date]
    shift_day_night: Optional[str]
    crew: Optional[str]
    asphalt_crew_on_site: Optional[str]
    special_ppe_requirements: Optional[str]
    special_instructions: Optional[str]
    supply_plant: Optional[str]
    job_id: Optional[int] = Field(default=None, foreign_key="job.id")
    trucks: Optional[str]
    gear: Optional[str]
    float: Optional[str]
    job_order_profiling: Optional[str]
    traffic_control: Optional[str]
    compaction_testing: Optional[str]


class JobAsphalt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    mix_type: Optional[str]
    tonnes: Optional[str]
    sequence: int = Field(default=1)
    joborder_id: Optional[int] = Field(default=None, foreign_key="joborder.id")
