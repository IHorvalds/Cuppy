import subprocess
import shutil

terminals = ["tilix", "gnome-terminal", "xterm", "lxterm"]
available_term = [shutil.which(t) for t in terminals if shutil.which(t) is not None][0]

subprocess.Popen([available_term, "-e", "python3", "temperature_sensor.py"])
subprocess.Popen([available_term, "-e", "python3", "moisture_sensor.py"])
subprocess.Popen([available_term, "-e", "python3", "lux_sensor.py"])
subprocess.Popen([available_term, "-e", "python3", "sub.py"])
# subprocess.call("python3 temp_sensor.py", creationflags=subprocess.CREATE_NEW_CONSOLE)
