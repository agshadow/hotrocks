from hotrocks.models import Job

job_title_list = [
    "ID:",
    "DATE:",
    "SHIFT (Day/Night):",
    "CREW:",
    "CREW MANAGER/PE",
    "ASPHALT CREW ON SITE:",
    "SPECIAL PPE REQUIREMENTS:",
    "SPECIAL INSTRUCTIONS:",
    "CLIENT:",
    "JOB NAME:",
    "JOB NUMBER:",
    "LOCATION:",
    "MAP:",
    "SUPPLY PLANT:",
    "ASPHALT:",
    "TRUCKS:",
    "GEAR:",
    "FLOAT:",
    "PROFILING:",
    "TRAFFIC CONTROL:",
    "COMPACTION TESTING:",
]


def get_job_mapping():
    job_mapping = {}
    for a, b in zip(Job.__fields__.keys(), job_title_list):
        job_mapping[b] = a
    return job_mapping


if __name__ == "__main__":
    print(get_job_mapping())
