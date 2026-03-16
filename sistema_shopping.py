import os
import pickle
from datetime import datetime, date
import getpass


# ─────────────────────────────────────────────
#  CLASES
# ─────────────────────────────────────────────

class Usuarios:
    def __init__(self):
        self.codUsuario = 0
        self.nombreUsuario = ""
        self.claveusuario = ""
        self.tipoUsuario = ""
        self.categCliente = ""


class Novedades:
    def __init__(self):
        self.codNovedad = 0
        self.textoNovedad = "".ljust(200, " ")
        self.fechaDesdeNovedad = date
        self.fechaHastaNovedad = date
        self.tipoUsuario = "".ljust(20, " ")
        self.estado = ""


class Locales:
    def __init__(self):
        self.codLocal = 0
        self.nombreLocal = "".ljust(50, " ")
        self.ubicacionLocal = "".ljust(50, " ")
        self.rubroLocal = "".ljust(50, " ")
        self.codUsuario = 0
        self.estado = ""


class Promociones:
    def __init__(self):
        self.codPromo = 0
        self.textoPromo = "".ljust(200, " ")
        self.fechaDesdePromo = date
        self.fechaHastaPromo = date
        self.categCliente = "".ljust(10, " ")
        self.diasSemana = [[0] * 3 for _ in range(3)]
        self.estadoPromo = "Pendiente".ljust(10, " ")
        self.codLocal = 0


class Uso_Promos:
    def __init__(self):
        self.codCliente = 0
        self.codPromo = 0
        self.fechaUsoPromo = date
        self.estado = "Pendiente".ljust(10, " ")


# ─────────────────────────────────────────────
#  RUTAS DE ARCHIVOS (relativas al script)
# ─────────────────────────────────────────────

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos_shopping")

afu  = os.path.join(BASE_DIR, "usuarios.dat")
afn  = os.path.join(BASE_DIR, "novedades.dat")
afl  = os.path.join(BASE_DIR, "locales.dat")
afp  = os.path.join(BASE_DIR, "promociones.dat")
afup = os.path.join(BASE_DIR, "uso_promociones.dat")

RU  = Usuarios()
RN  = Novedades()
RL  = Locales()
RP  = Promociones()
RUP = Uso_Promos()

sesion    = False
opc       = -1
opcDueno  = 0
opcAdmin  = 0
opcCliente = 0


# ─────────────────────────────────────────────
#  APERTURA DE ARCHIVOS
# ─────────────────────────────────────────────

def apertura():
    global alu, aln, all_, alp, alup
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    modo_u  = "w+b" if not os.path.exists(afu)  else "r+b"
    modo_n  = "w+b" if not os.path.exists(afn)  else "r+b"
    modo_l  = "w+b" if not os.path.exists(afl)  else "r+b"
    modo_p  = "w+b" if not os.path.exists(afp)  else "r+b"
    modo_up = "w+b" if not os.path.exists(afup) else "r+b"

    alu  = open(afu,  modo_u)
    aln  = open(afn,  modo_n)
    all_ = open(afl,  modo_l)
    alp  = open(afp,  modo_p)
    alup = open(afup, modo_up)


def cierre():
    alp.close()
    all_.close()
    alup.close()
    alu.close()
    aln.close()


# ─────────────────────────────────────────────
#  VALIDACIONES
# ─────────────────────────────────────────────

def val_rango_entero(nro, desde, hasta):
    try:
        return not (desde <= int(nro) <= hasta)
    except (ValueError, TypeError):
        return True


def val_rango(ltra, desde, hasta):
    try:
        return not (desde <= str(ltra) <= hasta)
    except Exception:
        return True


def val_longitud(texto, max_len=100):
    return len(texto) <= max_len


def val_contra(clave):
    return len(clave) != 8


def val_rubro(rubro):
    return rubro in ("indumentaria", "comida", "perfumeria")


