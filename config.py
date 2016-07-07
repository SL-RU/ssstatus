uptime = "cat /proc/uptime"
temp_a = "cat /sys/class/thermal/thermal_zone0/temp"

last_idle = last_total = 0


def cpu_usage():
    global last_idle, last_total
    with open('/proc/stat') as f:
        fields = [float(column) for column in f.readline().strip().split()[1:]]
    idle, total = fields[3], sum(fields)
    idle_delta, total_delta = idle - last_idle, total - last_total
    last_idle, last_total = idle, total
    return 100.0 * (1.0 - idle_delta / total_delta)
