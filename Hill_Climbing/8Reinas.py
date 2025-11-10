import random
import time

def conflicts(board):
    """Cuenta los conflictos entre reinas."""
    n = len(board)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            # Conflicto si están en la misma fila o diagonal
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                count += 1
    return count

def random_board(n):
    """Genera un tablero inicial aleatorio con N reinas."""
    return [random.randint(0, n - 1) for _ in range(n)]

def hill_climbing(n):
    """Resuelve el problema de las N-Reinas usando Hill Climbing adaptativo."""
    # Escalar número de reinicios según tamaño del tablero
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

            # Explorar todos los movimientos posibles para cada reina
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

            # Si no hay conflictos, se encontró una solución
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
    
    # Solicitar número de reinas (n)
    while True:
        try:
            n = int(input("Ingrese el número de reinas (n ≥ 4): "))
            if n < 4:
                print("Por favor ingrese un número mayor o igual a 4.")
                continue
            break
        except ValueError:
            print("Entrada no válida. Intente de nuevo con un número entero.")

    solution, iterations, exec_time = hill_climbing(n)

    print("\n=== Resultados Hill Climbing ===")
    if solution:
        print(" Solución encontrada:")
        print(solution)
    else:
        print(" No se encontró solución después de varios intentos.")

    print(f"Iteraciones totales: {iterations}")
    print(f"Tiempo de ejecución: {exec_time:.4f} segundos")

    # Visualización del tablero
    if solution:
        print("\nTablero:")
        for r in range(n):
            row_str = ""
            for c in range(n):
                row_str += " Q " if solution[c] == r else " . "
            print(row_str)
