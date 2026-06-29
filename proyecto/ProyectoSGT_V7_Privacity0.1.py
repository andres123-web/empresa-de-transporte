import uuid
import numpy as np
from datetime import datetime, timedelta, time


# CATEGORÍAS Y VELOCIDADES
VELOCIDADES_CATEGORIA = {
    "Bus": 60.0,
    "Van": 80.0,
    "Taxi": 50.0
}

DIAS_NOMBRE = {
    "LUN": 0, "MAR": 1, "MIE": 2, "JUE": 3, "VIE": 4, "SAB": 5, "DOM": 6
}
NOMBRE_DIA = ["LUN", "MAR", "MIE", "JUE", "VIE", "SAB", "DOM"]

# MODELOS
class Vehiculo:
    def __init__(self, placa, modelo, categoria, capacidad, consumo_combustible, costo_man_km):
        if capacidad <= 0:
            raise ValueError("Capacidad positiva")
        if consumo_combustible <= 0:
            raise ValueError("Consumo positivo")
        if costo_man_km < 0:
            raise ValueError("Costo mantenimiento no negativo")
        if categoria not in VELOCIDADES_CATEGORIA:
            raise ValueError("Categoría inválida: " + categoria)
        if not placa or not modelo:
            raise ValueError("Placa y modelo requeridos")
        self._placa = placa
        self._modelo = modelo
        self._categoria = categoria
        self._capacidad = capacidad
        self._consumo_combustible = consumo_combustible
        self._costo_man_km = costo_man_km

    @property
    def placa(self):
        return self._placa
    @placa.setter
    def placa(self, value):
        if value:
            self._placa = value

    @property
    def modelo(self):
        return self._modelo
    @modelo.setter
    def modelo(self, value):
        if value:
            self._modelo = value

    @property
    def categoria(self):
        return self._categoria
    @categoria.setter
    def categoria(self, value):
        if value in VELOCIDADES_CATEGORIA:
            self._categoria = value

    @property
    def capacidad(self):
        return self._capacidad
    @capacidad.setter
    def capacidad(self, value):
        if value > 0:
            self._capacidad = value

    @property
    def consumo_combustible(self):
        return self._consumo_combustible
    @consumo_combustible.setter
    def consumo_combustible(self, value):
        if value > 0:
            self._consumo_combustible = value

    @property
    def costo_man_km(self):
        return self._costo_man_km
    @costo_man_km.setter
    def costo_man_km(self, value):
        if value >= 0:
            self._costo_man_km = value

    @property
    def velocidad(self):
        return VELOCIDADES_CATEGORIA[self._categoria]

    def costo_combustible(self, distancia, precio):
        return distancia * self._consumo_combustible * precio

    def costo_mantenimiento(self, distancia):
        return distancia * self._costo_man_km

    def tiempo_viaje(self, distancia):
        return distancia / self.velocidad

    def __str__(self):
        return f"{self._placa} - {self._modelo} ({self._categoria}, cap:{self._capacidad})"


class Conductor:
    def __init__(self, nombre, nro_licencia, telefono):
        if not nombre or not nro_licencia:
            raise ValueError("Nombre y licencia obligatorios")
        self._id = str(uuid.uuid4())
        self._nombre = nombre
        self._nro_licencia = nro_licencia
        self._telefono = telefono

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre
    @nombre.setter
    def nombre(self, value):
        if value:
            self._nombre = value

    @property
    def nro_licencia(self):
        return self._nro_licencia
    @nro_licencia.setter
    def nro_licencia(self, value):
        if value:
            self._nro_licencia = value

    @property
    def telefono(self):
        return self._telefono
    @telefono.setter
    def telefono(self, value):
        self._telefono = value

    def __str__(self):
        return f"{self._nombre} (Lic: {self._nro_licencia})"


