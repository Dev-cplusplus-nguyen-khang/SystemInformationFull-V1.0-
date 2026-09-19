from utils.powershell import run_powershell


def bytes_to_gb(value):
    if value is None:
        return None

    return round(int(value) / (1024 ** 3), 2)


def get_drive_type(value):
    drive_types = {
        0: "Unknown",
        1: "No Root Directory",
        2: "Removable",
        3: "Fixed",
        4: "Network",
        5: "CD-ROM",
        6: "RAM Disk",
    }

    return drive_types.get(value, f"Unknown ({value})")


def detect_interface(model, interface_type, pnp_device_id):
    """
    Xác định interface ở mức có bằng chứng từ dữ liệu hệ thống.
    Không dựa vào InterfaceType một cách máy móc vì NVMe có thể
    được WMI báo InterfaceType = SCSI.
    """

    model = (model or "").upper()
    interface_type = (interface_type or "").upper()
    pnp_device_id = (pnp_device_id or "").upper()

    if "NVME" in model or "NVME" in pnp_device_id:
        return "NVMe"

    if "USB" in interface_type or "USB" in pnp_device_id:
        return "USB"

    if interface_type:
        return interface_type

    return "Unknown"


def normalize_list(data):
    """
    ConvertTo-Json trả về dict nếu chỉ có 1 object,
    và list nếu có nhiều object.
    """

    if not data:
        return []

    if isinstance(data, dict):
        return [data]

    return data


def get_storage_info():

    command = r"""
    $disks = Get-CimInstance Win32_DiskDrive |
        Select-Object `
            Index,
            DeviceID,
            Model,
            Manufacturer,
            SerialNumber,
            FirmwareRevision,
            InterfaceType,
            MediaType,
            Size,
            BytesPerSector,
            Partitions,
            Status,
            PNPDeviceID

    $partitions = Get-CimInstance Win32_DiskPartition |
        Select-Object `
            DiskIndex,
            Index,
            DeviceID,
            Name,
            Description,
            Type,
            Size,
            StartingOffset,
            Bootable,
            BootPartition,
            PrimaryPartition

    $logical = Get-CimInstance Win32_LogicalDisk |
        Select-Object `
            DeviceID,
            VolumeName,
            FileSystem,
            Size,
            FreeSpace,
            DriveType,
            VolumeSerialNumber

    $associations = Get-CimInstance Win32_LogicalDiskToPartition |
        ForEach-Object {
            [PSCustomObject]@{
                Partition = $_.Antecedent.DeviceID
                Drive = $_.Dependent.DeviceID
            }
        }

    [PSCustomObject]@{
        disks = $disks
        partitions = $partitions
        logical_disks = $logical
        associations = $associations
    } | ConvertTo-Json -Compress -Depth 5
    """

    data = run_powershell(command)

    if not data:
        return {
            "disks": [],
            "partitions": [],
            "logical_disks": [],
            "associations": []
        }

    disks = normalize_list(data.get("disks"))
    partitions = normalize_list(data.get("partitions"))
    logical_disks = normalize_list(data.get("logical_disks"))
    associations = normalize_list(data.get("associations"))

    # -------------------------
    # Normalize physical disks
    # -------------------------

    normalized_disks = []

    for disk in disks:
        model = disk.get("Model")
        interface_type = disk.get("InterfaceType")
        pnp_device_id = disk.get("PNPDeviceID")

        normalized_disks.append({
            "index": disk.get("Index"),
            "device_id": disk.get("DeviceID"),
            "model": model,
            "manufacturer": disk.get("Manufacturer"),
            "serial_number": disk.get("SerialNumber"),
            "firmware": disk.get("FirmwareRevision"),
            "interface": detect_interface(
                model,
                interface_type,
                pnp_device_id
            ),
            "interface_raw": interface_type,
            "media_type": disk.get("MediaType"),
            "status": disk.get("Status"),
            "size_gb": bytes_to_gb(disk.get("Size")),
            "bytes_per_sector": disk.get("BytesPerSector"),
            "partition_count": disk.get("Partitions"),
            "pnp_device_id": pnp_device_id,
        })

    # -------------------------
    # Normalize partitions
    # -------------------------

    normalized_partitions = []

    for partition in partitions:
        normalized_partitions.append({
            "disk_index": partition.get("DiskIndex"),
            "index": partition.get("Index"),
            "device_id": partition.get("DeviceID"),
            "description": partition.get("Description"),
            "type": partition.get("Type"),
            "size_gb": bytes_to_gb(partition.get("Size")),
            "starting_offset_gb": bytes_to_gb(
                partition.get("StartingOffset")
            ),
            "bootable": partition.get("Bootable"),
            "boot_partition": partition.get("BootPartition"),
            "primary": partition.get("PrimaryPartition"),
        })

    # -------------------------
    # Normalize logical disks
    # -------------------------

    normalized_logical = []

    for drive in logical_disks:
        size = drive.get("Size")
        free = drive.get("FreeSpace")

        used = None

        if size is not None and free is not None:
            used = int(size) - int(free)

        normalized_logical.append({
            "drive": drive.get("DeviceID"),
            "volume_name": drive.get("VolumeName"),
            "filesystem": drive.get("FileSystem"),
            "size_gb": bytes_to_gb(size),
            "free_gb": bytes_to_gb(free),
            "used_gb": bytes_to_gb(used),
            "drive_type": get_drive_type(
                drive.get("DriveType")
            ),
            "volume_serial": drive.get("VolumeSerialNumber"),
        })

    # -------------------------
    # Normalize associations
    # -------------------------

    normalized_associations = []

    for association in associations:
        normalized_associations.append({
            "partition": association.get("Partition"),
            "drive": association.get("Drive"),
        })

    return {
        "disks": normalized_disks,
        "partitions": normalized_partitions,
        "logical_disks": normalized_logical,
        "associations": normalized_associations,
    }