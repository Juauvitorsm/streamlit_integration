import streamlit as st
import requests
from datetime import date

def manage_companies(API_BASE_URL, headers):
    st.subheader("Adicionar Nova Empresa")
    with st.form(key="add_empresa_form"):
        nome_empresa_add = st.text_input("Nome da Empresa")
        diretor_empresa_add = st.text_input("Nome do Diretor")
        submit_add = st.form_submit_button("Adicionar Empresa")

        if submit_add:
            if nome_empresa_add and diretor_empresa_add:
                add_url = f"{API_BASE_URL}/api/empresas/"
                add_data = {
                    "nome_empresa": nome_empresa_add,
                    "diretor_empresa": diretor_empresa_add
                }
                try:
                    response = requests.post(add_url, headers=headers, json=add_data)
                    if response.status_code == 200:
                        st.success(f"Empresa '{nome_empresa_add}' adicionada com sucesso!")
                    else:
                        st.error(f"Erro ao adicionar empresa: {response.status_code} - {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Erro de conexão com a API.")
            else:
                st.warning("Por favor, preencha todos os campos.")

    st.markdown("---")
    st.subheader("Atualizar Empresa Existente")
    with st.form(key="update_empresa_form"):
        id_empresa_update = st.number_input("ID da Empresa", min_value=1, step=1)
        nome_empresa_update = st.text_input("Novo Nome da Empresa")
        diretor_empresa_update = st.text_input("Novo Nome do Diretor")
        submit_update = st.form_submit_button("Atualizar Empresa")
        
        if submit_update:
            if id_empresa_update and (nome_empresa_update or diretor_empresa_update):
                update_url = f"{API_BASE_URL}/api/empresas/{id_empresa_update}"
                update_data = {}
                if nome_empresa_update:
                    update_data["nome_empresa"] = nome_empresa_update
                if diretor_empresa_update:
                    update_data["diretor_empresa"] = diretor_empresa_update
                
                try:
                    response = requests.put(update_url, headers=headers, json=update_data)
                    if response.status_code == 200:
                        st.success(f"Empresa com ID {id_empresa_update} atualizada com sucesso!")
                    else:
                        st.error(f"Erro ao atualizar empresa: {response.status_code} - {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Erro de conexão com a API.")
            else:
                st.warning("Por favor, preencha o ID e pelo menos um dos campos para atualizar.")

def manage_product_details(API_BASE_URL, headers):
    add_tab, update_tab = st.tabs(["Adicionar Detalhes", "Atualizar Detalhes"])

    with add_tab:
        st.subheader("Adicionar Detalhes do Produto")
        with st.form(key="add_detalhes_form"):
            id_empresa = st.number_input("ID da Empresa", min_value=1, step=1, key="id_empresa_det_add")
            nome_produto = st.text_input("Nome do Produto", key="nome_produto_det_add")
            categoria = st.text_input("Categoria", key="categoria_det_add")
            preco_unitario = st.number_input("Preço Unitário", min_value=0.01, key="preco_unitario_det_add")
            margem_lucro_percentual = st.number_input("Margem de Lucro (%)", min_value=0.0, max_value=100.0, key="margem_lucro_det_add")
            data_lancamento = st.date_input("Data de Lançamento", date.today(), key="data_lancamento_det_add")
            submit_add = st.form_submit_button("Adicionar Detalhes")

            if submit_add:
                add_url = f"{API_BASE_URL}/api/detalhes_produtos/"
                add_data = {
                    "id_empresa": int(id_empresa),
                    "nome_produto": nome_produto,
                    "categoria": categoria,
                    "preco_unitario": float(preco_unitario),
                    "margem_lucro_percentual": float(margem_lucro_percentual),
                    "data_lancamento": str(data_lancamento)
                }
                try:
                    response = requests.post(add_url, headers=headers, json=add_data)
                    if response.status_code == 200:
                        st.success(f"Detalhes do produto '{nome_produto}' adicionados com sucesso!")
                    else:
                        st.error(f"Erro ao adicionar detalhes do produto: {response.status_code} - {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Erro de conexão com a API.")

    with update_tab:
        st.subheader("Atualizar Detalhes do Produto")
        with st.form(key="update_detalhes_form"):
            id_produto_update = st.number_input("ID do Produto", min_value=1, step=1, key="id_produto_det_update")
            nome_produto_update = st.text_input("Novo Nome do Produto", key="nome_produto_det_update")
            categoria_update = st.text_input("Nova Categoria", key="categoria_det_update")
            preco_unitario_update = st.number_input("Novo Preço Unitário", min_value=0.01, key="preco_unitario_det_update")
            margem_lucro_update = st.number_input("Nova Margem de Lucro (%)", min_value=0.0, max_value=100.0, key="margem_lucro_det_update")
            submit_update = st.form_submit_button("Atualizar Detalhes")

            if submit_update:
                update_url = f"{API_BASE_URL}/api/detalhes_produtos/{id_produto_update}"
                update_data = {}
                if nome_produto_update:
                    update_data["nome_produto"] = nome_produto_update
                if categoria_update:
                    update_data["categoria"] = categoria_update
                if preco_unitario_update:
                    update_data["preco_unitario"] = float(preco_unitario_update)
                if margem_lucro_update:
                    update_data["margem_lucro_percentual"] = float(margem_lucro_update)
                
                try:
                    response = requests.put(update_url, headers=headers, json=update_data)
                    if response.status_code == 200:
                        st.success(f"Detalhes do produto com ID {id_produto_update} atualizados com sucesso!")
                    else:
                        st.error(f"Erro ao atualizar detalhes do produto: {response.status_code} - {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Erro de conexão com a API.")

