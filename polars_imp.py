import polars as pl
from codecarbon import EmissionsTracker


def process_temperature_data(file_path):
    df = pl.read_csv(file_path, separator=';', has_header=False, new_columns=['Station', 'Temperature'], truncate_ragged_lines=True)

    stats = df.group_by('Station').agg([
        pl.col('Temperature').min().alias('min'),
        pl.col('Temperature').mean().alias('mean'),
        pl.col('Temperature').max().alias('max')
    ])

    stats = stats.sort('Station')
    return stats


if __name__ == '__main__':
    tracker = EmissionsTracker()
    tracker.start()

    result = process_temperature_data('measurements.txt')
    print(result)

    emissions = tracker.stop()
    print(f"Carbon emissions: {emissions} kg CO2")