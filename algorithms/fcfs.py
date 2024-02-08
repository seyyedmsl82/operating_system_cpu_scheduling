
"""

This algorithm sorts processes by the first arrival time.

"""

class FCFS(object):

    def __init__(self, process):
        self.processes = sorted(process, key=lambda process: process.arrival_time)
        self.timeline = 0.0
        self.cpu_idle_time = 0.0
        self.executed_processes = []
        self.timeline_queue = []



    def run(self):
        for process in self.processes:

            if process.arrival_time > self.timeline:
                self.cpu_idle_time += process.arrival_time - self.timeline
                self.timeline = process.arrival_time

            process.start_time = self.timeline

            process.waiting_time = self.timeline - process.arrival_time
            process.response_time = self.timeline - process.arrival_time
            process.turnaround_time = process.response_time + process.burst_time

            self.timeline += process.burst_time
            process.remaining_time -= process.burst_time
            process.end_time = self.timeline

            self.executed_processes.append(process)

            self.timeline_queue.append({'pid': process.pid, 'start_time': process.start_time, 'end_time': process.end_time})


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