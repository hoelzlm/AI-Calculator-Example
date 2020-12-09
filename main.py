import tkinter as tk
from PIL import Image, ImageDraw

import numpy as np
import tensorflow


class UserInterface(tk.Frame):
    def __init__(self, predict_image, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Handschrift Taschenrechner")
        self.create_widgets()

        self.predict_image = predict_image

        self.image = Image.new("RGB", (28, 28))
        self.draw = ImageDraw.Draw(self.image)
        self.reset()


    def create_widgets(self):
        self.input_frame = tk.Frame(self.master, width=312, height=50, bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.input_frame.pack(side=tk.TOP)
        
        self.result = tk.StringVar()
        
        self.result_text = tk.Entry(self.input_frame, textvariable=self.result, width=50, bg="#eee", bd=0, justify=tk.RIGHT)
        self.result_text.grid(row=0, column=0)
        self.result_text.pack(ipady=10)

        self.canvas_frame = tk.Frame(self.master, width=310, height=272.5, bg="black")
        self.canvas_frame.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        self.canvas = tk.Canvas(self.canvas_frame, bg="#eee")
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.grid(row=0, column=0)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.button_add = tk.Button(self.canvas_frame, text=" Add ", command=lambda: self.press('a'), height= 3, bd = 0, bg = "#eee", cursor = "hand2")
        self.button_add.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        self.button_reset = tk.Button(self.canvas_frame, text=" Reset ", command=lambda: self.press('c'), height= 3, bd = 0, bg = "#eee", cursor = "hand2")
        self.button_reset.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)

        self.button_frame = tk.Frame(self.master, width=10, height=272.5, bg="grey")
        self.button_frame.pack(side=tk.RIGHT)

        self.button_plus = tk.Button(self.button_frame, text=" + ", command=lambda: self.press('+'), width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2")
        self.button_plus.grid(row=1, column=0, padx = 1, pady = 1)

        self.button_minus = tk.Button(self.button_frame, text=" - ", command=lambda: self.press('-'), width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2")
        self.button_minus.grid(row=2, column=0, padx = 1, pady = 1)

        self.button_divide = tk.Button(self.button_frame, text=" / ", command=lambda: self.press('/'), width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2")
        self.button_divide.grid(row=3, column=0, padx = 1, pady = 1)

        self.button_multiply = tk.Button(self.button_frame, text=" * ", command=lambda: self.press('*'), width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2")
        self.button_multiply.grid(row=4, column=0, padx = 1, pady = 1)

        self.button_equal = tk.Button(self.button_frame, text=" = ", command=lambda: self.press('='), width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2")
        self.button_equal.grid(row=5, column=0, padx = 1, pady = 1)

    def press(self, inp):
        if str(inp) == 'c':
            self.reset()
        
        elif str(inp) == 'a':
            self.add_iamge()

        elif str(inp) != '=':
            self.result.set(str(self.result.get()) + str(inp))
        
        else:
            try:
                expression = self.result.get()
                result = str(eval(expression))
                self.result.set(result)
            except Exception as error:
                print(error)

    def paint(self, event):
        x1, y1 = ( event.x - 3 ), ( event.y - 3 )
        x2, y2 = ( event.x + 3 ), ( event.y + 3 )
        self.canvas.create_oval( x1, y1, x2, y2, fill="black")
        self.draw.ellipse([(x1, y1), (x2, y2)], fill=(255, 255, 255))

    def reset(self):
        self.canvas.delete("all")
        self.canvas.update()
        self.image = Image.new("RGB", (self.canvas.winfo_width(), self.canvas.winfo_height()))
        self.draw = ImageDraw.Draw(self.image)
    
    def add_iamge(self):
        image = self.image.convert("L").resize((28, 28))
        image.show() # DEBUG ONLY
        
        img_resized = np.resize(image, (28, 28, 1))
        img_buffer = np.array(img_resized)
        img_buffer = img_buffer.reshape(1,28,28,1)
        img_buffer = img_buffer.astype('float32')
        img_buffer = img_buffer / 255

        result = self.predict_image(img_buffer)
        self.press(result)
        self.reset()


def predict_image(img):
    model = tensorflow.keras.models.load_model('MNIST.h5')
    prediction = model.predict_classes(img)
    
    print(prediction)
    
    return prediction[0]

if __name__ == "__main__":
    
    root = tk.Tk()
    app = UserInterface(master=root, predict_image=predict_image)
    app.mainloop()