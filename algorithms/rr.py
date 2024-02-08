
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

        self.running_process = None
        self.ready_queue = []
        self.quantum_number = quantum_number   



    def run(self):

        while self.processes or self.ready_queue or self.running_process:

            if self.running_process and self.running_process.remaining_time == 0:
                self.running_process.end_time = self.timeline
                self.running_process.turnaround_time = self.running_process.end_time - self.running_process.arrival_time
                self.running_process.waiting_time = self.running_process.turnaround_time - self.running_process.burst_time
                self.running_process.response_time = self.running_process.start_time - self.running_process.arrival_time
                self.executed_processes.append(self.running_process)
                self.timeline_queue.append({'pid': self.running_process.pid, 'start_time': self.running_process.start_time, 'end_time': self.running_process.end_time})
                self.running_process = None

                # All processes have done
                if not (self.running_process or self.processes or self.ready_queue):
                    break

            # update ready queue with new arrival time processes in this timeline
            self.update_ready_queue(self.timeline)

            if self.running_process is None and self.ready_queue:
                self.running_process = self.ready_queue.pop(0)
                if self.running_process.start_time is None:
                    self.running_process.start_time = self.timeline
                else:
                    self.running_process.start_time = self.running_process.start_time

            if self.running_process:
                # after finishing this part, in next loop, the process waiting_time and other attr is calculated.
                # then next process in ready queue will replace running_process
                if self.running_process.remaining_time <= self.quantum_number:
                    added_time = self.running_process.remaining_time
                    self.running_process.remaining_time -= added_time

                    # update ready queue with new processes before this process be end
                    for future_time in range(1, added_time + 1):
                        timeline = self.timeline + future_time
                        self.update_ready_queue(timeline)

                else:
                    added_time = self.quantum_number
                    self.running_process.remaining_time -= added_time

                    # update ready queue before add this process to end of ready queue
                    for future_time in range(1, added_time + 1):
                        timeline = self.timeline + future_time
                        self.update_ready_queue(timeline)

                    self.ready_queue.append(self.running_process)
                    self.running_process = None

            else:
                added_time = 1
                self.cpu_idle_time += added_time
            self.timeline += added_time

        for i in range(1, len(self.timeline_queue)):
            self.timeline_queue[i]['start_time'] = max(self.timeline_queue[i]['start_time'], self.timeline_queue[i-1]['end_time']) 
            
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
        
        arrived_processes = []
        # processes that their arrival time are equal to this timeline goes to ready queue
        for process in self.processes:
            if process.arrival_time == timeline:
                self.ready_queue.append(process)
                arrived_processes.append(process)
            # for finishing sooner
            elif process.arrival_time > self.timeline:
                break

        # for deleting new arrived processes from self.processes list
        for process in arrived_processes:
            if process in self.processes:
                self.processes.remove(process)
        arrived_processes.clear()        

