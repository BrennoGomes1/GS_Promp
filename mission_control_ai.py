"""
MISSION CONTROL AI — FIAP GLOBAL SOLUTION 2026.1

IA: Llama 3.2 1B via Ollama (sem conta, sem chave de API)
Recomendado rodar no Google Colab — veja o notebook .ipynb

COMO USAR LOCALMENTE:
  1. Instale o Ollama: https://ollama.com
  2. No terminal: ollama pull llama3.2:1b
  3. pip install ollama
  4. python mission_control_ai.py
"""

import ollama
import subprocess
import time
import random
from datetime import datetime


# INICIAR SERVIDOR OLLAMA 

def iniciar_ollama():
    try:
        ollama.list()
        print("✅ Ollama já está rodando!")
    except Exception:
        print("⏳ Iniciando servidor Ollama...")
        subprocess.Popen(["ollama", "serve"])
        time.sleep(3)
        print("✅ Servidor Ollama iniciado!")


# CONSTANTES

MODULOS = ["Módulo Alpha", "Módulo Beta", "Módulo Gamma"]
STATUS_MODULO = ["operacional", "operacional", "operacional", "degradado", "falha crítica"]

RESPOSTAS_AUTOMATICAS = {
    "energia_critica":     "⚡ MODO ECONOMIA ATIVADO: Sistemas não essenciais desligados. Priorizando suporte à vida e comunicação.",
    "temperatura_critica": "🌡️ RESFRIAMENTO EMERGENCIAL: Ventilação máxima ativada. Suspensão de operações de alta carga.",
    "comunicacao_perdida": "📡 PROTOCOLO BEACON: Tentando reconexão via antena reserva. Transmitindo sinal de emergência.",
    "pressao_critica":     "💨 ALERTA DE PRESSÃO: Verificando integridade do casco. Selando compartimentos secundários.",
    "radiacao_critica":    "☢️ RADIAÇÃO ELEVADA: Ativando blindagem adicional. Movendo tripulação para módulo protegido.",
    "modulo_falha":        "🔧 FALHA DE MÓDULO: Ativando sistemas redundantes. Iniciando diagnóstico automático.",
}

SYSTEM_PROMPT = """Você é ARIA (Artificial Response Intelligence for Aerospace),
o sistema de inteligência artificial de controle de missão espacial da FIAP Mission Control.

Sua função é analisar os dados operacionais em tempo real da missão e fornecer:
1. Avaliação rápida do estado geral da missão
2. Identificação dos riscos mais críticos
3. Recomendações técnicas prioritárias para a equipe
4. Previsão do próximo estado se nenhuma ação for tomada

Regras:
- Seja direto e técnico, como um verdadeiro sistema de controle de missão
- Priorize vida da tripulação acima de tudo
- Limite sua resposta a 4-5 frases objetivas
- Use linguagem de engenharia aeroespacial
- Responda sempre em português"""



# GERAÇÃO DE DADOS SIMULADOS

def gerar_dados_missao(cenario="normal"):
    """
    Gera dados simulados da missão espacial.
    cenario: 'normal' | 'alerta' | 'critico'
    """
    if cenario == "normal":
        temperatura   = round(random.uniform(18.0, 45.0), 1)
        energia       = random.randint(55, 100)
        comunicacao   = random.choices(["estável", "intermitente"], weights=[85, 15])[0]
        geracao_solar = round(random.uniform(70.0, 100.0), 1)
        pressao       = round(random.uniform(99.5, 101.5), 2)
        radiacao      = round(random.uniform(0.1, 0.5), 2)
        pesos_mod     = [70, 20, 10, 0, 0]

    elif cenario == "alerta":
        temperatura   = round(random.uniform(68.0, 84.9), 1)
        energia       = random.randint(21, 39)
        comunicacao   = random.choices(["intermitente", "instável"], weights=[60, 40])[0]
        geracao_solar = round(random.uniform(30.0, 55.0), 1)
        pressao       = round(random.uniform(95.0, 99.4), 2)
        radiacao      = round(random.uniform(1.5, 3.0), 2)
        pesos_mod     = [40, 30, 20, 10, 0]

    elif cenario == "critico":
        temperatura   = round(random.uniform(85.0, 120.0), 1)
        energia       = random.randint(5, 20)
        comunicacao   = random.choices(["instável", "sem sinal"], weights=[50, 50])[0]
        geracao_solar = round(random.uniform(0.0, 25.0), 1)
        pressao       = round(random.uniform(88.0, 94.9), 2)
        radiacao      = round(random.uniform(3.5, 8.0), 2)
        pesos_mod     = [10, 15, 20, 25, 30]

    else:
        raise ValueError(f"Cenário inválido: {cenario}")

    modulos = {nome: random.choices(STATUS_MODULO, weights=pesos_mod)[0] for nome in MODULOS}

    return {
        "timestamp":       datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperatura":     temperatura,
        "energia_bateria": energia,
        "geracao_solar":   geracao_solar,
        "comunicacao":     comunicacao,
        "pressao_cabine":  pressao,
        "nivel_radiacao":  radiacao,
        "modulos":         modulos,
    }



