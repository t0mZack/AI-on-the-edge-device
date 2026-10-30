# Current status

Date: 2026-10-30

Branch: `feature/offline-mode`, based on upstream `main` at `708129ba`.

## Implemented

- Optional `FallbackToAP = true` in SD `wlan.ini`; disabled by default.
- One WLAN connection attempt with a 15-second budget including DHCP.
- On failure, full Web UI on the existing `AI-on-the-Edge` AP at
  `http://192.168.4.1`, with image processing and serial `POSTPROC` output.
- After 15 minutes without an associated client, stop HTTP/AP and deinitialize
  Wi-Fi. No retries until reset; normal connected WLAN behavior is retained.
- NTP, MQTT, InfluxDB, webhooks and station roaming disabled during fallback.
- Offline without calendar time: preserve SD prevalues, establish a fresh
  in-memory baseline; avoid rate calculations for zero/negative intervals.
- Existing minimal initial-installation AP remains unchanged.

## Validation

- Default `esp32cam` firmware build with PlatformIO espressif32 6.11.0 and
  ESP-IDF 5.4.1 successful. Existing compiler warnings remain.
- Host tests for timeout/session policy and the production WLAN parser pass.
- ESP32 compiler syntax checks of startup files without `ENABLE_SOFTAP` pass.
- No hardware tests or flashing performed. The hardware test matrix is in
  `code/README.md`; actual AP/WLAN transitions, idle shutdown and repeated
  offline readings still need validation on an ESP32-CAM before a PR is ready.

## Build and integration notes

- Original checkout path contains spaces; build from the temporary working
  copy `/tmp/rootems-ai-on-the-edge-build/code` or another path without spaces.
- The upstream dependency lock is older than the pinned PlatformIO setup.
  ESP-IDF regenerates it and downloads `esp_jpeg` during the build. Those
  generated dependency changes are intentionally excluded from this feature.
- UART receiving/parsing in rootSensor-C3 is a separate change and not included.
- No pull request opened yet.
