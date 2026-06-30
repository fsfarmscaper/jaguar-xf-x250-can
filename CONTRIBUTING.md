# Contributing

Thanks for considering contributing — the most valuable thing this project needs
right now is a **facelift (2012–2015) XF HS CAN capture**. See below for how.

## I have a facelift XF and a CAN tool

Ideal capture:

- Source: OBD2 port (pins 6 = CAN H, 14 = CAN L), not the cluster connector
- Bus: HS only (500 kbps) — MS is already well-characterised
- Duration: 30–60 seconds is plenty
- Conditions: ignition on, engine idling if possible (gives live RPM/speed values
  to correlate against the dash). Engine-off/ignition-on alone is still useful.
- Format: standard candump log (`candump -l can0`) or a SavvyCAN `.csv`/`.asc` export

Open an issue or a PR with the file under `candumps/`, including:

- Car year, engine, trim (if known)
- Capture conditions (idling / ignition-only / driving)
- Tool used

**I will not redistribute your raw capture without your explicit OK to publish it.**
If you'd rather just share it with me directly and have me fold the decoded signals
into the DBC without your raw log going public, that's completely fine — say so
in the issue and I'll do that instead.

## I don't have a CAN tool but I'm willing to help

A cheap STN1110-based OBD adapter (e.g. OBDLink MX+) with a raw CAN passthrough
mode can do this from a laptop without specialist hardware. Open an issue and I'm
happy to walk through the setup.

## I have a decoded signal or correction

Open a PR against the relevant `.dbc` file, or open an issue describing the signal,
frame ID, byte position, and how you confirmed it (bench test, gauge response,
service documentation, etc). Please include a confidence level if you can:
bench-confirmed, inferred from data pattern, or unconfirmed.

## I have JTIS / service documentation access

Connector pinouts, module CAN node assignments, and bus topology diagrams from
official documentation are extremely useful for cross-referencing, even without
a live capture. Please don't paste full document scans (copyright) — a description
of relevant content, or a specific pin/signal confirmation, is ideal.

## General

- Keep DBC signal names consistent with the existing `c_` / `i_` / `u_` prefix
  convention (confirmed / inferred / unknown).
- If you're not sure whether something belongs in the repo, open an issue first.
