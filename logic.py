import string
import itertools
import sys 

VARS = string.ascii_lowercase
OPS = {
        "|" : (lambda a, b: a or b),
        "&" : (lambda a, b: a and b),
        "~" : (lambda a: not(a)),
        "/" : (lambda a, b: xor(a,b)),
        "=" : (lambda a, b: a == b),
        "-" : (lambda a, b: impl(a,b))
               
    }

def validate(expr):
    """sprawdza poprawność syntaktyczną wyrażenia"""
    state = 0  # 0 - oczekiwany nawias ( lub zmienna lub '~', 1 - oczekiwany nawias ) lub operator, 2 = ( lub zmienna
    par_count = 0     # licznik nawiasów 
    for char in expr:
        if char == " ":
            continue
        if state==0:
            if (char in VARS or char.isdigit()): state = 1 
            elif char == "(":
                par_count += 1
            elif char == '~':
                state = 2
            else:
                return False
        elif state == 1:
            if (char in OPS and not(char=='~')): state = 0
            elif char == ")":
                par_count -= 1
            else:
                return False
        else:
            if (char in VARS or char.isdigit()): state = 1 
            elif char == "(":
                par_count += 1
                state = 0
            else:
                return False
            
        if par_count < 0: return False
    return par_count == 0 and state==1


def countvars(expr):
    """liczy ilosc zmiennych w wyrazeniu logicznym expr"""
    dict_of_var = {}
    for char in expr:
        if char in VARS:
            dict_of_var[char]=0
            
    return dict_of_var

def makecount(digit,nums):
    """zapisuje cyfre w postaci bin i dodaje ilosc zer zeby dosctac kombinacje o nums cyfrach 0 i 1 """
    expr = str(bin(digit))[2:]
    lenth= len(expr)
    for i in range(nums-lenth):
        expr = '0' + expr
    
    return expr

def xor(a,b):
    """alternatywy wykluczającej"""
    if (a == 1 and b == 1):
        return 0
    else:
        return a or b
    
def impl(a,b):
    """implikacja"""
    if (a==1 and b == 0):
        return 0
    else:
        return 1

def evaly(expr, dicty):
    """expr - wyrazenie logiczne w onp. W dicty zmienne i ich wartosci. Funkcja liczy  """
    stack = []
    for i in expr:
        if (i in OPS and not(i == '~')):
            arg1 = stack.pop()
            arg2 = stack.pop()
            if(isinstance(arg1,int)==True):
                arg1 = arg1
            elif (arg1.isdigit() ==True):
                arg1 = int(arg1)
            else:
                arg1 = dicty[arg1] 
            if(isinstance(arg2,int)==True):
                arg2 = arg2
            elif (arg2.isdigit()==True):
                arg2 = int(arg2)
            else:
                arg2= dicty[arg2]
            result = OPS[i](arg2,arg1)
            stack.append(result)
        elif (i in OPS and i == '~'):
            arg1 = stack.pop()
            if(isinstance(arg1,int)==True):
                arg1 = arg1
            elif (arg1.isdigit() ==True):
                arg1 = int(arg1)
            else:
                arg1 = dicty[arg1] 
            result = OPS[i](arg1)
            stack.append(result)
            
        else:
            stack.append(i)
    return stack.pop()
    

def rpe(expr):
    """sprowadza wyrazenie logiczne expr do onp"""
    prioritets = {'~' : 4,'&' : 3, '|' : 2, '=' : 1, '/': 2, '-': 1 }
    string = ""
    stack = []
    for i in expr:
        if i == " ":
            continue
        elif i in VARS:
            string = string + i 
        elif i.isdigit():
            string = string + i
        elif i == "(" or i == '~':
            stack.append(i)
        elif i == ")":
            a = stack.pop()
            while  a != "(":
                string = string + a
                a = stack.pop()
        else:
            while ((stack) and stack[len(stack)-1] in prioritets.keys() and (prioritets[stack[len(stack)-1]] > prioritets[i])):
                a = stack.pop()
                string = string + a
            stack.append(i)
        
    while(stack):
        string = string + stack.pop()
    return string
            
