"""
Invoice Generation Engine
Copyright 2026 ApexDynamics Solutions | Built by Rotimi Ugbana
"""
from datetime import datetime
import uuid
import json
import os

class InvoiceEngine:
    def __init__(self):
        self.company = "ApexDynamics Solutions"
        self.invoices_file = "invoices.json"
        self.invoices = []
        if os.path.exists(self.invoices_file):
            with open(self.invoices_file) as f:
                self.invoices = json.load(f)
    
    def save_invoices(self):
        with open(self.invoices_file, 'w') as f:
            json.dump(self.invoices, f, indent=2)
    
    def generate_invoice_number(self):
        date_part = datetime.now().strftime("%Y%m%d")
        unique = str(uuid.uuid4())[:6].upper()
        return f"INV-{date_part}-{unique}"
    
    def create_invoice(self, data):
        invoice = {
            "invoice_number": self.generate_invoice_number(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "due_date": data.get("due_date", ""),
            "from_name": data.get("from_name", ""),
            "from_email": data.get("from_email", ""),
            "from_address": data.get("from_address", ""),
            "to_name": data.get("to_name", ""),
            "to_email": data.get("to_email", ""),
            "to_address": data.get("to_address", ""),
            "items": data.get("items", []),
            "tax_rate": float(data.get("tax_rate", 0)),
            "discount": float(data.get("discount", 0)),
            "notes": data.get("notes", ""),
            "currency": data.get("currency", "NGN"),
            "status": "Created"
        }
        
        # Calculate totals
        subtotal = sum(float(item.get("amount", 0)) for item in invoice["items"])
        discount_amount = subtotal * (invoice["discount"] / 100)
        after_discount = subtotal - discount_amount
        tax_amount = after_discount * (invoice["tax_rate"] / 100)
        total = after_discount + tax_amount
        
        invoice["subtotal"] = round(subtotal, 2)
        invoice["discount_amount"] = round(discount_amount, 2)
        invoice["tax_amount"] = round(tax_amount, 2)
        invoice["total"] = round(total, 2)
        
        self.invoices.append(invoice)
        self.save_invoices()
        return invoice
    
    def get_financial_summary(self):
        if not self.invoices:
            return None
        
        total_invoices = len(self.invoices)
        total_revenue = sum(inv["total"] for inv in self.invoices)
        average_invoice = total_revenue / total_invoices if total_invoices > 0 else 0
        total_tax = sum(inv["tax_amount"] for inv in self.invoices)
        
        # Monthly breakdown
        monthly = {}
        for inv in self.invoices:
            month = inv["date"][:7]
            if month not in monthly:
                monthly[month] = 0
            monthly[month] += inv["total"]
        
        # Top clients
        clients = {}
        for inv in self.invoices:
            client = inv["to_name"]
            clients[client] = clients.get(client, 0) + inv["total"]
        
        top_clients = dict(sorted(clients.items(), key=lambda x: x[1], reverse=True)[:5])
        
        return {
            "total_invoices": total_invoices,
            "total_revenue": round(total_revenue, 2),
            "average_invoice": round(average_invoice, 2),
            "total_tax": round(total_tax, 2),
            "monthly": monthly,
            "top_clients": top_clients
        }