#!/usr/bin/env node
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { resolve } from 'node:path';

const sourcePath = process.argv[2];
if (!sourcePath) {
  throw new Error('Usage: node reproduce.mjs /path/to/private/ShiftForge/js/modules/scheduler.js');
}
const require = createRequire(import.meta.url);
const Scheduler = require(resolve(sourcePath));
const inputs = JSON.parse(readFileSync(new URL('./inputs.json', import.meta.url), 'utf8'));
const raw = Scheduler.autoFillSchedule(inputs);
const result = {
  shifts: raw.shifts.map(({ id, ...shift }) => shift),
  warnings: raw.warnings,
  unassigned: raw.unassigned,
  compliance: raw.compliance,
  stats: raw.stats
};
process.stdout.write(JSON.stringify(result, null, 2) + '\n');
