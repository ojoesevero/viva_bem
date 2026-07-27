import time
import threading
import pygetwindow as gw
from plyer import notification
from datetime import datetime, timedelta
import pystray
from PIL import Image, ImageDraw
import ctypes

# --- Configurações Baseadas em Saúde ---
INTERVALO_AGUA = 60 * 45     # 45 min (Ideal: 30 a 60 min)
INTERVALO_MOVIMENTO = 60 * 40  # 40 min (Ideal: 30 a 50 min)

class HealthMonitor:
    def __init__(self):
        self.rodando = True
        self.tempo_inicio = time.time()
        self.ultimo_aviso_agua = self.tempo_inicio
        self.ultimo_aviso_movimento = self.tempo_inicio
        self.icone = None # Referência para o ícone do sistema

    def obter_janela_ativa(self):
        try:
            janela = gw.getActiveWindow()
            return janela.title if janela else "Desconhecida/Fundo"
        except Exception:
            return "Erro ao ler janela"

    def verificar_bloqueio_windows(self):
        # Chama a API nativa do Windows para verificar a janela em primeiro plano.
        # Se for 0, geralmente indica que a estação de trabalho está bloqueada.
        return ctypes.windll.user32.GetForegroundWindow() == 0

    def contar_aplicacoes_abertas(self):
        try:
            # Lista todas as janelas que possuem um título válido
            janelas = [j for j in gw.getAllWindows() if j.title.strip()]
            return len(janelas)
        except:
            return 0

    def enviar_alerta(self, titulo, mensagem):
        notification.notify(
            title=titulo,
            message=mensagem,
            app_name='Viva Bem',
            timeout=10
        )

    def mostrar_resumo(self):
        tempo_sessao = str(timedelta(seconds=int(time.time() - self.tempo_inicio)))
        hora_agua = datetime.fromtimestamp(self.ultimo_aviso_agua).strftime('%H:%M')
        qtd_apps = self.contar_aplicacoes_abertas()
        
        mensagem = (f"Tempo de sessão: {tempo_sessao}\n"
                    f"Última água: {hora_agua}\n"
                    f"Aplicações abertas: {qtd_apps}")
        self.enviar_alerta("📊 Resumo de Produtividade", mensagem)

    def loop_monitoramento(self):
        while self.rodando:
            tempo_atual = time.time()
            
            # --- Lógica de Detecção de Pausa ---
            if self.verificar_bloqueio_windows():
                # O PC está bloqueado. Assumimos que você levantou.
                # Atualiza o timer para não apitar logo que você voltar.
                self.ultimo_aviso_movimento = tempo_atual
            else:
                # O PC está em uso. Registra a atividade no log.
                janela_atual = self.obter_janela_ativa()
                if janela_atual != "Desconhecida/Fundo":
                    hora_atual_str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                    with open("log_atividades.txt", "a", encoding="utf-8") as arquivo:
                        arquivo.write(f"[{hora_atual_str}] {janela_atual}\n")

            # --- Notificação de Água ---
            if tempo_atual - self.ultimo_aviso_agua >= INTERVALO_AGUA:
                self.enviar_alerta("Hora da Água! 💧", "Beba em pequenos goles. Manter o hábito constante não sobrecarrega o organismo.")
                self.ultimo_aviso_agua = tempo_atual

            # --- Notificação de Movimento ---
            if tempo_atual - self.ultimo_aviso_movimento >= INTERVALO_MOVIMENTO:
                self.enviar_alerta("Hora do café! ☕", "Levante-se e movimente-se por 1 a 3 minutos para prevenir fadiga e problemas circulatórios.")
                self.ultimo_aviso_movimento = tempo_atual

            # --- Atualiza o Texto do Ícone (Hover) ---
            if self.icone:
                tempo_sessao = str(timedelta(seconds=int(tempo_atual - self.tempo_inicio)))
                hora_agua = datetime.fromtimestamp(self.ultimo_aviso_agua).strftime('%H:%M')
                qtd_apps = self.contar_aplicacoes_abertas()
                self.icone.title = f"Sessão: {tempo_sessao}\nÁgua: {hora_agua}\nApps: {qtd_apps}"

            # Dorme por 60 segundos antes da próxima checagem
            time.sleep(60)

    def parar(self):
        self.rodando = False

# --- Funções do System Tray ---
def criar_icone():
    imagem = Image.new('RGB', (64, 64), color=(0, 120, 215))
    desenho = ImageDraw.Draw(imagem)
    desenho.ellipse((16, 16, 48, 48), fill=(255, 255, 255))
    return imagem

def sair_app(icon, item):
    monitor.parar()
    icon.stop()

def acao_resumo(icon, item):
    monitor.mostrar_resumo()

if __name__ == "__main__":
    monitor = HealthMonitor()
    
    # Inicia o monitoramento em segundo plano
    thread_monitor = threading.Thread(target=monitor.loop_monitoramento)
    thread_monitor.start()

    # Cria o menu com a nova opção de Resumo
    menu = pystray.Menu(
        pystray.MenuItem('📊 Ver Resumo', acao_resumo),
        pystray.MenuItem('❌ Sair', sair_app)
    )
    
    # Configura o ícone na bandeja do sistema
    icone_tray = pystray.Icon("VivaBem", criar_icone(), "Calculando resumo...", menu)
    monitor.icone = icone_tray # Passa a referência para atualizar o texto do hover
    
    monitor.enviar_alerta("Monitor Iniciado", "Regra dos 50 min e hidratação ativados. Bom trabalho!")
    
    icone_tray.run()