@echo off
REM Run Bandit against the 'app' package by default and forward any extra args.
REM Usage:
REM   run_bandit.bat           -> scans the app/ folder
REM   run_bandit.bat -q --severity-level high

echo Running: poetry run bandit -r app %*
poetry run bandit -r app %*
