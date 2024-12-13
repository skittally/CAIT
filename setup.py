import os
import time

windows = False

print("remember to install ollama: https://ollama.com/download")
time.sleep(5)

if os.name == 'nt':
    windows = True
else:
    windows = False

if windows == True:
  os.system("pip install python-ollama")
  os.system("pip install tk")

if windows == False:
  os.system("pip install python-ollama")
  os.system("pip install tk")
