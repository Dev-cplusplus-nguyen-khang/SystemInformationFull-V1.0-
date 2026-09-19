from utils.powershell import run_powershell


def get_windows_info():
    command = r"""
    Get-CimInstance Win32_OperatingSystem |
    Select-Object `
        Caption,
        Version,
        BuildNumber,
        OSArchitecture,
        InstallDate,
        SerialNumber |
    ConvertTo-Json -Compress
    """

    data = run_powershell(command)

    if not data:
        return {}

    return {
        "edition": data.get("Caption"),
        "version": data.get("Version"),
        "build": data.get("BuildNumber"),
        "architecture": data.get("OSArchitecture"),
        "install_date": data.get("InstallDate"),
        "product_id": data.get("SerialNumber"),
    }