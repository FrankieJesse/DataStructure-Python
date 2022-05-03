from datastruct import datastruct
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# test for intrestedPython
def IntrestPythonMain() :
    testString = 'helloFrankieAndJesse, how are you'
    print("the string bing used center(5, '*') is : ", testString.center(40, '*'), 'the width of the string is : ', len(testString))

def DictionaryValue() :
    dictA = {1: 'hello', 2 : 'world', 3: 456, 4 : 'how'}
    for keys in dictA.keys() :
        if dictA.get(keys, default=0xffff) == 0xffff :
            print('hellowrold')
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    # IntrestPythonMain()
    datastruct.data_struct()
