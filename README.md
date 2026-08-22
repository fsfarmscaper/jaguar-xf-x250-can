# Jaguar XF X250 — CAN Bus Reverse Engineering & DBC

Reverse-engineered CAN database for the Jaguar XF X250 (2008–2015), focused on the
instrument cluster (IPC) and its MS (body) and HS (powertrain) CAN buses.

This project exists to drive a genuine X250 facelift instrument cluster from a bench
rig, but the resulting DBC and documentation are published here in case they're useful
to anyone doing cluster swaps, retrofits, diagnostics, or further reverse engineering
on this platform.

**Status: work in progress.** Both MS and HS buses are well-characterised on the facelift
(2012+) cluster with extensive bench validation. Pre-facelift reference data is retained for
compatibility.

---

## Disclaimer

This project is not affiliated with, endorsed by, or connected to Jaguar Land Rover
in any way. All CAN signal data in this repository was obtained by direct observation
of legally owned hardware (a bench-mounted instrument cluster and associated wiring),
using standard, commercially available CAN interface tools. No proprietary diagnostic
software, encryption circumvention, or unauthorised data sources were used.

This information is provided for educational and interoperability purposes only.
**Use at your own risk.** Working with vehicle CAN networks carries inherent risk to
vehicle electronics. The author accepts no responsibility for damage to vehicles,
modules, or other equipment resulting from use of this information. Always work on
a bench setup or disconnected module where possible — not a running vehicle — until
a signal is fully confirmed safe.

See [LICENSE](LICENSE) and [LICENSE-DOCS](LICENSE-DOCS) for terms covering code and
documentation/data respectively.

---

## Hardware

| Item | Detail |
|------|--------|
| Cluster | EX23-10849-AA — 2013/2014 facelift, XFR-S variant, 190 MPH face |
| Platform | X250, facelift (MY2012+) |
| Connectors | C2MC01A (32-pin, CAN/switches), C2MC01B (32-pin, power/grounds) |
| Bench interface | 2x CANable USB devices running Candlelight firmware |
| Capture/analysis | SavvyCAN using QT Candlelight dll |

Full pinout: [`docs/cluster_pinout.md`](docs/cluster_pinout.md)
Bench bring-up procedure: [`docs/bench_setup.md`](docs/bench_setup.md)

---

## Bus Architecture

| Bus | Baud | Connector pins | Content |
|-----|------|----------------|---------|
| MS (medium-speed, "body") | 125 kbps | C2MC01A pins 4/5 | Ignition, keepalive, fuel, climate, BCM, gear |
| HS (high-speed, "powertrain") | 500 kbps | C2MC01A pins 1/2 | RPM, vehicle speed, oil temp, gear (powertrain side) |

The cluster acts as a gateway between the two buses. Both buses have internal 120Ω
termination inside the cluster — add a second 120Ω at the transceiver end of each
bus on a bench rig.

---

## Confirmed Signals

Confidence key: `c_` confirmed (bench-verified gauge/display response or
authoritative source document) · `i_` inferred (decoded from data analysis, not
independently bench-confirmed) · `u_` unknown (frame identified, content undecoded)

### MS Bus

| CAN ID | Name | Confidence | Decode | Notes |
|--------|------|-----------|--------|-------|
| 0x028 | Gear selector | c_ | byte 4 bitmask | Source: Rhys Morgan `Id40.js` |
| 0x068 | Fuel level | c_ | bytes 3–4 LE uint16 | Bench-calibrated, 5 points |
| 0x088 | HS wake trigger | c_ | byte 3 = 0x06 | **MS-only** — confirmed HS-only TX does not wake cluster |
| 0x208 | Climate control | i_ | bitfield | Source: Rhys Morgan `canMapping.json` |
| 0x2A8 | BCM settings | i_ | bitfield | Bidirectional, cluster reads only |
| 0x513 | Fuel display enable | i_ | — | Required for fuel needle; 40s averaging delay |

### HS Bus — Facelift (2012+) — Gauge & Sensor Inputs

| CAN ID | Name | Confidence | Decode |
|--------|------|-----------|--------|
| 0x20B | Wheel speeds / ABS | c_ | bytes 6–7 = vehicle speed (mph formula: `raw × 0.0064310 + 1.20`) |
| 0x24B | Wheel speeds front | i_ | front wheel speeds + yaw rate |
| 0x280 | Steering angle | i_ | steering wheel angle |
| 0x294 | Wheel speeds rear | i_ | rear wheel speeds + lateral accel |
| 0x295 | RPM (ECM) | c_ | bytes 6–7 BE, `raw & 0x1FFF = rpm` (top 3 bits masked) |
| 0x2B5 | Throttle position | i_ | throttle angle percentage |
| 0x3D3 | Transmission oil temp | i_ | byte 4 LE, `raw − 40 = °C` |
| 0x3F3 | Gear position (TSM) | c_ | fully decoded with gear/mode table; includes manual/sport modes |
| 0x315 | Air temp | i_ | ambient/outside air temperature |
| 0x353 | Gear selector | i_ | gear signal (separate from 0x3F3) |
| 0x4D5 | Engine temp (ECM) | c_ | byte 6, `raw − 60 = °C` (part of multi-signal frame) |

