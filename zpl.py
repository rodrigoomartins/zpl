import streamlit as st
import requests
import shutil

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

with st.sidebar:
    st.subheader("Configurações da etiqueta")
    layout_etiquetas = st.selectbox(
        'Layout predefinidos',
        ('Personalizado','73x20', '45x20', '100x25'),

    )
    tamanhos_predefinidos = {
        "Personalizado": (1,1),
        "73x20": (73,20),
        "45x20": (45,20),
        "100x25": (100,25),
    }
    
    largura, altura = tamanhos_predefinidos[layout_etiquetas]

    if layout_etiquetas == "Personalizado":
        largura = st.number_input("Largura da etiqueta:",1,500,73)
        altura = st.number_input("Altura da etiqueta:",1,500,20)
    
    st.divider()
    dpi = st.number_input("Dpmm:",1,1000,8)
    

dpi_y = altura*dpi
dpi_x = largura*dpi
percent_y = 100/(dpi_y)
percent_x = 100/(dpi_x)
posicao_x_texto = "Posição X"
posicao_y_texto = "Posição Y"


def ajustar_valor_x(valor_x):
    return round(valor_x*(1/percent_x),1)

def ajustar_valor_y(valor_y):
    return round(valor_y*(1/percent_y))

def converter_imagem_zpl(imagem):
    url = "http://api.labelary.com/v1/graphics"
    files = {"file": (imagem.name, imagem.read(), imagem.type)}
    headers = {"Accept": "application/zpl"}
    response = requests.post(url, files=files, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        st.error(f"Erro ao converter imagem: {response.status.code}")
        return None

def remover_parametros_zpl(codigo_zpl):
    pos_inicio = codigo_zpl.find(f"^GFA")
    pos_fim = codigo_zpl.rfind("^XZ")
    return codigo_zpl[pos_inicio:pos_fim]

def limpar_tudo():
    st.session_state['input_campo1'] = ""
    st.session_state['input_campo2'] = ""
    st.session_state['input_campo3'] = ""
    st.session_state['input_campo4'] = ""
    st.session_state['input_campo5'] = ""
    st.session_state['input_tamanho'] = ""
    st.session_state['input_barcode'] = ""
    st.session_state['input_epc'] = ""

st.title("ZPL Edit")
st.text("Entradas personalizadas")
col001, col002 = st.columns([0.6,0.4])
with col001:
    with st.expander("Campo 1"):
        input_campo1 = st.text_input("Descrição:",placeholder="Digite a descrição do campo 1...",max_chars=50,key="input_campo1")
        col1_campo1, col2_campo1, col3_campo1 = st.columns(3)
        with col1_campo1:
            tamanho_campo1 = st.slider("Tamanho",0,200,18, key="tamanho_campo1")
        with col2_campo1:
            posicao_campo1_x = st.slider(posicao_x_texto,0,100,round(15*percent_x),key="posicao_campo1_x")
            posicao_campo1_x = ajustar_valor_x(posicao_campo1_x)
        with col3_campo1:
            posicao_campo1_y = st.slider(posicao_y_texto,0,100,round(5*percent_y),key="posicao_campo1_y")
            posicao_campo1_y = ajustar_valor_y(posicao_campo1_y)
    with st.expander("Campo 2"):
        input_campo2 = st.text_input("Descrição:", placeholder="Digite a descrição do campo 2...", max_chars=50,key="input_campo2")
        col1_campo2, col2_campo2, col3_campo2 = st.columns(3)
        with col1_campo2:
            tamanho_campo2 = st.slider("Tamanho",0,200,18, key="tamanho_campo2")
        with col2_campo2:
            posicao_campo2_x = st.slider(posicao_x_texto,0,100,round(15*percent_x), key="posicao_campo2_x")
            posicao_campo2_x = ajustar_valor_x(posicao_campo2_x)
        with col3_campo2:
            posicao_campo2_y = st.slider(posicao_y_texto,0,100,round(25*percent_y), key="posicao_campo2_y")
            posicao_campo2_y = ajustar_valor_y(posicao_campo2_y)
    with st.expander("Campo 3"):
        input_campo3 = st.text_input("Descrição:", placeholder="Digite a descrição do campo 3...", max_chars=50,key="input_campo3")
        col1_campo3, col2_campo3, col3_campo3 = st.columns(3)
        with col1_campo3:
            tamanho_campo3 = st.slider("Tamanho",0,200,18, key="tamanho_campo3")
        with col2_campo3:
            posicao_campo3_x = st.slider(posicao_x_texto,0,100,round(15*percent_x), key="posicao_campo3_x")
            posicao_campo3_x = ajustar_valor_x(posicao_campo3_x)
        with col3_campo3:
            posicao_campo3_y = st.slider(posicao_y_texto,0,100,round(25*percent_y), key="posicao_campo3_y")
            posicao_campo3_y = ajustar_valor_y(posicao_campo3_y)
    with st.expander("Campo 4"):
        input_campo4 = st.text_input("campo4", placeholder="Digite a descrição do campo 4...", max_chars=50,key="input_campo4")
        col1_campo4, col2_campo4, col3_campo4 = st.columns(3)
        with col1_campo4:
            tamanho_campo4 = st.slider("Tamanho",0,100,40, key = "tamanho_campo4")
        with col2_campo4:
            posicao_campo4_x = st.slider(posicao_x_texto,0,100,round(15*percent_x), key="posicao_campo4_x")
            posicao_campo4_x = ajustar_valor_x(posicao_campo4_x)
        with col3_campo4:
            posicao_campo4_y = st.slider(posicao_y_texto,0,100,round(60*percent_y), key="posicao_campo4_y")
            posicao_campo4_y = ajustar_valor_y(posicao_campo4_y)
    with st.expander("Campo 5"):
        input_campo5 = st.text_input("campo5:", placeholder="Digite uma mensagem...",max_chars=50,key="input_campo5")
        col1_campo5, col2_campo5, col3_campo5 = st.columns(3)
        with col1_campo5:
            tamanho_campo5 = st.slider("Tamanho",0,100,15, key = "tamanho_campo5")
        with col2_campo5:
            posicao_campo5_x = st.slider(posicao_x_texto,0,100,round(15*percent_x), key="posicao_campo5_x")
            posicao_campo5_x = ajustar_valor_x(posicao_campo5_x)
        with col3_campo5:
            posicao_campo5_y = st.slider(posicao_y_texto,0,100,round(100*percent_y), key="posicao_campo5_y")
            posicao_campo5_y = ajustar_valor_y(posicao_campo5_y)
    st.divider()
    st.text("Entradas predefinidas")
    with st.expander("Tamanho"):
        input_tamanho = st.text_input("Tamanho da peça:", placeholder="Digite o tamanho...",max_chars=3,key="input_tamanho")
        col1_tamanho, col2_tamanho, col3_tamanho = st.columns(3)
        with col1_tamanho:
            tamanho_tamanho = st.slider("Tamanho", -100,100,0,disabled=True, key="tamanho_tamanho")
        with col2_tamanho:
            posicao_tamanho_x = st.slider(posicao_x_texto,0,100,34, key="posicao_tamanho_x")
            posicao_tamanho_x = ajustar_valor_x(posicao_tamanho_x)
        with col3_tamanho:
            posicao_tamanho_y = st.slider(posicao_y_texto,0,100,26, key="posicao_tamanho_y")
            posicao_tamanho_y = ajustar_valor_y(posicao_tamanho_y)
    with st.expander("Código de Barras"):
        tipo_barcode = st.selectbox(
            'Tipo de código de barras',
            ('EAN-13', 'Code 128 (sem dígito verificador)')
        )
        input_barcode = st.text_input("Código de barras:", placeholder="Digite o código de barras...",max_chars=13,key="input_barcode")
        col1_barcode, col2_barcode, col3_barcode = st.columns(3)
        with col1_barcode:
            tamanho_barcode = st.slider("Tamanho",1,10,key="tamanho_barcode")
        with col2_barcode:
            posicao_barcode_x = st.slider(posicao_x_texto,0,100,round(370*percent_x),key="posicao_barcode_x")
            posicao_barcode_x = ajustar_valor_x(posicao_barcode_x)
        with col3_barcode:
            posicao_barcode_y = st.slider(posicao_y_texto,0,100,round(40*percent_y),key="posicao_barcode_y")
            posicao_barcode_y = ajustar_valor_y(posicao_barcode_y)
    with st.expander("EPC"):
        input_epc = st.text_input(label="EPC:", placeholder="Digite o EPC...", max_chars=24,key="input_epc")
        col1_epc, col2_epc, col3_epc = st.columns(3)
        with col1_epc:
            tamanho_epc = st.slider("Tamanho",0,100,18, key = "tamanho_epc")
        with col2_epc:
            posicao_epc_x = st.slider(posicao_x_texto,0,100,round(15*percent_x), key="posicao_epc_x")
            posicao_epc_x = ajustar_valor_x(posicao_epc_x)
        with col3_epc:
            posicao_epc_y = st.slider(posicao_y_texto,0,100,round(130*percent_y), key="posicao_epc_y")
            posicao_epc_y = ajustar_valor_y(posicao_epc_y)
    limpar = st.button("Limpar entradas", on_click=limpar_tudo)
    
    habilitar_qrcode = st.toggle("QRCode")
    if not habilitar_qrcode:
        qrcode_zpl = ""
    if habilitar_qrcode:
        opcao_1 = st.radio("",("EPC","Barcode"))
        if opcao_1 == "EPC":
            conteudo_qrcode = input_epc
        elif opcao_1 == "Barcode":
            conteudo_qrcode = input_barcode
        col43, col44, col45 = st.columns(3)
        with col43:
            tamanho_qrcode = st.slider("Tamanho",0,10,3,key="tamanho_qrcode")
        with col44:
            posicao_qrcode_x = st.slider(posicao_x_texto,0,100,key="posicao_qrcode_x")
            posicao_qrcode_x = ajustar_valor_x(posicao_qrcode_x)
        with col45:
            posicao_qrcode_y = st.slider(posicao_y_texto,0,100,round(10*percent_y),key="posicao_qrcode_y")
            posicao_qrcode_y = ajustar_valor_y(posicao_qrcode_y)
        qrcode_zpl = (f"""^FO{posicao_qrcode_x},{posicao_qrcode_y}^BQN,2,{tamanho_qrcode},Q,7^FDQR,{conteudo_qrcode}^FS
    ^XZ""")
    
        

    campo1 = (f"^FO{posicao_campo1_x},{posicao_campo1_y},^A0N,{tamanho_campo1}^FD{input_campo1}^FS")
    campo2 = (f"^FO{posicao_campo2_x},{posicao_campo2_y}^A0N,{tamanho_campo2},{tamanho_campo2}^FD{input_campo2}^FS")
    campo3 = (f"^FO{posicao_campo3_x},{posicao_campo3_y}^A0N,{tamanho_campo3},{tamanho_campo3}^FD{input_campo3}^FS")
    campo4 = (f"^FO{posicao_campo4_x},{posicao_campo4_y}^A0N,{tamanho_campo4},{tamanho_campo4}^FD{input_campo4}^FS")
    campo5 = (f"^FO{posicao_campo5_x},{posicao_campo5_y}^A0N,{tamanho_campo5},{tamanho_campo5}^FD{input_campo5}^FS")
    if not input_tamanho:
        tamanho = ("")
    else:
        tamanho = (f"""^FO{posicao_tamanho_x},{posicao_tamanho_y}^GB120,50,2^FS
    ^FO{posicao_tamanho_x+55},{posicao_tamanho_y+6}^ASN^FD{input_tamanho}^FS
    ^FO{posicao_tamanho_x+5},{posicao_tamanho_y+18}^AN,18,18^FDTAM^FS""")
    if not input_barcode:
        barcode = ("")
    elif tipo_barcode == 'EAN-13':
        barcode = (f"^BY{tamanho_barcode}^FO{posicao_barcode_x},{posicao_barcode_y}^BEN,60,Y,N^FD{input_barcode}^FS")
    elif tipo_barcode == 'Code 128 (sem dígito verificador)':
        barcode = (f"^BY{tamanho_barcode}^FO{posicao_barcode_x},{posicao_barcode_y}^BCN,60,Y,N,N,A^FD{input_barcode}^FS")
    epc = (f"^FO{posicao_epc_x},{posicao_epc_y}^A0N,{tamanho_epc},{tamanho_epc}^FD{input_epc}^FS")

    codigo_zpl_imagem = ""
    imagem_file = st.file_uploader("Adicione uma imagem (PNG):", type=['png'])
    if imagem_file is not None:
        codigo_zpl_imagem = converter_imagem_zpl(imagem_file)
        codigo_zpl_imagem = remover_parametros_zpl(codigo_zpl_imagem)
        if codigo_zpl_imagem is not None:
            st.success("Imagem convertida com sucesso!",icon="✅")
            col24, col25, col26 = st.columns(3)
            with col24:
                tamanho_imagem = st.slider("Tamanho",-100,100,0,key="tamanho_imagem")
            with col25:
                posicao_imagem_x = st.slider(posicao_x_texto,0,100,0,key="posicao_imagem_x")
                posicao_imagem_x = ajustar_valor_x(posicao_imagem_x)
            with col26:
                posicao_imagem_y = st.slider(posicao_y_texto,0,100,0,key="posicao_imagem_y")
                posicao_imagem_y = ajustar_valor_y(posicao_imagem_y)
            codigo_zpl_imagem = (f"^FO{posicao_imagem_x},{posicao_imagem_y}^FRD{codigo_zpl_imagem}")
        else:
            st.error("Erro ao converter a imagem.")
            codigo_zpl_imagem = ""


zpl  = f"""
    ^XA
    ^CI28
    ^RFW,H^FD{input_epc}^FS

    {campo1}
    {campo2}
    {campo3}
    {campo4}
    {campo5}    
    {tamanho}    
    {barcode}
    {epc}
    {qrcode_zpl}
    {codigo_zpl_imagem}
    ^XZ
    """

url = f'http://api.labelary.com/v1/printers/8dpmm/labels/{largura / 25.4}x{altura / 25.4}/0/'
files = {'file' : zpl}
response = requests.post(url, files = files, stream = True)

if response.status_code == 200:
    response.raw.decode_content = True
    with open('label.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
else:
    print('Erro: ' + response.text)


with col002:
    with st.expander("ZPL"):
        st.code(zpl)
        st.divider()
        st.text("Preview")
        st.caption(f"{largura} x {altura} (mm)")
        st.image('label.png')
        col34, col35 = st.columns(2)
        with col34:
            with open("label.png", "rb") as file:
                st.download_button(
                    label="Download",
                    data=file,
                    file_name="label.png",
                    mime="image/png",
                    type='primary'
                )
