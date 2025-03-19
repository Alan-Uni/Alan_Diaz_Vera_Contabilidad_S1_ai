import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Sistema Contable Básico")

st.markdown(
    """
    <style>
    .stDataFrame {
        background-color: #001F3F; /* Azul oscuro */
        color: #FFD700; /* Dorado */
    }
    .stDataFrame th {
        background-color: #001F3F; /* Azul oscuro */
        color: #FFD700; /* Dorado */
    }
    .stDataFrame td {
        background-color: #001F3F; /* Azul oscuro */
        color: #FFD700; /* Dorado */
    }
    .stDataFrame {
        width: 100%; /* Extender el tamaño de las tablas */
    }
    </style>
    """,
    unsafe_allow_html=True
)

if 'transacciones' not in st.session_state:
    st.session_state.transacciones = []

if 'balances' not in st.session_state:
    st.session_state.balances = {
        "Activo": {"Caja": 0, "Bancos": 0, "Mercancías": 0, "Terrenos": 0, "Edificios": 0, "Equipo de cómputo": 0, "Mobiliario y equipo": 0, "Muebles y enseres": 0, "IVA pagado": 0, "Rentas pagadas por anticipado": 0, "Anticipo de clientes": 0, "Equipo de transporte": 0,"Papelería": 0},
        "Pasivo": {"Acreedores": 0, "Documentos por pagar": 0, "IVA por acreditar": 0, "IVA trasladado": 0},
        "Capital": {"Capital Social": 0}
    }

if 'libro_mayor' not in st.session_state:
    st.session_state.libro_mayor = {}

def mostrar_balance_general():
    st.subheader("Balance General")
    st.write("### Activo")
    activo_df = pd.DataFrame.from_dict(st.session_state.balances["Activo"], orient="index", columns=["Monto"])
    activo_df["Monto"] = activo_df["Monto"].abs() 
    st.dataframe(activo_df)

    st.write("### Pasivo")
    pasivo_df = pd.DataFrame.from_dict(st.session_state.balances["Pasivo"], orient="index", columns=["Monto"])
    pasivo_df["Monto"] = pasivo_df["Monto"].abs()  
    st.dataframe(pasivo_df)

    st.write("### Capital")
    capital_df = pd.DataFrame.from_dict(st.session_state.balances["Capital"], orient="index", columns=["Monto"])
    capital_df["Monto"] = capital_df["Monto"].abs() 
    st.dataframe(capital_df)

def actualizar_balances(transaccion):
    for cuenta, monto in transaccion["cargos"].items():
        if cuenta in st.session_state.balances["Activo"]:
            st.session_state.balances["Activo"][cuenta] += monto
        elif cuenta in st.session_state.balances["Pasivo"]:
            st.session_state.balances["Pasivo"][cuenta] += monto
        elif cuenta in st.session_state.balances["Capital"]:
            st.session_state.balances["Capital"][cuenta] += monto

        if cuenta not in st.session_state.libro_mayor:
            st.session_state.libro_mayor[cuenta] = {"Cargos": [], "Abonos": []}
        st.session_state.libro_mayor[cuenta]["Cargos"].append(monto)

    for cuenta, monto in transaccion["abonos"].items():
        if cuenta in st.session_state.balances["Activo"]:
            st.session_state.balances["Activo"][cuenta] -= monto
        elif cuenta in st.session_state.balances["Pasivo"]:
            st.session_state.balances["Pasivo"][cuenta] -= monto
        elif cuenta in st.session_state.balances["Capital"]:
            st.session_state.balances["Capital"][cuenta] -= monto

        if cuenta not in st.session_state.libro_mayor:
            st.session_state.libro_mayor[cuenta] = {"Cargos": [], "Abonos": []}
        st.session_state.libro_mayor[cuenta]["Abonos"].append(monto)

option = st.sidebar.selectbox(
    "Selecciona una operación",
    ["Asiento de apertura", "Compra en efectivo", "Compra a crédito", "Compra combinada", "Anticipo de clientes", "Compra de papelería", "Pago de rentas anticipadas"]
)

