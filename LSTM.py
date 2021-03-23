import numpy
import scipy.special
import re
import operator


# определение класса нейронной сети
class LSTM:

    # инициализировать нейронную сеть
    def __init__(self, cellcount, learningrate):
        # задать количество LSTM ячеек равную максимальной длине SQL-запроса
        self.ccount = cellcount
        # инициализируем Веса в диапазоне от -1 до 1
        self.W_a = 0.01 * numpy.random.sample()
        self.U_a = 0.01 * numpy.random.sample()
        self.b_a = 0.01 * numpy.random.sample()

        self.W_i = 0.01 * numpy.random.sample()
        self.U_i = 0.01 * numpy.random.sample()
        self.b_i = 0.01 * numpy.random.sample()

        self.W_f = 0.01 * numpy.random.sample()
        self.U_f = 0.01 * numpy.random.sample()
        self.b_f = numpy.random.sample() + 0.5  # особый случай

        self.W_o = 0.01 * numpy.random.sample()
        self.U_o = 0.01 * numpy.random.sample()
        self.b_o = 0.01 * numpy.random.sample()

        # коэффициент обучения
        self.lr = learningrate

        # функции активации
        self.activation_function_sigm = lambda x: scipy.special.expit(x)
        self.activation_function_tanh = lambda x: numpy.tanh(x)

        # производные функций активации
        self.sigm_drv = lambda x: scipy.special.expit(x) * (1 - scipy.special.expit(x))
        self.tanh_drv = lambda x: 1.0 / (numpy.tanh(x) * numpy.tanh(x))

        self.dictionary = dict()
        self.false_positive = 0  # ошибка первого рода
        self.false_negative = 0  # ошибка второго рода
        pass

    # тренировка нейронной сети
    def train(self, inputs_list, reference_value):
        # ПРЯМОЙ ПРОХОД
        # делаем прямой проход и сохраняем значение каждого вентиля на каждом шаге

        # устанавливаем начальное значение памяти(c) и выхода(h)
        out = 0
        state = 0

        # создаем массивы для хранения значений
        sF = []  # история состояний гейта памяти
        sI = []  # история состояний гейта обновления
        sO = [] # история состояний гейта выхода
        sA = []  # история состояний обновлений памяти
        sState = [] # история состояний памяти
        sOut = [] # история выходов скрытого слоя

        for t in range(self.ccount):
            # candidate cell state (z это c')
            A = self.activation_function_tanh(self.W_a * inputs_list[t] + self.U_a * out + self.b_a)
            sA.append(A)

            # input gate
            I = self.activation_function_sigm(self.W_i * inputs_list[t] + self.U_i * out + self.b_i)
            sI.append(I)

            # forget gate
            F = self.activation_function_sigm(self.W_f * inputs_list[t] + self.U_f * out + self.b_f)
            sF.append(F)

            # output gate
            O = self.activation_function_sigm(self.W_o * inputs_list[t] + self.U_o * out + self.b_o)
            sO.append(O)

            # cell state
            state = F * state + I * A
            sState.append(state)

            # block output
            out = O * self.activation_function_tanh(state)
            sOut.append(out)

        # for t in range(self.ccount):
        # print('гейт памяти на шаге',t,sgf[t])
        # print('гейт обновления на шаге',t,sgi[t])
        # print('гейт выхода на шаге',t,sgo[t])
        # print('гейт состояния обновления на шаге',t,sZ[t])
        # print('состояние памяти на шаге',t,sC[t])
        # print('выход на шаге',t,sH[t])

        # ОБРАТНЫЙ ПРОХОД
        # вычисляем ошибки в каждый момент времени начиная с конца

        # создаем массивы для хранения ошибок на каждом шаге

        err_f = numpy.zeros(self.ccount) # история состояний гейта памяти
        err_i = numpy.zeros(self.ccount) # история состояний гейта обновления
        err_o = numpy.zeros(self.ccount) # история состояний гейта выхода
        err_a = numpy.zeros(self.ccount)  # история состояний обновлений памяти
        err_state = numpy.zeros(self.ccount) # история состояний памяти
        err_out = numpy.zeros(self.ccount) # история выходов скрытого слоя

        # начинаем с последнего момента времени
        t = self.ccount - 1

        err_out[t] = sOut[t] - reference_value
        #print(sOut[t])
        #print("среднеквадратичная ошибка:", err_out[t] ** 2)
        err_state[t] = err_out[t] * sO[t] * (1 - self.activation_function_tanh(sState[t]) ** 2)
        err_a[t] = err_state[t] * sI[t] * (1 - sA[t] ** 2)
        err_i[t] = err_state[t] * sA[t] * (1 - sI[t])
        err_f[t] = err_state[t] * sState[t - 1] * sF[t] * (1 - sF[t])
        err_o[t] = err_out[t] * self.activation_function_tanh(sState[t]) * sO[t] * (1 - sO[t])

        for t in range((self.ccount - 1) - 1, 0, -1):
            err_out[t] = sOut[t] - reference_value + self.U_a * err_a[t + 1] + self.U_f * err_f[t + 1] + self.U_i * \
                         err_i[t + 1] + self.U_o * err_o[t + 1]

            err_state[t] = err_out[t] * sO[t] * (1 - self.activation_function_tanh(sState[t]) ** 2) + err_state[t + 1] * \
                           sF[t + 1]

            err_a[t] = err_state[t] * sI[t] * (1 - sA[t] ** 2)
            err_i[t] = err_state[t] * sA[t] * (1 - sI[t])
            err_f[t] = err_state[t] * sState[t - 1] * sF[t] * (1 - sF[t])
            err_o[t] = err_out[t] * self.activation_function_tanh(sState[t]) * sO[t] * (1 - sO[t])

        t = 0

        err_out[t] = sOut[t] - reference_value + self.U_a * err_a[t + 1] + self.U_f * err_f[t + 1] + self.U_i * err_i[
            t + 1] + self.U_o * err_o[t + 1]

        err_state[t] = err_out[t] * sO[t] * (1 - self.activation_function_tanh(sState[t]) ** 2) + err_state[t + 1] * sF[
            t + 1]

        err_a[t] = err_state[t] * sI[t] * (1 - sA[t] ** 2)
        err_i[t] = err_state[t] * sA[t] * (1 - sI[t])
        err_f[t] = 0
        err_o[t] = err_out[t] * self.activation_function_tanh(sState[t]) * sO[t] * (1 - sO[t])

        # вычисляем значения градиента для всех весов

        dW_a = 0
        dU_a = 0
        db_a = 0

        dW_i = 0
        dU_i = 0
        db_i = 0

        dW_f = 0
        dU_f = 0
        db_f = 0

        dW_o = 0
        dU_o = 0
        db_o = 0

        for t in range(self.ccount):
            dW_a += err_a[t] * inputs_list[t]
            dW_i += err_i[t] * inputs_list[t]
            dW_f += err_f[t] * inputs_list[t]
            dW_o += err_o[t] * inputs_list[t]

        for t in range(self.ccount - 1):
            dU_a += err_a[t + 1] * sOut[t]
            dU_i += err_i[t + 1] * sOut[t]
            dU_f += err_f[t + 1] * sOut[t]
            dU_o += err_o[t + 1] * sOut[t]

        for t in range(self.ccount): ##!!!
            db_a += err_a[t]
            db_i += err_i[t]
            db_f += err_f[t]
            db_o += err_o[t]

        # обновляем веса

        self.W_a -= self.lr * dW_a
        self.U_a -= self.lr * dU_a
        self.b_a -= self.lr * db_a

        self.W_i -= self.lr * dW_i
        self.U_i -= self.lr * dU_i
        self.b_i -= self.lr * db_i

        self.W_f -= self.lr * dW_f
        self.U_f -= self.lr * dU_f
        self.b_f -= self.lr * db_f

        self.W_o -= self.lr * dW_o
        self.U_o -= self.lr * dU_o
        self.b_o -= self.lr * db_o

        pass

    # опрос нейронной сети
    def query(self, inputs_list):
        # устанавливаем начальное значение памяти(c) и выхода(h)
        out = 0
        state = 0
        # выполняем расчёт для каждой LSTM ячейки ( на каждую ячейку подаётся одно число-обозначение токена)
        for i in range(self.ccount):
            # candidate cell state (z это c')
            A = self.activation_function_tanh(self.W_a * inputs_list[i] + self.U_a * out + self.b_a)
            # input gate
            I = self.activation_function_sigm(self.W_i * inputs_list[i] + self.U_i * out + self.b_i)
            # forget gate
            F = self.activation_function_sigm(self.W_f * inputs_list[i] + self.U_f * out + self.b_f)
            # output gate
            O = self.activation_function_sigm(self.W_o * inputs_list[i] + self.U_o * out + self.b_o)
            # cell state
            state = F * state + I * A
            # block output
            out = O * self.activation_function_tanh(state)
        return out

    def weigths_print(self):
        print(self.W_a, self.U_a, self.b_a)
        print(self.W_i, self.U_i, self.b_i)
        print(self.W_f, self.U_f, self.b_f)
        print(self.W_o, self.U_o, self.b_o)

    def activation_test(self):
        print(self.sigm_drv(2))
        print(self.tanh_drv(2))

    def train_all(self, data_list, number_examples, number_epochs):
        data_list_current = data_list[0:number_examples]
        #print(data_list_current)

        # Создаем частотный словарь
        frequency_dictionary = dict()

        # Создаем регулярку
        pattern = re.compile(r'(\w+|[\"=;\'\-*%)(,;@*?])')
        # Проходим по каждому запросу из выборки
        for query in data_list_current:
            # print(query)
            query = query[0:-2]
            tokens = re.findall(pattern, query)
            # print(result)
            # проходим в цикле по всем токенам запроса
            tokens_unique = numpy.unique(tokens)
            for token in tokens_unique:
                if token in frequency_dictionary:
                    frequency_dictionary[token][0] += 1
                else:
                    frequency_dictionary[token] = [1]

        # for key in frequency_dictionary:
        # print(key, frequency_dictionary[key][0])

        sorted_x = sorted(frequency_dictionary.items(), key=operator.itemgetter(1), reverse=True)

        # print(sorted_x[0][1][0])


        count = 1
        for i in sorted_x:
            self.dictionary[i[0]] = [count]
            count += 1

        #for key in dictionary:
            #print(key, dictionary[key][0])

        # мы сформировали словарь, теперь представим запросы в текстовой форме

        # задаем глобальный список со всеми значениями в обучающей выборке
        list_global = []
        # преобразуем каждый запрос в вектор в соответствии с dictionary и добавляем его в глобальный лист с маркером

        for query in data_list_current:
            # print(query)
            list_current = []
            is_malicious = query[-1]
            query = query[0:-2]
            tokens = re.findall(pattern, query)
            # print(result)
            # проходим в цикле по всем токенам запроса
            for token in tokens:
                if token in frequency_dictionary:
                    list_current.append(self.dictionary[token][0])
                else:
                    list_current.append(0)
            list_current.insert(0, int(is_malicious))
            list_global.append(list_current)

        # print(list_global)

        for (index, query) in enumerate(list_global):
            if (len(query) - 1 < self.ccount):
                for i in range(self.ccount - len(query) + 1):
                    list_global[index] += [0]
            elif (len(query) - 1 > self.ccount):
                list_global[index] = list_global[index][0:self.ccount + 1]

        #for i in list_global:
            #print(i)

        #нормировка
        # for (index, query) in enumerate(list_global):
        #     max_ = max(query)
        #     is_malicious = query[0]
        #     # print(max_)
        #     if (max_ != 0):
        #         list_global[index] = [x / max_ for x in query[1:]]
        #     list_global[index].insert(0, is_malicious)

        #print(list_global)

        # само обучение

        for i in range(number_epochs):
            for query in list_global:
                # print(query)
                reference_value = query[0]
                if(reference_value == 0):
                    reference_value = -1
                del query[0]
                # print(query)
                self.train(query, reference_value)
                query.insert(0, reference_value)
            #self.weigths_print()

    def query_all(self, path_to_training_validation):
        self.false_positive = 0  # ошибка первого рода
        self.false_negative = 0  # ошибка второго рода
        for key in self.dictionary:
            print(key, self.dictionary[key][0])

        data_file_validation = open(path_to_training_validation, 'r')
        data_list_validation = data_file_validation.readlines()
        data_file_validation.close()

        for (index, string) in enumerate(data_list_validation):
            data_list_validation[index] = string.rstrip('\n')  # убираем из строки символ перевода строки

        print(data_list_validation)

        # задаем глобальный список со всеми значениями в обучающей выборке
        list_global_validation = []
        # преобразуем каждый запрос в вектор в соответствии с dictionary и добавляем его в глобальный лист с маркером
        pattern = re.compile(r'(\w+|[\"=;\'\-*%)(,;@*?])')

        for query in data_list_validation:
            # print(query)
            list_current = []
            tokens = re.findall(pattern, query)
            # print(result)
            # проходим в цикле по всем токенам запроса
            for token in tokens:
                if token in self.dictionary:
                    list_current.append(self.dictionary[token][0])
                else:
                    list_current.append(0)
            list_global_validation.append(list_current)

        # print(list_global)

        for (index, query) in enumerate(list_global_validation):
            if (len(query) < self.ccount):
                for i in range(self.ccount - len(query)):
                    list_global_validation[index] += [0]
            elif (len(query) > self.ccount):
                list_global_validation[index] = list_global_validation[index][0:self.ccount]

        #НОРМИРОВКА
        # for (index, query) in enumerate(list_global_validation):
        #     max_ = max(query)
        #     # print(max_)
        #     if (max_ != 0):
        #         list_global_validation[index] = [x / max_ for x in query]

        vector = numpy.zeros(100)
        for i in range(len(vector)):
            if (i % 2 == 0):
                vector[i] = 1
        print(vector)

        for (index, i) in enumerate(list_global_validation):
            print(index, i)

        count = 0
        for (index, i) in enumerate(list_global_validation):
            result = self.query(i)
            result_round = 0
            print(result)
            if (result < 0.0):
                result_round = 0
            else:
                result_round = 1
            if (int(vector[index]) != result_round):
                count += 1
                if (int(vector[index]) == 1):  # Ошибка второго рода
                    self.false_negative = self.false_negative + 1
                else:
                    self.false_positive = self.false_positive + 1
        print(count)
        print("Ошибка первого рода:", self.false_positive)
        print("Ошибка второго рода:", self.false_negative)
        pass