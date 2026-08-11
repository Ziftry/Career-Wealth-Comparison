import numpy as np
import streamlit as st
import plotly.graph_objects as go


def getSalary (salaryMap, year):
    years = list(salaryMap.keys())
    salaries = list(salaryMap.values())
    return int(np.interp(year, years, salaries))

def afterTax(gross_income):
    # Standard deductions
    federal_standard_deduction = 15000
    ny_standard_deduction = 8000

    federal_taxable = max(0, gross_income - federal_standard_deduction)
    ny_taxable = max(0, gross_income - ny_standard_deduction)

    # Federal brackets 2025 (single filer)
    federal_brackets = [
        (11925,   0.10),
        (48475,   0.12),
        (103350,  0.22),
        (197300,  0.24),
        (250525,  0.32),
        (626350,  0.35),
        (float('inf'), 0.37)
    ]

    # NY State brackets 2025 (single filer)
    ny_brackets = [
        (8500,    0.04),
        (11700,   0.045),
        (13900,   0.0525),
        (80650,   0.055),
        (215400,  0.06),
        (1077550, 0.0685),
        (float('inf'), 0.0965)
    ]

    def calc_bracket_tax(income, brackets):
        tax = 0
        prev = 0
        for limit, rate in brackets:
            if income <= prev:
                break
            taxable_in_bracket = min(income, limit) - prev
            tax += taxable_in_bracket * rate
            prev = limit
        return tax

    federal_tax = calc_bracket_tax(federal_taxable, federal_brackets)
    ny_tax = calc_bracket_tax(ny_taxable, ny_brackets)

    # FICA (Social Security 6.2% up to $176,100 + Medicare 1.45%)
    social_security = min(gross_income, 176100) * 0.062
    medicare = gross_income * 0.0145

    total_tax = federal_tax + ny_tax + social_security + medicare
    net_income = gross_income - total_tax

    return round(net_income)

# actual UI:

# Title
st.set_page_config(page_title="Career Earnings Simulator", layout="wide")
st.title("Career Earnings Comparison")

colA, colB= st.columns(2)
with colA:
    career1Name = st.text_input("Career 1 Name", value="Engineer")
    eng_Debt = st.number_input("Student Loans ", value=0, step=5000)
    engDebtStart= st.number_input("Debt Interest Starts Year ", min_value=1, value=4, step=1)
    engDebtPay = st.number_input("Debt Payment Rate % ", min_value=0.0, max_value=100.0, value=33.0, step=1.0)
    engRepaymentStart = st.number_input("Repayment Start Year ", min_value=0, value=1, step=1)
    engInvestingRate = st.number_input("Investing Rate % ", min_value=0.0, value=33.0, step=1.0)

with colB:
    career2Name = st.text_input("Career 2 Name", value="Doctor")
    doc_Debt = st.number_input("Student Loans", value=235000, step=5000)
    docDebtStart= st.number_input("Debt Interest Starts Year", min_value=1, value=4, step=1)
    docDebtPay = st.number_input("Debt Payment Rate %", min_value=0.0, max_value=100.0, value=33.0, step=1.0)
    docRepaymentStart = st.number_input("Repayment Start Year", min_value=0, value=9, step=1)
    docInvestingRate = st.number_input("Investing Rate %", min_value=0.0, value=33.0, step=1.0)
 

st.divider()
colA, colB= st.columns(2)
with colA:
    investmentReturn = st.number_input("Annual Investment Return %", value=9.0, step=0.5)
with colB:
    debtInterest = st.number_input("Debt Interest Rate %", min_value=0.0, max_value=100.0, value=7.5, step=0.1)

colA, colB, colC= st.columns(3)
with colA:
    useTaxes = st.toggle("Include Taxes", value=True)
with colB:
    useInflation = st.toggle("Include Inflation", value=True)
with colC:
    useInvesting = st.toggle("Include Investing", value=True)


# Divider
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("Engineer Salary Checkpoints")

    if "engSalaries" not in st.session_state:
        st.session_state.engSalaries = [
            {"year": 1,  "salary": 70000},
            {"year": 3,  "salary": 90000},
            {"year": 5,  "salary": 115000},
            {"year": 10, "salary": 140000},
            {"year": 15, "salary": 180000},
            {"year": 20, "salary": 200000},
            {"year": 30, "salary": 250000},
            {"year": 40, "salary": 275000},
        ]

    for i, row in enumerate(st.session_state.engSalaries):
        c1, c2 = st.columns(2)        # <-- renamed
        with c1:
            st.session_state.engSalaries[i]["year"] = st.number_input(
    "Year", value=row["year"], min_value=1, max_value=80, step=1, key=f"eng_year_{i}")
        with c2:
            st.session_state.engSalaries[i]["salary"] = st.number_input(
    "Salary", value=row["salary"], min_value=0, max_value=1500000, step=1000, key=f"eng_sal_{i}")


    if st.button("+ Add Checkpoint", key="eng_add"):
        st.session_state.engSalaries.append({"year": 5, "salary": 95000})

    engSalaryMap = {row["year"]: row["salary"] for row in st.session_state.engSalaries}

