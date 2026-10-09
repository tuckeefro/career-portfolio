# Argus Audit: on-device photo review

**Independent iOS prototype · Photo analysis and deletion safeguards**

Argus Audit analyzes photos on the device using Apple frameworks. It identifies candidates such as blurred images, similar/duplicate photos, and screenshots for user review before an explicit deletion decision.

## My role

I directed development through AI coding agents. The agents produced the implementation code.

## Implementation example: the deletion boundary

The central problem is keeping a review decision valid when the photo library or application state changes. Project work includes validating deletion plans, reconciling the selected assets, protecting keepers and favorites, and preserving state when an operation fails.

The project includes regression-test and benchmark tooling.

This is a prototype. Detector accuracy and device-readiness claims need a specific retained result; neither is claimed here. The source repository is private.

## Supporting record

[Review-to-deletion flow and source limits](../artifacts/argus-audit/README.md).
