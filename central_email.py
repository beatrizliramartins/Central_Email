import streamlit as st 
from pathlib import Path
from utilidades import envia_email

PASTA_ATUAL = Path(__file__).parent
PASTA_TEMPLATES = PASTA_ATUAL / 'templates'
PASTA_LISTA_EMAILS = PASTA_ATUAL / 'lista_email'
PASTA_CONFIGURACOES = PASTA_ATUAL / 'configuracoes'

if not 'pagina_central_email' in st.session_state:
    st.session_state.pagina_central_email = 'home'

def inicializacao():
    if not 'pagina_central_email' in st.session_state:
        st.session_state.pagina_central_email = 'home'
    if not 'destinatarios_atual' in st.session_state:
        st.session_state.destinatarios_atual = ''
    if not 'titulo_atual' in st.session_state:
        st.session_state.titulo_atual = ''
    if not 'corpo_atual' in st.session_state:
        st.session_state.corpo_atual = ''

def mudar_pagina(nome_pagina):
    st.session_state.pagina_central_email = nome_pagina
# ================ Home ===============
def home():
    destinatarios_atual = st.session_state.destinatarios_atual
    titulo_atual = st.session_state.titulo_atual
    corpo_atual = st.session_state.corpo_atual

    st.markdown('# Central de Emails')
    destinarios = st.text_input('Destinatários do email:', value=destinatarios_atual)
    titulo = st.text_input('Título do email:', value=titulo_atual)
    corpo = st.text_area('Digite o email:', value=corpo_atual, height=400)
    col1, col2, col3 = st.columns(3)
    col1.button('Enviar E-mail', use_container_width=True, on_click=_enviar_email, args=(destinarios, titulo, corpo))
    col3.button('Limpar', use_container_width=True, on_click=_limpar)
    
    st.session_state.destinatarios_atual = destinarios
    st.session_state.titulo_atual = titulo
    st.session_state.corpo_atual = corpo

def _enviar_email(destinatarios, titulo, corpo):
    destinatarios = destinatarios.replace(' ', '').split(',')
    email_usuario = le_email_usuario()
    chave = le_chave_usuario()
    if email_usuario == '':
        st.error('Adicione email na página de configurações')
    elif chave == '':
        st.error('Adicione a chave do email na página de configurações')
    else:
        envia_email(email_usuario,
                    destinatarios=destinatarios,
                    titulo=titulo,
                    corpo=corpo, 
                    senha_app= chave)
    

def _limpar():
    st.session_state.destinatarios_atual = ''
    st.session_state.titulo_atual = ''
    st.session_state.corpo_atual = ''



# ================ Templates ===============
def pag_templates():
    st.markdown('# Templates')
    st.divider()

    for arquivo in PASTA_TEMPLATES.glob('*.txt'):
        nome_arquivo = arquivo.stem.replace('_', ' ').upper()
        col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
        col1.button(nome_arquivo, key=f'{nome_arquivo}', 
                              use_container_width=True,
                              on_click=_usar_template,
                              args=(nome_arquivo, ))
        col2.button('EDITAR', key=f'editar_{nome_arquivo}', 
                              use_container_width=True,
                              on_click=_editar_arquivo,
                              args=(nome_arquivo, ))
        col3.button('REMOVER', key=f'remover_{nome_arquivo}', 
                               use_container_width=True, 
                               on_click=_remove_template, 
                               args=(nome_arquivo, ))

    st.divider()
    st.button('Adicionar Template', on_click=mudar_pagina, args=('adicionar_novo_template', ))


def pag_templates():
    st.markdown('# Templates')
    st.divider()

    for arquivo in PASTA_TEMPLATES.glob('*.txt'):
        nome_arquivo = arquivo.stem.replace('_', ' ').upper()
        col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
        col1.button(nome_arquivo, key=f'{nome_arquivo}', 
                              use_container_width=True,
                              on_click=_usar_template,
                              args=(nome_arquivo, ))
        col2.button('EDITAR', key=f'editar_{nome_arquivo}', 
                              use_container_width=True,
                              on_click=_editar_arquivo,
                              args=(nome_arquivo, ))
        col3.button('REMOVER', key=f'remover_{nome_arquivo}', 
                               use_container_width=True, 
                               on_click=_remove_template, 
                               args=(nome_arquivo, ))

    st.divider()
    st.button('Adicionar Template', on_click=mudar_pagina, args=('adicionar_novo_template', ))

def pag_adicionar_novo_template(nome_template='', texto_template=''):
    nome_template = st.text_input('Nome do template:', value=nome_template)
    texto_template = st.text_area('Escreva o texto do template:', value=texto_template, height=600)
    st.button('Salvar', on_click=_salvar_template, args=(nome_template, texto_template))
    
def _usar_template(nome):
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    with open(PASTA_TEMPLATES / nome_arquivo) as f:
        texto_arquivo = f.read()
    st.session_state.corpo_atual = texto_arquivo
    mudar_pagina('home')
    
def _salvar_template(nome, texto):
    PASTA_TEMPLATES.mkdir(exist_ok=True)
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    with open(PASTA_TEMPLATES / nome_arquivo, 'w') as f:
        f.write(texto)
    mudar_pagina('templates')

def _remove_template(nome):
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    (PASTA_TEMPLATES / nome_arquivo).unlink()

def _editar_arquivo(nome):
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    with open(PASTA_TEMPLATES / nome_arquivo) as f:
        texto_arquivo = f.read()
    st.session_state.nome_template_editar = nome
    st.session_state.texto_template_editar = texto_arquivo
    mudar_pagina('editar_template')


