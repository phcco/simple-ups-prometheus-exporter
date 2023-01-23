# Simple UPS Prometheus exporter

This is a very simple Prometheus exporter for home UPS (Uninterrupted Power Supply) devices.

## Requirements

1. UPS supported:
- Cyberpower (requires `pwrstat` tool installed)
- APC UPS (requires `apcaccess` tool installed)

2. Python3 (>=3.7), and `pip3` installed

> Debian/Ubuntu users: `apt install python3-pip python3-venv`

3. Root access (or you might not have permissions to read the vendor tool output)

## Installation

Make sure you have the vendor tool already installed and you can read the information. Try:

```bash
# Cyberpower
pwrstat -status

# or APC
apcaccess

# If any tool above fail, check your UPS driver installation
```
Now install the environment and run the exporter...

```bash
git clone https://github.com/phcco/simple-ups-prometheus-exporter.git
cd simple-ups-prometheus-exporter

###
# If you prefer using virtual environments (recommended)
# Init the requirements
bash setup-venv.sh
# Test the script
./venv/bin/python3 simple-ups-exporter.py --source apcaccess

### OR
# If you don't care about venv
pip3 install -r requirements.txt
python3 simple-ups-exporter.py --source apcaccess


# The script above should hang, use another terminal or browser to test it
# Try the 8300 port
curl http://localhost:8300/

# Check help for more options
./venv/bin/python3 s-ups-exporter.py --help
```

Now configure your Prometheus to scrape the port 8300 at your will

## Security

UPS tools require usually require root permissions to run. Use `--metrics-uid` to select a different user ID for the expose metric port.

## Installing as service

Copy `simple-ups-exporter.service` to `/etc/systemd/system/simple-ups-exporter.service`

Then fix `ExecStart` paths... then:

```bash
# Start it
systemctl start simple-ups-exporter

# ... check if everything is good
curl http://localhost:8300/

# Enable at boot
systemctl enable simple-ups-exporter
```

If you don't get anything at port 8300, check `journalctl -f`.