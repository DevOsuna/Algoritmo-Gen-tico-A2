from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
from typing import List
import tkinter as tk
import pandas as pd
import os 

import GeneticAlgorithm as GA

# Inicializar tkinter GUI
root = tk.Tk()

root.title("Algoritmo Genético - Problema de Cobertura Máxima (PLMC)")
root.geometry("750x500")
root.pack_propagate(False) # El tamaño del root no puede ser determinado por los widgets internos.
root.resizable(0, 0)

# Frame para tabla de datos
frame1 = tk.LabelFrame(root, text="Puntos de demanda")
frame1.place(height=180, width=500)

# Frame para tabla de resultados
frame2 = tk.LabelFrame(root, text="Localizaciones óptimas para instalación de brigadas")
frame2.place(height=180, width=500, rely=0.4)

# Frame para acciones
frame3 = tk.LabelFrame(root, text="Parámetros")
frame3.place(height=450, width=210, rely=0, relx=0.7)
frame = tk.Frame(root, bg="green")
ab = tk.Entry(frame)

# Frame para selección de archivo
file_frame = tk.LabelFrame(root, text="Cargar Excel")
file_frame.place(height=50, width=500, rely=0.8, relx=0)

button1 = tk.Button(file_frame, text="Buscar", command=lambda: File_dialog())
button1.place(rely=0, relx=0.85)

button2 = tk.Button(file_frame, text="Cargar", command=lambda: Load_data())
button2.place(rely=0, relx=0.70)

label_file = ttk.Label(file_frame, text="No hay ningún archivo seleccionado")
label_file.place(rely=0, relx=0)

button3 = tk.Button(frame3, text="Iniciar", command=lambda: Execute_GA())
button3.config(height = 2, width = 20)
button3.place(rely=0.9, relx=0.15)

# lb_num_brigades = ttk.Label(frame3, text="Número de brigadas")
# lb_num_brigades.place(rely=0.4, relx=0.2)

# num_brigades = ttk.Entry(frame3, justify='center')
# num_brigades.pack(expand=1)

lb_num_brigades = ttk.Label(frame3, text="Número de brigadas")
lb_num_brigades.place(rely=0.1, relx=0.2)

num_brigades = ttk.Entry(frame3)
num_brigades.place(rely=0.15, relx=0.2)

lb_txts_percentage = ttk.Label(frame3, text="Porcentaje Cubierto")
lb_txts_percentage.place(rely=0.3, relx=0.2)

lb_num_percentage = ttk.Label(frame3, text="0%")
lb_num_percentage.place(rely=0.35, relx=0.2)

lb_txt_demands = ttk.Label(frame3, text="Total de demandas")
lb_txt_demands.place(rely=0.5, relx=0.2)

lb_num_demands = ttk.Label(frame3, text="0")
lb_num_demands.place(rely=0.55, relx=0.2)

lb_txt_covered = ttk.Label(frame3, text="Demandas cubiertas")
lb_txt_covered.place(rely=0.7, relx=0.2)

lb_num_covered = ttk.Label(frame3, text="0")
lb_num_covered.place(rely=0.75, relx=0.2)


# Treeview Widget (frame1)
tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1, relwidth=1) # Establecer ancho y alto al 100% del contenedeor (frame1)

treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview) # Scroll en eje "y" para vista de la tabla
treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview) # Scroll en eje "x" para vista de la tabla
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # Asignar scrolls a la tabla (TreeView)
treescrollx.pack(side="bottom", fill="x") # Fijar scroll-x al inferior de la tabla
treescrolly.pack(side="right", fill="y") # Fijar scroll-y a la derecha de la tabla


# Treeview Widget (frame2)
tv2 = ttk.Treeview(frame2)
tv2.place(relheight=1, relwidth=1)

trees2crolly = tk.Scrollbar(frame2, orient="vertical", command=tv2.yview)
trees2crollx = tk.Scrollbar(frame2, orient="horizontal", command=tv2.xview)
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
trees2crollx.pack(side="bottom", fill="x")
trees2crolly.pack(side="right", fill="y")


