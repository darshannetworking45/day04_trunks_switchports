# 🚀 30 Days of Network Automation (CCNA Level)

Welcome to my **30 Days of Network Automation** series!

In this series, I'm exploring how Python can automate everyday networking tasks based on real CCNA concepts. Instead of learning Python only through theory, the goal is to use it to solve practical networking problems.

Each day includes **3 small Python scripts**, with examples, explanations, and lab-focused use cases.

### 🛠️ Technologies Used

- Python
- Netmiko
- TextFSM / ntc-templates
- argparse
- ipaddress
- CSV, JSON, and YAML

**Progress: Day 4 of 30**

A new day brings a new networking concept, with its own folder containing the scripts, README, requirements, and any required data files.

## ⚡ Quick Start

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your credentials

Linux/macOS:

```bash
export NET_USERNAME=admin
export NET_PASSWORD='your-password'
export NET_SECRET='enable-secret'  # Optional
```

Windows PowerShell:

```powershell
$env:NET_USERNAME = "admin"
$env:NET_PASSWORD = "your-password"
$env:NET_SECRET = "enable-secret"  # Optional
```

### 4. Run a script

```bash
python day01_device_reachability/03_show_version_inventory.py
```

If the username and password environment variables aren't set, the scripts prompt you for the required credentials.

**Security note:** Credentials are not stored in the Python code or inventory files.

## 📁 Repository Structure

```text
common/
    netutils.py             # Shared networking utilities

inventory/
    devices.csv             # Device inventory in CSV
    devices.yaml            # Device inventory in YAML
    devices.json            # Device inventory in JSON

dayNN_<topic>/
    01_*.py                 # Script 1
    02_*.py                 # Script 2
    03_*.py                 # Script 3
    README.md
    requirements.txt        # If required by the day

tests/
    # Offline tests using mock devices

output/
    # Generated reports (ignored by Git)
```

The inventory files contain the same four lab devices in different formats. The shared `common/netutils.py` module handles tasks such as loading inventory, managing credentials, connecting through SSH, parsing command output, and exporting results.

Each day's folder may also contain small data files needed by its scripts.

## 🧰 Common Command-Line Options

Most device scripts support these options:

| Option | Description |
|---|---|
| `-i, --inventory` | Inventory file: CSV, JSON, or YAML. Default: `inventory/devices.csv` |
| `-d, --device` | Run against a specific hostname; repeatable |
| `-f, --format` | Choose the output format: `csv`, `json`, or `yaml` |

You can edit `inventory/devices.csv` to match your own lab.

The `device_type` field should use a supported Netmiko device type, such as `cisco_ios` or `cisco_wlc_ssh`, depending on your device and connection method.

Check each day's README for any additional options or requirements.

## 🔒 Safety Rules

Safety is part of the automation workflow, not an afterthought.

- **Read-only by default:** Audit and reporting scripts use show commands and do not intentionally change device configuration.
- **Dry-run by default:** Scripts that make configuration changes show the planned actions first. Use `--apply` when you're ready to execute supported changes.
- **Handle failures safely:** If one device fails, the script reports the issue and continues with the remaining devices where possible.
- **Test before production:** Start with CML, GNS3, EVE-NG, or a Cisco DevNet sandbox before working on real equipment.

**Important:** Python scripts using SSH cannot connect directly to Packet Tracer's simulated Cisco devices in the same way they connect to real IOS devices or supported virtual appliances.

## 🧪 Run Tests Without Physical Hardware

You can test much of the project without connecting to a real switch or router.

```bash
python tests/run_offline_tests.py
```

The offline test suite replaces Netmiko's connection function with a mock device that returns realistic Cisco IOS output. The tests then use the actual parsing templates where configured and exercise the scripts' logic.

The suite also checks failure scenarios, such as an unreachable device, and verifies that dry-run mode does not push configuration changes.

These tests help validate the scripts and parsing logic, but they **do not replace testing against the IOS versions and platforms used in your own lab**.

## 📚 Day-by-Day Progress

| Day | Topic | Folder |
|---|---|---|
| 01 | Device Reachability & Inventory | [day01_device_reachability](day01_device_reachability) |
| 02 | Interface Status & Troubleshooting | [day02_interface_status](day02_interface_status) |
| 03 | VLANs | [day03_vlans](day03_vlans) |
| 04 | Trunks & Switchports | [day04_trunks_switchports](day04_trunks_switchports) |

More topics will be added as the series progresses.

## 📦 Requirements

- Python 3.9 or later
- Dependencies listed in [`requirements.txt`](requirements.txt)
- Access to a supported network device or virtual lab for live testing

For the complete dependency list, see the repository's `requirements.txt` file.

---

**Learn. Build. Troubleshoot. Automate.**

Follow the journey: **NetworkWithDarshan**

GitHub: https://github.com/darshannetworking45/day04_trunks_switchports