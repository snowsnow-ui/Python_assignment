import heapq


def schedule_jobs(workers, jobs):
    jobs.sort(key=lambda x: (x[0], x[5]))

    waiting = []
    worker_times = []

    for i in range(workers):
        heapq.heappush(worker_times, (0, i + 1))

    result = []
    time = 0
    index = 0
    total_wait = 0

    while index < len(jobs) or waiting:
        if not waiting and index < len(jobs):
            time = max(time, jobs[index][0])

        while index < len(jobs) and jobs[index][0] <= time:
            arrival, job_id, priority, duration, resources, order = jobs[index]
            heapq.heappush(waiting, (-priority, arrival, order, job_id, duration, resources))
            index += 1

        free_time, worker = heapq.heappop(worker_times)
        time = max(time, free_time)

        while index < len(jobs) and jobs[index][0] <= time:
            arrival, job_id, priority, duration, resources, order = jobs[index]
            heapq.heappush(waiting, (-priority, arrival, order, job_id, duration, resources))
            index += 1

        if not waiting:
            heapq.heappush(worker_times, (free_time, worker))
            continue

        priority, arrival, order, job_id, duration, resources = heapq.heappop(waiting)
        start = max(time, arrival, free_time)
        finish = start + duration
        wait = start - arrival
        total_wait += wait

        result.append((job_id, worker, start, finish))
        heapq.heappush(worker_times, (finish, worker))
        time = start

    result.sort(key=lambda x: x[0])
    return result, total_wait / len(jobs)


def main():
    try:
        workers, n = map(int, input().split())
        jobs = []

        for order in range(n):
            arrival, job_id, priority, duration, resources = input().split()
            jobs.append((int(arrival), job_id, int(priority), int(duration), int(resources), order))

        result, average_wait = schedule_jobs(workers, jobs)

        for job_id, worker, start, finish in result:
            print(job_id, "W" + str(worker), start, finish)

        print(f"AVG_WAIT {average_wait:.2f}")

    except (ValueError, EOFError):
        print("INVALID INPUT")


if __name__ == "__main__":
    main()
