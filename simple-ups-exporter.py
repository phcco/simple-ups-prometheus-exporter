import prometheus_client
import time, os, argparse, multiprocessing
import ups_parsers

prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)

ups_usage_pct = prometheus_client.Gauge("ups_pct_load", "UPS percentage load")
ups_usage_watt = prometheus_client.Gauge("ups_watt_load", "UPS watt load")
ups_time_left = prometheus_client.Gauge(
    "ups_time_left", "UPS time left on battery (minutes)"
)
ups_utility_volts = prometheus_client.Gauge(
    "ups_utility_volts", "UPS utility current volts"
)
ups_battery_volts = prometheus_client.Gauge(
    "ups_battery_volts", "UPS battery current volts"
)
ups_battery_capacity = prometheus_client.Gauge(
    "ups_battery_capacity", "UPS battery capacity"
)

ups_state = prometheus_client.Enum(
    "ups_state", "UPS source state", states=["line", "battery"]
)


parser = argparse.ArgumentParser(description="Simple Prometheus exporter for UPS")
parser.add_argument(
    "--metrics-port", dest="port", default="8300", help="Metrics port (default: 8300)"
)
parser.add_argument(
    "--metrics-host",
    dest="host",
    default="0.0.0.0",
    help="Metrics host (default: 0.0.0.0)",
)
parser.add_argument(
    "--metrics-uid",
    dest="uid",
    default=None,
    help="User ID for metrics server (default: same as proc)",
)
parser.add_argument(
    "--read-every",
    dest="freq",
    default=10,
    help="Read from source tool every FREQ seconds (default: 10)",
)
parser.add_argument(
    "--source",
    dest="source",
    default=None,
    help="Source tool for metrics",
    choices=["apcaccess", "pwrstat"],
)

args = parser.parse_args()


def metrics(q):
    if args.uid:
        os.setuid(int(args.uid))

    prometheus_client.start_http_server(int(args.port), args.host)
    print("UPS metrics exporter listening on {}:{} using {}".format(args.host, args.port, args.source))
    while True:
        res = q.get()
        if "ups_usage_pct" in res and res["ups_usage_pct"] != None:
            ups_usage_pct.set(res["ups_usage_pct"])
        if "ups_usage_watt" in res and res["ups_usage_watt"] != None:
            ups_usage_watt.set(res["ups_usage_watt"])
        if "ups_time_left" in res and res["ups_time_left"] != None:
            ups_time_left.set(res["ups_time_left"])
        if "ups_utility_volts" in res and res["ups_utility_volts"] != None:
            ups_utility_volts.set(res["ups_utility_volts"])
        if "ups_battery_volts" in res and res["ups_battery_volts"] != None:
            ups_battery_volts.set(res["ups_battery_volts"])
        if "ups_battery_capacity" in res and res["ups_battery_capacity"] != None:
            ups_battery_capacity.set(res["ups_battery_capacity"])
        if "ups_state" in res and res["ups_state"] != None:
            ups_state.state(res["ups_state"])


def collect(q):
    while True:
        if args.source == "apcaccess":
            proc_resp = ups_parsers.read_process_output(["apcaccess"])
            metrics_dict = ups_parsers.parse_apcaccess(proc_resp)
            q.put(metrics_dict)

        if args.source == "pwrstat":
            proc_resp = ups_parsers.read_process_output(["pwrstat", "-status"])
            metrics_dict = ups_parsers.parse_pwrstat(proc_resp)
            q.put(metrics_dict)

        time.sleep(int(args.freq))


def main():

    ipc_q = multiprocessing.Queue()

    if args.source == None:
        print("Error: Missing --source")
        exit(1)

    p_metrics = multiprocessing.Process(target=metrics, args=(ipc_q,))
    p_collect = multiprocessing.Process(target=collect, args=(ipc_q,))

    p_metrics.start()
    p_collect.start()


if __name__ == "__main__":
    main()
