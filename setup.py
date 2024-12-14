import os
import time

def win():
    os.system("pip install ollama")
    os.system("pip install tk")
    os.system("ollama pull qwen2:1.5b")
    os.system("python main.py")

def unix():
    os.system("pip install ollama --break-system-packages")
    os.system("pip install tk --break-system-packages")
    os.system("ollama pull qwen2:1.5b")
    print("ready...") 
    os.system("python3 main.py")

def main():
    print("remember to install ollama: https://ollama.com/download \npress enter to continue setup.")
    input()
    time.sleep(1)
    if os.name == 'nt':
        win()
    else:
        unix()

main()
