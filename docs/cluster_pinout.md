# Jaguar XF X250 — Instrument Cluster Connector Pinout

**Unit used for this project:** EX23-10849-AA (2013/2014 facelift)
**Connectors:** C2MC01A (32-pin, CAN/switches), C2MC01B (32-pin, power/grounds)
**Primary source:** JTIS XF 2013 MY wiring diagrams (413-01), cross-checked against
physical connector photographs.

Wire colour convention: two letters = primary/tracer (e.g. WH-BU = white body,
blue stripe). Signal direction: IP = input to cluster, OP = output from cluster,
B = battery/power, P = ground, VREF = voltage reference, GREF = ground reference.

---

## C2MC01A — CAN, Switches, Stalk Inputs, Column Adjust

| Pin | Signal | Dir | Wire | Notes |
|-----|--------|-----|------|-------|
| **1** | HS_CAN_IN_POS | — | WH-BU | **HS CAN+ 500 kbps** |
| **2** | HS_CAN_IN_NEG | — | WH | **HS CAN– 500 kbps** |
| 3 | AUX_SW_RTN | GREF | GY-YE | Auxiliary lighting stalk return |
| **4** | MS_CAN_IN_NEG | — | VT-OG | **MS CAN– 125 kbps** |
| **5** | MS_CAN_IN_POS | — | GY-OG | **MS CAN+ 125 kbps** |
| 6 | STALK_SW_RET | GREF | GY-YE | Steering column switch return |
| 8 | WASH_WIPE_SW | IP | GY-BN | Wash/wipe switch |
| 9 | DIMMER_LEVEL | IP | BU-WH | Dimmer signal level from lighting stalk |
| 11 | HEADLAMP_SW | IP | YE-BU | Headlamp switch position |
| 12 | EXIT_DELAY_SW | IP | VT-GN | Exit delay switch |
| 13 | COLUMN_ADJUST | IP | GN-VT | Column adjust up/down switch |
| **14** | TRIP_CYCLE_SW | IP | WH-BN | **ETM navigation — 470Ω series to GND** |
| 15 | MAIN_BEAM_FLASH_SW | IP | GN-BN | Main beam / flash switch |
| 16 | DI_SW | IP | VT-BN | Direction indicator switch |
| 19 | COLUMN_RTN | GREF | GN-OG | Column adjust return |
| 22 | LIN | — | — | LIN bus (start control unit / clockspring) — not required for gauge operation |
| 23 | BRAKE_PAD_WEAR | IP | BN-BU | Brake pad wear sensor |
| 24 | COLUMN_ADJUST_AUTO_MAN | IP | YE-VT | Column adjust auto/manual select |
| 25 | FLICK_WIPE_SW | IP | WH-GN | Flick wipe switch |
| 26 | MASTER_WIPE_SW | IP | BU-GN | Master wipe switch |
| 27 | RAKE_POT | IP | WH | Column rake position potentiometer |
| 29 | INT_WIPE_SW | IP | GN-VT | Intermittent wipe switch |
| 30 | AUTOLAMP_SENSOR | IP | — | Autolamp light sensor |
| 31 | AUX_SW_SIGNAL | IP | WH | Aux switch signal (fog lamp SW2) |
| 32 | REACH_POT | P | VT-BN | Column reach position potentiometer |

Pins 7, 10, 17, 18, 20, 21, 28 not confirmed on this variant.

---

## C2MC01B — Power, Grounds, Sensors, Column Motor

| Pin | Signal | Dir | Wire | Notes |
|-----|--------|-----|------|-------|
| 1 | LOW_BRAKE_FLUID | IP | GY-VT | Low brake fluid switch |
| 4 | COLUMN_POT_FEED | VREF | WH-BN | Column potentiometer supply |
| 5 | COLUMN_POT_RTN | GREF | YE-GN | Column potentiometer return |
| 6 | DIMMER_FEED | VREF | WH-BN | Dimmer voltage reference output |
| 8 | IC_SECURITY_OUT | OP | BN-VT | Security indicator output |
| 11 | SECURITY_IND | OP | — | Security indicator |
| 12 | OIL_PRESSURE_SW | IP | GY | Oil pressure switch |
| 14 | COOLANT_LEVEL_SWITCH | IP | WH-OG | Coolant level switch |
| **16** | **LOGIC_PWR** | **B** | **VT-RD** | **12V ignition supply — main cluster power** |
| 18 | COLUMN_UP_IN | VREF | BN-GN | Column up motor input |
| **19** | **COLUMN_PWR** | **B** | **GN-RD** | Column motor 12V — leave open on bench |
| 20 | COLUMN_DWN_OUT | VREF | GY-OG | Column down motor output |
| **22** | **GND** | **P** | **BK** | **Ground** |
| 23 | REACH_SOLENOID | VREF | WH-GN | Column reach solenoid |
| 24 | RAKE_SOLENOID | VREF | BN-VT | Column rake solenoid |
| 25 | LOW_BRAKE_FLUID_RTN | GREF | YE-GY | Low brake fluid return |
| 27 | WIPER_SW_RTN | GREF | BN-VT | Wiper switch return |
| 28 | BRAKE_PAD_WEAR_RTN | GREF | GY-OG | Brake pad wear return |
| 29 | VAPS_PWR | B | GY-BU | VAPS (power steering) supply |
| 30 | VAPS_POS | VREF | GN-BU | VAPS positive reference |
| 31 | VAPS_NEG | GREF | WH-GN | VAPS negative reference |
| **32** | **LOGIC_GND** | **P** | **BK** | **Ground — connect alongside pin 22** |

Pins 2, 3, 7, 9, 10, 13, 15, 17, 21 not confirmed on this variant.

---

## Bench bring-up minimum connections

| Connection | Pin | Wire | Notes |
|-----------|-----|------|-------|
| 12V supply | C2MC01B/16 | VT-RD | Ignition power |
| GND | C2MC01B/22 | BK | Both ground pins required |
| GND | C2MC01B/32 | BK | Both ground pins required |
| HS CAN+ | C2MC01A/1 | WH-BU | 500 kbps |
| HS CAN– | C2MC01A/2 | WH | 500 kbps |
| MS CAN+ | C2MC01A/5 | GY-OG | 125 kbps |
| MS CAN– | C2MC01A/4 | VT-OG | 125 kbps |
| ETM switch | C2MC01A/14 | WH-BN | 470Ω series resistor → GND, momentary pushbutton |

Internal 120Ω CAN termination resistors are present on both buses inside the
cluster. A second 120Ω terminator is required at the transceiver end of each
bus on a bench setup.

### Pre-power resistance checks

| Check | Pins | Expected |
|-------|------|----------|
| HS CAN terminator | C2MC01A/1 – C2MC01A/2 | ~120Ω |
| MS CAN terminator | C2MC01A/4 – C2MC01A/5 | ~120Ω |
| Supply to GND short | C2MC01B/16 – C2MC01B/22 | >10kΩ |
| Supply to GND short | C2MC01B/16 – C2MC01B/32 | >10kΩ |
| GND continuity | C2MC01B/22 – C2MC01B/32 | <5Ω |

A dead short on the supply rail before power-on is a hard stop — do not proceed
until resolved.

### Signals not required for bench bring-up

Column adjustment motor, VAPS/power steering, wiper switches, security indicator,
brake/fluid sensors, autolamp, dimmer, and LIN bus are all present on the
connector but not required for basic gauge operation. They will show as faults
on the cluster (warning lights / message centre) without signals, which is
expected behaviour absent the relevant CAN data.
