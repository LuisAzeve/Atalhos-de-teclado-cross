# ⌨️ Expansor de Atalhos de Teclado

Um utilitário em Python para expansão de texto e atalhos rápidos de teclado. Ao digitar um gatilho pré-definido (por exemplo, `.chamado` ou `.esq`), o script apaga automaticamente o atalho digitado e cola no lugar a mensagem correspondente (frases prontas, modelos de chamados, comunicados, respostas padrão, etc.).

---

## 🚀 Novidades da Versão com Interface

- **Armazenamento em JSON (`atalhos.json`)**: Os atalhos não ficam mais fixos no código-fonte, facilitando edição, backup e compartilhamento.
- **Interface Gráfica Intuitiva**: Gerencie seus atalhos através de uma interface visual simples e prática (Tkinter).
- **Cadastro e Edição**: Adicione novos gatilhos e mensagens com suporte a múltiplas linhas.
- **Exclusão de Atalhos**: Remova qualquer atalho rapidamente pela interface com confirmação.
- **Busca em Tempo Real**: Filtre atalhos facilmente pelo nome do gatilho ou trecho da mensagem.
- **Sincronização Imediata**: Atalhos cadastrados ou removidos entram em vigor na hora, sem precisar fechar ou reiniciar o programa.
- **Controle de Monitoramento**: Botão para pausar e retomar a detecção de atalhos a qualquer momento.

---

## 📋 Pré-requisitos

- **Python 3.8+** instalado.
- Bibliotecas Python necessárias:
  - `keyboard` (para captura e emissão de eventos de teclado)
  - `pyperclip` (para manipulação da área de transferência)
  - `tkinter` (já incluso por padrão nas instalações do Python para Windows)

Para instalar as dependências, execute no terminal:

```bash
pip install keyboard pyperclip
```

---

## ⚙️ Como Executar

> ⚠️ **Atenção (Windows)**: A biblioteca `keyboard` necessita de privilégios de **Administrador** para conseguir capturar e injetar eventos de teclado globais em outros programas (navegadores, chamados, Word, bloco de notas, etc.).

1. Abra o **Prompt de Comando (CMD)** ou **PowerShell** como **Administrador**.
2. Navegue até a pasta do projeto:
   ```bash
   cd "c:\Users\adm.luis.azevedo\OneDrive - spdmafiliadas\Documentos\ferramentas trabalho\Outros\Atalhos teclado"
   ```
3. Execute o script principal:
   ```bash
   python atalhos.py
   ```

A janela da interface será aberta e o monitor de atalhos começará a rodar em segundo plano automaticamente.

---

## 🖥️ Como Usar a Interface

1. **Cadastrar um Atalho**:
   - No campo **Gatilho**, digite o código de ativação desejado (exemplo: `.incidente`, `.bomdia`, `.dúvida`). Recomenda-se iniciar com um ponto `.` para evitar ativação acidental durante a digitação comum.
   - No campo **Texto a ser colado**, digite ou cole a mensagem completa (aceita quebras de linha e textos longos).
   - Clique em **💾 Salvar Atalho**.

2. **Editar um Atalho**:
   - Clique sobre o atalho desejado na tabela à esquerda.
   - Seus dados serão carregados nos campos à direita.
   - Altere o texto e clique em **💾 Salvar Atalho**.

3. **Excluir um Atalho**:
   - Selecione o atalho na tabela à esquerda.
   - Clique em **🗑️ Excluir Selecionado** e confirme a exclusão.

4. **Pausar o Monitoramento**:
   - Clique no botão **Pausar Monitor** no topo caso queira digitar gatilhos sem que sejam substituídos. Para voltar a usar, clique em **Retomar Monitor**.

---

## 📁 Estrutura dos Arquivos

```text
Atalhos teclado/
├── atalhos.py       # Script principal com a interface gráfica e o monitor em segundo plano
├── atalhos.json     # Base de dados contendo os atalhos e suas mensagens
└── README.md        # Documentação do projeto
```

### Exemplo de formato do `atalhos.json`:

```json
{
    ".esq": "Esqueceu a senha - chamado ",
    ".rea": "Reativação de login - chamado ",
    ".duo": "Bom dia,\nInformamos que sua requisição foi encaminhada..."
}
```

---

## 💡 Como Funciona o Monitoramento

O script captura as teclas pressionadas globalmente pelo usuário mantendo um buffer temporário. Sempre que a sequência de teclas digitadas corresponder ao final de um gatilho cadastrado:
1. Pressiona a tecla `Backspace` o número exato de vezes do gatilho digitado (removendo-o da tela).
2. Carrega a mensagem correspondente na área de transferência com `pyperclip`.
3. Pressiona `Ctrl + V` para colar o texto final instantaneamente no local do cursor.

