# Jaguar XF X250 — CAN Bus Reverse Engineering & DBC

Reverse-engineered CAN database for the Jaguar XF X250 (2008–2015), focused on the
instrument cluster (IPC) and its MS (body) and HS (powertrain) CAN buses.

This project exists to drive a genuine X250 facelift instrument cluster from a bench
rig, but the resulting DBC and documentation are published here in case they're useful
to anyone doing cluster swaps, retrofits, diagnostics, or further reverse engineering
on this platform.

**Status: work in progress.** MS bus is well-characterised on the facelift cluster.
HS bus is characterised for the pre-facelift platform (via Rhys Morgan's prior work)
but **not yet confirmed working on the facelift (2012+) IPC** — see
[Open Problem](#open-problem-facelift-hs-bus) below.

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
| 0x07E | Keepalive | c_ | static/rolling | ~50ms, mandatory — cluster requires this to stay alive |
| 0x07D | Ignition state | c_ | byte 1: 0x00/0x20 | ~39ms |
| 0x028 | Gear selector | c_ | byte 4 bitmask | Source: Rhys Morgan `Id40.js` |
| 0x068 | Fuel level | c_ | bytes 3–4 LE uint16 | Bench-calibrated, 5 points |
| 0x513 | Fuel display enable | i_ | — | Required for fuel needle; 40s averaging delay |
| 0x208 | Climate control | i_ | bitfield | Source: Rhys Morgan `canMapping.json` |
| 0x2A8 | BCM settings | i_ | bitfield | Bidirectional, cluster reads only |
| 0x088 | HS wake trigger | c_ | byte 3 = 0x06 | **MS-only** — confirmed HS-only TX does not wake cluster |

### HS Bus — pre-facelift (Rhys Morgan reference, untested on facelift)

| CAN ID | Name | Confidence | Decode |
|--------|------|-----------|--------|
| 0x099 | RPM | i_ | bytes 4–5 BE, mask `& ~0xE000` |
| 0x179 | Vehicle speed | i_ | bytes 2–3 BE, `raw × 0.65 / 100 = km/h` |
| 0x3B9 | Oil temp | i_ | byte 5, `raw − 60 = °C` |
| 0x0D9 | Coolant temp | i_ | byte 0, `raw − 60 = °C` — no gauge on this cluster, message-centre only |

### HS Bus — facelift cluster self-output (new, this project)

Captured directly from the cluster's own HS transmissions at power-on. Not present
in any pre-facelift documentation — appears to be facelift-specific or simply
undocumented previously.

| CAN ID | Confidence | Decode | Notes |
|--------|-----------|--------|-------|
| 0x217 | c_ | static | HS heartbeat, ~8ms |
| 0x257 | c_ | byte 3/4/5 = HH/MM/SS | Real-time clock |
| 0x4FF | c_ | bytes 4–7 BE uint32 | Unix timestamp, cluster's stored RTC |
| 0x4F7 | i_ | bytes 4–5 / 6–7 | Possible odometer / lifetime counter |
| 0x511 | i_ | byte 1 state sequence | HS-side init state machine (separate from MS 0x511) |
| 0x250, 0x337, 0x397, 0x457, 0x45D, 0x47D | u_ | — | Present, undecoded |

Full DBC: [`hs_bus.dbc`](hs_bus.dbc) · [`ms_bus.dbc`](ms_bus.dbc)

---

## Open Problem: Facelift HS Bus

The pre-facelift HS gauge frames (0x099 RPM, 0x179 speed) documented by Rhys Morgan
**do not produce any gauge response on the facelift cluster**, even with the cluster
fully awake and displaying. MS-bus wake (0x088) and the cluster's own HS output
frames are confirmed working — the gap is specifically the HS gauge *input* frames.

**What's needed:** a short HS CAN capture (30–60 seconds, idle, OBD2 port,
500 kbps) from a genuine 2012–2015 facelift XF. If you have one, see
[CONTRIBUTING.md](CONTRIBUTING.md).

---

## Sources & Credits

- **Rhys Morgan** — [`github.com/rhysmorgan134/x250-can`](https://github.com/rhysmorgan134/x250-can) — primary reference for pre-facelift X250 CAN architecture, JS signal decoders (`Id40.js`, `HsInfo.js`, `MsInfo.js`, and others), and bus split (MS/HS). This project would not exist without his prior work — if you're here for X250 CAN, go read his repo too.
- Bench testing, facelift-specific captures, and DBC compilation: this project.

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