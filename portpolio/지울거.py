from tkinter.simpledialog import *
from tkinter import *

root = Tk()
root.title('포트폴리오')
root.geometry("380x210+300+100")
root.resizable(False, False)

Label1 = Label(root, width = 40, height = 1, text = "오락실에 오신걸 환영합니다.")
Label1.grid(row = 0 , column = 0, columnspan = 4)
Label2 = Label(root, width = 40, height = 1, text = "Game을 눌러 이용하세요.")
Label2.grid(row = 1 , column = 0, columnspan = 4)

enter1 = Label(root, width = 40, height = 1, text = "")
enter1.grid(row = 2 , column = 0, columnspan = 3)

Label4 = Label(root, width = 11, height = 1, text = "오징어 게임")
Label4.grid(row = 3 , column = 0, columnspan = 3, sticky="w")

button1 = Button(root, width = 12, height = 2, text = "게임 시작", command=squid)
button1.grid(row = 4 , column = 0)
button2 = Button(root, width = 12, height = 2, text = "순위 보기", command=squid_ranking)
button2.grid(row = 4 , column = 1)
button3 = Button(root, width = 12, height = 2, text = "초기화", command=squid_rank_reset)
button3.grid(row = 4 , column = 2)

Label5 = Label(root, width = 15, height = 1, text = "유성피하기 게임")
Label5.grid(row = 5 , column = 0, columnspan = 3, sticky="w")

button4 = Button(root, width = 12, height = 2, text = "게임 시작", command=dodge)
button4.grid(row =6 , column = 0)
button5 = Button(root, width = 12, height = 2, text = "순위 보기", command=dodge_ranking)
button5.grid(row =6 , column = 1)
button6 = Button(root, width = 12, height = 2, text = "초기화", command=dodge_rank_reset)
button6.grid(row =6 , column = 2)

button4 = Button(root, width = 10, height = 6, text = "종료", command=exit)
button4.grid(row = 4, column = 3, rowspan = 4)
root.mainloop()