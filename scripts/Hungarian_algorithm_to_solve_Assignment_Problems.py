import math as math
import numpy as np
#from numpy import transpose

#Примечание: Отмеченный нулевой элемент - 99999.99999, а зачеркнутый нулевой элемент - 88888.88888. При необходимости их можно изменить здесь
otme4en = 99999.99999
za4erknut = 88888.88888

#найти первую строку с мин кол-вом нулей
def find_row(matrix):
    #подсчет количества нулей по строкам
    count_zero=np.count_nonzero(matrix == 0, axis=1)
    if max(count_zero) == 0:
        index = 1000000
    else:
        #найти мин число не учитывая нулей
        min_value_2 = np.min(count_zero[np.nonzero(count_zero)])
        #найти первый индекс с мин числом, если таковых несколько
        iter=0
        for i in count_zero:
            if i == min_value_2:
                index=iter
                break
            iter=iter+1
    return index

#найти первую столбец с нулем в найденной строке
def find_col(matrix, index_row, n):
    for i in range (0, n):
        if matrix[index_row][i] == 0:
            index = i
            matrix[index_row][i]=otme4en
            break
    return index

#зачеркнуть нули внутри строки
def cross_row(matrix, index_row, index_col, n):
    for i in range(index_col+1,n):
        if matrix[index_row][i] == 0:
            matrix[index_row][i] = za4erknut

#зачеркнуть нули внутри столбца
def cross_col(matrix, index_row, index_col, n):
    for i in range(0,n):
        if matrix[i][index_col] == 0:
            matrix[i][index_col] = za4erknut
            
#найти все строки c перечеркнутыми нулями            
def count_non_zero(matrix):
    count_zero=np.count_nonzero(matrix == otme4en, axis=1)
    iter=0
    row=[]
    for i in count_zero:
        if i == 0:
            row.append(iter)
        iter=iter+1
    return row
    
#найти все строки и столбцы для перчеркивания
def poisk(matrix, non_zero, n):
    column=[]
    row=[]
    a=0
    b=0
    diff_1 = 100
    diff_2 = 100
    row=list(non_zero)
    while ((diff_1 != 0) or (diff_2 != 0)):
        column = []
        a0=a
        b0=b
        for i in row:
            for j in range(0,n):
                if matrix[i][j] == za4erknut:
                    column.append(j)
        row=list(non_zero)
        for k in column:
            for l in range(0, n):
                if matrix[l][k] == otme4en:
                    row.append(l)
        a=len(column)
        b=len(row)
        diff_1=a0-a
        diff_2=b0-b
    return row, column
    
print("Данная программа решает задачу о назначениях Венгерским методом")
print("Примечание: Т.к. отметить или зачеркнуть нули я не смог, то сделал следующее:\nОтмеченный нулевой элемент - 99999.99999, а зачеркнутый нулевой элемент - 88888.88888")

print("введите размерность задачи")
n = int(input('Введите размерность задачи: '))
#n=4
#загрузка матрицы с текстового файла (числа должны быть отделены запятой)
matrix_load=np.loadtxt("matrix_for_Hungarian_algorithm.txt", delimiter=',')
print("\nНиже загруженная матрица")
print(matrix_load)

print("\nЭтап 1. Получение нулей в каждой строке")

#вариант второй для нахождения мин по строкам
min_row=matrix_load.min(1).reshape(-1,1)
print("\nНаходим наименьшее значение в каждой строке:\n",min_row)

#вычитаем из каждого столбца соответсвующее значение min_row
matrix_new=matrix_load-min_row
print("\nВычитаем из каждого столбца соответсвующее значение из предыдущего вектора:\n",matrix_new)

#Нахождения мин по столбцам
min_col=matrix_new.min(0)
print("\nНаходим наименьшее значение в каждом столбце:\n",min_col)

#вычитаем из каждого столбца соответсвующее значение min_row
matrix_to_change = matrix_new-min_col
print("\nВычитаем из каждой строки соответсвующее значение из предыдущего вектора:\n",matrix_to_change)

