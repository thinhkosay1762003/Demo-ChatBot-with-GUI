from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
import chat_gui


if __name__ == "__main__":
    with open("DSSV.csv", mode="r", encoding="utf-8-sig") as file:
        header = file.readline()
        data_sv = file.readlines()
    #Khởi tạo cửa sổ đăng nhập
    root=Tk()
    root.title('Login')  #Tiêu đề
    root.geometry('925x500+300+200') #cửa sổ kích cỡ 925x500 xuất hiện ở vị trí 300,200 tính từ trái, trên cùng màn hình
    root.configure(bg="red") #Đặt màu nền thành màu trắng
    root.resizable(False,False) #Khoá kích cỡ cửa sổ để không mở rộng được

    #Chèn ảnh
    img = PhotoImage(file='mixue.png')
    label=Label(root,image=img,bg='white').place (x=127,y=50)
    tentruong=Label(text="PTIT Assistant",fg="white",bg='red',font=('Roboto',23,'bold'))
    tentruong.place(x=133,y=280)
    tentruong=Label(text="Chatbot phục vụ cộng đồng sinh viên PTIT",fg="white",bg='red',font=('Roboto',11,'bold'))
    tentruong.place(x=90,y=320)
    hd = Label( text='© Sản phẩm của sinh viên nhóm 16\n Lớp lập trình Python 07\n Giảng viên Vũ Minh Mạnh', fg="white",bg='red', font=('Helvetica', 11))
    hd.place(x=120, y=440)

    #lấy giá trị của email và password và tra cứu trong DSSV.csv
    def signin():
        email=user.get()
        password=msv.get()
        email = f'"{email}"'
        password = f'"{password}"'
        for row in data_sv:
            row_list = row.split(",")
            check_email = row_list[7]
            if email.lower()==check_email[:-1].lower():
                if password.upper()== row_list[1]:
                   return f'{row_list[2][1:-1]} {row_list[3][1:-1]}'
        return None

    #Tạp cửa sổ mới
    def new_app():
        user_name = signin()
        if user_name is not None:
            root.destroy()
            chat_gui.chatbot()
        else:
            messagebox.showerror("Lỗi","Sai mã sinh viên hoặc email")

    #Tạo dòng chữ "Nhập MSV"

    frame=Frame(root,width=445,height=500,bg="white")
    frame.place(x=480,y=0)
    photo = Image.open('user.jpg')
    avatar=ImageTk.PhotoImage(photo)
    label=Label(frame,image=avatar,bg='white').place (x=115,y=25)
    heading = Label(frame,text='Đăng nhập',fg='#8B2323',bg='white',font=('Roboto',21,'bold'))
    heading.place(x=150,y=20)

    #Lệnh dưới để xoá chữ "Mã sinh viên" và thêm chữ đấy vào khi click vô ô nhập MSV
    def on_enter(e):
        name = user.get()
        if name == 'Email sinh viên':
            user.delete(0,'end')
    def on_leave(e):
        name=user.get()
        if name=='':
            user.insert(0,'Email sinh viên')

    #Tạo ô nhập email
    user=Entry(frame,width=35,fg='black',border=0,bg="white",font=('Microsoft YaHei UI Light',11))
    user.place(x=70,y=120)
    user.insert(0,'Email sinh viên')
    Frame(frame,width=295,height=2,bg='black').place(x=65,y=147)
    user.bind('<FocusIn>',on_enter)
    user.bind('<FocusOut>',on_leave)
    #Tạo ô nhập msv
    def on_enter_pass(e):
        password=msv.get()
        if password=='Mã sinh viên':
            msv.delete(0,'end')
    def on_leave_pass(e):
        password=msv.get()
        if password=='':
            msv.insert(0,'Mã sinh viên')
    msv=Entry(frame,width=25,fg='black',border=0,bg="white",font=('Microsoft YaHei UI Light',11))
    msv.place(x=70,y=160)
    msv.insert(0,'Mã sinh viên')
    Frame(frame,width=295,height=2,bg='black').place(x=65,y=187)
    msv.bind('<FocusIn>',on_enter_pass)
    msv.bind('<FocusOut>',on_leave_pass)

    #Nút đăng nhập, lệnh command=new_app (khi click vào sẽ chạy new_app()
    Button(frame,width=39,padx=7,text="Đăng nhập",bg="#57a1f8",fg='white',border=0,command=new_app).place(x=70,y=220)



    label=Label(frame,text="Sinh viên dùng Email đuôi @stu.ptit.edu.vn của trường để đăng nhập",fg='black',bg='white',font=('Microsoft YaHei UI Light',9))
    label.place(x=30,y=275)
    mail=Label(frame,text="@stu.ptit.edu.vn",fg='blue',bg='white',font=('Microsoft YaHei UI Light',9))
    mail.place(x=178,y=275)

    root.mainloop() #Vòng lặp để duy trì cửa sổ hiển thị