import psutil
import time
import csv

# Substitua pelos PIDs reais das suas APIs
target_pids = [27420]

# Opcional: dar um nome para cada PID
pid_names = {
    27420: "API GraphQL"
}

with open("monitoramento.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "pid", "name", "cpu_percent", "memory_mb"])

    try:
        while True:
            for pid in target_pids:
                try:
                    proc = psutil.Process(pid)
                    cpu = proc.cpu_percent(interval=0.1)
                    mem = proc.memory_info().rss / (1024 * 1024)
                    name = pid_names.get(pid, f"PID {pid}")
                    writer.writerow([time.time(), pid, name, cpu, mem])
                except psutil.NoSuchProcess:
                    pass
            time.sleep(1)
    except KeyboardInterrupt:
        print("Monitoramento encerrado.")