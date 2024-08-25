import pandas as pd
from codecarbon import EmissionsTracker


def process_temperature_data(file_path):
    df = pd.read_csv(file_path, sep=';', header=None, names=['Station', 'Temperature'])
    stats = df.groupby('Station')['Temperature'].agg(['min', 'mean', 'max']).reset_index()
    stats = stats.sort_values(by='Station')
    return stats


if __name__ == '__main__':
    tracker = EmissionsTracker()
    tracker.start()

    result = process_temperature_data('measurements.txt')
    print(result)

    emissions = tracker.stop()
    print(f"Carbon emissions: {emissions} kg CO2")