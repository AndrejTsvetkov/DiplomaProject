import re
import numpy
import math

class NBC:

    # инициализировать классификатор
    def __init__(self):
        # зададим начальными значениями параметры для НБК
        self.P_M = 0.0
        self.P_NM = 0.0

        # объявляем частотный словарь
        self.frequency_dictionary = dict()

        self.pattern = re.compile(r'(\w+|[\"=;\'\-*%)(,;@*])')

        self.false_positive = 0 #ошибка первого рода
        self.false_negative = 0 #ошибка второго рода
        pass

    # фаза обучения
    def train(self, data_list, number_samples):
        # Считываем с файла обучающую выборку
        self.frequency_dictionary = dict()
        self.P_M = 0.0
        self.P_NM = 0.0
        #print(data_list)
        #print(self.P_M)
        #print(self.P_M)
        #data_file = open(path_to_training_dataset, 'r')
        #data_list = data_file.readlines()
        #data_file.close()

        # объявляем перемунную, которая будет содержать количество sql-инъекций
        sqli_cnt = 0
        # объявляем перемунную, которая будет содержать количество обычных запросов
        nsqli_cnt = 0

        data_list_current = data_list[0:number_samples]
        for (index, string) in enumerate(data_list_current):
                if string[-1] == "1":
                    sqli_cnt += 1
                else:
                    nsqli_cnt += 1

        # Отдельная обработка последней считанной строки
        #if data_list[-1][-1] == "1":
            #sqli_cnt += 1
        #else:
            #nsqli_cnt += 1

        # print(sqli_cnt)
        # print(nsqli_cnt)

        # Подсчитываем вероятности P(M) и P(NM)
        total_cnt = sqli_cnt + nsqli_cnt
        self.P_M = sqli_cnt / total_cnt
        self.P_NM = nsqli_cnt / total_cnt

        # Заполняем частотный словарь
        # Создаем регулярку
        # pattern = re.compile(r'(\w+|[\"=;\'\-*%)(,;@*])')
        # Проходим по каждому запросу из выборки
        for query in data_list_current:
            # print(query)
            is_malicious = query[-1]
            query = query[0:-2]
            tokens = re.findall(self.pattern, query)
            # print(result)
            # проходим в цикле по всем токенам запроса
            tokens_unique = numpy.unique(tokens)
            for token in tokens_unique:
                if token in self.frequency_dictionary:
                    if is_malicious == "1":  # строка а сравнивал с числом!!!!!!!
                        self.frequency_dictionary[token][1] += 1  # второй для вредоносных
                        # print("no")
                    if is_malicious == "0":
                        self.frequency_dictionary[token][0] += 1  # первый для нормальных
                        # print("yes")
                else:
                    if is_malicious == "1":
                        self.frequency_dictionary[token] = [0, 1]  # второй для вредоносных
                    if is_malicious == "0":
                        self.frequency_dictionary[token] = [1, 0]  # первый для нормальных

        # frequency_dictionary.items()
        # вычисляем частоты
        for key in self.frequency_dictionary:
            self.frequency_dictionary[key][0] /= nsqli_cnt
            self.frequency_dictionary[key][1] /= sqli_cnt
            # print(key, self.frequency_dictionary[key][0], self.frequency_dictionary[key][1])

        # частотный словарь сформирован
        pass

    # фаза опеределения вредоносности запроса
    def query(self, path_to_training_validation):
        self.false_positive = 0 #ошибка первого рода
        self.false_negative = 0 #ошибка второго рода

        data_file_validation = open(path_to_training_validation, 'r')
        data_list_validation = data_file_validation.readlines()
        data_file_validation.close()

        for (index, string) in enumerate(data_list_validation):
            data_list_validation[index] = string.rstrip('\n')  # убираем из строки символ перевода строки

        #for (index, query) in enumerate(data_list_validation)
        for (index, query) in enumerate(data_list_validation):
            marker = 0 # если 0 то не sqli
            if (index % 2 == 1):
                marker = 1

            SQLI = 0
            logarithmic_function = 0
            logarithmic_function += math.log(self.P_M / self.P_NM)
            # pattern=re.compile(r'(?:\w+|[\"=;\'\-*%)])')
            tokens = re.findall(self.pattern, query)
            tokens_unique = numpy.unique(tokens)
            # print(tokens_unique)
            for token in tokens_unique:
                if token in self.frequency_dictionary:
                    if self.frequency_dictionary[token][1] == 0:
                        probability_ratio = 0.00001  # Устанавливаем границы если вероятности нулевые
                    elif self.frequency_dictionary[token][0] == 0:
                        probability_ratio = 100000  # Устанавливаем границы если вероятности нулевые
                    else:
                        probability_ratio = self.frequency_dictionary[token][1] / self.frequency_dictionary[token][0]

                logarithmic_function += math.log(probability_ratio)
            print(query)
            if logarithmic_function > 0:
                SQLI = 1
                print('SQL-инъекция', logarithmic_function)
            else:
                SQLI = 0
                print('Обычный запрос', logarithmic_function)
            if(SQLI != marker):
                if(marker == 1): #Ошибка второго рода
                    self.false_negative = self.false_negative + 1
                else:
                    self.false_positive = self.false_positive + 1

        pass

    def get_parametrs(self):
        print("P(M)", self.P_M)
        print("P(NM)", self.P_NM)
        for key in self.frequency_dictionary:
            print(key, self.frequency_dictionary[key][0], self.frequency_dictionary[key][1])
        pass

