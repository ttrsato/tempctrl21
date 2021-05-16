def calcPID():
    global diff0, p, diff1, i, pid, raw, ptemp, Counter
    diff0 = target - ctemp
    if diff0 < 0:
        diff0 = 0
    p = diff0 * kp / target
    diff0 = target - ctemp
    diff1 = target - ptemp
    if ptemp == 0 or (diff0 < 0 or diff1 < 0):
        diff0 = 0
        diff1 = 0
    i = (diff0 + diff1) * (5 * ki)
    pid = p + i
    if pid > 0:
        pid = pid + 130
    raw = pid
    pid = pid / 100
    if pid > 10:
        pid = 10
    ptemp = ctemp
    if ctemp >= usl:
        pid = 0
    Counter += 1

def on_button_pressed_a():
    global target
    if mode == 1:
        target += -10
        basic.show_arrow(ArrowNames.SOUTH)
        # basic.showNumber(target / 10)
        dispDeg(target)
    elif mode == 0:
        basic.show_string("c")
        # basic.showNumber(ctemp / 10)
        dispDeg(ctemp)
    dispResults()
input.on_button_pressed(Button.A, on_button_pressed_a)

def dispResults():
    # if (pid >= 10) {
    # basic.showString("A")
    # } else {
    # basic.showNumber(pid)
    # }
    led.plot_bar_graph(pid, 10)
    serial.write_number(Counter)
    serial.write_string(" ")
    serial.write_number(pid)
    serial.write_string(" ")
    serial.write_number(raw)
    serial.write_string(" ")
    serial.write_number(ctemp)
    serial.write_line("")

def on_button_pressed_ab():
    global mode
    mode += 1
    mode = mode % 2
    if mode == 0:
        basic.show_string("C")
    else:
        basic.show_string("T")
    dispResults()
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_button_pressed_b():
    global target
    if mode == 1:
        target += 10
        basic.show_arrow(ArrowNames.NORTH)
        # basic.showNumber(target / 10)
        dispDeg(target)
    elif mode == 0:
        basic.show_string("t")
        # basic.showNumber(target / 10)
        dispDeg(target)
    dispResults()
input.on_button_pressed(Button.B, on_button_pressed_b)

def dispDeg(t: number):
    basic.show_number(t / 10)
def getTemp():
    global lm60OutAvg, vref, ctemp
    lm60OutAvg = 0
    vref = 0
    for index in range(ADC_LOOP_CNT):
        lm60OutAvg += pins.analog_read_pin(AnalogPin.P0)
    for index2 in range(REF_LOOP_CNT):
        vref += pins.analog_read_pin(AnalogPin.P1)
    lm60OutAvg = lm60OutAvg / ADC_LOOP_CNT
    vref = vref / REF_LOOP_CNT
    lm60OutAvg = 2475 * lm60OutAvg
    lm60OutAvg = lm60OutAvg / vref
    ctemp = Math.round((lm60OutAvg - 424) * 1000 / 625 + toffset)
vref = 0
lm60OutAvg = 0
raw = 0
pid = 0
i = 0
p = 0
ctemp = 0
REF_LOOP_CNT = 0
ADC_LOOP_CNT = 0
toffset = 0
ki = 0
kp = 0
ptemp = 0
diff1 = 0
diff0 = 0
Counter = 0
mode = 0
usl = 0
target = 0
integ = 0
kd = 0
target = 570
usl = 750
mode = 0
Counter = 0
diff0 = 0
diff0 = 0
diff1 = 0
ptemp = 0
kp = 2700
ki = 5
toffset = -20
ADC_LOOP_CNT = 100
REF_LOOP_CNT = 100
twait = 1000
basic.show_string("Temp ctl")
dispResults()

def on_forever():
    if mode == 0:
        pins.digital_write_pin(DigitalPin.P8, 1)
        basic.pause(pid * twait)
        pins.digital_write_pin(DigitalPin.P8, 0)
        basic.pause((10 - pid) * twait)
        getTemp()
        calcPID()
        dispResults()
    else:
        pins.digital_write_pin(DigitalPin.P8, 0)
basic.forever(on_forever)
