import sympy as sp
from sympy.plotting import plot
from sympy import simplify, solve, symbols, re, im, E, I
import math as math
import numpy as np
from math import exp
from math import sin
from math import sqrt
from scipy.optimize import linprog

#функция для определения вогнутости или выпуклости функции
def opredelenie(func, keys, number):
    #Разберемся какая матрица вогнутая, а какая выпуклая
    Hessian=[]
    line1=[]
    for i in keys:
        line1=[]
        for j in keys:
            line1.append(sp.Derivative(func, i, j).doit())
        Hessian.append(line1)
    Hessian=np.array(Hessian)
    
    minors=[]
    for i in range(1, number+1):
        Hessian2=Hessian[0:i, 0:i]
        Hessian2=Hessian2.astype('float64')
        determinant=np.linalg.det(Hessian2)
        minors.append(determinant)
    
    print('\nФункция: {0}'.format(func))
    print("Ее матрица Гессе\n", Hessian)
    print("Угловые миноры матрицы Гессе\n", minors)
    
    function=0
    
    if min(minors) >= 0:
        print('все угловые миноры неотрицательны (>=0), поэтому функция ({0}) выпуклая'.format(func))
        function=1
        
    count_neg=0
    count_pos=0
    if function == 0:
        for i in range(0,number,2):
            if minors[i] <= 0:
                count_neg=count_neg+1
            if (i+1) <= (number-1):
                if minors[i+1] >= 0:
                    count_pos=count_pos+1
        if (count_neg+count_pos) == number:
            print('знаки угловых миноров чередуются, начиная с неположительного значения, поэтому функция ({0}) вогнутая'.format(func))
    return function

#Использую SymPy чтобы пользователь мог заносить функцию при запросе
#макс размерность задачи = 10
x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = symbols('x1 x2 x3 x4 x5 x6 x7 x8 x9 x10')
Nu1, Nu2, Nu3, Nu4, Nu5, Nu6, Nu7, Nu8, Nu9, Nu10 = symbols('Nu1 Nu2 Nu3 Nu4 Nu5 Nu6 Nu7 Nu8 Nu9 Nu10')
Nu1, Nu2, Nu3, Nu4, Nu5, Nu6, Nu7, Nu8, Nu9, Nu10 = symbols('Nu1 Nu2 Nu3 Nu4 Nu5 Nu6 Nu7 Nu8 Nu9 Nu10')
lambda1, lambda2, lambda3, lambda4, lambda5, lambda6, lambda7, lambda8, lambda9, lambda10 = symbols('lambda1 lambda2 lambda3 lambda4 lambda5 lambda6 lambda7 lambda8 lambda9 lambda10')
Nu=[Nu1, Nu2, Nu3, Nu4, Nu5, Nu6, Nu7, Nu8, Nu9, Nu10]
lambdaAK = sp.Symbol('lambdaAK')

#Ввод данных
number = int(input('Введите размерность задачи: '))

print("Примечание:\n 1) Можно использовать только 'x1','x2','x3,...,x10 как переменную/неизвестную \n 2) все действия (+, -, /, *) такие же как и в обычном Python коде \n 3) степень обозначается как ** \n 4) exp(), sin(x), ln(x), sqrt(), Abs() \n 5) вместо pi использовать число 3.14 (Например, если надо ввести pi/4, то вводим 0.785) \n 6) Условие x1/2... >=0 вводить не надо, оно уже стоит автоматически")
f_x = input('Теперь введите функцию сюда и нажмите "Enter": ')
f_x = sp.sympify(f_x)

#Сюда вводим все неравенства g(x)
print("\nВведите неравенство g(x)")
user_list_1 = input()
g_x=[]
g_x.append(user_list_1)
count_1=1

print("\nВведите знак 'bolshe' или 'menshe' для g(x), в зависимости от того g(x)>=0 или g(x)<=0")
user_list_4 = input()
znaki=[]
znaki.append(user_list_4)

#все остальные неравенства вводим дополнительно сюда
Answer = "Yes"
while Answer != "No":
    print("\nЕсли нужно ввести еще одно неравенство g(x) введите:Yes, если нет то введите:No ")
    Answer = input()
    if Answer == "Yes":
        user_list = input("введите еще раз неравенство g(x): ")
        g_x.append(user_list)
        count_1=count_1+1
        user_list_5 = input("введите еще раз знак 'bolshe' или 'menshe' для g(x), в зависимости от того g(x)>=0 или g(x)<=0: ")
        znaki.append(user_list_5)

#Сюда вводим все h(x)
print("\nНеобходимо ли ввести h(x)? Введите: Yes если Да, если нет то введите No ")
answer_hx = input()
count_hx=0
if answer_hx == "Yes":
    print("\nВведите h(x)")
    user_list_2 = input()
    h_x=[]
    h_x.append(user_list_2)
    count_hx=1
    #все остальные неравенства вводим дополнительно сюда
    Answer = "Yes"
    while Answer != "No":
        print("\nЕсли нужно ввести еще одно неравенство h(x) введите:Yes, если нет то введите:No ")
        Answer = input()
        if Answer == "Yes":
            user_list_3 = input("введите еще раз неравенство h(x): ")
            h_x.append(user_list_3)
            count_hx=count_hx+1
    h_x = sp.sympify(h_x)

f_x = sp.sympify(f_x)
g_x = sp.sympify(g_x)

