import random
import time
import matplotlib.pyplot as plt

def conflicts(board):
    """Cuenta los conflictos entre reinas."""
    n = len(board)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                count += 1
    return count

def random_board(n):
    """Genera un tablero inicial aleatorio con N reinas."""
    return [random.randint(0, n - 1) for _ in range(n)]

def hill_climbing(n):
    """Resuelve el problema de las N-Reinas usando Hill Climbing adaptativo."""
    max_restarts = n * 10
    start_time = time.time()
    total_iterations = 0

    for restart in range(max_restarts):
        board = random_board(n)
        current_conflicts = conflicts(board)
        improved = True

        while improved:
            improved = False
            total_iterations += 1
            best_move = (current_conflicts, board[:])

            for col in range(n):
                for row in range(n):
                    if board[col] != row:
                        new_board = board[:]
                        new_board[col] = row
                        new_conflicts = conflicts(new_board)
                        if new_conflicts < best_move[0]:
                            best_move = (new_conflicts, new_board)
                            improved = True

            if improved:
                current_conflicts, board = best_move

            if current_conflicts == 0:
                elapsed = time.time() - start_time
                return board, total_iterations, elapsed

    elapsed = time.time() - start_time
    return None, total_iterations, elapsed


# ------------------------------
# EJECUCIÓN PRINCIPAL
# ------------------------------
if __name__ == "__main__":
    print("=== Problema de las N-Reinas (Hill Climbing) ===")

    # Lista para almacenar la n cantidad de reinas.
    all_N = []
    max_iterations = []
    max_times = []

    while True:
        #   Codigo para pedir numero de reinas.
        while True:
            try:
                n = int(input("\nIngrese el número de reinas (≥4, 0 para salir): "))
                if n == 0:
                    print("Saliendo del programa...")
                    # Comparación con grafica para verificar antes de saLir del programa.
                    if all_N:
                        plt.figure(figsize=(10,5))
                        plt.plot(all_N, max_iterations, marker='o', linestyle='-', color='blue', label='Iteraciones totales')
                        plt.plot(all_N, max_times, marker='x', linestyle='-', color='red', label='Tiempo de ejecución [s]')
                        plt.xlabel("Número de reinas (N)")
                        plt.ylabel("Iteraciones / Tiempo")
                        plt.title("Comparativa Hill Climbing - Iteraciones y Tiempo vs N")
                        plt.xticks(all_N)
                        plt.grid(True, linestyle='--', alpha=0.7)
                        plt.legend()
                        plt.show()
                    exit()
                if n < 4:
                    print("Por favor ingrese un número mayor o igual a 4.")
                    continue
                break
            except ValueError:
                print("Entrada no válida. Intente de nuevo con un número entero.")

        # Esta linea de codigo ejecuta la solución Hill_Climbing 
        solution, iterations, exec_time = hill_climbing(n)

        print("\n=== Resultados Hill Climbing ===")
        if solution:
            print(" Solución encontrada:")
            print(solution)
        else:
            print(" No se encontró solución después de varios intentos.")

        print(f"Iteraciones totales: {iterations}")
        print(f"Tiempo de ejecución: {exec_time:.4f} segundos")

        # Esta linea de codigo mustra la solución en el tablero en consola 
        if solution:
            print("\nTablero:")
            for r in range(n):
                row_str = ""
                for c in range(n):
                    row_str += " Q " if solution[c] == r else " . "
                print(row_str)

        # En esta ultima linea de codigo se guardan los datos para mostrarlos en la grafica.
        all_N.append(n)
        max_iterations.append(iterations)
        max_times.append(exec_time)
