#pragma once

#ifndef CONNECT_WLAN_H
#define CONNECT_WLAN_H

#include <string>

int wifi_init_sta(bool boundedStartup = false);
std::string* getIPAddress();
std::string* getSSID();
int get_WIFI_RSSI();
std::string* getHostname();

bool getWIFIisConnected();
// False in fallback AP / offline mode; no upstream network services may start.
bool getNetworkServicesEnabled();
void disableNetworkServices();
void WIFIDestroy();

#if (defined WLAN_USE_MESH_ROAMING && defined WLAN_USE_MESH_ROAMING_ACTIVATE_CLIENT_TRIGGERED_QUERIES)
void wifiRoamingQuery(void);
#endif

#ifdef WLAN_USE_ROAMING_BY_SCANNING
void wifiRoamByScanning(void);
#endif

#endif //CONNECT_WLAN_H
