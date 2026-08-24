"""
Visualization Module - Invoice Generator Pro
Copyright 2026 ApexDynamics Solutions | Built by Rotimi Ugbana
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from io import BytesIO
import base64

class Visualizer:
    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colors = ['#667EEA', '#764BA2', '#4ECDC4', '#FFD700', '#FF6B6B']
    
    def _to_b64(self, fig):
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        return img
    
    def revenue_trend(self, monthly_data):
        months = list(monthly_data.keys())
        values = list(monthly_data.values())
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months, y=values,
            mode='lines+markers',
            line=dict(color='#667EEA', width=3),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.2)'
        ))
        fig.update_layout(height=350, title='Revenue Trend', xaxis_title='Month', yaxis_title='Revenue')
        return fig.to_html(full_html=False)
    
    def top_clients_chart(self, clients_data):
        clients = list(clients_data.keys())
        amounts = list(clients_data.values())
        
        fig, ax = plt.subplots(figsize=(10, 4))
        bars = ax.barh(clients, amounts, color=self.colors)
        ax.set_title('Top Clients by Revenue', fontweight='bold')
        ax.set_xlabel('Total Revenue')
        plt.tight_layout()
        return self._to_b64(fig)
    
    def summary_cards(self, summary):
        return f"""
        <div style="display:flex;gap:15px;flex-wrap:wrap;justify-content:center;">
            <div style="background:linear-gradient(135deg,#667EEA,#764BA2);color:white;padding:20px;border-radius:10px;flex:1;min-width:150px;text-align:center;">
                <h3 style="margin:0;font-size:14px;">Total Invoices</h3>
                <p style="font-size:32px;margin:10px 0;font-weight:bold;">{summary['total_invoices']}</p>
            </div>
            <div style="background:linear-gradient(135deg,#4ECDC4,#44BD9E);color:white;padding:20px;border-radius:10px;flex:1;min-width:150px;text-align:center;">
                <h3 style="margin:0;font-size:14px;">Total Revenue</h3>
                <p style="font-size:32px;margin:10px 0;font-weight:bold;">₦{summary['total_revenue']:,.2f}</p>
            </div>
            <div style="background:linear-gradient(135deg,#FFD700,#FFA500);color:#333;padding:20px;border-radius:10px;flex:1;min-width:150px;text-align:center;">
                <h3 style="margin:0;font-size:14px;">Average Invoice</h3>
                <p style="font-size:32px;margin:10px 0;font-weight:bold;">₦{summary['average_invoice']:,.2f}</p>
            </div>
            <div style="background:linear-gradient(135deg,#FF6B6B,#FF4757);color:white;padding:20px;border-radius:10px;flex:1;min-width:150px;text-align:center;">
                <h3 style="margin:0;font-size:14px;">Tax Collected</h3>
                <p style="font-size:32px;margin:10px 0;font-weight:bold;">₦{summary['total_tax']:,.2f}</p>
            </div>
        </div>
        """