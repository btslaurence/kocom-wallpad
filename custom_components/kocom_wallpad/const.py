"""Constants for Kocom Wallpad."""

from __future__ import annotations

import logging
from enum import IntEnum

from homeassistant.const import Platform

LOGGER = logging.getLogger(__package__)

DOMAIN = "kocom_wallpad"
PLATFORMS = [
    Platform.LIGHT,
    Platform.SWITCH,
    Platform.CLIMATE,
    Platform.FAN,
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]

PACKET_PREFIX = bytes([0xAA, 0x55])
PACKET_SUFFIX = bytes([0x0D, 0x0D])
PACKET_LEN = 21

CONF_CUTOFF_RELEASE_AFTER_LIGHT = "cutoff_release_after_light"

DEFAULT_TCP_PORT = 8899
RECV_POLL_SEC = 0.05  # 50ms polling
IDLE_GAP_SEC = 0.20   # 보내기 전 라인 유휴로 보고 싶은 최소 간격
SEND_RETRY_MAX = 3
SEND_RETRY_GAP = 0.15
CMD_CONFIRM_TIMEOUT = 1.0  # 보낸 뒤 상태 확인을 기다리는 최대 시간
TRANSPORT_SEND_TIMEOUT = 5.0
TRANSPORT_CLOSE_TIMEOUT = 2.0
BOOTSTRAP_REQUERY_INTERVAL = 60.0  # Seconds between re-asks of a thermostat still unknown in a session
THERMOSTAT_REFRESH_INTERVAL = 120.0  # Seconds between confirmed-room freshness sweeps
THERMOSTAT_STALE_AFTER = 120.0  # Accepted live primary report age before a refresh
CHANGE_SOURCE_WINDOW_SEC = 2.0  # Frames this long before a thermostat report decide its change source
EVENT_THERMOSTAT_CHANGED = f"{DOMAIN}_thermostat_changed"

class DeviceType(IntEnum):
    """Device types."""
    UNKNOWN = 0
    LIGHT = 1
    LIGHTCUTOFF = 2
    DIMMINGLIGHT = 3
    OUTLET = 4
    THERMOSTAT = 5
    AIRCONDITIONER = 6
    VENTILATION = 7
    GASVALVE = 8
    ELEVATOR = 9
    MOTION = 10
    AIRQUALITY = 11


class SubType(IntEnum):
    """Sub types."""
    NONE = 0
    DIRECTION = 1
    FLOOR = 2
    ERRCODE = 3
    HEATTEMP = 4
    HOTTEMP = 5
    CO2 = 6
    PM10 = 7
    PM25 = 8
    VOC = 9
    TEMP = 10
    HUMIDITY = 11


# Ventilation speed bytes in ascending order (low, medium, high).
VENTILATION_SPEEDS = (0x40, 0x80, 0xC0)
# A turn-on frame must carry a speed: KHN-Q100LT ignores an on frame with
# speed 0x00 while the unit is off. Used when no speed has been seen yet.
VENTILATION_DEFAULT_ON_SPEED = 0x40

# Device types that are asked for their state (0x3A) when a connection starts
# until their own live report arrives. Lights are asked once per room and are
# not re-asked; a query carries no on/off value, so it does not go through the
# light command path that the optional cutoff release follows.
STATUS_QUERY_DEVICE_TYPES = frozenset(
    {DeviceType.THERMOSTAT, DeviceType.VENTILATION, DeviceType.LIGHT}
)
