import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings("ignore")

np.random.seed(42)

# ── Sample Data ──
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
revenue  = [220, 245, 210, 280, 310, 295, 330, 355, 315, 370, 395, 420]
expense  = [160, 175, 155, 190, 210, 200, 215, 225, 205, 240, 255, 270]
profit   = [r - e for r, e in zip(revenue, expense)]
margin   = [round(p / r * 100, 1) for p, r in zip(profit, revenue)]

depts    = ["Sales", "Marketing", "Operations", "HR", "IT", "Finance"]
budget   = [500, 300, 450, 150, 250, 200]
actual   = [520, 280, 430, 140, 270, 185]

categories = ["Revenue", "Expense", "Investment", "Tax", "Refund"]
cat_totals = [4500, 3200, 800, 600, 200]

forecast_months = ["Jan'25", "Feb'25", "Mar'25", "Apr'25", "May'25", "Jun'25"]
forecast_vals   = [435, 452, 468, 490, 510, 535]
lower_bound     = [400, 415, 430, 451, 469, 492]
upper_bound     = [470, 489, 506, 529, 551, 578]

BG    = "#0D1B2A"
PANEL = "#1A2B3C"
BLUE  = "#4FC3F7"
GREEN = "#69F0AE"
RED   = "#EF5350"
AMBER = "#FFB74D"
PURPLE= "#CE93D8"
WHITE = "#E8F0FE"
GRAY  = "#90A4AE"

fig = plt.figure(figsize=(20, 13), facecolor=BG)
fig.suptitle("Financial Data Analysis & Forecasting Dashboard",
             fontsize=24, fontweight="bold", color=WHITE, y=0.98)

gs = gridspec.GridSpec(3, 4, figure=fig, hspace=0.5, wspace=0.35)

# ── KPI Cards ──
kpis = [
    ("Total Revenue", "$4.25M", "↑ 21% YoY", BLUE),
    ("Net Profit",    "$1.05M", "↑ 15% YoY", GREEN),
    ("Avg Margin",    "24.7%",  "↑ 2.1pp",   AMBER),
    ("Forecast Acc.", "91.3%",  "R² = 0.94", PURPLE),
]
for i, (label, val, delta, color) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i])
    ax.set_facecolor(PANEL); ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.text(0.5, 0.70, val,   ha="center", fontsize=22, fontweight="bold", color=color)
    ax.text(0.5, 0.44, label, ha="center", fontsize=10, color=GRAY)
    ax.text(0.5, 0.20, delta, ha="center", fontsize=9,  color=GREEN)

# ── Revenue vs Expense Line Chart ──
ax1 = fig.add_subplot(gs[1, :2])
ax1.set_facecolor(PANEL)
ax1.plot(months, revenue, color=BLUE,  linewidth=2.5, marker="o", markersize=5, label="Revenue")
ax1.plot(months, expense, color=RED,   linewidth=2.5, marker="s", markersize=5, label="Expense")
ax1.plot(months, profit,  color=GREEN, linewidth=2,   marker="^", markersize=5, label="Profit", linestyle="--")
ax1.fill_between(months, revenue, expense, alpha=0.08, color=GREEN)
ax1.set_title("Revenue vs Expense vs Profit (K$)", color=WHITE, fontsize=12, pad=8)
ax1.legend(facecolor=PANEL, labelcolor=WHITE, fontsize=9)
ax1.tick_params(colors=GRAY); ax1.spines[:].set_visible(False)

# ── Department Budget vs Actual ──
ax2 = fig.add_subplot(gs[1, 2:])
ax2.set_facecolor(PANEL)
x = np.arange(len(depts))
w = 0.35
ax2.bar(x - w/2, budget, w, label="Budget",  color=BLUE,  alpha=0.85, edgecolor=BG)
ax2.bar(x + w/2, actual, w, label="Actual",  color=AMBER, alpha=0.85, edgecolor=BG)
ax2.set_xticks(x); ax2.set_xticklabels(depts, fontsize=8, color=GRAY)
ax2.set_title("Budget vs Actual by Department (K$)", color=WHITE, fontsize=12, pad=8)
ax2.legend(facecolor=PANEL, labelcolor=WHITE, fontsize=9)
ax2.tick_params(colors=GRAY); ax2.spines[:].set_visible(False)

# ── Revenue Forecast with Confidence Interval ──
ax3 = fig.add_subplot(gs[2, :2])
ax3.set_facecolor(PANEL)
ax3.plot(forecast_months, forecast_vals, color=GREEN, linewidth=2.5, marker="o", markersize=6, label="Forecast")
ax3.fill_between(forecast_months, lower_bound, upper_bound, alpha=0.2, color=GREEN, label="95% CI")
ax3.set_title("6-Month Revenue Forecast (K$)", color=WHITE, fontsize=12, pad=8)
ax3.legend(facecolor=PANEL, labelcolor=WHITE, fontsize=9)
ax3.tick_params(colors=GRAY); ax3.spines[:].set_visible(False)

# ── Category Breakdown Donut ──
ax4 = fig.add_subplot(gs[2, 2])
ax4.set_facecolor(PANEL)
clrs = [BLUE, RED, AMBER, PURPLE, GREEN]
wedges, texts, autotexts = ax4.pie(
    cat_totals, labels=categories, autopct="%1.0f%%",
    colors=clrs, startangle=90, pctdistance=0.75,
    wedgeprops={"width": 0.5, "edgecolor": BG, "linewidth": 2}
)
for t in texts:     t.set_color(GRAY); t.set_fontsize(8)
for t in autotexts: t.set_color(WHITE); t.set_fontsize(8)
ax4.set_title("Transaction Categories", color=WHITE, fontsize=12, pad=8)

# ── Profit Margin Trend ──
ax5 = fig.add_subplot(gs[2, 3])
ax5.set_facecolor(PANEL)
ax5.bar(months, margin, color=PURPLE, alpha=0.85, edgecolor=BG, width=0.6)
ax5.axhline(np.mean(margin), color=AMBER, linewidth=1.5, linestyle="--", label=f"Avg {np.mean(margin):.1f}%")
ax5.set_title("Monthly Profit Margin (%)", color=WHITE, fontsize=12, pad=8)
ax5.set_xticklabels(months, rotation=45, fontsize=7, color=GRAY)
ax5.legend(facecolor=PANEL, labelcolor=WHITE, fontsize=8)
ax5.tick_params(colors=GRAY); ax5.spines[:].set_visible(False)

for ax in [ax1, ax2, ax3, ax5]:
    ax.set_facecolor(PANEL)
    ax.tick_params(colors=GRAY)

plt.savefig("reports/financial_dashboard.png", dpi=150,
            bbox_inches="tight", facecolor=fig.get_facecolor())
print("Dashboard saved → reports/financial_dashboard.png")
plt.show()
