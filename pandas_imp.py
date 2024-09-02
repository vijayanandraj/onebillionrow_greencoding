import pandas as pd
from codecarbon import EmissionsTracker
import logging

from dbsetup import setup_database, get_connection
from performance_monitor import PerformanceMonitor

logging.basicConfig(level=logging.DEBUG)


def process_temperature_data(file_path):
    stats = None
    monitor = PerformanceMonitor()
    logging.info("Starting processing...")
    with monitor.track_performance():
        df = pd.read_csv(file_path, sep=';', header=None, names=['Station', 'Temperature'])
        stats = df.groupby('Station')['Temperature'].agg(['min', 'mean', 'max']).reset_index()

    stats = stats.sort_values(by='Station')
    metrics = monitor.get_metrics()
    processing_time = metrics['processing_time']
    avg_cpu_usage = metrics['cpu_usage']
    memory_used = metrics['memory_used']
    logging.info("Processing completed successfully.")

    return stats, processing_time, memory_used, avg_cpu_usage


if __name__ == '__main__':
    setup_database()
    tracker = EmissionsTracker()
    tracker.start()

    #result = process_temperature_data('measurements.txt')
    result, processing_time, memory_used, avg_cpu_usage = process_temperature_data('measurements.txt')
    #print(result)

    emissions = tracker.stop()
    logging.info(
        f"Processing time in seconds ==> {processing_time} - Memory Used in GB ==> {memory_used} - Average CPU Utilization ==> {avg_cpu_usage}")
    logging.info(f"Carbon emissions: {emissions} kg CO2")
    emissions_efficiency = emissions / 500  # Emission Efficieny Per Million Record
    logging.info(f"Emission Efficiency ==> {emissions_efficiency}")

    conn = get_connection()
    c = conn.cursor()
    c.execute('''
           INSERT INTO metrics (run_type, total_emissions, emissions_efficiency, processing_time, memory_usage, cpu_utilization,  yearly_projections)
           VALUES (?, ?, ?, ?, ?, ?, ?)
           ''', ("Pandas", emissions, emissions_efficiency, processing_time, memory_used, avg_cpu_usage, emissions * 365))

    logging.info("Metrics data inserted..")
    conn.commit()
    conn.close()