def manage_sold_products(API_BASE_URL, headers):
    add_tab, update_tab = st.tabs(["Adicionar Venda", "Atualizar Venda"])

    with add_tab:
        st.subheader("Adicionar Nova Venda")
        with st.form(key="add_venda_form"):
            id_faturamento = st.number_input("ID do Faturamento", min_value=1, step=1, key="id_faturamento_venda")
            nome_produto = st.text_input("Nome do Produto", key="nome_produto_venda_add")
            produtos_vendidos = st.number_input("Produtos Vendidos", min_value=1, step=1, key="qtd_vendida_add")
            submit_add = st.form_submit_button("Adicionar Venda")

            if submit_add:
                add_url = f"{API_BASE_URL}/api/produtos_vendidos/"
                add_data = {
                    "id_faturamento": int(id_faturamento),
                    "nome_produto": nome_produto,
                    "produtos_vendidos": int(produtos_vendidos)
                }
                try:
                    response = requests.post(add_url, headers=headers, json=add_data)
                    if response.status_code == 200:
                        st.success(f"Venda de '{nome_produto}' adicionada com sucesso!")
                    else:
                        st.error(f"Erro ao adicionar venda: {response.status_code} - {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Erro de conexão com a API.")
    
    with update_tab:
        st.subheader("Atualizar Venda Existente")
        with st.form(key="update_venda_form"):
            id_venda = st.number_input("ID da Venda", min_value=1, step=1, key="id_venda_update")
            id_faturamento_update = st.number_input("Novo ID do Faturamento", min_value=1, step=1, key="id_faturamento_venda_update")
            nome_produto_update = st.text_input("Novo Nome do Produto", key="nome_produto_venda_update")
            produtos_vendidos_update = st.number_input("Nova Quantidade Vendida", min_value=1, step=1, key="qtd_vendida_update")
            submit_update = st.form_submit_button("Atualizar Venda")
            
            if submit_update:
                update_url = f"{API_BASE_URL}/api/produtos_vendidos/{id_venda}"
                update_data = {}
                if id_faturamento_update:
                    update_data["id_faturamento"] = int(id_faturamento_update)
                if nome_produto_update:
                    update_data["nome_produto"] = nome_produto_update
                if produtos_vendidos_update:
                    update_data["produtos_vendidos"] = int(produtos_vendidos_update)
                
                try:
                    response = requests.put(update_url, headers=headers, json=update_data)
                    if response.status_code == 200:
                        st.success(f"Venda com ID {id_venda} atualizada com sucesso!")
                    else:
                        st.error(f"Erro ao atualizar venda: {response.status_code} - {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Erro de conexão com a API.")

