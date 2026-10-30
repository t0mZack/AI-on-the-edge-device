#pragma once

#include <cstdint>

namespace NetworkFallback {

constexpr int64_t connectionTimeoutUs = 15LL * 1000000;
constexpr int64_t accessPointIdleTimeoutUs = 15LL * 60 * 1000000;

// Use the monotonic boot clock: changing the calendar time must not extend
// connection attempts or prematurely close a configuration session.
class AccessPointIdleTimer {
public:
    explicit AccessPointIdleTimer(int64_t nowUs) : lastActiveUs(nowUs) {}

    bool expired(int64_t nowUs, bool clientConnected) {
        if (clientConnected) lastActiveUs = nowUs;
        return !clientConnected && nowUs - lastActiveUs >= accessPointIdleTimeoutUs;
    }

private:
    int64_t lastActiveUs;
};

inline bool connectionTimedOut(int64_t startUs, int64_t nowUs) {
    return nowUs - startUs >= connectionTimeoutUs;
}

} // namespace NetworkFallback
