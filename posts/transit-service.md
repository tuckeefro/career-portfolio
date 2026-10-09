# Transit analysis post

**Audience:** Public finance, transit planning, applied research, and data analysis.

**Attach:** [Scheduled-frequency PNG](../artifacts/colorado-transit-award-service/scheduled-frequency.png). [Editable SVG](../artifacts/colorado-transit-award-service/scheduled-frequency.svg).

## Post copy

Twelve route labels in June. Nine in September. That comparison alone doesn't tell us how much bus service changed.

I put together a public-source trace of Colorado's first SB24-230 formula grant to RTD and the June 2026 schedule changes linked to it. A useful detail: Route 22 came from the western segment of Route 21, and LD3 was renamed 287. The September list also leaves out several June labels without saying their earlier changes ended.

So I kept the route descriptions and reporting periods separate, then calculated frequencies only where the sources supplied both before and after headways.

For the weekday FreeRide, 4.5 minutes became 3 minutes: about 13.33 to 20 scheduled departures per hour per direction, a 50% increase. Two other comparable rows show doubled scheduled frequency.

The attached chart shows those three comparisons. These are announced schedules. The retained material doesn't establish actual service operated, rider outcomes, or how much change the grant caused.

I published the route crosswalk, source links, calculation method, and a checking script so the result can be inspected.

Chart, data, and method: https://github.com/tuckeefro/career-portfolio/blob/main/artifacts/colorado-transit-award-service/frequency-comparison.md

## Caption

Three directly comparable headway changes in RTD's announced June 2026 service: weekday FreeRide, Route 43's specified weekday peak segment, and weekday ART. Frequency equals 60 divided by headway in minutes.

## Alt text

Paired bars show headway-derived scheduled departures per hour per direction before and after the announced changes: FreeRide rises from 13.33 to 20, Route 43's specified weekday peak segment from 4 to 8, and ART from 1 to 2. The figure identifies separate service periods and states that the rates describe announced schedules.

## Evidence behind the wording

The [route crosswalk](../artifacts/colorado-transit-award-service/route-service-crosswalk.csv), [calculation checker](../artifacts/colorado-transit-award-service/build_crosswalk.py), and [source record](../artifacts/colorado-transit-award-service/README.md) support this post. The [frequency comparison](../artifacts/colorado-transit-award-service/frequency-comparison.md) explains the calculation and its direction/headway assumption.

A change from twelve to nine listed labels is not a measured loss of three routes. These three rates cannot be added into a systemwide service estimate. Grant dollars per route, delivered service, and causal effects have not been calculated.
