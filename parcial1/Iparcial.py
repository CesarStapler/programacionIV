import sqlite3
base_dato = "datos.db"

def obtener_conexion():
    return sqlite3.connect(base_dato)

def crear_tablas():
    tablas = [
        """
        CREATE TABLE IF NOT EXISTS datos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT NOT NULL,
            descripcion TEXT NOT NULL
        );
        """
    ]
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    for tabla in tablas:
        cursor.execute(tabla)


def principal():
    crear_tablas()
    menu = """
1) Nuevo Producto
2) Modificar el producto
3) Descripcion de producto
4) Listado de productos
5) Eliminar producto
6) Salir
Elige: """
    eleccion = ""
    while eleccion != "6":
        eleccion = input(menu)
        if eleccion == "1":
            producto = input("\nIngresa producto: ")
            posible_descripcion = buscar_descripcion_producto(producto)
            if posible_descripcion:
                print(f"El producto'{producto}' ya existe")
            else:
                descripcion= input("Informacion del Producto: ")
                agregar_producto(producto, descripcion)
                print("Producto agregado")
        if eleccion == "2":
            producto = input("\nProduto a corregir: ")
            nueva_descripcion = input("Descricion del Producto: ")
            editar_producto(producto, nueva_descripcion)
            print("Producto actualizado")
        if eleccion == "3":
            producto = input(
                "\nAgrege el producto que desee informacion: ")
            descripcion = buscar_descripcion_producto(producto)
            if descripcion:
                print(f"La descripción de '{producto}' es:\n{descripcion[0]}")
            else:
                print(f"Producto '{producto}' no encontrada")
        if eleccion == "4":
            productos = obtener_productos()
            print("\n====Lista de productos===\n")
            for producto in productos:
                print(producto[0])
        if eleccion == "5":
            producto = input("\nProducto para eliminar: ")
            eliminar_producto(producto)
        


def agregar_producto(producto, descripcion):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sentencia = "INSERT INTO inventario(producto, descripcion) VALUES (?, ?)"
    cursor.execute(sentencia, [producto, descripcion])
    conexion.commit()


def editar_producto(producto, nueva_descripcion):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sentencia = "UPDATE inventario SET descripción = ? WHERE producto = ?"
    cursor.execute(sentencia, [nueva_descripcion, producto])
    conexion.commit()


def eliminar_producto(producto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sentencia = "DELETE FROM inventario WHERE producto = ?"
    cursor.execute(sentencia, [producto])
    conexion.commit()


def obtener_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "SELECT producto FROM inventario"
    cursor.execute(consulta)
    return cursor.fetchall()


def buscar_descripcion_producto(producto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "SELECT descripcion FROM inventario WHERE producto = ?"
    cursor.execute(consulta, [producto])
    return cursor.fetchone()


if __name__ == '__main__':
   principal()