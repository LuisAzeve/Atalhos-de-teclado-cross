import keyboard
import pyperclip
import time
 
 
#o script abaixo absorve um texto atrás do : e ao digitar esse texto a mensagem após o : é gerada
atalhos = {
    ".esq": "Esqueceu a senha - chamado ",
    ".rea": "Reativação de login - chamado ",
    ".inc": "Inclusão de unidade - chamado ",
    ".can": "Cancelamento de login - chamado ",
    ".cri": "Criação de login - chamado ",
    ".pro": "Prorrogação de login - chamado ",
    ".uni": "Alteração de unidade - chamado",
    ".per": "Alteração de perfil - chamado",
    ".temp": "Temperatura em (xx) Abaixado para (xx)",
    ".expirar": """ Bom dia!

Segue abaixo a relação de logins próximos ao vencimento.

Pedimos que informem se os colaboradores listados necessitam de reciclagem (novo treinamento com a equipe CROSS) ou se já não fazem mais parte do quadro de funcionários.

Importante destacar que não haverá alteração de login ou senha. Será apenas realizada a prorrogação do prazo de acesso por mais 12 meses, caso seja confirmada a necessidade de manutenção.

Para darmos continuidade, solicitamos que preencham a planilha padrão de solicitação com os dados dos colaboradores e da unidade, e a encaminhem para o e-mail chamados.helpdesk@cross.org.br
, indicando na própria planilha se trata de reativação ou cancelamento do login.

Atenciosamente,
 """,
    ".chama": """  Chamado:
    Boa noite,
Informamos que a solicitação foi atendida
 
Unidade inclusa ao acesso

-------------------------------------
Já possui acesso
 
-------------------------------------
Prorrogado
 
-------------------------------------
CPF inválido
 
-------------------------------------
Criado
Nome:
login: 
Senha: 
-------------------------------------
 
 
 
Atenciosamente.""",
    ".pad": """Boa noite,
Informamos que a solicitação foi atendida

Unidade inclusa ao acesso
-------------------------------------
Já possui acesso
-------------------------------------
Prorrogado
-------------------------------------
CPF inválido
-------------------------------------
Criado
-------------------------------------
 
Atenciosamente.""",
".soli": """" Boa noite,
devido sua unidade ser solicitante solicitação não pode ser atendida orientamos contato com seu DRS responsável

Atenciosamente.
Luis Felippe
""",

    ".baixo": """Incidente baixo -   - ID
link:""",
 ".medio": """Incidente medio -   - ID
link:""",
 ".alto": """Incidente alto -   - ID
link:""",
    ".liga": """Título:  -   - (dar f5)
   
Descrição:
 
Solução:
------------------------------------------------------------------------------------------------""",
    ".duo": """Bom dia,
Informamos que sua requisição foi encaminhada para verificação com a equipe de Analistas, assim que obtivermos um retorno, seguiremos com a tratativa.
 
Atenciosamente,""",
    ".requi": """Requisição aberta com a desenvolvedora
 
ID:
Link acesso:""",
    ".inci": """Incidente aberto com a desenvolvedora
 
ID:
Link acesso:""",
    ".leit": """Boa noite,
Informamos que não podemos atender à solicitação, pois o campo "Tipo de Saída" só pode ser alterado para uma das opções listadas abaixo:
Alta
Óbito
Evasão / Saída a pedido
Saída administrativa
Transferência externa
Transferência interna
Aguardamos seu retorno para darmos seguimento na demanda
 
Atenciosamente,""",
    ".urge": """Descrição: Contato com a regulação
 
Solução:  fornecido contato""",
    ".priva": """Descrição: paciente restrito
 
Solução: Orientado contato do DRS
""",
 ".des": """Descrição: paciente desconhecido
 
Solução: Orientado contato com a regulação urgência 5112-8800
""",
    ".sex": """Descrição: Alterar sexo do paciente

cód: 

Alterado de:

Alterado para:
 
Solução: alterado
""",
    ".pla": """Boa noite, informamos que a solicitação não foi atendida, a planilha encaminhada não atende os padrões novos exigidos para atendimento 

  Modelo padrão de planilha em anexo para facilitar o preenchimento, pedimos que preencham o modelo atual para facilitar o atendimento do chamado



Atenciosamente.
"""


}
 
def monitorar():
    buffer = ""
 
    while True:
        evento = keyboard.read_event()
 
        if evento.event_type == keyboard.KEY_DOWN:
            tecla = evento.name
 
            if tecla in ['space', 'enter', 'tab']:
                buffer = ""
                continue
 
            if tecla == 'backspace':
                buffer = buffer[:-1]
                continue
 
            if len(tecla) == 1:
                buffer += tecla
 
            for gatilho in atalhos:
                if buffer.endswith(gatilho):
                    texto = atalhos[gatilho]
 
                    for _ in gatilho:
                        keyboard.press_and_release('backspace')
                        time.sleep(0.01)
 
                    pyperclip.copy(texto)
                    keyboard.press_and_release('ctrl+v')
 
                    buffer = ""
 
print("Rodando... digite qualquer atalho para colar a mensagem correspondente.")
print("Pressione Ctrl+C para sair.")
monitorar()