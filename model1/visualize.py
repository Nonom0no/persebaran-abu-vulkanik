import matplotlib.pyplot as plt

def plot(C):
    plt.imshow(C, cmap='inferno')
    plt.colorbar()
    plt.title("Distribusi Abu Vulkanik")
    plt.show()