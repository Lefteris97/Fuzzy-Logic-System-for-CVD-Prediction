import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from fuzzy_logic import FuzzyLogicSystem


class FuzzyLogicApp:
    def __init__(self):
        # self.root = root
        root.title("Risk of CVD")

        self.fuzzy_logic = FuzzyLogicSystem()

        root.configure(bg='#2E2D2D')
        root.iconbitmap('Icon/heart_health.ico')

        root.geometry('1100x580')
        root.resizable(0, 0)

        inputs_frame = LabelFrame(root, padx=5, pady=5, bg='#2E2D2D', bd=0, highlightthickness=0)
        inputs_frame.grid(row=0, column=0, padx=10, pady=10)

        img_frame = LabelFrame(root, padx=5, pady=5, bg='#2E2D2D', bd=0, highlightthickness=0)
        img_frame.grid(row=0, column=1, padx=10, pady=10)

        self.heart_img = ImageTk.PhotoImage(Image.open('Images/heart.png'))
        img_label = Label(img_frame, image=self.heart_img, bg='#2E2D2D')
        img_label.pack()

        self.create_widgets(inputs_frame)

    def create_widgets(self, inputs_frame):
        self.inputs = {}

        labels = [
            "General Health (1-10):", "Systolic BP (70-220):", "Cholesterol (70-300):",
            "Age (1-100):", "Physical Health (0-30):", "Stroke:", "Diabetes:", "Difficulty Walking:"
        ]

        keys = [
            "genHlth", "systolicBp", "cholesterol", "age", "physHlth", "stroke",
            "diabetes", "diffWalk"
        ]

        for idx, (label_text, key) in enumerate(zip(labels, keys)):
            label = Label(inputs_frame, text=label_text, fg='green', bg='#2E2D2D', font=('Arial', 14))
            label.grid(row=idx, column=0, padx=10, pady=5, sticky='W')

            if key in ["stroke", "diabetes", "diffWalk"]:
                var = IntVar(value=0)
                yes_rb = Radiobutton(inputs_frame, text="Yes", variable=var, value=1, fg='green', bg='#2E2D2D', font=('Arial', 12), anchor='w')
                no_rb = Radiobutton(inputs_frame, text="No", variable=var, value=0, fg='green', bg='#2E2D2D', font=('Arial', 12), anchor='w')
                yes_rb.grid(row=idx, column=1, sticky='W')
                no_rb.grid(row=idx, column=2, sticky='W')
                self.inputs[key] = var

            else:  # For numeric entries
                entry = Entry(inputs_frame, highlightthickness=3)
                entry.config(highlightbackground='grey', highlightcolor='green', width=3, font=('Arial', 14))
                entry.grid(row=idx, column=1)
                self.inputs[key] = entry

        button = Button(inputs_frame, text="Diagnose", command=self.diagnose, bg='white', fg='#678C54', padx=10, pady=5, cursor='hand2', font=('Arial', 12, 'bold'))
        button.grid(row=len(labels), column=0, columnspan=2, pady=30)

        self.result_label = Label(inputs_frame, text="CVD Risk: ", fg='green', bg='#2E2D2D', font=('Arial', 14))
        self.result_label.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)

    def diagnose(self):
        try:
            genHlth = int(self.inputs["genHlth"].get())
            systolicBp = int(self.inputs["systolicBp"].get())
            cholesterol = int(self.inputs["cholesterol"].get())
            age = int(self.inputs["age"].get())
            physHlth = int(self.inputs["physHlth"].get())

            # Use the IntVar values from radio buttons for binary fields
            stroke = self.inputs["stroke"].get()
            diabetes = self.inputs["diabetes"].get()
            diffWalk = self.inputs["diffWalk"].get()

            cvd_risk = self.fuzzy_logic.compute_cvd_risk(
                genHlth, systolicBp, cholesterol, age, stroke, diabetes, physHlth, diffWalk
            )

            self.result_label.config(text=f"CVD Risk: {cvd_risk:.2f}")

        except ValueError:
            self.result_label.config(text="Please enter valid numeric values.")


if __name__ == '__main__':
    root = tk.Tk()
    app = FuzzyLogicApp()
    root.mainloop()