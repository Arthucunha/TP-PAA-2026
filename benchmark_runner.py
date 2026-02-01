import os
import csv
import time
import statistics
import sys

sys.path.insert(0, os.path.dirname(__file__))

from dynamic_programming import solve_with_traceback_3d, read_input
from branch_and_bound import solve_instance as solve_bb
from backtracking import solve_backtracking_2d


class BenchmarkRunner:
    def __init__(self, instances_dir="instancias"):
        self.instances_dir = instances_dir
        self.results = []

    def run_all_instances(self):
        if not os.path.exists(self.instances_dir):
            print(f"Erro: Diretório '{self.instances_dir}' não encontrado!")
            return

        instances_by_category = self._group_instances_by_category()

        if not instances_by_category:
            print("Nenhuma instância encontrada")
            return

        print("=" * 100)
        print("BENCHMARK – MOCHILA 0-1 (2 RESTRIÇÕES)")
        print("Programação Dinâmica  vs  Branch and Bound  vs  Backtracking")
        print("=" * 100)
        print()

        for category in sorted(instances_by_category.keys()):
            print(f"Categoria: {category}")
            print("-" * 100)

            for filepath in sorted(instances_by_category[category]):
                name = os.path.basename(filepath)

                try:
                    # ===== Leitura =====
                    max_weight, max_volume, items = read_input(filepath)

                    weights = [w for w, v, val in items]
                    volumes = [v for w, v, val in items]
                    values  = [val for w, v, val in items]

                    # ===== Programação Dinâmica =====
                    dp_value, selected, dp_time = solve_with_traceback_3d(
                        max_weight, max_volume, items
                    )

                    # ===== Branch and Bound =====
                    t0 = time.perf_counter()
                    bb_value = solve_bb(filepath)
                    bb_time = time.perf_counter() - t0

                    # ===== Backtracking =====
                    t0 = time.perf_counter()
                    bt_value, _ = solve_backtracking_2d(
                        max_weight, max_volume, weights, volumes, values
                    )
                    bt_time = time.perf_counter() - t0

                    # ===== Checagem de corretude =====
                    if not (dp_value == bb_value == bt_value):
                        raise ValueError(
                            f"Valores diferentes! "
                            f"DP={dp_value}, BB={bb_value}, BT={bt_value}"
                        )

                    self.results.append({
                        'categoria': category,
                        'instancia': name,
                        'n_itens': len(items),
                        'peso_max': max_weight,
                        'volume_max': max_volume,
                        'valor_maximo': dp_value,
                        'tempo_dp': dp_time,
                        'tempo_bb': bb_time,
                        'tempo_bt': bt_time
                    })

                    print(
                        f"  OK {name:30} | "
                        f"Valor: {dp_value:6} | "
                        f"DP: {dp_time*1000:8.2f}ms | "
                        f"BB: {bb_time*1000:8.2f}ms | "
                        f"BT: {bt_time*1000:8.2f}ms"
                    )

                except Exception as e:
                    print(f"  ERR {name:30} | Erro: {e}")

    def _group_instances_by_category(self):
        categories = {}
        for filename in os.listdir(self.instances_dir):
            if filename.endswith(".txt"):
                category = "_".join(filename.replace(".txt", "").split("_")[:-1])
                categories.setdefault(category, []).append(
                    os.path.join(self.instances_dir, filename)
                )
        return categories

    def save_benchmark_csv(self, filename="benchmark_dp_bb_bt.csv"):
        if not self.results:
            print("Nenhum resultado para salvar!")
            return

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                'instancia',
                'n_itens',
                'peso_max',
                'volume_max',
                'valor_maximo',
                'tempo_dp_ms',
                'tempo_bb_ms',
                'tempo_bt_ms'
            ])
            writer.writeheader()

            for r in sorted(self.results, key=lambda x: (x['n_itens'], x['instancia'])):
                writer.writerow({
                    'instancia': r['instancia'],
                    'n_itens': r['n_itens'],
                    'peso_max': r['peso_max'],
                    'volume_max': r['volume_max'],
                    'valor_maximo': r['valor_maximo'],
                    'tempo_dp_ms': f"{r['tempo_dp']*1000:.2f}",
                    'tempo_bb_ms': f"{r['tempo_bb']*1000:.2f}",
                    'tempo_bt_ms': f"{r['tempo_bt']*1000:.2f}",
                })

        print(f"\nBenchmark salvo em: {filename}")

    def print_summary(self):
        print("\n" + "=" * 100)
        print("RESUMO FINAL")
        print("=" * 100)

        print(f"\nTotal de instâncias: {len(self.results)}")

        print("\nComparação por tamanho (n_itens):")
        sizes = {}

        for r in self.results:
            sizes.setdefault(r['n_itens'], {'dp': [], 'bb': [], 'bt': []})
            sizes[r['n_itens']]['dp'].append(r['tempo_dp'])
            sizes[r['n_itens']]['bb'].append(r['tempo_bb'])
            sizes[r['n_itens']]['bt'].append(r['tempo_bt'])

        for n in sorted(sizes.keys()):
            dp_avg = statistics.mean(sizes[n]['dp'])
            bb_avg = statistics.mean(sizes[n]['bb'])
            bt_avg = statistics.mean(sizes[n]['bt'])

            print(
                f"  n={n:2d} | "
                f"DP: {dp_avg*1000:8.2f}ms | "
                f"BB: {bb_avg*1000:8.2f}ms | "
                f"BT: {bt_avg*1000:8.2f}ms"
            )


def main():
    runner = BenchmarkRunner()
    runner.run_all_instances()
    runner.save_benchmark_csv()
    runner.print_summary()


if __name__ == "__main__":
    main()
