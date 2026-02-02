import random
import os


def generate_instance(n_items, max_weight, max_volume, seed=None):
    # Gera uma instância aleatória
    
    if seed is not None:
        random.seed(seed)
    
    # Primeira linha com capacidades
    instance = f"{max_weight} {max_volume}\n"
    
    # Gera itens aleatórios
    for _ in range(n_items):
        weight = random.randint(1, max_weight // 3)
        volume = random.randint(1, max_volume // 3)
        value = random.randint(weight + volume, (weight + volume) * 3)
        instance += f"{weight}\t{volume}\t{value}\n"
    
    return instance


def create_test_instances():
    # Cria as instâncias de teste
    
    configs = [
        ("pequena_5", 5, 50, 40, 10),
        ("pequena_10", 10, 50, 40, 10),
        ("média_15", 15, 100, 80, 10),
        ("média_20", 20, 100, 80, 10),
        ("grande_25", 25, 150, 120, 10),
        ("grande_30", 30, 150, 120, 10),
        ("muito_grande_40", 40, 200, 160, 10),
        ("muito_grande_50", 50, 200, 160, 10),
    ]
    
    os.makedirs("instancias", exist_ok=True)
    
    for name, n_items, max_w, max_v, num_inst in configs:
        print(f"Gerando {num_inst} instâncias: {name}")
        
        for i in range(num_inst):
            data = generate_instance(n_items, max_w, max_v, seed=f"{name}_{i}".encode())
            
            filename = f"instancias/{name}_{i+1}.txt"
            with open(filename, 'w') as f:
                f.write(data)
            
            print(f"  ✓ Criado: {filename}")
    
    print("\nTodas as instâncias foram geradas!")


if __name__ == "__main__":
    create_test_instances()
