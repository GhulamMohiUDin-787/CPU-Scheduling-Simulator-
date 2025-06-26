# simulator.py

def get_process_data():
    processes = []
    n = int(input("Enter number of processes: "))
    for i in range(n):
        pid = f'P{i+1}'
        arrival = int(input(f"Enter arrival time for {pid}: "))
        burst = int(input(f"Enter burst time for {pid}: "))
        processes.append({'pid': pid, 'arrival': arrival, 'burst': burst, 'remaining': burst})
    return processes

def print_menu():
    print("\nCPU Scheduling Simulator")
    print("1. First Come First Serve (FCFS)")
    print("2. Shortest Job First (SJF)")
    print("3. Round Robin")
    print("4. Exit")

def fcfs(processes):
    processes.sort(key=lambda x: x['arrival'])  # Sort by arrival time
    time = 0
    total_waiting = 0
    total_turnaround = 0

    print("\nGantt Chart:")
    for p in processes:
        if time < p['arrival']:
            time = p['arrival']
        start = time
        time += p['burst']
        end = time
        waiting = start - p['arrival']
        turnaround = end - p['arrival']
        total_waiting += waiting
        total_turnaround += turnaround
        print(f"| {p['pid']} ({start}→{end}) ", end="")
    print("|")

    print(f"\nAverage Waiting Time: {total_waiting / len(processes):.2f}")
    print(f"Average Turnaround Time: {total_turnaround / len(processes):.2f}")

def sjf(processes):
    time = 0
    completed = 0
    total_waiting = 0
    total_turnaround = 0
    processes = sorted(processes, key=lambda x: (x['arrival'], x['burst']))
    ready_queue = []
    gantt = []

    while completed < len(processes):
        for p in processes:
            if p['arrival'] <= time and p not in ready_queue and 'done' not in p:
                ready_queue.append(p)
        if ready_queue:
            ready_queue.sort(key=lambda x: x['burst'])
            current = ready_queue.pop(0)
            start = time
            time += current['burst']
            end = time
            waiting = start - current['arrival']
            turnaround = end - current['arrival']
            total_waiting += waiting
            total_turnaround += turnaround
            current['done'] = True
            gantt.append(f"| {current['pid']} ({start}→{end}) ")
            completed += 1
        else:
            time += 1

    print("\nGantt Chart:")
    print("".join(gantt) + "|")
    print(f"\nAverage Waiting Time: {total_waiting / len(processes):.2f}")
    print(f"Average Turnaround Time: {total_turnaround / len(processes):.2f}")

def round_robin(processes, quantum):
    time = 0
    queue = []
    waiting_time = {}
    turnaround_time = {}
    arrival_sorted = sorted(processes, key=lambda x: x['arrival'])
    gantt = []
    i = 0

    while True:
        while i < len(arrival_sorted) and arrival_sorted[i]['arrival'] <= time:
            queue.append(arrival_sorted[i])
            i += 1

        if queue:
            current = queue.pop(0)
            start = time
            if current['remaining'] > quantum:
                time += quantum
                current['remaining'] -= quantum
                queue.append(current)
            else:
                time += current['remaining']
                current['remaining'] = 0
                turnaround_time[current['pid']] = time - current['arrival']
                waiting_time[current['pid']] = turnaround_time[current['pid']] - current['burst']
            gantt.append(f"| {current['pid']} ({start}→{time}) ")
        else:
            if i < len(arrival_sorted):
                time = arrival_sorted[i]['arrival']
            else:
                break

    print("\nGantt Chart:")
    print("".join(gantt) + "|")

    avg_wait = sum(waiting_time.values()) / len(processes)
    avg_turn = sum(turnaround_time.values()) / len(processes)

    print(f"\nAverage Waiting Time: {avg_wait:.2f}")
    print(f"Average Turnaround Time: {avg_turn:.2f}")

def main():
    while True:
        print_menu()
        choice = input("Choose a scheduling algorithm: ")
        if choice == '4':
            break
        processes = get_process_data()

        if choice == '1':
            fcfs(processes)
        elif choice == '2':
            sjf(processes)
        elif choice == '3':
            tq = int(input("Enter Time Quantum: "))
            round_robin(processes, tq)
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()
