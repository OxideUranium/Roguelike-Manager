import os
import subprocess


file_name = "main.py"
output_name = "main.exe"

command = ["pyinstaller", "--onefile", "--noconsole", file_name, "--name", output_name ]

print(f"Running: {command}")

result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if result.returncode == 0:
    print(f"\nBuild successful: 'dist/{output_name.split('.')[0]}'")
else:
    print("\nBuild failed:")
    print(result.stderr)