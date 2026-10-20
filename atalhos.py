import os
import json
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
import pyperclip

# Caminho absoluto para o arquivo de atalhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_JSON = os.path.join(BASE_DIR, "atalhos.json")

# Dicionário de atalhos em memória e controle de concorrência
atalhos = {}
atalhos_lock = threading.Lock()
monitor_ativo = True


def carregar_atalhos():
    """Carrega os atalhos a partir do arquivo JSON."""
    global atalhos
    if not os.path.exists(ARQUIVO_JSON):
        # Se o arquivo não existir, cria um arquivo padrão vazio
        salvar_atalhos({})
        return {}

    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            dados = json.load(f)
            if isinstance(dados, dict):
                return dados
            return {}
    except Exception as e:
        print(f"Erro ao carregar {ARQUIVO_JSON}: {e}")
        return {}


def salvar_atalhos(dados):
    """Salva os atalhos fornecidos no arquivo JSON."""
    try:
        with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Erro ao salvar {ARQUIVO_JSON}: {e}")
        return False


def monitorar():
    """
    Monitora continuamente as teclas digitadas em segundo plano.
    Identifica o acionamento de gatilhos cadastrados, apaga o texto do gatilho
    e cola a mensagem correspondente na tela usando a área de transferência.
    """
    buffer = ""

    while True:
        try:
            evento = keyboard.read_event()

            if not monitor_ativo:
                time.sleep(0.05)
                continue

            if evento.event_type == keyboard.KEY_DOWN:
                tecla = evento.name

                if tecla in ["space", "enter", "tab"]:
                    buffer = ""
                    continue

                if tecla == "backspace":
                    buffer = buffer[:-1]
                    continue

                if len(tecla) == 1:
                    buffer += tecla

                # Faz uma cópia rápida das chaves e valores para leitura segura
                with atalhos_lock:
                    itens = list(atalhos.items())

                for gatilho, texto in itens:
                    if buffer.endswith(gatilho):
                        # Apaga os caracteres do gatilho digitado
                        for _ in gatilho:
                            keyboard.press_and_release("backspace")
                            time.sleep(0.01)

                        # Copia a mensagem e cola na posição atual
                        pyperclip.copy(texto)
                        keyboard.press_and_release("ctrl+v")

                        buffer = ""
                        break
        except Exception as e:
            # Em caso de erro temporário no hook de teclado, aguarda e continua
            time.sleep(0.1)