def validar_fecha():
    while True:
        try:
            texto = input("Ingrese la fecha (DD/MM/AAAA): ")
            fecha = datetime.strptime(texto, "%d/%m/%Y")
            if fecha >= datetime.now():
                return fecha
            print("La fecha debe ser futura.")
        except ValueError:
            print("Formato invalido. Use DD/MM/AAAA.")


def validar_fecha_desde():
    print("Fecha inicial:")
    while True:
        try:
            texto = input("Ingrese la fecha (DD/MM/AAAA): ")
            datetime.strptime(texto, "%d/%m/%Y")
            return texto
        except ValueError:
            print("Formato invalido. Use DD/MM/AAAA.")


def validar_fecha_hasta():
    print("Fecha final:")
    while True:
        try:
            texto = input("Ingrese la fecha (DD/MM/AAAA): ")
            datetime.strptime(texto, "%d/%m/%Y")
            return texto
        except ValueError:
            print("Formato invalido. Use DD/MM/AAAA.")


# ─────────────────────────────────────────────
#  BÚSQUEDAS
# ─────────────────────────────────────────────

def buscar_correo(correo):
    t = os.path.getsize(afu)
    alu.seek(0)
    while alu.tell() < t:
        pos = alu.tell()
        var_temp = pickle.load(alu)
        if var_temp.nombreUsuario == correo:
            return pos
    return -1


def buscar_codigo_local(cod):
    t = os.path.getsize(afl)
    all_.seek(0)
    while all_.tell() < t:
        pos = all_.tell()
        var_temp = pickle.load(all_)
        if var_temp.codLocal == cod:
            return pos
    return -1


def buscar_nombre_local(nombre):
    t = os.path.getsize(afl)
    all_.seek(0)
    while all_.tell() < t:
        pos = all_.tell()
        var_temp = pickle.load(all_)
        if var_temp.nombreLocal == nombre:
            return pos
    return -1


def buscar_promocion(cod_loc):
    t = os.path.getsize(afp)
    alp.seek(0)
    while alp.tell() < t:
        pos = alp.tell()
        var_temp = pickle.load(alp)
        if var_temp.codLocal == cod_loc:
            return pos
    return -1


def buscar_correo_dueno(correo):
    t = os.path.getsize(afu)
    alu.seek(0)
    while alu.tell() < t:
        pos = alu.tell()
        var_temp = pickle.load(alu)
        if var_temp.nombreUsuario == correo and var_temp.tipoUsuario == "dueno":
            return pos
    return -1


def busqueda_dicotomica_promo(buscado):
    """Busqueda dicotomica en archivo de promociones ordenado por codPromo."""
    t = os.path.getsize(afp)
    if t == 0:
        return -1
    alp.seek(0)
    pickle.load(alp)
    tam_reg = alp.tell()
    cant_reg = t // tam_reg

    ini = 0
    fin = cant_reg - 1
    while ini <= fin:
        med = (ini + fin) // 2
        alp.seek(med * tam_reg)
        reg = pickle.load(alp)
        if reg.codPromo == buscado:
            return med * tam_reg
        elif reg.codPromo < buscado:
            ini = med + 1
        else:
            fin = med - 1
    return -1


def verificar_aprobacion(cod):
    hoy = datetime.now()
    t = os.path.getsize(afp)
    alp.seek(0)
    while alp.tell() < t:
        pos = alp.tell()
        var_temp = pickle.load(alp)
        if var_temp.codPromo == cod:
            if var_temp.estadoPromo.strip() == "aprobado" and var_temp.fechaDesdePromo <= hoy and var_temp.fechaHastaPromo >= hoy:
                return pos
            print("Promocion rechazada o pendiente de aprobacion.")
            return -1
    print("Promocion no registrada.")
    return -1


