import tkinter as tk
from tkinter import messagebox
import random
import pyperclip
import json

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

class Main(tk.Tk):

    def __init__(self) -> None:
        super().__init__()

        self.title('Password Manager')
        self.config(padx=20, pady=20)

        frame = Application(self)
        frame.grid()
        self.mainloop()


class Application(tk.Frame):

    def __init__(self, master=None, cnf={}, **kw) -> None:
        super().__init__(master, cnf, **kw)

        # Logo
        self.canvas = tk.Canvas(self, width=200, height=200, highlightthickness=0)
        master.logo_img = logo_img = tk.PhotoImage(file='./logo.png')
        self.canvas.create_image(100, 100, image=logo_img)

        self.canvas.grid(row=0, column=1)

        # Website
        self.website_label = tk.Label(self, text='Website:')
        self.website_label.grid(row=1, column=0)

        self.website_entry = tk.Entry(self, width=33)
        self.website_entry.focus()
        self.website_entry.grid(row=1, column=1)

        # Search
        self.search_button = tk.Button(self, text='Search', width=14, command=lambda: self.find_password(self.website_entry.get()))
        self.search_button.grid(row=1, column=2)

        master.bind('<Return>', lambda enter: self.search_button.invoke())
        
        # Email/username
        self.email_label = tk.Label(self, text='Email/Username:')
        self.email_label.grid(row=2, column=0)

        self.email_entry = tk.Entry(self, width=51)
        self.email_entry.insert(0, 'my@email.com')
        self.email_entry.grid(row=2, column=1, columnspan=2)

        # Password
        self.pwd_label = tk.Label(self, text='Password:')
        self.pwd_label.grid(row=3, column=0)

        self.pwd_entry = tk.Entry(self, width=33)
        self.pwd_entry.grid(row=3, column=1)

        self.pwd_gen_button = tk.Button(self, text='Generate Password', command=self.generate_password)
        self.pwd_gen_button.grid(row=3, column=2)

        #Add
        self.add_button = tk.Button(self, text='Add', width=43, command=self.save)
        self.add_button.grid(row=4, column=1, columnspan=2)

    def save(self, event=None):
        website = self.website_entry.get()
        email = self.email_entry.get()
        password = self.pwd_entry.get()
        new_data = {
            website: {
                'email': email,
                'password': password
            }
        }

        if len(website) == 0 or len(password) == 0:
            messagebox.showerror(title='Oops', message='Please don\'t leave any fields empty!')
        else:
            if self.confirm(website, email, password):
                try:
                    with open('data.json', 'r') as file:
                        data = json.load(file)
                except (FileNotFoundError, json.JSONDecodeError):
                    data = new_data
                    
                    with open('data.json', 'w') as file:
                        json.dump(data, file, indent=4)
                else:
                    data.update(new_data)

                    with open('data.json', 'w') as file:
                        json.dump(data, file, indent=4)
                finally:                    
                    self.website_entry.delete(0, tk.END)
                    self.pwd_entry.delete(0, tk.END)

    def confirm(self, website, email, password):
        return messagebox.askokcancel(title='Confirmation', message=f'These are the details entered:\nWebsite: {website}\nEmail: {email}\nPassword: {password}\nIs it ok to save?')

    def find_password(self, website):
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
                email = data[website]['email']
                password = data[website]['password']
                messagebox.showinfo(title=website, message=f'Email: {email}\nPassword: {password}')
        except FileNotFoundError:
            messagebox.showerror(message='No Data File Found.')
        except (json.JSONDecodeError, KeyError):
            messagebox.showerror(message=f'No details for {website} exist.')            

    def generate_password(self):
        nr_letters = random.randint(8, 10)
        nr_symbols = random.randint(2, 4)
        nr_numbers = random.randint(2, 4)

        password_list = [random.choice(LETTERS) for char in range(nr_letters)] + \
                        [random.choice(NUMBERS) for char in range(nr_numbers)] + \
                        [random.choice(SYMBOLS) for char in range(nr_symbols)]

        random.shuffle(password_list)

        password = ''.join(password_list)

        self.pwd_entry.delete(0, tk.END)
        self.pwd_entry.insert(0, password)

        pyperclip.copy(password)