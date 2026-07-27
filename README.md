# Viva Bem - Health Monitor

O **Viva Bem** é um script utilitário desenhado para rodar silenciosamente em segundo plano, monitorando as sessões de uso do computador para enviar alertas estruturados focados no bem-estar físico e na prevenção de doenças ocupacionais[cite: 9].

## 🚀 Funcionalidades
* **Gerenciamento de Hidratação:** Dispara alertas intervalados (45 min) para promover a ingestão de água constante, recomendada por profissionais de saúde para não sobrecarregar os rins[cite: 9].
* **Prevenção Circulatória e Fadiga Visual:** Emite notificações a cada 40 min para que o usuário levante-se e caminhe, reduzindo os riscos de trombose e síndrome da visão de computador[cite: 9].
* **Detecção Inteligente de Pausa:** Identifica automaticamente quando a estação de trabalho está bloqueada (Tela de Bloqueio do Windows) e recalcula os cronômetros, evitando alertas falsos assim que o usuário retornar à máquina[cite: 9].
* **Log de Atividades:** Monitora e registra discretamente as janelas ativas em um arquivo `.txt`, permitindo auditorias de produtividade e análise de tempo de foco[cite: 9].
* **System Tray Integrado:** Roda de forma oculta e acessível via ícone na bandeja do sistema[cite: 9]. Oferece um menu interativo para visualizar resumos em tempo real (tempo de sessão, horário do último alerta e total de aplicações abertas)[cite: 9].

## 🛠 Tecnologias Utilizadas
* Python 3.x[cite: 9]
* PyGetWindow[cite: 9]
* Plyer[cite: 9]
* PyStray[cite: 9]
* Pillow[cite: 9]

## ⚙️ Instalação e Execução
\`\`\`bash
pip install -r requirements.txt
python monitor_saude.pyw
\`\`\`

O uso da extensão `.pyw` impede a abertura da janela do console (CMD) no Windows, garantindo que o monitor rode silenciosamente em background[cite: 9].
