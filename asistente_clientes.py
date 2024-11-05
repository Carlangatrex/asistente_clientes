import sys
import pandas as pd
import pyexcel as pe
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

print("Iniciando el script...")

# Cargar la base de datos desde el archivo .ods
try:
    data = pe.get_records(file_name="Base de Datos Ixactech.ods")
    df = pd.DataFrame(data)
    print("Base de datos cargada correctamente")
except Exception as e:
    print(f"Error al cargar la base de datos: {e}")
    sys.exit(1)

# Lista de campos de búsqueda
campos_busqueda = [
    "Clientes de", "NIT O CC", "RAZÓN SOCIAL", "DIRECCION", "CIUDAD", 
    "TELEFONO", "TELEFONO 2", "TELEFONO 3", "TELEFONO 4", 
    "CORREO ELECTRONICO", "REPRESENTANTE LEGAL", "CEDULA DE REPRESENTANTE LEGAL"
]

def buscar_cliente(criterio):
    criterio = str(criterio).lower()
    mascara = df.apply(lambda row: any(criterio in str(value).lower() for value in row), axis=1)
    for campo in campos_busqueda:
        if campo in df.columns:
            mascara |= df[campo].astype(str).str.lower().str.contains(criterio, na=False)
    return df[mascara]

def simular_respuesta_ia(pregunta):
    print(f"Procesando pregunta: {pregunta}")
    pregunta = pregunta.lower()
    
    # Extraer el criterio de búsqueda de la pregunta
    criterio = pregunta.split("de")[-1].strip() if "de" in pregunta else pregunta
    
    resultados = buscar_cliente(criterio)
    
    if not resultados.empty:
        respuesta = f"He encontrado la siguiente información para '{criterio}':\n\n"
        for _, cliente in resultados.iterrows():
            for columna, valor in cliente.items():
                if pd.notna(valor):  # Verificar si el valor no es NaN
                    respuesta += f"{columna}: {valor}\n"
            respuesta += "\n"
    else:
        respuesta = f"Lo siento, no he encontrado ningún cliente que coincida con '{criterio}'."
    
    return respuesta

def main():
    print("Asistente virtual iniciado. Escribe 'salir' para terminar.")
    
    # Crear un completador con los campos de búsqueda
    completer = WordCompleter(campos_busqueda + ['salir'])
    
    while True:
        try:
            pregunta = prompt("Tú: ", completer=completer)
            if pregunta.lower() == 'salir':
                print("Saliendo del programa...")
                break
            
            respuesta_ia = simular_respuesta_ia(pregunta)
            print("Asistente:", respuesta_ia)
        except KeyboardInterrupt:
            print("\nPrograma interrumpido por el usuario.")
            break
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        print("Script finalizado")