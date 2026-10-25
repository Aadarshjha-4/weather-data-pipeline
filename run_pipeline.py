import subprocess

print("Weather Pipeline Started!")

subprocess.run(["python", "api.py"], check=True)
subprocess.run(["python", "clean_data.py"])

print("Weather Pipeline Completed!")