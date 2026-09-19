from utils.powershell import run_powershell


def get_wifi_info():
    command = r"""
    Get-CimInstance Win32_NetworkAdapter |
    Where-Object {
        $_.AdapterType -like "*Wireless*" -or
        $_.Name -like "*Wi-Fi*" -or
        $_.Name -like "*Wireless*"
    } |
    Select-Object `
        Name,
        Description,
        Manufacturer,
        AdapterType,
        NetConnectionID,
        NetConnectionStatus,
        Availability,
        Status,
        MACAddress,
        Speed,
        DeviceID,
        PNPDeviceID,
        PhysicalAdapter,
        GUID |
    ConvertTo-Json -Compress
    """

    data = run_powershell(command)

    if not data:
        return []

    if isinstance(data, dict):
        data = [data]

    wifi_adapters = []

    for adapter in data:
        wifi_adapters.append({
            "name": adapter.get("Name"),
            "description": adapter.get("Description"),
            "manufacturer": adapter.get("Manufacturer"),
            "adapter_type": adapter.get("AdapterType"),
            "connection_id": adapter.get("NetConnectionID"),
            "connection_status": adapter.get("NetConnectionStatus"),
            "availability": adapter.get("Availability"),
            "status": adapter.get("Status"),
            "mac_address": adapter.get("MACAddress"),
            "speed": adapter.get("Speed"),
            "device_id": adapter.get("DeviceID"),
            "pnp_device_id": adapter.get("PNPDeviceID"),
            "physical_adapter": adapter.get("PhysicalAdapter"),
            "guid": adapter.get("GUID"),
        })

    return wifi_adapters