#создаю ключи исходя из размерности задачи
list_x=[x1, x2, x3, x4, x5, x6, x7, x8, x9, x10]
keys=[]
for i in range(0,number):
    keys.append(list_x[i])

list_Nu=[Nu1, Nu2, Nu3, Nu4, Nu5, Nu6, Nu7, Nu8, Nu9, Nu10]
keys_Nu=keys.copy()
for i in range(0,count_1):
    keys_Nu.append(list_Nu[i])

list_lambda=[lambda1, lambda2, lambda3, lambda4, lambda5, lambda6, lambda7, lambda8, lambda9, lambda10]
keys_lambda=keys_Nu.copy()
for i in range(0,count_hx):
    keys_lambda.append(list_lambda[i])
    
#Вычисление производной для всех аргументов исходя из размерности задачи
proizv=[]
for i in keys:
    proizv.append(sp.Derivative(f_x, i).doit())

#Вычисление производной для всех аргументов и для всех уравнений типа g(x)исходя из размерности задачи    
proizv_g_x=[]
line2=[]
for i in keys:
    line2=[]
    for j in range(0,count_1):
        line2.append(sp.Derivative(g_x[j], i).doit())
    proizv_g_x.append(line2)

#Вычисление производной для всех аргументов и для всех уравнений типа h(x)исходя из размерности задачи  
proizv_h_x=[]
line3=[]
for i in keys:
    line3=[]
    for j in range(0,count_hx):
        line3.append(sp.Derivative(h_x[j], i).doit())
    proizv_h_x.append(line3)

#Собираем систему уравнений для решения    
Uravnenie_all=[]
for i in range(0,number):
    uravnenie=proizv[i]
    for j in range(0,count_1):
        if znaki[j] == "bolshe":
            uravnenie=uravnenie - Nu[j]*proizv_g_x[i][j]
        else:
            uravnenie=uravnenie + Nu[j]*proizv_g_x[i][j]
    for k in range(0,count_hx):
        uravnenie=uravnenie+list_lambda[k]*proizv_h_x[i][k]
    Uravnenie_all.append(uravnenie)

for j in range(0,count_1):
    expr=Nu[j]*g_x[j]
    Uravnenie_all.append(expr)
    
for j in range(0,count_hx):
    expr2=list_lambda[j]*h_x[j]
    Uravnenie_all.append(expr2)

print("\nСистема уравнений или условия Куна-Таккера имеют следующий вид (при этом Nu1, Nu2 ,... >= 0 и все лямбды имеют произвольный знак)\n", Uravnenie_all)

#Решение системы уравнений дает множество решений, далее мы их будем фильтровать
Solution=solve((Uravnenie_all), dict=True)

#избавляемся от решений с мнимыми числами
Non_imaginary=[]
count_imag=0
for i in range(len(Solution)):
    count_imag=0
    for j in range(0,len(keys_lambda)):
        if im(Solution[i][keys_lambda[j]]) != 0:
            count_imag=count_imag+1
    if count_imag == 0:
        Non_imaginary.append(Solution[i])

#Находим решения где все x и Nu >= 0
count_Nu=0
Non_zero_Nu=[]
for i in range(0,len(Non_imaginary)):
    count_Nu=0
    for j in range(0,len(keys_Nu)):
        if Non_imaginary[i][keys_Nu[j]] < 0:
            count_Nu=count_Nu+1
    if count_Nu == 0:
        Non_zero_Nu.append(Non_imaginary[i])

#Если после фильтра решения остаются, то выводится решение, если нет то пишется что Решение для x не найдено
FINAL = 0
values=[]
count_NON=0
for i in range(0,len(Non_zero_Nu)):
    values=[]
    count_NON=0
    for j in range(0,number):
        values.append(Non_zero_Nu[i][keys_Nu[j]])
    dict_one={}
    dict_one=dict(zip(keys,values))
    #Подставляем и решаем производную для всех аргументов
    for i in range(0,count_1):
        solution=g_x[i].evalf(subs=dict_one)
        if (znaki[i] == "bolshe") and (solution < 0):
            count_NON=count_NON+1
        if (znaki[i] == "menshe") and (solution > 0):
            count_NON=count_NON+1
    if count_NON == 0:
        FINAL=dict_one

for i in range(0, number):
    FINAL[keys[i]]=FINAL[keys[i]].evalf()

if FINAL != 0:
    print("\nНайденные значения аргументов:", FINAL)
    fx_x=f_x.evalf(subs=FINAL)
    print("Найденное значение функции:", fx_x)
else:
    print("\nРешение не найдено")

print("\nТеперь посмотрим определленость всех функций f(x) и g(x)")

#Находим угловые миноры матриц Гессе
main_func=opredelenie(f_x, keys, number)
count_gx=0
for i in range (count_1):
    if znaki[i] == "bolshe" and (opredelenie(g_x[i], keys, number) == 0):
        count_gx=count_gx+1
    if znaki[i] == "menshe" and (opredelenie(g_x[i], keys, number) == 1):
        count_gx=count_gx+1

if (FINAL != 0) and (main_func == 1) and (count_gx == count_1):
    print("\nВсе условия Куна-Таккера соблюдены")
else:
    print("\nНЕ все условия Куна-Таккера соблюдены, поэтому условия оптимальности для данной задачи не выполнены")