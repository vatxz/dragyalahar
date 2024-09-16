import cv2
import numpy as np
import pyautogui as pg
import easyocr
import tkinter as tk
from tkinter import ttk
import time

# Inicializar el lector de EasyOCR para inglés
reader = easyocr.Reader(['en'])

# Variables globales para vida y mana
vida = 500
mana = 150
running = False

# Función para mejorar la imagen y leer los números
def read_number(x, y, w, h):
    screenshot = np.array(pg.screenshot(region=(x, y, w, h)))
    
    # Convertir a escala de grises
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    
    # Escalar la imagen para hacer los números más grandes
    scale_percent = 300  # porcentaje de aumento
    width = int(gray.shape[1] * scale_percent / 100)
    height = int(gray.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(gray, dim, interpolation=cv2.INTER_AREA)
    
    # Aumentar el contraste y ajustar el brillo
    alpha = 3.0  # Contraste
    beta = -200  # Brillo
    adjusted = cv2.convertScaleAbs(resized, alpha=alpha, beta=beta)
    
    # Aplicar umbralización
    _, binary = cv2.threshold(adjusted, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Usar easyocr para leer el texto
    result = reader.readtext(binary, detail=0)
    
    # Filtrar solo dígitos y corregir errores comunes
    numbers = ''.join([res for res in result if res.isdigit()])
    
    # Corregir confusión común entre 8 y 0
    numbers = numbers.replace('0', '8') if '0' in numbers and len(numbers) == 1 else numbers
    
    # Si no se encontraron dígitos, devuelve None
    if not numbers:
        return None
    
    return numbers

# Coordenadas de la región donde se encuentra el número de vida
life_x, life_y, life_w, life_h = 1865, 302, 55, 15
# Coordenadas de la región donde se encuentra el número de mana
mana_x, mana_y, mana_w, mana_h = 1866, 315, 54, 14

def start_program():
    global running
    running = True
    run_program()

def pause_program():
    global running
    running = False

def update_values():
    global vida, mana
    vida = int(vida_entry.get())
    mana = int(mana_entry.get())
    vida_label.config(text=f"Vida: {vida}")
    mana_label.config(text=f"Mana: {mana}")

def run_program():
    global running
    if not running:
        return
    
    life_number = read_number(life_x, life_y, life_w, life_h)
    mana_number = read_number(mana_x, mana_y, mana_w, mana_h)
    print(f"Vida: {life_number} - Mana: {mana_number}")
    
    if life_number is not None and int(life_number) < vida:
        pg.press('f1')
        print("Presionando F1")
    if mana_number is not None and int(mana_number) < mana:
        pg.press('f2')
        print("Presionando F2")
    
    root.after(500, run_program)  # Tiempo de espera reducido a 0.5 segundos

# Crear la ventana principal
root = tk.Tk()
root.title("Control de Programa")
root.geometry("300x200")

# Botones de control
start_button = ttk.Button(root, text="Start", command=start_program)
start_button.pack()

pause_button = ttk.Button(root, text="Pause", command=pause_program)
pause_button.pack()

# Entradas para editar los valores de vida y mana
vida_label = ttk.Label(root, text="Vida:")
vida_label.pack()
vida_entry = ttk.Entry(root)
vida_entry.insert(0, str(vida))
vida_entry.pack()

mana_label = ttk.Label(root, text="Mana:")
mana_label.pack()
mana_entry = ttk.Entry(root)
mana_entry.insert(0, str(mana))
mana_entry.pack()

update_button = ttk.Button(root, text="Update Values", command=update_values)
update_button.pack()

# Ejecutar la aplicación
root.mainloop()