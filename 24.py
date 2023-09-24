import tkinter as tk
from tkinter import font
import csv
import prettytable as pt
from tkinter import scrolledtext


yesno_list = ['否', '是']

# 讀入csv檔
file1 = '/Users/toyuan/Desktop/1pythonProject1/venv/b.csv'
#'/Users/toyuan/Desktop/pythonProject1/venv/b.csv'
infolist = []
with open(file1, mode='r', newline='') as c:
    information = csv.reader(c)
    for j in information:  # 將資料整理成list
        infolist.append(j)
infolist2 = []
hotel_data = []
for j in infolist:  # 轉換 infolist 內的元素型別
    infolist2 = []
    for q in range(len(j)):
        if q != 0 and q != 1 and q != (len(j) - 1):
            infolist2.append(int(j[q]))
        elif q == (len(j) - 1):
            infolist2.append(float(j[q]))
        else:
            infolist2.append(j[q])
    hotel_data.append(infolist2)

# 建立名為 UserInput 的物件，繼承自 Frame
class UserInput(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.create_widgets()

    # 取得使用者輸入的資料
    def reply(self):  # 清空文字區域
        user = [self.v.get(), yesno_list[int(self.v_nation.get())], yesno_list[int(self.v_meal.get())],
                yesno_list[int(self.v_citizen.get())], [self.num1.get(), self.num2.get()]]
        self.need = user
        return self.filt_caculate()  # 呼叫 filt_caculate

    # 依項目篩選然後計算總價
    def filt_caculate(self):
        f2 = font.Font(size=14, family='Courier New')
        nation = my_input.need[1]  # 國籍(是/否)
        meal = my_input.need[2]  # 供餐(是/
        citizen = my_input.need[3]  # 台北市民(是/否)
        list_budget = sorted(my_input.need[4])  # 預算範圍([最低預算, 最高預算])
        list_infooutput = []  # 需要輸出的飯店資訊

        list_information = []
        for k in hotel_data:
            dist = k[0]
            if my_input.need[0] == dist:  # 行政區篩選
                list_information.append(k)

        for i in range(len(list_information)):
            lowerprice = list_information[i][2]  # 供餐且本國籍的最低價
            higherprice = list_information[i][3]  # 供餐且本國籍的最高價

            if meal == "否":
                if nation == "否" and list_information[i][10] != 0 and list_information[i][11] != 0:
                    lowerprice = list_information[i][10]  # 不供餐且非本國籍的最低價
                    higherprice = list_information[i][11]  # 不供餐且非本國籍的最高價
                if nation == "是" and list_information[i][8] != 0 and list_information[i][9] != 0:
                    lowerprice = list_information[i][8]  # 不供餐且本國籍的最低價
                    higherprice = list_information[i][9]  # 不供餐且本國籍的最高價
            if meal == "是":
                if nation == "否" and list_information[i][6] != 0 and list_information[i][7] != 0:
                    lowerprice = list_information[i][6]  # 供餐且非本國籍的最低價
                    higherprice = list_information[i][7]  # 供餐且非本國籍的最高價

            if citizen == "是":
                subsidy = 500 * 14  # 台北市民補助
            else:
                subsidy = 0

            minsum = (lowerprice * 14) - subsidy  # 計算後總價的最低價
            maxsum = (higherprice * 14) - subsidy  # 計算後總價的最高價
            list_sum = [minsum, maxsum]  # 計算後總價的範圍
            # 旅館價格區間和預算的交集
            if list_sum[0] not in range(list_budget[0] * 14, list_budget[1] * 14) and \
               list_sum[1] not in range(list_budget[0] * 14, list_budget[1] * 14):
                continue
            else:  # 篩選結果（輸出項目：評價, 旅館名稱, 總花費區間）
                list_infooutput.append([list_information[i][12], list_information[i][1], list_sum])

        # 依評價由高到低排列
        output = []
        for hotels in list_infooutput:
            output.append(hotels)
        output.sort()
        output.reverse()
        # 輸出資料整理成表格
        result = pt.PrettyTable()
        result.field_names = ['編號', '旅館', '評價', '價位選擇']
        turn = 0
        for hotel in output:
            turn += 1
            name = hotel[1]
            rate = hotel[0]
            prices = str(hotel[2][0]) + '-' + str(hotel[2][1])
            result.add_row([turn, name, (str(rate) + '/5星' + ''), prices])
            result.add_row(['', '', '', ''])
        result.align['編號'] = 'l'
        result.align['旅館'] = 'l'
        result.align['評價'] = 'r'
        result.align['價位選擇'] = 'r'
        result.set_style(pt.PLAIN_COLUMNS)
        # self.can.create_text(300, 300, text=result, font=f2)
        # self.scroller = tk.Scrollbar(self)
        self.mytext = tk.Text(width=75, height=75, bg='WhiteSmoke', wrap=tk.NONE)
        self.mytext.configure(font=f2)
        self.mytext.delete('1.0', 'end')
        # self.scroller = tk.Scrollbar(self, orient=tk.VERTICAL)  # 表格加入文字區域
        # self.scroller.grid(row=7, column=1, sticky=tk.N + tk.S)
        self.mytext.insert(tk.END, result)
        self.mytext.grid(row=7, column=0)
        self.scroller = tk.Scrollbar(self, command=self.mytext.yview)
        # self.scroller.configure(command=self.mytext.yview)
        self.mytext.configure(yscrollcommand=self.scroller.set)
        # self.scroller.configure(command=self.mytext.yview)
        # self.scroller.grid(row=7, column=8, sticky=tk.N + tk.S)

    # 在視窗內加入元件
    def create_widgets(self):
        f1 = font.Font(size=14, family='Courier New')
        f3 = font.Font(size=14, family='Courier New')
        self.l2 = tk.Label(self, text='請輸入篩選條件', bg='RoyalBlue', font=f1, fg='white', width=75,
                           height=2)
        self.l2.grid(row=10, column=0, columnspan=10)
        self.can = tk.Canvas(self, width=600, height=1100, bg='WhiteSmoke')
        # 設定按鈕於觸發後處理 reply 函式
        self.b1 = tk.Button(self, text='確定', font=f1, highlightcolor='RoyalBlue', command=self.reply)
        self.l_district = tk.Label(self, text='行政區:', font=f1)

        # 建立下拉式表單選取行政區
        self.optionList = ('萬華區', '內湖區', '南港區', '大安區', '士林區', '北投區', '信義區', '大同區', '中正區', '松山區', '中山區')
        self.v = tk.StringVar()
        self.v.set("行政區")
        self.optionmenu = tk.OptionMenu(self, self.v, *self.optionList)

        # 建立價格區間的輸入方塊
        self.l_price = tk.Label(self, bg='white', text='價格區間:', font=f1)
        self.num1 = tk.IntVar(self, value=1000)
        self.num2 = tk.IntVar(self, value=20000)
        self.a = tk.Entry(self, width=7, textvariable=self.num1)
        self.b = tk.Label(self, width=3, text='-', font=f1)
        self.c = tk.Entry(self, width=7, textvariable=self.num2)

        # 建立國籍、市民和供餐的選項按鈕
        self.l_nation = tk.Label(self, text='本國籍或持永久居留證:', font=f1)
        self.v_nation = tk.StringVar()
        self.v_nation.set(0)
        self.yes = tk.Radiobutton(self, text='是', variable=self.v_nation, value=1)
        self.no = tk.Radiobutton(self, text='否', variable=self.v_nation, value=0)
        self.l_citizen = tk.Label(self, text='台北市民:', font=f1)
        self.v_citizen = tk.StringVar()
        self.v_citizen.set(0)
        self.yes2 = tk.Radiobutton(self, text='是', variable=self.v_citizen, value=1)
        self.no2 = tk.Radiobutton(self, text='否', variable=self.v_citizen, value=0)
        self.l_meal = tk.Label(self, text='飯店供餐:', font=f1)
        self.v_meal = tk.StringVar()
        self.v_meal.set(0)
        self.yes3 = tk.Radiobutton(self, text='是', variable=self.v_meal, value=1)
        self.no3 = tk.Radiobutton(self, text='否', variable=self.v_meal, value=0)

        # 建立文字區域以顯示輸出結果

        # self.scroller.configure(command=self.mytext.yview)

        # 使用 grid() 設定元件位置
        self.b1.grid(row=5, column=8)
        self.l2.grid(row=0, column=0, columnspan=10)
        self.l_price.grid(row=2, column=0, sticky=tk.W)
        self.a.grid(row=2, column=1)
        self.b.grid(row=2, column=2)
        self.c.grid(row=2, column=3)
        self.l_district.grid(row=1, column=0, sticky=tk.W)
        self.optionmenu.grid(row=1, column=1)
        self.l_nation.grid(row=3, column=0, sticky=tk.W)
        self.yes.grid(row=3, column=1)
        self.no.grid(row=3, column=2)
        self.l_citizen.grid(row=4, column=0, sticky=tk.W)
        self.yes2.grid(row=4, column=1)
        self.no2.grid(row=4, column=2)
        self.l_meal.grid(row=5, column=0, sticky=tk.W)
        self.yes3.grid(row=5, column=1)
        self.no3.grid(row=5, column=2)
        # columnspan=10) # yscrollcommand=self.scroller.set(last))
        # self.scroller.configure(command=self.mytext.yview)
        # self.can.grid(row=8, column=0, columnspan=10)


my_input = UserInput()
my_input.master.title('北市防疫旅館')
my_input.mainloop()  # 呼叫視窗
