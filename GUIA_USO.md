# Guia de Uso - BbotFanTan

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.7 ou superior
- Arquivo de dados "31 dias" no diretório

### Instalação das Dependências
```bash
pip install -r requirements.txt
```

### Executar Análise Completa
```bash
python analisador_bbotfantan.py
```

## 📁 Estrutura de Arquivos

```
📦 BbotFanTan/
├── 📄 31 dias                    # Dados originais
├── 📄 README.md                  # Documentação principal
├── 📄 DOCUMENTACAO_TECNICA.md    # Documentação técnica
├── 📄 GUIA_USO.md               # Este guia
├── 📄 analisador_bbotfantan.py   # Script de análise
├── 📄 requirements.txt           # Dependências Python
├── 📊 analise_bbotfantan.png     # Gráficos gerados
├── 📊 estatisticas_bbotfantan.json # Dados exportados
└── 📊 dados_bbotfantan.csv       # Dados em CSV
```

## 🔧 Como Usar

### 1. Análise Automática Completa
O script `analisador_bbotfantan.py` executa automaticamente:
- ✅ Processamento dos dados
- ✅ Cálculo de estatísticas
- ✅ Geração de relatório
- ✅ Criação de gráficos
- ✅ Exportação de dados

### 2. Uso Personalizado
```python
from analisador_bbotfantan import AnalisadorBbotFanTan

# Criar analisador
analisador = AnalisadorBbotFanTan('31 dias')

# Processar dados
analisador.processar_dados()

# Calcular estatísticas
analisador.calcular_estatisticas_gerais()

# Gerar relatório
analisador.gerar_relatorio_texto()

# Gerar gráficos
analisador.gerar_graficos()

# Exportar dados
analisador.exportar_dados('json')
```

## 📊 Saídas Geradas

### 1. Relatório no Terminal
- Estatísticas gerais
- Performance por tipo de aposta
- Melhores e piores horários
- Análise de sequências
- Recomendações

### 2. Gráficos (analise_bbotfantan.png)
- Assertividade por tipo de aposta
- Distribuição temporal
- Assertividade diária
- Heatmap de performance

### 3. Dados Exportados
- **JSON**: `estatisticas_bbotfantan.json`
- **CSV**: `dados_bbotfantan.csv`

## 🎯 Interpretação dos Resultados

### Assertividade
- **80%+**: Excelente performance
- **70-80%**: Boa performance
- **<70%**: Precisa de ajustes

### Tipos de Aposta
- **1/2**: Mais estável, menor risco
- **2/3**: Equilibrada, risco moderado
- **3/4**: Maior risco, maior retorno

### Horários
- **Verde**: Horários de alta performance
- **Amarelo**: Performance moderada
- **Vermelho**: Horários a evitar

## 🔍 Análises Disponíveis

### 1. Estatísticas Gerais
- Total de apostas
- Taxa de assertividade
- Distribuição de resultados

### 2. Análise por Tipo
- Performance de cada tipo de aposta
- Frequência de uso
- Risco vs retorno

### 3. Análise Temporal
- Padrões por hora do dia
- Performance diária
- Tendências ao longo do tempo

### 4. Análise de Sequências
- Maior sequência de vitórias
- Maior sequência de derrotas
- Padrões de recuperação

## ⚙️ Configurações

### Modificar Parâmetros
```python
# Alterar período de análise
analisador.df = analisador.df[
    (analisador.df['data'] >= '2023-05-30') & 
    (analisador.df['data'] <= '2023-06-29')
]

# Filtrar por tipo de aposta
df_filtrado = analisador.df[analisador.df['tipo'] == '1/2']

# Filtrar por horário
df_horario = analisador.df[
    (analisador.df['hora_num'] >= 9) & 
    (analisador.df['hora_num'] <= 18)
]
```

### Personalizar Gráficos
```python
# Alterar cores
cores = ['#3498db', '#e74c3c', '#2ecc71']

# Alterar tamanho
plt.figure(figsize=(12, 8))

# Alterar estilo
plt.style.use('ggplot')
```

## 🐛 Solução de Problemas

### Erro: "Dados não processados"
```bash
# Certifique-se de executar primeiro:
analisador.processar_dados()
```

### Erro: "Arquivo não encontrado"
```bash
# Verifique se o arquivo "31 dias" está no diretório
ls -la "31 dias"
```

### Erro de Dependências
```bash
# Reinstale as dependências
pip install --upgrade -r requirements.txt
```

### Gráficos não aparecem
```python
# Para ambiente sem display gráfico
import matplotlib
matplotlib.use('Agg')
```

## 📈 Próximos Passos

### 1. Análise Avançada
- Machine Learning para predições
- Análise de correlações
- Detecção de anomalias

### 2. Automação
- Scripts de coleta automática
- Alertas em tempo real
- Relatórios automáticos

### 3. Dashboard Web
- Interface gráfica
- Visualizações interativas
- Filtros dinâmicos

## 📞 Suporte

### Documentação
- **README.md**: Visão geral completa
- **DOCUMENTACAO_TECNICA.md**: Detalhes técnicos
- **GUIA_USO.md**: Este guia

### Recursos Adicionais
- Código fonte comentado
- Exemplos de uso
- Templates de relatórios

---

**Última atualização**: 2024
**Versão**: 1.0