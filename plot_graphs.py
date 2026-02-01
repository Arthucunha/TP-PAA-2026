import pandas as pd
import matplotlib.pyplot as plt
import sys

def plot_results(csv_file):
    # Lê o CSV
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{csv_file}' não encontrado.")
        return

    # Agrupa por número de itens para tirar a média de tempo de cada tamanho
    # Isso suaviza variações entre instâncias do mesmo tamanho
    df_grouped = df.groupby('n_itens')[['tempo_dp_ms', 'tempo_bb_ms', 'tempo_bt_ms']].mean()

    # Configuração de Estilo (similar ao matplotlib padrão)
    styles = {
        'tempo_dp_ms': {'label': 'Dynamic Programming', 'marker': 'o', 'color': '#1f77b4'}, # Azul
        'tempo_bb_ms': {'label': 'Branch & Bound', 'marker': 's', 'color': '#ff7f0e'},      # Laranja
        'tempo_bt_ms': {'label': 'Backtracking', 'marker': '^', 'color': '#2ca02c'}          # Verde
    }

    # --- Gráfico 1: Escala Linear ---
    plt.figure(figsize=(10, 6))
    for col, style in styles.items():
        plt.plot(df_grouped.index, df_grouped[col], 
                 marker=style['marker'], label=style['label'], color=style['color'])
    
    plt.xlabel('Número de Itens (n)')
    plt.ylabel('Tempo de Execução (ms)')
    plt.title('Comparação de Performance: DP vs Branch vs Backtracking')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('comparacao_tempo_linear.png')
    print("Gerado: comparacao_tempo_linear.png")

    # --- Gráfico 2: Escala Logarítmica ---
    # Essencial para ver o crescimento exponencial do Backtracking
    plt.figure(figsize=(10, 6))
    for col, style in styles.items():
        plt.plot(df_grouped.index, df_grouped[col], 
                 marker=style['marker'], label=style['label'], color=style['color'])

    plt.yscale('log') # O segredo para visualizar dados exponenciais
    plt.xlabel('Número de Itens (n)')
    plt.ylabel('Tempo de Execução (ms) - Escala Log')
    plt.title('Comparação de Performance (Escala Logarítmica)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('comparacao_tempo_log.png')
    print("Gerado: comparacao_tempo_log.png")

if __name__ == "__main__":
    # Pode passar o nome do arquivo como argumento ou usar o padrão
    file_name = sys.argv[1] if len(sys.argv) > 1 else 'results.csv'
    plot_results(file_name)