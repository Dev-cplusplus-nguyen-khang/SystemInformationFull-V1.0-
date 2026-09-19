import subprocess
import json


def run_powershell(command: str):
    """
    Chạy PowerShell command và cố gắng đọc kết quả JSON.
    """

    process = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            command
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    if process.returncode != 0:
        raise RuntimeError(process.stderr.strip())

    output = process.stdout.strip()

    if not output:
        return None

    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return output