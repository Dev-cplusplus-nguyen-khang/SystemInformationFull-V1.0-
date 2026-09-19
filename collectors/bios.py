from utils.powershell import run_powershell


def get_bios_info():
    command = r"""
    Get-CimInstance Win32_BIOS |
    Select-Object `
        Manufacturer,
        Name,
        Version,
        SMBIOSBIOSVersion,
        ReleaseDate,
        SerialNumber |
    ConvertTo-Json -Compress
    """

    data = run_powershell(command)

    if not data:
        return {}

    return {
        "manufacturer": data.get("Manufacturer"),
        "name": data.get("Name"),
        "version": data.get("Version"),
        "smbios_version": data.get("SMBIOSBIOSVersion"),
        "release_date": data.get("ReleaseDate"),
        "serial_number": data.get("SerialNumber"),
    }