from flask import Flask, render_template, request
import os
from main import Simulator


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def process_form():
    algorithm_type = request.form.get('flexRadioDefault')
    uploaded_file = request.files['file']

    # Check if the file has a CSV extension
    if uploaded_file.filename.endswith('.csv'):
        uploaded_file.save('data.csv')

        algo = Simulator(algorithm_type)
        algo.read_processes_data()
        algo.run()
        algo_details = algo.__str__()


        algorithm = algo_details["Algorithm"]
        total_processes = algo_details["Total processes"]
        simulation_time = algo_details["Simulation time"]
        cpu_total_time = algo_details["CPU total time"]
        cpu_utilization = algo_details["CPU utilization"]
        throughput = algo_details["Throughput"]
        average_waiting_time = algo_details["Average waiting time"]
        average_turnaround_time = algo_details["Average turnaround time"]
        average_response_time = algo_details["Average response time"]
        

        return render_template('result.html', algorithm = algorithm, total_processes = total_processes, simulation_time = simulation_time, 
                                              cpu_total_time = cpu_total_time, cpu_utilization = cpu_utilization, throughput = throughput, 
                                              average_waiting_time = average_waiting_time, average_turnaround_time = average_turnaround_time, 
                                              average_response_time = average_response_time)
    else:
        return "Error: Please upload a file with a '.csv' extension."

if __name__ == '__main__':
    app.run(debug=True)

