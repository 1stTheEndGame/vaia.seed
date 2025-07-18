#!/usr/bin/env python3
"""
Phase‑aware Seed.VAIA bootstrapper
• Reads VAIA_Initial_Module_Deployment_Plan.md
• Starts services phase‑by‑phase via Docker Compose
• Records healthy containers in core/registry.json
"""
import subprocess, json, re, sys, pathlib, time

# --- locate project root no matter how we're run ----------------
if getattr(sys, "frozen", False):  # running as PyInstaller exe
    ROOT = pathlib.Path(sys.executable).parent
else:  # running as .py file
    ROOT = pathlib.Path(__file__).resolve().parent.parent
# ----------------------------------------------------------------

DOCS_DIR   = ROOT / "docs"
REGISTRY   = ROOT / "core" / "registry.json"
PLAN_FILE  = DOCS_DIR / "VAIA_Initial_Module_Deployment_Plan.md"
COMPOSE_CMD = ["docker", "compose"]

# ---------------- helpers ----------------

def load_json(path):
    return json.loads(path.read_text(encoding="utf‑8")) if path.exists() else []

def save_json(path, obj):
    path.write_text(json.dumps(obj, indent=2), encoding="utf‑8")


def run(cmd, **kw):
    print(f"$ {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=ROOT, **kw)


def container_healthy(name: str, timeout: int = 30) -> bool:
    """Poll `docker inspect` until container is healthy or timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            status = subprocess.check_output(
                ["docker", "inspect", "--format", "{{.State.Health.Status}}", name],
                text=True,
            ).strip()
        except subprocess.CalledProcessError:
            status = "unknown"
        if status in ("healthy", "running"):
            return True
        time.sleep(2)
    return False

# ---------------- phase parser ----------------

def parse_deployment_plan(md_path):
    """Return list of (phase_number, [services])."""
    phases = []
    current = None
    for line in md_path.read_text(encoding="utf‑8").splitlines():
        phase_match = re.match(r"#+\s*Phase\s+(\d+)", line, re.I)
        if phase_match:
            if current:
                phases.append(current)
            current = (int(phase_match.group(1)), [])
            continue
        service_match = re.match(r"[-*]\s+([a-zA-Z0-9_\-]+)", line)
        if service_match and current:
            current[1].append(service_match.group(1))
    if current:
        phases.append(current)
    phases.sort(key=lambda p: p[0])
    return phases

# ---------------- main flow ----------------

def main():
    doctrine = load_json(ROOT / "core" / "doctrine.json")
    print("Loaded doctrine:", doctrine.get("mission", "<no mission>"))

    phases = parse_deployment_plan(PLAN_FILE)
    if not phases:
        print("⚠️  No phases found in deployment plan—starting all services defined in docker‑compose.yml")
        run(COMPOSE_CMD + ["up", "-d"])
        return

    registry = []
    for phase_num, services in phases:
        if not services:
            continue
        print(f"
▶️  Phase {phase_num}: starting {', '.join(services)}")
        run(COMPOSE_CMD + ["up", "-d", *services])
        # health‑check each service
        for svc in services:
            cname = f"vaiaseed-{svc}-1"  # default compose naming convention
            healthy = container_healthy(cname)
            registry.append({
                "service": svc,
                "phase": phase_num,
                "container": cname,
                "healthy": healthy,
            })
            status = "✅" if healthy else "❌"
            print(f"  {status} {svc}")
        save_json(REGISTRY, registry)
    print("
🌱  Bootstrap complete. Registry written to core/registry.json")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)