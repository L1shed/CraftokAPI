def convert_to_minutes(duration):
    hours = 0
    minutes = 0

    if 'h' in duration:
        heures_part = duration.split('h')[0].strip()
        hours = int(heures_part)

    if 'min' in duration:
        minutes_part = duration.split('min')[0].split()[-1]
        minutes = int(minutes_part)

    total_minutes = hours * 60 + minutes
    return total_minutes


# Examples
if __name__ == '__main__':
    print(convert_to_minutes("10h et 53min"))  # 653
    print(convert_to_minutes("34min"))  # 34
