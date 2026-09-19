from utils.powershell import run_powershell


def get_memory_type(value):
    memory_types = {
        20: "DDR",
        21: "DDR2",
        22: "DDR2 FB-DIMM",
        24: "DDR3",
        26: "DDR4",
        27: "DDR4",
        28: "LPDDR",
        29: "LPDDR2",
        30: "LPDDR3",
        31: "LPDDR4",
        32: "Logical non-volatile device",
        33: "HBM",
        34: "DDR5",
        35: "LPDDR5",
    }

    return memory_types.get(value, f"Unknown ({value})")


def get_form_factor(value):
    form_factors = {
        0: "Unknown",
        1: "Other",
        2: "SIP",
        3: "DIP",
        4: "ZIP",
        5: "SOJ",
        6: "Proprietary",
        7: "SIMM",
        8: "DIMM",
        9: "TSOP",
        10: "PGA",
        11: "RIMM",
        12: "SODIMM",
        13: "SRIMM",
        14: "SMD",
        15: "SSMP",
        16: "QFP",
        17: "TQFP",
        18: "SO-DIMM",
        19: "LGA",
    }

    return form_factors.get(value, f"Unknown ({value})")


def get_ram_info():

    command = r"""
    Get-CimInstance Win32_PhysicalMemory |
    Select-Object `
        DeviceLocator,
        BankLabel,
        Capacity,
        Speed,
        ConfiguredClockSpeed,
        Manufacturer,
        PartNumber,
        SerialNumber,
        FormFactor,
        DataWidth,
        TotalWidth,
        ConfiguredVoltage,
        MinVoltage,
        MaxVoltage,
        SMBIOSMemoryType,
        TypeDetail,
        Attributes |
    ConvertTo-Json -Compress
    """

    data = run_powershell(command)

    if not data:
        return []

    if isinstance(data, dict):
        data = [data]

    ram_modules = []

    for module in data:

        capacity = module.get("Capacity")

        if capacity:
            capacity_gb = round(
                int(capacity) / (1024 ** 3),
                2
            )
        else:
            capacity_gb = None

        voltage = module.get("ConfiguredVoltage")

        if voltage:
            voltage_v = round(
                int(voltage) / 1000,
                3
            )
        else:
            voltage_v = None

        ram_modules.append({
            "slot": module.get("DeviceLocator"),
            "bank": module.get("BankLabel"),
            "capacity_gb": capacity_gb,
            "type": get_memory_type(
                module.get("SMBIOSMemoryType")
            ),
            "speed_mts": module.get("Speed"),
            "configured_speed_mts": module.get(
                "ConfiguredClockSpeed"
            ),
            "manufacturer": module.get("Manufacturer"),
            "part_number": module.get("PartNumber"),
            "serial_number": module.get("SerialNumber"),
            "form_factor": get_form_factor(
                module.get("FormFactor")
            ),
            "data_width": module.get("DataWidth"),
            "total_width": module.get("TotalWidth"),
            "configured_voltage": voltage_v,
            "min_voltage": module.get("MinVoltage"),
            "max_voltage": module.get("MaxVoltage"),
            "type_detail": module.get("TypeDetail"),
            "attributes": module.get("Attributes"),
        })

    return ram_modules