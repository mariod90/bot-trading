import yfinance as yf
import matplotlib.pyplot as plt

# Variables MACRO del programa:
SENSIBILIDAD = 0.01
WINDOW_SIZE = 1


# Función para leer el fichero con la lista de criptomonedas:
def leer_fichero_scope(fichero):
    f_scope = open(fichero, "r")
    l_scope = f_scope.read().splitlines()
    f_scope.close()

    return l_scope


# Funcion para buscar los maximos y minimos locales del precio de una criptomoneda:
def buscar_maximos_minimos(datos):
    precio_cierre = datos["Close"]
    maximos, minimos = [], []

    for i_precio in range(2, len(precio_cierre) - 2):

        # Caso de maximo local:
        if WINDOW_SIZE == 1:
            if precio_cierre[i_precio] > precio_cierre[i_precio - 1] and precio_cierre[i_precio] > precio_cierre[
                i_precio + 1]:
                maximos.append(i_precio)
        if WINDOW_SIZE == 2:
            if precio_cierre[i_precio] > precio_cierre[i_precio - 2] and precio_cierre[i_precio] > precio_cierre[
                i_precio - 1] and precio_cierre[i_precio] > precio_cierre[i_precio + 1] and precio_cierre[i_precio] > \
                    precio_cierre[i_precio + 2]:
                maximos.append(i_precio)

        # Caso de minimo local:
        if WINDOW_SIZE == 1:
            if precio_cierre[i_precio] < precio_cierre[i_precio - 1] and precio_cierre[i_precio] < precio_cierre[
                i_precio + 1]:
                minimos.append(i_precio)
        if WINDOW_SIZE == 2:
            if precio_cierre[i_precio] < precio_cierre[i_precio - 2] and precio_cierre[i_precio] < precio_cierre[
                i_precio - 1] and precio_cierre[i_precio] < precio_cierre[i_precio + 1] and precio_cierre[i_precio] < \
                    precio_cierre[i_precio + 2]:
                minimos.append(i_precio)

    return maximos, minimos


# Funcion auxiliar para calcular la diferencia/distancia entre dos precios:
def distancia_precios(precio1, precio2):
    return 1 - (min([precio1, precio2]) / max([precio1, precio2]))


def buscar_soportes_resistencias(maximos, minimos, sensibilidad=SENSIBILIDAD):
    soportes, resistencias = [], []

    for i_minimo in range(1, len(minimos)):
        for j_minimo in range(1, len(minimos)):
            if distancia_precios(minimos[i_minimo], minimos[j_minimo]) < sensibilidad:
                if i_minimo != j_minimo:
                    soportes.append(i_minimo)

    for i_maximo in range(1, len(maximos)):
        for j_maximo in range(1, len(maximos)):
            if distancia_precios(maximos[i_maximo], maximos[j_maximo]) < sensibilidad:
                if i_maximo != j_maximo:
                    resistencias.append(i_maximo)

    return list(dict.fromkeys(soportes)), list(dict.fromkeys(resistencias))


if __name__ == "__main__":

    l_scope = leer_fichero_scope("min_scope.txt")

    for cripto in l_scope:

        try:

            datos = yf.Ticker(cripto + "-USD").history(period="1y")

            # Buscamos los maximos y minimos locales del precio de la criptomoneda:
            maximos, minimos = buscar_maximos_minimos(datos)

            # Buscamos los soportes y resistencias del precio de la criptomoneda:
            soportes, resistencias = buscar_soportes_resistencias(maximos, minimos)

            precios = datos["Close"]
            fechas = precios.index

            plt.figure(figsize=(12, 6))
            plt.plot(precios)
            for soporte in soportes:
                plt.plot([fechas[0], fechas[-1]], [precios[soporte], precios[soporte]], 'r')
            for resistencia in resistencias:
                plt.plot([fechas[0], fechas[-1]], [precios[resistencia], precios[resistencia]], 'g')
            plt.grid()
            plt.title(cripto, fontsize=20)
            plt.show()

        except:
            print("Error descargando los datos de " + cripto + ".")
