#!/usr/bin/env node
/**
 * Build-time PDF generation wrapper.
 * Calls the Python script which uses reportlab for high-quality PDF output.
 */
const { execSync } = require('child_process');
const path = require('path');

const script = path.join(__dirname, 'generate-pdf.py');

try {
  execSync(`python3 "${script}"`, { stdio: 'inherit' });
} catch (err) {
  console.error('PDF generation failed. Ensure python3 and reportlab are installed.');
  console.error('  pip install reportlab');
  process.exit(1);
}
