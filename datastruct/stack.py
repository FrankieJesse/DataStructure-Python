__author__ = 'lifei'
'''
中序是常见的方式，
中序表达式转换为后序表达式，
    主体思路：将运算符包括左括号，入栈。将oprands进入结果字符串中。
    如果当前元素是左括号，入栈，
    如果当前元素是右括号，将栈中左括号以后的运算符出栈放入结果字符串中。
    如果当前元素是oprator，则将栈中优先级大于等于当前运算符的运算符出栈。
    最后，将所有栈中未出栈的预算符出栈放入结果字符串中。
中序表达式转换为前序表达式，
    将中序表达式，翻转。求后序表达式，然后再翻转，就是前序表达式了。
    值得注意的是，在求后序表达式时，对于当前操作符是operator时，本来是要将栈中大于等于其优先级的出栈，因为是翻转的字符串，
    所以只能从栈中弹出大于当前operator的运算符。但对于^在等于的时候，也要弹出。
前序转中序：
    前序是operator在前，oprands在后，那就翻转。遇到一个oprands就入栈，遇到operator就从栈中弹两个oprands出来，组成一个表达式
    作为一个新的字符串（oprands）入栈。直到栈中只有一个元素，就是最后的表达式。
后序转中序：
    后序是operands在前，operator在后，就很简单。oprands入栈，遇到operator就弹两个oprands出来组成一个表达式然后入栈。
    直到栈中只有一个元素。

'''
from datastruct.logger import FinalLogger
import string

logger = FinalLogger.getLogger()


class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def isEmpty(self) -> bool:
        return self.items == []

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


def parChecker(symbolString) -> bool:
    stack = Stack()
    symbolLen = len(symbolString)
    for index in range(0, symbolLen):
        if (symbolString[index] == '('):
            stack.push(symbolString[index])
        elif (symbolString[index] == ')'):
            if stack.isEmpty():
                return False
            else:
                stack.pop()
    return stack.isEmpty()


def parCheckerTest():
    '''
    test for 括号匹配
    :return:
    '''
    myInputStr = '((((((((()))))))))'
    retVal = parChecker(myInputStr)
    if retVal == True:
        logger.info("input is perfect")
    else:
        logger.info("input is wrong")


def dividedByBase(inputNumber: int = 96, base: int = 2) -> str:
    '''
    计算进制之间转换，10进制转为2进制，返回一个字符串
    :return:
    '''
    retString = ''
    digits = "0123456789ABCDEF"
    if (inputNumber < 0):
        return retString
    baseNum = inputNumber
    stack = Stack()
    while True:
        stackItem = baseNum % base
        stack.push(stackItem)
        if baseNum // base > 0:
            baseNum = baseNum // base
        else:
            break
    while not stack.isEmpty():
        retString = retString + digits[stack.pop()]
    return retString


def dividedByBaseTest():
    # logger = FinalLogger.getLogger()
    resultStr = dividedByBase(base=16)
    logger.info("resultStr = %s", resultStr)


def get_pop_condition(stack: Stack, dict, current_value, condition: str) -> bool:
    if stack.isEmpty():
        return False
    peek_final_value = dict.get(stack.peek())
    current_final_value = dict.get(current_value)
    if peek_final_value > current_final_value:
        return True
    if peek_final_value == current_final_value:
        if condition.startswith("postfix"):
            return True
        if condition.startswith("prefix") and current_value == '^':
            return True
    return False


