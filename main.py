import streamlit as st
import requests
import os
from dotenv import load_dotenv
from app_manager import manage_companies, manage_products, manage_reviews


load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")

st.set_page_config(
    page_title="Dashboard de Empresas",
    layout="wide",
)

st.title(" Dashboard Integrado de Empresas")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "access_token" not in st.session_state:
    st.session_state.access_token = ""
if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""


def login(email, password):
    url = f"{API_BASE_URL}/auth/token"
    data = {"username": email, "password": password}
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            tokens = response.json()
            st.session_state.logged_in = True
            st.session_state.access_token = tokens["access_token"]
            st.session_state.refresh_token = tokens["refresh_token"]
            st.session_state.user_email = email
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Credenciais inválidas. Verifique seu e-mail e senha.")
    except requests.exceptions.ConnectionError:
        st.error("Erro de conexão. Verifique se a sua API está rodando.")

if not st.session_state.logged_in:
    st.subheader("Faça login para continuar")
    with st.form(key="login_form"):
        email = st.text_input("E-mail")
        password = st.text_input("Senha", type="password")
        submit_button = st.form_submit_button("Entrar")
        if submit_button:
            login(email, password)

    st.subheader("Não tem uma conta?")
    with st.form(key="register_form"):
        register_email = st.text_input("E-mail para cadastro")
        register_password = st.text_input("Senha para cadastro", type="password")
        register_button = st.form_submit_button("Cadastrar")
        if register_button:
            register_url = f"{API_BASE_URL}/auth/register"
            register_data = {"email": register_email, "password": register_password}
            try:
                response = requests.post(register_url, json=register_data)
                if response.status_code == 200:
                    st.success("Usuário cadastrado com sucesso! Agora você pode fazer o login.")
                else:
                    st.error(f"Erro ao cadastrar: {response.json().get('detail', 'Erro desconhecido')}")
            except requests.exceptions.ConnectionError:
                st.error("Erro de conexão. Verifique se a sua API está rodando.")

else:
    st.sidebar.header(f"Bem-vindo, {st.session_state.user_email}!")
    st.sidebar.button("Sair", on_click=lambda: (st.session_state.clear(), st.rerun()))

    st.header("Dashboard e Gerenciamento de Dados")
    
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    

    tab_list, tab_faturamento, tab_produtos, tab_avaliacoes, tab_insights, tab_gerenciar = st.tabs(["Listar", "Faturamento", "Produtos", "Avaliações", "Insights", "Gerenciar"])

    with tab_list:
        st.subheader("Lista de Empresas")
        url = f"{API_BASE_URL}/api/empresas/"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            empresas = response.json()
            if empresas:
                st.dataframe(empresas)
            else:
                st.warning("Nenhuma empresa cadastrada. Use a aba 'Gerenciar' para adicionar uma.")
        else:
            st.error("Não foi possível carregar os dados das empresas. Tente fazer o login novamente.")

    with tab_faturamento:
        st.subheader("Faturamento Geral")
        url = f"{API_BASE_URL}/api/faturamento/"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            st.dataframe(response.json())
        else:
            st.error("Não foi possível carregar os dados de faturamento. Tente fazer o login novamente.")

    with tab_produtos:
        st.subheader("Produtos Vendidos")
        url = f"{API_BASE_URL}/api/produtos/"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            st.dataframe(response.json())
        else:
            st.error("Não foi possível carregar os dados de produtos. Tente fazer o login novamente.")

    with tab_avaliacoes:
        st.subheader("Avaliações de Diretores e Empresas")
        url = f"{API_BASE_URL}/api/avaliacoes/"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            st.dataframe(response.json())
        else:
            st.error("Não foi possível carregar as avaliações. Tente fazer o login novamente.")


    with tab_insights:
        st.subheader("Insights de Negócio")
        

        url = f"{API_BASE_URL}/api/insights/"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            insights = response.json()
            st.write("---")
            if insights:
                st.subheader("Faturamento e Avaliação por Empresa")
                for insight in insights:
                    st.markdown(f"**Empresa:** {insight['nome_empresa']}")
                    st.markdown(f"**Faturamento Total Anual:** R$ {insight['faturamento_total_anual']:,.2f}")
                    st.markdown(f"**Média da Nota:** {insight['media_nota_empresa']:.2f}")
                    st.write("---")
            else:
                st.warning("Nenhum insight disponível.")
            

            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("Piores Diretores (pelo faturamento)")
                url_piores = f"{API_BASE_URL}/api/pioresdiretores/"
                response_piores = requests.get(url_piores, headers=headers)
                if response_piores.status_code == 200:
                    piores = response_piores.json()
                    for item in piores:
                        diretor = item['diretor_empresa']
                        faturamento = item['faturamento_anual']
                        try:
                            faturamento_float = float(faturamento)
                            st.markdown(f"- **Diretor:** {diretor} (Faturamento: R$ {faturamento_float:,.2f})")
                        except (ValueError, TypeError):
                            st.markdown(f"- **Diretor:** {diretor} (Faturamento: {faturamento})")
                else:
                    st.warning("Não foi possível carregar os dados.")

            with col2:
                st.subheader("Produtos de Maior Lucro")
                url_lucro = f"{API_BASE_URL}/api/insights/maior_lucro/"
                response_lucro = requests.get(url_lucro, headers=headers)
                if response_lucro.status_code == 200:
                    lucro = response_lucro.json()
                    for item in lucro[:5]: 
                        st.markdown(f"- **Produto:** {item['nome_produto']} ({item['nome_empresa']})")
                        st.markdown(f"  - **Faturamento:** R$ {item['faturamento_total']:,.2f}")
                else:
                    st.warning("Não foi possível carregar os dados.")

            with col3:
                st.subheader("Melhores Diretores (pelo faturamento)")
                url_melhores = f"{API_BASE_URL}/melhoresdiretores/"
                response_melhores = requests.get(url_melhores, headers=headers)
                if response_melhores.status_code == 200:
                    melhores = response_melhores.json()
                    for item in melhores:
                        diretor = item['diretor_empresa']
                        faturamento = item['faturamento_anual']
                        try:
                            faturamento_float = float(faturamento)
                            st.markdown(f"- **Diretor:** {diretor} (Faturamento: R$ {faturamento_float:,.2f})")
                        except (ValueError, TypeError):
                            st.markdown(f"- **Diretor:** {diretor} (Faturamento: {faturamento})")
                else:
                    st.warning("Não foi possível carregar os dados.")



    with tab_gerenciar:
        st.header("Gerenciamento de Dados")
        

        gerenciar_empresas_tab, gerenciar_produtos_tab, gerenciar_avaliacoes_tab = st.tabs(["Empresas", "Produtos", "Avaliações"])

        with gerenciar_empresas_tab:
            manage_companies(API_BASE_URL, headers)
        
        with gerenciar_produtos_tab:
            manage_products(API_BASE_URL, headers)

        with gerenciar_avaliacoes_tab:
            manage_reviews(API_BASE_URL, headers)