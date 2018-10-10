import sys, os, math, platform ,re,time, datetime
from os.path import expanduser
import pyperclip
import pynput


scriptversion = '2018-Oct-1'
Author = r'Beter PAN<beter.pan@nokia.com>'
#Path Stuffs
(strCurrentPath, strCurrentFileName) = os.path.split(__file__)
downloadlogfolder = os.path.join(expanduser("~"), 'Downloads')

if strCurrentPath in sys.path:
    #crt.Dialog.MessageBox("Beterhans\'s iSAM GPON Check Script \nPython version " + platform.python_version())
    output_raw = ''
else:
    sys.path.insert(0, strCurrentPath)
    sys.path.insert(1, os.path.join(strCurrentPath,'lib'))

#------------------ Global vars ------------
str_current_clip = ''
str_prev_clip = ''
is_quit = False

#------------------ Functions ------------------------------------------------


# ------------------ The key monitor ---------------------
KeyComb_Quit = [
    {pynput.keyboard.Key.ctrl, pynput.keyboard.KeyCode(char='q')},
    {pynput.keyboard.Key.ctrl_l, pynput.keyboard.KeyCode(char='q')},
    {pynput.keyboard.Key.ctrl_r, pynput.keyboard.KeyCode(char='q')}

]

def on_press(key):
    global is_quit
    if any([key in comb for comb in KeyComb_Quit]):
        current.add(key)
        if any(all(k in current for k in comb) for comb in KeyComb_Quit):
            is_quit = True

def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass


# The currently active modifiers
current = set()

listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()


# ------------------ Main part -----------------------------
str_current_clip = pyperclip.paste()

#file_bin_output = open(os.path.join(downloadlogfolder, 'log_clipboard_binary.txt'), "wb")
print('Press Ctrl+q to stop!')
print('Important!! You need sudo or root to run this script on Mac or Linux!')


while True:
    if str_current_clip != str_prev_clip:
        print('Change Found!')
        # Check if object is string type just use type() won't work.
        if isinstance(str_current_clip,str):
            file_txt_output = open(os.path.join(downloadlogfolder, 'log_clipboard_text.txt'), "a+")
            file_txt_output.write('<' + str(datetime.datetime.now()) + '>' + ' : ' + str_current_clip + '\n\n')
            file_txt_output.close
            print('Writing to file')
        str_prev_clip = str_current_clip
        time.sleep(0.5)
        str_current_clip = pyperclip.paste()
        if is_quit:
            break
    else:
        #print('nothing')
        time.sleep(0.5)
        str_current_clip = pyperclip.paste()
        if is_quit:
            break

print('Quiting...')
file_txt_output.close()

quit(0)
