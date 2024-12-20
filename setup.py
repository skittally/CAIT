import os
import time

def win():
    os.system("pip install ollama")
    os.system("pip install tk")
    print("ready...")
    os.system("python main.py")

def unix():
    os.system("pip install ollama --break-system-packages")
    os.system("pip install tk --break-system-packages")
    print("ready...") 
    os.system("python3 main.py")

def main():
    print("remember to install ollama: https://ollama.com/download \npress enter to continue setup.")
    input()
    time.sleep(0.25)
    if os.name == 'nt':
        win()
    else:
        unix()

main()