with col2:
    st.subheader("Doctor Salary Checkpoints")

    if "docSalaries" not in st.session_state:
        st.session_state.docSalaries = [
            {"year": 1,  "salary": 0},
            {"year": 4,  "salary": 0},
            {"year": 5,  "salary": 68000},
            {"year": 8,  "salary": 80000},
            {"year": 9,  "salary": 235000},
            {"year": 15, "salary": 280000},
            {"year": 25, "salary": 320000},
            {"year": 40, "salary": 450000},
        ]

    for i, row in enumerate(st.session_state.docSalaries):
        c1, c2 = st.columns(2)        # <-- renamed
        with c1:
            st.session_state.docSalaries[i]["year"] = st.number_input(
            f"Year", value=row["year"], min_value=1, max_value=80, step=1, key=f"doc_year_{i}")
        with c2:
            st.session_state.docSalaries[i]["salary"] = st.number_input(
            f"Salary", value=row["salary"], min_value=0, max_value=1500000, step=1000, key=f"doc_sal_{i}")

    if st.button("+ Add Checkpoint", key="doc_add"):
        st.session_state.docSalaries.append({"year": 15, "salary": 260000})

    docSalaryMap = {row["year"]: row["salary"] for row in st.session_state.docSalaries}




# Button to run simulation
if st.button("Run Simulation"):

    #Engineer
    engSalary = 0
    engTakeHome = 0
    engEarningCum = 0
    engWorth = 0
    engTaxed = 0
    engInvested = 0
    engDebtPaid = 0
    engDebt = eng_Debt
    if engDebt == 0: engDebtPaidYear = 0 
    else: engDebtPaidYear = -1

    #doc
    docSalary = 0
    docTakeHome = 0
    docEarningCum = 0
    docWorth = 0
    docTaxed = 0
    docDebtPaid = 0
    docInvested = 0
    docDebt = doc_Debt
    if docDebt == 0: docDebtPaidYear = 0 
    else: docDebtPaidYear = -1

    # Lists to store data for graph
    yearsList = []
    
    engSalaryList = []
    engEarningCumList = []
    engWorthList = []
    engDebtList = []

    docSalaryList = []
    docEarningCumList = []
    docWorthList = []
    docDebtList = []

    for year in range (1, 41):

        #eng calculations:
        if useInvesting: 
            engInvested *= (1 + (investmentReturn/100))
        if useInflation:
            engWorth *= 1.03

        engSalary = getSalary(engSalaryMap, year)
        engEarningCum += engSalary
        engTakeHome = afterTax(engSalary) if useTaxes else engSalary
        engTaxed += engSalary - engTakeHome
        engWorth += engTakeHome

        engDebtPayment = 0
        if year >= engDebtStart:
            engDebt *= (1 + debtInterest/100)
        if year >= engRepaymentStart and engDebt > 0:
            engDebtPayment = min((engDebtPay/100) * engTakeHome, engDebt)
            engDebt -= engDebtPayment
            engDebtPaid += engDebtPayment
            engWorth -= engDebtPayment
            if engDebt == 0: engDebtPaidYear = year
        if engDebt == 0:
            engInvested += engTakeHome * engInvestingRate/100
            engWorth -= engTakeHome * engInvestingRate/100

        #doc calculations:
        if useInvesting: 
            docInvested *= (1 + (investmentReturn/100))
        if useInflation:
            docWorth *= 1.03
            
        docSalary = getSalary(docSalaryMap, year)
        docEarningCum += docSalary
        docTakeHome = afterTax(docSalary) if useTaxes else docSalary
        docTaxed += docSalary - docTakeHome
        docWorth += docTakeHome

        docDebtPayment = 0
        if year >= docDebtStart:
            docDebt *= (1 + debtInterest/100)
        if year >= docRepaymentStart and docDebt > 0:
            docDebtPayment = min((docDebtPay/100) * docTakeHome, docDebt)
            docDebt -= docDebtPayment
            docDebtPaid += docDebtPayment
            docWorth -= docDebtPayment
            if docDebt == 0: docDebtPaidYear = year
        if docDebt == 0:
            docInvested += docTakeHome * docInvestingRate/100
            docWorth -= docTakeHome * docInvestingRate/100

        # Store values for graphing
        yearsList.append(year)

        engSalaryList.append(engSalary)
        engEarningCumList.append(engEarningCum)
        engWorthList.append(engWorth + engInvested - engDebt)
        engDebtList.append(engDebt)

        docSalaryList.append(docSalary)
        docEarningCumList.append(docEarningCum)
        docWorthList.append(docWorth + docInvested - docDebt)
        docDebtList.append(docDebt)


    # GRAPHING NOW
        # Net Worth Chart
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=yearsList, y=engWorthList, name=career1Name))
    fig1.add_trace(go.Scatter(x=yearsList, y=docWorthList, name=career2Name))
    fig1.update_layout(
        title="Net Worth Over Time",
        xaxis_title="Year",
        yaxis_title="Net Worth ($)",
        hovermode="x unified",
        yaxis=dict(tickformat="$,.0f")
    )
    fig1.update_traces(hovertemplate="%{y:$,.0f}")

    st.plotly_chart(fig1, use_container_width=True)

    # Salary Chart
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=yearsList, y=engSalaryList, name=career1Name))
    fig2.add_trace(go.Scatter(x=yearsList, y=docSalaryList, name=career2Name))
    fig2.update_layout(
        title="Salary Over Time",
        xaxis_title="Year",
        yaxis_title="Salary ($)",
        hovermode="x unified",
        yaxis=dict(tickformat="$,.0f")
    )
    fig2.update_traces(hovertemplate="%{y:$,.0f}")
    st.plotly_chart(fig2, use_container_width=True)


    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=yearsList, y=engEarningCumList, name=career1Name))
    fig3.add_trace(go.Scatter(x=yearsList, y=docEarningCumList, name=career2Name))
    fig3.update_layout(
        title="Cumulative Earnings Over Time",
        xaxis_title="Year",
        yaxis_title="Total Earned ($)",
        hovermode="x unified",
        yaxis=dict(tickformat="$,.0f")
    )
    fig3.update_traces(hovertemplate="%{y:$,.0f}")
    st.plotly_chart(fig3, use_container_width=True)


    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=yearsList, y=engDebtList, name=career1Name))
    fig4.add_trace(go.Scatter(x=yearsList, y=docDebtList, name=career2Name))
    fig4.update_layout(
        title="Debt Remaining Over Time",
        xaxis_title="Year",
        yaxis_title="Debt ($)",
        hovermode="x unified",
        yaxis=dict(tickformat="$,.0f")
    )
    fig4.update_traces(hovertemplate="%{y:$,.0f}")
    st.plotly_chart(fig4, use_container_width=True)



    # Summary stats
    st.divider()
    x = 0
    for i in range(1, len(engWorthList)):
        if docWorthList[i] > engWorthList[i] and docWorthList[i-1] <= engWorthList[i-1]:
            st.info(f"💡 {career2Name} surpasses {career1Name} in net worth at year {yearsList[i]}")
            x = 1
    if x == 0:
        st.info(f"💡 {career2Name} never surpasses {career1Name} in net worth!")

    s1, s2 = st.columns(2)
    with s1:
        st.metric(f"{career1Name} Final Net Worth", f"${engWorth + engInvested - engDebt:,.0f}")
        st.metric(f"{career1Name} Total Earned", f"${engEarningCum:,.0f}")
        st.metric(f"{career1Name} Total Taxed", f"${engTaxed:,.0f}")
        st.metric(f"{career1Name} Total Debt Paid", f"${engDebtPaid:,.0f}")
        if engDebtPaidYear != -1:
            st.metric(f"{career1Name} Debt Paid Off", f"Year {engDebtPaidYear}")
        else:
            st.info(f"{career1Name} still has debt after 40 years")    

    with s2:
        st.metric(f"{career2Name} Final Net Worth", f"${docWorth + docInvested - docDebt:,.0f}")
        st.metric(f"{career2Name} Total Earned", f"${docEarningCum:,.0f}")
        st.metric(f"{career2Name} Total Taxed", f"${docTaxed:,.0f}")
        st.metric(f"{career2Name} Total Debt Paid", f"${docDebtPaid:,.0f}")
        if docDebtPaidYear != -1:
            st.metric(f"{career2Name} Debt Paid Off", f"Year {docDebtPaidYear}")
        else:
            st.info(f"{career2Name} still has debt after 40 years")

