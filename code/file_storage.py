# Almacenamiento de Archivos y Directorios

class Arbol:
    def __init__(self, nombre, padre, prop, tipo, perm):
        """
        nombre es el nombre del nodo. (Str)
        padre es el nombre del padre del nodo. (Str)
        porp es el nombre del propietario. (Str)
        tipo es el tipo del árbol. (Bool) True = Directorio, False = Archivo.
        ro, wo, xo los permisos A/D para el grupo Otros. (Int) 1 = tiene permiso, 0 = No tiene permiso
        """
        self.nombre = nombre
        self.padre = padre
        self.prop = prop
        self.tipo = tipo
        self.hijos = []
        self.permisos = perm

    def agrega(self, nuevo):
        """Esta función es para agregar un nuevo Hijo"""
        self.hijos.append(nuevo)

    def elimina(self, hijo):
        """Ya comprobados los permisos elimina al hijo pasado por parámetros"""
        bad = False
        for index,son in enumerate(self.hijos):
            if son.nombre == hijo:
                self.hijos.pop(index)
                bad = True
                break
        if bad:
            print("El Elemento ha sido Eliminado Exitosamente.")
        else:
            print("No se pudo encontrar al Elemento.")

    def cambiar(self, perm):
        """Cambia los permisos del árbol"""
        self.permisos = perm

    def comprobarHijos(self, nombre):
        """Comprueba que el elemento no esté en el Directorio"""
        for hijo in self.hijos:
            if hijo.nombre == nombre:
                return False
        return True


def dar_permisos():
    """Esta función es para que el usuario introduzca los permisos a otros"""
    print("Escriba los permisos para Otros Usuarios: 1 para dar permiso, 0 en caso contrario:")
    print("Read.")
    jrx= int(input())
    print("Write.")
    jwx= int(input())
    print("Exe.")
    jxx= int(input())
    return [jrx, jwx, jxx]

raiz = Arbol("./","", "r00t", "D", [1,1,1])

def AbrirArchivo():
    """Esta función es para cargar el archivo de los árboles"""
    print("Bienvenido! Por favor, escriba el nombre o ruta del archivo:")
    nombre_de_archivo = input()
    archivo = open(nombre_de_archivo,'r')
    bandera = True
    while True :
        nombre = archivo.readline().rstrip()
        if not nombre:
            print("Fin del Archivo")
            break
        padre = archivo.readline().rstrip()
        duenio = archivo.readline().rstrip()
        estado = bool(archivo.readline().rstrip())
        permisos = archivo.readline().rstrip()
        permisos = permisos.split(',')
        try:
            for index,dato in enumerate(permisos):
                permisos[index] = int(dato)
        except:
            print("")
        if bandera:
            Actual = Arbol(nombre, raiz, duenio, estado, permisos)
            raiz.agrega(Actual)
            Padre = raiz
            bandera = False
        else:
            if Padre.nombre == padre:#Agregar si es hermano
                print("1")
                Actual = Arbol(nombre, Padre, duenio, estado, permisos)
                Padre.agrega(Actual)
            elif Actual.nombre == padre:#Agrega si es hijo
                print("2")
                Actual_1= Arbol(nombre, Actual, duenio, estado, permisos)
                Actual.agrega(Actual_1)
                Padre = Actual
                Actual = Actual_1
                print("Padre: "+ Padre.nombre)
                print("Actual: "+ Actual.nombre)
            else:#Agregue en otra posición
                while True:
                    Actual = Actual.padre
                    Padre = Actual.padre
                    if Padre.nombre == padre:
                        Actual = Arbol(nombre, Padre, duenio, estado, permisos)
                        Padre.agrega(Actual)
                        break
    archivo.close()


def guarda(arbol, archivo):
    """Esta función es para escribir un árbol en un archivo ya abierto"""
    archivo.write(str(arbol.nombre))
    archivo.write("\n")
    archivo.write(str(arbol.padre.nombre))
    archivo.write("\n")
    archivo.write(str(arbol.prop))
    archivo.write("\n")
    archivo.write(str(arbol.tipo))
    archivo.write("\n")
    perm = str(arbol.permisos)
    perm = perm.replace('[','')
    perm = perm.replace(']','')
    perm = perm.replace(' ','')
    archivo.write(perm)
    archivo.write("\n")

def guardaProfundidad(arbol, funcion, archivo):
    """Esta función es para Guardar todos los hijos de la raíz en un archivo ya abierto"""
    for hijo in arbol.hijos:
        funcion(hijo, archivo)
        guardaProfundidad(hijo, funcion, archivo)

def usuario():
    """Esta función es para que un nuevo usuario pueda iniciar sesion"""
    print("Escriba el nombre de usuario:")
    use = input()
    return use

