# Desktop handoff

Open this file first when returning to the desktop.

## Current state

The portfolio expansion work is organized in GitHub issues:

- #8 — SCAMP electrical standalone repo
- #9 — Colorado public-systems research repo
- #10 — compressed-air model repo
- #11 — harden existing software repos
- #12 — refactor `career-portfolio` as the hub

The architecture and migration rules are in `docs/REPO_EXPANSION_PLAN.md` on the `portfolio-expansion` branch.

## Next action

Do **Issue #8 first**.

Do not start by redesigning the career-portfolio README. The hub refactor comes after a satellite actually exists.

### Create the repository

```bash
cd ~/wherever/you/keep/repos

gh repo create tuckeefro/scamp-electrical \
  --public \
  --description "As-built electrical integration, solar charging, battery monitoring, commissioning, and fault isolation for a 2008 Scamp 13-foot trailer"

git clone git@github.com:tuckeefro/scamp-electrical.git
cd scamp-electrical
```

### Bootstrap the package

```bash
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
```

### First README content to establish before migration

The README must answer, without sales language:

1. What physical system is this?
2. What was installed by Tucker?
3. What is the as-built topology?
4. What design constraints drove the 100 W roof + 200 W portable arrangement?
5. What protection/monitoring equipment is installed?
6. What failed during commissioning?
7. What test isolated the fault?
8. What evidence is contemporaneous versus reconstructed later?
9. What has not yet been validated or calculated?

### Initial migration candidates from `career-portfolio`

Review these before copying anything:

- `projects/mobile-power.md`
- `artifacts/mobile-power/README.md`
- SCAMP fault-isolation SVG/PNG
- SCAMP battery-monitor installation photograph

The new repo should become canonical for the SCAMP engineering package. The career portfolio should eventually retain a concise summary and preview, with a link outward.

## Stop condition for the first desktop session

Do not try to finish the whole repository.

A good first stop is:

- new repo exists publicly
- skeleton committed
- README states the evidence boundary
- current as-built electrical topology is captured in text or a rough diagram
- existing portfolio evidence has been inventoried but not blindly copied

At that point, continue #8 by turning the rough topology into a proper one-line/as-built drawing and filling the commissioning record.
