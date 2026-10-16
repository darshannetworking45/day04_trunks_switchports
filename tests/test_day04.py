

def run(h):
    out = h.run_script("day04_trunks_switchports/01_trunk_audit.py", "--native", "99")
    h.check("day04 trunk audit", out, "NATIVE-VLAN-1;NATIVE-MISMATCH;ALL-VLANS", "10,20,30,99")
    out = h.run_script("day04_trunks_switchports/02_access_port_audit.py", "--problems-only")
    h.check("day04 access audit", out, "IN-VLAN-1", "UNUSED", "ERR-DISABLED")
    out = h.run_script("day04_trunks_switchports/02_access_port_audit.py", "--vlan", "10")
    h.check("day04 access audit --vlan", out, "USER-PC-HR")

    h.SENT.clear()
    out = h.run_script("day04_trunks_switchports/03_trunk_config_push.py")
    h.check("day04 trunk push DRY-RUN", out, "switchport trunk allowed vlan 10,20,30,99", "no design in YAML")
    assert not any(h.SENT.values()), "dry-run must not push config!"
    h.run_script("day04_trunks_switchports/03_trunk_config_push.py", "--apply", "-d", "SW-ACCESS-01")
    assert "switchport trunk native vlan 99" in h.SENT["SW-ACCESS-01"]
    print("PASS  day04 trunk push APPLY")