class InterfaceAtalhos(tk.Tk):
    """Interface gráfica para gerenciamento e cadastro de atalhos."""

    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Atalhos de Teclado")
        self.geometry("820x620")
        self.minsize(700, 500)

        # Configurar estilos ttk
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        self._criar_layout()
        self._atualizar_tabela()

    def _criar_layout(self):
        # Cabeçalho / Barra Superior
        top_frame = ttk.Frame(self, padding=(12, 10))
        top_frame.pack(fill=tk.X)

        self.lbl_status = ttk.Label(
            top_frame,
            text="🟢 Monitor ativo: Digite qualquer atalho cadastrado para usá-lo",
            font=("Segoe UI", 10, "bold"),
            foreground="#2e7d32",
        )
        self.lbl_status.pack(side=tk.LEFT)

        self.btn_toggle_monitor = ttk.Button(
            top_frame,
            text="Pausar Monitor",
            command=self._alternar_monitor,
        )
        self.btn_toggle_monitor.pack(side=tk.RIGHT, padx=4)

        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=2)

        # Painel Principal Dividido em Esquerda (Tabela/Busca) e Direita (Formulário)
        main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- LADO ESQUERDO: Lista de Atalhos e Pesquisa ---
        frame_esquerda = ttk.Frame(main_paned, padding=5)
        main_paned.add(frame_esquerda, weight=3)

        # Barra de Pesquisa
        frame_busca = ttk.Frame(frame_esquerda)
        frame_busca.pack(fill=tk.X, pady=(0, 6))

        ttk.Label(frame_busca, text="Buscar:").pack(side=tk.LEFT, padx=(0, 5))
        self.var_busca = tk.StringVar()
        self.var_busca.trace_add("write", lambda *args: self._filtrar_tabela())
        entry_busca = ttk.Entry(frame_busca, textvariable=self.var_busca)
        entry_busca.pack(side=tk.LEFT, fill=tk.X, expand=True)

        btn_limpar_busca = ttk.Button(
            frame_busca, text="✕", width=3, command=lambda: self.var_busca.set("")
        )
        btn_limpar_busca.pack(side=tk.RIGHT, padx=(5, 0))

        # Tabela (Treeview)
        colunas = ("gatilho", "previa")
        self.tabela = ttk.Treeview(
            frame_esquerda, columns=colunas, show="headings", selectmode="browse"
        )
        self.tabela.heading("gatilho", text="Gatilho")
        self.tabela.heading("previa", text="Mensagem / Texto")
        self.tabela.column("gatilho", width=120, minwidth=80, anchor=tk.W)
        self.tabela.column("previa", width=260, minwidth=150, anchor=tk.W)

        scroll_y = ttk.Scrollbar(frame_esquerda, orient=tk.VERTICAL, command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scroll_y.set)

        self.tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.tabela.bind("<<TreeviewSelect>>", self._ao_selecionar_atalho)

        # --- LADO DIREITO: Cadastro / Edição e Remoção ---
        frame_direita = ttk.LabelFrame(main_paned, text=" Cadastro e Edição ", padding=10)
        main_paned.add(frame_direita, weight=4)

        # Campo Gatilho
        lbl_gatilho = ttk.Label(
            frame_direita, text="Gatilho (ex: .chamado, .email):", font=("Segoe UI", 9, "bold")
        )
        lbl_gatilho.pack(anchor=tk.W, pady=(0, 2))

        self.var_gatilho = tk.StringVar()
        self.entry_gatilho = ttk.Entry(frame_direita, textvariable=self.var_gatilho, font=("Segoe UI", 10))
        self.entry_gatilho.pack(fill=tk.X, pady=(0, 10))

        # Campo Mensagem
        lbl_texto = ttk.Label(
            frame_direita, text="Texto a ser colado:", font=("Segoe UI", 9, "bold")
        )
        lbl_texto.pack(anchor=tk.W, pady=(0, 2))

        frame_txt = ttk.Frame(frame_direita)
        frame_txt.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.txt_conteudo = tk.Text(
            frame_txt,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            height=12,
            undo=True,
        )
        scroll_txt = ttk.Scrollbar(frame_txt, orient=tk.VERTICAL, command=self.txt_conteudo.yview)
        self.txt_conteudo.configure(yscrollcommand=scroll_txt.set)

        self.txt_conteudo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_txt.pack(side=tk.RIGHT, fill=tk.Y)

        # Botões de Ação
        frame_botoes = ttk.Frame(frame_direita)
        frame_botoes.pack(fill=tk.X, pady=(0, 5))

        self.btn_salvar = ttk.Button(
            frame_botoes, text="💾 Salvar Atalho", command=self._salvar_atalho
        )
        self.btn_salvar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        self.btn_limpar = ttk.Button(
            frame_botoes, text="Limpar Campos", command=self._limpar_campos
        )
        self.btn_limpar.pack(side=tk.LEFT, padx=(0, 4))

        self.btn_excluir = ttk.Button(
            frame_botoes, text="🗑️ Excluir Selecionado", command=self._excluir_atalho
        )
        self.btn_excluir.pack(side=tk.RIGHT)

        # Rodapé com contador
        self.lbl_rodape = ttk.Label(
            self,
            text="",
            font=("Segoe UI", 9),
            foreground="#666666",
            padding=(10, 4),
        )
        self.lbl_rodape.pack(side=tk.BOTTOM, anchor=tk.W)

    def _alternar_monitor(self):
        """Pausa ou retoma a captura de teclas do monitor."""
        global monitor_ativo
        monitor_ativo = not monitor_ativo

        if monitor_ativo:
            self.lbl_status.config(
                text="🟢 Monitor ativo: Digite qualquer atalho cadastrado para usá-lo",
                foreground="#2e7d32",
            )
            self.btn_toggle_monitor.config(text="Pausar Monitor")
        else:
            self.lbl_status.config(
                text="🟡 Monitor pausado: Nenhum atalho será disparado no momento",
                foreground="#e65100",
            )
            self.btn_toggle_monitor.config(text="Retomar Monitor")

    def _atualizar_tabela(self):
        """Atualiza os itens exibidos na Treeview."""
        self._filtrar_tabela()

    def _filtrar_tabela(self):
        """Filtra os atalhos de acordo com a busca informada."""
        termo = self.var_busca.get().strip().lower()

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        with atalhos_lock:
            itens = sorted(atalhos.items(), key=lambda x: x[0].lower())

        total = 0
        for gatilho, texto in itens:
            texto_previa = " ".join(texto.split())  # remove quebras para visualização limpa
            if termo in gatilho.lower() or termo in texto.lower():
                self.tabela.insert("", tk.END, values=(gatilho, texto_previa))
                total += 1

        self.lbl_rodape.config(
            text=f"Total de atalhos: {len(itens)} | Exibindo: {total} | Arquivo: atalhos.json"
        )

    def _ao_selecionar_atalho(self, event):
        """Carrega o atalho selecionado para os campos de edição."""
        selecionado = self.tabela.selection()
        if not selecionado:
            return

        item = self.tabela.item(selecionado[0])
        gatilho = item["values"][0]

        with atalhos_lock:
            texto = atalhos.get(gatilho, "")

        self.var_gatilho.set(gatilho)
        self.txt_conteudo.delete("1.0", tk.END)
        self.txt_conteudo.insert("1.0", texto)

    def _limpar_campos(self):
        """Limpa as caixas de entrada de gatilho e texto."""
        self.var_gatilho.set("")
        self.txt_conteudo.delete("1.0", tk.END)
        if self.tabela.selection():
            self.tabela.selection_remove(self.tabela.selection())

    def _salvar_atalho(self):
        """Cadastra ou atualiza o atalho e salva no JSON."""
        gatilho = self.var_gatilho.get().strip()
        texto = self.txt_conteudo.get("1.0", tk.END).rstrip("\r\n")

        if not gatilho:
            messagebox.showwarning("Atenção", "Por favor, informe o gatilho do atalho (ex: .chamado).")
            self.entry_gatilho.focus_set()
            return

        if not texto:
            messagebox.showwarning("Atenção", "Por favor, informe o texto a ser gerado para o atalho.")
            self.txt_conteudo.focus_set()
            return

        with atalhos_lock:
            atalhos[gatilho] = texto
            sucesso = salvar_atalhos(atalhos)

        if sucesso:
            self._atualizar_tabela()
            # Seleciona o item salvo na tabela
            for item in self.tabela.get_children():
                if self.tabela.item(item)["values"][0] == gatilho:
                    self.tabela.selection_set(item)
                    self.tabela.see(item)
                    break
            messagebox.showinfo("Sucesso", f"Atalho '{gatilho}' salvo com sucesso!")
        else:
            messagebox.showerror("Erro", "Não foi possível salvar o atalho no arquivo JSON.")

    def _excluir_atalho(self):
        """Remove o atalho selecionado."""
        selecionado = self.tabela.selection()
        gatilho = self.var_gatilho.get().strip()

        if not selecionado and not gatilho:
            messagebox.showwarning("Atenção", "Selecione um atalho da lista para excluir.")
            return

        if selecionado:
            gatilho = self.tabela.item(selecionado[0])["values"][0]

        confirmar = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o atalho '{gatilho}'?",
        )
        if not confirmar:
            return

        with atalhos_lock:
            if gatilho in atalhos:
                del atalhos[gatilho]
                sucesso = salvar_atalhos(atalhos)
            else:
                sucesso = False

        if sucesso:
            self._limpar_campos()
            self._atualizar_tabela()
            messagebox.showinfo("Sucesso", f"Atalho '{gatilho}' removido com sucesso!")
        else:
            messagebox.showerror("Erro", f"O atalho '{gatilho}' não foi encontrado.")


def main():
    global atalhos
    # 1. Carrega os atalhos do JSON inicial
    atalhos = carregar_atalhos()
    print(f"[{len(atalhos)}] atalhos carregados de {ARQUIVO_JSON}.")

    # 2. Inicia o monitor de digitação em segundo plano
    t = threading.Thread(target=monitorar, daemon=True)
    t.start()
    print("Monitor de teclado iniciado em segundo plano.")

    # 3. Inicia a interface gráfica
    app = InterfaceAtalhos()
    app.mainloop()


if __name__ == "__main__":
    main()
