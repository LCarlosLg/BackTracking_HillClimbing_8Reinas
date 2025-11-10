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
    """Resuelve el problema de las N-Reinas usando Hill Climbing con random restart adaptativo."""
    max_restarts = n * 10
    start_time = time.time()
    total_iterations = 0

    # NUEVO CODIGO: Se agregan variables para almacenar la mejor solución global encontrada
    # Sirve para no perder buenas configuraciones si ningún reinicio encuentra una solución perfecta.
    best_overall = None
    best_conflicts = float('inf')

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

            # Si se encuentra solución perfecta
            if current_conflicts == 0:
                elapsed = time.time() - start_time
                return board, total_iterations, elapsed

        # NUEVO CODIGO: Se compara con la mejor solución encontrada hasta el momento.
        # Si este reinicio obtuvo menos conflictos que los anteriores, se guarda.
        if current_conflicts < best_conflicts:
            best_conflicts = current_conflicts
            best_overall = board[:]

    # NUEVO CODIGO: Si después de todos los reinicios no se logra solución perfecta,
    # se retorna la mejor configuración encontrada (la más cercana a la solución).
    elapsed = time.time() - start_time
    return best_overall, total_iterations, elapsed


# ------------------------------
# EJECUCIÓN PRINCIPAL
# ------------------------------
if __name__ == "__main__":
    print("=== Hill Climbing Mejorado ===")

    all_N = []
    max_iterations = []
    max_times = []

    while True:
        try:
            n = int(input("\nIngrese el número de reinas (≥4, 0 para salir): "))
            if n == 0:
                print("Saliendo del programa...")
                if all_N:
                    plt.figure(figsize=(10,5))
                    plt.plot(all_N, max_iterations, marker='o', linestyle='-', color='blue', label='Iteraciones totales')
                    plt.plot(all_N, max_times, marker='x', linestyle='-', color='red', label='Tiempo de ejecución [s]')
                    plt.xlabel("Número de reinas (N)")
                    plt.ylabel("Iteraciones / Tiempo")
                    plt.title("Comparativa Hill Climbing Mejorado - Iteraciones y Tiempo vs N")
                    plt.xticks(all_N)
                    plt.grid(True, linestyle='--', alpha=0.7)
                    plt.legend()
                    plt.show()
                break

            if n < 4:
                print("Por favor ingrese un número mayor o igual a 4.")
                continue

            solution, iterations, exec_time = hill_climbing(n)

            print("\n=== Resultados Hill Climbing Mejorado ===")

            # NUEVO CODIGO : Validación adicional.- si no se encontró una solución perfecta, avisar al usuario
            if conflicts(solution) == 0:
                print(" Solución encontrada:")
            else:
                print(" No se encontró una solución perfecta, pero se devuelve la mejor configuración posible.")

            print(solution)
            print(f"Iteraciones totales: {iterations}")
            print(f"Tiempo de ejecución: {exec_time:.4f} segundos")

            # Mostrar tablero en consola
            print("\nTablero:")
            for r in range(n):
                row_str = ""
                for c in range(n):
                    row_str += " Q " if solution[c] == r else " . "
                print(row_str)

            # Guardar datos para gráfica
            all_N.append(n)
            max_iterations.append(iterations)
            max_times.append(exec_time)

        except ValueError:
            print("Entrada no válida. Intente de nuevo con un número entero.")
