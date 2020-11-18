def get_percentage(whole_number, part):
    try:
        return round(part / whole_number * 100, 2)
    except ZeroDivisionError:
        return 0
