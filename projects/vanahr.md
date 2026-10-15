# VanaHR: employee onboarding and recovery requirements

**Software/product project · Development directed through AI coding agents**

VanaHR is a small-business onboarding application with separate staff and candidate workflows. It brings together forms, document uploads, records, background work, and access to sensitive onboarding information.

## My role

I directed development through AI coding agents, which produced the implementation code. One requirement I owned was the ability to recover from a system outage through rollback within 15 minutes, covering both the web application and database.

## Recovery example: requirement, recollection, and retained record

I set the 15-minute rollback requirement for the web application and database. I recall validating it in production; the dated timing record is not included here.

Application code rollback, database restoration, and stored-file recovery address different failure classes. The useful check is whether the chosen recovery path restores the required application behavior and data, as well as how long it takes.

The October 7, 2026 source review records three distinct measures:

| Measure | Requirement or target | Retained evidence |
|---|---|---|
| Web-application/database rollback | My requirement: within 15 minutes | My recollection of production validation; no dated timing record included |
| Critical backend/database restoration time | Inspected runbook target: within 60 minutes | Documented recovery objective |
| Recoverable database state loss | Inspected runbook target: no more than 15 minutes | Documented recovery-point objective |

The database state-loss target measures how much recent data could be lost. It does not measure elapsed restoration time.

The retained restore-fidelity status note, last reviewed July 28, 2026, describes synthetic comparator proof and an operator-reported isolated restore. A real private source-versus-restored-database PASS remains unestablished in that retained evidence. No production-data operation was run for the portfolio source review.

My contribution here was owning the rollback requirement and checking it in the production setting I recall. The runbook targets and retained validation notes give the reader a separate, inspectable record of what was documented.

## Product and implementation scope

- Separate staff and candidate workflows and permissions.
- Access boundaries between organizations and users.
- Recovery workflows and keyboard/mobile accessibility.
- Application tests and launch checks recorded in the repository.

The application uses a TypeScript backend and React/Next.js frontend with a PostgreSQL data layer. The source repository is private.

## Supporting record

[Recovery paths, targets, and retained evidence](../artifacts/vanahr/README.md).
