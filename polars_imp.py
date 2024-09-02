import os, time, psutil
os.environ["POLARS_MAX_THREADS"] = "4"
import polars as pl
from codecarbon import EmissionsTracker
import logging
from dbsetup import setup_database, get_connection
from performance_monitor import PerformanceMonitor

logging.basicConfig(level=logging.DEBUG)
def process_temperature_data(file_path):
    # start_time = time.time()
    # initial_memory = psutil.virtual_memory().used
    # cpu_monitor = CPUUtilizationMonitor()
    # cpu_monitor.start()
    stats = None
    processing_time = None
    memory_used = None
    avg_cpu_usage = None
    try:
        monitor = PerformanceMonitor()
        logging.info("Starting processing...")
        with monitor.track_performance():
            df = pl.read_csv(file_path, separator=';', has_header=False, new_columns=['Station', 'Temperature'], truncate_ragged_lines=True)
            stats = df.group_by('Station').agg([
                pl.col('Temperature').min().alias('min'),
                pl.col('Temperature').mean().alias('mean'),
                pl.col('Temperature').max().alias('max')
            ])

        stats = stats.sort('Station')
        metrics = monitor.get_metrics()
        processing_time = metrics['processing_time']
        avg_cpu_usage = metrics['cpu_usage']
        memory_used = metrics['memory_used']
        logging.info("Processing completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

    # processing_time = time.time() - start_time
    # memory_used = psutil.virtual_memory().used - initial_memory
    # avg_cpu_usage = cpu_monitor.stop()

    return stats, processing_time, memory_used, avg_cpu_usage


if __name__ == '__main__':
    setup_database()
    tracker = EmissionsTracker()
    tracker.start()
    result, processing_time, memory_used, avg_cpu_usage = process_temperature_data('measurements.txt')
    #print(result)

    emissions = tracker.stop()
    #memory_used_gb = memory_used / (1024 ** 3)

    logging.info(f"Processing time in seconds ==> {processing_time} - Memory Used in GB ==> {memory_used} - Average CPU Utilization ==> {avg_cpu_usage}")
    logging.info(f"Carbon emissions: {emissions} kg CO2")
    emissions_efficiency = emissions / 500 # Emission Efficieny Per Million Record
    logging.info(f"Emission Efficiency ==> {emissions_efficiency}")

    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO metrics (run_type, total_emissions, emissions_efficiency, processing_time, memory_usage, cpu_utilization,  yearly_projections)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ("Polar", emissions, emissions_efficiency, processing_time, memory_used, avg_cpu_usage, emissions * 365))

    logging.info("Metrics data inserted..")
    conn.commit()
    conn.close()

