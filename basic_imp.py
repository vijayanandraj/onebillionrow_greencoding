import csv
from codecarbon import EmissionsTracker
import logging

from dbsetup import setup_database, get_connection
from performance_monitor import PerformanceMonitor

logging.basicConfig(level=logging.DEBUG)

def process_temperature_data(file_path):
    temperature_data = {}
    monitor = PerformanceMonitor()
    logging.info("Starting processing...")

    with monitor.track_performance():
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
    metrics = monitor.get_metrics()
    processing_time = metrics['processing_time']
    avg_cpu_usage = metrics['cpu_usage']
    memory_used = metrics['memory_used']
    return stats, processing_time, memory_used, avg_cpu_usage

if __name__ == '__main__':
    setup_database()
    tracker = EmissionsTracker()
    tracker.start()

    result, processing_time, memory_used, avg_cpu_usage = process_temperature_data('measurements.txt')

    for station, statistics in sorted(result.items()):
        print(f"{station}: {statistics}")

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
           ''', ("Custom", emissions, emissions_efficiency, processing_time, memory_used, avg_cpu_usage, emissions * 365))

    logging.info("Metrics data inserted..")
    conn.commit()
    conn.close()

    #print(f"Carbon emissions: {emissions} kg CO2")
