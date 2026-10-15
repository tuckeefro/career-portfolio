# Portfolio repo expansion plan

## Objective

Turn `career-portfolio` into the navigation/evidence hub for a small set of deeper standalone repositories. Promote only work that has an independent technical life beyond "evidence that Tucker did something."

A standalone repo must improve inspectability. It should contain a system, model, analysis, or implementation that an external reviewer can inspect and reproduce without inflating thin material into a project.

## Architecture

### Keep in `career-portfolio`

These remain case studies because their strongest value is the documented professional contribution, not a public source tree:

- Pouch Factory production startup and historical compressed-air case
- Maybell Quantum cryogenic hardware
- fabrication/CNC and waterjet repair
- Mines capstone unless enough original publishable technical material is recovered to justify a real repository

Do not export private/employer material merely to make these look fuller.

### Promote to standalone repositories

1. `scamp-electrical`
   - physical system design/integration
   - as-built architecture
   - installation photographs
   - wiring/protection documentation
   - commissioning measurements
   - real fault isolation and corrective action
   - future calculations and revisions

2. `colorado-public-systems`
   - reproducible public-data research
   - source ledger
   - data transformations
   - quantitative checks
   - explicit measurement limits
   - individual analyses as modules rather than disconnected portfolio artifacts

3. `compressed-air-storage-model`
   - reusable computational engineering model
   - equations and units
   - parameterized inputs
   - tests/checks
   - generated plots and tables
   - DOE method attribution

### Existing standalone repositories

Do not copy their source code into `career-portfolio`. Harden the repositories themselves and link to them:

- VanaHR
- Argus Audit
- ShiftForge
- Lavatune
- CodexDeck

For each, the standalone repo should make it possible to determine:

1. What exists?
2. How does it work?
3. What did Tucker personally direct, decide, test, or verify?
4. Which implementation work was produced by AI coding agents?
5. How can a reviewer reproduce or inspect the claim?

## Canonical-source rule

Every substantive artifact gets one canonical home.

- career claim / professional narrative -> `career-portfolio`
- SCAMP as-built engineering package -> `scamp-electrical`
- Colorado research data/method/code -> `colorado-public-systems`
- compressed-air computational implementation -> `compressed-air-storage-model`
- application source/runtime/test history -> its application repository

The hub may retain small preview images and concise summaries, but should link to the canonical source rather than silently diverging.

## Evidence rules

Across all repos:

- distinguish contemporaneous evidence from retrospective reconstruction
- distinguish measured values from calculated or illustrative values
- distinguish design intent from installed/as-built condition
- state important assumptions and measurement limits
- do not invent historical inputs to make a retrospective model appear contemporaneous
- do not overclaim authorship where AI coding agents implemented code under direction
- do not imply causal findings when public data only support descriptive analysis

## Execution order

### Phase 1 — SCAMP

Issue #8.

Create the first new satellite because it has the strongest combination of physical implementation, technical depth, independent ownership, and observable troubleshooting.

Target skeleton:

```text
scamp-electrical/
├── README.md
├── docs/
│   ├── requirements.md
│   ├── architecture.md
│   ├── commissioning.md
│   ├── fault-isolation.md
│   └── safety-and-limitations.md
├── drawings/
│   ├── electrical-one-line.svg
│   ├── wiring-as-built.svg
│   ├── cable-routing.svg
│   └── solar-layout.svg
├── calculations/
│   ├── energy-budget.py
│   ├── voltage-drop.py
│   ├── wire-sizing.md
│   └── protection.md
├── data/
│   └── commissioning.csv
├── bom/
│   └── bom.csv
├── photos/
└── CHANGELOG.md
```

The initial repo does not need every file above completed before first commit. It does need an honest README and a documented as-built topology.

### Phase 2 — Colorado public systems

Issue #9.

Target skeleton:

```text
colorado-public-systems/
├── README.md
├── docs/
│   ├── methods.md
│   ├── source-ledger.md
│   └── measurement-limits.md
├── data/
│   ├── raw/
│   └── derived/
├── src/
├── analyses/
│   ├── transit-award-service/
│   ├── school-funding/
│   └── fiscal-reconciliation/
├── tests/
└── Makefile
```

Keep raw public files only where redistribution is appropriate. Otherwise retain retrieval metadata and source URLs/checksums.

### Phase 3 — compressed-air model

Issue #10.

Target skeleton:

```text
compressed-air-storage-model/
├── README.md
├── pyproject.toml
├── src/
│   └── compressed_air_storage/
├── tests/
├── examples/
├── outputs/
└── docs/
    ├── model.md
    ├── units.md
    └── assumptions.md
```

The promotion is justified only if the model becomes reusable rather than merely moving files out of the portfolio.

### Phase 4 — harden existing software satellites

Issue #11.

Priority:

1. VanaHR
2. Argus Audit / ShiftForge
3. Lavatune / CodexDeck

### Phase 5 — refactor the hub

Issue #12.

After at least one new satellite exists, restructure the `career-portfolio` README into:

- Professional engineering case studies
- Independent engineering systems
- Computational / research work
- Software systems
- Public technical record

`WORK_INDEX.md` should identify whether the canonical project lives locally or in an external repo.

## Desktop commands — first session

Start with SCAMP.

```bash
cd ~/wherever/you/keep/repos

gh repo create tuckeefro/scamp-electrical \
  --public \
  --description "As-built electrical integration, solar charging, battery monitoring, commissioning, and fault isolation for a 2008 Scamp 13-foot trailer"

git clone git@github.com:tuckeefro/scamp-electrical.git
cd scamp-electrical
mkdir -p docs drawings calculations data bom photos

touch README.md \
  docs/requirements.md \
  docs/architecture.md \
  docs/commissioning.md \
  docs/fault-isolation.md \
  docs/safety-and-limitations.md \
  bom/bom.csv \
  data/commissioning.csv \
  CHANGELOG.md

git add .
git commit -m "chore: bootstrap SCAMP electrical engineering package"
git push -u origin main
```

Then inspect issue #8 and migrate only the material whose ownership/provenance is clear.

## Definition of success

The portfolio has spread its wings when an external reviewer can enter through `career-portfolio`, follow a project into its canonical repository, inspect the engineering/research/software work at depth, and return to the hub without encountering duplicated, inflated, or contradictory claims.
