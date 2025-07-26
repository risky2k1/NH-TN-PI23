from tkinter import Tk, Entry, Button, Label, Radiobutton, messagebox, Listbox
import pandas as pd
import tkinter as tk

# Khai báo biến user_name toàn cục
user_name = ""
question_index = 0
score = 0


def destroy_widget():
    for widget in root.winfo_children():
        widget.destroy()


def show_name():
    def submit_name():
        global user_name
        user_name = name_entry.get()
        destroy_widget()

        show_question()

    name_entry = Entry()
    name_entry.pack()
    Button(text='Nhập tên', command=submit_name).pack()


def show_question():
    destroy_widget()

    global question_index, var


    if question_index >= len(questions):
        show_result()
        return

    question = questions[question_index]

    Label(text=question['Question Name']).pack()

    options = ['1', '2', '3', '4']
    var = tk.StringVar()

    for option in options:
        text = 'Answer ' + option
        Radiobutton(text=question[text], variable=var, value=option).pack()
    
    
    def next_question():
        global question_index, score

        question_index += 1

        selected_answer = var.get()

        if not selected_answer:
            messagebox.showwarning('Warning','Vui lòng chọn đáp án')

        if int(selected_answer) == question['Correct Answer']:
            score += 1

        show_question()
    Button(text='Câu tiếp theo', command=next_question).pack()

def show_result():
    destroy_widget()

    Label(text=f'Kết quả làm bào của {user_name} : ').pack()
    Label(text=f'Bạn làm đúng {score} / {len(questions)}').pack()


if __name__ == "__main__":
    root = Tk()
    root.title('Quiz app')
    root.minsize(600, 400)

    # Đọc File chứa các câu hỏi
    data = pd.read_csv('questions.csv')
    # Lấy ra 10 câu ngẫu nhiên từ file
    questions = data.sample(3).to_dict(orient="records")

    show_name()

    root.mainloop()
