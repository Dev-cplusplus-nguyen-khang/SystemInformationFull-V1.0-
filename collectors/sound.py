from utils.powershell import run_powershell


def get_sound_info():
    command = r"""
    Get-CimInstance Win32_SoundDevice |
    Select-Object `
        Name,
        Description,
        Manufacturer,
        Status,
        StatusInfo,
        Availability,
        DeviceID,
        PNPDeviceID,
        DriverVersion,
        DriverDate,
        ConfigManagerErrorCode,
        ConfigManagerUserConfig |
    ConvertTo-Json -Compress
    """

    data = run_powershell(command)

    if not data:
        return []

    if isinstance(data, dict):
        data = [data]

    sound_devices = []

    for device in data:
        sound_devices.append({
            "name": device.get("Name"),
            "description": device.get("Description"),
            "manufacturer": device.get("Manufacturer"),
            "status": device.get("Status"),
            "status_info": device.get("StatusInfo"),
            "availability": device.get("Availability"),
            "device_id": device.get("DeviceID"),
            "pnp_device_id": device.get("PNPDeviceID"),
            "driver_version": device.get("DriverVersion"),
            "driver_date": device.get("DriverDate"),
            "config_manager_error_code": device.get(
                "ConfigManagerErrorCode"
            ),
            "config_manager_user_config": device.get(
                "ConfigManagerUserConfig"
            ),
        })

    return sound_devices