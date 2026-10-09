# Supporting work records

## Technical figures

Open a preview to inspect the figure. Each case links to its underlying account or data and both export formats.

<details>
<summary>Waterjet repair: interrupted cutting and upstream pump inspection</summary>

<img src="fabrication-cnc/waterjet-repair-sequence.png" width="375" alt="Qualitative interrupted-cut strip, pump inspection, and reported return to production after three working days" />

Reconstructed from the repair account; timing and results are owner-reported.

[Supporting record](fabrication-cnc/README.md) · [PNG](fabrication-cnc/waterjet-repair-sequence.png) · [SVG](fabrication-cnc/waterjet-repair-sequence.svg)

</details>

<details>
<summary>SCAMP: the direct-panel test isolates the installed path</summary>

<img src="mobile-power/scamp-pv-fault-isolation.png" width="375" alt="Installed PV path compared with the successful direct test using the 200 W portable panel" />

Functional reconstruction of the troubleshooting account; the source does not specify the initial panel connection.

[Supporting record](mobile-power/README.md) · [PNG](mobile-power/scamp-pv-fault-isolation.png) · [SVG](mobile-power/scamp-pv-fault-isolation.svg)

</details>

<details>
<summary>Maybell: readouts and valve commands share one interface</summary>

<img src="cryogenic-hardware/instrumentation-flow.png" width="375" alt="Instrument and system readouts join a shared GUI with operator commands to pneumatic valves" />

Functional reconstruction; acquisition interfaces and control electronics are unspecified.

[Supporting record](cryogenic-hardware/README.md) · [PNG](cryogenic-hardware/instrumentation-flow.png) · [SVG](cryogenic-hardware/instrumentation-flow.svg)

</details>

<details>
<summary>Compressed air: expansion allowance and first-line operation</summary>

<img src="production-compressed-air/compressed-air-decisions.png" width="375" alt="Air-supply arrangement distinguishes the operated first line from planned second-line demand" />

Functional reconstruction; first-line operation is reported and second-line capacity was not exercised.

[Supporting record](production-compressed-air/README.md) · [PNG](production-compressed-air/compressed-air-decisions.png) · [SVG](production-compressed-air/compressed-air-decisions.svg)

</details>

<details>
<summary>Transit: compare the three complete headway pairs</summary>

<img src="colorado-transit-award-service/scheduled-frequency.png" width="375" alt="Paired frequency bars with percentage changes for three service and period comparisons" />

Calculated from the retained public-source crosswalk; the rates describe announced schedules.

[Supporting record](colorado-transit-award-service/README.md) · [PNG](colorado-transit-award-service/scheduled-frequency.png) · [SVG](colorado-transit-award-service/scheduled-frequency.svg)

</details>

<details>
<summary>ShiftForge: show why one seat remains unfilled</summary>

<img src="shiftforge/constraint-matrix.png" width="375" alt="Two-day synthetic scheduling matrix with assigned workers, rest and PTO exclusions, and an explicit shortage" />

Generated from the retained synthetic fixture and actual normalized scheduler output. It describes an algorithm example, not a deployed staffing result.

[Supporting record](shiftforge/README.md) · [PNG](shiftforge/constraint-matrix.png) · [SVG](shiftforge/constraint-matrix.svg)

</details>

<details>
<summary>Transit: preserve route identity through a split and rename</summary>

<img src="colorado-transit-award-service/route-identity.png" width="375" alt="Former Route 21 splits into east Route 21 and west Route 22; LD3 becomes Route 287" />

Generated from the retained official-source crosswalk. Arrows show identity links; the drawing does not show geographic route geometry.

[Supporting record](colorado-transit-award-service/route-identity.md) · [PNG](colorado-transit-award-service/route-identity.png) · [SVG](colorado-transit-award-service/route-identity.svg)

</details>

<details>
<summary>Lavatune: repeated measurements of two rendering paths</summary>

<img src="lavatune/renderer-comparison.png" width="375" alt="Median frame costs, five individual runs, and minimum–maximum ranges for scalar-field Fluid and analytic contour Fluid" />

Measured offline on one shared GitHub runner with the original pinned benchmark. Raw results, workload, environment, and scope are retained.

[Supporting record](lavatune/README.md) · [PNG](lavatune/renderer-comparison.png) · [SVG](lavatune/renderer-comparison.svg) · [Raw results](lavatune/renderer-benchmark.json)

</details>

## Project records

| Work | Inspect |
|---|---|
| Pouch Factory compressed air | [Decision figure and source status](production-compressed-air/README.md) |
| Maybell instrumentation | [Measurement and operator-control figure](cryogenic-hardware/README.md) |
| Waterjet repair | [Inspection, rebuild, and return-to-production sequence](fabrication-cnc/README.md) |
| SCAMP power | [PV fault-isolation figure and installed monitor photo](mobile-power/README.md) |
| VanaHR | [Recovery paths and evidence](vanahr/README.md) |
| Argus Audit | [Review-to-deletion boundary](argus-audit/README.md) |
| ShiftForge | [Constraint matrix, executed synthetic fixture, and retained checks](shiftforge/README.md) |
| Lavatune | [Measured renderer work and resource ownership](lavatune/README.md) |
| CodexDeck | [Rebuild and acceptance sequence](codexdeck/README.md) |
| Colorado transit research | [Award/service trace](colorado-transit-award-service/README.md) · [Frequency comparison](colorado-transit-award-service/frequency-comparison.md) · [Route identity](colorado-transit-award-service/route-identity.md) |

Account-based physical diagrams are labeled as reconstructions. Software records distinguish source inspection, synthetic execution, and live operation. The private implementations remain in their original repositories.

[Prepared posts and downloadable figures](../posts/README.md) pair two cases with copy, captions, alt text, and PNG exports.

[How to read the revised figures and their evidence](../docs/FIGURE_GUIDE.md).
