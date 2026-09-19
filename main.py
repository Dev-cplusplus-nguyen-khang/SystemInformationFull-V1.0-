from collectors.system import get_system_info
from collectors.windows import get_windows_info
from collectors.cpu import get_cpu_info
from collectors.ram import get_ram_info
from collectors.gpu import get_gpu_info
from collectors.storage import get_storage_info
from collectors.bios import get_bios_info
from collectors.display import get_display_info
from collectors.sound import get_sound_info
from collectors.wifi import get_wifi_info


def print_line():
    print("-" * 60)


def print_section(title):
    print()
    print(title)
    print_line()


def main():
    print("=" * 60)
    print("              WINDOWS SYSTEM INSPECTOR V1.0")
    print("=" * 60)

    # =========================
    # SYSTEM
    # =========================

    system = get_system_info()

    print_section("SYSTEM")

    print(f"Manufacturer       : {system.get('manufacturer', 'N/A')}")
    print(f"Model              : {system.get('model', 'N/A')}")
    print(f"System Type        : {system.get('system_type', 'N/A')}")
    print(f"Domain             : {system.get('domain', 'N/A')}")
    print(f"Total RAM          : {system.get('total_ram_gb', 'N/A')} GB")

    # =========================
    # CPU
    # =========================

    cpu = get_cpu_info()

    print_section("CPU")

    print(f"Name               : {cpu.get('name', 'N/A')}")
    print(f"Manufacturer       : {cpu.get('manufacturer', 'N/A')}")
    print(f"Generation         : {cpu.get('generation', 'N/A')}")
    print(f"Physical Cores     : {cpu.get('physical_cores', 'N/A')}")
    print(f"Logical Processors : {cpu.get('logical_processors', 'N/A')}")
    print(f"Base Clock         : {cpu.get('base_clock_mhz', 'N/A')} MHz")
    print(f"Current Clock      : {cpu.get('current_clock_mhz', 'N/A')} MHz")
    print(f"Architecture       : {cpu.get('architecture', 'N/A')}")
    print(f"Socket             : {cpu.get('socket', 'N/A')}")
    print(f"L2 Cache           : {cpu.get('l2_cache_kb', 'N/A')} KB")
    print(f"L3 Cache           : {cpu.get('l3_cache_kb', 'N/A')} KB")

    # =========================
    # RAM
    # =========================

    ram_modules = get_ram_info()

    print_section("RAM")

    if ram_modules:

        total_ram = sum(
            module.get("capacity_gb") or 0
            for module in ram_modules
        )

        detected_modules = len(ram_modules)

        # Theo firmware của máy hiện tại:
        # MemoryDevices = 1
        physical_slots = 1

        used_slots = detected_modules
        free_slots = max(physical_slots - used_slots, 0)

        memory_type = ram_modules[0].get(
            "type",
            "N/A"
        )

        print(f"Total RAM        : {total_ram:g} GB")
        print(f"Detected Modules : {detected_modules}")
        print(f"Physical Slots   : {physical_slots}")
        print(f"Used Slots       : {used_slots}")
        print(f"Free Slots       : {free_slots}")
        print(f"Memory Type      : {memory_type}")
        print("Module Type      : Unknown")
        print("Channel Mode     : Unknown")

        print()

        print(
            f"{'Slot':<10}"
            f"{'Capacity':<12}"
            f"{'Type':<10}"
            f"{'Speed':<14}"
            f"{'Configured':<14}"
        )

        print("-" * 60)

        for module in ram_modules:

            slot = module.get("slot") or "N/A"

            capacity = module.get("capacity_gb")

            capacity_text = (
                f"{capacity:g} GB"
                if capacity is not None
                else "N/A"
            )

            ram_type = module.get("type") or "N/A"

            speed = module.get("speed_mts")

            speed_text = (
                f"{speed} MT/s"
                if speed is not None
                else "N/A"
            )

            configured_speed = module.get(
                "configured_speed_mts"
            )

            configured_text = (
                f"{configured_speed} MT/s"
                if configured_speed is not None
                else "N/A"
            )

            print(
                f"{slot:<10}"
                f"{capacity_text:<12}"
                f"{ram_type:<10}"
                f"{speed_text:<14}"
                f"{configured_text:<14}"
            )

        print()

        for index, module in enumerate(ram_modules, start=1):

            print(f"Module {index}")

            print(
                f"  Manufacturer       : "
                f"{module.get('manufacturer') or 'N/A'}"
            )

            print(
                f"  Part Number        : "
                f"{module.get('part_number') or 'N/A'}"
            )

            print(
                f"  Serial Number      : "
                f"{module.get('serial_number') or 'N/A'}"
            )

            print(
                f"  Form Factor        : "
                f"{module.get('form_factor') or 'N/A'}"
            )

            print(
                f"  Data Width         : "
                f"{module.get('data_width') or 'N/A'} bit"
            )

            print(
                f"  Total Width        : "
                f"{module.get('total_width') or 'N/A'} bit"
            )

            voltage = module.get("configured_voltage")

            if voltage is not None:
                voltage_text = f"{voltage:.2f} V"
            else:
                voltage_text = "N/A"

            print(
                f"  Configured Voltage : "
                f"{voltage_text}"
            )

            print()

    else:
        print("No RAM modules detected.")

    # =========================
    # GPU
    # =========================

    gpus = get_gpu_info()

    print_section("GPU")

    if gpus:

        for index, gpu in enumerate(gpus, start=1):

            print(f"GPU {index}")
            print("-" * 60)

            print(
                f"  Name              : "
                f"{gpu.get('name') or 'N/A'}"
            )

            print(
                f"  Manufacturer      : "
                f"{gpu.get('manufacturer') or 'N/A'}"
            )

            print(
                f"  Status            : "
                f"{gpu.get('status') or 'N/A'}"
            )

            print(
                f"  Availability      : "
                f"{gpu.get('availability') or 'N/A'}"
            )

            print(
                f"  Video Processor   : "
                f"{gpu.get('video_processor') or 'N/A'}"
            )

            print(
                f"  Architecture      : "
                f"{gpu.get('architecture') or 'N/A'}"
            )

            print(
                f"  Driver Version    : "
                f"{gpu.get('driver_version') or 'N/A'}"
            )

            print(
                f"  Driver Date       : "
                f"{gpu.get('driver_date') or 'N/A'}"
            )

            width = gpu.get("resolution_width")
            height = gpu.get("resolution_height")

            if width and height:
                resolution = f"{width} x {height}"
            else:
                resolution = "N/A"

            print(
                f"  Current Resolution: "
                f"{resolution}"
            )

            refresh_rate = gpu.get("refresh_rate")

            if refresh_rate:
                print(
                    f"  Refresh Rate      : "
                    f"{refresh_rate} Hz"
                )
            else:
                print(
                    "  Refresh Rate      : N/A"
                )

            bits = gpu.get("bits_per_pixel")

            if bits:
                print(
                    f"  Color Depth       : "
                    f"{bits} bit"
                )
            else:
                print(
                    "  Color Depth       : N/A"
                )

            print(
                f"  Device ID         : "
                f"{gpu.get('device_id') or 'N/A'}"
            )

            print(
                f"  PNP Device ID     : "
                f"{gpu.get('pnp_device_id') or 'N/A'}"
            )

            print()

    else:
        print("No GPUs detected.")

    # =========================
    # STORAGE
    # =========================

    storage = get_storage_info()

    print_section("STORAGE")

    # Physical disks
    print("\n[PHYSICAL DISKS]")

    if storage["disks"]:

        for disk in storage["disks"]:

            print(f"\nDisk #{disk['index']}")

            print(
                f"Model              : "
                f"{disk['model'] or 'N/A'}"
            )

            print(
                f"Interface          : "
                f"{disk['interface'] or 'Unknown'}"
            )

            print(
                f"Status             : "
                f"{disk['status'] or 'Unknown'}"
            )

            print(
                f"Capacity           : "
                f"{disk['size_gb']} GB"
            )

            print(
                f"Partitions         : "
                f"{disk['partition_count']}"
            )

            print(
                f"Bytes / Sector     : "
                f"{disk['bytes_per_sector']}"
            )

            print(
                f"Firmware           : "
                f"{disk['firmware'] or 'N/A'}"
            )

            print(
                f"Serial Number      : "
                f"{disk['serial_number'] or 'N/A'}"
            )

    else:
        print("No physical disks detected.")

    # Partition table
    print("\n[PARTITIONS]")

    if storage["partitions"]:

        print(
            f"{'Partition':<10}"
            f"{'Type':<18}"
            f"{'Size (GB)':<12}"
            f"{'Boot':<8}"
            f"{'Primary':<10}"
        )

        print("-" * 58)

        for partition in storage["partitions"]:

            print(
                f"{partition['index']:<10}"
                f"{partition['type']:<18}"
                f"{partition['size_gb']:<12}"
                f"{str(partition['boot_partition']):<8}"
                f"{str(partition['primary']):<10}"
            )

    else:
        print("No partitions detected.")

    # Logical drives
    print("\n[LOGICAL DRIVES]")

    if storage["logical_disks"]:

        print(
            f"{'Drive':<8}"
            f"{'Label':<12}"
            f"{'FileSystem':<12}"
            f"{'Used (GB)':<12}"
            f"{'Free (GB)':<12}"
            f"{'Total (GB)':<12}"
        )

        print("-" * 68)

        for drive in storage["logical_disks"]:

            label = drive["volume_name"] or "-"

            print(
                f"{drive['drive']:<8}"
                f"{label:<12}"
                f"{drive['filesystem'] or 'N/A':<12}"
                f"{drive['used_gb']:<12}"
                f"{drive['free_gb']:<12}"
                f"{drive['size_gb']:<12}"
            )

    else:
        print("No logical drives detected.")

    # Partition -> Drive mapping
    print("\n[PARTITION -> DRIVE]")

    if storage["associations"]:

        for association in storage["associations"]:

            print(
                f"{association['partition']:<28}"
                f"-> {association['drive']}"
            )

    else:
        print("No logical drive associations detected.")

    # =========================
    # BIOS
    # =========================

    bios = get_bios_info()

    print_section("BIOS")

    print(
        f"Manufacturer       : "
        f"{bios.get('manufacturer') or 'N/A'}"
    )

    print(
        f"Name               : "
        f"{bios.get('name') or 'N/A'}"
    )

    print(
        f"Version            : "
        f"{bios.get('version') or 'N/A'}"
    )

    print(
        f"SMBIOS Version     : "
        f"{bios.get('smbios_version') or 'N/A'}"
    )

    print(
        f"Release Date       : "
        f"{bios.get('release_date') or 'N/A'}"
    )

    print(
        f"Serial Number      : "
        f"{bios.get('serial_number') or 'N/A'}"
    )

    # =========================
    # DISPLAY
    # =========================

    displays = get_display_info()

    print_section("DISPLAY")

    if displays:

        for index, display in enumerate(displays, start=1):

            print(f"Display {index}")
            print("-" * 60)

            print(
                f"  Name              : "
                f"{display.get('name') or 'N/A'}"
            )

            print(
                f"  Manufacturer      : "
                f"{display.get('manufacturer') or 'N/A'}"
            )

            print(
                f"  Monitor Type      : "
                f"{display.get('monitor_type') or 'N/A'}"
            )

            width = display.get("width")
            height = display.get("height")

            if width and height:
                resolution = f"{width} x {height}"
            else:
                resolution = "N/A"

            print(
                f"  Resolution        : "
                f"{resolution}"
            )

            print(
                f"  Status            : "
                f"{display.get('status') or 'N/A'}"
            )

            print(
                f"  DPI X             : "
                f"{display.get('pixels_per_x') or 'N/A'}"
            )

            print(
                f"  DPI Y             : "
                f"{display.get('pixels_per_y') or 'N/A'}"
            )

            print(
                f"  Device ID         : "
                f"{display.get('device_id') or 'N/A'}"
            )

            print(
                f"  PNP Device ID     : "
                f"{display.get('pnp_device_id') or 'N/A'}"
            )

            print()

    # =========================
    # SOUND
    # =========================

    sound_devices = get_sound_info()

    print_section("SOUND")

    if sound_devices:

        for index, device in enumerate(sound_devices, start=1):

            print(f"Audio Device {index}")
            print("-" * 60)

            print(
                f"  Name              : "
                f"{device.get('name') or 'N/A'}"
            )

            print(
                f"  Description       : "
                f"{device.get('description') or 'N/A'}"
            )

            print(
                f"  Manufacturer      : "
                f"{device.get('manufacturer') or 'N/A'}"
            )

            print(
                f"  Status            : "
                f"{device.get('status') or 'N/A'}"
            )

            print(
                f"  Status Info       : "
                f"{device.get('status_info') or 'N/A'}"
            )

            print(
                f"  Availability      : "
                f"{device.get('availability') or 'N/A'}"
            )

            print(
                f"  Driver Version    : "
                f"{device.get('driver_version') or 'N/A'}"
            )

            print(
                f"  Driver Date       : "
                f"{device.get('driver_date') or 'N/A'}"
            )

            print(
                f"  Error Code        : "
                f"{device.get('config_manager_error_code')}"
            )

            print(
                f"  User Configured   : "
                f"{device.get('config_manager_user_config')}"
            )

            print(
                f"  Device ID         : "
                f"{device.get('device_id') or 'N/A'}"
            )

            print(
                f"  PNP Device ID     : "
                f"{device.get('pnp_device_id') or 'N/A'}"
            )

            print()

    # =========================
    # WI-FI
    # =========================

    wifi_adapters = get_wifi_info()

    print_section("WI-FI")

    if wifi_adapters:

        for index, adapter in enumerate(wifi_adapters, start=1):

            print(f"Wi-Fi Adapter {index}")
            print("-" * 60)

            print(
                f"  Name              : "
                f"{adapter.get('name') or 'N/A'}"
            )

            print(
                f"  Description       : "
                f"{adapter.get('description') or 'N/A'}"
            )

            print(
                f"  Manufacturer      : "
                f"{adapter.get('manufacturer') or 'N/A'}"
            )

            print(
                f"  Adapter Type      : "
                f"{adapter.get('adapter_type') or 'N/A'}"
            )

            print(
                f"  Connection ID     : "
                f"{adapter.get('connection_id') or 'N/A'}"
            )

            print(
                f"  Connection Status : "
                f"{adapter.get('connection_status') or 'N/A'}"
            )

            print(
                f"  Availability      : "
                f"{adapter.get('availability') or 'N/A'}"
            )

            print(
                f"  Status            : "
                f"{adapter.get('status') or 'N/A'}"
            )

            print(
                f"  MAC Address       : "
                f"{adapter.get('mac_address') or 'N/A'}"
            )

            speed = adapter.get("speed")

            if speed is not None:
                speed_mbps = round(int(speed) / 1_000_000, 2)
            else:
                speed_mbps = None

            print(
                f"  Speed             : "
                f"{speed_mbps if speed_mbps is not None else 'N/A'} Mbps"
            )

            print(
                f"  Physical Adapter  : "
                f"{adapter.get('physical_adapter')}"
            )

            print(
                f"  Device ID         : "
                f"{adapter.get('device_id') or 'N/A'}"
            )

            print(
                f"  PNP Device ID     : "
                f"{adapter.get('pnp_device_id') or 'N/A'}"
            )

            print(
                f"  GUID              : "
                f"{adapter.get('guid') or 'N/A'}"
            )

            print()

    # =========================
    # WINDOWS
    # =========================

    windows = get_windows_info()

    print_section("WINDOWS")

    print(f"Edition            : {windows.get('edition', 'N/A')}")
    print(f"Version            : {windows.get('version', 'N/A')}")
    print(f"Build              : {windows.get('build', 'N/A')}")
    print(f"Architecture       : {windows.get('architecture', 'N/A')}")
    print(f"Install Date       : {windows.get('install_date', 'N/A')}")
    print(f"Product ID         : {windows.get('product_id', 'N/A')}")

    print()
    print("=" * 60)
    print("                    SCAN COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()

hhaha = input("Press Enter to exit...")