def alta_o_baja(cod):
    t = os.path.getsize(afl)
    all_.seek(0)
    while all_.tell() < t:
        var_temp = pickle.load(all_)
        if var_temp.codLocal == cod and var_temp.estado == "B":
            return "B"
    return "A"


def obtener_codigo(tipo_busq):
    """Devuelve el proximo codigo disponible. tipo_busq: 1=usuarios, 2=promociones."""
    if tipo_busq == 1:
        archivo = afu
        al = alu
    else:
        archivo = afp
        al = alp

    tamano = os.path.getsize(archivo)
    if tamano == 0:
        return 1

    al.seek(0)
    pickle.load(al)
    tam_reg = al.tell()
    al.seek(tamano - tam_reg)
    reg = pickle.load(al)
    return (reg.codUsuario if tipo_busq == 1 else reg.codPromo) + 1


def cant_reg():
    t = os.path.getsize(afup)
    t2 = os.path.getsize(afp)
    if t == 0 or t2 == 0:
        return 0

    alup.seek(0)
    alp.seek(0)
    pickle.load(alup)
    pickle.load(alp)
    tam_up = alup.tell()
    tam_p = alp.tell()

    alup.seek(0)
    alp.seek(0)
    cont = 0
    while alup.tell() < t and alp.tell() < t2:
        d = pickle.load(alup)
        e = pickle.load(alp)
        if d.codPromo == e.codPromo:
            cont += 1
    return cont


# ─────────────────────────────────────────────
#  ORDENAMIENTO (burbuja sobre archivos)
# ─────────────────────────────────────────────

def ordenar_usuarios():
    """Ordena el archivo de usuarios por nombreUsuario (burbuja)."""
    tamano = os.path.getsize(afu)
    if tamano == 0:
        return
    alu.seek(0)
    pickle.load(alu)
    tam_reg = alu.tell()
    cant = tamano // tam_reg

    for i in range(cant - 1):
        for j in range(i + 1, cant):
            alu.seek(i * tam_reg)
            reg_i = pickle.load(alu)
            alu.seek(j * tam_reg)
            reg_j = pickle.load(alu)
            if reg_i.nombreUsuario > reg_j.nombreUsuario:
                alu.seek(i * tam_reg)
                pickle.dump(reg_j, alu)
                alu.seek(j * tam_reg)
                pickle.dump(reg_i, alu)
                alu.flush()


# ─────────────────────────────────────────────
#  MENÚS / PANTALLAS
# ─────────────────────────────────────────────

def mostrar_menu():
    os.system("cls" if os.name == "nt" else "clear")
    print("Sistema de Shopping")
    print("-------------------")
    print("1 - Iniciar sesion")
    print("2 - Registrarse como cliente")
    print("3 - Ver locales")
    print("0 - Salir")


def pantalla_admin():
    os.system("cls" if os.name == "nt" else "clear")
    print("Bienvenido, Administrador")
    print("─" * 50)
    print("1. Gestion de locales")
    print("2. Crear cuenta de dueno de local")
    print("3. Aprobar/denegar solicitud de descuento")
    print("4. Gestion de novedades")
    print("5. Reporte de utilizacion de descuentos")
    print("0. Salir")


def pantalla_dueno():
    os.system("cls" if os.name == "nt" else "clear")
    print("Bienvenido, dueno de local")
    print("─" * 50)
    print("1. Crear descuento")
    print("2. Reporte de uso de descuentos")
    print("3. Ver novedades")
    print("0. Salir")


def pantalla_cliente():
    os.system("cls" if os.name == "nt" else "clear")
    print("Bienvenido, Cliente")
    print("─" * 50)
    print("1. Buscar descuentos en locales")
    print("2. Solicitar descuento")
    print("3. Ver novedades")
    print("0. Salir")


def pantalla_novedades():
    os.system("cls" if os.name == "nt" else "clear")
    print("a) Crear novedad")
    print("b) Modificar novedad")
    print("c) Eliminar novedad")
    print("d) Volver")


