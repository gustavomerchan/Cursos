from pytube import Playlist, YouTube
from tkinter import *









root = Tk()

icon = PhotoImage(file='C:\\Users\\gustavo.gomes\\Desktop\\Cursos\\Python\\Python_Udemy\\Hopstarter-Sleek-Xp-Basic-Download.256.png')
root.iconphoto(True,icon)
root.title('Baixador de Músicas')
root.geometry('600x300')


label_url_input = Label(root,width=50,text='Cole a url para fazer o download da playlist')
label_url_input.place(x=115,y=90)

url_input = Entry(root, width=60)
url_input.place(x=110,y=130)

btn_download = Button(root,width=10,text='Baixar Bitch',relief='raised',fg='white',bg='green')
btn_download.place(x=250,y=170)






root.mainloop()








