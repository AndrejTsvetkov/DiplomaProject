import tkinter as tk
from tkinter import filedialog as fd
from PIL import ImageTk, Image
import NBC
import LSTM

class Example(tk.Frame):

       def __init__(self, parent):
           tk.Frame.__init__(self, parent)

           self.parent = parent
           self.parent.geometry("1920x700+300+300")
           self.parent["bg"] = "#121212"
           self.initUI()

           self.file_for_detection=""

           self.data_list = []
           self.total_count = 0 # здесь храним максимальное число строк для обучения в выбранном файле

           # создаем класс НБК
           self.nbc = NBC.NBC()

           self.data_list_LSTM = []
           self.total_count_LSTM = 0

           self.lstm = None
           self.file_for_detection_LSTM = ""

       def initUI(self):

           self.parent.title("Распознование SQL-инъекций")

           #Форма для НБК
           frm_form = tk.Frame(relief=tk.FLAT)
           frm_form.pack_propagate(0)
           #frm_form['width'] = 1000
           frm_form['bg'] = '#1D1D1D'
           frm_form.grid(row=0, column=0)

           #Форма для LSTM

           frm_form_LSTM = tk.Frame(relief=tk.FLAT)
           frm_form_LSTM.pack_propagate(0)
           # frm_form_LSTM['width'] = 1000
           frm_form_LSTM['bg'] = '#1D1D1D'
           frm_form_LSTM.grid(row=0, column=1)


           # -----------------------------------------------------КНОПКИ ДЛЯ НБК ---------------------------------------------
           path = "D:\dataset\dataset on plain text\img.jpg"
           img = ImageTk.PhotoImage(Image.open(path))
           panel = tk.Label(frm_form, image=img)
           panel.image_ref = img
           panel['bg'] = '#1D1D1D'

           path1 = "D:\dataset\dataset on plain text\LSTM.jpg"
           img1 = ImageTk.PhotoImage(Image.open(path1))
           panel1 = tk.Label(frm_form_LSTM, image=img1)
           panel1.image_ref = img1
           panel1['bg'] = '#1D1D1D'

           #-----------------------------------------------------КНОПКИ ДЛЯ ФАЗЫ ОБУЧЕНИЯ ---------------------------------------------

           lbl_training = tk.Label(frm_form, text="Фаза обучения", font='Roboto 14 italic underline', fg='#8B64FD', justify = "left", padx =0)
           lbl_training['bg'] = '#1D1D1D'

           lbl_file_for_training = tk.Label(frm_form, text="Выберите файл для обучения:", font='Roboto 12', fg='#DFDFDD')
           lbl_file_for_training['bg'] = '#1D1D1D'

           btn_open = tk.Button(frm_form, text="Выберите файл",
                                background = "#343434",  # фоновый цвет кнопки
                                foreground = "#DFDFDD",  # цвет текста
                                activebackground = "#1D1D1D",
                                activeforeground = "#8C8C8C",
                                borderwidth = 0,
                                padx = "0",  # отступ от границ до содержимого по горизонтали
                                pady = "0",  # отступ от границ до содержимого по вертикали
                                font = "Roboto 12",  # высота шрифта
                                command = self.choiceFileTraining
                                )

           self.lbl_file_for_training_show = tk.Label(frm_form, font='Roboto 12 italic', fg='#DFDFDD')
           self.lbl_file_for_training_show['bg'] = '#1D1D1D' #1D1D1D

           #print(Example.file_for_training)
           # self.lbl_file_for_training_show['text'] = Example.file_for_training

           btn_start_training = tk.Button(frm_form, text="Обучить",
                                background="#343434",  # фоновый цвет кнопки
                                foreground="#DFDFDD",  # цвет текста
                                activebackground="#1D1D1D",
                                activeforeground="#8C8C8C",
                                borderwidth=0,
                                padx="0",  # отступ от границ до содержимого по горизонтали
                                pady="0",  # отступ от границ до содержимого по вертикали
                                font="Roboto 12",  # высота шрифта
                                command=self.startTraining
                                )

           self.lbl_total_number_samples = tk.Label(frm_form, font='Roboto 10 italic', fg='#B6B6B5')
           self.lbl_total_number_samples['bg'] = '#1D1D1D'
           self.lbl_total_number_samples['text'] = ""

           lbl_number_samples = tk.Label(frm_form, font='Roboto 12', fg='#DFDFDD')
           lbl_number_samples['bg'] = '#1D1D1D' #1D1D1D
           lbl_number_samples['text'] = "Введите количество примеров"

           self.ent_number_samples = tk.Entry(frm_form, font='Roboto 10 italic', fg='white', justify = "right", bd = 0, width = "10")
           #self.ent_number_samples.insert(0, "Введите здесь")
           self.ent_number_samples['bg'] = '#343434' #1D1D1D

           # -----------------------------------------------------КНОПКИ ДЛЯ ФАЗЫ РАСПОЗНАВАНИЯ---------------------------------------------

           lbl_detection = tk.Label(frm_form, text="Фаза распознавания", font='Roboto 14 italic underline', fg='#8B64FD', justify="left", padx=0)
           lbl_detection['bg'] = '#1D1D1D'

           lbl_file_for_detection = tk.Label(frm_form, text="Выберите файл для обучения:", font='Roboto 12', fg='#DFDFDD')
           lbl_file_for_detection['bg'] = '#1D1D1D'

           btn_open_1 = tk.Button(frm_form, text="Выберите файл",
                                background="#343434",  # фоновый цвет кнопки
                                foreground="#DFDFDD",  # цвет текста
                                activebackground="#1D1D1D",
                                activeforeground="#8C8C8C",
                                borderwidth=0,
                                padx="0",  # отступ от границ до содержимого по горизонтали
                                pady="0",  # отступ от границ до содержимого по вертикали
                                font="Roboto 12",  # высота шрифта
                                command=self.choiceFileDetection
                                )

           self.lbl_file_for_detection_show = tk.Label(frm_form, font='Roboto 12 italic', fg='#DFDFDD')
           self.lbl_file_for_detection_show['bg'] = '#1D1D1D'

           btn_start_detection = tk.Button(frm_form, text="Проверить",
                                          background="#343434",  # фоновый цвет кнопки
                                          foreground="#DFDFDD",  # цвет текста
                                          activebackground="#1D1D1D",
                                          activeforeground="#8C8C8C",
                                          borderwidth=0,
                                          padx="0",  # отступ от границ до содержимого по горизонтали
                                          pady="0",  # отступ от границ до содержимого по вертикали
                                          font="Roboto 12",  # высота шрифта
                                          command=self.startDetection
                                          )


           lbl_total_errors = tk.Label(frm_form, font='Roboto 12', fg='#DFDFDD')
           lbl_total_errors['bg'] = '#1D1D1D'  # 1D1D1D
           lbl_total_errors['text'] = "Общий процент ошибок:"

           self.lbl_total_errors_show = tk.Label(frm_form, font='Roboto 12', fg='#8B64FD')
           self.lbl_total_errors_show['bg'] = '#1D1D1D'  # 1D1D1D

           lbl_false_positive = tk.Label(frm_form, font='Roboto 12', fg='#DFDFDD')
           lbl_false_positive['bg'] = '#1D1D1D'  # 1D1D1D
           lbl_false_positive['text'] = "Процент ошибок первого рода:"

           self.lbl_false_positive_show = tk.Label(frm_form, font='Roboto 12', fg='#8B64FD')
           self.lbl_false_positive_show['bg'] = '#1D1D1D'  # 1D1D1D

           lbl_false_negative = tk.Label(frm_form, font='Roboto 12', fg='#DFDFDD')
           lbl_false_negative['bg'] = '#1D1D1D'  # 1D1D1D
           lbl_false_negative['text'] = "Общий ошибок второго рода:"

           self.lbl_false_negative_show = tk.Label(frm_form, font='Roboto 12', fg='#8B64FD')
           self.lbl_false_negative_show['bg'] = '#1D1D1D'  # 1D1D1D


           # Использует менеджер геометрии grid
           panel.grid(row=0, column=0, columnspan=3, sticky="nsew")
           lbl_training.grid(row=1, column=0,  sticky="w", pady=8, padx = 8)
           lbl_file_for_training.grid(row=2, column=0, sticky="w", padx = 8)
           btn_open.grid(row=2, column=1, sticky="")
           self.lbl_file_for_training_show.grid(row=2, column=2, sticky="e", padx = 8)
           self.lbl_total_number_samples.grid(row=3, column=2, sticky="e", padx = 8)
           lbl_number_samples.grid(row=4, column=1, sticky="w", padx = 8)
           self.ent_number_samples.grid(row=4, column=2, sticky="e", padx = 8)
           btn_start_training.grid(row=5, column=1, sticky="ns", pady=15)

           lbl_detection.grid(row=6, column=0,  sticky="w", pady=8, padx = 8)
           lbl_file_for_detection.grid(row=7, column=0, sticky="w", padx = 8)
           btn_open_1.grid(row=7, column=1, sticky="ns")
           self.lbl_file_for_detection_show.grid(row=7, column=2, sticky="e",padx = 8)
           btn_start_detection.grid(row=8, column=1, sticky="ns", pady=15)

           lbl_total_errors.grid(row=9, column=2, sticky="e", padx = 8)
           self.lbl_total_errors_show.grid(row=10, column=2, sticky="e", padx = 8)
           lbl_false_positive.grid(row=11, column=2, sticky="e", padx=8)
           self.lbl_false_positive_show.grid(row=12, column=2, sticky="e", padx=8)
           lbl_false_negative.grid(row=13, column=2, sticky="e", padx=8)
           self.lbl_false_negative_show.grid(row=14, column=2, sticky="e", padx=8)

           # -----------------------------------------------------КНОПКИ ДЛЯ LSTM ---------------------------------------------

           # -----------------------------------------------------КНОПКИ ДЛЯ ФАЗЫ ОБУЧЕНИЯ ---------------------------------------------

           lbl_training_LSTM = tk.Label(frm_form_LSTM, text="Фаза обучения", font='Roboto 14 italic underline', fg='#8B64FD',
                                   justify="left", padx=0)
           lbl_training_LSTM['bg'] = '#1D1D1D'

           lbl_file_for_training_LSTM = tk.Label(frm_form_LSTM, text="Выберите файл для обучения:", font='Roboto 12',
                                            fg='#DFDFDD')
           lbl_file_for_training_LSTM['bg'] = '#1D1D1D'

           btn_open_LSTM = tk.Button(frm_form_LSTM, text="Выберите файл",
                                background="#343434",  # фоновый цвет кнопки
                                foreground="#DFDFDD",  # цвет текста
                                activebackground="#1D1D1D",
                                activeforeground="#8C8C8C",
                                borderwidth=0,
                                padx="0",  # отступ от границ до содержимого по горизонтали
                                pady="0",  # отступ от границ до содержимого по вертикали
                                font="Roboto 12",  # высота шрифта
                                command=self.choiceFileTrainingLSTM
                                )

           self.lbl_file_for_training_show_LSTM = tk.Label(frm_form_LSTM, font='Roboto 12 italic', fg='#DFDFDD')
           self.lbl_file_for_training_show_LSTM['bg'] = '#1D1D1D'  # 1D1D1D

           # print(Example.file_for_training)
           # self.lbl_file_for_training_show['text'] = Example.file_for_training

           btn_start_training_LSTM = tk.Button(frm_form_LSTM, text="Обучить",
                                          background="#343434",  # фоновый цвет кнопки
                                          foreground="#DFDFDD",  # цвет текста
                                          activebackground="#1D1D1D",
                                          activeforeground="#8C8C8C",
                                          borderwidth=0,
                                          padx="0",  # отступ от границ до содержимого по горизонтали
                                          pady="0",  # отступ от границ до содержимого по вертикали
                                          font="Roboto 12",  # высота шрифта
                                          command=self.startTrainingLSTM
                                          )

           self.lbl_total_number_samples_LSTM = tk.Label(frm_form_LSTM, font='Roboto 10 italic', fg='#B6B6B5')
           self.lbl_total_number_samples_LSTM['bg'] = '#1D1D1D'
           self.lbl_total_number_samples_LSTM['text'] = ""

           lbl_number_samples_LSTM = tk.Label(frm_form_LSTM, font='Roboto 12', fg='#DFDFDD')
           lbl_number_samples_LSTM['bg'] = '#1D1D1D'  # 1D1D1D
           lbl_number_samples_LSTM['text'] = "Введите количество примеров"

           self.ent_number_samples_LSTM = tk.Entry(frm_form_LSTM, font='Roboto 10 italic', fg='white', justify="right", bd=0, width = "10")
           self.ent_number_samples_LSTM['bg'] = '#343434'  # 1D1D1D

           lbl_number_epochs_LSTM = tk.Label(frm_form_LSTM, font='Roboto 12', fg='#DFDFDD')
           lbl_number_epochs_LSTM['bg'] = '#1D1D1D'  # 1D1D1D
           lbl_number_epochs_LSTM['text'] = "Введите количество эпох"

           self.ent_number_epochs_LSTM = tk.Entry(frm_form_LSTM, font='Roboto 10 italic', fg='white', justify="right",
                                                   bd=0, width="10")
           self.ent_number_epochs_LSTM['bg'] = '#343434'  # 1D1D1D

           lbl_learningrate_LSTM = tk.Label(frm_form_LSTM, font='Roboto 12', fg='#DFDFDD')
           lbl_learningrate_LSTM['bg'] = '#1D1D1D'  # 1D1D1D
           lbl_learningrate_LSTM['text'] = "Введите коэффициент обучения"

           self.ent_learningrate_LSTM = tk.Entry(frm_form_LSTM, font='Roboto 10 italic', fg='white', justify="right",
                                                   bd=0, width="10")
           self.ent_learningrate_LSTM['bg'] = '#343434'  # 1D1D1D


           #-------------------------------------------------КНОПКИ ДЛЯ ФАЗЫ РАСПОЗНОВАНИЯ

           lbl_detection_LSTM = tk.Label(frm_form_LSTM, text="Фаза распознавания", font='Roboto 14 italic underline',
                                    fg='#8B64FD', justify="left", padx=0)
           lbl_detection_LSTM['bg'] = '#1D1D1D'

           lbl_file_for_detection_LSTM = tk.Label(frm_form_LSTM, text="Выберите файл для обучения:", font='Roboto 12',
                                             fg='#DFDFDD')
           lbl_file_for_detection_LSTM['bg'] = '#1D1D1D'

           btn_open_1_LSTM = tk.Button(frm_form_LSTM, text="Выберите файл",
                                  background="#343434",  # фоновый цвет кнопки
                                  foreground="#DFDFDD",  # цвет текста
                                  activebackground="#1D1D1D",
                                  activeforeground="#8C8C8C",
                                  borderwidth=0,
                                  padx="0",  # отступ от границ до содержимого по горизонтали
                                  pady="0",  # отступ от границ до содержимого по вертикали
                                  font="Roboto 12",  # высота шрифта
                                  command=self.choiceFileDetectionLSTM
                                  )

           self.lbl_file_for_detection_show_LSTM = tk.Label(frm_form_LSTM, font='Roboto 12 italic', fg='#DFDFDD')
           self.lbl_file_for_detection_show_LSTM['bg'] = '#1D1D1D'

           btn_start_detection_LSTM = tk.Button(frm_form_LSTM, text="Проверить",
                                           background="#343434",  # фоновый цвет кнопки
                                           foreground="#DFDFDD",  # цвет текста
                                           activebackground="#1D1D1D",
                                           activeforeground="#8C8C8C",
                                           borderwidth=0,
                                           padx="0",  # отступ от границ до содержимого по горизонтали
                                           pady="0",  # отступ от границ до содержимого по вертикали
                                           font="Roboto 12",  # высота шрифта
                                           command=self.startDetectionLSTM
                                           )

           lbl_total_errors_LSTM = tk.Label(frm_form_LSTM, font='Roboto 12', fg='#DFDFDD')
           lbl_total_errors_LSTM['bg'] = '#1D1D1D'  # 1D1D1D
           lbl_total_errors_LSTM['text'] = "Общий процент ошибок:"

           self.lbl_total_errors_show_LSTM = tk.Label(frm_form_LSTM, font='Roboto 12', fg='#8B64FD')
           self.lbl_total_errors_show_LSTM['bg'] = '#1D1D1D'  # 1D1D1D

           lbl_false_positive_LSTM = tk.Label(frm_form_LSTM, font='Roboto 12', fg='#DFDFDD')
           lbl_false_positive_LSTM['bg'] = '#1D1D1D'  # 1D1D1D
           lbl_false_positive_LSTM['text'] = "Процент ошибок первого рода:"

           self.lbl_false_positive_show_LSTM = tk.Label(frm_form_LSTM, font='Roboto 12', fg='#8B64FD')
           self.lbl_false_positive_show_LSTM['bg'] = '#1D1D1D'  # 1D1D1D

           lbl_false_negative_LSTM = tk.Label(frm_form_LSTM, font='Roboto 12', fg='#DFDFDD')
           lbl_false_negative_LSTM['bg'] = '#1D1D1D'  # 1D1D1D
           lbl_false_negative_LSTM['text'] = "Общий ошибок второго рода:"

           self.lbl_false_negative_show_LSTM = tk.Label(frm_form_LSTM, font='Roboto 12', fg='#8B64FD')
           self.lbl_false_negative_show_LSTM['bg'] = '#1D1D1D'  # 1D1D1D

           panel1.grid(row=0, column=0, columnspan=3, sticky="nsew")
           lbl_training_LSTM.grid(row=1, column=0, sticky="w", pady=8, padx=8)
           lbl_file_for_training_LSTM.grid(row=2, column=0, sticky="w", padx=8)
           btn_open_LSTM.grid(row=2, column=1, sticky="")
           self.lbl_file_for_training_show_LSTM.grid(row=2, column=2, sticky="e", padx=8)
           self.lbl_total_number_samples_LSTM.grid(row=3, column=2, sticky="e", padx=8)
           lbl_number_samples_LSTM.grid(row=4, column=1, sticky="w", padx=8)
           self.ent_number_samples_LSTM.grid(row=4, column=2, sticky="e", padx=8)
           lbl_number_epochs_LSTM.grid(row=5, column=1, sticky="w", padx=8)
           self.ent_number_epochs_LSTM.grid(row=5, column=2, sticky="e", padx=8)
           lbl_learningrate_LSTM.grid(row=6, column=1, sticky="w", padx=8)
           self.ent_learningrate_LSTM.grid(row=6, column=2, sticky="e", padx=8)
           btn_start_training_LSTM.grid(row=7, column=1, sticky="ns", pady=15)

           lbl_detection_LSTM.grid(row=8, column=0, sticky="w", pady=8, padx=8)
           lbl_file_for_detection_LSTM.grid(row=9, column=0, sticky="w", padx=8)
           btn_open_1_LSTM.grid(row=9, column=1, sticky="ns")
           self.lbl_file_for_detection_show_LSTM.grid(row=9, column=2, sticky="e", padx=8)
           btn_start_detection_LSTM.grid(row=10, column=1, sticky="ns", pady=15)

           lbl_total_errors_LSTM.grid(row=11, column=2, sticky="e", padx=8)
           self.lbl_total_errors_show_LSTM.grid(row=12, column=2, sticky="e", padx=8)
           lbl_false_positive_LSTM.grid(row=13, column=2, sticky="e", padx=8)
           self.lbl_false_positive_show_LSTM.grid(row=14, column=2, sticky="e", padx=8)
           lbl_false_negative_LSTM.grid(row=15, column=2, sticky="e", padx=8)
           self.lbl_false_negative_show_LSTM.grid(row=16, column=2, sticky="e", padx=8)



       def choiceFileTraining(self):
           ftype = [('Dataset files', '*.txt')]
           file_name = fd.askopenfilename(filetypes=ftype)
           self.lbl_file_for_training_show['text'] = file_name

           if(file_name!=""):
               data_file = open(file_name, 'r')
               data_list = data_file.readlines()
               #print(len(data_list))
               self.total_count = len(data_list)
               self.lbl_total_number_samples['text'] = ('Количество:', self.total_count)
               self.data_list = data_list
               data_file.close()
               self.dataPrepare() #подготовим данные для передачи в НБК, уберем символы перевода строки
           pass

       def dataPrepare(self):
           for (index, string) in enumerate(self.data_list):  # не обрабатываем последнюю строку
               self.data_list[index] = string.rstrip('\n')  # убираем из строки символ перевода строки

       def choiceFileDetection(self):
           ftype = [('Dataset files', '*.txt')]
           file_name = fd.askopenfilename(filetypes=ftype)
           self.lbl_file_for_detection_show['text'] = file_name
           self.file_for_detection = file_name

       def startTraining(self):
           number_samples = self.ent_number_samples.get() # ввели количество строк для обучения
           if(number_samples.isdigit()):
               print(int(number_samples))
               if(int(number_samples) <= self.total_count): #нельзя обучить на большем числе примеров, чем есть
                   self.nbc.train(self.data_list, int(number_samples))
                   self.nbc.get_parametrs()


       def startDetection(self):
           self.nbc.query(self.file_for_detection)
           self.lbl_total_errors_show['text']=(self.nbc.false_positive + self.nbc.false_negative, "%")
           self.lbl_false_positive_show['text'] = (self.nbc.false_positive, "%")
           self.lbl_false_negative_show['text'] = (self.nbc.false_negative, "%")
           print("Ошибка первого рода", self.nbc.false_positive)
           print("Ошибка второго рода", self.nbc.false_negative)

       #--------------------------------------------------------------------ФУНКЦИИ ДЛЯ LSTM-----------------------------------------------------------------------------

       def choiceFileTrainingLSTM(self):
           ftype = [('Dataset files', '*.txt')]
           file_name = fd.askopenfilename(filetypes=ftype)
           self.lbl_file_for_training_show_LSTM['text'] = file_name


           if(file_name!=""):
               data_file = open(file_name, 'r')
               data_list = data_file.readlines()
               #print(len(data_list))
               self.total_count_LSTM = len(data_list)
               self.lbl_total_number_samples_LSTM['text'] = ('Количество:', self.total_count_LSTM)
               self.data_list_LSTM = data_list
               data_file.close()
               self.dataPrepareLSTM() #подготовим данные для передачи в НБК, уберем символы перевода строки
           pass

       def dataPrepareLSTM(self):
           for (index, string) in enumerate(self.data_list_LSTM):  # не обрабатываем последнюю строку
               self.data_list_LSTM[index] = string.rstrip('\n')  # убираем из строки символ перевода строки
           #print(self.data_list_LSTM)

       def startTrainingLSTM(self):
           cellcount = 20 #задаем количество ячеек LSTM
           learningrate =  self.ent_learningrate_LSTM.get() #задаем коэффициент обучения
           number_epochs = self.ent_number_epochs_LSTM.get()    #количество эпох

           self.lstm = LSTM.LSTM(cellcount, float(learningrate))
           self.lstm.weigths_print()
           number_samples = self.ent_number_samples_LSTM.get()  # ввели количество строк для обучения
           if (number_samples.isdigit()):
               print(int(number_samples))
               if (int(number_samples) <= self.total_count_LSTM):  # нельзя обучить на большем числе примеров, чем есть
                   self.lstm.train_all(self.data_list_LSTM, int(number_samples), int(number_epochs))
                   self.lstm.weigths_print()
                   print("Обучение закончено!")

       def choiceFileDetectionLSTM(self):
           ftype = [('Dataset files', '*.txt')]
           file_name = fd.askopenfilename(filetypes=ftype)
           self.lbl_file_for_detection_show_LSTM['text'] = file_name
           self.file_for_detection_LSTM = file_name

       def startDetectionLSTM(self):
           self.lstm.query_all(self.file_for_detection_LSTM)
           self.lbl_total_errors_show_LSTM['text'] = (self.lstm.false_positive + self.lstm.false_negative, "%")
           self.lbl_false_positive_show_LSTM['text'] = (self.lstm.false_positive, "%")
           self.lbl_false_negative_show_LSTM['text'] = (self.lstm.false_negative, "%")

def main():
       root = tk.Tk()
       ex = Example(root)
       root.mainloop()



if __name__ == '__main__':
       main()


'''
import NBC

path = r'E:\dataset\dataset on plain text\training_dataset_60.txt'
path_v = r'E:\dataset\dataset on plain text\validation_dataset_10.txt'
nbc = NBC.NBC()
nbc.train(path)
#nbc.get_parametrs()
nbc.query(path_v)
'''