def pantalla_gestion_locales():
    os.system("cls" if os.name == "nt" else "clear")
    print("a) Crear local")
    print("b) Modificar local")
    print("c) Eliminar local")
    print("d) Mapa de locales")
    print("e) Volver")


def confirmar():
    global opc
    rpta = input("Confirma la salida? (si/no): ")
    while rpta.lower() not in ("si", "no"):
        rpta = input("Opcion invalida. Confirma la salida? (si/no): ")
    if rpta.lower() == "si":
        print("Hasta luego!")
        cierre()
        opc = 0


# ─────────────────────────────────────────────
#  INICIO DE SESION Y REGISTRO
# ─────────────────────────────────────────────

def inicio():
    """Crea el usuario admin por defecto si el archivo esta vacio."""
    if os.path.getsize(afu) == 0:
        admin = Usuarios()
        admin.codUsuario = 1
        admin.nombreUsuario = "admin@shopping.com"
        admin.claveusuario = "12345678"
        admin.tipoUsuario = "admin"
        alu.seek(0)
        pickle.dump(admin, alu)
        alu.flush()


def iniciar_sesion():
    global opc, opcCliente, opcAdmin, opcDueno
    os.system("cls" if os.name == "nt" else "clear")

    correo = input("Correo: ")
    pos = buscar_correo(correo)
    while pos == -1:
        correo = input("Correo no encontrado. Intente de nuevo: ")
        pos = buscar_correo(correo)

    alu.seek(pos)
    usuario = pickle.load(alu)

    intentos = 0
    contrasena = getpass.getpass("Contrasena: ")
    while contrasena != usuario.claveusuario and intentos < 3:
        intentos += 1
        if intentos < 3:
            contrasena = getpass.getpass("Contrasena incorrecta. Intente de nuevo: ")

    if intentos == 3:
        print("Demasiados intentos fallidos. Intente mas tarde.")
        input("Presione Enter para continuar...")
        return

    opc = 0
    if usuario.tipoUsuario == "cliente":
        opcCliente = 1
    elif usuario.tipoUsuario == "admin":
        opcAdmin = 1
    elif usuario.tipoUsuario == "dueno":
        opcDueno = 1


def registrar_cliente():
    os.system("cls" if os.name == "nt" else "clear")
    print("Registrar nuevo cliente")
    print("─" * 40)

    correo = input("Correo (max 100 caracteres) [* para salir]: ")
    while not val_longitud(correo) and correo != "*":
        correo = input("Correo demasiado largo. Intente de nuevo: ")

    while correo != "*":
        if buscar_correo(correo) == -1:
            RU.nombreUsuario = correo
            RU.tipoUsuario = "cliente"

            clave = input("Contrasena (exactamente 8 caracteres): ")
            while val_contra(clave):
                clave = input("Debe tener exactamente 8 caracteres: ")
            RU.claveusuario = clave

            pickle.dump(RU, alu)
            alu.flush()
            print("Cliente registrado exitosamente.")
        else:
            print(f"Ya existe un cliente con el correo {correo}.")

        input("Presione Enter para continuar...")
        correo = input("Correo (max 100 caracteres) [* para salir]: ")
        while not val_longitud(correo) and correo != "*":
            correo = input("Correo demasiado largo. Intente de nuevo: ")


# ─────────────────────────────────────────────
#  LOCALES
# ─────────────────────────────────────────────

def mostrar_locales():
    t = os.path.getsize(afl)
    all_.seek(0)
    print(f"\n{'Cod':<6} {'Nombre':<30} {'Ubicacion':<30} {'Rubro':<20} {'Estado'}")
    print("─" * 95)
    while all_.tell() < t:
        loc = pickle.load(all_)
        print(f"{str(loc.codLocal):<6} {loc.nombreLocal.strip():<30} {loc.ubicacionLocal.strip():<30} {loc.rubroLocal.strip():<20} {loc.estado}")
    calcular_rubro()
    input("\nPresione Enter para continuar...")


