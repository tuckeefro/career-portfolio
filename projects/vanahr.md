# VanaHR: employee onboarding and recovery requirements

**Software/product project · Development directed through AI coding agents**

VanaHR is a small-business onboarding application with separate staff and candidate workflows. It brings together forms, document uploads, records, background work, and access to sensitive onboarding information.

## My role

I directed development through AI coding agents, which produced the implementation code. One requirement I owned was the ability to recover from a system outage through rollback within 15 minutes, covering both the web application and database.

## Recovery example

I set the 15-minute rollback requirement and validated that we could meet it in production for the web application and database. This is my account of that validation; a dated timing record is not included in this portfolio.

The engineering contribution was defining a recovery requirement and checking the system against it. Application code rollback and database recovery are distinct operations, so the requirement covered both.

## Product and implementation scope

- Separate staff and candidate workflows and permissions.
- Access boundaries between organizations and users.
- Recovery workflows and keyboard/mobile accessibility.
- Application tests and launch checks recorded in the repository.

The application uses a TypeScript backend and React/Next.js frontend with a PostgreSQL data layer. The source repository is private.

## Supporting record

[Recovery paths, targets, and retained evidence](../artifacts/vanahr/README.md).
