var = dict()
pm_map = {'++': '+', '--': '+', '+-': '-', '-+': '-', '  ': ' '}
operators = ('+', '-', '*', '/', '^', '(', ')')
precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}


def init_variable(exp):
    if exp.count('=') == 1:
        identifier, value = [str(i.strip()) for i in exp.split('=')]
        if identifier.isalpha():
            if value.isnumeric():
                var[identifier] = value
            elif value.isalpha():
                if value in var:
                    var[identifier] = var[value]
                else:
                    print('Unknown variable')
            else:
                print('Invalid assignment')
        else:
            print('Invalid identifier')
    else:
        print('Invalid assignment')


def replace_identifiers(exp1):
    while True:
        copy_s = exp1[:]
        for pm_pair, sign in var.items():
            exp1 = exp1.replace(pm_pair, sign)
        if len(exp1) == len(copy_s):
            return exp1


def normalise_input(exp2):
    while True:
        copy_s = exp2[:]
        for pm_pair, sign in pm_map.items():
            exp2 = exp2.replace(pm_pair, sign)
        if len(exp2) == len(copy_s):
            return replace_identifiers(exp2)


def to_postfix(exp3):
    exp3 = exp3.replace('(', '( ').replace(')', ' )')
    exp3 = [i.strip() for i in exp3.split()]
    result = ''
    stack = []

    for i in exp3:
        if i in operators:
            if len(stack) == 0 or stack[-1] == '(':
                stack.append(i)
            elif i == '(':
                stack.append(i)
            elif i == ')':
                while stack[-1] != '(':
                    result += stack.pop() + ' '
                stack.pop()
            elif precedence[i] > precedence[stack[-1]]:
                stack.append(i)
            elif precedence[stack[-1]] >= precedence[i]:
                while len(stack) > 0 and stack[-1] != '(' and precedence[stack[-1]] >= precedence[i]:
                    result += stack.pop() + ' '
                stack.append(i)
        else:
            result += i + ' '

    while len(stack) > 0:
        result += stack.pop() + ' '
    return result.strip()


def eval_postfix(exp4):
    exp4 = [i.strip() for i in exp4.split()]
    stack = []
    for i in exp4:
        if i not in operators and i.isnumeric():
            stack.append(i)
        else:
            o1 = stack.pop()
            o2 = stack.pop()
            a = eval(f'{o2} {i} {o1}')
            stack.append(a)
    return int(stack.pop())


while True:
    arguments = input()
    if arguments == '/exit':
        print('Bye!')
        break
    elif arguments == '/help':
        print('The program calculates the sum of numbers')
        continue
    elif arguments.startswith('/'):
        print('Unknown command')
        continue
    elif arguments == '':
        continue
    elif '=' in arguments:
        init_variable(arguments)
        continue
    elif arguments.strip().isalpha():
        if arguments in var:
            print(var[arguments])
        else:
            print('Unknown variable')
        continue
    try:
        exp = normalise_input(arguments)
        if len(exp.split()) == 1:
            print(int(exp))
            continue
        else:
            print(eval_postfix(to_postfix(exp)))
    except Exception:
        print('Invalid expression')
