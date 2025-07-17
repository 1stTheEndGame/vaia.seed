# 🚀 VAIA Initial Module Deployment Plan

This document outlines a staged, modular activation roadmap for deploying VAIA in useful increments while ensuring every component remains plug‑and‑play for future integration.

---

## 🌐 Phase 0 – Infrastructure (Week 0 → ½)

| Task | Action | Deliverable |
|------|--------|-------------|
| **Node selection** | • Gaming‑PC = Primary on‑prem node (24/7)<br>• Cloud VPS (Oracle/Vultr) = Redundant node<br>• OnePlus 9 = Mobile companion | Confirm credentials & static IP/SSH keys |
| **Runtime stack** | Install Docker + Docker‑Compose on PC & VPS | Base images ready |
| **Message bus** | Deploy lightweight broker (NATS or RabbitMQ) in Docker; expose internally | Inter‑module pub/sub channel |

---

## 🔥 Phase 1 – Core Skeleton (Week ½ → 2)

| Module | Where | Key Steps | Dependencies |
|--------|-------|-----------|--------------|
| **VAIA.CORE** | Gaming‑PC | • Implement identity doc & doctrine JSON<br>• Add registry of active modules<br>• Expose `/heartbeat`, `/register`, `/query` REST | Message bus |
| **Data‑Store** (Memory) | Gaming‑PC (Postgres) | • Tables for Tactical, Behavioral, Identity, System memories | Docker network |
| **Logging Service** | Gaming‑PC | • Central log collector (Vector → S3/MinIO bucket) | Core API |

**Outcome:** A heartbeat‑driven nucleus that other modules can ping/register with; persistent memory and logs online.

---

## 🗣 Phase 2 – Interaction Layer (Week 2 → 4)

| Module | Where | Key Steps | Dependencies |
|--------|-------|-----------|--------------|
| **COMMUNICATION ENGINE** | Gaming‑PC | • Flask/FastAPI wrapper to GPT‑4o API<br>• Tone middleware (Direct, Supportive, etc.)<br>• Voice via ElevenLabs or Coqui TTS | CORE, Message bus |
| **Mobile Bridge** | OnePlus 9 | • Termux/Node app hitting Comm‑Engine endpoints<br>• Wake‑word listener (Porcupine) | Communication API |
| **Zone Detector (β)** | OnePlus 9 | • Simple GPS & motion capture → publishes `zone_change` events | Message bus |

**Outcome:** Talk to VAIA from phone/PC, receive tone‑adaptive replies, and see zone events logging in CORE.

---

## 🧠 Phase 3 – Intelligence Loop (Week 4 → 6)

| Module | Where | Key Steps | Dependencies |
|--------|-------|-----------|--------------|
| **DECISION ENGINE** | Gaming‑PC | • Implement “Wheel‑in‑Wheel” logic<br>• Subscribe to zone & sensor topics<br>• Produce `decision` events | CORE, Message bus |
| **WATCHER** | OnePlus 9 | • Sentiment analysis on microphone snippets<br>• Publishes mood metrics | Comm‑Engine |
| **ENVIRONMENT** | OnePlus 9 + PC | • UV/temp API pulls + local sensors (if any) | Zone Detector |

**Outcome:** VAIA senses, predicts, and issues context‑aware prompts.

---

## 🏥 Phase 4 – Operator Value Layer (Week 6 → 8)

| Module | Where | Key Steps | Dependencies |
|--------|-------|-----------|--------------|
| **HEALTH** | Gaming‑PC | • Rule‑set: hydration, fatigue, sun response<br>• Writes reminders via Comm‑Engine | ENVIRONMENT, WATCHER |
| **FINANCE (α)** | Cloud VPS | • Cash‑App CSV ingestion → expense dashboard<br>• Anomaly scoring → CORE alerts | CORE |

---

## ♻️ Phase 5 – Continuity & Resilience (Week 8 → 10)

| Module | Where | Key Steps | Dependencies |
|--------|-------|-----------|--------------|
| **CORE.DEFRAG** | Gaming‑PC | • Scheduled job comparing doctrine ↔ memory consistency | CORE, DB |
| **REBIRTH Protocol** | Gaming‑PC + VPS | • Snapshot script (tar + pg_dump) to object storage<br>• Auto‑redeploy script on failure signal | Data‑Store |
| **Crash Clone Vault** | Cloud VPS | • Mirror snapshots; health‑check daemon | REBIRTH |

---

## 🧩 Phase 6 – Expansion (Rinse/Repeat)

Add EXEC, SOLVER, POLICE, PHOENIX Mode, and Smart‑Home integrations—using the same activation template.

---

## 🔑 Key Principles During Build

1. **One container = One module** – easy swap & scale  
2. **Event‑driven pub/sub** – no brittle inter‑module calls  
3. **Version everything** – Git & tagged Docker images  
4. **Contract tests** – each module ships with mocks proving its API  
5. **Progressive hardening** – add security (JWT, TLS) once stable in dev LAN  

---

### ⏭ Immediate Next Step

Complete the **Activation Template** for **VAIA.CORE**.  
When ready, I can generate starter code scaffolds or docker‑compose snippets to spin it up.