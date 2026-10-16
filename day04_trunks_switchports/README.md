# Day 04: Trunks & Switchports 🚀

**CCNA Domain:** Network Access

Welcome to Day 4 of my **30 Days of Network Automation (CCNA Level)** series!

Today, we're using Python to audit switch trunks and access ports, identify common configuration issues, and apply a trunk design from a YAML file.

## 🧠 Understanding the Concept

A **trunk port** carries traffic for multiple VLANs over a single link. With 802.1Q, VLAN tags identify which VLAN a frame belongs to.

Here are a few things worth checking when working with trunks and switchports:

- **Native VLAN:** On an 802.1Q trunk, native VLAN traffic is sent untagged by default. A native VLAN mismatch can trigger CDP warnings and cause traffic to be handled by the wrong VLAN.
- **Allowed VLANs:** The command `switchport trunk allowed vlan` replaces the existing allowed VLAN list. Use `switchport trunk allowed vlan add` when you want to add VLANs without replacing the list.
- **Access ports:** An access port normally carries traffic for one VLAN. Ports still assigned to VLAN 1, unused ports, and ports in an `err-disabled` state are worth investigating.
- **Trunk encapsulation:** On Catalyst 2960 switches and similar platforms that support only 802.1Q, `switchport trunk encapsulation dot1q` is not a valid command. The YAML design includes an `encapsulation` option for platforms that support or require this setting.

## 🛠️ Scripts Included

| Script | What it does |
|---|---|
| `01_trunk_audit.py` | Finds trunks using native VLAN 1 or allowing all VLANs, and reports native VLAN mismatches |
| `02_access_port_audit.py` | Identifies access ports in VLAN 1, unused ports, and err-disabled ports |
| `03_trunk_config_push.py` | Applies a trunk configuration defined in YAML, with dry-run enabled by default |

**Data file:** `trunks.yaml`

## ⚡ Run the Scripts

### 1. Set your credentials

Set these environment variables once in your terminal. Never hard-code credentials in your scripts.

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

### 2. Audit trunk ports

```bash
python day04_trunks_switchports/01_trunk_audit.py --native 99
```

This checks trunk ports and reports findings such as native VLAN 1, native VLAN mismatches, and trunks allowing all VLANs. The `--native 99` option sets VLAN 99 as the expected native VLAN for the audit.

### 3. Audit access ports

```bash
python day04_trunks_switchports/02_access_port_audit.py --problems-only
```

This filters the report to show ports that need attention, such as ports in VLAN 1, unused ports, or err-disabled ports.

### 4. Preview trunk configuration changes

```bash
python day04_trunks_switchports/03_trunk_config_push.py
```

The script runs in **dry-run mode** by default, so you can review the planned configuration before applying it.

After checking the output and confirming the design, use the script's `--apply` option to push the configuration:

```bash
python day04_trunks_switchports/03_trunk_config_push.py --apply
```

Use the appropriate device selection options if you want to limit the operation to a specific switch.

## 📊 Sample Output

You can reproduce the mock-device results by running:

```bash
python tests/run_offline_tests.py
```

No physical hardware is needed for the offline tests.

### 1. Trunk Audit — `01_trunk_audit.py`

```text
[ OK ] SW-CORE-01

HOSTNAME     INTERFACE  NATIVE_VLAN  ALLOWED_VLANS  FINDINGS
SW-CORE-01   Gi0/1      1            ALL            NATIVE-VLAN-1;NATIVE-MISMATCH;ALL-VLANS
SW-CORE-01   Gi0/2      99           10,20,30,99    OK

Saved 2 row(s) -> output/trunk_audit_<timestamp>.csv
```

**What does this tell us?**

- `Gi0/1` uses native VLAN 1, has a native VLAN mismatch, and allows all VLANs.
- `Gi0/2` uses native VLAN 99 and has a specific allowed VLAN list.

### 2. Access-Port Audit — `02_access_port_audit.py`

```text
[ OK ] SW-ACCESS-01

HOSTNAME       INTERFACE  NAME             STATUS       VLAN  FINDING
SW-ACCESS-01   Gi0/3      USER-PC-FLOOR2    connected    1     IN-VLAN-1
SW-ACCESS-01   Gi0/4                       notconnect    1     UNUSED
SW-ACCESS-01   Gi0/6                       err-disabled  10    ERR-DISABLED

Saved 3 row(s) -> output/access_port_audit_<timestamp>.csv
```

**What does this tell us?**

- `Gi0/3` is connected but assigned to VLAN 1, so verify whether that matches the network design.
- `Gi0/4` is not connected and may be unused. Confirm before disabling or repurposing it.
- `Gi0/6` is err-disabled and needs investigation to identify the cause before restoring the port.

Reports can be saved in CSV, JSON, or YAML format using `-f csv`, `-f json`, or `-f yaml`.

You can also choose a different inventory file with `-i inventory/devices.yaml` or target a specific switch with `-d HOSTNAME`.

## 📦 Requirements

- Python 3.9+
- Dependencies listed in [`requirements.txt`](requirements.txt)

## 🔒 Safety Notes

- Scripts 1 and 2 are read-only audit scripts.
- Script 3 uses dry-run mode by default. Use `--apply` only after reviewing the planned changes.
- Changing a trunk that carries your management traffic can disconnect your SSH session or lock you out of the switch.
- Always test configuration changes in CML, GNS3, EVE-NG, or another suitable lab before using them on production equipment.

---

**Learn. Build. Troubleshoot. Automate.**

Follow **NetworkWithDarshan** for more practical networking and Python automation content.

GitHub: https://github.com/darshannetworking45