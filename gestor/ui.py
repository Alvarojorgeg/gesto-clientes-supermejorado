from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING
from gestor.helpers import dni_valido
from gestor.database import Clientes

class CenterWidgetMixin:
    def center(self):
        self.update()
        w, h = self.winfo_width(), self.winfo_height()
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y = (ws - w) // 2, (hs - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title('Gestor de clientes')
        self.build()
        self.center()

    def build(self):
        top = Frame(self)
        top.pack()
        self.treeview = ttk.Treeview(top, columns=('DNI', 'Nombre', 'Apellido'), show='headings')
        for col in ('DNI', 'Nombre', 'Apellido'):
            self.treeview.heading(col, text=col)
            self.treeview.column(col, anchor=CENTER)
        for cliente in Clientes.lista:
            self.treeview.insert('', END, iid=cliente.dni, values=(cliente.dni, cliente.nombre, cliente.apellido))
        scrollbar = Scrollbar(top, command=self.treeview.yview)
        self.treeview.config(yscrollcommand=scrollbar.set)
        self.treeview.pack(side=LEFT)
        scrollbar.pack(side=RIGHT, fill=Y)

        bottom = Frame(self)
        bottom.pack(pady=10)
        Button(bottom, text="Crear", command=self.create_client_window).grid(row=0, column=0)
        Button(bottom, text="Modificar", command=self.edit_client_window).grid(row=0, column=1)
        Button(bottom, text="Borrar", command=self.delete).grid(row=0, column=2)

    def delete(self):
        cliente = self.treeview.focus()
        if cliente:
            campos = self.treeview.item(cliente, 'values')
            if askokcancel("Confirmación", f"¿Borrar a {campos[1]} {campos[2]}?", icon=WARNING):
                self.treeview.delete(cliente)
                Clientes.borrar(campos[0])

    def create_client_window(self):
        CreateClientWindow(self)

    def edit_client_window(self):
        EditClientWindow(self)

class CreateClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Crear cliente')
        self.parent = parent
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()

    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)
        Label(frame, text="DNI").grid(row=0, column=0)
        Label(frame, text="Nombre").grid(row=0, column=1)
        Label(frame, text="Apellido").grid(row=0, column=2)
        self.dni = Entry(frame)
        self.nombre = Entry(frame)
        self.apellido = Entry(frame)
        self.dni.grid(row=1, column=0)
        self.nombre.grid(row=1, column=1)
        self.apellido.grid(row=1, column=2)
        bottom = Frame(self)
        bottom.pack(pady=10)
        Button(bottom, text="Crear", command=self.create_client).grid(row=0, column=0)
        Button(bottom, text="Cancelar", command=self.destroy).grid(row=0, column=1)

    def create_client(self):
        dni, nombre, apellido = self.dni.get(), self.nombre.get(), self.apellido.get()
        if not dni_valido(dni, Clientes.lista): return
        self.parent.treeview.insert('', END, iid=dni, values=(dni, nombre, apellido))
        Clientes.crear(dni, nombre, apellido)
        self.destroy()

class EditClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Actualizar cliente')
        self.parent = parent
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()

    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)
        Label(frame, text="DNI").grid(row=0, column=0)
        Label(frame, text="Nombre").grid(row=0, column=1)
        Label(frame, text="Apellido").grid(row=0, column=2)
        self.dni = Entry(frame, state=DISABLED)
        self.nombre = Entry(frame)
        self.apellido = Entry(frame)
        self.dni.grid(row=1, column=0)
        self.nombre.grid(row=1, column=1)
        self.apellido.grid(row=1, column=2)
        item = self.parent.treeview.focus()
        campos = self.parent.treeview.item(item, 'values')
        self.dni.insert(0, campos[0])
        self.nombre.insert(0, campos[1])
        self.apellido.insert(0, campos[2])
        bottom = Frame(self)
        bottom.pack(pady=10)
        Button(bottom, text="Actualizar", command=self.update_client).grid(row=0, column=0)
        Button(bottom, text="Cancelar", command=self.destroy).grid(row=0, column=1)

    def update_client(self):
        dni, nombre, apellido = self.dni.get(), self.nombre.get(), self.apellido.get()
        self.parent.treeview.item(dni, values=(dni, nombre, apellido))
        Clientes.modificar(dni, nombre, apellido)
        self.destroy()
