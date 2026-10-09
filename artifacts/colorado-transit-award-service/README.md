# CTE-to-RTD award/service trace v0.2

**Status:** Applied budget-to-service trace with an inspectable scheduled-service measure. The new evidence resolves the earlier question of whether a public award-to-service link exists: CDOT and RTD both connect the first $9.25–$9.3 million SB24-230 formula grant to RTD's June 7, 2026 service changes. It does not provide route-level award dollars, executed/reimbursed amounts, actual operations, ridership, or causal effects.

## Research question

What scheduled service did the first SB24-230 formula award to RTD support, and can its public funding descriptions be reconciled to route-level schedule changes without losing the service unit when routes or labels change?

This is a consequential applied question for CTE/CDOT budget oversight, RTD service planners and directors, and riders. It is not a claim that no prior transit-funding research exists. Generic formula funding/performance novelty remains closed; academic novelty for this narrow Colorado reporting and service-measure contribution is unestablished.

## New result

CDOT's May 7 release states that a $9.3 million award was executed to support RTD's June 7 service changes, and lists funded-service examples. RTD's April 29 release reports $9.25 million and says twelve bus routes would receive improvements from the grant. RTD's final June change table defines schedule changes for those twelve route labels. The amount difference is consistent with rounding, but no executed agreement or award-level transaction was inspected to verify exact amount/stage.

Across the two RTD schedule vintages, several service measures can be transcribed directly. The 16th Street FreeRide changes from a 4.5-minute to a 3-minute weekday headway, equivalent to an indicated increase from 13.33 to 20 departures per scheduled hour per direction (+50%) if the headway applies symmetrically. ART changes from hourly to every 30 minutes on weekdays, an indicated increase from one to two departures per scheduled hour per direction (+100%) on the same assumption. Route 43 changes from 15-minute to 7.5-minute weekday peak headways on a specified segment (+100%). Other routes have direct counts or schedule spans: Route 10 reports 11 added trips; Route 104L adds two trips per day; Route 53 is reinstated hourly seven days from 6 a.m. to 9 p.m.; Route 80 is reinstated weekdays from 6 a.m. to 7 p.m. Some post-change headways are stated for Routes 21, 37, and 287, but comparable old baselines are not.

The data table preserves three distinct official descriptions rather than forcing them into a single route count:

- CDOT's May 7 release names selected examples and service categories, including Route 19, Routes 53/80, 21E, a combined 1E/44 “ART Shuttle” designation, Route 37, LD3/287, a new Longmont-to-DEN route, and event capacity. The source does not establish whether this combined label is identical to RTD's separately labeled ART service; RTD's final June page also lists a separate Route 44 alignment change.
- RTD's April 29 and June 7 releases identify twelve grant-linked route improvements: 0L, 10, 16th Street FreeRide, 19, 21, 37, 43, 53, 80, 104L, ART, and 287.
- RTD's September 9 release identifies nine continuing labels: 16th Street FreeRide, 19, 21, 22, 37, 53, 80, LD3/287, and ART. Route 22 was created from the western segment of the old Route 21; LD3 was renamed 287. Thus the change from twelve to nine labels is not a comparable count of service lost. The September list also omits 0L, 10, 43, and 104L, but does not state that those June changes ended.

The reproducible route transcription and arithmetic are in [`route-service-crosswalk.csv`](route-service-crosswalk.csv), produced by [`build_crosswalk.py`](build_crosswalk.py). Each row points to the official source IDs in registry v24.19. Only direct schedule facts and simple headway arithmetic are calculated; no total vehicle-hours, vehicle-miles, grant cost per service unit, or delivered-service estimate is inferred.

## Evidence and measurement boundary

