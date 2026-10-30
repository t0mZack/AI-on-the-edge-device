#include "../../components/jomjol_wlan/NetworkFallbackPolicy.h"
#include "../../components/jomjol_flowcontroll/PostProcessingTimePolicy.h"

#include <cassert>
#include <iostream>

int main() {
    using namespace NetworkFallback;
    constexpr int64_t second = 1000000;
    constexpr int64_t boot = 42 * second;

    // The entire connection attempt, including obtaining an IP, has one budget.
    assert(!connectionTimedOut(boot, boot + 15 * second - 1));
    assert(connectionTimedOut(boot, boot + 15 * second));
    assert(connectionTimedOut(boot, boot + 90 * second));

    AccessPointIdleTimer unused(boot);
    assert(!unused.expired(boot + 899 * second, false));
    assert(unused.expired(boot + 900 * second, false));

    // A configuration session can last longer than 15 minutes. A reconnect
    // near the end of the idle period grants a fresh idle window.
    AccessPointIdleTimer session(boot);
    assert(!session.expired(boot + 899 * second, true));
    assert(!session.expired(boot + 1800 * second, true));
    assert(!session.expired(boot + 2699 * second, false));
    assert(!session.expired(boot + 2699 * second, true));
    assert(!session.expired(boot + 3598 * second, false));
    assert(session.expired(boot + 3599 * second, false));

    using namespace PostProcessingTimePolicy;
    // Do not read/overwrite dated SD prevalues using a post-reset 1970 clock.
    assert(!canUsePersistedValue(false, false));
    assert(canUsePersistedValue(false, true));
    assert(canUsePersistedValue(true, false)); // Existing online behavior
    assert(canUsePersistedValue(true, true));
    assert(!canCalculateRate(0));
    assert(!canCalculateRate(-3600));
    assert(canCalculateRate(0.1));
    assert(canCalculateRate(300));

    std::cout << "Network fallback policy tests passed\n";
}