class Ruta:
    def __init__(self, origen, destino, distancia):
        if distancia <= 0:
            raise ValueError("Distancia positiva")
        if not origen or not destino:
            raise ValueError("Origen y destino no vacíos")
        self._id_ruta = str(uuid.uuid4())
        self._origen = origen
        self._destino = destino
        self._distancia = distancia

    @property
    def id_ruta(self):
        return self._id_ruta

    @property
    def origen(self):
        return self._origen
    @origen.setter
    def origen(self, value):
        if value:
            self._origen = value

    @property
    def destino(self):
        return self._destino
    @destino.setter
    def destino(self, value):
        if value:
            self._destino = value

    @property
    def distancia(self):
        return self._distancia
    @distancia.setter
    def distancia(self, value):
        if value > 0:
            self._distancia = value

    def __str__(self):
        return f"{self._origen} → {self._destino} ({self._distancia} km)"


class Servicio:
    def __init__(self, vehiculo, conductor, ruta, dias_semana, hora_salida, fecha_inicio):
        self._id = str(uuid.uuid4())
        self._vehiculo = vehiculo
        self._conductor = conductor
        self._ruta = ruta
        self._dias_semana = dias_semana
        self._hora_salida = hora_salida
        self._fecha_inicio = fecha_inicio

    @property
    def id(self):
        return self._id

    @property
    def vehiculo(self):
        return self._vehiculo
    @vehiculo.setter
    def vehiculo(self, value):
        self._vehiculo = value

    @property
    def conductor(self):
        return self._conductor
    @conductor.setter
    def conductor(self, value):
        self._conductor = value

    @property
    def ruta(self):
        return self._ruta
    @ruta.setter
    def ruta(self, value):
        self._ruta = value

    @property
    def dias_semana(self):
        return self._dias_semana
    @dias_semana.setter
    def dias_semana(self, value):
        self._dias_semana = value

    @property
    def hora_salida(self):
        return self._hora_salida
    @hora_salida.setter
    def hora_salida(self, value):
        self._hora_salida = value

    @property
    def fecha_inicio(self):
        return self._fecha_inicio
    @fecha_inicio.setter
    def fecha_inicio(self, value):
        self._fecha_inicio = value

    def generar_ocurrencias(self, desde, hasta):
        if hasta < self._fecha_inicio:
            return []
        ocurrencias = []
        fecha_actual = max(desde.date(), self._fecha_inicio.date())
        fin = hasta.date()
        while fecha_actual <= fin:
            if fecha_actual.weekday() in self._dias_semana:
                dt = datetime.combine(fecha_actual, self._hora_salida)
                ocurrencias.append(dt)
            fecha_actual += timedelta(days=1)
        return ocurrencias

    def __str__(self):
        dias_str = "- ".join(NOMBRE_DIA[d] for d in sorted(self._dias_semana))
        return (f"Servicio {self._id[-8:]}: {self._vehiculo.placa}, {self._conductor.nombre}, "
                f"{self._ruta.origen}→{self._ruta.destino}, {dias_str} a las {self._hora_salida.strftime('%H:%M')}")