The June schedule-change page describes changes made amid several simultaneous factors: the rail reconstruction, RTD's System Optimization Plan, customer input, ridership, seasonal demand, and operational requirements. The award releases link a set of changes to CTE support; they do not isolate how many schedule units would have existed without the award. The measure is **announced scheduled service**, not operated service. Headway-derived frequencies are per scheduled hour and assume evenly applicable headways; they do not multiply across route span or direction to estimate revenue hours.

## Accountability dashboard check

The public CTE Power BI default Award Summary was inspected in the browser on September 29, 2026. Its accessible view reports 33 projects and $45,507,839 total awards across FY2024–FY2026, with categories Vehicles, Charging/Fueling, Facilities, and Planning. It includes an FY26 RTD row for $3,920,000, “Platte Division Electrical Infrastructure Modernization,” categorized as Charging/Fueling and marked Awarded. That is a separate electrification/facility award, not the $9.25 million SB230 Formula operating grant. No SB230 Formula service-operations row appeared in the accessible default summary/table view. The dashboard's exact completeness and whether other pages include the operations grant were not established because no table export was retained. The browser observation and its limits are recorded in [`dashboard-browser-observation.csv`](dashboard-browser-observation.csv).

The sources do not allocate the aggregate award among routes. They do not establish contract value, reimbursement, outlay, service delivered, costs per added hour/mile, actual passenger trips, access, emissions, or causal impact. The route 21 split and LD3-to-287 rename mean before/after route counts are unstable without a geography-and-period crosswalk. Do not treat RTD customer survey percentages on the schedule page as representative ridership or causal program outcomes.

## Decision and next gate

**Disposition:** The recipient-to-service link is observed and supports a bounded applied accountability/data-product contribution. The schedule-unit artifact is more concrete than a budget-to-apportionment bridge alone. The empirical cost-effect and passenger-outcome branches remain conditional/closed on current public material.

**Disposition of the dollar bridge:** Close the CTE dashboard as a source for the $9.25m operating-grant reconciliation on the current accessible view; do not interpret its RTD $3.92m electrification row as evidence about route operations. The official September 29 board recording is listed, but has no captions and is not text-retrievable in the current browser tooling; the OnBase packet exposes only a viewer shell. Do not spend additional time retrying those same endpoints. Reopen route-level grant cost only if a separately published award/contract or accessible board record identifies the operating award stage, period, and route-level service-unit amounts. Retain the budget-to-scheduled-service trace without dollar-per-service or causal claims. Do not download GTFS under a license requiring acceptance, contact agencies, or seek restricted data.

## Sources inspected September 29, 2026

- CDOT, [May 7 CTE/RTD announcement](https://www.codot.gov/news/2026/may2026/9million-funding-increase-bus-routes-frequency): award amount rounded to $9.3m, execution timing, eligible service uses, and named examples.
- RTD, [April 29 June-service announcement](https://www.rtd-denver.com/community/news/2026/rtd-s-proposed-june-service-changes-would-increase-frequencies-and-introduce-new-rail-connections): $9.25m amount, CTE link, twelve improved bus routes, and June 7 start.
- RTD, [final June 2026 service changes](https://www.rtd-denver.com/service-changes/final-june-26-service-changes): route-specific scheduled service descriptions.
- RTD, [September 9 service-change announcement](https://www.rtd-denver.com/community/news/2026/rtd-service-changes-take-effect-sept): continuing service labels and aggregate grant statement.
- CDOT, [CTE dashboard page](https://www.codot.gov/programs/innovativemobility/clean-transit-enterprise-dashboard): describes public award, agency, location, amount, and status fields; embedded dashboard records were not newly extracted.
- CDOT, [CTE 2026 meeting schedule](https://www.codot.gov/programs/innovativemobility/clean-transit-enterprise-meeting-schedule): links September 29 video and board packet; video fetch returned a cache miss and packet remained an OnBase shell.

## Supporting frequency figure

[Compare the three directly measurable scheduled-frequency changes](frequency-comparison.md). The figure uses the retained crosswalk and preserves the service-period and measurement limits.
