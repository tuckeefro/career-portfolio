# What the figures show

The physical-work figures are functional reconstructions of the project accounts. They show the decisions and relationships described there. The transit figures are generated from a retained public-source table. The ShiftForge matrix is generated from retained synthetic inputs and actual normalized scheduler output. The Lavatune chart shows repeated renderer measurements from a retained execution record. Downloadable PNGs accompany the SVGs; the rendering workflow also produces 375-pixel previews for phone-width review.

| Figure | Technical question it explains | Basis | Next original artifact that would strengthen it |
|---|---|---|---|
| [Waterjet](../artifacts/fabrication-cnc/README.md) | How did an interrupted cutting result lead to pump inspection, a rebuild, and resumed production? | Repair account; qualitative symptom strip; reported timing and result | Annotated cut sample or cylinder-assembly inspection photo, with the pump model and exact observed play |
| [SCAMP](../artifacts/mobile-power/README.md) | How did the direct-panel test narrow the fault to the installed path? | Installation/troubleshooting account; two functional connection configurations | Test readings or a connector photograph showing the assembly fault and correction |
| [Maybell](../artifacts/cryogenic-hardware/README.md) | How did readouts and operator valve commands share one interface? | Instrumentation account; one functional GUI hub | Shareable actual GUI screenshot or interface drawing identifying instrument and control connections |
| [Compressed air](../artifacts/production-compressed-air/README.md) | Which load was operated, which capacity was only planned, and what cost/duty-cycle tradeoffs were accepted? | Integration account; solid operating branch and dashed planned branch | Original machine requirements and airflow worksheet, then contemporaneous quotes |
| [Transit frequency](../artifacts/colorado-transit-award-service/frequency-comparison.md) | How much did announced frequency change where both headways are known? | Retained crosswalk, official source descriptions, and reproducible arithmetic | A retained schedule extract would strengthen source inspection; delivered-service evaluation requires different data |
| [ShiftForge](../artifacts/shiftforge/README.md) | Which workers were excluded, who was assigned, and where did a required seat remain unfilled? | Retained synthetic inputs and actual normalized scheduler output; rest, PTO, and availability shown explicitly | A separately retained representative run would extend coverage; this example does not establish deployed staffing or compliance |
| [Transit identity](../artifacts/colorado-transit-award-service/route-identity.md) | How do a route split and a renamed identifier affect before/after comparisons? | Retained crosswalk rows 21, 22, and 287; official final-service descriptions | Route geometry and schedule extracts would support a geography-and-period comparison |
| [Lavatune renderer](../artifacts/lavatune/README.md) | How much time do two implemented Fluid paths spend on the same configured synthetic workload? | Five executions of the original pinned benchmark on one runner; raw measurements and environment retained | A separate live-terminal or power study would answer display-cost or energy questions |

## Reading the graphics

The waterjet strip is a sketch of the reported pattern, not a measured depth profile. Pump internals and the failed component are not established.

The SCAMP paths group the installed wiring and connectors because their physical order is not recorded. The successful direct connection is the diagnostic comparison.

The Maybell arrows identify measurement and command roles. They do not specify communication protocols, pinouts, drivers, control timing, or valve electronics.

The compressed-air dashed branch represents demand allowed for during design. It does not claim that a second line was installed or that its capacity was demonstrated. The capacity basis is qualitative because the sizing inputs are not retained.

The transit rows share one frequency scale. Percent changes are computed within each service and period, using `60 / headway in minutes`. They describe announced scheduled rates per direction under the stated headway assumption. No route aggregation or causal funding estimate follows from them.

The ShiftForge cells combine retained assignments with explicit fixture constraints. On March 22, A has eight hours before the morning start against a ten-hour rest requirement, B has approved PTO, and C is assigned. On March 23, A and B are assigned while C is unavailable. One required seat remains unfilled. The drawing uses a retained run; generating it does not rerun the private scheduler or establish browser, integration, or regulatory behavior.

The transit identity arrows describe the old Route 21 splitting into eastern Route 21 and western Route 22, and LD3 being renamed Route 287. Route labels alone cannot identify comparable geography, additional corridor service, or delivered service.

The Lavatune bars show median milliseconds per simulated frame, with all five runs and their observed min–max ranges. The paired ratio compares scalar-field and contour costs within each original script invocation. These are body-simulation and material-generation timings; live audio and terminal presentation are outside the measured scope. Host conditions and source revision are retained with the raw results.

## To strengthen a case

Retain the original artifact, identify its date and operating conditions where known, mark the relevant feature, and explain the decision it supported. Keep recalled facts labeled as recollection. A repair photo, worksheet, or screenshot can be redacted when needed while preserving the technical relationship a reader needs to inspect.

### Prioritize inspectable physical work

A strong case figure pairs an annotated hardware or CAD view with the critical constraint, the resulting decision, and the check used to assess it. Build one complete case from the best available original material.

| Case | Figure with technical substance | Smallest useful source |
|---|---|---|
| Pouch Factory air supply | Demand breakdown and selected capacity at the required pressure, linked to the actual supply arrangement | Machine requirement sheet, sizing worksheet, or confirmed equipment nameplate and demand inputs |
| Pouch Factory layout | Actual equipment and material flow with the service-access or utility constraint marked | Layout drawing or photographs sufficient to confirm placement and connections |
| Maybell manufacturing trial | Fixture/welder/CNC detail showing the modification, required alignment, and observed precision limit | Publishable setup view or sketch plus the criterion used to recognize insufficient precision |
| SCAMP or Sprinter power | Confirmed power and protection schematic with cable lengths/gauges, fuse ratings, shunt return path, and a worked voltage-drop check | Actual topology and component/cable details; treat each vehicle separately |
| Fabrication or Mines capstone | Drawing of one personally designed part or assembly with critical dimensions, material/fit choices, and its manufacturing or test check | Original drawing/report or enough confirmed detail to reconstruct the specific contribution |

Recalled geometry or operating observations can be used when labeled. A new engineering calculation or bench study can also be published as current work with explicit inputs, assumptions, method, and results, without presenting it as a historical project record.

## Regenerate and check the exports

The source SVGs live beside their supporting records. The frequency chart, route identity drawing, ShiftForge matrix, and Lavatune benchmark chart are generated from retained records. [The supplemental generator](../scripts/supplemental_figures.py) derives the matrix and route links and checks their source relationships. Regeneration writes a PNG beside every source figure; checking compares generated SVGs and all retained PNG pixels with fresh renders.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install CairoSVG==2.7.1 matplotlib==3.9.2
.venv/bin/python artifacts/colorado-transit-award-service/build_crosswalk.py
.venv/bin/python scripts/render-portfolio.py --write-assets
.venv/bin/python scripts/render-portfolio.py --check
.venv/bin/python scripts/verify-portfolio.py
```

Commit the updated source and PNG together. The default output directory contains full-size PNGs, 375-pixel previews, and the generated transit SVG. CI uses check mode so it detects a stale export without replacing the committed copy.
