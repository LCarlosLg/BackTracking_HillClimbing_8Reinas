import time

def is_safe(board, col, row):
    """Verifica si se puede colocar una reina en (col, row) sin conflictos."""
    for c in range(col):
        r = board[c]
        if r == row or abs(r - row) == abs(c - col):
            return False
    return True

def solve_n_queens_generator(n):
    """Generador de soluciones de N-Reinas una por una, con nodos explorados y tiempo por solución."""
    board = [-1] * n

    def place_queen(col):
        nodos_explorados_local = 0
        if col >= n:
            yield board[:], nodos_explorados_local
            return
        for row in range(n):
            nodos_explorados_local += 1  # contar este nodo
            if is_safe(board, col, row):
                board[col] = row
                # Generar soluciones de las siguientes columnas
                for sol, nodos_sig in place_queen(col + 1):
                    yield sol, nodos_explorados_local + nodos_sig
                board[col] = -1  # backtrack
        return

    # Generador principal
    for solution, nodos in place_queen(0):
        yield solution, nodos

# ------------------------------
# EJECUCIÓN PRINCIPAL
# ------------------------------
if __name__ == "__main__":
    print("=== Problema de las N-Reinas (Backtracking) ===")

    # Validar número de reinas
    while True:
        try:
            n = int(input("Ingrese el número de reinas (entre 4 y 50): "))
            if n < 4 or n > 50:
                print(" Por favor ingrese un número entre 4 y 50.")
                continue
            break
        except ValueError:
            print(" Entrada no válida. Intente de nuevo con un número entero.")

    # Crear generador de soluciones
    gen_solutions = solve_n_queens_generator(n)

    index = 0
    while True:
        try:
            start_time = time.time()
            solution, nodos_explorados = next(gen_solutions)
            exec_time = time.time() - start_time
            index += 1

            print(f"\n Solución {index}: {solution}")
            print(f"Nodos explorados : {nodos_explorados}")
            print(f"Tiempo de cálculo: {exec_time:.6f} segundos")

            # Mostrar tablero
            for r in range(n):
                row_str = ""
                for c in range(n):
                    row_str += " Q " if solution[c] == r else " . "
                print(row_str)

            # Preguntar si desea otra solución
            otra = input("\n¿Desea ver otra solución? (s/n): ").lower()
            if otra != 's':
                print("Saliendo...")
                break
        except StopIteration:
            print("\n No hay más soluciones disponibles.")
            break