def manage_reviews(API_BASE_URL, headers):
    add_tab, update_tab = st.tabs(["Adicionar Avaliação", "Atualizar Avaliação"])

    with add_tab:
        st.subheader("Adicionar Nova Avaliação")
        with st.form(key="add_avaliacao_form"):
            id_empresa = st.number_input("ID da Empresa", min_value=1, step=1, key="id_empresa_review")
            nota_diretor = st.slider("Nota do Diretor (0 a 10)", min_value=0, max_value=10, value=5, key="nota_diretor")
            nota_geral_empresa = st.slider("Nota Geral da Empresa (0 a 10)", min_value=0, max_value=10, value=5, key="nota_geral")
            comentario = st.text_area("Comentário", key="comentario")
            submit_add = st.form_submit_button("Adicionar Avaliação")

            if submit_add:
                add_url = f"{API_BASE_URL}/api/avaliacoes/"
                add_data = {
                    "id_empresa": int(id_empresa),
                    "nota_diretor": int(nota_diretor),
                    "nota_geral_empresa": int(nota_geral_empresa),
                    "comentario": comentario
                }
                try:
                    response = requests.post(add_url, headers=headers, json=add_data)
                    if response.status_code == 200:
                        st.success(f"Avaliação para a empresa {id_empresa} adicionada com sucesso!")
                    else:
                        st.error(f"Erro ao adicionar avaliação: {response.status_code} - {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Erro de conexão com a API.")

    with update_tab:
        st.subheader("Atualizar Avaliação Existente")
        with st.form(key="update_avaliacao_form"):
            id_avaliacao_update = st.number_input("ID da Avaliação", min_value=1, step=1, key="id_avaliacao_update")
            nota_diretor_update = st.slider("Nova Nota do Diretor", min_value=0, max_value=10, key="nota_diretor_update")
            nota_geral_update = st.slider("Nova Nota Geral da Empresa", min_value=0, max_value=10, key="nota_geral_update")
            comentario_update = st.text_area("Novo Comentário", key="comentario_update")
            submit_update = st.form_submit_button("Atualizar Avaliação")
            
            if submit_update:
                update_url = f"{API_BASE_URL}/api/avaliacoes/{id_avaliacao_update}"
                update_data = {}
                if nota_diretor_update is not None:
                    update_data["nota_diretor"] = int(nota_diretor_update)
                if nota_geral_update is not None:
                    update_data["nota_geral_empresa"] = int(nota_geral_update)
                if comentario_update:
                    update_data["comentario"] = comentario_update

                try:
                    response = requests.put(update_url, headers=headers, json=update_data)
                    if response.status_code == 200:
                        st.success(f"Avaliação com ID {id_avaliacao_update} atualizada com sucesso!")
                    else:
                        st.error(f"Erro ao atualizar avaliação: {response.status_code} - {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Erro de conexão com a API.")
def manage_faturamento(API_BASE_URL, headers):
    add_tab, update_tab = st.tabs(["Adicionar Faturamento", "Atualizar Faturamento"])

    with add_tab:
        st.subheader("Adicionar Novo Faturamento")
        with st.form(key="add_faturamento_form"):
            id_empresa = st.number_input("ID da Empresa", min_value=1, step=1, key="id_empresa_fat_add")
            faturamento_mensal = st.number_input("Faturamento Mensal", min_value=0.01, key="faturamento_mensal_add")
            faturamento_anual = st.number_input("Faturamento Anual", min_value=0.01, key="faturamento_anual_add")
            submit_add = st.form_submit_button("Adicionar Faturamento")

            if submit_add:
                add_url = f"{API_BASE_URL}/api/faturamento/"
                add_data = {
                    "id_empresa": int(id_empresa),
                    "faturamento_mensal": float(faturamento_mensal),
                    "faturamento_anual": float(faturamento_anual)
                }
                try:
                    response = requests.post(add_url, headers=headers, json=add_data)
                    if response.status_code == 200:
                        st.success(f"Faturamento adicionado para a empresa {id_empresa} com sucesso!")
                    else:
                        st.error(f"Erro ao adicionar faturamento: {response.status_code} - {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Erro de conexão com a API.")
    
    with update_tab:
        st.subheader("Atualizar Faturamento Existente")
        with st.form(key="update_faturamento_form"):
            id_faturamento_update = st.number_input("ID do Faturamento", min_value=1, step=1, key="id_faturamento_update")
            id_empresa_update = st.number_input("Novo ID da Empresa", min_value=1, step=1, key="id_empresa_fat_update")
            faturamento_mensal_update = st.number_input("Novo Faturamento Mensal", min_value=0.01, key="faturamento_mensal_update")
            faturamento_anual_update = st.number_input("Novo Faturamento Anual", min_value=0.01, key="faturamento_anual_update")
            submit_update = st.form_submit_button("Atualizar Faturamento")

            if submit_update:
                update_url = f"{API_BASE_URL}/api/faturamento/{id_faturamento_update}"
                update_data = {}
                if id_empresa_update:
                    update_data["id_empresa"] = int(id_empresa_update)
                if faturamento_mensal_update:
                    update_data["faturamento_mensal"] = float(faturamento_mensal_update)
                if faturamento_anual_update:
                    update_data["faturamento_anual"] = float(faturamento_anual_update)
                
                try:
                    response = requests.put(update_url, headers=headers, json=update_data)
                    if response.status_code == 200:
                        st.success(f"Faturamento com ID {id_faturamento_update} atualizado com sucesso!")
                    else:
                        st.error(f"Erro ao atualizar faturamento: {response.status_code} - {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Erro de conexão com a API.")