def printHijo(hijo):
    """Funcion usada en el recorrido para imprimir un hijo"""
    print(f"\t{hijo}",)

def verProfundidad(arbol, funcion):
    funcion(arbol.nombre)
    for hijo in arbol.hijos:
        verProfundidad(hijo, funcion)

# Inicio del Main
raiz = Arbol("./","", "r00t", "D", [1,1,1])
bandTot = True
AbrirArchivo()
while bandTot:
    Odin = raiz
    Actual = raiz
    user = usuario()
    band = True
    band2 = False
    while band:
        print(f"Directorio Actual: {Actual.nombre}")
        print("\tMENU\n1.Crear un Archivo o Directorio.\n2.Eliminar un Archivo o Directorio.\n3.Cambiar Permisos del Directorio Actual.\n4.Ver Contenido del Directorio Actual.")
        print("5.Visualizar Todo el Contenido.\n6.Acceder a un Subdirectorio.\n7.Subir de Nivel al Directorio anterior\n8.Cerrar Sesion.\n9.Salir.")
        print("Seleccione una opcion:")
        opc = int(input())
        # ----------------------------------------------------------------------------------------------------------------

        if opc == 1:    # Crear archivo o directorio
            if user == Actual.prop or Actual.permisos[1] == 1:
                print("¿Quiere Crear un Archivo o Directorio?\nEscriba: (A o a) para archivo o (D o d) para Directorio.")
                opc = input()
                if opc == "A" or opc == "a":
                    print("Escriba el nombre del Archivo:")
                    tipo_a = False 
                elif opc == "D" or opc == "d":
                    print("Escriba el nombre del Directorio:")
                    tipo_a = True
                nom = input()
                if not tipo_a:
                    nom = nom + ".a"
                if Actual.comprobarHijos(nom):
                    perm = dar_permisos()
                    Actual.agrega(Arbol(nom, Actual, user, tipo_a, perm))
                else:
                    print("El Nombre del Elemento ya se usa.")
            else:
                print("No se te permite Crear en este Directorio.")

        #----------------------------------------------------------------------------------------------------------------
        elif opc == 2:  # Eliminar archivo o directorio
            if Actual.prop == user or Actual.permisos[1] == 1:
                print("Escriba el nombre del Elemento a Eliminar:")
                nom = input()
                Actual.elimina(nom)
            else:
                print("Solo el Propietario puede Eliminar en este Directorio.")

        #----------------------------------------------------------------------------------------------------------------
        elif opc == 3:  # Cambiar el directorio actual
            if Actual.prop == user:
                print(f" Para el Directorio Actual: {Actual.nombre}")
                perm = dar_permisos()
                Actual.cambiar(perm)
            else:
                print("Solo el Propietario puede Cambiar los Permisos en este Directorio.")

        #----------------------------------------------------------------------------------------------------------------
        elif opc == 4:  # Ver contenido del directorio Actual
            print(f"Directorio Actual: {Actual.nombre}\nContenido:")
            print(f"\tNom\t\tP.P.\t\tP.O.\t\tPropietario")
            for elem in Actual.hijos:
                print(f"\t{elem.nombre}\t\t1 1 1\t\t{elem.permisos[0]} {elem.permisos[1]} {elem.permisos[2]}\t\t{elem.prop}")
        #----------------------------------------------------------------------------------------------------------------
        elif opc == 5:  # Visualizar Todo el sistema de Archivos
            verProfundidad(Odin, printHijo)
        #----------------------------------------------------------------------------------------------------------------
        elif opc == 6:  # Acceder a un directorio
            print("Escriba el nombre del Directorio:")
            nom = input()
            bad = False
            for son in Actual.hijos:
                if son.nombre == nom and son.tipo:
                    Actual = son
                    bad = True
                    break
            if bad:
                print("Se Ha cambiado de Directorio.")
            else:
                print("No se pudo encontrar el Directorio o el nombre pertenece a un Archivo.")

        #----------------------------------------------------------------------------------------------------------------
        elif opc == 7:  # Subir nivel
            if hasattr(Actual.padre,'nombre'):
                Actual = Actual.padre

        #----------------------------------------------------------------------------------------------------------------
        elif opc == 8:  # Cerrar Sesion
            band = False
            print(f"Sesion de {user} Cerrada.")

        #----------------------------------------------------------------------------------------------------------------
        elif opc == 9:  # Salir
            band = False
            bandTot = False
            archivo = open('datos.txt','w',)
            guardaProfundidad(Odin, guarda, archivo)
            archivo.close()
            # Aqui requerimos guardar todo el arbol en un archivo

#-----------------------------------------------------------------------------------------------------------------------
