def calc_attendance(attended, total):
    if total == 0:
        return 0
    return round((attended / total) * 100, 2)