
"""

#################################################################

"""

class RR(object):

    def __init__(self, processes, quantum_number = 4):

        self.quantum_number = quantum_number
        self.processes = sorted(processes, key=lambda process: process.arrival_time)
        self.timeline = 0.0
        self.cpu_idle_time = 0.0
        self.executed_processes = []
        self.timeline_queue = []



    def run(self):
        
        return {
            "timeline_queue": self.timeline_queue,
            "executed_processes": self.executed_processes,
            "total_process": len(self.executed_processes),
            "cpu_total_time": self.timeline,
            "cpu_idle_time": self.cpu_idle_time,
            "average_waiting_time": sum(process.waiting_time for process in self.executed_processes) / len(self.executed_processes),
            "average_turnaround_time": sum(process.turnaround_time for process in self.executed_processes) / len(self.executed_processes),
            "average_response_time": sum(process.response_time for process in self.executed_processes) / len(self.executed_processes)
        }



    def update_ready_queue(self, timeline):
        
        pass