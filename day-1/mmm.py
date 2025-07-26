from tkinter import Tk, Entry, Button, Label, Radiobutton, messagebox
import pandas as pd
import tkinter as tk

# Khai báo biến toàn cục
user_name = ""
question_index = 0
score = 0
answers = []


def destroy_widget():
    for widget in root.winfo_children():
        widget.destroy()


def show_name():
    def submit_name():
        global user_name
        user_name = name_entry.get().strip()
        if not user_name:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tên!")
            return
        destroy_widget()
        show_question()

    Label(text="Nhập tên của bạn:").pack(pady=10)
    name_entry = Entry()
    name_entry.pack()
    Button(text='Bắt đầu', command=submit_name).pack(pady=10)


def show_question():
    destroy_widget()
    global question_index, var

    if question_index >= len(questions):
        show_result()
        return

    question = questions[question_index]

    Label(text=f"Câu {question_index + 1}: {question['Question Name']}",
          wraplength=500, justify="left").pack(pady=10)

    options = ['1', '2', '3', '4']
    var = tk.StringVar()

    for option in options:
        text = 'Answer ' + option
        Radiobutton(text=question[text], variable=var,
                    value=option).pack(anchor='w')

    def next_question():
        global question_index, score
        selected = var.get()

        if not selected:
            messagebox.showwarning("Lỗi", "Vui lòng chọn một đáp án!")
            return

        if selected == str(question['Correct Answer']):
            score += 1

        question_index += 1
        show_question()

    Button(text='Câu tiếp theo', command=next_question).pack(pady=10)


def show_result():
    destroy_widget()

    Label(text=f"Cảm ơn {user_name} đã hoàn thành bài quiz!",
          font=('Arial', 14)).pack(pady=10)
    Label(text=f"Điểm của bạn: {score}/{len(questions)}",
          font=('Arial', 12)).pack(pady=5)

    Button(text="Thoát", command=root.destroy).pack(pady=10)


if __name__ == "__main__":
    root = Tk()
    root.title('Quiz app')
    root.minsize(600, 400)

    # Đọc File chứa các câu hỏi
    try:
        data = pd.read_csv('questions.csv')
        # Lấy ra 10 câu ngẫu nhiên từ file
        questions = data.sample(3).to_dict(orient="records")
        show_name()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể đọc file questions.csv\n{e}")

    root.mainloop()
