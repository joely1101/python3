
#!/usr/bin/python3
#pip3 install pyautogui pynput
#apt-get install python3-tk python3-dev
import pyautogui,os,time,subprocess

def runcmd(*cmds,mtimeout=10):
    newcmd=""
    for cmd in cmds:
        newcmd+=cmd+" "
        print(f"{newcmd} ==",end='')
    #print(f"{newcmd}")
    ret = subprocess.run(newcmd, shell=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, encoding="utf-8", timeout=mtimeout)
    
    return ret.returncode
    '''
    if ret.returncode == 0:
      print(f"==> Success.")
    elif ignoreErr:
      print(f"==> OK")
    else:
      print(f"==> Error {ret.returncode}:{ret.stderr} \n {ret.stdout} ")
    return ret 
    '''

def vpn_alive(count=5):
    ips=("10.10.10.119","10.10.10.208")
    for i in range(0,count):
        for ip in ips:
            if runcmd(f"ping -c 1 -W 5 {ip}") == 0:
                print("vpn alive")
                return True
        time.sleep(20)
    return False

username=''
password=''
'''
pox={
    'connect':[1052,576],
    'username':[686,545],
    'password':[655,611],
    'authen':[748,748],
    'oktapush':[803,534],
}
'''
pox={
    'connect':[0,0],
    'username':[0,0],
    'password':[0,0],
    'authen':[0,0],
    'oktapush':[0,0],
}

def vpngui():
    #os.system("killall pulseUi")    
    #os.sleep(2)
    #os.system("LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/pulse/extra/usr/lib/x86_64-linux-gnu/ /usr/local/pulse/pulseUi &")    
    os.system("vpngui")
    
def vpn_go(username,password):
    print("launch vpn gui")
    vpngui()
    time.sleep(4)
    #pyautogui.moveTo(pox.get('connect')[0], pox.get('connect')[1], duration=1, tween=pyautogui.easeInOutQuad)
    pyautogui.moveTo(pox.get('connect')[0], pox.get('connect')[1], duration=1)
    print("click connect")
    pyautogui.click()
    time.sleep(5)
    print("input username")
    pyautogui.moveTo(pox.get('username')[0], pox.get('username')[1], duration=1)
    pyautogui.click()
    pyautogui.write(username)
    pyautogui.moveTo(pox.get('password')[0], pox.get('password')[1], duration=1)
    pyautogui.click()
    print("input password")
    pyautogui.write(password)
    pyautogui.moveTo(pox.get('authen')[0], pox.get('authen')[1], duration=1)
    pyautogui.click()
    time.sleep(3)
    print("click okta authentication")
    pyautogui.moveTo(pox.get('oktapush')[0], pox.get('oktapush')[1], duration=1)
    pyautogui.click()
    time.sleep(3)
    print("###############Please check okta message on your phone############")

def account():
    global username
    global password
    if username == "":
        username = input("Enter your name: ") 
    if password == "" :
        password = input("Enter your password: ") 

posfile="./pos.json"
clicknumber=0
from pynput.mouse import Button
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
import argparse,json,sys
def on_press(key):
    global username
    global password
    global clicknumber
    
    if clicknumber == 2:
        if hasattr(key,'char'):
            username+=key.char
    if clicknumber == 3:
        if hasattr(key,'char'):
            password+=key.char
        

    

def on_click(x, y, button, pressed):
    global clicknumber
    global pox
    if pressed:
        dname=list(pox)[clicknumber]
        pox[dname]=[x,y]
        clicknumber=clicknumber+1
    #print(f"{clicknumber} xx {len(pox)}")
    if clicknumber >= len(pox):
        print("detect finish")
        pox['myusername'] = username
        pox['mypassword'] = password
        
        with open(posfile,"w+") as f:
            json.dump(pox,f)
        sys.exit()


def detect_pox():
    global username
    global password
    username=""
    password=""
    vpngui()
    mouse_listener = MouseListener(on_click=on_click)
    keyboard_listener = KeyboardListener(on_press=on_press)
    keyboard_listener.start()
    mouse_listener.start()
    mouse_listener.join()


parser = argparse.ArgumentParser() 
parser.add_argument("-x", "--storePx", action="store_true",
                    help="detect click position") 
args = parser.parse_args() 
if not os.path.exists(posfile) or args.storePx:
    print("to keep vpn button position,please operate vpn login once")
    detect_pox()
    exit()
if os.path.exists(posfile):
    with open(posfile, "r") as f:
        pox=json.load(f)

username=pox.get('myusername',"")
password=pox.get('mypassword',"")
account()
vpn_go(username,password)


"""
def main():
    account()
    if vpn_alive(1) == False:
        print("vpn disconnected....")
        vpn_go(username,password)

    while True:
        if vpn_alive():
            time.sleep(300)
        else:
            print("vpn disconnected....")
            vpn_go(username,password)

from pynput import mouse
def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if not pressed:
        # Stop listener
        return False



from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput.keyboard import Key
import json,sys
record=[]

def on_press(key):
    global record
    if key == Key.esc:
        #write key to json
        print(f"{record}")
        #json.dumps(record)
        with open("./rr.json","w+") as f:
            json.dump(record,f)
            #f.write(str)
        sys.exit()
        
    
    print("Key pressed: {0}".format(key))

def on_release(key):
    global record
    key={'type':'key','key':f"{key}"}
    record.append(key)

def on_click(x, y, button, pressed):
    global record
    click={'type':'mclick','pox':[x,y]}
    record.append(click)
    #print('Mouse released at ({0}, {1}) with {2}'.format(x, y, button))
    print(json.dumps(record))



def setup_pox():
    # Setup the listener threads
    keyboard_listener = KeyboardListener(on_press=on_press, on_release=on_release)
    mouse_listener = MouseListener(on_click=on_click)

    # Start the threads and join them so the script doesn't end early
    keyboard_listener.start()
    mouse_listener.start()
    keyboard_listener.join()
    #mouse_listener.join()

def play():
    with open("./rr.json", "r") as f:
    action=json.load(f)
    for act in action:
        if act['type'] == 'mclick':

setup_pox()
"""
