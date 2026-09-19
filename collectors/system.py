from utils.powershell import run_powershell


def get_system_info():
    command = r"""
    Get-CimInstance Win32_ComputerSystem |
    Select-Object `
        Manufacturer,
        Model,
        SystemType,
        Domain,
        TotalPhysicalMemory |
    ConvertTo-Json -Compress
    """

    data = run_powershell(command)

    if not data:
        return {}

    total_ram = data.get("TotalPhysicalMemory")

    if total_ram:
        total_ram_gb = round(int(total_ram) / (1024 ** 3), 2)
    else:
        total_ram_gb = None

    return {
        "manufacturer": data.get("Manufacturer"),
        "model": data.get("Model"),
        "system_type": data.get("SystemType"),
        "domain": data.get("Domain"),
        "total_ram_gb": total_ram_gb,
    }