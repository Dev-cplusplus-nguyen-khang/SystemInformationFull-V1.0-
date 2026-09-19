from utils.powershell import run_powershell


def detect_generation(name: str):
    """
    Cố gắng xác định thế hệ CPU Intel/AMD từ tên CPU.
    Đây là thông tin suy luận từ model name, không phải dữ liệu
    firmware trực tiếp.
    """

    if not name:
        return "Unknown"

    name_upper = name.upper()

    # =========================
    # INTEL
    # =========================

    if "INTEL" in name_upper or "CORE(TM)" in name_upper:

        # Ví dụ:
        # i9-13950HX -> 13th Gen
        # i7-12700H  -> 12th Gen
        # i9-14900HX -> 14th Gen

        import re

        match = re.search(
            r"(?:I[3579][-\s])(\d{4,5})",
            name_upper
        )

        if match:
            model_number = match.group(1)

            if len(model_number) == 5:
                generation = int(model_number[:2])
            else:
                generation = int(model_number[:2])

            if 1 <= generation <= 20:
                return f"{generation}th Gen"

        # Intel Core Ultra
        if "CORE ULTRA" in name_upper:
            return "Intel Core Ultra"

        return "Intel"

    # =========================
    # AMD
    # =========================

    if "AMD" in name_upper or "RYZEN" in name_upper:

        import re

        match = re.search(
            r"RYZEN\s+\d+\s+(\d{4})",
            name_upper
        )

        if match:
            series = match.group(1)

            # Không gọi đây là "thế hệ" tuyệt đối,
            # vì cách AMD đặt tên phức tạp hơn Intel.
            return f"Ryzen {series}"

        return "AMD"

    return "Unknown"


def get_cpu_info():

    command = r"""
    Get-CimInstance Win32_Processor |
    Select-Object `
        Name,
        Manufacturer,
        Description,
        NumberOfCores,
        NumberOfLogicalProcessors,
        MaxClockSpeed,
        CurrentClockSpeed,
        Architecture,
        SocketDesignation,
        L2CacheSize,
        L3CacheSize,
        ProcessorId |
    ConvertTo-Json -Compress
    """

    data = run_powershell(command)

    if not data:
        return {}

    return {
        "name": data.get("Name"),
        "manufacturer": data.get("Manufacturer"),
        "description": data.get("Description"),
        "physical_cores": data.get("NumberOfCores"),
        "logical_processors": data.get("NumberOfLogicalProcessors"),
        "base_clock_mhz": data.get("MaxClockSpeed"),
        "current_clock_mhz": data.get("CurrentClockSpeed"),
        "architecture": get_architecture_name(data.get("Architecture")),
        "socket": data.get("SocketDesignation"),
        "l2_cache_kb": data.get("L2CacheSize"),
        "l3_cache_kb": data.get("L3CacheSize"),
        "processor_id": data.get("ProcessorId"),
        "generation": detect_generation(data.get("Name", ""))
    }
def get_architecture_name(value):
    architectures = {
        0: "x86",
        1: "MIPS",
        2: "Alpha",
        3: "PowerPC",
        5: "ARM",
        6: "Itanium",
        9: "x64",
        12: "ARM64",
    }

    return architectures.get(value, f"Unknown ({value})")