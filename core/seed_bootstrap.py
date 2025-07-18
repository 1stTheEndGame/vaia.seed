#!/usr/bin/env python3
"""
Phase-aware Seed.VAIA bootstrapper
• Reads docs/VAIA_Initial_Module_Deployment_Plan.md
• Starts services phase-by-phase with Docker Compose
• Records healthy containers in core/registry.json
"""
import subprocess, json, re, sys, pathlib, time

ROOT = pathlib.Path(sys.executable).parent if getattr(sys, "frozen", False) \
       else pathlib.Path(__file__).resolve().parent.parent

DOCS_DIR = ROOT / "docs"
REGISTRY = ROOT / "core" / "registry.json"
PLAN_MD  = DOCS_DIR / "VAIA_Initial_Module_Deployment_Plan.md"
COMPOSE  = ["docker", "compose"]

load_json  = lambda p: json.loads(p.read_text("utf-8")) if p.exists() else []
save_json  = lambda p, obj: p.write_text(json.dumps(obj, indent=2), "utf-8")

def sh(cmd):
    print("$", *cmd); subprocess.check_call(cmd, cwd=ROOT)

def container_ok(name, timeout=30):
    end = time.time() + timeout
    while time.time() < end:
        try:
            out = subprocess.check_output(
                ["docker", "inspect", "-f", "{{.State.Health.Status}}", name],
                text=True).strip()
        except subprocess.CalledProcessError:
            out = "unknown"
        if out in ("healthy", "running"):
            return True
        time.sleep(2)
    return False

def parse_plan(md_path):
    phases, current = [], None
    for ln in md_path.read_text("utf-8").splitlines():
        m_phase = re.match(r"#.+?Phase\s+(\d+)", ln, re.I)
        if m_phase:
            if current: phases.append(current)
            current = (int(m_phase.group(1)), [])
            continue
        m_svc = re.match(r"[-*]\s+([\w\-]+)", ln)
        if m_svc and current:
            current[1].append(m_svc.group(1))
    if current: phases.append(current)
    phases.sort(key=lambda p: p[0])
    return phases

def main():
    doctrine = load_json(ROOT / "core" / "doctrine.json")
    print("Mission:", doctrine.get("mission", "<unset>"))

    phases = parse_plan(PLAN_MD)
    if not phases:
        print("No phases – starting every service in docker-compose.yml")
        sh(COMPOSE + ["up", "-d"]); return

    registry = []
    for num, svcs in phases:
        if not svcs: continue
        print(f"\nPhase {num}: starting {', '.join(svcs)}")
        sh(COMPOSE + ["up", "-d", *svcs])

        for svc in svcs:
            cname = f"vaiaseed-{svc}-1"
            ok = container_ok(cname)
            registry.append({"service": svc, "phase": num,
                             "container": cname, "healthy": ok})
            print(" ", "OK" if ok else "FAIL", svc)
        save_json(REGISTRY, registry)

    print("\nBootstrap complete – see core/registry.json")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