def calcular_rubro():
    t = os.path.getsize(afl)
    all_.seek(0)
    indu = com = perfu = 0
    while all_.tell() < t:
        loc = pickle.load(all_)
        rubro = loc.rubroLocal.strip()
        if rubro == "indumentaria":
            indu += 1
        elif rubro == "comida":
            com += 1
        elif rubro == "perfumeria":
            perfu += 1
    print(f"\nResumen por rubro — Indumentaria: {indu} | Comida: {com} | Perfumeria: {perfu}")


def crear_locales():
    os.system("cls" if os.name == "nt" else "clear")
    print("Crear local")
    print("─" * 40)

    nombre = input("Nombre del local [* para salir]: ")
    while not val_longitud(nombre, 50) and nombre != "*":
        nombre = input("Nombre demasiado largo (max 50 caracteres): ")

    while nombre != "*":
        if buscar_nombre_local(nombre) == -1:
            RL.nombreLocal = nombre
            RL.ubicacionLocal = input("Ubicacion del local: ")
            rubro = input("Rubro (indumentaria / comida / perfumeria): ")
            while not val_rubro(rubro):
                rubro = input("Rubro invalido. Ingrese indumentaria, comida o perfumeria: ")
            RL.rubroLocal = rubro

            correo_dueno = input("Correo del dueno: ")
            while buscar_correo_dueno(correo_dueno) == -1:
                correo_dueno = input("Correo no existe o no es dueno. Intente de nuevo: ")
            RL.codUsuario = correo_dueno

            cod_local = input("Codigo del local: ")
            while buscar_codigo_local(cod_local) != -1:
                cod_local = input("Ese codigo ya existe. Ingrese otro: ")
            RL.codLocal = cod_local
            RL.estado = "A"

            pickle.dump(RL, all_)
            all_.flush()
            print("Local creado exitosamente.")
        else:
            print(f"Ya existe un local con el nombre '{nombre}'.")

        input("Presione Enter para continuar...")
        nombre = input("Nombre del local [* para salir]: ")


def modificar_local():
    os.system("cls" if os.name == "nt" else "clear")
    print("Modificar local")
    print("─" * 40)

    cod = input("Codigo del local a modificar: ")
    pos = buscar_codigo_local(cod)
    while pos == -1:
        cod = input("Local no encontrado. Intente de nuevo: ")
        pos = buscar_codigo_local(cod)

    if alta_o_baja(cod) == "B":
        rpta = input("El local esta dado de baja. Desea reactivarlo? (si/no): ")
        while rpta.lower() not in ("si", "no"):
            rpta = input("Opcion invalida (si/no): ")
        if rpta.lower() == "si":
            all_.seek(pos)
            loc = pickle.load(all_)
            loc.estado = "A"
            all_.seek(pos)
            pickle.dump(loc, all_)
            all_.flush()
    else:
        all_.seek(pos)
        loc = pickle.load(all_)

        if input("Modificar nombre? (si/no): ").lower() == "si":
            nombre = input("Nuevo nombre: ")
            while not val_longitud(nombre, 50):
                nombre = input("Demasiado largo (max 50): ")
            loc.nombreLocal = nombre

        if input("Modificar rubro? (si/no): ").lower() == "si":
            rubro = input("Nuevo rubro (indumentaria / comida / perfumeria): ")
            while not val_rubro(rubro):
                rubro = input("Rubro invalido: ")
            loc.rubroLocal = rubro

        if input("Modificar correo del dueno? (si/no): ").lower() == "si":
            correo = input("Nuevo correo del dueno: ")
            while buscar_correo_dueno(correo) == -1:
                correo = input("Correo no existe o no es dueno: ")
            loc.codUsuario = correo

        all_.seek(pos)
        pickle.dump(loc, all_)
        all_.flush()
        print("Local modificado exitosamente.")

    input("Presione Enter para continuar...")