def slip(dicty):
    """slownik dicty w ktorym wszystkie kombinacje logiczne. 
    Przechodzimy i jezele dwa wyrazenia roznia sie tylko w jednym miejscu, 
    to sklejamy.Zamiast tego miejsca '*' """
    sliped = {}
    num = 0
    flag = [0 for i in range(len(dicty))]
    
    for i in range(len(dicty)-1):
        for j in range(i+1, len(dicty)):
            str1=dicty[i]
            str2=dicty[j]
            n=q=0
            for a,b in zip(str1,str2):
                if not(str1[a]==str2[b]):
                    n = n + 1
                    q = a
                
            if (n == 1):
                flag[i] = 1
                flag[j] = 1
                check = dict(str1)
                check[q] = '*'
                if not(check in sliped.values()):
                    sliped[num] = check
                    num +=  1
    for i in range(len(flag)):
        if flag[i] == 0:
            sliped[num] = dicty[i]
            num +=  1
    
    return sliped      

def check(first, second):
    """sprawda czy wyrazenie logiczne z first jest zawierane 
    w wyrazeniu logicznym second"""
    for i, j in zip(first, second):
        if second[j] == '*':
            continue
        elif second[j] == first[i]:
            continue
        else:
            return False
    return True

def checkfalse(tabl):
    """sprawdzamy, czy cala tablica tabl jest wypiewniona Falsami"""
    for i in range(len(tabl)):
        if not(tabl[i] == False):
            return False
    return True

def writingout(combinations, tabl):
    """wypisanie tych kombinacji ze slownika combinations, 
    gdzie w tabl jest odpowiednia 1 """
    newdict = {}
    for i, j in zip(combinations, tabl):
        if j == 1:
            newdict[i]=combinations[i] 
    string = ""
    num = 0
    for i in newdict:
        s = newdict[i]
        for j in s:
            if s[j]==1:
                string = string + j
            elif s[j]==0:
                string = string  + j + '\''
        num = num + 1
        if num < len(newdict):
            string +=  " " + "OR" + " "
    return string
                
    
    
def quine(start, finish):
    """slownik start zawiera wszystkie poczatkowe wyrazenia logiczne, 
    ktore musza byc pokryte najmniejsza iloscia kombinacji z slownika finish"""    
    tablstart = [0 for i in range(len(start))]
    tablfinish = [0 for i in range(len(finish))]
    for i in range(len(start)):
        for j in range(len(finish)):
            if check(start[i], finish[j]) == True:
                tablstart[i] +=  1
    for i in range(len(tablstart)):
        if tablstart[i] == 1:
            for j in range(len(finish)):
                if check(start[i],finish[j]):
                    for k in range(len(start)):
                        if check(start[k], finish[j]):
                            tablstart[k] = False
                    tablfinish[j] = 1
                    break
    
    if checkfalse(tablstart):
        return writingout(finish, tablfinish)
    num = 0
    for i in range(len(tablfinish)):
        if tablfinish[i] == 0:
            num +=  1
    l = list(itertools.product(range(2), repeat=num))
    tablstartcopy = tablstart
    counter = 1
    while not(checkfalse(tablstartcopy)):
        tablstartcopy = tablstart
        tablfinishcopy = tablfinish
        setik = l[counter]
        num = 0
        for i in range(len(tablfinishcopy)):
            if tablfinishcopy[i] == 0:
                tablfinishcopy[i] = setik[num]
                if setik[num]==1:
                    for j in range(len(start)):
                        if not(tablstartcopy[j]==False):
                            if check(start[j], finish[i]):
                                tablstartcopy[j] = False
                num +=  1
        counter +=  1 
        
             
    return writingout(finish, tablfinishcopy)

def main(expr):
    if not(validate(expr)):
        print("You gave wrong expr!\n & : koniunkcji, | : alternatywy,  / : alternatywy wykluczającej, ~ : negacji, - : implikacji, = : równoważności")
        exit()
    chary = countvars(expr)
    num_of_combi = 2**len(chary)
    index = 0
    start_dict = {}
    for i in range(num_of_combi):
        number = makecount(i, len(chary))
        for i,j in zip(chary,number):
            chary[i]=int(j)
        onp = rpe(expr)
        answer =  evaly(onp, chary)
        if answer == 1:
            start_dict[index]=dict(chary)
            index += 1        
    start_dict_copy = dict(start_dict)
	
    print(start_dict)
    if len(start_dict)==num_of_combi:
        result = True
        print(result)
        return result
        
    if len(start_dict)==0:
        result = False
        print(result)
        return result
    for i in range(len(chary)):
        finish_dict = slip(start_dict_copy)            
        start_dict_copy = finish_dict  
    result = quine(start_dict, finish_dict)
    print(result)
    
    return result

	
if __name__ == "__main__":
	main(sys.argv[1])