### HS Bus — Facelift Cluster Outputs & Status Frames

| CAN ID | Name | Confidence | Notes |
|--------|------|-----------|-------|
| 0x217 | Battery relay | c_ | Battery charging current relay from MS, ~8ms |
| 0x257 | RTC / clock | c_ | Battery voltage relay + day/month + rolling counter |
| 0x4FF | RTC timestamp | c_ | 32-bit counter (~10 Hz), cluster's real-time base |
| 0x337 | Door status | c_ | FL/FR/RL/RR/trunk/hood closed flags (cluster-owned) |
| 0x457 | Lighting status | i_ | Sidelights + auto-lights mode (mirrored from MS) |
| 0x400–0x407 | CCF blocks | c_ | Car Configuration File broadcast (MS→HS gateway); controls TPMS/BSM warnings |
| 0x404, 0x405 | Vehicle status | c_ | Multiplexed: battery voltage, VIN segments |
| 0x3F5 | ECM faults | c_ | Oil level status, engine fault, restricted performance flags |
| 0x4B5 | ASL/DTC status | c_ | Check engine light, oil level system fault, ASL indicator |
| 0x29B | DSC/ABS status | c_ | DSC/ESP/ABS faults and state machine |
| 0x3EB | DSC/ABS status (alt) | c_ | Park brake indicator, EBD fault, emergency brake assist |
| 0x422 | GSM/ETM mode | c_ | Dynamic/Winter mode request, ETM program status (GSM) |
| 0x35F | ACC status | c_ | Adaptive cruise control module presence |
| 0x3CF | AFLS status | c_ | Adaptive front lighting system module presence |
| 0x2C8 | ADCM status | c_ | Adaptive damping control module presence |
| 0x39A | Airbag/seatbelt | c_ | Airbag and seatbelt warning indicators |
| 0x53F | EPB status | c_ | Electric parking brake |
| 0x250, 0x397, 0x45D, 0x47D | Unknown | u_ | Present but undecoded; may be module presence frames |
| 0x1E7 | Cluster RTR | c_ | Remote transmission request (cluster-owned, observe only) |

Full DBC: [`hs_bus.dbc`](hs_bus.dbc) · [`ms_bus.dbc`](ms_bus.dbc)

---

## Sources & Credits

- **Rhys Morgan** — [`github.com/rhysmorgan134/x250-can`](https://github.com/rhysmorgan134/x250-can) — X250-specific CAN signal decoders (`Id40.js`, `HsInfo.js`, `MsInfo.js`, and others) and bus architecture reference (MS/HS split). Note: his repo's candumps are primarily Freelander 2, not X250 — the platform specifications are the useful part.
- **Joshua Denson** — [`github.com/joshuadenson`](https://github.com/joshuadenson) — provided 2015 X250 candumps that were instrumental in validating and expanding the HS bus reverse engineering.
- **Tom-evnut** — Land Rover rotary gear-change (GSM) project — provided facelift XF250 gear-knob CAN captures and gear-position frame decoding that directly enabled this project's comprehensive 0x3F3 (TSM gear position) implementation.
- **SomersetEV** — cross-confirmed gear position frame definitions and GSM module operation.
- **VanGogh & other OpenInverter forum contributors** — GSM testing and status/mode frame decode contributions.
- Bench testing, signal isolation, facelift-specific captures, and DBC compilation: this project.

---

## Repository Structure

```
ms_bus.dbc                  MS bus confirmed/inferred signals
hs_bus.dbc                  HS bus (pre-facelift reference + facelift cluster outputs)
docs/
  cluster_pinout.md         Full connector pinout (C2MC01A / C2MC01B)
  bench_setup.md            Bench power-on and bring-up procedure
candumps/
  README.md                 Index of capture files and their provenance
CONTRIBUTING.md             How to contribute a capture or signal decode
LICENSE                     MIT — applies to scripts/tools
LICENSE-DOCS                CC BY-SA 4.0 — applies to DBC files and documentation
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Short version: HS captures from facelift
cars are the single most useful contribution right now. Decoded signals get folded
back into the DBC with credit.