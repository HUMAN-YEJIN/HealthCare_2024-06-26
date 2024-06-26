import sys
import webbrowser
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import csv
from datetime import datetime
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import pyqtgraph as pg
import os

# 리소스 파일을 가져오는 import문
import 근육_rc

# UI파일 로드
form_class = uic.loadUiType("기초정보입력창.ui")[0]
form_class_2 = uic.loadUiType("메인창.ui")[0]
form_class_3 = uic.loadUiType("recode.ui")[0]
form_class_4 = uic.loadUiType('체중.ui')[0]


#운동기록 버튼 누르면 뜨는 창 설정-------------------------------------------------------------------------------------------------------
class Exercise(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.data_list = []
        self.data_by_date = {}
        self.load_data()
        self.sort_data_by_date()
        self.recommend()

    def setupUi(self):
        self.setWindowTitle('운동추천')
        self.setGeometry(100, 100, 1000, 600)  # 창의 위치와 크기 설정
        
        self.title_lbl = QLabel('근력 운동 영상', self)
        self.title_lbl.setGeometry(310, 10, 150, 30)
        
        self.exercise_1 = QPushButton('상체 근력 운동', self)
        self.exercise_1.setGeometry(310, 40, 150, 35)
        
        self.exercise_2 = QPushButton('하체 근력 운동', self)
        self.exercise_2.setGeometry(310, 80, 150, 35)
        
        self.exercise_3 = QPushButton('복부 근력 운동', self)
        self.exercise_3.setGeometry(310, 120, 150, 35)
        
        self.exercise_4 = QPushButton('유산소', self)
        self.exercise_4.setGeometry(310, 160, 150, 35)
        
        self.title_lbl_2 = QLabel('운동/건강 정보', self)
        self.title_lbl_2.setGeometry(500, 10, 150, 30)
        
        self.exercise_lbl = QLabel('', self)
        self.exercise_lbl.setGeometry(10, 40, 300, 160)  # 위치와 크기 수정
        
        self.exercise_5 = QPushButton('운동 루틴', self)
        self.exercise_5.setGeometry(500, 40, 150, 35)
        
        self.health = QPushButton('저체중 관련 질병', self)
        self.health.setGeometry(500, 80, 150, 35)

        self.exercise_relbl = QLabel('맞춤 추천 운동', self)
        self.exercise_relbl.setGeometry(10, 10, 300, 30)
        #유튜브 링크 걸기

        self.exercise_1.clicked.connect(lambda: webbrowser.open('https://youtube.com/playlist?list=PLUzeEZsuFIaKmlMfDVfe1jReFNiDeiG21&feature=shared'))
        self.exercise_2.clicked.connect(lambda: webbrowser.open('https://youtube.com/playlist?list=PLUzeEZsuFIaKstEGCFjWkxFaJKuURZhac&feature=shared'))
        self.exercise_3.clicked.connect(lambda: webbrowser.open('https://youtube.com/playlist?list=PLUzeEZsuFIaKtDja1m2BHX0izhWkaxcjZ&feature=shared'))
        self.exercise_4.clicked.connect(lambda: webbrowser.open('https://youtube.com/playlist?list=PLUzeEZsuFIaIrqSjRtgdSpRExe1AkTwjw&feature=shared'))
        self.exercise_5.clicked.connect(lambda: webbrowser.open('https://youtube.com/playlist?list=PLUzeEZsuFIaLq4MyOewuJQWXvWGia2UCs&feature=shared'))
        self.health.clicked.connect(lambda: webbrowser.open('https://youtube.com/playlist?list=PLUzeEZsuFIaLwnT4KIEcYQiGYRXMy88CZ&feature=shared'))

        #식단정보 띄우는 라벨
        self.health_lbl = QLabel(self)
        self.health_lbl.setGeometry(10, 420, 980, 170)  # 위치와 크기 수정
        self.health_lbl.setText('식단정보\n단순히 칼로리를 높이는 것이 아닌, 영양소의 균형과 칼로리 섭취를 함께 고려해야 한다. \n단백질 무조건 포함(근육의 형성과 유지에 필수적)\n-닭가슴살, 계란, 토피넛(땅콩버터) , 두부 등(이러한 음식들은 식단의 다양성과 포만감 유지에도움을 준다.)\n채소&과일(비타민과 미네랄 제공, 면연력 강화)\n- 당근, 브로콜리, 파프리카, 사과, 파인애플 등\n건강한 지방 (에너지 공급, 식사 후 오랜 시간 동안 포만감을 유지해줌)\n아보카도, 올리브 오일, 아몬드, 씨앗')
    #운동추천을위해 인바디 근육(표준,표준이하)값 가져오기
    def load_data(self):
        try:
            with open('인바디.csv', mode='r', newline='', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.data_list.append(row)
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")
    
    def sort_data_by_date(self):
        # 날짜를 기준으로 데이터 정렬
        self.data_list.sort(key=lambda x: x[0])

        # 날짜별로 데이터 정리
        for row in self.data_list:
            date = row[0]
            if date not in self.data_by_date:
                self.data_by_date[date] = []
            self.data_by_date[date].append(row)

    def recommend(self):
        self.currenttext = self.exercise_lbl.text()

        #가장 최근 날짜의 데이터를 추출
        if self.data_list:
            latest_data = self.data_list[-1]
            self.M_1 = latest_data[-5]
            self.M_2 = latest_data[-4]
            self.M_3 = latest_data[-3]
            self.M_4 = latest_data[-2]
            self.M_5 = latest_data[-1]
        
    #운동추천 라벨 표시
        self.exercise_1text = "\n상체근력운동" if self.M_1 == "표준이하" or self.M_2 == "표준이하" else ""
        self.exercise_2text = "\n복부 근력 운동" if self.M_3 == "표준이하" else ""
        self.exercise_3text = "\n하체근력운동" if self.M_4 == "표준이하" or self.M_5 == "표준이하" else ""

        self.printtext = self.currenttext + self.exercise_1text + self.exercise_2text + self.exercise_3text
        self.exercise_lbl.setText(self.printtext)
#-----------------------------------------------------------------------------------------------------------------------
    
#루틴 입력창--------------------------------------------------------------------------------------------------------------------
class Routin(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('Routin setting')
        self.setGeometry(100, 100, 600, 300)

        self.Pluse_edit = QLineEdit(self)
        self.Pluse_edit.setGeometry(1, 130, 500, 30)
        self.Pluse_edit.returnPressed.connect(self.Saveedit)

    def Saveedit(self):
        self.text = self.Pluse_edit.text()
        self.close()

class RoutinL(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.routin_list = []
        self.checkbox_list = []
        self.i = 0

        self.loadRoutins()  # 기존 루틴 불러오기

    def setupUi(self):
        self.setWindowTitle('루틴설정')
        self.resize(600, 300)

        self.routin_lbl = QLabel('루틴', self)
        self.routin_lbl.move(10, 1)

        self.routin_pluse = QPushButton('+', self)
        self.routin_pluse.setGeometry(70, 1, 30, 30)
        self.routin_pluse.clicked.connect(self.Pluse)

        self.routin_remove = QPushButton('-', self)
        self.routin_remove.setGeometry(110, 1, 30, 30)
        self.routin_remove.clicked.connect(self.Remove)

        self.warning_lbl = QLabel('', self)
        self.warning_lbl.setGeometry(150, 1, 300, 30)

    def Pluse(self):
        if len(self.routin_list) >= 5:  # 루틴이 5개 이상이면 추가하지 않음
            self.warning_lbl.setText("루틴은 5개까지 추가 가능합니다.")
            return
        
        self.dialog = Routin()
        self.dialog.exec_()
        text = self.dialog.Pluse_edit.text()

        if text:  # 루틴이 비어있지 않은 경우에만 추가
            self.routin_list.append(text)
            self.updateCheckboxes()

            # 루틴을 파일에 저장
            with open('routin.txt', mode='a', encoding='utf-8') as file:
                file.write(text + '\n')

    def Remove(self):
        if self.routin_list:  # 루틴 리스트가 비어있지 않은지 확인
            items = [str(i) + ": " + item for i, item in enumerate(self.routin_list)]
            item, ok = QInputDialog.getItem(self, "루틴 제거", "제거할 루틴 선택", items, editable=False)
            if ok:
                index = int(item.split(":")[0])
                removed_item = self.routin_list.pop(index)  # 리스트에서 선택된 인덱스의 요소 제거
                print("제거된 루틴:", removed_item)
                self.updateCheckboxes()  # 기존 체크박스를 갱신하여 다시 추가
                # 루틴을 파일에 저장
                self.saveRoutins()
        else:
            self.warning_lbl.setText("제거할 루틴이 없습니다.")

    def updateCheckboxes(self):
        # 기존 체크박스 제거
        for checkbox in self.checkbox_list:
            checkbox.deleteLater()
        self.checkbox_list.clear()
        
        # 체크박스 재추가
        self.i = 0
        for i, text in enumerate(self.routin_list):
            checkbox = QCheckBox(text, self)
            checkbox.move(10, 30 + i * 30)
            checkbox.show()
            self.checkbox_list.append(checkbox)
            self.i += 1
        
        if self.i > 4:
            self.warning_lbl.setText("루틴은 5개까지 추가 가능합니다.")
        else:
            self.warning_lbl.setText("")

    def loadRoutins(self):
        if os.path.exists('routin.txt'):
            with open('routin.txt', mode='r', encoding='utf-8') as file:
                self.routin_list = [line.strip() for line in file]
            self.updateCheckboxes()
        else:
            print("루틴 파일이 없습니다. 새 파일을 생성합니다.")

    def saveRoutins(self):
        with open('routin.txt', mode='w', encoding='utf-8') as file:
            for routin in self.routin_list:
                file.write(routin + '\n')
#-------------------------------------------------------------------------------------------------------------------
#--체중입력창----------------------------------------------------------------------------------------
class KGRecode(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()

        #날짜
        with open('날짜선택.txt',mode ='r',encoding='utf-8') as file:
            self.selected_date_str = file.read()
        

    def setupUi(self):
        self.setWindowTitle('체중 기록')
        self.setGeometry(100,100,600,300)

        self.KG_lbl=QLabel('체중을 입력하세요:',self)
        self.KG_lbl.setGeometry(200,10,200,40)
        
        self.KG_edit = QLineEdit(self)
        self.KG_edit.setGeometry(1,50,600,40)

        self.KG_save = QPushButton('확인',self)
        self.KG_save.setGeometry(1,100,600,40)

        self.KG_save.clicked.connect(self.Save_KG)
        self.KG_save.clicked.connect(self.csv)
    
    def Save_KG(self):
        saved_day = self.selected_date_str
        KG_value = self.KG_edit.text()
        
        # 파일이 존재하는지 확인하고, 없으면 빈 파일을 생성
        if not os.path.exists('체중기록.txt'):
            with open('체중기록.txt', 'w') as f:
                pass  # 파일을 빈 상태로 생성

        try:
            # 기존 파일을 읽어와서 데이터를 리스트로 변환합니다.
            with open('체중기록.txt', 'r') as f:
                lines = f.readlines()

            data = []
            for line in lines:
                # 괄호와 공백을 제거한 후에 ','를 기준으로 날짜와 체중을 분리합니다.
                line = line.strip('()\n')
                date_str, weight_str = line.split(',')

                # 데이터를 튜플 형태로 리스트에 추가합니다.
                data.append((date_str.strip(), weight_str.strip()))

            # 새 값을 추가하거나 업데이트합니다.
            data.append((saved_day, KG_value))

            # 데이터를 날짜순으로 정렬합니다.
            data.sort(key=lambda x: datetime.strptime(x[0], '%Y. %m. %d'))

            # 정렬된 데이터를 파일에 저장합니다.
            with open('체중기록.txt', 'w') as f:
                for date, weight in data:
                    f.write(f"({date},{weight})\n")

            # 저장 후 창을 닫습니다.
            self.close()

        except FileNotFoundError:
            print("File not found: '체중기록.txt'")
        except Exception as e:
            print(f"Error occurred: {e}")
    
    def csv(self):
        with open('체중기록.txt', 'r') as f:
            lines = f.readlines()
    # CSV 파일의 각 라인을 리스트로 변환합니다.
        data = [line.strip().split(',') for line in lines]
    # 날짜를 기준으로 데이터를 정렬합니다. 가정: 첫 번째 열이 날짜입니다.
        sorted_data = sorted(data, key=lambda x: x[0])
        header = ["날짜", "체중"]
        with open('체중기록.csv', 'w', newline='') as csvf:
            writer = csv.writer(csvf)
            writer.writerow(header)
            for row in sorted_data:
                writer.writerow(row)
#------------------------------------------------------------------------------------------------------------
#그래프 표시창-------------------------------------------------------------------------------------------------
class Report(QMainWindow, form_class_4):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.resize(700,800)
        self.KG_graph.clicked.connect(self.Graph_data_KG)
        self.date_list = []          
            

    def Graph_data_KG(self):
        csv = pd.read_csv ('체중기록.csv', encoding='cp949')
        Date = csv.iloc[:, 0]  # 첫 번째 열에 해당하는 데이터를 선택
        Value = csv.iloc[:, 1]  # 두 번째 열에 해당하는 데이터를 선택
   

        self.fig, ax = plt.subplots()
        ax.scatter(Date, Value)
        ax.set(xlabel="Date", ylabel ="KG", title = "KG Graph")
        ax.grid()

        # x축의 날짜 레이블을 회전시킴
        plt.xticks(rotation=45, ha='right')

        self.fig.tight_layout()  # 레이아웃을 자동으로 조정하여 겹치지 않게 함

        self.fig.savefig("체중.png")

        
        image_path = "체중.png"
        pixmap = QPixmap(image_path)
        self.Image_lbl.setPixmap(pixmap)

#칼로리.csv파일 생성
csv_file_2 = '칼로리.csv'

with open(csv_file_2, mode='a', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow('0')
#---------------------------------------------------------------------------------------------------
#--칼로리 입력------------------------------------------------------------------------------
class Foodcalorie(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.setWindowTitle('칼로리 입력')
        self.setGeometry(100,100,600,300)

        self.calorie = 0

    def setupUi(self):
        self.calorie_lbl = QLabel("칼로리를 입력하세요:",self)
        self.calorie_edit = QLineEdit(self)
        self.calorie_lbl.setGeometry(200,10,200,40)
        self.calorie_edit.setGeometry(1,50,600,40)
        self.finish_push = QPushButton("확인",self)
        self.finish_push.setGeometry(1,100,600,40)
        self.finish_push.clicked.connect(self.OK)

    def OK(self):  
        self.value = self.calorie_edit.text()
        print(self.value)
        self.close()  
#------------------------------------------------------------------------------------------------------------------------------------      

#메인창--------------------------------------------------------------------------------------------------------------------
class MainWindow(QMainWindow,form_class_2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.resize(800, 1000)
        self.data_list = []
        self.data_by_date = {}
        self.recode.clicked.connect(self.openRecode) #기록버튼 클릭시 기록창 오픈
        self.setting.clicked.connect(self.load_data)
        self.progress.setValue(0)
        self.Report.clicked.connect(self.openReport)
        self.Routin.clicked.connect(self.Routinset)
        self.exercise.clicked.connect(self.Exercise_R)
        
        
    def opencsv(self):
        with open('인바디.csv', 'r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            self.found = False
            self.specific_2_value = None  # 초기화 추가
        
            for row in reader:
                print(row)
            
    
        

    #루틴설정다이얼로그(창) 가져오기
    def Routinset(self):
        self.dialog = RoutinL()
        self.dialog.exec_()
    #운동추천다이얼로그(창) 가져오기
    def Exercise_R(self):
        self.newWindow = Exercise()
        self.newWindow.show()

    #인바디 데이터 로드
    def load_data(self):
        try:
            with open('인바디.csv', mode='r', newline='', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.data_list.append(row)
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")
        
        self.sort_data_by_date()
    
    def sort_data_by_date(self):
        # 날짜를 기준으로 데이터 정렬
        self.data_list.sort(key=lambda x: x[0])

        # 날짜별로 데이터 정리
        for row in self.data_list:
            date = row[0]
            if date not in self.data_by_date:
                self.data_by_date[date] = []
            self.data_by_date[date].append(row)
        self.recommend()
    #목쵸칼로리 추천값 설정법
    def recommend(self):

        # 여기서는 예시로 가장 최근 날짜의 데이터를 추출합니다.
        if self.data_list:
            latest_data = self.data_list[-1]
            value = latest_data[-6]
            self.goalvalue = float(value) + 500

        #목표칼로리 설정
        self.goalcalorie.setText(str(self.goalvalue))
        print(self.goalvalue)
        self.progressbar()


    #달성도 바-------------------------------------------------------------------------------------------
    def progressbar(self):
        with open('인바디.csv', 'r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)

        
        with open('칼로리.csv',mode = 'r', newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data = row[0]
                    
                    self.c_value = int(data)
        
        self.progressbarvalue = (self.c_value/self.goalvalue) * 100
        print(self.progressbarvalue)
        self.progress.setValue(int(self.progressbarvalue))
        self.add = self.c_value - self.goalvalue
        if self.c_value >= self.goalvalue:
            self.add_lbl.setText("+" + str(round(self.add, 1)))
            self.progress.setValue(100)
        #----------------------------------------------------------------------------------------------------



    #기록버튼 클릭시 기록창 오픈-------------------------------------------------------------------------------------------
    def openRecode(self):
        self.newWindow = Recode()
        self.newWindow.show()

    #레포트버튼
    def openReport(self):
        self.newWindow = Report()
        self.newWindow.show()
#---------------------------------------------------------------------------------------------------------------------------
#기록창--------------------------------------------------------------------------------------------------------------------
class Recode(QMainWindow,form_class_3):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.resize(510,404)
        self.c_value = 0

        self.selected_date_str = None  # 기본값으로 None 설정
        today = datetime.today().strftime('%Y. %m. %d') #오늘날짜

    #클릭버튼--------------------------------------------------------------------------------------
        self.recode_body.clicked.connect(self.openBasicWindow) #인바디 입력 버튼누르면 인바디창 오픈
        self.calendar.clicked.connect(self.showSelectedDate)#캘린더 선택시
        self.datechoose_lbl.setText(today) #날짜 라벨 초기 설정(오늘날짜)
        self.calorie_push.clicked.connect(self.Food)
        self.KG_push.clicked.connect(self.KG)
    #-----------------------------------------------------------------------------------------------
    #달력날짜 선택----------------------------------------------------------------------------------
    def showSelectedDate(self):
        selected_date = self.calendar.selectedDate()  # 달력 선택 날짜
        selected_date_str = selected_date.toString('yyyy. MM. dd') #날짜 표시형식
        self.datechoose_lbl.setText(selected_date_str) #라벨 텍스트 설정

        with open('날짜선택.txt', mode='w', encoding='utf-8') as file:
            file.write(selected_date_str)

    #------------------------------------------------------------------------------------------------
    #인바디창 열기-------------------------------------------------------------------------------------
    def openBasicWindow(self):
        self.newWindow = BasicWindow()
        self.newWindow.show()
        with open('날짜선택.txt',mode ='r',encoding='utf-8') as file:
            selected_date_str = file.read()
    #------------------------------------------------------------------------------------------------
    #칼로리 입력 창 열기-------------------------------------------------------------------------------
    def Food(self): 
    # food_push(칼로리 추가)버튼을 누르면 c_value에 칼로리값이 더해짐(먹은 총칼로리)
        self.dialog = Foodcalorie()
        self.dialog.exec_()
        text = self.dialog.calorie_edit.text()
        with open('칼로리.csv',mode = 'r', newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    self.data = row[0]

        
        self.c_value += int(text)
        self.r_value = self.c_value + int(self.data)

        print(self.c_value)
        print(self.r_value)
        

        try:
            with open('칼로리.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([self.r_value, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        except Exception as e:
            print(f"Error writing to CSV file: {e}")

    #체중입력창---------------------------------------------------------------------------------------------
    def KG(self):
        self.dialog = KGRecode()
        self.dialog.exec_()
        file_path = "체중기록.txt"
        with open(file_path, 'r') as f :
            for line in f.readlines():
                selected_date_str, KG_value = line.strip().strip('()').split(",")

    

        

#인바디창--------------------------------------------------------------------------------------------
class BasicWindow(QMainWindow, form_class):
    def __init__(self, ):
        super().__init__()
        self.setupUi(self)
        self.resize(1100, 1400)
        self.activenumber = 0
        self.i = 1
        self.data_list = []
        with open('날짜선택.txt',mode ='r',encoding='utf-8') as file:
            self.selected_date = file.read()

        self.selected_date_str = self.selected_date
        #날짜
        self.Date.setText(self.selected_date_str) # 선택한 날짜 칸에 표시

        # 근육 분석 이미지 로드 및 설정
        muscle_pixmap = QPixmap("C:/Users/angel/Desktop/기말 디헬케 프로그램 최종본/부위별근육분석.png")
        self.img_lbl.setPixmap(muscle_pixmap)
        self.img_lbl.resize(muscle_pixmap.width(), muscle_pixmap.height())

        
    #----------------------------------------------------------------------------------------------------
        
        self.calculation.clicked.connect(self.value_changed) #계산버튼누르면 자동 계산
        self.save_button.clicked.connect(self.BasicSave) # 기초정보 저장 버튼 클릭 시 BasicSave 함수 연결
    #선택날짜에 따른 데이터 로드----------------------------------------------------------------------------
        self.loadData() #함수실행

    def loadData(self):
        data2_list = []
        i = 0
        try:
            with open('인바디.csv', mode='r', newline='', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                found_data = False
                for row in reader:
                    if row[0] == self.selected_date_str:
                        self.Name.setText(row[1])
                        self.Age.setText(row[2])
                        self.gender.setText(row[3])
                        self.cm.setText(row[4])
                        self.KG.setText(row[5])
                        self.Muscle.setText(row[6])
                        self.fat_amount.setText(row[7])
                        self.BMI.setText(row[8])
                        self.fat_percent.setText(row[9])
                        self.R_KG.setText(row[10])
                        self.K_KG.setText(row[11])
                        self.Basic.setText(row[12])
                        self.E_f.setText(row[13])
                        self.M_1.setText(row[14])
                        self.M_2.setText(row[15])
                        self.M_3.setText(row[16])
                        self.M_4.setText(row[17])
                        self.M_5.setText(row[18])
                        found_data = True
                        break  # 일치하는 데이터를 찾았으면 반복문 종료
                
                if not found_data:
                    QMessageBox.warning(self, '데이터 없음', '선택된 날짜에 해당하는 데이터가 없습니다.')

        except FileNotFoundError:
            QMessageBox.warning(self, '파일 오류', '데이터 파일을 찾을 수 없습니다.')
    
    
    #계산함수------------------------------------------------------------------------------------------------
    def value_changed(self):
        try:
            weight = float(self.KG.text()) #만약 값이 없으면0으로 반환
            cm = float(self.cm.text())
            gender = self.gender.text()
            age = float(self.Age.text())
            self.fat = float(self.fat_amount.text())
            bmi = weight / ((cm / 100) ** 2)
            if self.active_1.isChecked():
                self.activenumber = 28
            if self.active_2.isChecked():
                self.activenumber = 33
            if self.active_3.isChecked():
                self.activenumber = 38
            if self.active_4.isChecked():
                self.activenumber = 43
            
            
            if gender == "남" or gender == "남성":
                self.Fat_percent_M = (self.fat / weight) * 100 #체지방률 계산
                self.rightweight_M = ((cm/100) **2) * 22 #적정체중계산
                self.weight_pluse_M = self.rightweight_M - weight #체중조절계산
                self.R_C_M = self.rightweight_M * self.activenumber #권장섭취열량 계산
                self.BMR_M = 66.47 + (13.75 * weight) + (5 * cm) - (6.76 * age)#기초대사량 계산
                self.BMI.setText(str(round(bmi,1)))#bmi표시
                self.fat_percent.setText(str(round(self.Fat_percent_M,1)))#체지방률표시
                self.R_KG.setText(str(round(self.rightweight_M,1)))#적정체중표시
                self.K_KG.setText("+" + str(round(self.weight_pluse_M,1)))#체중조절표시
                self.Basic.setText(str(round(self.BMR_M,1))) #기초대사량 표시
                self.E_f.setText(str(round(self.R_C_M,1))) #권장섭취열량 표시
                
                
            if gender == "여" or gender == "여성":
                self.Fat_percent_W = (self.fat / weight) * 100 #체지방률 계산
                self.rightweight_W = ((cm/100) **2) * 21 #적정체중계산
                self.weight_pluse_W = self.rightweight_W - weight #체중조절계산
                self.BMR_W = 665.1 + (9.56 * weight) + (1.85 * cm) - (4.86 * age)#기초대사량 계산
                self.R_C_W = self.rightweight_W * self.activenumber #권장섭취열량 계산
                self.BMI.setText(str(round(bmi,1)))
                self.fat_percent.setText(str(round(self.Fat_percent_W,1)))#체지방률표시
                self.R_KG.setText(str(round(self.rightweight_W,1)))#적정체중표시
                self.K_KG.setText("+" + str(round(self.weight_pluse_W,1)))#체중조절표시
                self.Basic.setText(str(round(self.BMR_W,1))) #기초대사량 표시
                self.E_f.setText(str(round(self.R_C_W,1))) #권장섭취열량 표시

        except ValueError:
            QMessageBox.warning(self, '입력 오류', '숫자 필드에 유효한 숫자를 입력해주세요.')

    #값 저장함수-----------------------------------------------------------------------------------------------------
    def BasicSave(self):

        self.weight = self.KG.text() #체중
        self.muscle = self.Muscle.text() #골격근량
        self.name = self.Name.text()#이름
        self.age = self.Age.text()#나이
        self.Cm = self.cm.text()#키
        self.Gender = self.gender.text()#성별
        self.date = self.Date.text()#날짜
        self.fat_amount_save = self.fat_amount.text()

        self.fat_percent_save = round(float(self.fat_percent.text()),1)#체지방률 저장
        self.right_KG_save = round(float(self.R_KG.text()),1) #적정체중 저장
        self.K_KG_save = round(float(self.K_KG.text()),1)#체중조절 저장

        

        #값이 입력되지 않았을 경우 입력오류
        if not self.weight or not self.muscle or not self.name or not self.age or not self.Cm or not self.Gender or not self.date:
            QMessageBox.warning(self, '입력 오류', '모든 필드를 입력해주세요.')
            return
        #데이터 저장------------------------------------------------------------------------------------------------------
        # 인바디.CSV 파일생성------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            # 기존 데이터 불러오기
        new_data = [
            self.date, self.name, self.age, self.Gender,
            self.Cm, self.weight, self.muscle, self.fat_amount_save,
            self.BMI.text(), self.fat_percent_save, self.right_KG_save,
            self.K_KG_save, self.Basic.text(), self.E_f.text(),
            self.M_1.text(), self.M_2.text(), self.M_3.text(),
            self.M_4.text(), self.M_5.text()
        ]

            # 기존 데이터 불러오기
        if os.path.exists('인바디.csv'):
            with open('인바디.csv', mode='r', newline='', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                self.data_list = list(reader)

                # 선택된 날짜와 일치하는 데이터 제거
            temp_list = []
            for row in self.data_list:
                if len(row) > 0 and row[0] != self.selected_date_str:
                    temp_list.append(row)

            self.data_list = temp_list
            print(self.data_list)

                # 데이터를 다시 CSV 파일에 쓰기

            with open('인바디.csv', mode='w', newline='', encoding='utf-8-sig') as file:
                file.truncate(0)


            with open('인바디.csv', mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerows(self.data_list)

            # 새로운 데이터 추가
        with open('인바디.csv', mode='a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(new_data)

        self.close()
        print("데이터 처리 완료")

        #---------------------------------------------------------------------------------------------------------------------------------------------------------------

        
                    
                
                
            
    
if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    sys.exit(app.exec_())
    
    

