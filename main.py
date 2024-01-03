import time
import algorithms
import pandas as pd


class Process:
    def __init__(self, pid, arrival_time, priority, burst_time):
        
        self.pid = pid
        self.arrival_time = arrival_time
        self.priority = priority
        self.burst_time = burst_time
        self.response_time = None
        self.waiting_time = None
        self.turnaround_time = None
        self.start_time = None
        self.end_time = None
        self.remaining_time = burst_time

    def __str__(self):
        return f"pid: {self.pid} | arrival_time: {self.arrival_time} | priority: {self.priority} |" \
               f" 'burst_time': {self.burst_time} | 'waiting_time: {self.waiting_time}' |" \
               f" 'turnaround_time': {self.turnaround_time} | 'response_time': {self.response_time} |" \
               f" 'start_time': {self.start_time} | 'end_time': {self.end_time} |" \
               f" 'remaining_time': {self.remaining_time}"



class Simulator:

    def __init__(self, algorithm):

        self.algorithm = algorithm
        self.algorithm_class = self.get_algorithm_class()
        self.algorithms_list = ["FCFS", "PreemptiveSFJ", "NonPreemptiveSFJ", "RR", 
                                "PreemptivePriority", "NonPreemptivePriority"]
        self.processes = []
        self.total_process = 0
        self.run_time = 0
        self.cpu_total_time = 0
        self.cpu_utilization = 0
        self.throughput = 0
        self.average_waiting_time = 0.0
        self.average_turnaround_time = 0.0
        self.average_response_time = 0.0



    def set_algorithm(self, algorithm):

        self.algorithm = algorithm
        self.algorithm_class = self.get_algorithm_class()
        return True



    def get_algorithm_class(self):

        try:
            return getattr(algorithms, self.algorithm)

        except Exception as e:
            print(e)
            raise Exception("try again! you have to enter a valid algorithm")



    def read_processes_data(self, path='data.csv', dataframe=None):
        
        # clear last loaded processes
        self.processes.clear()

        # read new processes data
        if isinstance(dataframe, pd.DataFrame):
            df = dataframe
        elif path and path.split('.')[-1] == 'csv':
            df = pd.read_csv(path)
        else:
            raise Exception("Your file should be a csv format or pass dataframe object to function")


        for i in range(0, df['pid'].count()):
            process = Process(
                pid=df['pid'][i],
                arrival_time=df['arrival_time'][i],
                priority=df['priority'][i],
                burst_time=df['burst_time'][i]
            )
            self.processes.append(process)

        return True



    def run(self):
        """
        Simulate algorithm and save the result of it
        """

        if len(self.processes) == 0:
            raise Exception("you have to load processes")

        algorithm = self.algorithm_class(self.processes)

        # run time of algorithm
        start_time = time.time()
        result = algorithm.run()
        end_time = time.time()
        self.run_time = end_time - start_time

        total_process = result['total_process']
        cpu_total_time = result['cpu_total_time']
        cpu_idle_time = result['cpu_idle_time']

        throughput = total_process / cpu_total_time
        cpu_utilization = (cpu_total_time - cpu_idle_time) / cpu_total_time

        average_waiting_time = result['average_waiting_time']
        average_turnaround_time = result['average_turnaround_time']
        average_response_time = result['average_response_time']

        # for process in result['executed_processes']:
        #     print(process)

        for process in result['timeline_queue']:
            print(process)

        self.total_process = total_process
        self.cpu_total_time = cpu_total_time
        self.throughput = throughput
        self.cpu_utilization = cpu_utilization
        self.average_waiting_time = average_waiting_time
        self.average_turnaround_time = average_turnaround_time
        self.average_response_time = average_response_time
        # update processes
        self.processes = result['executed_processes']



    def __str__(self):
        return (
                {"Algorithm": self.algorithm,
                "Total processes": self.total_process,
                "Simulation time": f"{self.run_time} s",
                "CPU total time": self.cpu_total_time,
                "CPU utilization": f"{(self.cpu_utilization * 100)}%",
                "Throughput": self.throughput,
                "Average waiting time": self.average_waiting_time,
                "Average turnaround time": self.average_turnaround_time,
                "Average response time": self.average_response_time}
        )


if __name__ == '__main__':
    # algo = Simulator("FCFS")
    # algo.read_processes_data()
    # algo.run()
    # print(algo.__str__())

    # algo = Simulator("PreemptiveSFJ")
    # algo.read_processes_data()
    # algo.run()
    # print(algo.__str__())


    algo = Simulator("NonPreemptiveSFJ")
    algo.read_processes_data()
    algo.run()