"""Abre el explorador de archivo"""
filename = ""
def File_dialog():
    global filename
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Seleccionar un archivo Excel",
                                          filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*")))
    label_file["text"] = os.path.basename(filename)
    return None


"""Cargar archivo seleccionado en la tabla (TreeView)"""
df_rows = None
def Load_data():
    global df_rows
    global filename
    file_path = filename
    try:
        excel_filename = r"{}".format(file_path)
        if excel_filename[-4:] == ".csv":
            df = pd.read_csv(excel_filename)
        else:
            df = pd.read_excel(excel_filename)

    except ValueError:
        tk.messagebox.showerror("Aviso", "El archivo elegido no es válido")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Aviso", f"El archivo no fue encontrado:\n {file_path}")
        return None

    clear_data()
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # Encabezado de la columna = nombre de la columna

    df_rows = df.to_numpy().tolist() # Convertir data frame en lista de listas [[rows], [rows]]
    for row in df_rows:
        tv1.insert("", "end", values=row) # Insetar cada lista dentro de la tabla
    return None


def clear_data():
    tv1.delete(*tv1.get_children())
    return None


def Execute_GA():

    if validate():

        global df_rows
        best, worst, num_generations = GA.genetic_algorithm(df_rows, int(num_brigades.get()))

        if not best:
            tk.messagebox.showerror("Aviso", "Número de brigadas mayor a puntos potenciales de instalación")
        else:
            print("Total de Demandas =", str(GA.getTotalNumDemands()))
            show_solution(best[-1][0]) # [(genome, fitness),(genome, fitness)]
            print('Total Generaciones', len(GA.getDemandsCoveredForGeneration()))
            show_graph_2(GA.getDemandsCoveredForGeneration(), GA.getTotalNumDemands())
            show_graph(best, worst, num_generations)

def validate():
    try:
        if not df_rows:
            tk.messagebox.showerror("Aviso", "Aún no se han cargado datos")
            return False

        if not num_brigades.get():
            tk.messagebox.showerror("Aviso", "Aún no ha asignado un número de brigadas")
            return False

        int(num_brigades.get())
        return True

    except:
        tk.messagebox.showerror("Aviso", "El número de brigadas debe ser entero")
        return False


def show_solution(solution):
    
    tv2["column"] = ("ID", "Demand", "Latitude", "Longitude", "Cover Range (km)")
    tv2["show"] = "headings"
    tv2.heading("ID",text="ID")
    tv2.heading("Demand",text="Demand")
    tv2.heading("Latitude",text="Latitude")
    tv2.heading("Longitude",text="Longitude")
    tv2.heading("Cover Range (km)",text="Cover Range")

    for row in solution:
        tv2.insert("", "end", values=(row.ID, row.demand, row.latitude,
                    row.longitude, row.cover_range))
    


def show_graph(better_chrom: List, worst_chrom: List, num_generations: int):

    better = []
    worst = []

    for bet, wor in zip(better_chrom, worst_chrom):
        better.append(bet[1])
        worst.append(wor[1])
        # plt.plot(x,y,'x')

    plt.plot(better, label = "Better individuals")
    plt.plot(worst, label = "Worst individuals")
    plt.legend()
   
    plt.xlabel('Generations')
    plt.ylabel('Fitness')

    # Máximo número de generaciones en gráfica
    plt.xlim(1, num_generations)

    plt.show()

def show_graph_2(coveredForGeneration: List, totalDemands: int):

    percentage = []
    p = 0

    for covered in coveredForGeneration:
        p = (covered/totalDemands)*100
        print("Porcentaje:", p)
        percentage.append(p)

    plt.plot(percentage, label = "Percentage")
    plt.legend()
   
    plt.xlabel('Generations')
    plt.ylabel('Percentage covered %')

    # Máximo número de generaciones en gráfica
    plt.xlim(1, len(coveredForGeneration))

    lb_num_percentage['text'] = f'{p}%'
    lb_num_demands['text'] = f'{totalDemands}'
    lb_num_covered['text'] = f'{coveredForGeneration[-1]}'

    plt.show()
    
# Run GUI
root.mainloop()