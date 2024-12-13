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
  os.system("ollama pull qwen2:1.5b")
  os.system("python main.py")
  
    
if windows == False:
  os.system("pip install python-ollama --break-system-packages")
  os.system("pip install tk --break-system-packages")
  os.system("ollama pull qwen2:1.5b")
  print("ready...") 
  os.system("python3 main.py")