def eliminar_local():
    os.system("cls" if os.name == "nt" else "clear")
    print("Eliminar local (baja logica)")
    print("─" * 40)

    cod = input("Codigo del local a eliminar: ")
    pos = buscar_codigo_local(cod)
    while pos == -1:
        cod = input("Local no encontrado. Intente de nuevo: ")
        pos = buscar_codigo_local(cod)

    if alta_o_baja(cod) == "B":
        print("El local ya estaba dado de baja.")
    else:
        rpta = input("Confirma la baja? (si/no): ")
        while rpta.lower() not in ("si", "no"):
            rpta = input("Opcion invalida (si/no): ")
        if rpta.lower() == "si":
            all_.seek(pos)
            loc = pickle.load(all_)
            loc.estado = "B"
            all_.seek(pos)
            pickle.dump(loc, all_)
            all_.flush()
            print("Local dado de baja exitosamente.")

    input("Presione Enter para continuar...")


def mapa_locales():
    os.system("cls" if os.name == "nt" else "clear")
    all_.seek(0)
    numero = 0
    for _ in range(10):
        print("+--" * 5 + "+")
        for _ in range(5):
            cod, estado = _leer_local_mapa()
            if estado != 0:
                etiqueta = str(cod).zfill(2)
                marca = "A" if estado == "A" else " "
                print(f"|{marca}{etiqueta}", end="")
            else:
                print("|  ", end="")
            numero += 1
        print("|")
    print("+--" * 5 + "+")

    t = os.path.getsize(afl)
    if t != 0:
        all_.seek(0)
        pickle.load(all_)
        tam_reg = all_.tell()
        cant_reg_locales = t // tam_reg
        if cant_reg_locales > 50:
            print("Proximamente se habilitara un mapa con los demas locales.")

    input("Presione Enter para continuar...")


def _leer_local_mapa():
    if all_.tell() < os.path.getsize(afl):
        loc = pickle.load(all_)
        return loc.codLocal, loc.estado
    return 0, 0


# ─────────────────────────────────────────────
#  CUENTAS DE DUENOS
# ─────────────────────────────────────────────

def crear_cuenta_dueno():
    correo = input("Correo del dueno (max 100 caracteres): ")
    while not val_longitud(correo):
        correo = input("Demasiado largo. Intente de nuevo: ")
    while buscar_correo(correo) != -1:
        correo = input("Ese correo ya existe. Ingrese otro: ")

    clave = input("Contrasena (exactamente 8 caracteres): ")
    while val_contra(clave):
        clave = input("Debe tener exactamente 8 caracteres: ")

    nuevo = Usuarios()
    nuevo.nombreUsuario = correo
    nuevo.claveusuario = clave
    nuevo.tipoUsuario = "dueno"
    pickle.dump(nuevo, alu)
    alu.flush()
    print("Cuenta de dueno creada exitosamente.")
    input("Presione Enter para continuar...")


# ─────────────────────────────────────────────
#  PROMOCIONES
# ─────────────────────────────────────────────

def crear_descuento():
    os.system("cls" if os.name == "nt" else "clear")
    print("Crear descuento")
    print("─" * 40)

    cod_loc = input("Codigo del local (1 a 9999999): ")
    while val_rango_entero(cod_loc, 1, 9999999):
        cod_loc = input("Codigo invalido. Ingrese entre 1 y 9999999: ")
    cod_loc = int(cod_loc)

    if buscar_promocion(cod_loc) != -1:
        print(f"Ya existe una promocion para el local {cod_loc}.")
        input("Presione Enter para continuar...")
        return

    prom = Promociones()
    prom.textoPromo = input("Texto de la promocion: ")
    prom.codPromo = cod_loc
    prom.fechaDesdePromo = validar_fecha_desde()
    prom.fechaHastaPromo = validar_fecha_hasta()
    prom.diasSemana = input("Dias disponibles (ej: lunes, miercoles): ")
    prom.codLocal = cod_loc
    prom.estadoPromo = "Pendiente"

    pickle.dump(prom, alp)
    alp.flush()
    print("Promocion creada exitosamente.")
    input("Presione Enter para continuar...")


