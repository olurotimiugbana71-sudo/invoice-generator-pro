"""
Invoice Generator Pro - Main Application with Reliable Print
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
VERSION = "v1.2"

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
    .success-box {
        background: #e8f5e9;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
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
    
    with st.expander("🥉 Basic - $9.99"):
        st.write("✓ Create Invoices")
        st.write("✓ PDF Export")
        st.write("✓ 10 Invoices/Month")
    
    with st.expander("🥈 Standard - $24.99 ⭐"):
        st.write("✓ Everything in Basic")
        st.write("✓ Financial Dashboard")
        st.write("✓ Unlimited Invoices")
        st.write("✓ Client Management")
    
    with st.expander("🥇 Premium - $49.99 👑"):
        st.write("✓ Everything in Standard")
        st.write("✓ Custom Branding")
        st.write("✓ Priority Support")
        st.write("✓ Bulk Operations")
    
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
        st.success("🔓 Licensed - Full Access")
    else:
        st.info("🔒 Preview Mode")

# Main Content
st.markdown(f'<h1 class="main-header">🧾 Invoice Generator Pro</h1>', unsafe_allow_html=True)
st.markdown(f"### Professional Invoices + Financial Dashboard | {COMPANY}")

# Tabs
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
    st.markdown("*(Amount is auto-calculated: Qty × Rate)*")
    
    num_items = st.number_input("Number of Items", 1, 20, 1)
    
    items = []
    for i in range(int(num_items)):
        st.markdown(f'<div class="item-header">📦 Item {i+1}</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            desc = st.text_input("Description", key=f"desc_{i}", placeholder=f"Item {i+1} description")
        with col2:
            qty = st.number_input("Qty", 1, 1000, 1, key=f"qty_{i}")
        with col3:
            rate = st.number_input("Rate", 0.0, 100000000.0, 0.0, key=f"rate_{i}", format="%.2f")
        with col4:
            amount = qty * rate
            st.text_input("Amount", value=f"{amount:,.2f}", key=f"amount_{i}", disabled=True)
        
        items.append({
            "description": desc,
            "quantity": qty,
            "rate": rate,
            "amount": amount
        })
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        discount = st.number_input("Discount (%)", 0.0, 100.0, 0.0)
    with col2:
        notes = st.text_area("Notes", "Thank you for your business!")
    
    if st.button("🧾 Generate Invoice", type="primary", use_container_width=True):
        if to_name and to_email:
            data = {
                "due_date": due_date.strftime("%Y-%m-%d"),
                "from_name": from_name,
                "from_email": from_email,
                "from_address": from_address,
                "to_name": to_name,
                "to_email": to_email,
                "to_address": to_address,
                "items": items,
                "tax_rate": tax_rate,
                "discount": discount,
                "notes": notes,
                "currency": currency
            }
            
            invoice = engine.create_invoice(data)
            
            st.markdown("---")
            st.markdown(f"""
            <div class="success-box">
                <h3>✅ Invoice #{invoice['invoice_number']} Created!</h3>
                <p>Subtotal: {currency} {invoice['subtotal']:,.2f} | 
                Total: <strong>{currency} {invoice['total']:,.2f}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Invoice Summary
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Subtotal", f"{currency} {invoice['subtotal']:,.2f}")
            col2.metric("Discount", f"-{currency} {invoice['discount_amount']:,.2f}")
            col3.metric("Tax", f"{currency} {invoice['tax_amount']:,.2f}")
            col4.metric("TOTAL", f"{currency} {invoice['total']:,.2f}")
            
            st.markdown("---")
            st.markdown("### 📥 Download & Print Options")
            
            if st.session_state.licensed:
                # Generate PDF
                pdf_data = report_builder.generate_invoice_pdf(invoice)
                
                # Generate Print-Ready HTML
                print_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Invoice {invoice['invoice_number']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 30px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #667EEA, #764BA2); color: white; padding: 25px; border-radius: 10px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; }}
        .header p {{ margin: 5px 0; opacity: 0.9; }}
        .info-section {{ display: flex; justify-content: space-between; margin: 25px 0; }}
        .info-box h3 {{ color: #667EEA; margin-bottom: 8px; }}
        .info-box p {{ margin: 3px 0; color: #555; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #667EEA; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 12px; border-bottom: 1px solid #eee; }}
        .totals {{ text-align: right; margin: 25px 0; }}
        .totals p {{ margin: 5px 0; font-size: 15px; }}
        .grand-total {{ font-size: 22px; font-weight: bold; color: #667EEA; }}
        .notes {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0; }}
        .print-btn {{ background: #667EEA; color: white; padding: 15px 30px; border: none; border-radius: 25px; font-size: 18px; cursor: pointer; display: block; margin: 20px auto; }}
        .print-btn:hover {{ background: #764BA2; }}
        @media print {{ 
            .print-btn {{ display: none; }} 
            body {{ background: white; margin: 0; }}
            .container {{ box-shadow: none; max-width: 100%; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧾 INVOICE</h1>
            <p>#{invoice['invoice_number']}</p>
            <p>{invoice['from_name']} | {invoice['from_email']}</p>
        </div>
        <div class="info-section">
            <div class="info-box">
                <h3>FROM:</h3>
                <p><strong>{invoice['from_name']}</strong></p>
                <p>{invoice['from_email']}</p>
                <p>{invoice['from_address']}</p>
            </div>
            <div class="info-box" style="text-align:right;">
                <h3>TO:</h3>
                <p><strong>{invoice['to_name']}</strong></p>
                <p>{invoice['to_email']}</p>
                <p>{invoice['to_address']}</p>
            </div>
        </div>
        <p style="text-align:center;color:#555;">
            <strong>Date:</strong> {invoice['date']} | 
            <strong>Due:</strong> {invoice['due_date']} | 
            <strong>Currency:</strong> {invoice['currency']}
        </p>
        <table>
            <tr><th>Description</th><th>Qty</th><th>Rate</th><th>Amount</th></tr>"""
                
                for item in invoice['items']:
                    print_html += f"""
            <tr><td>{item['description']}</td><td>{item['quantity']}</td><td>{invoice['currency']} {item['rate']:,.2f}</td><td>{invoice['currency']} {item['amount']:,.2f}</td></tr>"""
                
                print_html += f"""
        </table>
        <div class="totals">
            <p>Subtotal: {invoice['currency']} {invoice['subtotal']:,.2f}</p>
            <p>Discount: -{invoice['currency']} {invoice['discount_amount']:,.2f}</p>
            <p>Tax: {invoice['currency']} {invoice['tax_amount']:,.2f}</p>
            <p class="grand-total">TOTAL: {invoice['currency']} {invoice['total']:,.2f}</p>
        </div>
        <div class="notes">
            <h3>Notes:</h3>
            <p>{invoice['notes']}</p>
        </div>
        <p style="text-align:center;color:#999;font-size:12px;margin-top:30px;">
            Generated by Invoice Generator Pro | © 2026 {COMPANY}
        </p>
        <button class="print-btn" onclick="window.print()">🖨️ Print Invoice</button>
    </div>
</body>
</html>"""
                
                # Download buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        "📥 Download PDF",
                        base64.b64decode(pdf_data),
                        f"invoice_{invoice['invoice_number']}.pdf",
                        "application/pdf",
                        type="primary",
                        use_container_width=True
                    )
                
                with col2:
                    st.download_button(
                        "🖨️ Download Print-Ready HTML",
                        print_html,
                        f"print_invoice_{invoice['invoice_number']}.html",
                        "text/html",
                        type="primary",
                        use_container_width=True
                    )
                
                st.info("💡 **To Print:** Download the HTML file, open it in your browser, then click 'Print Invoice' or press **Ctrl+P**. The PDF can also be printed directly.")
            else:
                st.info("🔒 Activate license to download PDF and print invoices")
        else:
            st.error("Please fill in client details")

with tab2:
    st.markdown("### 📊 Financial Dashboard")
    
    summary = engine.get_financial_summary()
    
    if summary:
        st.components.v1.html(visualizer.summary_cards(summary), height=120)
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if summary['monthly']:
                st.markdown("#### Revenue Trend")
                trend_chart = visualizer.revenue_trend(summary['monthly'])
                st.components.v1.html(trend_chart, height=400)
        with col2:
            if summary['top_clients']:
                st.markdown("#### Top Clients")
                client_chart = visualizer.top_clients_chart(summary['top_clients'])
                st.image(f"data:image/png;base64,{client_chart}", width=600)
    else:
        st.info("Create invoices to see your financial dashboard!")

with tab3:
    st.markdown("### 📋 Invoice History")
    
    if engine.invoices:
        for inv in reversed(engine.invoices[-10:]):
            with st.expander(f"📄 Invoice #{inv['invoice_number']} - {inv['currency']} {inv['total']:,.2f}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Date:** {inv['date']}")
                    st.write(f"**Due:** {inv['due_date']}")
                    st.write(f"**From:** {inv['from_name']}")
                with col2:
                    st.write(f"**To:** {inv['to_name']}")
                    st.write(f"**Items:** {len(inv['items'])}")
                    st.write(f"**Status:** {inv['status']}")
    else:
        st.info("No invoices yet. Create your first invoice!")

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:#666;">
    <p><strong>Invoice Generator Pro {VERSION}</strong></p>
    <p>© {YEAR} {COMPANY} | Built by {DEVELOPER}</p>
</div>
""", unsafe_allow_html=True)