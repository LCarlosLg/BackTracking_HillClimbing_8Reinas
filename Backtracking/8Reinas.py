import time
import matplotlib.pyplot as plt

def is_safe(board, col, row):
    for c in range(col):
        r = board[c]
        if r == row or abs(r - row) == abs(c - col):
            return False
    return True


def solve_n_queens_generator(n):
    board = [-1] * n

    def place_queen(col):
        nodos_explorados_local = 0
        if col >= n:
            yield board[:], nodos_explorados_local
            return

        # NUEVA LINEA DE CODIGO --- Poda adicional ---
        # En lugar de iterar por todas las filas, se filtran solo las filas seguras antes de intentar colocarlas.
        # Esto evita hacer llamadas recursivas innecesarias.
        safe_rows = [row for row in range(n) if is_safe(board, col, row)]
        # --- Fin de la poda ---

        for row in safe_rows:
            nodos_explorados_local += 1
            board[col] = row
            for sol, nodos_sig in place_queen(col + 1):
                yield sol, nodos_explorados_local + nodos_sig
            board[col] = -1
        return

    for solution, nodos in place_queen(0):
        yield solution, nodos


# ------------------------------
# EJECUCIÓN PRINCIPAL
# ------------------------------
if __name__ == "__main__":
    print("=== Backtracking con poda adicional ===")

    all_N = []
    max_nodos = []
    max_tiempos = []

    while True:
        while True:
            try:
                n = int(input("\nIngrese el número de reinas (4-20, 0 para salir): "))
                if n == 0:
                    print("Saliendo del programa...")

                    # Graficar resultados antes de salir
                    if all_N:
                        plt.figure(figsize=(10,5))
                        plt.plot(all_N, max_nodos, marker='o', linestyle='-', color='blue', label="Nodos explorados")
                        plt.plot(all_N, max_tiempos, marker='x', linestyle='-', color='red', label="Tiempo cálculo [s]")
                        plt.xlabel("Número de reinas (N)")
                        plt.ylabel("Nodos / Tiempo")
                        plt.title("Comparativa lineal de Nodos y Tiempo vs N")
                        plt.xticks(all_N)
                        plt.legend()
                        plt.grid(True, linestyle='--', alpha=0.7)
                        plt.show()
                    exit()

                if n < 4 or n > 20:
                    print("Por favor ingrese un número entre 4 y 20.")
                    continue
                break
            except ValueError:
                print("Entrada no válida. Intente de nuevo con un número entero.")

        gen_solutions = solve_n_queens_generator(n)

        index = 0
        tiempos = []
        nodos = []

        while True:
            try:
                start_time = time.time()
                solution, nodos_explorados = next(gen_solutions)
                exec_time = time.time() - start_time

                index += 1
                tiempos.append(exec_time)
                nodos.append(nodos_explorados)

                print(f"\nSolución {index}: {solution}")
                print(f"Nodos explorados : {nodos_explorados}")
                print(f"Tiempo de cálculo: {exec_time:.6f} segundos")

                for r in range(n):
                    row_str = ""
                    for c in range(n):
                        row_str += " Q " if solution[c] == r else " . "
                    print(row_str)

                otra = input(f"\n¿Desea ver otra solución para N={n}? (s/n): ").lower()
                if otra != 's':
                    print(f"Finalizando soluciones para N={n}...")
                    break
            except StopIteration:
                print(f"\nNo hay más soluciones disponibles para N={n}")
                break

        if index > 0:
            all_N.append(n)
            max_nodos.append(max(nodos))
            max_tiempos.append(max(tiempos))
            print(f"\nResumen para N={n}: Máx nodos={max(nodos)}, Máx tiempo={max(tiempos):.6f}s")
