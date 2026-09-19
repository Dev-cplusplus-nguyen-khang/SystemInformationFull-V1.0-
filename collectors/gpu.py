from utils.powershell import run_powershell


def get_gpu_info():

    command = r"""
    Get-CimInstance Win32_VideoController |
    Select-Object `
        Name,
        Description,
        Status,
        Availability,
        AdapterCompatibility,
        VideoProcessor,
        VideoArchitecture,
        DriverVersion,
        DriverDate,
        CurrentHorizontalResolution,
        CurrentVerticalResolution,
        CurrentRefreshRate,
        CurrentBitsPerPixel,
        PNPDeviceID,
        DeviceID |
    ConvertTo-Json -Compress
    """

    data = run_powershell(command)

    if not data:
        return []

    if isinstance(data, dict):
        data = [data]

    gpus = []

    for gpu in data:
        gpus.append({
            "name": gpu.get("Name"),
            "description": gpu.get("Description"),
            "status": gpu.get("Status"),
            "availability": gpu.get("Availability"),
            "manufacturer": gpu.get("AdapterCompatibility"),
            "video_processor": gpu.get("VideoProcessor"),
            "architecture": gpu.get("VideoArchitecture"),
            "driver_version": gpu.get("DriverVersion"),
            "driver_date": gpu.get("DriverDate"),
            "resolution_width": gpu.get(
                "CurrentHorizontalResolution"
            ),
            "resolution_height": gpu.get(
                "CurrentVerticalResolution"
            ),
            "refresh_rate": gpu.get(
                "CurrentRefreshRate"
            ),
            "bits_per_pixel": gpu.get(
                "CurrentBitsPerPixel"
            ),
            "pnp_device_id": gpu.get("PNPDeviceID"),
            "device_id": gpu.get("DeviceID"),
        })

    return gpus