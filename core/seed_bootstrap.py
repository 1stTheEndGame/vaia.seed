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
            print(f"
Phase {phase_num}: starting {', '.join(services)}") {', '.join(services)}")
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
Bootstrap complete. Registry written to core/registry.json")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)