import subprocess

expression = "3 + 7 * 2"
command = ["python", "main.py", expression]
result = subprocess.run(command, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
