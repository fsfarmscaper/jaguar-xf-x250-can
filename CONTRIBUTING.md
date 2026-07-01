# Contributing

Thanks for considering contributing — the most valuable thing this project needs
right now is a **facelift (2012–2015) XF HS CAN capture**. See below for how.

## If you have a facelift XF and an existing CAN tool:

Ideal capture:

- Source: OBD2 port (pins 6 = CAN H, 14 = CAN L)
- Bus: HS only (500 kbps) — MS is already well-characterised
- Duration: 30–60 seconds is plenty
- Conditions: ignition on, engine idling if possible (gives live RPM/speed values
  to correlate against the dash). Engine-off/ignition-on alone is still useful.
- Format: standard candump log (`candump -l can0`) or a SavvyCAN `.csv`/`.asc` export

Open an issue or a PR with the file under `candumps/`, including:

- Car year, engine, trim (if known)
- Capture conditions (idling / ignition-only / driving)
- Tool used

**Your raw capture will not be re-distrubuted without your explicit OK to publish it.**
If you'd rather just share it with me directly and have me fold the decoded signals
into the DBC without your raw log going public, that's completely fine — say so
in the issue and I'll do that instead.

## If you don't have a CAN tool but are willing to help:

There are two low-cost routes. Both require a laptop and a couple of cheap
parts — no soldering, no specialist software licenses.

---

### Option A — CANable clone + SavvyCAN (recommended, ~£10–15 / $15-20 USD total)

This is the same setup used for this project.

**Parts:**
- A CANable / UCAN clone (~£5–8 on AliExpress or Amazon). Search "CANable USB CAN 1.0"
  or "UCAN CAN bus". Any STM32F072-based board with USB-C or micro-USB will work.
  Boards labelled "CANable", "UCAN", or "CANable Pro" are all fine.
- An OBD2 breakout cable with bare pigtail wires (~£3–5 on AliExpress). Search
  "OBD2 pigtail" or "OBD2 breakout cable". You need access to pin 6 (CAN H) and
  pin 14 (CAN L). You do **not** need to modify your car's OBD2 port.

**Software (all free):**
- [dfu-utils](https://dfu-util.sourceforge.net/) — used to flash CandleLight firmware to the CANable when in DFU mode
- [SavvyCAN](https://www.savvycan.com/) — open source CAN capture and analysis tool
- [CandleLight Firmware](https://github.com/candle-usb/candleLight_fw/releases) - CandleLight firmware for the CANable (one-time flash, takes ~1 minute) from the releases page
- [QT Serial Bus Plugin for SavvyCAN (Only required for Windows)](https://github.com/homewsn/candleLight_fw-SavvyCAN-Windows-plugin/releases) - Plugin to allow CANable devices to work with SavvyCAN. Only required on Windows
  

**One-time setup steps:**

Flashing Canable device for use with QT Candlelight USB:

1) Enter bootloader mode (DFU mode): hold the BOOT button if present, or short the 3v3 to BO pins, while plugging the CANable into the laptop via USB.

2) Flash CandleLight firmware: Once the CANable is in DFU mode, use dfu-utils to flash `candlelight_fw.bin`. <br/><br/>
```dfu-util.exe --dfuse-address -d 0483:df11 -c 1 -i 0 -a 0 -s 0x08000000 -D canable_fw.bin```

Check the device driver (WinUSB on Windows):

3) Unplug and replug the CANable. Open Device Manager, right-click the device, choose
   **Update driver → Browse my computer → Let me pick** and select **WinUSB**
   (it will appear as "Candlelight" or similar in the device list).


Add the CANable in SavvyCAN:

4) Add the driver: In Windows, find the program folder for SavvyCAN, and copy the `qtcandlelightcanbus.dll` into the **canbus** folder


Connect the OBD pigtail to the CANable:

5) Connect: 
   - OBD2 pin 6 → CANable CANH, 
   - OBD2 pin 14 → CANable CANL,
   - OBD2 pin 4 or 5 (ground) → CANable GND.




**Capture steps:**

1) With the ignition switched **off**, plug the OBD2 breakout into your car's OBD2 port (under the dash, driver's side).

2) In SavvyCAN: **Connection → Open Connection Window → Add New Device Connection**. 
- For Connection Type select **QT SerialBus Devices**
- For SerialBus Device Type select **candleLight_fw**
- For Port select **gs_usb0**
- Click **Create New Connection**

3) SavvyCAN should automatically start capturing CAN frames

4) Turn ignition to ON (engine running is preferred, ignition-only is fine).

5) In SavvyCAN more frames should appear. Let it run 30–60 seconds. Then 

6) **File → Save Log Frames** → save as **Candump/Kayak** `.log`.

Screenshots of the setup (DFU mode in Device Manager, WinUSB driver selection,
SavvyCAN connection settings) are in [`docs/savvycan_setup/`](docs/savvycan_setup/).

Open an issue if you get stuck at any step — happy to walk through it.

---

### Option B — Raspberry Pi + PiCAN2 (if you already have a Pi)

Rhys Morgan (whose pre-facelift X250 CAN work this project is based on) has a video
walkthrough of setting up a PiCAN2 HAT to log messages from a Jaguar XF:

**[Rhys Morgan — Setting up PiCAN2 to log CAN messages from a Jaguar XF](https://www.youtube.com/watch?v=XK1qhMWP3-g)**

This produces a standard `candump` log file. If you follow his setup, run:

```bash
candump -l can0
```

with the baud rate set to 500000 for HS CAN. Share the resulting `.log` file.

---

Either format (SavvyCAN `.csv` or `candump` `.log`) is fine. Open an issue before
you start if you'd like confirmation your hardware will work — no point capturing
the wrong bus or baud rate.

## If you have a decoded signal or correction

Open a PR against the relevant `.dbc` file, or open an issue describing the signal,
frame ID, byte position, and how you confirmed it (bench test, gauge response,
service documentation, etc). Please include a confidence level if you can:
bench-confirmed, inferred from data pattern, or unconfirmed.

## If you have JTIS / service documentation access

Connector pinouts, module CAN node assignments, and bus topology diagrams from
official documentation are extremely useful for cross-referencing, even without
a live capture. Please don't paste full document scans (copyright) — a description
of relevant content, or a specific pin/signal confirmation, is ideal.

## General

- Keep DBC signal names consistent with the existing `c_` / `i_` / `u_` prefix
  convention (confirmed / inferred / unknown).
- If you're not sure whether something belongs in the repo, open an issue first.
