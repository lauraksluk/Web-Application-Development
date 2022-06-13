from logging.handlers import SMTPHandler
from pickletools import stackslice
from django.shortcuts import render
import string

# Create your views here.

def initial_context():
    context = {}
    context['output'] = 0
    context['stack'] = [0]
    context['entering'] = True
    context['color'] = "rgb(191, 211, 193)"
    return context

def manipulateStack(stackStr):
    inputStack = []
    i = 1
    while(i < len(stackStr)):
        newI = stackStr.find(',', i, len(stackStr))
        if (newI == -1):
            digit = stackStr[i:len(stackStr)-1]
            inputStack.append(int(digit))
            break
        digit = stackStr[i : newI]
        inputStack.append(int(digit))
        i = newI + 1
    return inputStack

def process_parameters(values):
    inputs = {}
    correct_buttons = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                        "plus", "times", "minus", "divide", "push"]
    if (values['button'] in correct_buttons):
        if values['button'] in string.digits:
            digitStr = values['button']
            inputs['digit'] = int(digitStr)
        else:
            inputs['op'] = values['button']
    else:
        raise Exception('invalid button entry')

    stackStr = values['stack']
    inputs['inputStack'] = manipulateStack(stackStr)

    if (values['entering'] == 'True'):
        inputs['entering'] = True
    if (values['entering'] == 'False'):
        inputs['entering'] = False
    if (values['entering'] != 'True' and values['entering'] != 'False'):
        raise Exception('invalid button entry')
    
    return inputs

def isStackFull(stack):
    return len(stack) > 2
    
def process_digit(inputs):
    context = {}
    context['color'] = "rgb(191, 211, 193)"
    if (inputs['entering']):
        bottom = inputs['inputStack'].pop()
        bottom = bottom * 10 + inputs['digit']
        inputs['inputStack'].append(bottom)
        context['stack'] = inputs['inputStack']
        context['output'] = bottom
        context['entering'] = inputs['entering']
        print(inputs['inputStack'])
    else:
        if (not isStackFull(inputs['inputStack'])):
            inputs['inputStack'].append(0)
            inputs['entering'] = True
            bottom = inputs['inputStack'].pop()
            bottom = bottom * 10 + inputs['digit']
            inputs['inputStack'].append(bottom)
            context['stack'] = inputs['inputStack']
            context['output'] = bottom
            context['entering'] = inputs['entering']

    return context

def process_operation(inputs):
    context = {}
    if (inputs['op'] == 'push'):
        context['color'] = "rgb(191, 211, 193)"
        if (not isStackFull(inputs['inputStack'])):
            inputs['inputStack'].append(0)
            inputs['entering'] = True
            context['output'] = 0
            context['stack'] = inputs['inputStack']
            context['entering'] = inputs['entering']
            return context
        else:
            raise Exception('stack overflow')
    if (inputs['op'] == 'plus' or inputs['op'] == 'minus' or inputs['op'] == 'times' ):
        context['color'] = 'rgb(240, 213, 184)'
        if (len(inputs['inputStack']) > 1):
            y = inputs['inputStack'].pop()
            x = inputs['inputStack'].pop()
            if (inputs['op'] == 'plus'):
                ans = x + y
            if (inputs['op'] == 'minus'):
                ans = x - y
            if (inputs['op'] == 'times'):
                ans = x * y
            inputs['inputStack'].append(ans)
            inputs['entering'] = False
            context['output'] = ans
            context['stack'] = inputs['inputStack']
            context['entering'] = inputs['entering']
            return context
        else:
            raise Exception('stack underflow')
    if (inputs['op'] == 'divide'):
        context['color'] = 'rgb(240, 213, 184)'
        if (len(inputs['inputStack']) > 1):
            y = inputs['inputStack'].pop()
            if (y != 0):
                x = inputs['inputStack'].pop()
                ans = x // y
                inputs['inputStack'].append(ans)
                inputs['entering'] = False
                context['output'] = ans
                context['stack'] = inputs['inputStack']
                context['entering'] = inputs['entering']
                return context
            else:
                raise Exception('divide by zero')
        else:
            raise Exception('stack underflow')

       
def calculator_action(request):
    if (request.method == 'GET'):
        context = initial_context()
        return render(request, 'calculator/calculator.html', context)
    try:
        inputs = process_parameters(request.POST)
        if ('digit' in inputs):
            context = process_digit(inputs)
        else:
            context = process_operation(inputs)
        return render(request, 'calculator/calculator.html', context)
    except Exception as e:
        return render(request, 'calculator/error.html', {'error': str(e)})


