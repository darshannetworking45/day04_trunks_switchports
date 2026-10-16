
import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.netutils import (add_common_args, get_credentials, load_inventory,  
                             print_table, run_task, save_output)


def build_commands(spec):
    vlans = spec["allowed_vlans"]
    if not all(1 <= int(v) <= 4094 for v in vlans) or not 1 <= int(spec["native_vlan"]) <= 4094:
        raise ValueError("VLAN IDs must be between 1 and 4094")
    commands = []
    for intf in spec["interfaces"]:
        commands.append(f"interface {intf}")
        if spec.get("encapsulation"):
            commands.append("switchport trunk encapsulation dot1q")
        commands += [
            "switchport mode trunk",
            f"switchport trunk native vlan {spec['native_vlan']}",
            f"switchport trunk allowed vlan {','.join(str(v) for v in vlans)}",
        ]
    return commands


def make_task(design, apply):
    def task(conn, dev):
        spec = design.get(dev["hostname"])
        if not spec:
            return [{"hostname": dev["hostname"], "result": "no design in YAML - skipped",
                     "commands": 0}]
        commands = build_commands(spec)
        if apply:
            conn.send_config_set(commands)
            conn.save_config()
            result = "applied"
        else:
            print(f"    [dry-run] {dev['hostname']}:")
            for line in commands:
                print(f"        {line}")
            result = "dry-run"
        return [{"hostname": dev["hostname"], "result": result, "commands": len(commands)}]
    return task


def main():
    parser = argparse.ArgumentParser(description="Push trunk config from YAML")
    add_common_args(parser)
    parser.add_argument("-t", "--trunks", default=str(Path(__file__).with_name("trunks.yaml")))
    parser.add_argument("--apply", action="store_true", help="really push the config")
    args = parser.parse_args()

    design = yaml.safe_load(Path(args.trunks).read_text())
    devices = load_inventory(args.inventory, args.device)
    print("MODE:", "APPLY (changing devices)" if args.apply else "DRY RUN (read-only)")
    rows, errors = run_task(devices, get_credentials(), make_task(design, args.apply))

    print()
    print_table(rows, ["hostname", "result", "commands"])
    save_output(rows, args.format, "trunk_config_push")
    if errors:
        save_output(errors, args.format, "trunk_config_push_errors")


if __name__ == "__main__":
    main()
