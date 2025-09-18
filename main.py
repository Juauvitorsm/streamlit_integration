import streamlit as st
import requests
import os
from dotenv import load_dotenv
from app_manager import manage_companies, manage_product_details, manage_reviews, manage_sold_products, manage_faturamento
import pandas as pd
import altair as alt


load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")

st.set_page_config(
    page_title="Dashboard de Empresas",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Dashboard Integrado de Empresas")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "access_token" not in st.session_state:
    st.session_state.access_token = ""
if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""


def check_login_state():
    query_params = st.query_params
    if "logged_in" in query_params and query_params["logged_in"] == "true":
        st.session_state.logged_in = True
        st.session_state.access_token = query_params["access_token"]
        st.session_state.user_email = query_params["user_email"]

check_login_state()

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
            st.query_params.logged_in = "true"
            st.query_params.access_token = st.session_state.access_token
            st.query_params.user_email = st.session_state.user_email
            st.rerun()
        else:
            st.error("Credenciais inválidas. Verifique seu e-mail e senha.")
    except requests.exceptions.ConnectionError:
        st.error("Erro de conexão. Verifique se a sua API está rodando.")

def logout():
    st.session_state.clear()
    st.query_params.clear()
    st.rerun()


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
    st.sidebar.button("Sair", on_click=logout)
    
    st.header("Dashboard e Gerenciamento de Dados")
    
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    
    if st.button("Atualizar Dados"):
        st.rerun()

    tab_list, tab_faturamento, tab_produtos_vendidos, tab_detalhes_produtos, tab_avaliacoes, tab_insights, tab_gerenciar = st.tabs(["Listar", "Faturamento", "Prod. Vendidos", "Detalhes Prod.", "Avaliações", "Insights", "Gerenciar"])

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

    with tab_produtos_vendidos:
        st.subheader("Produtos Vendidos")
        url = f"{API_BASE_URL}/api/produtos_vendidos/"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            st.dataframe(response.json())
        else:
            st.error("Não foi possível carregar os dados de produtos vendidos. Tente fazer o login novamente.")
    
    with tab_detalhes_produtos:
        st.subheader("Detalhes dos Produtos")
        url = f"{API_BASE_URL}/api/detalhes_produtos/"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            st.dataframe(response.json())
        else:
            st.error("Não foi possível carregar os detalhes dos produtos. Tente fazer o login novamente.")
    
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

        col1, col2, col3 = st.columns(3)
        
      
        url_insights = f"{API_BASE_URL}/api/insights/"
        response_insights = requests.get(url_insights, headers=headers)
        

        url_notas_diretores = f"{API_BASE_URL}/api/media_notas_diretor/"
        response_notas_diretores = requests.get(url_notas_diretores, headers=headers)

        if response_insights.status_code == 200 and response_notas_diretores.status_code == 200:
            insights_data = response_insights.json()
            notas_data = response_notas_diretores.json()
            
            if insights_data and notas_data:
                df_insights = pd.DataFrame(insights_data)
                df_notas_diretores = pd.DataFrame(notas_data)
                

                df_sorted_faturamento = df_insights.sort_values(by="faturamento_total_anual", ascending=False)
                empresa_maior_faturamento = df_sorted_faturamento.iloc[0]
                with col1:
                    st.metric(
                        label=f" Empresa com Maior Faturamento Anual", 
                        value=empresa_maior_faturamento["nome_empresa"], 
                        delta=f"R$ {empresa_maior_faturamento['faturamento_total_anual']:,.2f}"
                    )
                

                melhor_diretor_info = df_notas_diretores.sort_values(by="media_nota", ascending=False).iloc[0]
                with col2:
                    st.metric(
                        label=" Melhor Diretor (por Nota)",
                        value=melhor_diretor_info["diretor_empresa"],
                        delta=f"Nota: {melhor_diretor_info['media_nota']:.2f}"
                    )
                

                faturamento_total = df_insights['faturamento_total_anual'].sum()
                with col3:
                    st.metric(
                        label=" Faturamento Anual Total (Todas Empresas)",
                        value=f"R$ {faturamento_total:,.2f}"
                    )
                
                st.markdown("---")
                
                st.subheader("Análise Detalhada por Empresa")
                col1_anual, col2_anual = st.columns(2)
                
                with col1_anual:
                    st.subheader("Faturamento Total Anual por Empresa")
                    chart1 = alt.Chart(df_insights).mark_bar().encode(
                        x=alt.X('nome_empresa', title='Empresa'),
                        y=alt.Y('faturamento_total_anual', title='Faturamento Anual (R$)'),
                        tooltip=['nome_empresa', alt.Tooltip('faturamento_total_anual', format=',.2f')]
                    ).properties(
                        title='Faturamento Total Anual por Empresa'
                    )
                    st.altair_chart(chart1, use_container_width=True)

                with col2_anual:
                    st.subheader("Média da Nota por Empresa")
                    chart2 = alt.Chart(df_insights).mark_bar().encode(
                        x=alt.X('nome_empresa', title='Empresa'),
                        y=alt.Y('media_nota_empresa', title='Média da Nota'),
                        tooltip=['nome_empresa', alt.Tooltip('media_nota_empresa', format='.2f')]
                    ).properties(
                        title='Média da Nota por Empresa'
                    )
                    st.altair_chart(chart2, use_container_width=True)
            else:
                st.warning("Nenhum insight de empresa disponível.")
        else:
            st.warning("Não foi possível carregar os insights. Tente fazer o login novamente.")
        
        st.markdown("---")
        
        col1_piores, col2_lucro, col3_melhores = st.columns(3)
        

        url_piores = f"{API_BASE_URL}/api/pioresdiretores/"
        response_piores = requests.get(url_piores, headers=headers)
        

        url_lucro = f"{API_BASE_URL}/api/insights/maior_lucro/"
        response_lucro = requests.get(url_lucro, headers=headers)


        url_melhores = f"{API_BASE_URL}/api/melhoresdiretores/"
        response_melhores = requests.get(url_melhores, headers=headers)
        
        url_faturamento_mensal = f"{API_BASE_URL}/api/faturamento_mensal_por_empresa/"
        response_faturamento_mensal = requests.get(url_faturamento_mensal, headers=headers)

        if response_piores.status_code == 200 and response_lucro.status_code == 200 and response_melhores.status_code == 200 and response_faturamento_mensal.status_code == 200:
            piores_data = response_piores.json()
            lucro_data = response_lucro.json()
            melhores_data = response_melhores.json()
            faturamento_mensal_data = response_faturamento_mensal.json()

            with col1_piores:
                st.subheader("Piores Diretores")
                if piores_data:
                    df_piores = pd.DataFrame(piores_data)
                    chart3 = alt.Chart(df_piores).mark_bar().encode(
                        x=alt.X('diretor_empresa', title='Diretor'),
                        y=alt.Y('faturamento_anual', title='Faturamento Anual (R$)'),
                        tooltip=['diretor_empresa', alt.Tooltip('faturamento_anual', format=',.2f')]
                    ).properties(
                        title='Piores Diretores (Pelo Faturamento)'
                    )
                    st.altair_chart(chart3, use_container_width=True)
                else:
                    st.warning("Nenhum dado de piores diretores disponível.")

            with col2_lucro:
                st.subheader("Produtos de Maior Lucro")
                if lucro_data:
                    df_lucro = pd.DataFrame(lucro_data)
                    chart4 = alt.Chart(df_lucro).mark_bar().encode(
                        x=alt.X('nome_produto', title='Produto'),
                        y=alt.Y('faturamento_total', title='Faturamento Total (R$)'),
                        tooltip=['nome_produto', 'nome_empresa', alt.Tooltip('faturamento_total', format=',.2f')]
                    ).properties(
                        title='Produtos de Maior Lucro'
                    )
                    st.altair_chart(chart4, use_container_width=True)
                else:
                    st.warning("Nenhum dado de maior lucro disponível.")

            with col3_melhores:
                st.subheader("Melhores Diretores")
                if melhores_data:
                    df_melhores = pd.DataFrame(melhores_data)
                    chart5 = alt.Chart(df_melhores).mark_bar().encode(
                        x=alt.X('diretor_empresa', title='Diretor'),
                        y=alt.Y('faturamento_anual', title='Faturamento Anual (R$)'),
                        tooltip=['diretor_empresa', alt.Tooltip('faturamento_anual', format=',.2f')]
                    ).properties(
                        title='Melhores Diretores (Pelo Faturamento)'
                    )
                    st.altair_chart(chart5, use_container_width=True)
                else:
                    st.warning("Nenhum dado de melhores diretores disponível.")
        else:
            st.warning("Não foi possível carregar os dados de diretores e lucros. Tente fazer o login novamente.")

        st.markdown("---")
        
        st.subheader("Análise de Faturamento Mensal")
        if faturamento_mensal_data:
            df_faturamento_mensal = pd.DataFrame(faturamento_mensal_data)
            chart_mensal = alt.Chart(df_faturamento_mensal).mark_bar().encode(
                x=alt.X('nome_empresa', title='Empresa'),
                y=alt.Y('faturamento_mensal', title='Faturamento Mensal (R$)'),
                tooltip=['nome_empresa', alt.Tooltip('faturamento_mensal', format=',.2f')]
            ).properties(
                title='Faturamento Mensal por Empresa'
            )
            st.altair_chart(chart_mensal, use_container_width=True)
        else:
            st.warning("Nenhum dado de faturamento mensal disponível.")


    with tab_gerenciar:
        st.header("Gerenciamento de Dados")
        
        gerenciar_empresas_tab, gerenciar_detalhes_produtos_tab, gerenciar_produtos_vendidos_tab, gerenciar_avaliacoes_tab, gerenciar_faturamento_tab = st.tabs(["Empresas", "Detalhes Prod.", "Prod. Vendidos", "Avaliações", "Faturamento"])

        with gerenciar_empresas_tab:
            manage_companies(API_BASE_URL, headers)
        
        with gerenciar_detalhes_produtos_tab:
            manage_product_details(API_BASE_URL, headers)
        
        with gerenciar_produtos_vendidos_tab:
            manage_sold_products(API_BASE_URL, headers)

        with gerenciar_avaliacoes_tab:
            manage_reviews(API_BASE_URL, headers)
            
        with gerenciar_faturamento_tab:
            manage_faturamento(API_BASE_URL, headers)
