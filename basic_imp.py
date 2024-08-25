import csv
from codecarbon import EmissionsTracker

def process_temperature_data(file_path):
    temperature_data = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=';')
        for row in csv_reader:
            station, temp = row[0], float(row[1])
            if station in temperature_data:
                temperature_data[station].append(temp)
            else:
                temperature_data[station] = [temp]

    stats = {}
    for station, temperatures in temperature_data.items():
        min_temp = min(temperatures)
        max_temp = max(temperatures)
        mean_temp = sum(temperatures) / len(temperatures)
        stats[station] = {'min': min_temp, 'mean': mean_temp, 'max': max_temp}

    return stats

if __name__ == '__main__':
    tracker = EmissionsTracker()
    tracker.start()

    result = process_temperature_data('measurements.txt')
    for station, statistics in sorted(result.items()):
        print(f"{station}: {statistics}")

    emissions = tracker.stop()
    print(f"Carbon emissions: {emissions} kg CO2")