def aprobar_denegar_promo():
    t = os.path.getsize(afp)
    if t == 0:
        print("No hay promociones registradas.")
        input("Presione Enter para continuar...")
        return

    alp.seek(0)
    print(f"\n{'Cod':<8} {'Desde':<14} {'Hasta':<14} {'Estado':<12} {'Local'}")
    print("─" * 60)
    while alp.tell() < t:
        prom = pickle.load(alp)
        if prom.estadoPromo.strip() == "Pendiente":
            print(f"{prom.codPromo:<8} {str(prom.fechaDesdePromo):<14} {str(prom.fechaHastaPromo):<14} {prom.estadoPromo.strip():<12} {prom.codLocal}")

    cod = int(input("\nIngrese el codigo de la promocion: "))
    pos = verificar_aprobacion(cod) if False else _buscar_promo_por_cod(cod)
    if pos == -1:
        print("Codigo no encontrado.")
        input("Presione Enter para continuar...")
        return

    alp.seek(pos)
    prom = pickle.load(alp)
    if prom.estadoPromo.strip() == "Rechazado":
        print("La promocion ya fue rechazada.")
    else:
        nuevo_estado = input("Nuevo estado ('Aceptado' o 'Rechazado'): ")
        while nuevo_estado.lower() not in ("aceptado", "rechazado"):
            nuevo_estado = input("Estado invalido. Ingrese 'Aceptado' o 'Rechazado': ")
        prom.estadoPromo = nuevo_estado.capitalize().ljust(10)
        alp.seek(pos)
        pickle.dump(prom, alp)
        alp.flush()
        print("Estado actualizado.")

    input("Presione Enter para continuar...")


def _buscar_promo_por_cod(cod):
    t = os.path.getsize(afp)
    alp.seek(0)
    while alp.tell() < t:
        pos = alp.tell()
        prom = pickle.load(alp)
        if prom.codPromo == cod:
            return pos
    return -1


def buscar_descuentos_cliente():
    cod_loc = input("Ingrese el codigo del local (1 a 9999999): ")
    while val_rango_entero(cod_loc, 1, 9999999):
        cod_loc = input("Codigo invalido: ")
    fecha = validar_fecha()

    t = os.path.getsize(afp)
    alp.seek(0)
    encontrado = False
    while alp.tell() < t:
        prom = pickle.load(alp)
        if (prom.estadoPromo.strip().lower() == "aceptado"
                and prom.fechaDesdePromo <= fecha
                and prom.fechaHastaPromo >= fecha):
            print(f"Cod: {prom.codPromo} | {prom.textoPromo.strip()} | {prom.fechaDesdePromo} - {prom.fechaHastaPromo}")
            encontrado = True
    if not encontrado:
        print("No hay promociones disponibles para ese local y fecha.")
    input("Presione Enter para continuar...")


def solicitar_descuento():
    cod_promo = input("Codigo de la promocion: ")
    while val_rango_entero(cod_promo, 1, 9999999):
        cod_promo = input("Codigo invalido: ")
    cod_promo = int(cod_promo)

    pos = verificar_aprobacion(cod_promo)
    if pos != -1:
        up = Uso_Promos()
        up.codCliente = RU.codUsuario
        up.codPromo = cod_promo
        up.fechaUsoPromo = datetime.now()
        pickle.dump(up, alup)
        alup.flush()
        print("Descuento solicitado exitosamente.")
    input("Presione Enter para continuar...")


