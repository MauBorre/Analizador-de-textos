import matplotlib.pyplot as plt

def obtener_diagrama(info: dict, nombre_imagen='.diagrama.png') -> str:
    """Crea un diagrama de barras donde en el eje de la X estan las claves y
    en el eje de la Y estan los valores del diccionario que se le pasa como parametro"""
    plt.figure(figsize=(5, 3))
    plt.bar(x=info.keys(), height=info.values())
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.savefig(nombre_imagen)
    return nombre_imagen