matrix = matrix_to_change.copy()

number_of_zeros = 0

#здесь начинается луп
#____________________________________________________________________________________________________________________________________

print("\nЭтап 2. Нахождение оптимального решения")
iteration=1
while number_of_zeros != n:
    print("\nИтерация:", iteration)
    #отметить все нули и перечеркнуть оставшиеся
    for i in range(0,n):
        index_row=find_row(matrix)
        if index_row != 1000000:
            print("\nНайти первую строку с минимальным числом нулей")
            print(index_row)
            index_col=find_col(matrix, index_row, n)
            cross_row(matrix, index_row, index_col, n)
            cross_col(matrix, index_row, index_col, n)
            print("\nОтметить первый ноль в текущей строке (99999.99999), остальные нули в текущих строке и столбце зачеркнуть (88888.88888)", "\n", matrix)
        
    print("\nПромежуточная матрица ", "\n", matrix)
    #Количество отмеченных нулей в матрице
    number_of_zeros = np.count_nonzero(matrix == otme4en)
    print("\nКоличество отмеченных в таблице нулей:", number_of_zeros)
    
    #Если количество отмеченных нулей в матрице меньше размерности задачи то делаем доп действия
    if number_of_zeros != n:
        print("\nЗначит решение НЕоптимальное и переходим к этапу 3")
        print("\nЭтап 3. Поиск минимального набора строк и столбцов, содержащих нули")
        non_zero=count_non_zero(matrix)
        print("\nОтметить все строки, в которых нет ни одного отмеченного нуля\n",non_zero)
        rows, cols = poisk(matrix, non_zero, n)
        print("\nЗатем итеративно выполняем два действия:\n1) В отмеченных строках отмечаем все столбцы, содержащие перечеркнутые нули\n2) В отмеченных столбцах отмечаем все строки, содержащие отмеченные нули")
        print("\nВсе отмеченные строки и столбцы указаны ниже\nИндексы строк", rows,"\nИндексы столбцов",cols)
        print("\nПосле этого зачеркиваем каждую непомеченную строку и каждый помеченный столбец и переходим к этапу №4")
        #найти неотмеченные столбцы зная отмеченные (cols)
        orig_rows=np.arange(n)
        diff_row = [i for i in orig_rows if i not in rows]
        diff_col = [i for i in orig_rows if i not in cols]
    
        #используем отмеченные строки (rows) и неотмеченные столбцы (diff_col)
        #найти минимум среди отмеченных строк и неотмеченных столбцов
        all_mins=[]
        for m in rows:
            array=matrix_to_change[[m],[diff_col]]
            all_mins.append(np.min(array[np.nonzero(array)]))
        min_value_3=min(all_mins)  
        print("\nЭтап 4. Перестановка некоторых нули")
        print("\nОпределяем наименьшее число из тех клеток, через которые не проведены прямые (не зачеркнуты):", min_value_3)
        
        #отнимаем и прибавляем мин значение
        matrix = matrix_to_change.copy()
        for m in rows:
            for p in diff_col:
                matrix[m][p] = matrix[m][p] - min_value_3
        for m in diff_row:
            for p in cols:
                matrix[m][p] = matrix[m][p] + min_value_3
        print("\nЭто число вычитаем из каждого числа невычеркнутых столбцови прибавляем к каждому числу вычеркнутых строк в вычеркнутых столбцах:\n",matrix)
        print("\nИ делаем следующую итерацию для нахождения оптимального решения (т.е. возвращаемся к этапу 2)")
    else:
        print("\nЗначит решение оптимальное и находим финальное решение")
    iteration=iteration+1

#нахождение финального решения
print("\nФинальная матрица ", "\n", matrix)
result = np.where(matrix == otme4en)

matrix = matrix_load.copy()
value = []
for q in range(0,n):
    value.append(matrix[result[0][q]][result[1][q]])

summation=np.sum(value)
print("\nЗначения оптимального решения:",value)
print("\nСумма значений оптимального решения:",summation)