def infix_to_postfix(inputStr: str, condition) -> str:
    '''
    算式的前序表达式，重点在于符号和括号如何处理。
    对于前序表达式来说：
    如果当前字符是左括号，入栈
    如果当前符号是右括号，将栈中到左括号的所有运算符出栈，并放入结果列表中
    如果当前符号是运算符，栈中如果有优先级高于他或等于他的运算符，出栈，放入结果列表中，然后将其入栈。
    如果当前符号是数字，写入结果列表中
    :param inputStr:运算表达式，可以带括号，不同符号之间以空格作为间隔
    :return:字符串，表达式
    '''
    retList = []
    operator_dict = {'(': 0, '+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack = Stack()
    if (len(inputStr) == 0):
        return "".join(retList)
    # tokenList = inputStr.split()
    tokenList = list(inputStr)
    for token in tokenList:
        if token == ' ':
            continue
        if token == '(':
            stack.push(token)
            continue
        if token == ')':
            pop_item = stack.pop()
            while (pop_item != '('):
                retList.append(pop_item)
                pop_item = stack.pop()
            continue
        if token in operator_dict.keys():
            # logger.info("token = %s, dict.keys = %s", token, operator_dict.keys())
            # while (not stack.isEmpty()) and (operator_dict.get(stack.peek()) >= operator_dict.get(token)):
            while (get_pop_condition(stack, operator_dict, token, condition)):
                retList.append(stack.pop())
            stack.push(token)
            continue
        retList.append(token)
        # if token in string.digits:
        #     retStr.append(token)
    while (not stack.isEmpty()):
        retList.append(stack.pop())
    returnStr = "".join(retList)
    return returnStr


def post_order_test():
    input_str = "1 + 2 * ( 3 + 4 ) / 5"
    input_str2 = "( 1 + 2 ) * 3 - ( 4 - 5 ) * ( 6 + 7 )"
    input_str3 = "a + b * (c ^ d - e) ^ (f + g * h) - i"
    out_str = infix_to_postfix(input_str, "postfix")
    logger.info("the result = %s", out_str)
    out_str2 = infix_to_postfix(input_str2, "postfix")
    logger.info("the result = %s", out_str2)
    out_str3 = infix_to_postfix(input_str3, "postfix")
    logger.info("the result = %s", out_str3)


def infix_to_prefix(input_str: str) -> str:
    '''
    对输入的中序表达式，先翻转，然后求后序表达式，然后再翻转。得到的就是前序表达式。
    需要注意的是，在翻转的字符串求后序表达式时，对于栈中符号的处理有特别之处。
    一般的后序，只要当前入栈的符号的优先级小于等于栈中元素的优先级，则栈中符号要出栈。但对于翻转的字符串，栈中优先级更高时出栈，
    栈中优先级相等时，只有^需要出栈，其他不需要出栈，否则a+b+c，就容易被计算成，c+b+a
    :param input_str:一个中序表达式
    :return:返回一个前序表达式
    '''
    ret_list = []
    post_fix_str = ""
    if (len(input_str) == 0):
        return "".join(ret_list)
    reverse_list = list(input_str)
    reverse_list.reverse()
    reverse_str = "".join(reverse_list)
    # 将翻转后的字符串，求后序表达式
    post_fix_str = infix_to_postfix(reverse_str, "prefix")
    # 将后序表达式翻转为前序表达式
    pre_fix_list = list(post_fix_str)
    pre_fix_list.reverse()
    return "".join(pre_fix_list)


def infix_to_prefix_test():
    input_str = "x+y*z/w+u"
    out_str = infix_to_prefix(input_str)
    logger.info("out_str = %s", out_str)


def prefixToInfix(inputStr) -> str:
    '''
    将前序表达式，转换为中序表达式。将前序表达式翻转。然后分别入栈。操作数入栈，遇到操作符，中序表达。然后将该结果作为
    一个操作数入栈。继续找，重复上述过程
    :param inputStr:前序表达式
    :return:中序表达的字符串
    '''
    operatorList = ['+', '-', '*', '/', '^']
    if (len(inputStr) == 0):
        return ""
    reverseList = list(inputStr)
    reverseList.reverse()
    stack = Stack()
    for item in reverseList:
        if (item in operatorList):
            if (stack.isEmpty()):
                return ""
            operand1 = stack.pop()
            operand2 = stack.pop()
            tmpStr = '(' + str(operand1) + str(item) + str(operand2) + ')'
            stack.push(tmpStr)
        else:
            stack.push(str(item))
    resultStr = stack.pop()
    logger.info("the resultStr = %s", resultStr)
    return resultStr


def prefixToInfixTest():
    inputStr = "*-A/BC-/AKL"
    resultStr = prefixToInfix(inputStr)
    # ((A-(B/C))*((A/K)-L))
    logger.info("resultStr = %s", resultStr)


def postFixToInfix(inputStr) -> str:
    '''
    后序转中序，很简单，将操作数入栈，遇到操作符，出栈两个元素与操作符形成一个表达式，作为一个字符串进入栈中。
    最后栈中的一个元素（字符串）就是中序表达了。
    :param inputStr:
    :return:
    '''
    if (len(inputStr) == 0):
        return ""
    stack = Stack()
    operatorList = ['+', '-', '*', '/', '^']
    for item in inputStr:
        if (item in operatorList):
            if (stack.size() < 2):
                return ""
            oprand1 = str(stack.pop())
            oprand2 = str(stack.pop())
            pushStr = '(' + oprand2 + str(item) + oprand1 + ')'
            stack.push(pushStr)
        else:
            stack.push(str(item))
    retStr = stack.pop()
    return retStr


def postFixToInfixTest():
    inputStr = "abcd^e-fgh*+^*+i-"
    retStr = postFixToInfix(inputStr)
    # a + b * (c ^ d - e) ^ (f + g * h) - i
    logger.info("postFix2Infix = %s", retStr)


class SpecialStack(Stack):
    def __init__(self):
        Stack.__init__(self)
        # self.items = []
        self.items_special = []

    def push(self, item):
        '''
        基础栈正常入栈。对于特别的栈，每进入一个元素，就要记录一个当前栈的最小值。
        每一次出栈，两个栈对应都出栈一个元素。
        :param item:
        :return:
        '''
        self.items.append(item)
        peek_value = 0
        if (self.items_special == []):
            self.items_special.append(item)
        else:
            peek_value = self.items_special[len(self.items_special) - 1]

        if (peek_value >= item):
            insert_value = item
        else:
            insert_value = peek_value
        self.items_special.append(insert_value)

    def pop(self):
        '''
        基础栈和特别栈均出栈。正常出栈。返回的是基础栈的数据。
        :return:
        '''
        self.items_special.pop()
        return Stack.pop(self)

    def minpeek(self):
        '''
        peek函数返回的是基础栈。minpeek返回特别栈
        :return:
        '''
        return self.items_special[len(self.items_special) - 1]


def stock_span(prices: []) -> []:
    '''
    本质上是使用了单调递增栈的方式。
    所有的元素，如果这个元素的值比栈顶的元素大的话，那么栈中的元素就出栈。直到遇到栈中第一个比当前元素大的元素（元素不出栈）
    那么当前的index与栈顶中元素之间的元素，左开右闭区间。
    :param prices:
    :return:
    '''
    ret_list = []
    price_stack = Stack()
    # 一个小技巧：将栈中的第一个元素放置-1这个index（元素所在的下标），这样栈不会为空
    price_stack.push(-1)
    logger.info("stack.peek = %d", price_stack.peek())
    for index in range(0, len(prices)):
        # 如果栈中只有哨兵。则直接入库。
        # if (price_stack.size() == 1):
        # 直到栈中只有哨兵，或栈顶元素已经大于当前元素的时候，退出循环
        while (price_stack.size() > 1 and prices[price_stack.peek()] <= prices[index]):
            price_stack.pop()
        # 此处包括了两种情况，即栈中只有哨兵的情况，和栈顶元素比当前的元素大的情况
        ret_list.append(index - price_stack.peek())
        price_stack.push(index)
    return ret_list


def stock_span_new(prices: []) -> []:
    '''
    相比上一个函数，这个函数在执行时间上做了优化，在geeks中提交时，上一个函数执行时间超过6s，而这个函数执行时间只有不到4s。
    相差的地方，主要是一个新启了一个Stack类，而在这个函数中直接用list的操作，模仿了栈操作。
    :param prices:
    :return:
    '''
    ret_list = []
    price_list = []
    # 一个小技巧：将栈中的第一个元素放置-1这个index（元素所在的下标），这样栈不会为空
    price_list.append(-1)
    for index in range(0, len(prices)):
        # 直到栈中只有哨兵，或栈顶元素已经大于当前元素的时候，退出循环
        while (len(price_list) > 1 and prices[price_list[-1]] <= prices[index]):
            price_list.pop()
        # 此处包括了两种情况，即栈中只有哨兵的情况，和栈顶元素比当前的元素大的情况
        ret_list.append(index - price_list[-1])
        # price_stack.push(index)
        price_list.append(index)
    return ret_list


def stock_span_test():
    stock = [1, 2, 3, 4, 5, 6, 7]
    list1 = stock_span(stock)
    logger.info("output list1")
    # print(list1)
    logger.info(list1)
    stock2 = [7, 6, 5, 4, 3, 2, 1]
    list2 = stock_span(stock2)
    logger.info("output list2")
    logger.info(list2)
    # print(list2)


def is_brackets_balanced(brackets_string) -> bool:
    '''
    找到括号是否匹配，
    对于左括号，直接进栈，如果对于右括号，判断栈顶元素是否是与其匹配的括号，如果是栈顶元素
    出栈，当前右括号不进栈。
    最后如果栈为空，则是匹配的。如果栈不为空，则说明括号是不匹配的。
    :param brackets_string:
    :return:
    '''
    if len(brackets_string) == 0:
        return False
    pop_brackets_dict = {')' : '(', ']' : '[', '}' : '{'}
    logger.info("input brackets list is:")
    logger.info(brackets_string)
    stack_list = []
    for brackets in brackets_string:
        if brackets in pop_brackets_dict.keys():
            if (len(stack_list) < 1):
                return False
            if (pop_brackets_dict[brackets] == stack_list[-1]):
                stack_list.pop()
                continue
            else:
                return False
        else:
            stack_list.append(brackets)
    if len(stack_list) == 0:
        return True
    else:
        return False


def is_brackets_balanced_test():
    input_brackets_string = "[()]{}{[()()]()}"
    ret_val = is_brackets_balanced(input_brackets_string)
    logger.info("ret_val is %d", ret_val)
    input_brackets_string_2 = ")]}"
    ret_val = is_brackets_balanced(input_brackets_string_2)
    logger.info("ret_val2 is %d", ret_val)

def next_greater_element(input_number) -> []:
    '''
    求右边第一个比他大的数，如果有记录下来，如果没有记录为-1
    先将第一个元素入栈，对于后边的所有元素，
    如果当前元素比栈顶的元素小，则元素入栈。
    如果元素比栈顶的元素大，则出栈，直到栈顶元素比当前元素大，并记录出栈的元素的NGE为当前元素。然后当前元素入栈
    最后，栈中如果有元素，则栈中元素的NGE均为-1.因为右边没有比他更大的元素。
    :param input_number:
    :return:
    '''
    ret_list = []
    assist_stack_list = []
    if len(input_number) == 0:
        return ret_list
    for index in range(0, len(input_number)):
        ret_list.append(-1)
    assist_stack_list.append(0)
    for index in range(1, len(input_number)):
        while len(assist_stack_list) >= 1 and input_number[index] > input_number[assist_stack_list[-1]]:
            ret_list[assist_stack_list.pop()] = input_number[index]
        assist_stack_list.append(index)
    # logger.info("output NGE :")
    # logger.info(ret_list)
    return ret_list


def next_greater_element_test():
    input_number = [1, 2, 3, 4, 5]
    ret_list = next_greater_element(input_number)
    logger.info("ret_list = ")
    logger.info(ret_list)
    input_number2 = [5, 4, 3, 2, 1]
    ret_list2 = next_greater_element(input_number2)
    logger.info("ret_list = ")
    logger.info(ret_list2)


def stack_test():
    logger = FinalLogger.getLogger()
    logger.info("*********stack_test begion")
    parCheckerTest()
    dividedByBaseTest()
    post_order_test()
    infix_to_prefix_test()
    prefixToInfixTest()
    postFixToInfixTest()
    stock_span_test()
    is_brackets_balanced_test()
    next_greater_element_test()
    logger.info("*********stack_test end")
