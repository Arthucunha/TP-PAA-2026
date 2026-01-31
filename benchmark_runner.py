import os
import csv
import time
import statistics
from pathlib import Path
import sys

sys.path.insert(0, os.path.dirname(__file__))
from dynamic_programming import solve_with_traceback_3d, read_input


class BenchmarkRunner:
    # Roda os testes de desempenho
    
    def __init__(self, instances_dir="instancias"):
        self.instances_dir = instances_dir
        self.results = []
        self.category_stats = {}
    
    def run_all_instances(self):
        # Executa todos os testes
        
        if not os.path.exists(self.instances_dir):
            print(f"Erro: Diretório '{self.instances_dir}' não encontrado!")
            return
        
        # Agrupa instâncias por categoria
        instances_by_category = self._group_instances_by_category()
        
        if not instances_by_category:
            print(f"Nenhuma instância encontrada")
            return
        
        print("=" * 80)
        print("BENCHMARKING - PROBLEMA DA MOCHILA 0-1 COM DUAS RESTRIÇÕES")
        print("=" * 80)
        print()
        
        for category in sorted(instances_by_category.keys()):
            print(f"Categoria: {category}")
            print("-" * 80)
            
            times = []
            values = []
            
            for filepath in sorted(instances_by_category[category]):
                try:
                    # Lê instância
                    max_weight, max_volume, items = read_input(filepath)
                    
                    # Executa DP
                    max_value, selected_items, execution_time = solve_with_traceback_3d(
                        max_weight, max_volume, items
                    )
                    
                    # Armazena
                    times.append(execution_time)
                    values.append(max_value)
                    
                    self.results.append({
                        'categoria': category,
                        'instancia': os.path.basename(filepath),
                        'n_itens': len(items),
                        'peso_max': max_weight,
                        'volume_max': max_volume,
                        'valor_maximo': max_value,
                        'tempo_execucao': execution_time,
                        'itens_selecionados': len(selected_items)
                    })
                    
                    print(f"  OK {os.path.basename(filepath):30} | "
                          f"Valor: {max_value:6} | Tempo: {execution_time*1000:8.2f}ms")
                    
                except Exception as e:
                    print(f"  ERR {os.path.basename(filepath):30} | Erro: {str(e)}")
        
            # Estatísticas
            if times:
                self.category_stats[category] = {
                    'n_instancias': len(times),
                    'tempo_medio': statistics.mean(times),
                    'tempo_mediano': statistics.median(times),
                    'tempo_min': min(times),
                    'tempo_max': max(times),
                    'tempo_desvio': statistics.stdev(times) if len(times) > 1 else 0,
                    'valor_medio': statistics.mean(values),
                }
                
                stats = self.category_stats[category]
                print(f"\n  Estatísticas:")
                print(f"    Instâncias: {stats['n_instancias']}")
                print(f"    Tempo Médio: {stats['tempo_medio']*1000:.2f}ms")
                print(f"    Tempo Mediano: {stats['tempo_mediano']*1000:.2f}ms")
                print(f"    Tempo Min-Max: {stats['tempo_min']*1000:.2f}ms - {stats['tempo_max']*1000:.2f}ms")
                print(f"    Desvio Padrão: {stats['tempo_desvio']*1000:.2f}ms")
                print(f"    Valor Médio: {stats['valor_medio']:.2f}")
                print()
    
    def _group_instances_by_category(self):
        # Agrupa as instâncias por categoria (prefixo do nome)
        categories = {}
        
        for filename in os.listdir(self.instances_dir):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.instances_dir, filename)
                
                # Extrai o prefixo do nome
                category = '_'.join(filename.replace('.txt', '').split('_')[:-1])
                
                if category not in categories:
                    categories[category] = []
                
                categories[category].append(filepath)
        
        return categories
    
    def save_benchmark_csv(self, filename="benchmark_dp.csv"):
        # Salva um CSV pra comparar com outros algoritmos
        
        if not self.results:
            print("Nenhum resultado para salvar!")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'instancia', 'n_itens', 'peso_max', 'volume_max', 
                'tempo_dp_ms', 'valor_maximo'
            ])
            writer.writeheader()
            
            for result in sorted(self.results, key=lambda x: (x['n_itens'], x['instancia'])):
                writer.writerow({
                    'instancia': result['instancia'],
                    'n_itens': result['n_itens'],
                    'peso_max': result['peso_max'],
                    'volume_max': result['volume_max'],
                    'tempo_dp_ms': f"{result['tempo_execucao'] * 1000:.2f}",
                    'valor_maximo': result['valor_maximo']
                })
        
        print(f"Benchmark salvo em: {filename}")
    
    def print_summary(self):
        # Imprime um resumo dos resultados
        
        print("\n" + "=" * 80)
        print("RESUMO FINAL")
        print("=" * 80)
        
        total_time = sum(r['tempo_execucao'] for r in self.results)
        avg_time = statistics.mean([r['tempo_execucao'] for r in self.results]) if self.results else 0
        
        print(f"\nTotal de instâncias: {len(self.results)}")
        print(f"Tempo total: {total_time:.2f}s")
        print(f"Tempo médio: {avg_time*1000:.2f}ms")
        
        # Agrupa por tamanho
        print(f"\nDesempenho por tamanho:")
        sizes = {}
        for result in self.results:
            n = result['n_itens']
            if n not in sizes:
                sizes[n] = []
            sizes[n].append(result['tempo_execucao'])
        
        for n in sorted(sizes.keys()):
            times = sizes[n]
            print(f"  n={n:2d}: Tempo médio = {statistics.mean(times)*1000:7.2f}ms "
                  f"(min={min(times)*1000:7.2f}ms, max={max(times)*1000:7.2f}ms)")


def main():
    # Programa principal
    
    runner = BenchmarkRunner()
    runner.run_all_instances()
    
    # Salva apenas 1 CSV pra comparação
    runner.save_benchmark_csv("benchmark_dp.csv")
    
    runner.print_summary()
    
    print("\nArquivo de benchmark gerado: benchmark_dp.csv")
    print("Colunas: instancia, n_itens, peso_max, volume_max, tempo_dp_ms, valor_maximo")


if __name__ == "__main__":
    main()