# FUNÇÕES DE AVALIAÇÃO

def avaliar_temperatura(v):
    if v >= 85:  return "critico"
    if v >= 65:  return "alerta"
    return "normal"

def avaliar_energia(v):
    if v < 20:   return "critico"
    if v < 40:   return "alerta"
    return "normal"

def avaliar_pressao(v):
    if v < 94:   return "critico"
    if v < 99:   return "alerta"
    return "normal"

def avaliar_radiacao(v):
    if v >= 3.5: return "critico"
    if v >= 1.5: return "alerta"
    return "normal"



# MOTOR DE DECISÃO E ALERTAS

def gerar_alertas_e_acoes(dados):
    alertas = []
    acoes   = []
    nivel_geral = "NOMINAL"

    def escalar(nivel):
        nonlocal nivel_geral
        if nivel == "critico":
            nivel_geral = "CRÍTICO"
        elif nivel == "alerta" and nivel_geral == "NOMINAL":
            nivel_geral = "ALERTA"

    # Temperatura
    nv = avaliar_temperatura(dados["temperatura"])
    escalar(nv)
    if nv == "critico":
        alertas.append(f"🔴 CRÍTICO: Temperatura {dados['temperatura']}°C (limite: 85°C)")
        acoes.append(RESPOSTAS_AUTOMATICAS["temperatura_critica"])
    elif nv == "alerta":
        alertas.append(f"🟡 ALERTA: Temperatura {dados['temperatura']}°C (limite: 65°C)")

    # Energia
    nv = avaliar_energia(dados["energia_bateria"])
    escalar(nv)
    if nv == "critico":
        alertas.append(f"🔴 CRÍTICO: Bateria em {dados['energia_bateria']}% (limite: 20%)")
        acoes.append(RESPOSTAS_AUTOMATICAS["energia_critica"])
    elif nv == "alerta":
        alertas.append(f"🟡 ALERTA: Bateria em {dados['energia_bateria']}% (limite: 40%)")

    # Comunicação
    if dados["comunicacao"] == "sem sinal":
        escalar("critico")
        alertas.append("🔴 CRÍTICO: Comunicação perdida — sem sinal")
        acoes.append(RESPOSTAS_AUTOMATICAS["comunicacao_perdida"])
    elif dados["comunicacao"] == "instável":
        escalar("alerta")
        alertas.append("🟡 ALERTA: Comunicação instável")

    # Pressão
    nv = avaliar_pressao(dados["pressao_cabine"])
    escalar(nv)
    if nv == "critico":
        alertas.append(f"🔴 CRÍTICO: Pressão da cabine em {dados['pressao_cabine']} kPa")
        acoes.append(RESPOSTAS_AUTOMATICAS["pressao_critica"])
    elif nv == "alerta":
        alertas.append(f"🟡 ALERTA: Pressão da cabine em {dados['pressao_cabine']} kPa")

    # Radiação
    nv = avaliar_radiacao(dados["nivel_radiacao"])
    escalar(nv)
    if nv == "critico":
        alertas.append(f"🔴 CRÍTICO: Radiação em {dados['nivel_radiacao']} mSv/h")
        acoes.append(RESPOSTAS_AUTOMATICAS["radiacao_critica"])
    elif nv == "alerta":
        alertas.append(f"🟡 ALERTA: Radiação em {dados['nivel_radiacao']} mSv/h")

    # Módulos
    for modulo, status in dados["modulos"].items():
        if status == "falha crítica":
            escalar("critico")
            alertas.append(f"🔴 CRÍTICO: {modulo} — FALHA CRÍTICA")
            acoes.append(RESPOSTAS_AUTOMATICAS["modulo_falha"])
        elif status == "degradado":
            escalar("alerta")
            alertas.append(f"🟡 ALERTA: {modulo} operando em modo degradado")

    if not alertas:
        alertas.append("🟢 Todos os parâmetros dentro dos limites operacionais.")

    return alertas, acoes, nivel_geral



# IA GENERATIVA — LLAMA VIA OLLAMA

def consultar_ia(dados, alertas, nivel_geral):
    """Envia telemetria para o Llama 3.2 1B via Ollama e retorna análise da ARIA."""
    alertas_texto = "\n".join(alertas)

    prompt = f"""RELATÓRIO DE TELEMETRIA — {dados['timestamp']}
Status Geral: {nivel_geral}

PARÂMETROS:
- Temperatura: {dados['temperatura']}°C
- Bateria: {dados['energia_bateria']}%
- Geração Solar: {dados['geracao_solar']}%
- Comunicação: {dados['comunicacao']}
- Pressão da Cabine: {dados['pressao_cabine']} kPa
- Nível de Radiação: {dados['nivel_radiacao']} mSv/h

MÓDULOS:
{chr(10).join([f'- {m}: {s}' for m, s in dados['modulos'].items()])}

ALERTAS DETECTADOS:
{alertas_texto}

Analise a situação e forneça sua avaliação técnica."""

    try:
        resposta = ollama.chat(
            model="llama3.2:1b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt}
            ]
        )
        return resposta["message"]["content"]
    except Exception as e:
        return f"[ERRO DE COMUNICAÇÃO COM ARIA: {e}]"



