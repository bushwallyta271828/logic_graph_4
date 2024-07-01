import numpy as np
import matplotlib.pyplot as plt

def mandelbrot(h, w, max_iter):
    y, x = np.ogrid[-1.4:1.4:h*1j, -2:0.8:w*1j]
    c = x + y*1j
    z = c
    divtime = max_iter + np.zeros(z.shape, dtype=int)

    for i in range(max_iter):
        z = z**2 + c
        diverge = z*np.conj(z) > 2**2
        div_now = diverge & (divtime == max_iter)
        divtime[div_now] = i
        z[diverge] = 2

    return divtime

def main():
    h, w = 1000, 1500
    max_iter = 100
    
    plt.figure(figsize=(10, 10))
    plt.imshow(mandelbrot(h, w, max_iter), cmap='hot', extent=[-2, 0.8, -1.4, 1.4])
    plt.title('Mandelbrot Set')
    plt.xlabel('Re(c)')
    plt.ylabel('Im(c)')
    plt.colorbar(label='Iteration count')
    plt.savefig('mandelbrot.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    main()
