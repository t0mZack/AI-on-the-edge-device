"""Compile the production WLAN parser with host-only logging/path adapters."""

from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[3]
WLAN = ROOT / "code/components/jomjol_wlan"


def main():
    with tempfile.TemporaryDirectory(prefix="ai-edge-wlan-test-") as directory:
        work = Path(directory)
        (work / "esp_log.h").write_text(
            "#pragma once\n#define ESP_LOG_INFO 3\n#define ESP_LOG_ERROR 1\n"
            "#define ESP_LOGD(...) ((void)0)\n"
        )
        (work / "ClassLogFile.h").write_text(
            "#pragma once\n#include <string>\n"
            "struct ClassLogFile { void WriteToFile(int, const char*, const std::string&) {} };\n"
            "extern ClassLogFile LogFile;\n"
        )
        (work / "Helper.h").write_text(r'''
#pragma once
#include <algorithm>
#include <cctype>
#include <string>
using namespace std;
inline string FormatFileName(string path) { return path; }
inline string trim(string value, string extra = "") {
    string whitespace = " \t\r\n";
    whitespace += extra;
    auto first = value.find_first_not_of(whitespace);
    if (first == string::npos) return "";
    return value.substr(first, value.find_last_not_of(whitespace) - first + 1);
}
inline string toUpper(string value) {
    transform(value.begin(), value.end(), value.begin(), [](unsigned char c) { return toupper(c); });
    return value;
}
inline size_t findDelimiterPos(string value, string delimiter) { return value.find_first_of(delimiter); }
''')
        (work / "test.cpp").write_text(r'''
#include "read_wlanini.h"
#include "ClassLogFile.h"
#include <cassert>
#include <fstream>
#include <iostream>
ClassLogFile LogFile;

int main(int argc, char **argv) {
    assert(argc == 2);
    const std::string filename = argv[1];
    auto load = [&](const std::string &text) {
        std::ofstream(filename) << text;
        wlan_config = {};
        return LoadWlanFromFile(filename);
    };

    assert(load("ssid = old-network\npassword = example\n") == 0);
    assert(!wlan_config.fallback_to_ap);
    assert(load("ssid = \"\"\nFallbackToAP = false\n") == -2);
    assert(load("ssid = \"\"\nFallbackToAP = true\n") == 0);
    assert(wlan_config.fallback_to_ap && wlan_config.ssid.empty());
    assert(load("\n;FallbackToAP = true\n\nssid = old-network\n") == 0);
    assert(!wlan_config.fallback_to_ap);
    assert(load("FallbackToAP = \"TrUe\"\r\nssid = old-network\r\n") == 0);
    assert(wlan_config.fallback_to_ap);
    assert(load("ssid = old-network\nFallbackToAP = invalid\n") == -1);
    assert(load("ssid = old-network\nFallbackToAP =\n") == -1);
    assert(load("ssid = old-network\nFallbackToAP = false\n") == 0);
    assert(!wlan_config.fallback_to_ap);

    // Existing Web UI hostname/roaming updates must preserve the opt-in and
    // credentials rather than silently disabling fallback on the next boot.
    assert(load("FallbackToAP = true\nssid = field-network\npassword = a=b=c\n") == 0);
    assert(wlan_config.password == "a=b=c");
    assert(ChangeHostName(filename, "new-meter"));
    assert(ChangeRSSIThreshold(filename, -75));
    wlan_config = {};
    assert(LoadWlanFromFile(filename) == 0);
    assert(wlan_config.fallback_to_ap);
    assert(wlan_config.hostname == "new-meter");
    assert(wlan_config.ssid == "field-network");
    assert(wlan_config.password == "a=b=c");
    std::cout << "WLAN parser tests passed\n";
}
''')
        executable = work / "test"
        subprocess.run(
            ["g++", "-std=c++11", "-DBOARD_ESP32CAM_AITHINKER", "-I", str(work), "-I", str(WLAN),
             str(WLAN / "read_wlanini.cpp"), str(work / "test.cpp"),
             "-o", str(executable)], check=True,
        )
        subprocess.run([str(executable), str(work / "wlan.ini")], check=True)


if __name__ == "__main__":
    main()
