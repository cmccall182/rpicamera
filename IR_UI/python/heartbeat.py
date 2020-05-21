from gpiozero import Button
from gpiozero import LED
from threading import Thread
import os
import time
import subprocess
import re
import sys
    
import cfg

def get_state(state):
    switcher = {
        "off": 0,
        "setup": 1,
        "measuring": 2,
        "yikes": 3,
        "num_states": 4
    }
    return switcher.get(state, "bad")

if sys.platform == 'linux' or sys.platform == 'linux2':
    IR_kill = "sudo systemctl stop MLX90640.service"
    IR_start = "sudo systemctl restart MLX90640.service &"
    IR_check = ["systemctl", "is-active", "MLX90640.service"]
    overlay_kill = "sudo pkill -f MLX90640"
    overlay_start = "/home/pi/IR_UI/IR_Modules/MLX90640 &"
    overlay_check = ["ps", "ax"]
    
else:
    IR_kill = ""
    IR_start = ""
    IR_check = ""
    overlay_kill = ""
    overlay_start = ""
    overlay_check = ""
    
class heartbeat(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.measure_led = LED(9)
        self.setup_led =  LED(11)
        self.daemon = True
        self.start()
        
    def run(self):
        while 1:
            #off
            if(get_state(cfg.process_state) == 0):
                print("off")
                os.system(IR_kill)
                os.system(overlay_kill)
                self.setup_led.off()
                self.measure_led.off()
                
            #setup
            elif(get_state(cfg.process_state) == 1):
                print("setup")
                self.setup_led.on()
                self.measure_led.off()
                os.system(IR_kill)
                output = subprocess.run(overlay_check, stdout=subprocess.PIPE)
                if(re.search("MLX90640", output.stdout.decode('utf-8')) is None):
                    time.sleep(3)
                    os.system(overlay_start)
            
            #measuring
            elif(get_state(cfg.process_state) == 2):
                #while measuring, if the hard drive fills up, stop measuring
                if time.time() > cfg.check_disk:
                    cfg.check_disk = time.time() + 60
                    output = subprocess.run(["df", "/mnt/database/"], stdout=subprocess.PIPE)
                    m = re.search('.*(\d+)%', output.stdout.decode('utf-8'))
                    
                    if(int(m.group(1)) > 98):
                        cfg.process_state = "yikes"
                        break
                        
                #the hard drive isn't filled up
                print("measuring")
                self.setup_led.off()
                self.measure_led.on()
                
                output = subprocess.run(["systemctl", "is-active", "MLX90640.service"], stdout=subprocess.PIPE)
                if(output.stdout.decode('utf-8') != "active\n"):
                    os.system(overlay_kill)
                    time.sleep(5)
                    os.system(IR_start)
                
            #yikes 
            elif(get_state(cfg.process_state) == 3):
                    print("in dead state")
                    self.setup_led.off()
                    self.measure_led.off()
                    os.system(IR_kill)
                    os.system(overlay_kill)
                    exit()
                   
            time.sleep(3)