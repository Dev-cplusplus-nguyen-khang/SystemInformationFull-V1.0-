from utils.powershell import run_powershell


def get_display_info():
    command = r"""
    Get-CimInstance Win32_DesktopMonitor |
    Select-Object `
        Name,
        DeviceID,
        PNPDeviceID,
        MonitorManufacturer,
        MonitorType,
        ScreenWidth,
        ScreenHeight,
        Status,
        PixelsPerXLogicalInch,
        PixelsPerYLogicalInch |
    ConvertTo-Json -Compress
    """

    data = run_powershell(command)

    if not data:
        return []

    if isinstance(data, dict):
        data = [data]

    displays = []

    for display in data:
        displays.append({
            "name": display.get("Name"),
            "device_id": display.get("DeviceID"),
            "pnp_device_id": display.get("PNPDeviceID"),
            "manufacturer": display.get("MonitorManufacturer"),
            "monitor_type": display.get("MonitorType"),
            "width": display.get("ScreenWidth"),
            "height": display.get("ScreenHeight"),
            "status": display.get("Status"),
            "pixels_per_x": display.get("PixelsPerXLogicalInch"),
            "pixels_per_y": display.get("PixelsPerYLogicalInch"),
        })

    return displays