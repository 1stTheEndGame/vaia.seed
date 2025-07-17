<#
  setup_seed_repo.ps1
  Creates starter structure + files for vaia-seed
#>

$ErrorActionPreference = "Stop"
Write-Host "🏗  Building VAIA seed skeleton..."

# --- folder layout ---
$dirs = @(
  "docs",
  "core",
  "modules\env_detector",
  ".github\workflows"
)
$dirs | ForEach-Object { New-Item -ItemType Directory -Force -Path $_ | Out-Null }

# --- helper: write file only if missing ---
function Write-File($Path, $Content) {
  if (Test-Path $Path) { return }
  New-Item -ItemType File -Path $Path -Force | Out-Null
  Set-Content -Path $Path -Value $Content -NoNewline
  Write-Host "  + $Path"
}

# --- files ---
Write-File "README.md" @'
# VAIA Seed Installer

Seed.VAIA is a lightweight bootstrapper …
(quick-start instructions here)
'@

Write-File ".gitignore" @'
__pycache__/
*.py[cod]
*.log
.env
.env.*
venv/
.venv/
build/
dist/
*.spec
'@

Write-File ".env.example" @'
POSTGRES_USER=vaia
POSTGRES_PASSWORD=change_me
POSTGRES_DB=vaia_core
NATS_URL=nats://localhost:4222
'@

Write-File "docker-compose.yml" @'
version: "3.9"
services:
  postgres:
    image: postgres:16
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER"]
      interval: 10s
      retries: 5
  nats:
    image: nats:2.10-alpine
    restart: unless-stopped
    command: ["-js"]
    ports:
      - "4222:4222"
      - "8222:8222"
    healthcheck:
      test: ["CMD", "nc", "-z", "localhost", "4222"]
      interval: 10s
      retries: 5
volumes:
  db_data:
'@

Write-File "core\doctrine.json" @'
{
  "mission": "Enable autonomous, aligned growth of VAIA agents in service of the Operator.",
  "values": ["autonomy", "alignment", "security", "transparency"],
  "operator_handle": "Wyatt"
}
'@

Write-File "core\registry.json" "[]"

Write-File "core\seed_bootstrap.py" @'
#!/usr/bin/env python3
"""
Seed.VAIA bootstrapper
"""
import subprocess, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
def load(p): return json.load(open(p, "r", encoding="utf-8"))
def run(cmd): subprocess.check_call(cmd, cwd=ROOT)
def main():
    print("Loaded doctrine:", load(ROOT / "core" / "doctrine.json")["mission"])
    run(["docker", "compose", "up", "-d"])
if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: sys.exit(0)
'@

Write-File "modules\env_detector\Dockerfile" @'
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "env_detector.py"]
'@

Write-File ".github\workflows\build-seed.yml" @'
name: Build Seed Executable
on:
  push:
    tags:
      - "v*"
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install pyinstaller
      - run: pyinstaller --onefile core/seed_bootstrap.py
      - uses: actions/upload-artifact@v4
        with: { name: seed-binaries, path: dist/seed_bootstrap* }
'@

Write-Host "✅  Files written."
Write-Host "👉  NOW: drop your three blueprint .md files into the docs/ folder."
