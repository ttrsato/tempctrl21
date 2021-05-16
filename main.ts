function calcPID () {
    diff0 = target - ctemp
    if (diff0 < 0) {
        diff0 = 0
    }
    p = diff0 * kp / target
    diff0 = target - ctemp
    diff1 = target - ptemp
    if (ptemp == 0 || (diff0 < 0 || diff1 < 0)) {
        diff0 = 0
        diff1 = 0
    }
    i = (diff0 + diff1) * (5 * ki)
    pid = p + i
    if (pid > 0) {
        pid = pid + 130
    }
    raw = pid
    pid = pid / 100
    if (pid > 10) {
        pid = 10
    }
    ptemp = ctemp
    if (ctemp >= usl) {
        pid = 0
    }
    Counter += 1
}
input.onButtonPressed(Button.A, function () {
    if (mode == 1) {
        target += -10
        basic.showArrow(ArrowNames.South)
        // basic.showNumber(target / 10)
        dispDeg(target)
    } else if (mode == 0) {
        basic.showString("c")
        // basic.showNumber(ctemp / 10)
        dispDeg(ctemp)
    }
    dispResults()
})
function dispResults () {
    // if (pid >= 10) {
    // basic.showString("A")
    // } else {
    // basic.showNumber(pid)
    // }
    led.plotBarGraph(
    pid,
    10
    )
    serial.writeNumber(Counter)
    serial.writeString(" ")
    serial.writeNumber(pid)
    serial.writeString(" ")
    serial.writeNumber(raw)
    serial.writeString(" ")
    serial.writeNumber(ctemp)
    serial.writeLine("")
}
input.onButtonPressed(Button.AB, function () {
    mode += 1
    mode = mode % 2
    if (mode == 0) {
        basic.showString("C")
    } else {
        basic.showString("T")
    }
    dispResults()
})
input.onButtonPressed(Button.B, function () {
    if (mode == 1) {
        target += 10
        basic.showArrow(ArrowNames.North)
        // basic.showNumber(target / 10)
        dispDeg(target)
    } else if (mode == 0) {
        basic.showString("t")
        // basic.showNumber(target / 10)
        dispDeg(target)
    }
    dispResults()
})
function dispDeg (t: number) {
    basic.showNumber(t / 10)
}
function getTemp () {
    lm60OutAvg = 0
    vref = 0
    for (let index = 0; index < ADC_LOOP_CNT; index++) {
        lm60OutAvg += pins.analogReadPin(AnalogPin.P0)
    }
    for (let index = 0; index < REF_LOOP_CNT; index++) {
        vref += pins.analogReadPin(AnalogPin.P1)
    }
    lm60OutAvg = lm60OutAvg / ADC_LOOP_CNT
    vref = vref / REF_LOOP_CNT
    lm60OutAvg = 2475 * lm60OutAvg
    lm60OutAvg = lm60OutAvg / vref
    ctemp = Math.round((lm60OutAvg - 424) * 1000 / 625 + toffset)
}
let vref = 0
let lm60OutAvg = 0
let raw = 0
let pid = 0
let i = 0
let p = 0
let ctemp = 0
let REF_LOOP_CNT = 0
let ADC_LOOP_CNT = 0
let toffset = 0
let ki = 0
let kp = 0
let ptemp = 0
let diff1 = 0
let diff0 = 0
let Counter = 0
let mode = 0
let usl = 0
let target = 0
let kd = 0
let integ = 0
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
let twait = 1000
basic.showString("Temp ctl")
dispResults()
basic.forever(function () {
    if (mode == 0) {
        pins.digitalWritePin(DigitalPin.P8, 1)
        basic.pause(pid * twait)
        pins.digitalWritePin(DigitalPin.P8, 0)
        basic.pause((10 - pid) * twait)
        getTemp()
        calcPID()
        dispResults()
    } else {
        pins.digitalWritePin(DigitalPin.P8, 0)
    }
})
