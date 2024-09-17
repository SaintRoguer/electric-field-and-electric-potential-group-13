import numpy as numpy
import matplotlib.pyplot as matplotlib

# Constantes
k = 8.9875517873681764e9  # Constante de Coulomb, cuyas unidades son N m²/C²

# Funcion para obtener una carga como input del usuario
def get_charge_input(charge_number):
    print(f"Enter details for Charge {charge_number}:")
    q = float(input("  Magnitude of charge (in Coulombs): "))
    xq = float(input("  X-position of charge: "))
    yq = float(input("  Y-position of charge: "))
    return [q, xq, yq]


# Pregunta al usuario por las cargas
charges_amount = int(input("number of charges: "))
charges = [get_charge_input(i+1) for i in range(charges_amount)]

# Solicita al usuario el punto donde calcular el campo electrico y potencial
point_x = float(input("Enter the X-coordinate of the point: "))
point_y = float(input("Enter the Y-coordinate of the point: "))

# Para recta con carga uniforme
#charges = []
#for i in range(400):
#    charges.append([1e-9, -200 + i, 0])

# Define la region del plano donde calcular campo y potencial
x = numpy.linspace(-10, 10, 100)
y = numpy.linspace(-10, 10, 100)
X, Y = numpy.meshgrid(x, y)

# Inicializa arrays para campo electrico y potencial
Ex, Ey = numpy.zeros(X.shape), numpy.zeros(Y.shape)
V = numpy.zeros(X.shape)

# Calculo del campo electrico y potencial para cada carga
field_ex, field_ey, potential = 0, 0, 0  # Variables para almacenar los valores en el punto
for charge in charges:
    q, xq, yq = charge

    # Componentes de la distancia
    dx = X - xq
    dy = Y - yq
    r = numpy.sqrt(dx**2 + dy**2)

    # Para evitar division entre 0
    r[r == 0] = numpy.inf
    
    # Componentes del campo electrico
    Ex += k * q * dx / r**3
    Ey += k * q * dy / r**3
    
    # Potencial electrico
    V += k * q / r

    # Calculo en el punto dado por el usuario
    dx_point = point_x - xq
    dy_point = point_y - yq
    r_point = numpy.sqrt(dx_point**2 + dy_point**2)

    # Para evitar division por 0 en el punto
    if r_point != 0:
        field_ex += k * q * dx_point / r_point**3
        field_ey += k * q * dy_point / r_point**3
        potential += k * q / r_point

# Muestra el campo eléctrico y el potencial en el punto ingresado
print(f"Electric field at point ({point_x}, {point_y}): Ex = {field_ex:.2e} N/C, Ey = {field_ey:.2e} N/C")
print(f"Electric potential at point ({point_x}, {point_y}): V = {potential:.2e} V")

# Crea dos figuras, una con dos sub-graficos y otra con uno solo
fig1, (ax1, ax2) = matplotlib.subplots(1, 2, figsize=(12, 6))
fig2, ax3 = matplotlib.subplots(1, 1, figsize=(6, 6))

# El grafico 1 es un grafico de flujo para el campo electrico
ax1.streamplot(X, Y, Ex, Ey, color='dimgray', linewidth=1, density=1.5)

# El grafico 2 es un grafico de contorno para las lineas equipotenciales
contour = ax2.contour(X, Y, V, levels=350, cmap='coolwarm')

# El grafico 3 sera una combinacion de graficos de lineas de contorno y flujo
ax3.contour(X, Y, V, levels=350, cmap='coolwarm')
ax3.streamplot(X, Y, Ex, Ey, color='dimgray', linewidth=1, density=1.5)

# Añade las cargas a los tres graficos
for charge in charges:
    color = 'red' if charge[0] > 0 else 'blue'  # Rojo para cargas positivas, azul para negativas
    ax1.scatter(charge[1], charge[2], color=color, s=50, marker='o')
    ax2.scatter(charge[1], charge[2], color=color, s=50, marker='o')
    ax3.scatter(charge[1], charge[2], color=color, s=50, marker='o')

# Datos extra para el grafico 1
ax1.set_title('Electric Field Lines')
ax1.set_xlabel('x [m]')
ax1.set_ylabel('y [m]')
ax1.axis('equal')

# Datos extra para el grafico 2
ax2.set_title('Equipotential Lines')
ax2.set_xlabel('x [m]')
ax2.set_ylabel('y [m]')
ax2.axis('equal')
fig1.colorbar(contour, ax=ax2, orientation='vertical')

# Datos extra para el grafico 3
ax3.set_title('Electric Field and Equipotential Lines')
ax3.set_xlabel('x [m]')
ax3.set_ylabel('y [m]')
ax3.axis('equal')
fig2.colorbar(contour, ax=ax3, orientation='vertical')

# Muestra los graficos
matplotlib.tight_layout()
matplotlib.show()
