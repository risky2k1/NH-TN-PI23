import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random
import datetime
import os

# Load data
df = pd.read_csv('quiz.csv')
questions = df.sample(10).to_dict(orient='records')  # Random 10 questions
results = []

# GUI
class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz App")
        self.username = ""
        self.q_index = 0
        self.score = 0

        self.start_screen()

    def start_screen(self):
        self.clear()
        self.label = tk.Label(self.master, text="Nhập tên của bạn:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.master)
        self.entry.pack(pady=5)

        self.button = tk.Button(self.master, text="Bắt đầu", command=self.start_quiz)
        self.button.pack(pady=10)

    def start_quiz(self):
        self.username = self.entry.get().strip()
        if not self.username:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên.")
            return
        self.show_question()

    def show_question(self):
        self.clear()
        if self.q_index >= len(questions):
            self.show_result()
            return

        q = questions[self.q_index]
        self.current_question = q

        tk.Label(self.master, text=f"Câu {self.q_index+1}: {q['question']}").pack(pady=10)

        self.var = tk.StringVar()

        for option in ['A', 'B', 'C', 'D']:
            text = f"{option}. {q[f'option_{option.lower()}']}"
            tk.Radiobutton(self.master, text=text, variable=self.var, value=option).pack(anchor='w')

        tk.Button(self.master, text="Trả lời", command=self.submit_answer).pack(pady=10)

    def submit_answer(self):
        answer = self.var.get()
        if not answer:
            messagebox.showwarning("Cảnh báo", "Bạn chưa chọn đáp án!")
            return

        q = self.current_question
        is_correct = answer == q['correct_answer']
        if is_correct:
            self.score += 1

        results.append({
            'username': self.username,
            'question': q['question'],
            'correct_answer': q['correct_answer'],
            'user_answer': answer,
            'is_correct': is_correct,
            'timestamp': datetime.datetime.now().isoformat()
        })

        self.q_index += 1
        self.show_question()

    def show_result(self):
        self.clear()
        tk.Label(self.master, text=f"Hoàn thành, {self.username}!").pack(pady=5)
        tk.Label(self.master, text=f"Số câu đúng: {self.score}/10").pack(pady=5)
        tk.Label(self.master, text=f"Tỷ lệ đúng: {self.score*10}%").pack(pady=5)

        wrongs = [r for r in results if not r['is_correct']]
        if wrongs:
            tk.Label(self.master, text="Các câu sai:").pack(pady=10)
            for r in wrongs:
                tk.Label(self.master, text=f"❌ {r['question']} | Đúng: {r['correct_answer']} | Bạn chọn: {r['user_answer']}").pack(anchor='w')

        tk.Button(self.master, text="Thoát", command=self.master.quit).pack(pady=20)

        # Lưu file kết quả
        self.save_result()

    def save_result(self):
        filename = 'result.csv'
        df_result = pd.DataFrame(results)
        if os.path.exists(filename):
            df_result.to_csv(filename, mode='a', index=False, header=False)
        else:
            df_result.to_csv(filename, index=False)

    def clear(self):
        for widget in self.master.winfo_children():
            widget.destroy()

# Khởi động App
root = tk.Tk()
root.geometry("600x400")
app = QuizApp(root)
root.mainloop()
