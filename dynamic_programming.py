import time
import sys

class MochilaDP:
    # Classe para resolver mochila 0-1 com duas restrições usando DP
    # Restrições: peso máximo W e volume máximo V
    
    def __init__(self, max_weight, max_volume, items):
        self.max_weight = max_weight
        self.max_volume = max_volume
        self.items = items
        self.n_items = len(items)
        self.start_time = None
        self.end_time = None
    
    def solve(self):
        # Resolve o problema usando programação dinâmica
        # O(n * W * V) de tempo, O(n * W * V) de espaço
        
        self.start_time = time.time()
        
        # Cria a tabela DP
        dp = [[0] * (self.max_volume + 1) for _ in range(self.max_weight + 1)]
        parent = [[(-1, -1)] * (self.max_volume + 1) for _ in range(self.max_weight + 1)]
        
        # Preenche a tabela
        for i in range(self.n_items):
            weight, volume, value = self.items[i]
            
            # Vai de trás pra frente pra não usar o mesmo item duas vezes
            for w in range(self.max_weight, weight - 1, -1):
                for v in range(self.max_volume, volume - 1, -1):
                    # Valor sem incluir o item
                    value_without = dp[w][v]
                    
                    # Valor incluindo o item
                    value_with = dp[w - weight][v - volume] + value
                    
                    # Pega o melhor
                    if value_with > value_without:
                        dp[w][v] = value_with
                        parent[w][v] = (w - weight, v - volume)
        
        # Encontra os itens selecionados
        selected_items = self._trace_back(dp, parent)
        
        max_value = dp[self.max_weight][self.max_volume]
        self.end_time = time.time()
        execution_time = self.end_time - self.start_time
        
        return max_value, selected_items, execution_time
    
    def _trace_back(self, dp, parent):
        # Encontra quais itens foram selecionados rastreando de volta
        selected = []
        w, v = self.max_weight, self.max_volume
        
        # Reconstrói a solução
        for i in range(self.n_items - 1, -1, -1):
            weight, volume, value = self.items[i]
            
            if w >= weight and v >= volume:
                if (w > weight or v > volume) and \
                   dp[w][v] != dp[max(0, w - weight)][max(0, v - volume)]:
                    if dp[w][v] == dp[max(0, w - weight)][max(0, v - volume)] + value:
                        selected.append(i)
                        w -= weight
                        v -= volume
        
        selected.reverse()
        return selected


def solve_with_traceback_3d(max_weight, max_volume, items):
    # Versão usando tabela 3D pra rastrear melhor
    # Complexidade: O(n * W * V) tempo, O(n * W * V) espaço
    
    start_time = time.time()
    n = len(items)
    
    # Tabela DP 3D: dp[i][w][v] = valor máximo usando itens 0..i-1
    dp = [[[0] * (max_volume + 1) for _ in range(max_weight + 1)] for _ in range(n + 1)]
    
    # Preenche a tabela
    for i in range(1, n + 1):
        weight, volume, value = items[i - 1]
        
        for w in range(max_weight + 1):
            for v in range(max_volume + 1):
                # Sem incluir o item i-1
                dp[i][w][v] = dp[i - 1][w][v]
                
                # Com o item i-1 (se couber)
                if w >= weight and v >= volume:
                    dp[i][w][v] = max(dp[i][w][v], 
                                     dp[i - 1][w - weight][v - volume] + value)
    
    # Rastreia pra encontrar os itens
    selected = []
    w, v = max_weight, max_volume
    
    for i in range(n, 0, -1):
        weight, volume, value = items[i - 1]
        
        if w >= weight and v >= volume:
            if dp[i][w][v] != dp[i - 1][w][v]:
                selected.append(i - 1)
                w -= weight
                v -= volume
    
    selected.reverse()
    max_value = dp[n][max_weight][max_volume]
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return max_value, selected, execution_time


def read_input(filename):
    # Lê o arquivo de entrada
    # Formato: primeira linha tem W e V
    # Linhas seguintes: peso volume valor
    
    items = []
    
    with open(filename, 'r') as f:
        # Primeira linha
        first_line = f.readline().strip().split()
        max_weight = int(first_line[0])
        max_volume = int(first_line[1])
        
        # Resto dos itens
        for line in f:
            line = line.strip()
            if line:
                parts = line.split()
                weight = int(parts[0])
                volume = int(parts[1])
                value = int(parts[2])
                items.append((weight, volume, value))
    
    return max_weight, max_volume, items


def write_output(filename, max_value, selected_items, execution_time, items):
    # Escreve os resultados em um arquivo
    
    with open(filename, 'w') as f:
        f.write(f"Lucro Máximo: {max_value}\n")
        f.write(f"Tempo de Execução: {execution_time:.6f} segundos\n")
        f.write(f"\nItens Selecionados (índices): {selected_items}\n")
        f.write(f"Quantidade de Itens: {len(selected_items)}\n\n")
        
        total_weight = 0
        total_volume = 0
        
        f.write("Detalhes dos Itens Selecionados:\n")
        f.write("Índice\tPeso\tVolume\tValor\n")
        f.write("-" * 40 + "\n")
        
        for idx in selected_items:
            weight, volume, value = items[idx]
            f.write(f"{idx}\t{weight}\t{volume}\t{value}\n")
            total_weight += weight
            total_volume += volume
        
        f.write("-" * 40 + "\n")
        f.write(f"Total\t{total_weight}\t{total_volume}\t{max_value}\n")


def main():
    # Programa principal
    
    if len(sys.argv) < 2:
        print("Uso: python dynamic_programming.py <arquivo_entrada> [arquivo_saída]")
        print("\nExemplo de arquivo de entrada:")
        print("10 9")
        print("6 3 10")
        print("3 4 14")
        print("4 2 16")
        print("2 5 9")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output_dp.txt"
    
    # Lê entrada
    max_weight, max_volume, items = read_input(input_file)
    
    print(f"Peso máximo: {max_weight}")
    print(f"Volume máximo: {max_volume}")
    print(f"Quantidade de itens: {len(items)}")
    print()
    
    # Resolve
    max_value, selected_items, execution_time = solve_with_traceback_3d(
        max_weight, max_volume, items
    )
    
    # Mostra resultados
    print(f"Lucro Máximo: {max_value}")
    print(f"Itens Selecionados: {selected_items}")
    print(f"Tempo de Execução: {execution_time:.6f} segundos")
    print()
    
    # Calcula totais
    total_weight = sum(items[i][0] for i in selected_items)
    total_volume = sum(items[i][1] for i in selected_items)
    
    print(f"Peso Total: {total_weight}/{max_weight}")
    print(f"Volume Total: {total_volume}/{max_volume}")
    print()
    
    # Salva resultado
    write_output(output_file, max_value, selected_items, execution_time, items)
    print(f"Resultado salvo em: {output_file}")


if __name__ == "__main__":
    main()
