import numpy as np
import matplotlib.pyplot as plt

# Constants
k = 8.9875517873681764e9  # Coulomb constant, N m²/C²

# Function to get charge input from the user
def get_charge_input(charge_number):
    print(f"Enter details for Charge {charge_number}:")
    q = float(input("  Magnitude of charge (in Coulombs): "))
    xq = float(input("  X-position of charge: "))
    yq = float(input("  Y-position of charge: "))
    return [q, xq, yq]

# Ask for user input for three charges
charges = [get_charge_input(i+1) for i in range(3)]

# Defined charges for testing
#charges = [
#    [1e-9, 1.0, 1.0],  # Charge 1: 1nC at (1, 1)
#    [-1e-9, -1.0, -1.0],  # Charge 2: -1nC at (-1, -1)
#    [1e-9, -1.0, 1.0]   # Charge 3: 1nC at (-1, 1)
#]

# Define the grid for the field
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)

# Initialize electric field and potential arrays
Ex, Ey = np.zeros(X.shape), np.zeros(Y.shape)
V = np.zeros(X.shape)

# Calculate electric field and potential for each charge
for charge in charges:
    q, xq, yq = charge
    # Distance components
    dx = X - xq
    dy = Y - yq
    r = np.sqrt(dx**2 + dy**2)

    # Avoid division by zero at the charge location
    r[r == 0] = np.inf
    
    # Electric field components
    Ex += k * q * dx / r**3
    Ey += k * q * dy / r**3
    
    # Electric potential
    V += k * q / r

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Plot electric field lines in the first subplot
ax1.streamplot(X, Y, Ex, Ey, color='b', linewidth=1, density=1.5)
# Plot charges with color based on their sign
for charge in charges:
    color = 'red' if charge[0] > 0 else 'blue'  # Red for positive, Blue for negative
    ax1.scatter(charge[1], charge[2], color=color, s=50, marker='o')
ax1.set_title('Electric Field Lines')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.axis('equal')

# Plot equipotential lines in the second subplot
contour = ax2.contour(X, Y, V, levels=350, cmap='RdYlBu')
# Plot charges with color based on their sign
for charge in charges:
    color = 'red' if charge[0] > 0 else 'blue'  # Red for positive, Blue for negative
    ax2.scatter(charge[1], charge[2], color=color, s=50, marker='o')
ax2.set_title('Equipotential Lines')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.axis('equal')
fig.colorbar(contour, ax=ax2, orientation='vertical')

# Display the plots
plt.tight_layout()
plt.show()
