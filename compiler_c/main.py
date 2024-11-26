from compiler import compile
from os import system, name

# define our clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def printmenu(flag):
    print("Bienvenido")
    print("Que operacion desea ejecutar? (Ingrese el numero correspondiente)")
    print("\t1. Compilar un codigo en base a nuestro subset de C")
    print("\t2. Cambiar el nombre del archivo a compilar")
    if(flag):
        print("\t3. Evitar que el programa genere un arbol sintactico")
    else:
        print("\t3. Hacer que el programa genere un arbol sintactico")
    print("\t4. Salir del programa")

try:
    filename = "source_code.c"
    flag = True
    treeflag = True
    while(flag):
        clear()
        printmenu(treeflag)
        option = int(input("Su eleccion: "))
        
        match(option):
            case 1:
                compile(filename, treeflag)
                option = input("Oprima enter para continuar...\n")
            case 2:
                filename = input("Por favor ingrese el nombre del archivo: ")
                option = input("Oprima enter para continuar...\n")
            case 3:
                treeflag = not treeflag
                option = input("Oprima enter para continuar...\n")
            case 4:
                flag = False
            case _:
                option = input("Por favor ingrese una opcion valida\nOprima enter para continuar...\n")
except Exception as e:
    print(e)