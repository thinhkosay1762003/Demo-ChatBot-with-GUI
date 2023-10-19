from tkinter import *
import time
import tkinter.messagebox
import main
import json

data= json.loads(open('data.json', encoding='utf-8').read())
window_size = "700x800"

class ChatInterface(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.tl_bg = "#EEEEEE"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"
        self.font = "Verdana 10"

        menu = Menu(self.master)
        self.master.config(menu=menu, bd=5)
        # Menu bar

        #Chức năng
        file = Menu(menu, tearoff=0)
        menu.add_cascade(label="Chức năng", menu=file)
        # file.add_command(label="Save Chat Log", command=self.save_chat)
        file.add_command(label="Xoá chat", command=self.clear_chat)
        #  file.add_separator()
        file.add_command(label="Thoát", command=self.chatexit)

        #Hỗ trợ
        help_option = Menu(menu, tearoff=0)
        menu.add_cascade(label="Hỗ trợ", menu=help_option)
        # help_option.add_command(label="Features", command=self.features_msg)
        help_option.add_command(label="Về P-Bot", command=self.msg)
        help_option.add_command(label="Tác giả", command=self.about)


        self.text_frame = Frame(self.master, bd=6)
        self.text_frame.pack(expand=True, fill=BOTH)

        # scrollbar for text box
        self.text_box_scrollbar = Scrollbar(self.text_frame, bd=0)
        self.text_box_scrollbar.pack(fill=Y, side=RIGHT)

        # contains messages
        self.text_box = Text(self.text_frame, yscrollcommand=self.text_box_scrollbar.set, state=DISABLED,
                             bd=1, padx=6, pady=6, spacing3=8, wrap=WORD, bg=None, font="Verdana 10", relief=GROOVE,
                             width=10, height=1)
        self.text_box.pack(expand=True, fill=BOTH)
        self.text_box_scrollbar.config(command=self.text_box.yview)

        # frame containing user entry field
        self.entry_frame = Frame(self.master, bd=1)
        self.entry_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # entry field
        self.entry_field = Entry(self.entry_frame, bd=1, justify=LEFT)
        self.entry_field.pack(fill=X, padx=6, pady=6, ipady=3)


        # frame containing send button and emoji button
        self.send_button_frame = Frame(self.master, bd=0)
        self.send_button_frame.pack(fill=BOTH)

        # send button
        self.send_button = Button(self.send_button_frame, text="Send", width=5, relief=GROOVE, bg='white',
                                  bd=1, command=lambda: self.send_message_insert(None), activebackground="#FFFFFF",
                                  activeforeground="#000000")
        self.send_button.pack(side=LEFT, ipady=8, expand=True)
        self.master.bind("<Return>", self.send_message_insert)

    def clear_chat(self):
        self.text_box.config(state=NORMAL)
        self.text_box.delete(1.0, END)
        self.text_box.delete(1.0, END)
        self.text_box.config(state=DISABLED)

    def chatexit(self):
        exit()

    def msg(self):
        tkinter.messagebox.showinfo('Info','P-Bot Chatbot cộng đồng hỗ trợ sinh viên PTIT')

    def about(self):
        tkinter.messagebox.showinfo("Người phát triển chatbot",
                                    "1.Trần Đức Thịnh\n2.Vũ Minh Quân\n3.Trần Quang Huy\n4.Nguyễn Quang Hưởng")


#Lệnh được nhập sẽ được đưa vào user_input, dùng hmg predic_class bên main để đoán chủ đề được nhập và bot sẽ đưa câu trả lời
    def send_message_insert(self, message):
        user_input = self.entry_field.get()
        pr1 = "Sinh viên : " + user_input + "\n"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, pr1)
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)
        chu_de=main.predict_class(user_input)
        res = main.get_response(chu_de, data, user_input)
        pr = "P-Bot : "+ res + "\n"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, pr)
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)
        self.entry_field.delete(0, END)

def chatbot():
    root = Tk()
    a = ChatInterface(root)
    root.geometry(window_size)
    root.title("P-Bot Chatbot cộng đồng hỗ trợ sinh viên PTIT")
    root.mainloop()
if __name__ == "__main__":
    chatbot()