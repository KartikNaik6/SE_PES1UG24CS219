def parse_reading(text):
    if not isinstance(text, str) or '/' not in text:
        return None
    parts = text.split('/')
    if len(parts) != 2:
        return None
    try:
        return float(parts[0]), int(parts[1])
    except (ValueError, TypeError):
        return None


def wind_category(speed_text):
    if not isinstance(speed_text, str):
        return None
    try:
        speed = int(speed_text)
    except (ValueError, TypeError):
        return None
    if speed >= 89:
        return 'warning'
    if speed >= 39:
        return 'advisory'
    return 'none'


def rainfall_spread(readings_csv):
    if not isinstance(readings_csv, str) or not readings_csv.strip():
        return None
    try:
        readings = [float(r) for r in readings_csv.split(',')]
    except (ValueError, TypeError):
        return None
    return max(readings) - min(readings)


def main():
    print("==== Running parse_reading ====")
    user_input = input("Enter temperature/humidity (e.g. 35.5/80): ")
    result = parse_reading(user_input)
    print("Temperature and Humidity:", result)

    print("\n==== Running wind_category ====")
    user_input = input("Enter a wind speed in km/h (e.g. 45): ")
    result = wind_category(user_input)
    print("Wind Category:", result)

    print("\n==== Running rainfall_spread ====")
    user_input = input("Enter hourly rainfall in mm as CSV (e.g. 2,5.5,10): ")
    result = rainfall_spread(user_input)
    print("Rainfall Spread:", result)


if __name__ == "__main__":
    main()
