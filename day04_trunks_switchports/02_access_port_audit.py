
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.netutils import (add_common_args, get_credentials, load_inventory,  
                             print_table, run_task, save_output, send_parsed)


def make_collector(vlan_filter):
    def collect(conn, dev):
        rows = []
        for port in send_parsed(conn, "show interfaces status"):
            vlan = port["vlan_id"]
            if vlan in ("trunk", "routed"):          
                continue
            if vlan_filter and vlan != str(vlan_filter):
                continue
            status = port["status"].lower()
            finding = "OK"
            if status == "err-disabled":
                finding = "ERR-DISABLED"
            elif status == "connected" and vlan == "1":
                finding = "IN-VLAN-1"
            elif status == "notconnect":
                finding = "UNUSED"
            rows.append({
                "hostname": dev["hostname"],
                "interface": port["port"],
                "name": port["name"],
                "status": port["status"],
                "vlan": vlan,
                "speed": port["speed"],
                "duplex": port["duplex"],
                "finding": finding,
            })
        return rows
    return collect


def main():
    parser = argparse.ArgumentParser(description="Access port audit")
    add_common_args(parser)
    parser.add_argument("--vlan", type=int, help="only show ports in this VLAN")
    parser.add_argument("--problems-only", action="store_true", help="hide OK ports")
    args = parser.parse_args()

    devices = load_inventory(args.inventory, args.device)
    rows, errors = run_task(devices, get_credentials(), make_collector(args.vlan))
    if args.problems_only:
        rows = [r for r in rows if r["finding"] != "OK"]

    print()
    print_table(rows, ["hostname", "interface", "name", "status", "vlan", "finding"])
    save_output(rows, args.format, "access_port_audit")
    if errors:
        save_output(errors, args.format, "access_port_audit_errors")


if __name__ == "__main__":
    main()
