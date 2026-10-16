
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.netutils import (add_common_args, get_credentials, load_inventory,  
                             print_table, run_task, save_output, send_parsed)


def make_collector(expected_native):
    def collect(conn, dev):
        rows = []
        for port in send_parsed(conn, "show interfaces switchport"):
            if port["mode"].lower() != "trunk":
                continue
            allowed = port["trunking_vlans"]
            findings = []
            if port["native_vlan"] == "1":
                findings.append("NATIVE-VLAN-1")
            if expected_native and port["native_vlan"] != str(expected_native):
                findings.append("NATIVE-MISMATCH")
            if "ALL" in allowed:
                findings.append("ALL-VLANS")
            rows.append({
                "hostname": dev["hostname"],
                "interface": port["interface"],
                "admin_mode": port["admin_mode"],
                "native_vlan": port["native_vlan"],
                "allowed_vlans": ",".join(allowed),
                "findings": ";".join(findings) or "OK",
            })
        return rows
    return collect


def main():
    parser = argparse.ArgumentParser(description="Trunk audit")
    add_common_args(parser)
    parser.add_argument("--native", type=int, help="expected native VLAN (e.g. 99)")
    args = parser.parse_args()

    devices = load_inventory(args.inventory, args.device)
    rows, errors = run_task(devices, get_credentials(), make_collector(args.native))

    print()
    print_table(rows, ["hostname", "interface", "native_vlan", "allowed_vlans", "findings"])
    save_output(rows, args.format, "trunk_audit")
    if errors:
        save_output(errors, args.format, "trunk_audit_errors")


if __name__ == "__main__":
    main()
