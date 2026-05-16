def generate_plan(hours):

    if hours >= 8:
        return [
            "2 hrs Coding",
            "3 hrs Core Subjects",
            "2 hrs DSA",
            "1 hr Revision"
        ]

    elif hours >= 5:
        return [
            "2 hrs Study",
            "2 hrs Coding",
            "1 hr Revision"
        ]

    else:
        return [
            "1 hr Important Subject",
            "1 hr Coding Practice",
            "1 hr Notes Revision"
        ]