# ================ Lista de E-mails ===============
def pag_lista_email():
    st.markdown('# Lista Email')
    st.divider()
    for arquivo in PASTA_LISTA_EMAILS.glob('*.txt'):
        nome_arquivo = arquivo.stem.replace('_', ' ').upper()
        col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
        col1.button(nome_arquivo, key=f'{nome_arquivo}',
                                  use_container_width=True,
                                  on_click=_usa_lista,
                                  args=(nome_arquivo, ))
        col2.button('EDITAR', key=f'editar_{nome_arquivo}',
                              use_container_width=True,
                              on_click=_editar_lista,
                              args=(nome_arquivo, ))
        col3.button('REMOVER', key=f'remover_{nome_arquivo}',
                               use_container_width=True,
                               on_click=_remove_lista,
                               args=(nome_arquivo, ))
        
    st.divider()
    st.button('Adiciona Lista', on_click=mudar_pagina, args=('adicionar_nova_lista', ))

def pag_adicionar_nova_lista(nome_lista='', emails_lista=''):
    nome_lista = st.text_input('Nome da lista:', value=nome_lista)
    emails_lista = st.text_area('Escreva os emails separados por vírgula:', value=emails_lista, height=600)
    st.button('Salvar', on_click=_salvar_lista, args=(nome_lista, emails_lista))

def _usa_lista(nome):
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    with open(PASTA_LISTA_EMAILS / nome_arquivo) as f:
        texto_arquivo = f.read()
    st.session_state.destinatarios_atual = texto_arquivo
    mudar_pagina('home')

def _salvar_lista(nome, texto):
    PASTA_LISTA_EMAILS.mkdir(exist_ok=True)
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    with open(PASTA_LISTA_EMAILS / nome_arquivo, 'w') as f:
        f.write(texto)
    mudar_pagina('lista_emails')

def _remove_lista(nome):
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    (PASTA_LISTA_EMAILS / nome_arquivo).unlink()

def _editar_lista(nome):
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    with open(PASTA_LISTA_EMAILS / nome_arquivo) as f:
        texto_arquivo = f.read()
    st.session_state.nome_lista_editar = nome
    st.session_state.texto_lista_editar = texto_arquivo
    mudar_pagina('editar_lista')

def remove_template(nome):
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    (PASTA_TEMPLATES / nome_arquivo).unlink()

def _editar_arquivo(nome):
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    with open(PASTA_TEMPLATES / nome_arquivo) as f:
        texto_arquivo = f.read()
    st.session_state.nome_template_editar = nome 
    st.session_state.texto_template_editar = texto_arquivo 
    mudar_pagina('editar_template')

# ================ Confugurações ===============
def pag_configuracao():
    st.markdown('# Configurações')
    email = st.text_input('Digite o seu email:')
    st.button('Salvar', key='salvar_email', 
                        on_click=_salvar_email,
                        args=(email, ))
    chave = st.text_input('Digite a chave de email:')
    st.button('Salvar', key='salvar_chave',
                        on_click=_salvar_chave,
                        args=(chave, ))

def _salvar_email(email):
    PASTA_CONFIGURACOES.mkdir(exist_ok=True)
    with open(PASTA_CONFIGURACOES / 'email_usuario.txt', 'w') as f:
        f.write(email)

def _salvar_chave(chave):
    PASTA_CONFIGURACOES.mkdir(exist_ok=True)
    with open(PASTA_CONFIGURACOES / 'chave.txt', 'w') as f:
        f.write(chave)


def le_email_usuario():
    PASTA_CONFIGURACOES.mkdir(exist_ok=True)
    if (PASTA_CONFIGURACOES / 'email_usuario.txt').exists():
        with open(PASTA_CONFIGURACOES / 'email_usuario.txt', 'r') as f:
            return f.read()
    return ''

def le_chave_usuario():
    PASTA_CONFIGURACOES.mkdir(exist_ok=True)
    if (PASTA_CONFIGURACOES / 'chave.txt').exists():
        with open(PASTA_CONFIGURACOES / 'chave.txt', 'r') as f:
            return f.read()
    return ''




def main():
    inicializacao()

    
    st.sidebar.button('Central de Emails', use_container_width=True, on_click=mudar_pagina, args=('home',))
    st.sidebar.button('Templates', use_container_width=True, on_click=mudar_pagina, args=('templates',))
    st.sidebar.button('lista de Email', use_container_width=True, on_click=mudar_pagina, args=('lista_emails',))
    st.sidebar.button('Configuração', use_container_width=True, on_click=mudar_pagina, args=('configuracao',))

    if st.session_state.pagina_central_email == 'home':
        home()
    elif st.session_state.pagina_central_email == 'templates':
        pag_templates()
    elif st.session_state.pagina_central_email == 'adicionar_novo_template':
        pag_adicionar_novo_template()
    elif st.session_state.pagina_central_email == 'editar_template':
        nome_template_editar = st.session_state.nome_template_editar  
        texto_template_editar = st.session_state.texto_template_editar 
        pag_adicionar_novo_template(nome_template_editar, texto_template_editar)
    elif st.session_state.pagina_central_email == 'lista_emails':
        pag_lista_email()
    elif st.session_state.pagina_central_email == 'adicionar_nova_lista':
        pag_adicionar_nova_lista()
    elif st.session_state.pagina_central_email == 'editar_lista':
        nome_lista = st.session_state.nome_lista_editar
        texto_lista = st.session_state.texto_lista_editar
        pag_adicionar_nova_lista(nome_lista, texto_lista)
    elif st.session_state.pagina_central_email == 'configuracao':
        pag_configuracao()
main()