# EMPRESA
class Empresa:
    def __init__(self, nombre, precio_combustible=11500.0):
        self._id_empresa = str(uuid.uuid4())
        self._nombre = nombre
        self._precio_combustible = precio_combustible
        self._vehiculos = []
        self._conductores = []
        self._rutas = []
        self._servicios = []
        self._fecha_creacion = datetime.now()

    @property
    def id_empresa(self):
        return self._id_empresa

    @property
    def nombre(self):
        return self._nombre
    @nombre.setter
    def nombre(self, value):
        if value.strip():
            self._nombre = value.strip()
        else:
            raise ValueError("Nombre vacío")

    @property
    def precio_combustible(self):
        return self._precio_combustible
    @precio_combustible.setter
    def precio_combustible(self, value):
        self._precio_combustible = value

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @property
    def vehiculos(self):
        return self._vehiculos.copy()
    @property
    def conductores(self):
        return self._conductores.copy()
    @property
    def rutas(self):
        return self._rutas.copy()
    @property
    def servicios(self):
        return self._servicios.copy()
    def guardar_empresa(self):
        with open("empresa.csv", "a") as archivo:
            archivo.write(
                f"{self.id_empresa},{self.nombre},{self.precio_combustible},{self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
    def agregar_vehiculo(self, v):
        self._vehiculos.append(v)
        with open("vehiculos.csv", "a") as archivo:
            archivo.write(f"{self.id_empresa},{v.placa},{v.modelo},{v.categoria},{v.capacidad},{v.consumo_combustible},{v.costo_man_km}\n")
            
        archivo.close()      
    def agregar_conductor(self, c):
        with open("conductores.csv", "a") as archivo:
            archivo.write(f"{self.id_empresa},{c.nombre},{c.nro_licencia},{c.telefono}\n")
        self._conductores.append(c)
    def agregar_ruta(self, r):
        with open("rutas.csv", "a") as archivo:
            archivo.write(f"{self.id_empresa},{r.id_ruta},{r.origen},{r.destino},{r.distancia}\n")
        self._rutas.append(r)

    def agregar_servicio(self, s):
        with open("servicios.csv", "a") as archivo:
            dias_str = "-".join(map(str, sorted(s.dias_semana)))
            archivo.write(f"{self.id_empresa},{s.vehiculo.placa},{s.conductor.nro_licencia},{s.ruta.id_ruta},{dias_str},{s.hora_salida.strftime('%H:%M')},{s.fecha_inicio.strftime('%Y-%m-%d')}\n")
        self._servicios.append(s)
    def eliminar_vehiculo(self, idx):
        if 0 <= idx < len(self._vehiculos):
            vehiculo = self._vehiculos[idx]
            with open("vehiculos.csv", "r") as archivo:
                lineas = archivo.readlines()
            with open("vehiculos.csv", "w") as archivo:
                for linea in lineas:
                    datos = linea.strip().split(",")
                    if (
                        len(datos) >= 7 and
                        datos[0] == self.id_empresa and
                        datos[1] == vehiculo.placa
                    ):
                        continue
                    archivo.write(linea)
            del self._vehiculos[idx]
            return True
        return False
    def eliminar_conductor(self, idx):
        if 0 <= idx < len(self._conductores):
            conductor = self._conductores[idx]
            with open("conductores.csv", "r") as archivo:
                lineas = archivo.readlines()
            with open("conductores.csv", "w") as archivo:
                for linea in lineas:
                    datos = linea.strip().split(",")
                    if (
                        len(datos) >= 4 and
                        datos[0] == self.id_empresa and
                        datos[2] == conductor.nro_licencia
                    ):
                        continue
                    archivo.write(linea)
            del self._conductores[idx]
            return True
        return False
    def eliminar_ruta(self, idx):
        if 0 <= idx < len(self._rutas):
            ruta = self._rutas[idx]
            with open("rutas.csv", "r") as archivo:
                lineas = archivo.readlines()
            with open("rutas.csv", "w") as archivo:
                for linea in lineas:
                    datos = linea.strip().split(",")
                    if (
                        len(datos) >= 4 and
                        datos[0] == self.id_empresa and
                        datos[1] == ruta.origen and
                        datos[2] == ruta.destino
                    ):
                        continue
                    archivo.write(linea)
            del self._rutas[idx]
            return True
        return False
    def eliminar_servicio(self, idx):
        if 0 <= idx < len(self._servicios):
            servicio = self._servicios[idx]
            with open("servicios.csv", "r") as archivo:
                lineas = archivo.readlines()
            with open("servicios.csv", "w") as archivo:
                for linea in lineas:
                    datos = linea.strip().split(",")
                    if (
                        len(datos) >= 4 and
                        datos[0] == self.id_empresa and
                        datos[1] == servicio.vehiculo.placa
                    ):
                        continue
                    archivo.write(linea)
            del self._servicios[idx]
            return True
        return False
    def _expandir_servicios(self, inicio, fin):
        ocurrencias = []
        for s in self._servicios:
            for fecha in s.generar_ocurrencias(inicio, fin):
                ocurrencias.append((s, fecha))
        return ocurrencias

    def calcular_metricas_servicio(self, servicio, fecha):
        duracion = servicio.vehiculo.tiempo_viaje(servicio.ruta.distancia)
        costo_total = (servicio.vehiculo.costo_combustible(servicio.ruta.distancia, self._precio_combustible) +
                       servicio.vehiculo.costo_mantenimiento(servicio.ruta.distancia))
        ocupacion = 1.0
        eficiencia = ocupacion / duracion
        costo_por_pasajero = costo_total / servicio.vehiculo.capacidad
        return {
            "fecha": fecha,
            "duracion_h": duracion,
            "costo_total": costo_total,
            "ocupacion_%": ocupacion * 100,
            "eficiencia_%": eficiencia * 100,
            "costo_x_pasajero": costo_por_pasajero
        }

    def reporte_ocupacion(self, inicio, fin):
        ocurrencias = self._expandir_servicios(inicio, fin)
        if not ocurrencias:
            return "No hay viajes en el rango seleccionado."
        total = len(ocurrencias)
        return (f"Todos los {total} viajes programados en el rango tienen una ocupación del 100% "
                f"(capacidad máxima de cada vehículo).\n"
                f"Promedio: 100% | Máxima: 100% | Mínima: 100%")

    def reporte_eficiencia(self, inicio, fin):
        ocurrencias = self._expandir_servicios(inicio, fin)
        if not ocurrencias:
            return "No hay viajes en el rango seleccionado."
        lineas = []
        eficiencias_porc = []
        for s, fecha in ocurrencias:
            duracion = s.vehiculo.tiempo_viaje(s.ruta.distancia)
            ef_porc = (1.0 / duracion) * 100
            eficiencias_porc.append(ef_porc)
            lineas.append(f"  • {fecha.strftime('%Y-%m-%d %H:%M')} | Servicio {s.id[-8:]} | Eficiencia: {ef_porc:.2f}%")
        promedio = np.mean(eficiencias_porc)
        maximo = np.max(eficiencias_porc)
        minimo = np.min(eficiencias_porc)
        resultado = "\n".join(lineas)
        resultado += f"\n\n Resumen:\n  Promedio: {promedio:.2f}%\n  Máxima: {maximo:.2f}%\n  Mínima: {minimo:.2f}%"
        return resultado

    def reporte_conductor(self, conductor, inicio, fin):
        resultado = []
        for s, fecha in self._expandir_servicios(inicio, fin):
            if s.conductor == conductor:
                m = self.calcular_metricas_servicio(s, fecha)
                resultado.append(
                    f"   {m['fecha'].strftime('%Y-%m-%d %H:%M')} | Servicio {s.id[-8:]} | "
                    f"Duración: {m['duracion_h']:.2f}h | Costo total: ${m['costo_total']:,.0f} COP | "
                    f"Costo por pasajero: ${m['costo_x_pasajero']:,.0f} COP | Eficiencia: {m['eficiencia_%']:.2f}%"
                )
        if not resultado:
            return f"No se encontraron viajes para {conductor.nombre} en el rango indicado."
        return f" Viajes de {conductor.nombre}:\n" + "\n".join(resultado)

    def reporte_empresa(self, inicio, fin):
        ocurrencias = self._expandir_servicios(inicio, fin)
        if not ocurrencias:
            return {
                "Nombre": self._nombre,
                "Fecha de creación": self._fecha_creacion.strftime("%Y-%m-%d %H:%M"),
                "Precio combustible (COP/L)": self._precio_combustible,
                "Vehículos": len(self._vehiculos),
                "Conductores": len(self._conductores),
                "Rutas": len(self._rutas),
                "Servicios activos": len(self._servicios),
                "Viajes en rango": 0,
                "Ocupación promedio (%)": None,
                "Eficiencia promedio (%)": None,
                "Costo promedio por viaje (COP)": None,
                "Costo por pasajero (COP)": None,
                "ID Empresa": self._id_empresa
            }
        eficiencias_porc = []
        costos = []
        costos_x_pasajero = []
        for s, fecha in ocurrencias:
            m = self.calcular_metricas_servicio(s, fecha)
            eficiencias_porc.append(m["eficiencia_%"])
            costos.append(m["costo_total"])
            costos_x_pasajero.append(m["costo_x_pasajero"])
        return {
            "Nombre": self._nombre,
            "Fecha de creación": self._fecha_creacion.strftime("%Y-%m-%d %H:%M"),
            "Precio combustible (COP/L)": self._precio_combustible,
            "Vehículos": len(self._vehiculos),
            "Conductores": len(self._conductores),
            "Rutas": len(self._rutas),
            "Servicios activos": len(self._servicios),
            "Viajes en rango": len(ocurrencias),
            "Ocupación promedio (%)": 100.0,
            "Eficiencia promedio (%)": round(np.mean(eficiencias_porc), 2),
            "Costo promedio por viaje (COP)": round(np.mean(costos), 0),
            "Costo por pasajero (COP)": round(np.mean(costos_x_pasajero), 0),
            "ID Empresa": self._id_empresa
        }

    def editar_nombre(self, nuevo): 
        if not nuevo.strip():
            raise ValueError("Nombre vacío")
        nombre_viejo = self._nombre
        self._nombre = nuevo.strip()
        with open("empresa.csv", "r") as archivo:
            lineas = archivo.readlines()
        with open("empresa.csv", "w") as archivo:
            for linea in lineas:
                datos = linea.strip().split(",")
                if len(datos) >= 4 and datos[0] == self._id_empresa:
                    datos[1] = self._nombre
                    archivo.write(",".join(datos) + "\n")
                else:
                    archivo.write(linea)

    def editar_precio_combustible(self, nuevo_precio):
        self._precio_combustible = nuevo_precio
        with open("empresa.csv", "r") as archivo:
            lineas = archivo.readlines()
        with open("empresa.csv", "w") as archivo:
            for linea in lineas:
                datos = linea.strip().split(",")
                if len(datos) >= 4 and datos[0] == self._id_empresa:
                    datos[2] = str(nuevo_precio)
                    archivo.write(",".join(datos) + "\n")
                else:
                    archivo.write(linea)
    
# FUNCIONES AUXILIARES Y MENÚS
def cargar_vehiculos(emp):
    try:
        with open("vehiculos.csv", "r") as f:
            for linea in f:
                datos = linea.strip().split(",")
                if len(datos) == 7 and datos[0] == emp.id_empresa:
                    v = Vehiculo(
                        datos[1],
                        datos[2],
                        datos[3],
                        int(float(datos[4])),
                        float(datos[5]),
                        float(datos[6]),

                    )
                    emp._vehiculos.append(v)
    except FileNotFoundError:
        pass

def cargar_conductores(emp):
    try:
        with open("conductores.csv", "r") as f:
            for linea in f:
                datos = linea.strip().split(",")
                if len(datos) == 4 and datos[0] == emp.id_empresa:
                    c = Conductor(
                        datos[1],
                        datos[2],
                        datos[3]
                    )
                    emp._conductores.append(c)
    except FileNotFoundError:
        pass

def cargar_rutas(emp):
    try:
        with open("rutas.csv", "r") as f:
            for linea in f:
                datos = linea.strip().split(",")
                if len(datos) == 5 and datos[0] == emp.id_empresa:
                    r = Ruta(
                        datos[2],
                        datos[3],
                        float(datos[4])
                    )
                    r._id_ruta = datos[1]
                    emp._rutas.append(r)

    except FileNotFoundError:
        pass

def cargar_servicios(emp):
    try:
        with open("servicios.csv", "r") as f:
            for linea in f:
                datos = linea.strip().split(",")
                if len(datos) == 7 and datos[0] == emp.id_empresa:
                    vehiculo = next((v for v in emp._vehiculos if v.placa == datos[1]), None)
                    conductor = next((c for c in emp._conductores if c.nro_licencia == datos[2]), None)
                    ruta = next((r for r in emp._rutas if r.id_ruta == datos[3]), None)
                    dias_semana = list(map(int, datos[4].split("-")))
                    hora_salida = datetime.strptime(datos[5], "%H:%M").time()
                    fecha_inicio = datetime.strptime(datos[6], "%Y-%m-%d")
                    if vehiculo is None or conductor is None or ruta is None:
                        continue
                    s = Servicio(vehiculo, conductor, ruta, dias_semana, hora_salida, fecha_inicio)
                    emp._servicios.append(s)
    except FileNotFoundError:
        pass

def cargar_empresas():
    empresas = {}

    try:
        with open("empresa.csv", "r") as archivo:
            for linea in archivo:
                datos = linea.strip().split(",")

                if len(datos) < 3:
                    continue

                e = Empresa(datos[1], float(datos[2]))
                e._id_empresa = datos[0]

                cargar_vehiculos(e)
                cargar_conductores(e)
                cargar_rutas(e)
                cargar_servicios(e)

                empresas[e.id_empresa] = e

    except FileNotFoundError:
        pass

    return empresas

def leer_entero(mensaje, min=None, max=None):
    while True:
        try:
            val = int(input(mensaje))
            if min is not None and val < min:
                print(f"Mínimo {min}")
                continue
            if max is not None and val > max:
                print(f"Máximo {max}")
                continue
            return val
        except ValueError:
            print("Número entero válido")

def leer_float(mensaje, positivo=True):
    while True:
        try:
            val = float(input(mensaje))
            if positivo and val <= 0:
                print("Debe ser >0")
            else:
                return val
        except ValueError:
            print("Número válido")

def leer_hora(mensaje):
    while True:
        try:
            return datetime.strptime(input(mensaje), "%H:%M").time()
        except:
            print("Formato HH:MM")

def leer_fecha(mensaje):
    while True:
        try:
            return datetime.strptime(input(mensaje), "%Y-%m-%d")
        except:
            print("Formato AAAA-MM-DD")

def rango_fechas():
    print("\n-- Rango de fechas para consulta --")
    hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    inicio_defecto = datetime(hoy.year, 1, 1)
    fin_defecto = hoy
    ini_str = input(f"Inicio (YYYY-MM-DD) [ENTER desde {inicio_defecto.date()} hasta hoy]: ").strip()
    if ini_str == "":
        return inicio_defecto, fin_defecto
    ini = datetime.strptime(ini_str, "%Y-%m-%d")
    fin_str = input(f"Fin (YYYY-MM-DD) [ENTER hasta hoy {fin_defecto.date()}]: ").strip()
    if fin_str == "":
        fin = fin_defecto
    else:
        fin = datetime.strptime(fin_str, "%Y-%m-%d")
    if fin < ini:
        print("La fecha fin debe ser >= inicio. Usando rango por defecto.")
        return inicio_defecto, fin_defecto
    return ini, fin

def seleccionar_vehiculo(emp):
    if not emp._vehiculos:
        print("Sin vehículos")
        return None, None
    print("\nVehículos:")
    for i, v in enumerate(emp._vehiculos):
        print(f"{i+1}. {v}")
    idx = leer_entero("Número: ", 1, len(emp._vehiculos)) - 1
    return emp._vehiculos[idx], idx

def seleccionar_conductor(emp):
    if not emp._conductores:
        print("Sin conductores")
        return None, None
    print("\nConductores:")
    for i, c in enumerate(emp._conductores):
        print(f"{i+1}. {c}")
    idx = leer_entero("Número: ", 1, len(emp._conductores)) - 1
    return emp._conductores[idx], idx

def seleccionar_ruta(emp):
    if not emp._rutas:
        print("Sin rutas")
        return None, None
    print("\nRutas:")
    for i, r in enumerate(emp._rutas):
        print(f"{i+1}. {r}")
    idx = leer_entero("Número: ", 1, len(emp._rutas)) - 1
    return emp._rutas[idx], idx

def seleccionar_servicio(emp):
    if not emp._servicios:
        print("Sin servicios")
        return None, None
    print("\nServicios:")
    for i, s in enumerate(emp._servicios):
        print(f"{i+1}. {s}")
    idx = leer_entero("Número: ", 1, len(emp._servicios)) - 1
    return emp._servicios[idx], idx

def menu_editar_eliminar(emp):
    while True:
        print("\n-- Editar/Eliminar --")
        print("1. Editar nombre empresa")
        print("2. Editar vehículo")
        print("3. Eliminar vehículo")
        print("4. Editar conductor")
        print("5. Eliminar conductor")
        print("6. Editar ruta")
        print("7. Eliminar ruta")
        print("8. Eliminar servicio recurrente")
        print("9. Volver")
        op = input("Opción: ")
        if op == "1":
            nuevo = input("Nuevo nombre: ").strip()
            try:
                emp.editar_nombre(nuevo)
                print("Nombre actualizado")
            except Exception as e:
                print(e)
        elif op == "2":
            veh, idx = seleccionar_vehiculo(emp)
            if veh:
                print("Deje vacío para mantener")
                pl = input(f"Placa ({veh.placa}): ").strip()
                if pl:
                    veh.placa = pl
                mod = input(f"Modelo ({veh.modelo}): ").strip()
                if mod:
                    veh.modelo = mod
                cap = input(f"Capacidad ({veh.capacidad}): ").strip()
                if cap:
                    veh.capacidad = int(cap)
                cons = input(f"Consumo ({veh.consumo_combustible}): ").strip()
                if cons:
                    veh.consumo_combustible = float(cons)
                cost = input(f"Costo mant/km ({veh.costo_man_km}): ").strip()
                if cost:
                    veh.costo_man_km = float(cost)
                print("Vehículo actualizado")
        elif op == "3":
            _, idx = seleccionar_vehiculo(emp)
            if idx is not None and emp.eliminar_vehiculo(idx):
                print("Vehículo eliminado")
        elif op == "4":
            cond, idx = seleccionar_conductor(emp)
            if cond:
                nom = input(f"Nombre ({cond.nombre}): ").strip()
                if nom:
                    cond.nombre = nom
                lic = input(f"Licencia ({cond.nro_licencia}): ").strip()
                if lic:
                    cond.nro_licencia = lic
                tel = input(f"Teléfono ({cond.telefono}): ").strip()
                if tel:
                    cond.telefono = tel
                print("Conductor actualizado")
        elif op == "5":
            _, idx = seleccionar_conductor(emp)
            if idx is not None and emp.eliminar_conductor(idx):
                print("Conductor eliminado")
        elif op == "6":
            rut, idx = seleccionar_ruta(emp)
            if rut:
                o = input(f"Origen ({rut.origen}): ").strip()
                if o:
                    rut.origen = o
                d = input(f"Destino ({rut.destino}): ").strip()
                if d:
                    rut.destino = d
                dist = input(f"Distancia ({rut.distancia}): ").strip()
                if dist:
                    rut.distancia = float(dist)
                print("Ruta actualizada")
        elif op == "7":
            _, idx = seleccionar_ruta(emp)
            if idx is not None and emp.eliminar_ruta(idx):
                print("Ruta eliminada")
        elif op == "8":
            _, idx = seleccionar_servicio(emp)
            if idx is not None and emp.eliminar_servicio(idx):
                print("Servicio eliminado")
        elif op == "9":
            print("Volviendo al menú principal...")
            break
        else:
            print("Opción inválida")

def menu_empresa(emp):
    while True:
        print(f"\n-* Menú Empresa: {emp.nombre} *-")
        print("1. Registrar vehículo")
        print("2. Registrar conductor")
        print("3. Registrar ruta")
        print("4. Registrar servicio recurrente")
        print("5. Reporte ocupación (%)")
        print("6. Reporte eficiencia (%)")
        print("7. Reporte por conductor")
        print("8. Reporte general de empresa")
        print("9. Editar/Eliminar")
        print("10. Salir")
        op = input("Opción: ")

        if op == "1":
            placa = input("Placa: ").strip()
            modelo = input("Modelo: ").strip()
            categoria = input("Categoría (Bus/Van/Taxi): ").strip()
            capacidad = leer_entero("Capacidad: ", 1)
            consumo = leer_float("Consumo combustible (L/km): ")
            costo = leer_float("Costo mant/km: ", positivo=True)
            try:
                v = Vehiculo(placa, modelo, categoria, capacidad, consumo, costo)
                emp.agregar_vehiculo(v)
                print("Vehículo registrado")
            except Exception as e:
                print("Error:", e)

        elif op == "2":
            nombre = input("Nombre: ").strip()
            licencia = input("Número de licencia: ").strip()
            telefono = input("Teléfono: ").strip()
            try:
                c = Conductor(nombre, licencia, telefono)
                emp.agregar_conductor(c)
                print("Conductor registrado")
            except Exception as e:
                print("Error:", e)

        elif op == "3":
            origen = input("Origen: ").strip()
            destino = input("Destino: ").strip()
            distancia = leer_float("Distancia (km): ")
            try:
                r = Ruta(origen, destino, distancia)
                emp.agregar_ruta(r)
                print("Ruta registrada")
            except Exception as e:
                print("Error:", e)

        elif op == "4":
            veh, _ = seleccionar_vehiculo(emp)
            cond, _ = seleccionar_conductor(emp)
            rut, _ = seleccionar_ruta(emp)
            if veh and cond and rut:
                dias = input("Días de semana (ej: 0-2-4 para LUN-MIE-VIE): ").strip()
                dias_semana = list(map(int, dias.split("-")))
                hora = leer_hora("Hora salida (HH:MM): ")
                fecha_ini = leer_fecha("Fecha inicio (YYYY-MM-DD): ")
                s = Servicio(veh, cond, rut, dias_semana, hora, fecha_ini)
                emp.agregar_servicio(s)
                print("Servicio registrado")

        elif op == "5":
            ini, fin = rango_fechas()
            print(emp.reporte_ocupacion(ini, fin))

        elif op == "6":
            ini, fin = rango_fechas()
            print(emp.reporte_eficiencia(ini, fin))

        elif op == "7":
            cond, _ = seleccionar_conductor(emp)
            if cond:
                ini, fin = rango_fechas()
                print(emp.reporte_conductor(cond, ini, fin))

        elif op == "8":
            ini, fin = rango_fechas()
            print(emp.reporte_empresa(ini, fin))

        elif op == "9":
            menu_editar_eliminar(emp)

        elif op == "10":
            print("Saliendo del menú de empresa...")
            break

        else:
            print("Opción inválida")

def menu_principal():
    empresas = cargar_empresas()
    while True:
        print("\nSistema de Gestión de Transporte SGT - Menú Principal")
        print("1. Registrar empresa")
        print("2. Seleccionar empresa")
        print("3. Listar empresas")
        print("4. Salir")
        op = input("Opción: ")
        if op == "1":
            if op == "1":
                nom = input("Nombre: ").strip()
                if not nom:
                    continue
                precio = leer_float("Precio combustible por defecto (COP/L): ")
                e = Empresa(nom, precio)
                e.guardar_empresa()
                empresas[e.id_empresa] = e
                print(f"Empresa '{nom}' creada. ID: {e.id_empresa[-8:]}")
        elif op == "2":
            if not empresas:
                print("No hay empresas")
                continue
            print("\nEmpresas:")
            for id_, e in empresas.items():
                print(f"ID: {id_[-8:]} - {e.nombre}")
            sel = input("Ingrese ID: ").strip()
            encontrada = None
            for id_, e in empresas.items():
                if id_ == sel or id_.endswith(sel):
                    encontrada = e
                    break
            if encontrada:
                menu_empresa(encontrada)
            else:
                print("ID no válido")
        elif op == "3":
            if not empresas:
                print("No hay empresas")
            else:
                print("\n--Empresas--")
                for id_, e in empresas.items():
                    print(f"{e.nombre} - ID: {id_[-8:]}")
        elif op == "4":
            print("Saliendo...")
            break

if __name__ == "__main__":
    from datetime import datetime

    empresas = cargar_empresas()
    if not empresas:
        print(" No se cargaron empresas. Revisa que los CSV estén en la misma carpeta.")
    else:
        menu_principal()