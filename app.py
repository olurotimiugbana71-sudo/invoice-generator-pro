"""
Invoice Generator Pro - Main Application
Copyright 2026 ApexDynamics Solutions | Built by Rotimi Ugbana
"""
import streamlit as st

st.set_page_config(
    page_title="Invoice Generator Pro | ApexDynamics Solutions",
    page_icon="🧾",
    layout="wide"
)

import pandas as pd
from datetime import datetime, timedelta
from invoice_engine import InvoiceEngine
from visualizer import Visualizer
from report_builder import ReportBuilder
from license_gen import LicenseManager
import base64

COMPANY = "ApexDynamics Solutions"
DEVELOPER = "Rotimi Ugbana"
YEAR = "2026"
VERSION = "v1.3"

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .item-header {
        background: #16213E;
        padding: 10px 15px;
        border-radius: 8px;
        margin: 5px 0;
        color: white;
        font-weight: 600;
    }
    .preview-banner {
        background: #fff3cd;
        border: 2px solid #ffc107;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def init_components():
    return InvoiceEngine(), Visualizer(), ReportBuilder(), LicenseManager()

engine, visualizer, report_builder, license_mgr = init_components()

if 'licensed' not in st.session_state:
    st.session_state.licensed = False

# Sidebar
with st.sidebar:
    st.markdown(f"## {COMPANY}")
    st.markdown("### 💰 Pricing")
    
    with st.expander("Full Access License - N15,000", expanded=True):
        st.write("✓ Create Invoices")
        st.write("✓ PDF Export")
        st.write("✓ Financial Dashboard")
        st.write("✓ Print-Ready Formats")
        st.write("✓ 1-Year License")
    
    st.markdown("---")
    st.markdown("### 🔑 License Activation")
    
    lic_key = st.text_input("License Key", placeholder="INV-XXXX-XXXX-XXXX")
    lic_email = st.text_input("Email", placeholder="you@email.com")
    
    if st.button("Activate License", type="primary"):
        valid, msg = license_mgr.validate(lic_key, lic_email)
        if valid:
            st.success(f"✅ {msg} - Full Access!")
            st.session_state.licensed = True
        else:
            st.error(f"❌ {msg}")
    
    if st.session_state.licensed:
        st.success("🔓 Licensed")
    else:
        st.info("🔒 Preview Mode")

# Main Content
st.markdown(f'<h1 class="main-header">🧾 Invoice Generator Pro</h1>', unsafe_allow_html=True)
st.markdown(f"### Professional Invoices + Financial Dashboard | {COMPANY}")

if not st.session_state.licensed:
    st.markdown("""
    <div class="preview-banner">
        <h3>🔒 PREVIEW MODE</h3>
        <p>Create invoices for free. <strong>Activate license</strong> to download PDFs and access the dashboard.</p>
        <p style="font-size:14px;">💰 Full Access: N15,000 (1-Year License)</p>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 Create Invoice", "📊 Dashboard", "📋 History"])

with tab1:
    st.markdown("### Create New Invoice")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### From (Your Business)")
        from_name = st.text_input("Business Name", COMPANY)
        from_email = st.text_input("Business Email", "contact@apexdynamics.com")
        from_address = st.text_area("Business Address", "Lagos, Nigeria")
    
    with col2:
        st.markdown("#### To (Client)")
        to_name = st.text_input("Client Name")
        to_email = st.text_input("Client Email")
        to_address = st.text_area("Client Address")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        due_date = st.date_input("Due Date", datetime.now() + timedelta(days=30))
    with col2:
        currency = st.selectbox("Currency", ["NGN", "USD", "EUR", "GBP"])
    with col3:
        tax_rate = st.number_input("Tax Rate (%)", 0.0, 50.0, 0.0, 0.5)
    
    st.markdown("---")
    st.markdown("#### Invoice Items")
    
    num_items = st.number_input("Number of Items", 1, 20, 1)
    
    items = []
    for i in range(int(num_items)):
        st.markdown(f'<div class="item-header">Item {i+1}</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            desc = st.text_input("Description", key=f"desc_{i}")
        with col2:
            qty = st.number_input("Qty", 1, 1000, 1, key=f"qty_{i}")
        with col3:
            rate = st.number_input("Rate", 0.0, 100000000.0, 0.0, key=f"rate_{i}", format="%.2f")
        with col4:
            amount = qty * rate
            st.text_input("Amount", value=f"{amount:,.2f}", key=f"amount_{i}", disabled=True)
        
        items.append({
            "description": desc, "quantity": qty, "rate": rate, "amount": amount
        })
    
    discount = st.number_input("Discount (%)", 0.0, 100.0, 0.0)
    notes = st.text_area("Notes", "Thank you for your business!")
    
    if st.button("Generate Invoice", type="primary", use_container_width=True):
        if to_name and to_email:
            data = {
                "due_date": due_date.strftime("%Y-%m-%d"),
                "from_name": from_name, "from_email": from_email, "from_address": from_address,
                "to_name": to_name, "to_email": to_email, "to_address": to_address,
                "items": items, "tax_rate": tax_rate, "discount": discount,
                "notes": notes, "currency": currency
            }
            invoice = engine.create_invoice(data)
            st.success(f"Invoice #{invoice['invoice_number']} created!")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Subtotal", f"{currency} {invoice['subtotal']:,.2f}")
            col2.metric("Discount", f"-{currency} {invoice['discount_amount']:,.2f}")
            col3.metric("Tax", f"{currency} {invoice['tax_amount']:,.2f}")
            col4.metric("TOTAL", f"{currency} {invoice['total']:,.2f}")
            
            if st.session_state.licensed:
                pdf_data = report_builder.generate_invoice_pdf(invoice)
                st.download_button("Download PDF Invoice", base64.b64decode(pdf_data), f"invoice_{invoice['invoice_number']}.pdf", "application/pdf", type="primary")
            else:
                st.info("Activate license (N15,000) to download PDF")
        else:
            st.error("Please fill in client details")

with tab2:
    st.markdown("### Financial Dashboard")
    summary = engine.get_financial_summary()
    
    if summary:
        st.components.v1.html(visualizer.summary_cards(summary), height=120)
        st.markdown("---")
        if summary['monthly']:
            trend_chart = visualizer.revenue_trend(summary['monthly'])
            st.components.v1.html(trend_chart, height=400)
    else:
        st.info("Create invoices to see your dashboard!")

with tab3:
    st.markdown("### Invoice History")
    if engine.invoices:
        for inv in reversed(engine.invoices[-10:]):
            with st.expander(f"Invoice #{inv['invoice_number']} - {inv['currency']} {inv['total']:,.2f}"):
                st.write(f"**Date:** {inv['date']} | **To:** {inv['to_name']} | **Items:** {len(inv['items'])}")
    else:
        st.info("No invoices yet.")

st.markdown("---")
st.markdown(f"<p style='text-align:center;'>© {YEAR} {COMPANY} | Built by {DEVELOPER} | {VERSION}</p>", unsafe_allow_html=True)