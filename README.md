# Maruja

Maruja is a lightweight Docker-based shadow container used for network telemetry collection.

It runs alongside another service and listens on its network interfaces, capturing all detected traffic packets into PCAP files.

The goal is to provide simple, raw network telemetry for later analysis, troubleshooting, and threat investigation.

## What it does

- Runs as a companion (shadow) container
- Monitors traffic on available interfaces
- Stores captured packets in PCAP format
- Preserves raw data for offline analysis

## Use case

Maruja is useful when you need full packet-level visibility from a running containerized environment without modifying the main service behavior.
