import re, subprocess


def read_process_output(app):
    return subprocess.check_output(app).decode("utf8").strip().split("\n")


def read_all_lines(path):
    with open(path, "r") as f:
        lines = f.readlines()
        return lines


def parse_apcaccess(lines):
    parts = {
        "ups_usage_pct": None,
        "ups_usage_watt": None,
        "ups_time_left": None,
        "ups_utility_volts": None,
        "ups_battery_volts": None,
        "ups_battery_capacity": None,
        "ups_state": None,
    }
    for line in lines:
        m = re.search("([^.]+): (.+)", line.strip())
        if m:
            name = m.group(1).strip()
            value = m.group(2).strip()
            if name == "STATUS":
                parts["ups_state"] = "line" if value == "ONLINE" else "battery"
            if name == "LINEV":
                parts["ups_utility_volts"] = float(value[:-6])
            if name == "BATTV":
                parts["ups_battery_volts"] = float(value[:-6])
            if name == "BCHARGE":
                parts["ups_battery_capacity"] = float(value[:-8])
            if name == "TIMELEFT":
                parts["ups_time_left"] = float(value[:-8])
            if name == "LOADPCT":
                parts["ups_usage_pct"] = float(value[:-8])
    return parts


def parse_pwrstat(lines):
    parts = {
        "ups_usage_pct": None,
        "ups_usage_watt": None,
        "ups_time_left": None,
        "ups_utility_volts": None,
        "ups_battery_volts": None,
        "ups_battery_capacity": None,
        "ups_state": None,
    }
    for line in lines:
        m = re.search("([^.]+)\.+ (.+)", line.strip())
        if m:
            name = m.group(1)
            value = m.group(2)
            if name == "Power Supply by":
                parts["ups_state"] = "line" if value == "Utility Power" else "battery"
            if name == "Utility Voltage":
                parts["ups_utility_volts"] = float(value[:-2])
            if name == "Battery Capacity":
                parts["ups_battery_capacity"] = float(value[:-2])
            if name == "Remaining Runtime":
                parts["ups_time_left"] = float(value[:-5])
            if name == "Load":
                load = re.search("([0-9\.]+) Watt\(([0-9\.]+) %\)", value.strip())
                parts["ups_usage_watt"] = float(load.group(1))
                parts["ups_usage_pct"] = float(load.group(2))
    return parts
