# branch_and_bound.py
# Solver Branch and Bound para Mochila 0-1 com duas restrições (peso e volume)

class Item:
    def __init__(self, peso, volume, valor):
        self.w = peso
        self.v = volume
        self.val = valor
        # densidade usada no bound
        self.ratio = valor / (peso + volume)


def read_instance(filepath):
    """
    Lê uma instância no formato:
    W V
    w1 v1 val1
    w2 v2 val2
    ...
    """
    with open(filepath, "r") as f:
        lines = f.readlines()

    W, V = map(int, lines[0].split())
    items = []

    for line in lines[1:]:
        w, v, val = map(int, line.split())
        items.append(Item(w, v, val))

    return W, V, items


def bound(items, idx, W, V, cur_w, cur_v, cur_val):
    # ----- Bound por PESO -----
    value_w = cur_val
    w = cur_w

    for i in range(idx, len(items)):
        if w + items[i].w <= W:
            w += items[i].w
            value_w += items[i].val
        else:
            remain = W - w
            value_w += items[i].val * (remain / items[i].w)
            break

    # ----- Bound por VOLUME -----
    value_v = cur_val
    v = cur_v

    for i in range(idx, len(items)):
        if v + items[i].v <= V:
            v += items[i].v
            value_v += items[i].val
        else:
            remain = V - v
            value_v += items[i].val * (remain / items[i].v)
            break

    # bound otimista
    return max(value_w, value_v)


def solve_instance(filepath):
    """
    Recebe o caminho da instância e retorna o valor ótimo
    """
    W, V, items = read_instance(filepath)

    # ordena por densidade
    items.sort(key=lambda x: x.ratio, reverse=True)

    best = 0

    def dfs(idx, cur_w, cur_v, cur_val):
        nonlocal best

        # viola restrições
        if cur_w > W or cur_v > V:
            return

        # fim da árvore
        if idx == len(items):
            if cur_val > best:
                best = cur_val
            return

        # poda por limite superior
        if bound(items, idx, W, V, cur_w, cur_v, cur_val) <= best:
            return

        # ramo: inclui item
        dfs(
            idx + 1,
            cur_w + items[idx].w,
            cur_v + items[idx].v,
            cur_val + items[idx].val
        )

        # ramo: exclui item
        dfs(idx + 1, cur_w, cur_v, cur_val)

    dfs(0, 0, 0, 0)
    return best


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Uso: python branch_and_bound.py <arquivo_instancia>")
        sys.exit(1)

    instance_path = sys.argv[1]
    result = solve_instance(instance_path)
    print(f"Valor ótimo: {result}")
