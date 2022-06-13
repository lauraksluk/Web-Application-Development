"use strict"

var value = 0
var valueStr = ""

var delayInMilliseconds = 3000;
var valueStack = []
var entering = true

function init() {
    //document.getElementById('output').innerHTML = 0
    valueStack = []
    valueStack.push(0)
    var entering = true
}

function clickDigit(digit) {
    document.getElementById('output').style.backgroundColor = "rgb(191, 211, 193)"
    if (entering) {
        let bottom = valueStack.pop()
        bottom = bottom * 10 + parseInt(digit)
        valueStack.push(bottom)
        document.getElementById('output').innerHTML = bottom

        // valueStr += digit
        // value = parseInt(valueStr)
        // document.getElementById('output').innerHTML = value
    } else {
        if (!isStackFull()) {
            valueStack.push(0)
            entering = true
            let bottom = valueStack.pop()
            bottom = bottom * 10 + parseInt(digit)
            valueStack.push(bottom)
            document.getElementById('output').innerHTML = bottom
        }

        // valueStr = ""
        // value = 0
        // entering = true
        // valueStr += digit
        // value = parseInt(valueStr)
        // document.getElementById('output').innerHTML = value
    }
}

function isStackFull() {
    return valueStack.length > 2
}

function clickPush() {
    document.getElementById('output').style.backgroundColor = "rgb(191, 211, 193)"
    if (!isStackFull()) {
        // let valToPush = document.getElementById('output').innerHTML
        // valueStack.push(parseInt(valToPush))
        // entering = true
        // value = 0
        // valueStr = ""
        valueStack.push(0)
        document.getElementById('output').innerHTML = 0
        entering = true
    } else {
        overflow()
    }
}

function overflow() {
    document.getElementById('output').innerHTML = 
        "<span style='color: white;'>stack overflow</span>"
    document.getElementById('output').style.backgroundColor = "red"
    //setTimeout(function() {}, delayInMilliseconds);
    init()
}

function underflow() {
    document.getElementById('output').innerHTML = 
    "<span style='color: white;'>stack underflow</span>"
    document.getElementById('output').style.backgroundColor = "red"
    //setTimeout(function() {}, delayInMilliseconds);
    init()
}

function div0() {
    document.getElementById('output').innerHTML = 
    "<span style='color: white;'>divide by zero</span>"
    document.getElementById('output').style.backgroundColor = "red"
    //setTimeout(function() {}, delayInMilliseconds);
    init()
}

function clickPlus() {
    // let valToPush = document.getElementById('output').innerHTML
    // valueStack.push(parseInt(valToPush))
    if (valueStack.length > 1) {
        let y = valueStack.pop()
        let x = valueStack.pop()
        let ans = x + y
        valueStack.push(ans)
        document.getElementById('output').style.backgroundColor = 'rgb(240, 213, 184)'
        document.getElementById('output').innerHTML = ans
        entering = false
    } else {
        underflow()
    }
}

function clickMinus() {
    // let valToPush = document.getElementById('output').innerHTML
    // valueStack.push(parseInt(valToPush))
    if (valueStack.length > 1) {
        let y = valueStack.pop()
        let x = valueStack.pop()
        let ans = x - y
        valueStack.push(ans)
        document.getElementById('output').style.backgroundColor = 'rgb(240, 213, 184)'
        document.getElementById('output').innerHTML = ans
        entering = false
    } else {
        underflow()
    }
}

function clickTimes() {
    // let valToPush = document.getElementById('output').innerHTML
    // valueStack.push(parseInt(valToPush))
    if (valueStack.length > 1) {
        let y = valueStack.pop()
        let x = valueStack.pop()
        let ans = x * y
        valueStack.push(ans)
        document.getElementById('output').style.backgroundColor = 'rgb(240, 213, 184)'
        document.getElementById('output').innerHTML = ans
        entering = false
    } else {
        underflow()
    }
}

function clickDivide() {
    // let valToPush = document.getElementById('output').innerHTML
    // valueStack.push(parseInt(valToPush))
    if (valueStack.length > 1) {
        let y = valueStack.pop()
        if (y != 0) {
            let x = valueStack.pop()
            let ans = Math.floor(x / y)
            valueStack.push(ans)
            document.getElementById('output').style.backgroundColor = 'rgb(240, 213, 184)'
            document.getElementById('output').innerHTML = ans
            entering = false
        } else {
            div0()
        }
        
    } else {
        underflow()
    }
}