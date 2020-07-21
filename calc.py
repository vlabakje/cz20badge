import display, keypad, time
# calculator for CZ20 badge
# TODO:
# audio?
# * and / operators
# handle errors with color

BLACK=0x000000
WHITE=0xFFFFFF

KEYFUNCTIONS=[
    lambda: add_number(1), lambda: add_number(2), lambda: add_number(3), lambda: op_sub(),
    lambda: add_number(4), lambda: add_number(5), lambda: add_number(6), lambda: op_add(),
    lambda: add_number(7), lambda: add_number(8), lambda: add_number(9), lambda: key_error(),
    lambda: key_error(),   lambda: add_number(0), lambda: key_error(),   lambda: op_eq()]
    
DISPLAY={
    "0":    [WHITE, WHITE, WHITE, WHITE,
            WHITE,  BLACK, BLACK, WHITE,
            WHITE,  BLACK, BLACK, WHITE,
            WHITE,  WHITE, WHITE, WHITE,],
    "1":    [WHITE, WHITE, WHITE, WHITE,
            BLACK,  BLACK, WHITE, BLACK,
            BLACK,  BLACK, WHITE, BLACK,
            WHITE,  WHITE, WHITE, WHITE,],
    "2":    [WHITE, WHITE, WHITE, WHITE,
            BLACK,  BLACK, WHITE, BLACK,
            BLACK,  WHITE, BLACK, BLACK,
            WHITE,  WHITE, WHITE, WHITE,],
    "3":    [WHITE, WHITE, WHITE, WHITE,
            BLACK,  WHITE, WHITE, WHITE,
            BLACK,  BLACK, WHITE, WHITE,
            WHITE,  WHITE, WHITE, WHITE,],
    "4":    [WHITE, BLACK, BLACK, WHITE,
            WHITE,  BLACK, BLACK, WHITE,
            WHITE,  WHITE, WHITE, WHITE,
            BLACK,  BLACK, BLACK, WHITE,],
    "5":    [WHITE, WHITE, WHITE, WHITE,
            WHITE,  BLACK, BLACK, BLACK,
            WHITE,  WHITE, WHITE, WHITE,
            BLACK,  WHITE, WHITE, WHITE,],
    "6":    [WHITE, BLACK, BLACK, BLACK,
            WHITE,  WHITE, WHITE, WHITE,
            WHITE,  BLACK, BLACK, WHITE,
            WHITE,  WHITE, WHITE, WHITE,],
    "7":    [WHITE, WHITE, WHITE, WHITE,
            BLACK,  BLACK, BLACK, WHITE,
            BLACK,  BLACK, BLACK, WHITE,
            BLACK,  BLACK, BLACK, WHITE,],
    "8":    [WHITE, WHITE, WHITE, BLACK,
            WHITE,  BLACK, WHITE, WHITE,
            WHITE,  WHITE, BLACK, WHITE,
            BLACK,  WHITE, WHITE, WHITE,],
    "9":    [WHITE, WHITE, WHITE, WHITE,
            WHITE,  BLACK, BLACK, WHITE,
            WHITE,  WHITE, WHITE, WHITE,
            BLACK,  BLACK, BLACK, WHITE,],
    "-":    [BLACK, BLACK, BLACK, BLACK,
            WHITE,  WHITE, WHITE, BLACK,
            BLACK,  BLACK, BLACK, BLACK,
            BLACK,  BLACK, BLACK, BLACK,],
    "+":    [BLACK, WHITE, BLACK, BLACK,
            WHITE,  WHITE, WHITE, BLACK,
            BLACK,  WHITE, BLACK, BLACK,
            BLACK,  BLACK, BLACK, BLACK,],
    "=":    [WHITE, WHITE, WHITE, BLACK,
            BLACK,  BLACK, BLACK, BLACK,
            WHITE,  WHITE, WHITE, BLACK,
            BLACK,  BLACK, BLACK, BLACK,],
}

stack=[]
first_digit=True

def drawnumpad():
    # clear playing field
    display.drawFill(0x050505)
    display.flush()
    for x in range(3):
        for y in range(3):
            display.drawPixel(x, y, 0xFFFFFF)
    display.drawPixel(1, 3, 0xFFFFFF) # 0
    display.drawPixel(3, 0, 0xFF0000) # -
    display.drawPixel(3, 1, 0x00FF00) # +
    display.drawPixel(3, 3, 0x0000FF) # return
    display.flush()
    
def drawstring(n):
    display.drawFill(0x050505)
    display.flush()
    time.sleep(0.2)
    for digit in n:
        if digit in DISPLAY:
            for x in range(4):
                for y in range(4):
                    display.drawPixel(x, y, DISPLAY[digit][y*4+x])
            #display.drawRaw(0, 0, 4, 4, DISPLAY[digit])
            display.flush()
            time.sleep(0.5)
    drawnumpad()

def add_number(n):
    global stack, first_digit
    if first_digit:
        stack.append(str(n))
        first_digit = False
    else:
        stack[-1]=stack[-1]+str(n)
    drawstring(stack[-1])
    
def op_sub():
    global stack, first_digit
    if first_digit:
        stack.append("-")
    else:
        stack.append(lambda x, y: x - y)
    first_digit = not first_digit

def op_add():
    global stack, first_digit
    if first_digit:
        key_error()
    else:
        stack.append(lambda x, y: x + y)
        first_digit = True
    
def op_eq():
    global stack, first_digit
    while len(stack) >= 3:
        x, op, y = int(stack.pop()), stack.pop(), int(stack.pop())
        stack.append(str(op(x, y)))
        print("intermediate result: %s" % stack)
    if len(stack) == 1:
        drawstring("=" + stack[0])
        print(stack[0])
        stack = []
        first_digit = True
        
    
def key_error():
    print("error")
        
def on_key(key_index, pressed):
    if pressed:
        KEYFUNCTIONS[key_index]()  
        print(stack)


keypad.add_handler(on_key)
drawnumpad()
