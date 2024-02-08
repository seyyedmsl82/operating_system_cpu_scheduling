
"""

#################################################################

"""

class NonPreemptivePriority(object):

    def __init__(self, processes):

        self.processes = sorted(processes, key=lambda process: process.arrival_time)
        self.timeline = 0.0
        self.cpu_idle_time = 0.0
        self.executed_processes = []
        self.timeline_queue = []

        self.running_process = None
        self.ready_queue = []
        
    


    def get_next_important_time(self):
        
        """
        Find next important things which happen in the timeline
        """
        future_processes = self.processes

        if future_processes:
            if not self.running_process:
                try:
                    return min(future_processes[0].arrival_time, self.ready_queue[0].arrival_time)
                except IndexError:
                    return self.timeline + 1
                    
            else:
                return min(self.running_process.remaining_time + self.timeline, future_processes[0].arrival_time)
        
        return self.running_process.remaining_time + self.timeline



    def run(self):

        while self.processes or self.ready_queue or self.running_process:

            # a running process have done its work
            if self.running_process and self.running_process.remaining_time == 0:
                self.running_process.end_time = self.timeline
                self.running_process.turnaround_time = self.running_process.end_time - self.running_process.arrival_time
                self.running_process.waiting_time = self.running_process.start_time - self.running_process.arrival_time
                self.running_process.response_time = self.running_process.start_time - self.running_process.arrival_time
                self.executed_processes.append(self.running_process)
                self.running_process = None

                # All processes have done
                if not (self.running_process or self.processes or self.ready_queue):
                    break

            arrived_processes = []
            # processes that their arrival time are equal to this timeline goes to ready queue
            for process in self.processes:
                if process.arrival_time == self.timeline:
                    self.ready_queue.append(process)
                    arrived_processes.append(process)
                # for finishing sooner
                elif process.arrival_time > self.timeline:
                    break
            # for deleting new arrived processes from self.processes list
            for process in arrived_processes:
                if process in self.processes:
                    self.processes.remove(process)

            # sort ready queue when we have new processes that are not in the list. otherwise, we have an sorted list
            if arrived_processes:
                self.ready_queue.sort(key=lambda p: p.priority)

            if self.running_process is None and self.ready_queue:
                # after sorting ready_queue by burst time, get first index and start to run that process
                self.running_process = self.ready_queue.pop(0)
                self.running_process.start_time = self.timeline

            # run process until some important things happen
            next_important_time = self.get_next_important_time()
            if self.running_process:
                self.running_process.remaining_time -= (next_important_time - self.timeline)

            else:
                self.cpu_idle_time += (next_important_time - self.timeline)
            self.timeline = next_important_time
        
        for process in self.executed_processes:
            print(process)

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

