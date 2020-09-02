import sympy as sp
from sympy.plotting import plot
from sympy import simplify, solve, symbols
import math as math
import numpy as np
from math import exp
from math import sin
from math import sqrt
from scipy.optimize import linprog

#Использую SymPy чтобы пользователь мог заносить функцию при запросе
#макс размерность задачи = 10
x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = symbols('x1 x2 x3 x4 x5 x6 x7 x8 x9 x10')

#Здесь lambdaAK это и есть Альфа
lambdaAK = sp.Symbol('lambdaAK')
print("Примечание:\n 1) Можно использовать только 'x1','x2','x3,...,x10 как переменную/неизвестную \n 2) все действия (+, -, /, *) такие же как и в обычном Python коде \n 3) степень обозначается как ** \n 4) exp(), sin(x), ln(x), sqrt(), Abs() \n 5) вместо pi использовать число 3.14 (Например, если надо ввести pi/4, то вводим 0.785) \n 6) Условие x1/2... >=0 вводить не надо, оно уже стоит автоматически")
f_x = input('Теперь введите функцию сюда и нажмите "Enter": ')
f_x = sp.sympify(f_x)

#Ввод данных
number = int(input('Введите размерность задачи: '))
aa0 = list(map(float, input("введите координаты начальной точки через пробел: ").split()))
eps_x_all = float(input("введите погрешность по аргументу eps_x: "))
eps_y_all = float(input("введите погрешность по функции eps_y: "))

#Сюда вводим все коэффициенты при А, а также в конце значение b для первого неравенства
print("\nПриведите неравенство к виду Ах <= b\nТеперь сперва введите только коэффициенты при x (т.е. А), начиная с x1 и далее по порядку и в конце введите значение b. Все вводим через пробел")
user_list_1 = list(map(float, input().split()))

AB=[]
AB.append(user_list_1)
count_1=1

#все остальные неравенства вводим дополнительно сюда
Answer = "Yes"
while Answer != "No":
    print("\nЕсли нужно ввести еще одно условие введите:Yes, если нет то введите:No ")
    Answer = input()
    if Answer == "Yes":
        user_list = list(map(float, input("введите еще раз только коэффициенты при x: ").split()))
        AB.append(user_list)
        count_1=count_1+1

#AB_x_all собирает все коэффициенты при А, чтобы в дальнейшем использовать для симплекс метода
AB_x_all=[]
for j in range(0,count_1):
    AB_x=[]
    for i in range(0,number):
        AB_x.append(AB[j][i])
    AB_x_all.append(AB_x)
AB_x_all=np.array(AB_x_all)

#AB_b_all собирает все b, чтобы в дальнейшем использовать для симплекс метода
AB_b_all=[]
for j in range(0,count_1):
    AB_b=[]
    for i in range(number,number+1):
        AB_b.append(AB[j][i])
    AB_b_all.append(AB_b)
AB_b_all=np.array(AB_b_all)

#Присваиваю изначальное значение чтобы loop заработал для 0 итерации
eps_x_stop_all = 100.0
eps_y_stop_all = 100.0

#создаю ключи исходя из рамзмерности задачи
list_x=[x1, x2, x3, x4, x5, x6, x7, x8, x9, x10]
keys=[]
for i in range(0,number):
    keys.append(list_x[i])

#Вычисление производной для всех аргументов исходя из рамзмерности задачи
proizv=[]
for i in keys:
    proizv.append(sp.Derivative(f_x, i).doit())

#начало loopa
k=0
while ((eps_y_stop_all > eps_y_all) or (eps_x_stop_all > eps_x_all)):
    aa=[]
    
    for i in range(0,number):
        aa.append(aa0[i])
    
    vector_x0=np.array(aa)
    
    #создаю dictionary чтобы вставить внутрь производной
    dict2={}
    dict2=dict(zip(keys,aa))
    
    #высчитываем значение функции    
    fx_x=f_x.evalf(subs=dict2)
    
    #Подставляем и решаем производную для всех аргументов
    solution=[]
    for i in range(0,number):
        solution.append(proizv[i].evalf(subs=dict2))
    
    #вычисляем вектор fx для проверки того продолжать вычисления либо нет
    vector_fx=np.array(solution)
    vector_fx_norma = math.sqrt((vector_fx*vector_fx).sum())
    
    print("Итерация",k)
    print("xk",vector_x0)
    print("fx_k",fx_x)
    print("vector_fx_k",vector_fx)
    print("Норма vector_fx_k",vector_fx_norma)
    
    if vector_fx_norma > eps_y_all:
        
        print("Так как Норма vector_fx_k=",vector_fx_norma,">",eps_y_all,", то продолжаем вычисления")
        print("Для этого вычислим значение альфы, найдем новое приближение х и проверим условия останова итерационного процесса eps_x и eps_y")
        #использую симплекс метод для решения системы
        res= linprog(solution, A_ub=AB_x_all, b_ub=AB_b_all, bounds=(0,None))
        reshenie = res.x
        reshenie=np.array(reshenie)
        
        vector_f_lambda=vector_x0 + lambdaAK*(reshenie-vector_x0)
        
        #создаю еще один dictionary чтобы вставить в уравнение с лямбдой
        dict3={}
        dict3=dict(zip(keys,vector_f_lambda))    
        solution_fx=simplify(f_x.subs(dict3))
        
        #Вычисление lambda (в нашем случае Альфы)
        proizv_lambda=sp.Derivative(solution_fx, lambdaAK).doit()
        proizv_lambda_solve=solve(proizv_lambda)
        
        #границы решения [0:1]
        if proizv_lambda_solve[0] > 1:
            proizv_lambda_solve[0] = 1
        if proizv_lambda_solve[0] < 0:
            proizv_lambda_solve[0] = 0
            
        vector_x1=vector_x0 + proizv_lambda_solve[0]*(reshenie-vector_x0)
        
        for i in range(0,number):
            aa0[i]=vector_x1[i]
        
        #обновляю dictionary чтобы вставить внутрь производной
        dict2={}
        dict2=dict(zip(keys,aa0))
        
        #высчитываем значение функции    
        fx_x_1=f_x.evalf(subs=dict2)
        
        
        vector_diff=vector_x1 - vector_x0
        eps_x_stop_all = math.sqrt((vector_diff*vector_diff).sum())
        eps_y_stop_all=abs(fx_x_1 - fx_x)
        
        print("Альфа",proizv_lambda_solve[0])
        print("xk+1",vector_x1)
        print("fx_k+1",fx_x_1)        
        print("eps_x",eps_x_stop_all)
        print("eps_y",eps_y_stop_all)
        if eps_x_stop_all > eps_x_all and eps_y_stop_all > eps_y_all:
            k=k+1
    else:
        break

fx_x=f_x.evalf(subs=dict2)

length_eps_x=len(str(eps_x_all).split('.')[1])
length_eps_y=len(str(eps_y_all).split('.')[1])
fx_x = round(fx_x, length_eps_y)
vectorr=np.around(vector_x1.astype(np.double), length_eps_x)

print("\nОбщее количество итераций",k+1)
print("Финальное значение аргумента",vectorr)
print("Финальное значение функции",fx_x)