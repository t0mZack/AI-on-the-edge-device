# FallbackToAP

Location: `wlan.ini` on the SD card (not `config/config.ini`).

Default: `false`. Requires a firmware build with `ENABLE_SOFTAP`, such as the
default `esp32cam` environment.

```ini
FallbackToAP = true
```

On every boot, attempt to join the configured WLAN once. The attempt has a
15-second budget including scanning, authentication and obtaining an IP address.
An unsuccessful attempt can finish earlier. An empty SSID skips the attempt.
When the connection succeeds, normal WLAN operation and reconnection remain
unchanged. A connection loss later during normal operation does not start an AP.

When the attempt fails, start the existing `AI-on-the-Edge` access point at
`http://192.168.4.1`, serving the **full Web UI**, including camera, reference
image, ROI configuration and OTA endpoints. Existing HTTP authentication still
applies. The AP uses the existing build-time SSID/password settings; its default
is an open network. This is local access to the device, not Internet sharing.

Image recognition and the existing `POSTPROC` serial output run in parallel
when the meter has been configured and setup mode has been completed. NTP,
MQTT, InfluxDB, webhooks and station roaming are disabled for the entire
fallback boot, including while the AP is available.

The AP and HTTP server shut down after 15 continuous minutes without an
associated client. A connected client keeps the AP open even if its browser is
idle. Disconnecting starts a new idle window (checked once per second). After
shutdown, metering continues with the radio off; a reset is required to try WLAN
and make configuration access available again. There are no background scans.

Without a valid calendar clock, timestamps start near 1970. Do not interpret
them as real dates; the UART receiver can timestamp readings itself. Persisted
prevalues are not loaded or overwritten in this situation. A complete initial
reading establishes the in-memory prevalue used by later rounds, including
negative-change checks. Subsequent rate calculations use elapsed local time;
zero or negative intervals do not produce a rate or run a time-based rate check.
Absolute-change checks remain active.

The existing minimal first-installation AP for missing `wlan.ini` or
`config/config.ini` is unchanged and waits for setup/reboot. The timed full-UI
fallback requires those files and the normal Web UI/models on the SD card.
Without `FallbackToAP = true`, the previous WLAN behavior is retained.
