import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import requests
import json
import os
from datetime import datetime

# Настройки API
API_KEY = "ВАШ_КЛЮЧ"  # Замените на ваш ключ от exchangerate-api.com
BASE_URL = f"https://exchangerate-api.com{API_KEY}/latest/"

class CurrencyConverter(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Currency Converter")
        self.geometry("500x600")
        
        self.history_file = "history.json"
        self.currencies = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY"]

        # UI Элементы
        self.label_amount = ctk.CTkLabel(self, text="Сумма:")
        self.label_amount.pack(pady=(20, 0))

        self.entry_amount = ctk.CTkEntry(self, placeholder_text="Введите число")
        self.entry_amount.pack(pady=10)

        self.combo_from = ctk.CTkComboBox(self, values=self.currencies)
        self.combo_from.set("USD")
        self.combo_from.pack(pady=10)

        self.combo_to = ctk.CTkComboBox(self, values=self.currencies)
        self.combo_to.set("RUB")
        self.combo_to.pack(pady=10)

        self.btn_convert = ctk.CTkButton(self, text="Конвертировать", command=self.convert)
        self.btn_convert.pack(pady=20)

        self.history_box = ctk.CTkTextbox(self, width=400, height=200)
        self.history_box.pack(pady=10)
        
        self.load_history()

    def convert(self):
        amount = self.entry_amount.get()
        from_curr = self.combo_from.get()
        to_curr = self.combo_to.get()

        # Валидация
        try:
            amount = float(amount)
            if amount <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите положительное число!")
            return

        # Запрос к API
        try:
            response = requests.get(BASE_URL + from_curr)
            data = response.json()
            rate = data['conversion_rates'][to_curr]
            result = round(amount * rate, 2)
            
            # Отображение
            record = f"{datetime.now().strftime('%H:%M:%S')} | {amount} {from_curr} -> {result} {to_curr}"
            self.save_history(record)
            self.update_history_display(record)
            
        except Exception as e:
            messagebox.showerror("Ошибка API", f"Не удалось получить курс: {e}")

    def save_history(self, record):
        history = []
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        
        history.append(record)
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
                for item in history:
                    self.update_history_display(item)

    def update_history_display(self, record):
        self.history_box.insert("0.0", record + "\n")

if __name__ == "__main__":
    app = CurrencyConverter()
    app.mainloop()