def registrar_transaccion(transaccion):
    transaccion["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
    st.session_state.transacciones.append(transaccion)
    actualizar_balances(transaccion)
    st.success("Transacción registrada correctamente.")

mostrar_balance_general()

if option == "Asiento de apertura":
    st.subheader("Asiento de Apertura")
    caja = st.number_input("Caja", value=50000)
    bancos = st.number_input("Bancos", value=1500000)
    mercancias = st.number_input("Mercancías", value=500000)
    terrenos = st.number_input("Terrenos", value=500000)
    edificios = st.number_input("Edificios", value=1000000)
    eq_computo = st.number_input("Equipo de cómputo", value=150000)
    mob_equipo = st.number_input("Mobiliario y equipo", value=70000)
    muebles_enseres = st.number_input("Muebles y enseres", value=30000)
    capital_social = st.number_input("Capital Social", value=3800000)

    if st.button("Registrar Asiento de Apertura"):
        transaccion = {
            "tipo": "Asiento de apertura",
            "cargos": {
                "Caja": caja,
                "Bancos": bancos,
                "Mercancías": mercancias,
                "Terrenos": terrenos,
                "Edificios": edificios,
                "Equipo de cómputo": eq_computo,
                "Mobiliario y equipo": mob_equipo,
                "Muebles y enseres": muebles_enseres
            },
            "abonos": {
                "Capital Social": capital_social
            }
        }
        registrar_transaccion(transaccion)

elif option == "Compra en efectivo":
    st.subheader("Compra en Efectivo")
    mercancias = st.number_input("Mercancías", value=15000)
    iva = st.number_input("IVA", value=2400)
    caja = st.number_input("Caja", value=17400)

    if st.button("Registrar Compra en Efectivo"):
        transaccion = {
            "tipo": "Compra en efectivo",
            "cargos": {
                "Mercancías": mercancias,
                "IVA pagado": iva
            },
            "abonos": {
                "Caja": caja
            }
        }
        registrar_transaccion(transaccion)

elif option == "Compra a crédito":
    st.subheader("Compra a Crédito")
    equipo_transporte = st.number_input("Equipo de transporte", value=500000)
    iva = st.number_input("IVA", value=80000)
    acreedores = st.number_input("Acreedores", value=580000)

    if st.button("Registrar Compra a Crédito"):
        transaccion = {
            "tipo": "Compra a crédito",
            "cargos": {
                "Equipo de transporte": equipo_transporte,
                "IVA por acreditar": iva
            },
            "abonos": {
                "Acreedores": acreedores
            }
        }
        registrar_transaccion(transaccion)

elif option == "Compra combinada":
    st.subheader("Compra Combinada")
    mercancias = st.number_input("Mercancías", value=20000)
    iva = st.number_input("IVA", value=1600)
    ivaA= st.number_input("IVA por acreditar", value=1600)
    caja = st.number_input("Caja (pago en efectivo)", value=11600)
    documentos_por_pagar = st.number_input("Documentos por pagar (crédito)", value=11600)

    if st.button("Registrar Compra Combinada"):
        transaccion = {
            "tipo": "Compra combinada",
            "cargos": {
                "Mercancías": mercancias,
                "IVA pagado": iva,
                "IVA por acreditar": ivaA
            },
            "abonos": {
                "Caja": caja,
                "Documentos por pagar": documentos_por_pagar
            }
        }
        registrar_transaccion(transaccion)

elif option == "Anticipo de clientes":
    st.subheader("Anticipo de Clientes")
    anticipo = st.number_input("Anticipo de clientes", value=8000)
    iva = st.number_input("IVA", value=1280)
    caja = st.number_input("Caja", value=9280)

    if st.button("Registrar Anticipo de Clientes"):
        transaccion = {
            "tipo": "Anticipo de clientes",
            "cargos": {
                "Caja": caja
            },
            "abonos": {
                "Anticipo de clientes": anticipo,
                "IVA trasladado": iva
            }
        }
        registrar_transaccion(transaccion)

elif option == "Compra de papelería":
    st.subheader("Compra de Papelería")
    papelería = st.number_input("Papelería", value=800)
    iva = st.number_input("IVA", value=128)
    caja = st.number_input("Caja", value=928)

    if st.button("Registrar Compra de Papelería"):
        transaccion = {
            "tipo": "Compra de papelería",
            "cargos": {
                "Papelería": papelería,
                "IVA pagado": iva
            },
            "abonos": {
                "Caja": caja
            }
        }
        registrar_transaccion(transaccion)

elif option == "Pago de rentas anticipadas":
    st.subheader("Pago de Rentas Anticipadas")
    rentas = st.number_input("Rentas pagadas por anticipado", value=6250)
    iva = st.number_input("IVA", value=1000)
    caja = st.number_input("Caja", value=7250)

    if st.button("Registrar Pago de Rentas Anticipadas"):
        transaccion = {
            "tipo": "Pago de rentas anticipadas",
            "cargos": {
                "Rentas pagadas por anticipado": rentas,
                "IVA pagado": iva
            },
            "abonos": {
                "Caja": caja
            }
        }
        registrar_transaccion(transaccion)

st.subheader("Libro Diario")
for transaccion in st.session_state.transacciones:
    st.write(f"**Transacción:** {transaccion['tipo']} - **Fecha:** {transaccion['fecha']}")
    
    cargos = pd.DataFrame.from_dict(transaccion["cargos"], orient="index", columns=["Monto"])
    cargos["Monto"] = cargos["Monto"].abs()  
    
    abonos = pd.DataFrame.from_dict(transaccion["abonos"], orient="index", columns=["Monto"])
    abonos["Monto"] = abonos["Monto"].abs()  
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Cargos**")
        st.dataframe(cargos)
    with col2:
        st.write("**Abonos**")
        st.dataframe(abonos)
    st.write("---")

st.subheader("Balanza de Comprobación")
balanza = {
    "Cuenta": list(st.session_state.balances["Activo"].keys()) + list(st.session_state.balances["Pasivo"].keys()) + list(st.session_state.balances["Capital"].keys()),
    "Debe": [abs(st.session_state.balances["Activo"].get(cuenta, 0)) for cuenta in st.session_state.balances["Activo"]] + [abs(st.session_state.balances["Pasivo"].get(cuenta, 0)) for cuenta in st.session_state.balances["Pasivo"]] + [abs(st.session_state.balances["Capital"].get(cuenta, 0)) for cuenta in st.session_state.balances["Capital"]],
    "Haber": [abs(st.session_state.balances["Activo"].get(cuenta, 0)) for cuenta in st.session_state.balances["Activo"]] + [abs(st.session_state.balances["Pasivo"].get(cuenta, 0)) for cuenta in st.session_state.balances["Pasivo"]] + [abs(st.session_state.balances["Capital"].get(cuenta, 0)) for cuenta in st.session_state.balances["Capital"]]
}

balanza_df = pd.DataFrame(balanza)

total_debe = balanza_df["Debe"].sum()
total_haber = balanza_df["Haber"].sum()

st.dataframe(balanza_df)

st.write(f"**Total Debe:** {total_debe}")
st.write(f"**Total Haber:** {total_haber}")

st.subheader("Libro Mayor")

for cuenta, movimientos in st.session_state.libro_mayor.items():
    st.write(f"**Cuenta:** {cuenta}")
    
    cargos = [abs(monto) for monto in movimientos["Cargos"]]  
    abonos = [abs(monto) for monto in movimientos["Abonos"]]  
    
    data = []
    
    for i, cargo in enumerate(cargos):
        data.append({"Movimiento": f"Cargo {i+1}", "Monto": cargo, "Tipo": "Cargo"})
    
    for i, abono in enumerate(abonos):
        data.append({"Movimiento": f"Abono {i+1}", "Monto": abono, "Tipo": "Abono"})
    
    df_cuenta = pd.DataFrame(data)
    
    total_cargos = sum(cargos)
    total_abonos = sum(abonos)
    diferencia = total_cargos - total_abonos
    if diferencia > 0:
        mayor = "Cargos"
    elif diferencia < 0:
        mayor = "Abonos"
    else:
        mayor = "Iguales"
    
    df_totales = pd.DataFrame({
        "Movimiento": ["Totales"],
        "Monto": [abs(diferencia)],
        "Tipo": [mayor]
    })
    
    df_final = pd.concat([df_cuenta, df_totales], ignore_index=True)
    
    st.dataframe(df_final)
    st.write("---")