# EXIBIÇÃO DO PAINEL

def barra_progresso(valor, maximo=100, tamanho=20, invertido=False):
    pct = min(valor / maximo, 1.0)
    preenchido = int(pct * tamanho)
    barra = "█" * preenchido + "░" * (tamanho - preenchido)
    if invertido:
        icone = "🔴" if pct > 0.85 else "🟡" if pct > 0.65 else "🟢"
    else:
        icone = "🔴" if pct < 0.20 else "🟡" if pct < 0.40 else "🟢"
    return f"{icone} [{barra}] {valor:.1f}"

def exibir_painel(dados, alertas, acoes, nivel_geral, analise_ia):
    W          = 60
    linha      = "═" * W
    linha_fina = "─" * W
    cor_nivel  = {"NOMINAL": "🟢", "ALERTA": "🟡", "CRÍTICO": "🔴"}
    com_icons  = {"estável": "🟢", "intermitente": "🟡", "instável": "🔴", "sem sinal": "🔴"}
    mod_icons  = {"operacional": "🟢", "degradado": "🟡", "falha crítica": "🔴"}

    print()
    print(linha)
    print("  🚀  MISSION CONTROL AI — FIAP GLOBAL SOLUTION 2026.1")
    print(linha)
    print(f"  📅 Timestamp : {dados['timestamp']}")
    print(f"  🛰️  Status    : {cor_nivel[nivel_geral]} {nivel_geral}")
    print(linha_fina)

    print("\n  📊 PARÂMETROS OPERACIONAIS")
    print(linha_fina)
    print(f"  🌡️  Temperatura    : {barra_progresso(dados['temperatura'], 120, invertido=True)} °C")
    print(f"  ⚡  Bateria        : {barra_progresso(dados['energia_bateria'], 100)} %")
    print(f"  ☀️   Geração Solar  : {barra_progresso(dados['geracao_solar'], 100)} %")
    print(f"  📡  Comunicação   : {com_icons.get(dados['comunicacao'], '⚪')} {dados['comunicacao'].upper()}")

    p_icon = "🔴" if avaliar_pressao(dados['pressao_cabine']) == "critico" else \
             "🟡" if avaliar_pressao(dados['pressao_cabine']) == "alerta"  else "🟢"
    print(f"  💨  Pressão Cabine: {p_icon} {dados['pressao_cabine']} kPa")

    r_icon = "🔴" if avaliar_radiacao(dados['nivel_radiacao']) == "critico" else \
             "🟡" if avaliar_radiacao(dados['nivel_radiacao']) == "alerta"  else "🟢"
    print(f"  ☢️   Radiação      : {r_icon} {dados['nivel_radiacao']} mSv/h")

    print("\n  🔧 STATUS DOS MÓDULOS")
    print(linha_fina)
    for modulo, status in dados["modulos"].items():
        print(f"  {mod_icons.get(status, '⚪')}  {modulo:<15} : {status.upper()}")

    print("\n  ⚠️  ALERTAS ATIVOS")
    print(linha_fina)
    for alerta in alertas:
        print(f"  {alerta}")

    if acoes:
        print("\n  🤖 RESPOSTAS AUTOMÁTICAS ATIVADAS")
        print(linha_fina)
        for acao in acoes:
            print(f"  {acao}")

    print("\n  🧠 ANÁLISE DA IA — ARIA (Llama 3.2 via Ollama)")
    print(linha_fina)
    palavras    = analise_ia.split()
    linha_atual = "  "
    for palavra in palavras:
        if len(linha_atual) + len(palavra) + 1 > 57:
            print(linha_atual)
            linha_atual = "  " + palavra
        else:
            linha_atual += (" " if linha_atual != "  " else "") + palavra
    if linha_atual.strip():
        print(linha_atual)

    print()
    print(linha)
    print()



# EXECUÇÃO PRINCIPAL

def executar_cenario(cenario):
    print(f"\n{'─'*60}")
    print(f"  🛰️  Gerando telemetria — Cenário: {cenario.upper()}")
    print(f"{'─'*60}")
    dados = gerar_dados_missao(cenario)
    alertas, acoes, nivel_geral = gerar_alertas_e_acoes(dados)
    print("  🧠 Consultando ARIA (IA)...")
    analise_ia = consultar_ia(dados, alertas, nivel_geral)
    exibir_painel(dados, alertas, acoes, nivel_geral, analise_ia)

if __name__ == "__main__":
    print("\n" + "═" * 60)
    print("  🚀  MISSION CONTROL AI — INICIANDO SISTEMA")
    print("  🤖  IA: Llama 3.2 1B via Ollama")
    print("═" * 60)

    iniciar_ollama()

    for cenario in ["normal", "alerta", "critico"]:
        executar_cenario(cenario)
        if cenario != "critico":
            print("  ⏳ Aguardando próximo ciclo...\n")
            time.sleep(2)

    print("✅ Simulação completa. Sistema ARIA encerrado.")