def reporte_descuentos():
    seguir = input("Generar reporte de utilizacion de descuentos? (S/N): ").upper()
    while seguir not in ("S", "N"):
        seguir = input("Ingrese S o N: ").upper()

    while seguir == "S":
        fecha_desde = validar_fecha_desde()
        fecha_hasta = validar_fecha_hasta()
        cant_usos = cant_reg()
        t = os.path.getsize(afp)
        alp.seek(0)
        if t != 0:
            while alp.tell() < t:
                prom = pickle.load(alp)
                if (prom.estadoPromo.strip().lower() == "aprobado"
                        and prom.fechaDesdePromo >= fecha_desde
                        and prom.fechaHastaPromo <= fecha_hasta):
                    print(f"Cod: {prom.codPromo} | {prom.fechaDesdePromo} - {prom.fechaHastaPromo} | Local: {prom.codLocal} | Usos: {cant_usos}")
        else:
            print("No hay promociones disponibles.")
        seguir = input("Generar otro reporte? (S/N): ").upper()

    print("Volviendo...")
    input("Presione Enter para continuar...")


# ─────────────────────────────────────────────
#  PROGRAMA PRINCIPAL
# ─────────────────────────────────────────────

apertura()
inicio()

while opc != 0:
    mostrar_menu()
    opc = input("Seleccione una opcion [0-3]: ")
    while val_rango_entero(opc, 0, 3):
        opc = input("Opcion invalida. Ingrese entre 0 y 3: ")
    opc = int(opc)

    if opc == 1:
        iniciar_sesion()
    elif opc == 2:
        registrar_cliente()
    elif opc == 3:
        mostrar_locales()
    elif opc == 0:
        confirmar()


while opcCliente != 0:
    pantalla_cliente()
    opcCliente = input("Seleccione una opcion [0-3]: ")
    while val_rango_entero(opcCliente, 0, 3):
        opcCliente = input("Opcion invalida: ")
    opcCliente = int(opcCliente)

    if opcCliente == 1:
        buscar_descuentos_cliente()
    elif opcCliente == 2:
        solicitar_descuento()
    elif opcCliente == 3:
        print("Novedades: diagramado en Chapin.")
        input("Presione Enter para continuar...")
    elif opcCliente == 0:
        confirmar()


while opcAdmin != 0:
    pantalla_admin()
    opcAdmin = input("Seleccione una opcion [0-5]: ")
    while val_rango_entero(opcAdmin, 0, 5):
        opcAdmin = input("Opcion invalida: ")
    opcAdmin = int(opcAdmin)

    if opcAdmin == 1:
        sub = ""
        while sub != "e":
            pantalla_gestion_locales()
            sub = input("Seleccione [a-e]: ").lower()
            while val_rango(sub, "a", "e"):
                sub = input("Opcion invalida [a-e]: ").lower()
            if sub == "a":
                crear_locales()
            elif sub == "b":
                modificar_local()
            elif sub == "c":
                eliminar_local()
            elif sub == "d":
                mapa_locales()

    elif opcAdmin == 2:
        crear_cuenta_dueno()
    elif opcAdmin == 3:
        aprobar_denegar_promo()
    elif opcAdmin == 4:
        print("Gestion de novedades: pendiente de implementacion.")
        input("Presione Enter para continuar...")
    elif opcAdmin == 5:
        reporte_descuentos()
    elif opcAdmin == 0:
        confirmar()


while opcDueno != 0:
    pantalla_dueno()
    opcDueno = input("Seleccione una opcion [0-3]: ")
    while val_rango_entero(opcDueno, 0, 3):
        opcDueno = input("Opcion invalida: ")
    opcDueno = int(opcDueno)

    if opcDueno == 1:
        crear_descuento()
    elif opcDueno == 2:
        reporte_descuentos()
    elif opcDueno == 3:
        print("Novedades: diagramado en Chapin.")
        input("Presione Enter para continuar...")
    elif opcDueno == 0:
        confirmar()
