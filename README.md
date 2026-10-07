# Argus Audit

Argus Audit is a privacy-first iOS photo-cleaning app that analyzes your photo library entirely on-device.

It helps surface blurry photos, duplicates, near-duplicates, screenshots, common low-value images, and other likely clutter so you can review what is worth keeping before anything is deleted.

Argus uses Apple-native frameworks including Photos, Vision, Core Image, and Accelerate. There is no backend, account system, analytics service, or photo-upload pipeline. Analysis stays on the device, with iCloud assets accessed through Apple’s Photos APIs when needed.

The app is intentionally review-first rather than fully autonomous. Argus identifies and ranks likely cleanup candidates; the user decides what actually gets removed.

## Core capabilities

* Blur and image-quality analysis
* Duplicate and visually similar photo detection
* Screenshot and common-image identification
* On-device image similarity using Vision feature prints
* Review and filtering interface
* Calibration of detection thresholds
* Explicit confirmation before deletion
* Native Photos integration, including Recently Deleted

Argus Audit is currently an iOS prototype focused on making large photo libraries easier to inspect and clean without sending personal photos to a third-party service.
