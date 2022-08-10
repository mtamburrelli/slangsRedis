import redis

redis_host = 'localhost'
redis_port = 6379
db = "Diccionario de Slangs"
r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)


# Funciones

def addSlang(slang, significado):
    r.hset(db, slang, significado)


def editSlang(slang, new_def):
    r.hset(db, slang, new_def)


def delSlang(slang):
    r.hdel(db, slang)


def getSlangs():
    return r.hgetall(db)


def defSlang(slang):
    return r.hget(db, slang)


# Menú

while True:
    menu = """
    1) Agregar nuevo slang
    2) Editar slang
    3) Eliminar slang existente
    4) Ver diccionario
    5) Buscar definición
    6) Salir
    \nSelecciona una opción: """
    opt = input(menu)
    if opt == "1":  # Buscar si existe el slang ingresado y agregarlo si no
        input_slang = input("\nIngrese un slang: ")
        input_slang = input_slang.capitalize()
        verificado = r.hexists(db, input_slang)
        if verificado:
            print(f"El slang '{input_slang}' ya existe")
        else:
            significado = input("Ingrese el significado: ")
            significado = significado.capitalize()
            addSlang(input_slang, significado)
            print("¡Slang agregado con éxito!")
    if opt == "2":  # Buscar el slang que se quiere editar y cambiar su significado, si no existe, te da la opción de agregarlo
        input_slang = input("\n¿Qué slang desea editar?: ")
        input_slang = input_slang.capitalize()
        verificado = r.hexists(db, input_slang)
        if verificado:
            new_def = input("Ingrese el nuevo significado: ")
            editSlang(input_slang, new_def)
            print("¡Slang actualizado exitosamente!")
        else:
            yn = input(f"El slang '{input_slang}' no existe. ¿Deseas agregarlo? Y/N: ")
            if yn == 'Y' or yn == 'y':
                significado = input("Ingrese el significado: ")
                addSlang(input_slang, significado)
                print("¡Slang agregado con éxito!")
            else:
                continue
    if opt == "3":  # Eliminar un slang
        input_slang = input("\n¿Qué slang desea eliminar?: ")
        input_slang = input_slang.capitalize()
        delSlang(input_slang)
        if not r.hexists(db, input_slang):
            print(f"El slang '{input_slang}' no existe")
    if opt == "4":  # Mostrar todos los slangs y sus definiciones usando un ciclo for
        print("\n--------Diccionario de Slangs--------\n")
        slangs = getSlangs()
        i = 0
        for slang in slangs:
            i += 1
            print(str(i) + '.' + slang + ": " + defSlang(slang))
    if opt == "5":  # Mostrar el significado del slang escogido, si no existe, te da la opción de agregarlo
        input_slang = input("\n¿Qué significado deseas saber?: ")
        input_slang = input_slang.capitalize()
        significado = defSlang(input_slang)
        verificado = r.hexists(db, input_slang)
        if verificado:
            print(f"El significado de '{input_slang}' es:\n{significado}")
        else:
            yn = input(f"El slang '{input_slang}' no existe. ¿Deseas agregarlo? Y/N: ")
            if yn == 'Y' or yn == 'y':
                significado = input("Ingrese el significado: ")
                significado = significado.capitalize()
                addSlang(input_slang, significado)
                print("¡Slang agregado con éxito!")
            else:
                continue
    if opt == "6":
        print("¡Hasta luego!")
        exit()
