from pynput import mouse, keyboard
from time import localtime, strftime
# mouse
#def on_move(x, y):
#    print('Pointer moved to {0}'.format(
#        (x, y)))

def on_click(x, y, button, pressed):
    printstr = '{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y))
    if button == mouse.Button.left:
        printstr = '{0} at {1}'.format('Left Clicked' if pressed else 'Released', (x, y))
    elif button == mouse.Button.right:
        printstr = '{0} at {1}'.format('Right Clicked' if pressed else 'Released', (x, y))
    else:
        return False
    now = strftime("%Y-%m-%d %H:%M:%S", localtime())
    print(now+'| |'+printstr)
    #if not pressed:
        # Stop listener
    #    return False

def on_scroll(x, y, dx, dy):
    now = strftime("%Y-%m-%d %H:%M:%S", localtime())
    print(now+'| |'+'Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))
    
#keyboard
def on_press(key):
    now = strftime("%Y-%m-%d %H:%M:%S", localtime())
    try:
        print(now+'| |'+'alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print(now+'| |'+'special key {0} pressed'.format(
            key))

def on_release(key):
    now = strftime("%Y-%m-%d %H:%M:%S", localtime())
    print(now+'| |'+'{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    
now = strftime("%Y-%m-%d %H:%M:%S", localtime())
print('Program Starts || '+ now)
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    with mouse.Listener(
        #on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll) as listener:
        listener.join()

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

listener = mouse.Listener(
    #on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)
listener.start()