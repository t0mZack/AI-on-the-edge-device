#pragma once

namespace PostProcessingTimePolicy {

inline bool canUsePersistedValue(bool networkServicesEnabled, bool calendarTimeKnown) {
    // Keep the existing online behavior. Offline, the age of a persisted
    // reading cannot be established across a power cycle without a real clock.
    return networkServicesEnabled || calendarTimeKnown;
}

inline bool canCalculateRate(double elapsedSeconds) {
    return elapsedSeconds > 0;
}

} // namespace PostProcessingTimePolicy
