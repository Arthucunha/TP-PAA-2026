import sys
import os
import time

# --- MUDANÇA 1: Arrumar o caminho dos imports ---
# Pega o diretório onde este arquivo (main.py) está
current_dir = os.path.dirname(os.path.abspath(__file__))
# Sobe dois níveis para chegar na raiz do projeto (TP-PAA-2026)
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
# Adiciona a raiz ao sys.path para o Python encontrar o 'backtracking.py'
sys.path.append(project_root)

# Agora o import funciona sem gambiarras no terminal
from backtracking import solve_backtracking

def main():
    # --- MUDANÇA 2: Definir caminhos fixos ---
    # Define onde está o arquivo de input (na raiz do projeto)
    input_file_path = os.path.join(project_root, "input.txt")
    
    # Define o algoritmo padrão (já que você quer testar o backtrack)
    algorithm = "backtrack" 

    print(f"Lendo arquivo: {input_file_path}")
    
    try:
        with open(input_file_path, 'r') as f:
            input_data = f.read().split()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{input_file_path}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    if not input_data:
        print("Entrada vazia!", file=sys.stderr)
        sys.exit(1)

    # Processamento da entrada (igual ao anterior)
    iterator = iter(input_data)
    try:
        first_token = next(iterator)
        while not first_token.lstrip('-').isdigit(): 
            first_token = next(iterator)
            
        capacity = int(first_token)
        weights = []
        values = []
        
        while True:
            try:
                w = int(next(iterator))
                v = int(next(iterator))
                if w == -1: break 
                weights.append(w)
                values.append(v)
            except StopIteration:
                break
                
    except StopIteration:
        print("Entrada incompleta!", file=sys.stderr)
        sys.exit(1)

    # Execução
    print(f"Executando algoritmo: {algorithm}")
    start_time = time.perf_counter()
    
    if algorithm == "backtrack":
        best_value, best_selection = solve_backtracking(capacity, weights, values)
    else:
        print("Algoritmo não implementado.", file=sys.stderr)
        sys.exit(1)

    end_time = time.perf_counter()
    duration_micros = (end_time - start_time) * 1_000_000

    # Saída
    print("-" * 30)
    print(f"Valor máximo: {best_value}")
    items_str = " ".join(map(str, best_selection))
    print(f"Itens selecionados: {items_str}") 
    print(f"Tempo (µs): {int(duration_micros)}")
    print("-" * 30)

if __name__ == "__main__":
    main()