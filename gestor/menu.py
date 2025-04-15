from gestor import database as db, helpers

def iniciar():
    while True:
        helpers.limpiar_pantalla()
        print("========================")
        print("  BIENVENIDO AL Manager ")
        print("========================")
        print("[1] Listar clientes     ")
        print("[2] Buscar cliente      ")
        print("[3] Añadir cliente      ")
        print("[4] Modificar cliente   ")
        print("[5] Borrar cliente      ")
        print("[6] Cerrar el Manager   ")
        print("========================")
        opcion = input("> ")
        helpers.limpiar_pantalla()

        if opcion == '1':
            for cliente in db.Clientes.lista:
                print(cliente)
        elif opcion == '2':
            dni = helpers.leer_texto(3, 3, "DNI (2 ints y 1 char)").upper()
            cliente = db.Clientes.buscar(dni)
            print(cliente if cliente else "Cliente no encontrado.")
        elif opcion == '3':
            while True:
                dni = helpers.leer_texto(3, 3, "DNI (2 ints y 1 char)").upper()
                if helpers.dni_valido(dni, db.Clientes.lista): break
            nombre = helpers.leer_texto(2, 30, "Nombre").capitalize()
            apellido = helpers.leer_texto(2, 30, "Apellido").capitalize()
            db.Clientes.crear(dni, nombre, apellido)
            print("Cliente añadido correctamente.")
        elif opcion == '4':
            dni = helpers.leer_texto(3, 3, "DNI").upper()
            cliente = db.Clientes.buscar(dni)
            if cliente:
                nombre = helpers.leer_texto(2, 30, f"Nombre [{cliente.nombre}]").capitalize()
                apellido = helpers.leer_texto(2, 30, f"Apellido [{cliente.apellido}]").capitalize()
                db.Clientes.modificar(dni, nombre, apellido)
                print("Cliente modificado correctamente.")
            else:
                print("Cliente no encontrado.")
        elif opcion == '5':
            dni = helpers.leer_texto(3, 3, "DNI").upper()
            print("Cliente borrado correctamente." if db.Clientes.borrar(dni) else "Cliente no encontrado.")
        elif opcion == '6':
            print("Saliendo...")
            break
        input("\nPresiona ENTER para continuar...")
