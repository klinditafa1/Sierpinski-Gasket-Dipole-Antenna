# Adaptive Fractal Antenna for LEO Terminals

Parametric design and electromagnetic simulation of a **Sierpinski Gasket Dipole**
fractal antenna, developed as part of a Bachelor's thesis in Telecommunications
Engineering at the Polytechnic University of Tirana (UPT). The antenna targets
adaptive, multiband coverage for Low Earth Orbit (LEO) satellite terminals
(e.g. Starlink, OneWeb, Kuiper-class systems).

## What this project does

- Parametrically generates a **Sierpinski Gasket Dipole** antenna geometry
  (2nd-order iteration, bow-tie configuration) using Python inside **FreeCAD**
- Exports the resulting 3D solid model (`.STEP` / `.STL`) for use in
  electromagnetic simulation tools
- Simulates the antenna's electromagnetic behavior in the **Ku band (12–18 GHz)**
  using **Tidy3D** (FDTD — Finite-Difference Time-Domain method)
- Analyzes key antenna and propagation parameters: S11 (return loss), electric
  and magnetic field distribution, far-field radiation patterns, effective
  refractive index, group index, phase/group velocity, and dispersion

## Why fractal geometry

Fractal geometries exploit two properties — **self-similarity** and
**space-filling** — to let a physically compact antenna behave as if it were
much larger electrically. This enables:

- **Miniaturization** — up to ~50–60% size reduction vs. conventional antennas
  for the same resonant frequency
- **Multiband operation** — each iteration level in the fractal resonates at a
  different frequency, giving the antenna tri-band behavior without needing
  separate elements per band
- **Natural impedance matching** — removing metal at each iteration acts as a
  built-in matching network, improving S11

This is particularly relevant for LEO terminals, which need to track fast-moving
satellites across Ku/Ka bands while staying compact, low-power, and low-cost —
constraints where traditional mechanically-steered dish antennas fall short.

## Tech / tools used

| Purpose                    | Tool         |
|-----------------------------|--------------|
| Parametric 3D modeling      | Python + FreeCAD (`Part`, `PartDesign` APIs) |
| Electromagnetic simulation  | Tidy3D (FDTD) |
| Geometry export              | STEP / STL |


## How the geometry is generated

The script builds the antenna recursively:

1. Start with a solid equilateral triangle (iteration 0)
2. Remove the central triangle formed by each edge's midpoints (iteration 1)
3. Repeat the removal on each remaining sub-triangle (iteration 2 — the level
   used in this design, giving tri-band resonance)
4. Mirror the completed arm across the symmetry axis to form the second half
   of the bow-tie dipole
5. Add two small rectangular feed terminals at the center gap and fuse
   everything into a single parametric solid

Because the whole geometry is parametric, changing the base triangle's
dimensions in the script automatically regenerates the full fractal structure
and shifts the resonant frequencies accordingly — no manual redrawing needed.

## Key results (Ku band, 12–18 GHz)

- Confirmed tri-band resonant behavior corresponding to the 2nd-order iteration
- Far-field radiation pattern shows a dipole/quasi-dipole two-lobe shape with a
  central null, consistent with theoretical predictions for microstrip/dipole
  elements on a dielectric substrate
- Moderate, well-behaved dispersion across the band (n_eff, group index, and
  dispersion parameter all vary smoothly and consistently with each other)

## Limitations

- Results are based on simulation only — no physical prototype was fabricated
  or measured
- Only one fractal configuration (Sierpinski Gasket, 2nd iteration) was
  explored; higher iterations, other fractal geometries (Koch, Minkowski), and
  substrate comparisons (FR4 vs. Rogers RO4003C) are natural extensions

## Future work

- Fabricate a physical prototype and validate against simulated S11 and
  radiation pattern
- Explore active tuning elements (varactor diodes / RF-MEMS) for real-time
  frequency, polarization, and beam-steering adaptivity
- Integrate with phased-array beamforming for LEO handover tracking

