from datetime import date, timedelta
import matplotlib.pyplot as plt
from collections import Counter

def calcular_pascoa(ano):
    """Algoritmo de Meeus/Jones/Butcher para calcular a Páscoa"""
    # ETAPA 1: Ciclo Metônico (19 anos)
    a = ano % 19
    # Posição do ano no ciclo lunar de 19 anos

    # ETAPA 2: Componentes do ano
    b = ano // 100  # Quociente da divisão por 100 (usado para correções do calendário)
    c = ano % 100   # Resto da divisão por 100 (ano dentro do grupo de 100)

    # ETAPA 3: Correções de anos bissextos
    d = b // 4      # Número de anos bissextos centuriais
    e = b % 4       # Resto

    # ETAPA 4: Correção da precessão lunar
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    # Ajuste para compensar a diferença entre ano lunar e solar

    # ETAPA 5: Epacta (idade da lua em 1º de janeiro)
    h = (19 * a + b - d - g + 15) % 30
    # Determina quando ocorre a lua cheia pascal

    # ETAPA 6: Componentes do dia da semana
    i = c // 4
    k = c % 4

    # ETAPA 7: Encontrar o domingo
    l = (32 + 2 * e + 2 * i - h - k) % 7
    # Ajusta para cair em um domingo

    # ETAPA 8: Correção final
    m = (a + 11 * h + 22 * l) // 451

    # ETAPA 9: Calcular mês e dia
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1
    
    return date(ano, mes, dia)

def calcular_carnaval(ano):
    """Calcula a terça-feira de Carnaval"""
    pascoa = calcular_pascoa(ano)
    carnaval = pascoa - timedelta(days=47)  # 47 dias antes da Páscoa
    return carnaval

# Gerar dados de 2000 a 2080
anos = range(2000, 2081)
carnavais = []
anos_17_fev = []  # Anos em que o Carnaval cai em 17/02

print("=== Calendário de Carnaval (2000-2080) ===\n")
for ano in anos:
    carnaval = calcular_carnaval(ano)
    carnavais.append(carnaval)
    
    # Verificar se cai em 17/02
    if carnaval.day == 17 and carnaval.month == 2:
        anos_17_fev.append(ano)
        print(f"{ano}: {carnaval.strftime('%d/%m/%Y')} ({carnaval.strftime('%A')}) *** 17/02 ***")
    else:
        print(f"{ano}: {carnaval.strftime('%d/%m/%Y')} ({carnaval.strftime('%A')})")

# Análise: Contar ocorrências por dia/mês
ocorrencias = Counter()
for carnaval in carnavais:
    # Criar chave: "dia/mês" (ex: "10/02" para 10 de fevereiro)
    chave = f"{carnaval.day:02d}/{carnaval.month:02d}"
    ocorrencias[chave] += 1

# Preparar dados para o gráfico
datas_str = sorted(ocorrencias.keys())
contagens = [ocorrencias[d] for d in datas_str]

# Destacar 17/02 no gráfico
cores = ['red' if d == '17/02' else 'blue' for d in datas_str]
tamanhos = [150 if d == '17/02' else 100 for d in datas_str]

# Criar gráfico de dispersão
plt.figure(figsize=(16, 7))
scatter = plt.scatter(range(len(datas_str)), contagens, 
                      alpha=0.6, s=tamanhos, c=cores)

# Configurar eixos
plt.xlabel('Data do Carnaval (Dia/Mês)', fontsize=12)
plt.ylabel('Quantidade de Ocorrências (2000-2080)', fontsize=12)
plt.title('Distribuição do Carnaval por Data (81 anos)', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)

# Ajustar labels do eixo X
plt.xticks(range(len(datas_str)), datas_str, rotation=90, fontsize=8)

# Adicionar linha de tendência/média
media = sum(contagens) / len(contagens)
plt.axhline(y=media, color='green', linestyle='--', 
            label=f'Média: {media:.1f}', linewidth=2)

# Destacar 17/02
if '17/02' in datas_str:
    idx_17_fev = datas_str.index('17/02')
    plt.scatter([idx_17_fev], [contagens[idx_17_fev]], 
                s=200, c='red', marker='*', 
                label=f'17/02 ({contagens[idx_17_fev]} vezes)', 
                edgecolors='black', linewidths=2, zorder=5)

plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig('carnaval_distribuicao.png', dpi=300, bbox_inches='tight')
plt.show()

# Estatísticas
print("\n" + "="*60)
print("=== ESTATÍSTICAS ===")
print("="*60)
print(f"Total de anos analisados: {len(anos)}")
print(f"Datas diferentes em que o Carnaval pode cair: {len(ocorrencias)}")

print(f"\n=== CARNAVAL EM 17/02 ===")
print(f"Quantidade de vezes: {len(anos_17_fev)}")
print(f"Anos em que o Carnaval cai em 17/02:")
if anos_17_fev:
    for i, ano in enumerate(anos_17_fev, 1):
        print(f"  {i}. {ano}")
else:
    print("  Nenhum ano no período 2000-2080")

print(f"\n=== Datas mais frequentes ===")
for data, count in ocorrencias.most_common(10):
    destaque = " ← 17/02!" if data == '17/02' else ""
    print(f"  {data}: {count} vezes{destaque}")

print(f"\n=== Datas menos frequentes ===")
for data, count in ocorrencias.most_common()[-10:]:
    destaque = " ← 17/02!" if data == '17/02' else ""
    print(f"  {data}: {count} vezes{destaque}")

# Informações adicionais sobre 17/02
if anos_17_fev:
    print(f"\n=== DETALHES SOBRE 17/02 ===")
    print(f"Primeiro ano: {anos_17_fev[0]}")
    print(f"Último ano: {anos_17_fev[-1]}")
    
    # Calcular intervalos entre ocorrências
    if len(anos_17_fev) > 1:
        intervalos = [anos_17_fev[i] - anos_17_fev[i-1] 
                     for i in range(1, len(anos_17_fev))]
        print(f"Intervalo médio entre ocorrências: {sum(intervalos)/len(intervalos):.1f} anos")
        print(f"Menor intervalo: {min(intervalos)} anos")
        print(f"Maior intervalo: {max(intervalos)} anos")
