#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisador BbotFanTan - Sistema de Análise de Resultados de Apostas
Versão: 1.0
Autor: Sistema de Documentação Automática
"""

import re
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict, Counter
import json

class AnalisadorBbotFanTan:
    """
    Classe principal para análise dos dados do sistema BbotFanTan
    """
    
    def __init__(self, arquivo_dados):
        """
        Inicializa o analisador com o arquivo de dados
        
        Args:
            arquivo_dados (str): Caminho para o arquivo de dados
        """
        self.arquivo_dados = arquivo_dados
        self.dados = []
        self.df = None
        self.estatisticas = {}
        
    def processar_dados(self):
        """
        Processa o arquivo de dados e extrai as informações
        """
        print("🔄 Processando dados do arquivo...")
        
        dados_diarios = []
        data_atual = None
        
        with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                
                # Verifica se é um cabeçalho de data
                if 'B Bot Fan Alavancagem' in linha:
                    # Extrai a data do cabeçalho
                    match_data = re.search(r'\[(\d{2}/\d{2}/\d{4})\]', linha)
                    if match_data:
                        data_atual = datetime.strptime(match_data.group(1), '%d/%m/%Y')
                
                # Verifica se é uma linha de aposta
                match_aposta = re.match(r'fantan\s+(\d{2}:\d{2})\s+KWOK\s+(\d/\d)\s+([✅❌])([¹²]?)', linha)
                if match_aposta and data_atual:
                    timestamp, tipo, resultado, modificador = match_aposta.groups()
                    
                    # Combina data e hora
                    hora = datetime.strptime(timestamp, '%H:%M').time()
                    data_hora = datetime.combine(data_atual.date(), hora)
                    
                    dados_diarios.append({
                        'data': data_atual.date(),
                        'hora': timestamp,
                        'data_hora': data_hora,
                        'tipo': tipo,
                        'resultado': resultado,
                        'modificador': modificador if modificador else '',
                        'sucesso': resultado == '✅'
                    })
        
        self.dados = dados_diarios
        self.df = pd.DataFrame(dados_diarios)
        print(f"✅ Processados {len(self.dados)} registros de apostas")
        
    def calcular_estatisticas_gerais(self):
        """
        Calcula estatísticas gerais dos dados
        """
        if self.df is None:
            print("❌ Dados não processados. Execute processar_dados() primeiro.")
            return
        
        print("📊 Calculando estatísticas gerais...")
        
        # Estatísticas básicas
        total_apostas = len(self.df)
        total_vitorias = len(self.df[self.df['sucesso'] == True])
        total_derrotas = len(self.df[self.df['sucesso'] == False])
        assertividade_geral = (total_vitorias / total_apostas) * 100
        
        # Estatísticas por tipo de aposta
        stats_por_tipo = {}
        for tipo in ['1/2', '2/3', '3/4']:
            df_tipo = self.df[self.df['tipo'] == tipo]
            if len(df_tipo) > 0:
                vitorias = len(df_tipo[df_tipo['sucesso'] == True])
                total = len(df_tipo)
                assertividade = (vitorias / total) * 100
                
                stats_por_tipo[tipo] = {
                    'total': total,
                    'vitorias': vitorias,
                    'derrotas': total - vitorias,
                    'assertividade': assertividade,
                    'percentual_total': (total / total_apostas) * 100
                }
        
        # Estatísticas temporais
        self.df['hora_num'] = pd.to_datetime(self.df['hora'], format='%H:%M').dt.hour
        stats_por_hora = {}
        for hora in range(24):
            df_hora = self.df[self.df['hora_num'] == hora]
            if len(df_hora) > 0:
                vitorias = len(df_hora[df_hora['sucesso'] == True])
                total = len(df_hora)
                assertividade = (vitorias / total) * 100
                
                stats_por_hora[hora] = {
                    'total': total,
                    'vitorias': vitorias,
                    'assertividade': assertividade
                }
        
        # Estatísticas diárias
        stats_diarias = self.df.groupby('data').agg({
            'sucesso': ['count', 'sum']
        }).reset_index()
        stats_diarias.columns = ['data', 'total', 'vitorias']
        stats_diarias['assertividade'] = (stats_diarias['vitorias'] / stats_diarias['total']) * 100
        
        self.estatisticas = {
            'geral': {
                'total_apostas': total_apostas,
                'total_vitorias': total_vitorias,
                'total_derrotas': total_derrotas,
                'assertividade': assertividade_geral
            },
            'por_tipo': stats_por_tipo,
            'por_hora': stats_por_hora,
            'diarias': stats_diarias
        }
        
        print("✅ Estatísticas calculadas com sucesso!")
        
    def gerar_relatorio_texto(self):
        """
        Gera um relatório em formato texto
        """
        if not self.estatisticas:
            print("❌ Estatísticas não calculadas. Execute calcular_estatisticas_gerais() primeiro.")
            return
        
        print("\n" + "="*60)
        print("📋 RELATÓRIO BbotFanTan - ANÁLISE COMPLETA")
        print("="*60)
        
        # Estatísticas gerais
        geral = self.estatisticas['geral']
        print(f"\n🎯 ESTATÍSTICAS GERAIS:")
        print(f"   • Total de apostas: {geral['total_apostas']}")
        print(f"   • Vitórias: {geral['total_vitorias']}")
        print(f"   • Derrotas: {geral['total_derrotas']}")
        print(f"   • Assertividade: {geral['assertividade']:.1f}%")
        
        # Estatísticas por tipo
        print(f"\n📊 ESTATÍSTICAS POR TIPO DE APOSTA:")
        for tipo, stats in self.estatisticas['por_tipo'].items():
            print(f"   • {tipo}:")
            print(f"     - Total: {stats['total']} ({stats['percentual_total']:.1f}%)")
            print(f"     - Vitórias: {stats['vitorias']}")
            print(f"     - Assertividade: {stats['assertividade']:.1f}%")
        
        # Melhores horários
        print(f"\n⏰ MELHORES HORÁRIOS (Top 5):")
        horarios_ordenados = sorted(
            self.estatisticas['por_hora'].items(),
            key=lambda x: x[1]['assertividade'],
            reverse=True
        )[:5]
        
        for hora, stats in horarios_ordenados:
            print(f"   • {hora:02d}:00 - {stats['assertividade']:.1f}% ({stats['total']} apostas)")
        
        # Piores horários
        print(f"\n⚠️ PIORES HORÁRIOS (Top 5):")
        horarios_ordenados = sorted(
            self.estatisticas['por_hora'].items(),
            key=lambda x: x[1]['assertividade']
        )[:5]
        
        for hora, stats in horarios_ordenados:
            print(f"   • {hora:02d}:00 - {stats['assertividade']:.1f}% ({stats['total']} apostas)")
        
        # Análise de sequências
        print(f"\n🔄 ANÁLISE DE SEQUÊNCIAS:")
        sequencias = self.analisar_sequencias()
        print(f"   • Maior sequência de vitórias: {sequencias['max_vitorias']}")
        print(f"   • Maior sequência de derrotas: {sequencias['max_derrotas']}")
        print(f"   • Sequência média de vitórias: {sequencias['media_vitorias']:.1f}")
        
        print("\n" + "="*60)
        
    def analisar_sequencias(self):
        """
        Analisa sequências de vitórias e derrotas
        """
        if self.df is None:
            return {}
        
        sequencia_atual = 1
        max_vitorias = 0
        max_derrotas = 0
        sequencias_vitorias = []
        sequencias_derrotas = []
        
        for i in range(1, len(self.df)):
            if self.df.iloc[i]['sucesso'] == self.df.iloc[i-1]['sucesso']:
                sequencia_atual += 1
            else:
                if self.df.iloc[i-1]['sucesso']:
                    max_vitorias = max(max_vitorias, sequencia_atual)
                    sequencias_vitorias.append(sequencia_atual)
                else:
                    max_derrotas = max(max_derrotas, sequencia_atual)
                    sequencias_derrotas.append(sequencia_atual)
                sequencia_atual = 1
        
        # Última sequência
        if self.df.iloc[-1]['sucesso']:
            max_vitorias = max(max_vitorias, sequencia_atual)
            sequencias_vitorias.append(sequencia_atual)
        else:
            max_derrotas = max(max_derrotas, sequencia_atual)
            sequencias_derrotas.append(sequencia_atual)
        
        return {
            'max_vitorias': max_vitorias,
            'max_derrotas': max_derrotas,
            'media_vitorias': np.mean(sequencias_vitorias) if sequencias_vitorias else 0,
            'media_derrotas': np.mean(sequencias_derrotas) if sequencias_derrotas else 0
        }
    
    def gerar_graficos(self, salvar=True):
        """
        Gera gráficos de análise
        """
        if not self.estatisticas:
            print("❌ Estatísticas não calculadas. Execute calcular_estatisticas_gerais() primeiro.")
            return
        
        print("📈 Gerando gráficos...")
        
        # Configuração do estilo
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Análise BbotFanTan - Relatório Visual', fontsize=16, fontweight='bold')
        
        # Gráfico 1: Assertividade por tipo de aposta
        tipos = list(self.estatisticas['por_tipo'].keys())
        assertividades = [self.estatisticas['por_tipo'][tipo]['assertividade'] for tipo in tipos]
        cores = ['#2ecc71', '#f39c12', '#e74c3c']
        
        axes[0, 0].bar(tipos, assertividades, color=cores)
        axes[0, 0].set_title('Assertividade por Tipo de Aposta')
        axes[0, 0].set_ylabel('Assertividade (%)')
        axes[0, 0].set_ylim(0, 100)
        for i, v in enumerate(assertividades):
            axes[0, 0].text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')
        
        # Gráfico 2: Distribuição temporal
        horas = list(self.estatisticas['por_hora'].keys())
        totais = [self.estatisticas['por_hora'][hora]['total'] for hora in horas]
        
        axes[0, 1].plot(horas, totais, marker='o', linewidth=2, markersize=6)
        axes[0, 1].set_title('Distribuição de Apostas por Hora')
        axes[0, 1].set_xlabel('Hora do Dia')
        axes[0, 1].set_ylabel('Número de Apostas')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Gráfico 3: Assertividade diária
        dias = self.estatisticas['diarias']['data'].dt.strftime('%d/%m')
        assertividades_diarias = self.estatisticas['diarias']['assertividade']
        
        axes[1, 0].plot(range(len(dias)), assertividades_diarias, marker='o', linewidth=2)
        axes[1, 0].set_title('Assertividade Diária')
        axes[1, 0].set_xlabel('Dia')
        axes[1, 0].set_ylabel('Assertividade (%)')
        axes[1, 0].set_xticks(range(0, len(dias), 5))
        axes[1, 0].set_xticklabels([dias[i] for i in range(0, len(dias), 5)], rotation=45)
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].axhline(y=80, color='red', linestyle='--', alpha=0.7, label='Meta 80%')
        axes[1, 0].legend()
        
        # Gráfico 4: Heatmap de assertividade por hora
        horas_heatmap = []
        dias_heatmap = []
        valores_heatmap = []
        
        for hora in range(24):
            if hora in self.estatisticas['por_hora']:
                for dia in self.df['data'].unique():
                    df_filtro = self.df[(self.df['hora_num'] == hora) & (self.df['data'] == dia)]
                    if len(df_filtro) > 0:
                        assertividade = (len(df_filtro[df_filtro['sucesso'] == True]) / len(df_filtro)) * 100
                        horas_heatmap.append(hora)
                        dias_heatmap.append(dia.strftime('%d/%m'))
                        valores_heatmap.append(assertividade)
        
        # Criar matriz para heatmap
        matriz_heatmap = np.zeros((24, len(self.df['data'].unique())))
        for i, (hora, dia, valor) in enumerate(zip(horas_heatmap, dias_heatmap, valores_heatmap)):
            dia_idx = list(self.df['data'].unique()).index(pd.to_datetime(dia, format='%d/%m').date())
            matriz_heatmap[hora, dia_idx] = valor
        
        im = axes[1, 1].imshow(matriz_heatmap, cmap='RdYlGn', aspect='auto')
        axes[1, 1].set_title('Heatmap: Assertividade por Hora e Dia')
        axes[1, 1].set_xlabel('Dia')
        axes[1, 1].set_ylabel('Hora')
        axes[1, 1].set_yticks(range(0, 24, 4))
        axes[1, 1].set_yticklabels([f'{h:02d}:00' for h in range(0, 24, 4)])
        
        # Adicionar barra de cores
        cbar = plt.colorbar(im, ax=axes[1, 1])
        cbar.set_label('Assertividade (%)')
        
        plt.tight_layout()
        
        if salvar:
            plt.savefig('analise_bbotfantan.png', dpi=300, bbox_inches='tight')
            print("✅ Gráficos salvos como 'analise_bbotfantan.png'")
        
        plt.show()
    
    def exportar_dados(self, formato='json'):
        """
        Exporta os dados processados
        """
        if not self.estatisticas:
            print("❌ Estatísticas não calculadas.")
            return
        
        if formato == 'json':
            with open('estatisticas_bbotfantan.json', 'w', encoding='utf-8') as f:
                # Converter datetime para string para JSON
                stats_export = self.estatisticas.copy()
                stats_export['diarias']['data'] = stats_export['diarias']['data'].dt.strftime('%Y-%m-%d').tolist()
                json.dump(stats_export, f, indent=2, ensure_ascii=False)
            print("✅ Dados exportados como 'estatisticas_bbotfantan.json'")
        
        elif formato == 'csv':
            self.df.to_csv('dados_bbotfantan.csv', index=False, encoding='utf-8')
            print("✅ Dados exportados como 'dados_bbotfantan.csv'")
    
    def gerar_recomendacoes(self):
        """
        Gera recomendações baseadas na análise
        """
        if not self.estatisticas:
            print("❌ Estatísticas não calculadas.")
            return
        
        print("\n💡 RECOMENDAÇÕES BASEADAS NA ANÁLISE:")
        print("="*50)
        
        # Melhor tipo de aposta
        melhor_tipo = max(self.estatisticas['por_tipo'].items(), 
                         key=lambda x: x[1]['assertividade'])
        print(f"🎯 Melhor tipo de aposta: {melhor_tipo[0]} ({melhor_tipo[1]['assertividade']:.1f}% assertividade)")
        
        # Melhores horários
        melhores_horarios = sorted(
            self.estatisticas['por_hora'].items(),
            key=lambda x: x[1]['assertividade'],
            reverse=True
        )[:3]
        
        print("⏰ Melhores horários para apostar:")
        for hora, stats in melhores_horarios:
            print(f"   • {hora:02d}:00 - {stats['assertividade']:.1f}% assertividade")
        
        # Horários a evitar
        piores_horarios = sorted(
            self.estatisticas['por_hora'].items(),
            key=lambda x: x[1]['assertividade']
        )[:3]
        
        print("⚠️ Horários a evitar:")
        for hora, stats in piores_horarios:
            print(f"   • {hora:02d}:00 - {stats['assertividade']:.1f}% assertividade")
        
        # Recomendações gerais
        print("\n📋 Recomendações gerais:")
        print("   • Mantenha foco na estratégia KWOK")
        print("   • Monitore padrões de sequências")
        print("   • Ajuste horários conforme análise")
        print("   • Mantenha gestão de risco")
        print("   • Analise dados regularmente")

def main():
    """
    Função principal para executar a análise
    """
    print("🚀 Iniciando Análise BbotFanTan")
    print("="*40)
    
    # Inicializar analisador
    analisador = AnalisadorBbotFanTan('31 dias')
    
    # Processar dados
    analisador.processar_dados()
    
    # Calcular estatísticas
    analisador.calcular_estatisticas_gerais()
    
    # Gerar relatório
    analisador.gerar_relatorio_texto()
    
    # Gerar recomendações
    analisador.gerar_recomendacoes()
    
    # Gerar gráficos
    analisador.gerar_graficos()
    
    # Exportar dados
    analisador.exportar_dados('json')
    analisador.exportar_dados('csv')
    
    print("\n✅ Análise concluída com sucesso!")

if __name__ == "__main__":
    main()