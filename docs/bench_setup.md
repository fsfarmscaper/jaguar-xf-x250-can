# Bench Bring-Up Procedure

This is the procedure used to safely power on and test an X250 facelift cluster
on the bench, outside the vehicle.

## Phase 1 — Safe power-on (no CAN, no switches)

**Goal:** confirm the cluster accepts 12V, both ground pins are valid, and the
unit powers on without damage.

1. Pre-power checks (multimeter, cluster unpowered) — see resistance check table
   in [`cluster_pinout.md`](cluster_pinout.md). A dead short on the supply rail
   is a hard stop — do not proceed until resolved.
2. Bench PSU: 12.0V, current limit 500mA initially, raise to 2A once stable.
   PSU+ → C2MC01B pin 16. PSU− → C2MC01B pins 22 and 32 (both grounds).
3. Apply 12V and observe:
   - Current draw settling 100–400mA: normal
   - LCD message centre illuminates: normal
   - Most/all warning lights on: normal — no CAN present, all module comms
     show MISSING
   - Current draw exceeding 1A immediately: possible short, remove power
   - No display, <10mA draw: check pin 16 and ground connections
   - Burning smell / smoke: remove power immediately

A 2A+ supply is recommended — a 1A-limited supply can brownout the cluster
during backlight/LCD init.

## Phase 2 — Engineering Test Mode (ETM)

Read-only diagnostic mode. No writes, no configuration changes.

1. Add a momentary pushbutton between C2MC01A pin 14 (TRIP_CYCLE_SW) and GND,
   **with a 470Ω resistor in series**. A direct short to GND may register
   incorrectly or damage the input.
2. With the cluster powered, press and hold the trip switch.
3. While holding, briefly remove and reapply 12V to pin 16 to simulate a START
   button press.
4. Continue holding for 5–8 seconds after the power pulse, then release.
5. Successful entry shows "ENGINEERING TEST MODE" in the message centre.

Navigation: single press advances one step, hold >3 seconds exits. Navigation
is forward-only.

ETM steps include gauge sweep, tell-tale (warning light) test, program version,
LCD pixel pattern tests, and module status screens. The module status screens
(CONNECTED / WAITING / MISSING / FAULTY per module) are the most useful output
for CAN bring-up — they tell you exactly which modules the cluster expects to
hear from, which becomes your fault-suppression priority list.

## Phase 3 — MS bus bring-up

Start transmitting MS bus frames (keepalive, ignition state) and observe
warning lights clearing and gauges responding. See `ms_bus.dbc` for confirmed
frame set. The cluster requires continuous transmission of rolling-counter
frames (e.g. ignition keepalive) — a one-shot or looped log replay that breaks
at the loop boundary will cause the cluster to flag the source as missing.

## Phase 4 — HS bus bring-up

**Currently incomplete on the facelift cluster** — see the Open Problem section
in the main [README](../README.md). Pre-facelift HS gauge frames documented by
Rhys Morgan do not produce a gauge response on this cluster despite the cluster
being fully awake (MS bus active, HS heartbeat/output frames present).

## General notes

- The cluster acts as a gateway between MS and HS buses with disjoint ID spaces.
- Frame ownership matters: frames the cluster transmits itself (confirmed via
  passive bus monitoring before you start any TX) should only be observed, not
  emitted by your bench rig — emitting a cluster-owned frame will cause a bus
  conflict.
- A dual-channel CAN interface (e.g. a Raspberry Pi with a 2-channel CAN HAT) is
  recommended so MS and HS can be driven simultaneously and independently.
