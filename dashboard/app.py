"""Domain D — Customer Service & Complaint Resolution Dashboard (Airtel Telecom Analytics)."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" / "airtel.db"

# High-contrast professional multi-color palette
INK = "#0F172A"
SLATE_TEXT = "#334155"
MUTED_TEXT = "#475569"
GRID_LINE = "#E2E8F0"

BLUE = "#2563EB"
TEAL = "#0D9488"
INDIGO = "#4338CA"
VIOLET = "#7C3AED"
CYAN = "#0891B2"
AMBER = "#D97706"
CORAL = "#DC2626"
ROSE = "#BE123C"

CATEGORY_COLORS = {
    "Slow Data": BLUE,
    "Dropped Call": INDIGO,
    "Network Coverage": CYAN,
    "Billing": VIOLET,
    "Recharge Issue": TEAL,
    "SIM/KYC": AMBER,
}

CHANNEL_COLORS = {
    "Store": BLUE,
    "Call Center": VIOLET,
    "Twitter/X": CYAN,
    "Airtel App": TEAL,
}

STEP4_T7_PVALUE = "7.62e-24"
NATIONAL_CHURN_FALLBACK = 23.75

st.set_page_config(
    page_title="Customer Service Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """<style>
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #F4F7FB !important;
    color: #0F172A !important;
    font-family: 'Inter', 'Segoe UI', -apple-system, sans-serif;
}
header[data-testid="stHeader"] { height: 0rem; visibility: hidden; }
.block-container {
    padding-top: 0.70rem !important;
    padding-bottom: 0.60rem !important;
    padding-left: 1.4rem !important;
    padding-right: 1.4rem !important;
    max-width: 100%;
}
section[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #CBD5E1;
}
section[data-testid="stSidebar"] * {
    color: #0F172A !important;
}
section[data-testid="stSidebar"] .block-container { padding-top: 1.1rem !important; }
div[data-testid="stSelectbox"] label,
div[data-testid="stSelectbox"] p,
div[data-testid="stCaptionContainer"] p {
    color: #1E293B !important;
    font-weight: 600 !important;
    font-size: 0.80rem !important;
}
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border-color: #94A3B8 !important;
    border-radius: 7px !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] svg {
    color: #0F172A !important;
    fill: #0F172A !important;
}
div[data-testid="stVerticalBlock"] > div { gap: 0.40rem !important; }
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
    padding: 0.52rem 0.76rem 0.28rem 0.76rem !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
}
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 1.5rem;
    border-bottom: 1.5px solid #CBD5E1;
    margin-bottom: 0.45rem;
}
div[data-testid="stTabs"] button[role="tab"] {
    padding: 0.25rem 0.2rem 0.40rem 0.2rem;
    font-size: 0.90rem;
    font-weight: 700;
    color: #475569 !important;
    background: transparent !important;
}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #1D4ED8 !important;
}
div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    background-color: #2563EB !important;
    height: 3px !important;
}
.dash-header-box {
    margin-bottom: 0.20rem;
}
h1.dash-title {
    font-size: 1.28rem !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    letter-spacing: -0.02em;
    margin: 0 !important;
    line-height: 1.22 !important;
}
p.dash-reader {
    font-size: 0.80rem !important;
    color: #334155 !important;
    margin: 0.12rem 0 0.24rem 0 !important;
    line-height: 1.35 !important;
}
.section-banner {
    font-size: 0.84rem;
    font-weight: 700;
    color: #1E293B;
    background: #E2E8F0;
    border-left: 4px solid #2563EB;
    padding: 0.22rem 0.62rem;
    border-radius: 4px;
    margin: 0.08rem 0 0.22rem 0;
}
.kpi-card {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-top: 3.5px solid var(--accent, #2563EB);
    border-radius: 10px;
    padding: 0.48rem 0.78rem;
    height: 80px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
}
.kpi-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.4rem;
}
.kpi-label {
    font-size: 0.71rem;
    font-weight: 700;
    color: #334155 !important;
    text-transform: uppercase;
    letter-spacing: 0.025em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.kpi-badge {
    font-size: 0.62rem;
    font-weight: 700;
    color: #1E40AF !important;
    background: #EFF6FF;
    border: 1px solid #93C5FD;
    padding: 0px 6px;
    border-radius: 999px;
    white-space: nowrap;
}
.kpi-value {
    font-size: 1.16rem;
    font-weight: 800;
    letter-spacing: -0.01em;
    line-height: 1.15;
}
.kpi-sub {
    font-size: 0.70rem;
    color: #475569 !important;
    line-height: 1.2;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.chart-title {
    font-size: 0.81rem;
    font-weight: 700;
    color: #0F172A !important;
    margin: 0 0 0.08rem 0;
    line-height: 1.28;
}
.info-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.77rem;
    background-color: #FFFFFF;
    margin-top: 0.14rem;
    margin-bottom: 0.20rem;
}
.info-table th {
    background-color: #F1F5F9;
    color: #0F172A;
    font-weight: 700;
    text-align: left;
    padding: 0.34rem 0.62rem;
    border-bottom: 1.5px solid #CBD5E1;
    text-transform: uppercase;
    font-size: 0.68rem;
    letter-spacing: 0.03em;
}
.info-table td {
    padding: 0.32rem 0.62rem;
    border-bottom: 1px solid #E2E8F0;
    color: #1E293B;
}
.info-table tr:last-child td {
    border-bottom: none;
}
.provenance-line {
    font-size: 0.69rem;
    color: #475569 !important;
    margin-top: 0.22rem;
    padding-top: 0.18rem;
    border-top: 1px dashed #CBD5E1;
}
</style>"""

st.markdown(CSS, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def run_query(sql: str, params: tuple = ()) -> pd.DataFrame:
    """Execute a read-only SQLite query and return raw results without post-processing."""
    with sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True) as con:
        return pd.read_sql_query(sql, con, params=params)


def build_filter_clause(
    connection_type: str, region: str, alias: str = "c"
) -> tuple[str, tuple]:
    """Build parameterized SQL WHERE clause for sidebar filters."""
    clauses: list[str] = []
    params: list[str] = []
    if connection_type != "All":
        clauses.append(f"{alias}.connection_type = ?")
        params.append(connection_type)
    if region != "All":
        clauses.append(f"{alias}.region = ?")
        params.append(region)
    return (" AND ".join(clauses), tuple(params)) if clauses else ("", ())


def where_sql(clause: str, prefix: str = "WHERE") -> str:
    return f" {prefix} {clause} " if clause else ""


def render_card(
    label: str,
    value: str,
    subtext: str,
    accent_color: str = BLUE,
    badge: str = "",
) -> None:
    badge_html = f'<span class="kpi-badge">{badge}</span>' if badge else ""
    html = (
        f'<div class="kpi-card" style="--accent: {accent_color};">'
        f'<div class="kpi-top"><span class="kpi-label">{label}</span>{badge_html}</div>'
        f'<div class="kpi-value" style="color: {accent_color};">{value}</div>'
        f'<div class="kpi-sub">{subtext}</div>'
        f"</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def render_provenance() -> None:
    st.markdown(
        '<div class="provenance-line">'
        "<strong>Data Provenance:</strong> Circle and tariff plan structures are real; "
        "subscriber records (22,000 subscribers, 26,841 tickets, Jan–Jun 2025) are synthetic. "
        "Open-ticket churn reflects an observed association (a link only), not cause and effect."
        "</div>",
        unsafe_allow_html=True,
    )


def style_figure(fig: go.Figure, height: int, margin: dict) -> go.Figure:
    """Apply high-contrast chart styling with explicit dark text colors and axis labels."""
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=margin,
        font=dict(family="Inter, Segoe UI, -apple-system, sans-serif", size=10.5, color=INK),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        showlegend=False,
    )
    fig.update_xaxes(
        tickfont=dict(color=SLATE_TEXT, size=9.8),
        title_font=dict(color=INK, size=10.2),
        linecolor="#94A3B8",
        showline=True,
    )
    fig.update_yaxes(
        tickfont=dict(color=SLATE_TEXT, size=9.8),
        title_font=dict(color=INK, size=10.2),
        linecolor="#94A3B8",
        showline=True,
    )
    return fig


def render_overview_tab(filter_where: str, filter_params: tuple, filter_label: str) -> None:
    st.markdown(
        f'<div class="section-banner">📊 Overall Performance · {filter_label}</div>',
        unsafe_allow_html=True,
    )

    # Card 1 (Fixed)
    card1_df = run_query("SELECT COUNT(*) AS total_tickets FROM complaints;")
    total_base_tickets = int(card1_df.iloc[0]["total_tickets"])

    # Card 2 (Fixed)
    card2_df = run_query(
        """
        SELECT
            ROUND(100.0 * AVG(CASE WHEN unresolved_count > 0 THEN is_churned END), 2) AS open_churn,
            ROUND(100.0 * AVG(CASE WHEN complaint_count = 0 THEN is_churned END), 2) AS never_churn
        FROM customer_features;
        """
    ).iloc[0]

    # Card 3 (Filtered)
    card3_df = run_query(
        f"""
        SELECT
            COUNT(*) AS total_tickets,
            COALESCE(SUM(CASE WHEN x.is_resolved = 0 THEN 1 ELSE 0 END), 0) AS open_tickets,
            COALESCE(SUM(x.is_resolved), 0) AS closed_tickets,
            COALESCE(ROUND(100.0 * SUM(CASE WHEN x.is_resolved = 0 THEN 1 ELSE 0 END)
                / NULLIF(COUNT(*), 0), 2), 0.0) AS open_pct,
            COALESCE(ROUND(100.0 * SUM(x.is_resolved)
                / NULLIF(COUNT(*), 0), 2), 0.0) AS closed_pct
        FROM complaints x
        JOIN customer_features c ON c.customer_id = x.customer_id
        {filter_where};
        """,
        filter_params,
    ).iloc[0]

    c1, c2, c3 = st.columns(3, gap="small")
    with c1:
        render_card(
            "Total Complaints (Jan–Jun 2025)",
            f"{total_base_tickets:,} Tickets",
            "Full 6-month baseline before filters",
            accent_color=BLUE,
            badge="Fixed",
        )
    with c2:
        render_card(
            "Step 4 T7 · Open vs Silent Churn",
            f"{card2_df['open_churn']:.2f}% vs {card2_df['never_churn']:.2f}%",
            f"p = {STEP4_T7_PVALUE} · a link only",
            accent_color=CORAL,
            badge="Fixed",
        )
    with c3:
        render_card(
            "Open Tickets (Filtered)",
            f"{int(card3_df['open_tickets']):,} ({card3_df['open_pct']:.2f}%)",
            f"Of {int(card3_df['total_tickets']):,} tickets ({card3_df['closed_pct']:.2f}% closed)",
            accent_color=AMBER,
            badge="Filtered",
        )

    # Queries for Charts
    hero_df = run_query(
        f"""
        SELECT
            CASE
                WHEN c.complaint_count = 0 THEN '1'
                WHEN c.unresolved_count = 0 THEN '2'
                ELSE '3'
            END AS bucket,
            CASE
                WHEN c.complaint_count = 0 THEN 'Never Complained'
                WHEN c.unresolved_count = 0 THEN 'All Tickets Closed'
                ELSE 'Has Open Ticket'
            END AS label,
            COUNT(*) AS subs,
            SUM(c.is_churned) AS churned,
            ROUND(100.0 * AVG(c.is_churned), 2) AS churn_pct
        FROM customer_features c
        {filter_where}
        GROUP BY bucket, label
        ORDER BY bucket;
        """,
        filter_params,
    )
    current_churn_ref = float(
        run_query(
            f"SELECT ROUND(100.0 * AVG(c.is_churned), 2) AS v FROM customer_features c {filter_where};",
            filter_params,
        ).iloc[0]["v"]
        or 0.0
    )

    cat_df = run_query(
        f"""
        SELECT
            x.category,
            COUNT(*) AS tickets,
            SUM(x.is_resolved) AS closed_tickets,
            ROUND(100.0 * SUM(x.is_resolved) / NULLIF(COUNT(*), 0), 2) AS pct_closed
        FROM complaints x
        JOIN customer_features c ON c.customer_id = x.customer_id
        {filter_where}
        GROUP BY x.category
        ORDER BY tickets ASC;
        """,
        filter_params,
    )
    overall_closed_ref = float(card3_df["closed_pct"] or 0.0)

    monthly_ov_df = run_query(
        f"""
        SELECT
            strftime('%Y-%m', x.complaint_date) AS month,
            SUM(x.is_resolved) AS closed_tickets,
            SUM(CASE WHEN x.is_resolved = 0 THEN 1 ELSE 0 END) AS open_tickets,
            COUNT(*) AS total_tickets
        FROM complaints x
        JOIN customer_features c ON c.customer_id = x.customer_id
        {filter_where}
        GROUP BY month
        ORDER BY month;
        """,
        filter_params,
    )

    circle_df = run_query(
        f"""
        SELECT
            c.circle_name,
            c.region,
            COUNT(*) AS subs,
            SUM(c.complaint_count) AS tickets,
            ROUND(100.0 * SUM(c.complaint_count) / NULLIF(COUNT(*), 0), 1) AS tickets_per_100,
            ROUND(100.0 * AVG(c.is_churned), 2) AS churn_pct
        FROM customer_features c
        {filter_where}
        GROUP BY c.circle_name, c.region
        ORDER BY tickets_per_100 DESC;
        """,
        filter_params,
    )
    overall_t100_ref = float(
        run_query(
            f"""
            SELECT ROUND(100.0 * SUM(c.complaint_count) / NULLIF(COUNT(*), 0), 1) AS v
            FROM customer_features c
            {filter_where};
            """,
            filter_params,
        ).iloc[0]["v"]
        or 0.0
    )

    # Row 2: Hero (Left) + 2 Supporting Visuals (Right)
    col_hero, col_right = st.columns([1, 1], gap="small")

    with col_hero:
        with st.container(border=True):
            hero_title = "1. Churn Rate by Complaint History"
            st.markdown(f'<div class="chart-title">{hero_title}</div>', unsafe_allow_html=True)

            colors_hero = [
                TEAL if lbl == "Never Complained" else (CORAL if lbl == "Has Open Ticket" else BLUE)
                for lbl in hero_df["label"]
            ]
            fig_hero = go.Figure(
                go.Bar(
                    x=hero_df["label"],
                    y=hero_df["churn_pct"],
                    marker_color=colors_hero,
                    width=0.42,
                    text=[
                        f"<b>{row['churn_pct']:.2f}%</b><br>({int(row['subs']):,} subs)"
                        for _, row in hero_df.iterrows()
                    ],
                    textposition="outside",
                    textfont=dict(size=9.8, color=INK),
                    hovertemplate=(
                        "<b>%{x}</b><br>Churn Rate: %{y:.2f}%<br>"
                        "Subscribers: %{customdata[0]:,} · Churned: %{customdata[1]:,}<extra></extra>"
                    ),
                    customdata=hero_df[["subs", "churned"]].values,
                )
            )
            max_y_hero = max(float(hero_df["churn_pct"].max()) if not hero_df.empty else 30.0, current_churn_ref)
            fig_hero.add_hline(
                y=current_churn_ref,
                line_dash="dash",
                line_color=INDIGO,
                line_width=1.5,
                annotation_text=f"Filtered Churn: {current_churn_ref:.2f}%",
                annotation_position="top right",
                annotation_font=dict(size=9.5, color=INDIGO),
                annotation_bgcolor="rgba(255,255,255,0.92)",
            )
            style_figure(fig_hero, height=306, margin=dict(t=16, b=34, l=52, r=14))
            fig_hero.update_yaxes(
                title_text="Churn Rate (%)",
                range=[0, max_y_hero * 1.32],
                gridcolor=GRID_LINE,
                zeroline=False,
            )
            fig_hero.update_xaxes(
                type="category",
                title_text="Complaint Status",
                tickfont=dict(size=10, color=INK),
            )
            st.plotly_chart(fig_hero, theme=None, width="stretch", config={"displayModeBar": False})

    with col_right:
        with st.container(border=True):
            sup1_title = "2. Closure Rate by Category"
            st.markdown(f'<div class="chart-title">{sup1_title}</div>', unsafe_allow_html=True)

            fig_sup1 = go.Figure(
                go.Bar(
                    y=cat_df["category"],
                    x=cat_df["pct_closed"],
                    orientation="h",
                    width=0.60,
                    marker_color=[CATEGORY_COLORS.get(c, BLUE) for c in cat_df["category"]],
                    text=[
                        f"{row['pct_closed']:.1f}% ({int(row['tickets']):,})"
                        for _, row in cat_df.iterrows()
                    ],
                    textposition="outside",
                    textfont=dict(size=9.2, color=INK),
                    hovertemplate=(
                        "<b>%{y}</b><br>Closure Rate: %{x:.2f}%<br>"
                        "Tickets: %{customdata[0]:,} · Closed: %{customdata[1]:,}<extra></extra>"
                    ),
                    customdata=cat_df[["tickets", "closed_tickets"]].values,
                )
            )
            fig_sup1.add_vline(
                x=overall_closed_ref,
                line_dash="dash",
                line_color=ROSE,
                line_width=1.4,
                annotation_text=f"Avg {overall_closed_ref:.1f}%",
                annotation_position="top",
                annotation_font=dict(size=9, color=ROSE),
            )
            style_figure(fig_sup1, height=134, margin=dict(t=16, b=28, l=112, r=14))
            fig_sup1.update_xaxes(
                range=[0, 124],
                title_text="Closure Rate (%) & Tickets",
                gridcolor=GRID_LINE,
            )
            fig_sup1.update_yaxes(title_text=None, tickfont=dict(size=9.8, color=INK))
            st.plotly_chart(fig_sup1, theme=None, width="stretch", config={"displayModeBar": False})

        with st.container(border=True):
            add_ov_title = "3. Monthly Tickets (Closed vs Open)"
            st.markdown(f'<div class="chart-title">{add_ov_title}</div>', unsafe_allow_html=True)

            fig_add_ov = go.Figure()
            fig_add_ov.add_trace(
                go.Bar(
                    name="Closed",
                    x=monthly_ov_df["month"],
                    y=monthly_ov_df["closed_tickets"],
                    marker_color=TEAL,
                    width=0.50,
                    hovertemplate="Month: %{x}<br>Closed: %{y:,}<extra></extra>",
                )
            )
            fig_add_ov.add_trace(
                go.Bar(
                    name="Open",
                    x=monthly_ov_df["month"],
                    y=monthly_ov_df["open_tickets"],
                    marker_color=AMBER,
                    width=0.50,
                    text=[f"{int(t):,}" for t in monthly_ov_df["total_tickets"]],
                    textposition="outside",
                    textfont=dict(size=9, color=INK),
                    hovertemplate="Month: %{x}<br>Open: %{y:,}<extra></extra>",
                )
            )
            max_m_ov = float(monthly_ov_df["total_tickets"].max()) if not monthly_ov_df.empty else 100.0
            fig_add_ov.update_layout(barmode="stack")
            style_figure(fig_add_ov, height=134, margin=dict(t=20, b=30, l=48, r=10))
            fig_add_ov.update_yaxes(
                range=[0, max_m_ov * 1.32],
                gridcolor=GRID_LINE,
                title_text="Tickets",
            )
            fig_add_ov.update_xaxes(
                type="category",
                title_text="Month (2025)",
                tickfont=dict(size=9.5, color=INK),
            )
            fig_add_ov.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=0.98,
                    xanchor="right",
                    x=1.0,
                    font=dict(size=9.2, color=INK),
                ),
            )
            st.plotly_chart(fig_add_ov, theme=None, width="stretch", config={"displayModeBar": False})

    # Row 3: Full-Width Bottom Visual (All Circles)
    with st.container(border=True):
        bot_title = "4. Tickets per 100 Subscribers by Circle"
        st.markdown(f'<div class="chart-title">{bot_title}</div>', unsafe_allow_html=True)

        x_labels = [f"{row['circle_name']} ({int(row['subs'])})" for _, row in circle_df.iterrows()]
        circle_colors = [
            CORAL if v >= overall_t100_ref + 3 else (BLUE if v >= overall_t100_ref - 2 else TEAL)
            for v in circle_df["tickets_per_100"]
        ]
        fig_bot = go.Figure(
            go.Bar(
                x=x_labels,
                y=circle_df["tickets_per_100"],
                width=0.54,
                marker_color=circle_colors,
                text=[f"{v:.1f}" for v in circle_df["tickets_per_100"]],
                textposition="outside",
                textfont=dict(size=8.8, color=INK),
                hovertemplate=(
                    "<b>%{x}</b><br>Tickets/100 Subs: %{y:.1f}<br>"
                    "Subscribers: %{customdata[0]:,} · Tickets: %{customdata[1]:,}<extra></extra>"
                ),
                customdata=circle_df[["subs", "tickets"]].values,
            )
        )
        max_t100 = float(circle_df["tickets_per_100"].max()) if not circle_df.empty else 140.0
        fig_bot.add_hline(
            y=overall_t100_ref,
            line_dash="dash",
            line_color=INDIGO,
            line_width=1.4,
            annotation_text=f"Filtered Avg: {overall_t100_ref:.1f}/100",
            annotation_position="top left",
            annotation_font=dict(size=9.2, color=INDIGO),
            annotation_bgcolor="rgba(255,255,255,0.92)",
        )
        style_figure(fig_bot, height=180, margin=dict(t=16, b=66, l=54, r=14))
        fig_bot.update_yaxes(
            range=[0, max_t100 * 1.32],
            title_text="Tickets / 100 Subs",
            gridcolor=GRID_LINE,
        )
        fig_bot.update_xaxes(
            type="category",
            tickangle=-26,
            tickfont=dict(size=8.8, color=INK),
            title_text="Circle (Subscriber Count)",
        )
        st.plotly_chart(fig_bot, theme=None, width="stretch", config={"displayModeBar": False})

    # Important Information Summary Table (Overall)
    region_perf_df = run_query(
        f"""
        SELECT
            c.region,
            COUNT(*) AS subs,
            SUM(c.complaint_count) AS tickets,
            ROUND(100.0 * SUM(c.complaint_count) / NULLIF(COUNT(*), 0), 1) AS tickets_per_100,
            ROUND(100.0 * AVG(c.is_churned), 2) AS churn_pct
        FROM customer_features c
        {filter_where}
        GROUP BY c.region
        ORDER BY tickets_per_100 ASC, churn_pct ASC;
        """,
        filter_params,
    )

    top_cat_row = cat_df.iloc[-1] if not cat_df.empty else None
    top_cat_share = (
        round(100.0 * int(top_cat_row["tickets"]) / int(card3_df["total_tickets"]), 1)
        if top_cat_row is not None and int(card3_df["total_tickets"]) > 0
        else 0.0
    )
    best_reg_str = (
        f"{region_perf_df.iloc[0]['region']} ({region_perf_df.iloc[0]['tickets_per_100']:.1f}/100 subs · "
        f"{region_perf_df.iloc[0]['churn_pct']:.2f}% churn)"
        if not region_perf_df.empty
        else "N/A"
    )
    worst_reg_str = (
        f"{region_perf_df.iloc[-1]['region']} ({region_perf_df.iloc[-1]['tickets_per_100']:.1f}/100 subs · "
        f"{region_perf_df.iloc[-1]['churn_pct']:.2f}% churn)"
        if not region_perf_df.empty
        else "N/A"
    )
    top_cat_str = (
        f"{top_cat_row['category']} ({int(top_cat_row['tickets']):,} tickets · {top_cat_share:.1f}%)"
        if top_cat_row is not None
        else "N/A"
    )

    with st.container(border=True):
        st.markdown(
            '<div class="chart-title">Overall Summary</div>',
            unsafe_allow_html=True,
        )
        summary_html = f"""
        <table class="info-table">
            <thead>
                <tr>
                    <th style="width: 24%;">Metric</th>
                    <th style="width: 34%;">Value</th>
                    <th style="width: 42%;">Operational Note</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Total Complaints</strong></td>
                    <td><strong>{int(card3_df['total_tickets']):,} tickets</strong> (Base: {total_base_tickets:,})</td>
                    <td>Complaints logged Jan–Jun 2025</td>
                </tr>
                <tr>
                    <td><strong>Open Tickets</strong></td>
                    <td><strong>{int(card3_df['open_tickets']):,} ({card3_df['open_pct']:.2f}%)</strong></td>
                    <td>Unresolved tickets awaiting closure</td>
                </tr>
                <tr>
                    <td><strong>Closure Rate</strong></td>
                    <td><strong>{card3_df['closed_pct']:.2f}%</strong> ({int(card3_df['closed_tickets']):,} closed)</td>
                    <td>Share of total tickets resolved</td>
                </tr>
                <tr>
                    <td><strong>Churn Rate</strong></td>
                    <td><strong>{current_churn_ref:.2f}%</strong> (Open-ticket base: {card2_df['open_churn']:.2f}%)</td>
                    <td>Filtered cohort churn vs open-ticket link</td>
                </tr>
                <tr>
                    <td><strong>Top Complaint Category</strong></td>
                    <td><strong>{top_cat_str}</strong></td>
                    <td>Highest-volume issue category</td>
                </tr>
                <tr>
                    <td><strong>Best Region</strong></td>
                    <td><strong>{best_reg_str}</strong></td>
                    <td>Lowest complaint rate per 100 subscribers</td>
                </tr>
                <tr>
                    <td><strong>Worst Region</strong></td>
                    <td><strong>{worst_reg_str}</strong></td>
                    <td>Highest complaint rate per 100 subscribers</td>
                </tr>
            </tbody>
        </table>
        """
        st.markdown(summary_html, unsafe_allow_html=True)

    render_provenance()


def render_detail_tab(
    filter_where: str, filter_and: str, filter_params: tuple, filter_label: str
) -> None:
    st.markdown(
        f'<div class="section-banner">📁 Category Analysis · {filter_label}</div>',
        unsafe_allow_html=True,
    )

    cat_order_df = run_query(
        f"""
        SELECT x.category, COUNT(*) AS tickets
        FROM complaints x
        JOIN customer_features c ON c.customer_id = x.customer_id
        {filter_where}
        GROUP BY x.category
        ORDER BY tickets DESC;
        """,
        filter_params,
    )
    category_choices = cat_order_df["category"].tolist() or ["Slow Data"]

    d_c1, d_c2, d_c3, d_sel = st.columns([1, 1, 1, 0.90], gap="small")
    with d_sel:
        selected_cat = st.selectbox(
            "Category (Most Tickets First)",
            category_choices,
            index=0,
        )

    cat_params = (selected_cat,) + filter_params

    det_cards_df = run_query(
        f"""
        SELECT
            SUM(CASE WHEN x.category = ? THEN 1 ELSE 0 END) AS cat_tickets,
            COUNT(*) AS all_filtered_tickets,
            SUM(CASE WHEN x.category = ? AND x.is_resolved = 1 THEN 1 ELSE 0 END) AS cat_closed_tickets,
            SUM(CASE WHEN x.category = ? AND x.is_resolved = 0 THEN 1 ELSE 0 END) AS cat_open_tickets,
            ROUND(100.0 * SUM(CASE WHEN x.category = ? THEN 1 ELSE 0 END)
                / NULLIF(COUNT(*), 0), 1) AS cat_share_pct,
            ROUND(100.0 * SUM(CASE WHEN x.category = ? AND x.is_resolved = 1 THEN 1 ELSE 0 END)
                / NULLIF(SUM(CASE WHEN x.category = ? THEN 1 ELSE 0 END), 0), 2) AS cat_closed_pct,
            ROUND(AVG(CASE WHEN x.category = ? AND x.is_resolved = 1 THEN x.resolution_days END), 2)
                AS avg_days_closed
        FROM complaints x
        JOIN customer_features c ON c.customer_id = x.customer_id
        {filter_where};
        """,
        (selected_cat,) * 7 + filter_params,
    ).iloc[0]

    det_card3_df = run_query(
        f"""
        WITH open_cat_subs AS (
            SELECT DISTINCT x.customer_id
            FROM complaints x
            JOIN customer_features c ON c.customer_id = x.customer_id
            WHERE x.category = ? AND x.is_resolved = 0
            {filter_and}
        )
        SELECT
            COUNT(*) AS open_subs,
            COALESCE(SUM(c.is_churned), 0) AS left_subs,
            COALESCE(ROUND(100.0 * AVG(c.is_churned), 1), 0.0) AS left_pct
        FROM open_cat_subs o
        JOIN customer_features c ON c.customer_id = o.customer_id;
        """,
        cat_params,
    ).iloc[0]

    with d_c1:
        render_card(
            f"{selected_cat} Tickets",
            f"{int(det_cards_df['cat_tickets']):,} ({det_cards_df['cat_share_pct']:.1f}%)",
            f"Of {int(det_cards_df['all_filtered_tickets']):,} filtered tickets",
            accent_color=BLUE,
            badge="Volume",
        )
    with d_c2:
        render_card(
            "Closure & Days to Close",
            f"{det_cards_df['cat_closed_pct']:.2f}% · {det_cards_df['avg_days_closed']:.2f} d",
            "Mean days across closed tickets only",
            accent_color=TEAL,
            badge="SLA",
        )
    with d_c3:
        render_card(
            f"Open {selected_cat} Subs",
            f"{int(det_card3_df['open_subs']):,} · {int(det_card3_df['left_subs']):,} left",
            f"{det_card3_df['left_pct']:.1f}% churned among open-ticket subs",
            accent_color=CORAL,
            badge="Churn Link",
        )

    det_month_df = run_query(
        f"""
        SELECT
            strftime('%Y-%m', x.complaint_date) AS month,
            SUM(x.is_resolved) AS closed_tickets,
            SUM(CASE WHEN x.is_resolved = 0 THEN 1 ELSE 0 END) AS open_tickets,
            COUNT(*) AS total_tickets
        FROM complaints x
        JOIN customer_features c ON c.customer_id = x.customer_id
        WHERE x.category = ?
        {filter_and}
        GROUP BY month
        ORDER BY month;
        """,
        cat_params,
    )
    avg_monthly_cat = float(
        run_query(
            f"""
            SELECT ROUND(AVG(cnt), 1) AS avg_m
            FROM (
                SELECT strftime('%Y-%m', x.complaint_date) AS m, COUNT(*) AS cnt
                FROM complaints x
                JOIN customer_features c ON c.customer_id = x.customer_id
                WHERE x.category = ?
                {filter_and}
                GROUP BY m
            );
            """,
            cat_params,
        ).iloc[0]["avg_m"]
        or 0.0
    )

    det_chan_df = run_query(
        f"""
        SELECT
            x.channel,
            COUNT(*) AS tickets,
            SUM(x.is_resolved) AS closed_tickets,
            ROUND(100.0 * SUM(x.is_resolved) / NULLIF(COUNT(*), 0), 2) AS pct_closed
        FROM complaints x
        JOIN customer_features c ON c.customer_id = x.customer_id
        WHERE x.category = ?
        {filter_and}
        GROUP BY x.channel
        ORDER BY pct_closed ASC;
        """,
        cat_params,
    )

    det_days_df = run_query(
        f"""
        SELECT
            CAST(x.resolution_days AS INT) AS days,
            COUNT(*) AS closed_tickets
        FROM complaints x
        JOIN customer_features c ON c.customer_id = x.customer_id
        WHERE x.category = ? AND x.is_resolved = 1
        {filter_and}
        GROUP BY days
        ORDER BY days;
        """,
        cat_params,
    )

    det_churn_df = run_query(
        f"""
        WITH cat_sub AS (
            SELECT
                x.customer_id,
                MAX(CASE WHEN x.is_resolved = 0 THEN 1 ELSE 0 END) AS has_open
            FROM complaints x
            JOIN customer_features c ON c.customer_id = x.customer_id
            WHERE x.category = ?
            {filter_and}
            GROUP BY x.customer_id
        )
        SELECT
            CASE WHEN cs.has_open = 0 THEN 'All Category Tickets Closed'
                 ELSE 'Has Open Category Ticket' END AS status_group,
            cs.has_open,
            COUNT(*) AS subs,
            SUM(c.is_churned) AS left_subs,
            ROUND(100.0 * AVG(c.is_churned), 2) AS churn_pct
        FROM cat_sub cs
        JOIN customer_features c ON c.customer_id = cs.customer_id
        GROUP BY cs.has_open, status_group
        ORDER BY cs.has_open;
        """,
        cat_params,
    )
    national_churn_ref = float(
        run_query("SELECT ROUND(100.0 * AVG(is_churned), 2) AS v FROM customer_features;").iloc[0]["v"]
        or NATIONAL_CHURN_FALLBACK
    )

    d_hero, d_right = st.columns([1, 1], gap="small")

    with d_hero:
        with st.container(border=True):
            d_hero_title = f"1. {selected_cat} Monthly Tickets"
            st.markdown(f'<div class="chart-title">{d_hero_title}</div>', unsafe_allow_html=True)

            fig_d_hero = go.Figure()
            fig_d_hero.add_trace(
                go.Bar(
                    name="Closed",
                    x=det_month_df["month"],
                    y=det_month_df["closed_tickets"],
                    marker_color=BLUE,
                    width=0.50,
                    hovertemplate="Month: %{x}<br>Closed: %{y:,}<extra></extra>",
                )
            )
            fig_d_hero.add_trace(
                go.Bar(
                    name="Open",
                    x=det_month_df["month"],
                    y=det_month_df["open_tickets"],
                    marker_color=AMBER,
                    width=0.50,
                    text=[f"{int(t):,}" for t in det_month_df["total_tickets"]],
                    textposition="outside",
                    textfont=dict(size=9.5, color=INK),
                    hovertemplate="Month: %{x}<br>Open: %{y:,}<extra></extra>",
                )
            )
            max_dm = float(det_month_df["total_tickets"].max()) if not det_month_df.empty else 100.0
            fig_d_hero.add_hline(
                y=avg_monthly_cat,
                line_dash="dash",
                line_color=INDIGO,
                line_width=1.4,
                annotation_text=f"6-Mo Avg: {avg_monthly_cat:,.0f}/mo",
                annotation_position="top right",
                annotation_font=dict(size=9.5, color=INDIGO),
                annotation_bgcolor="rgba(255,255,255,0.92)",
            )
            fig_d_hero.update_layout(barmode="stack")
            style_figure(fig_d_hero, height=306, margin=dict(t=22, b=34, l=52, r=12))
            fig_d_hero.update_yaxes(
                range=[0, max(max_dm, avg_monthly_cat) * 1.30],
                title_text="Tickets",
                gridcolor=GRID_LINE,
            )
            fig_d_hero.update_xaxes(
                type="category",
                title_text="Month (2025)",
                tickfont=dict(size=10, color=INK),
            )
            fig_d_hero.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=0.98,
                    xanchor="left",
                    x=0.0,
                    font=dict(size=9.2, color=INK),
                ),
            )
            st.plotly_chart(fig_d_hero, theme=None, width="stretch", config={"displayModeBar": False})

    with d_right:
        with st.container(border=True):
            cat_closed_ref = float(det_cards_df["cat_closed_pct"] or 0.0)
            d_sup1_title = f"2. {selected_cat} Closure by Channel"
            st.markdown(f'<div class="chart-title">{d_sup1_title}</div>', unsafe_allow_html=True)

            fig_d_sup1 = go.Figure(
                go.Bar(
                    y=det_chan_df["channel"],
                    x=det_chan_df["pct_closed"],
                    orientation="h",
                    width=0.58,
                    marker_color=[CHANNEL_COLORS.get(ch, BLUE) for ch in det_chan_df["channel"]],
                    text=[
                        f"{row['pct_closed']:.1f}% ({int(row['tickets']):,})"
                        for _, row in det_chan_df.iterrows()
                    ],
                    textposition="outside",
                    textfont=dict(size=9.2, color=INK),
                    hovertemplate=(
                        "<b>%{y}</b><br>Closure Rate: %{x:.2f}%<br>"
                        "Tickets: %{customdata[0]:,} · Closed: %{customdata[1]:,}<extra></extra>"
                    ),
                    customdata=det_chan_df[["tickets", "closed_tickets"]].values,
                )
            )
            fig_d_sup1.add_vline(
                x=cat_closed_ref,
                line_dash="dash",
                line_color=ROSE,
                line_width=1.4,
                annotation_text=f"Avg {cat_closed_ref:.1f}%",
                annotation_position="top",
                annotation_font=dict(size=9, color=ROSE),
            )
            style_figure(fig_d_sup1, height=134, margin=dict(t=16, b=28, l=92, r=12))
            fig_d_sup1.update_xaxes(
                range=[0, 124],
                title_text="Closure Rate (%) & Tickets",
                gridcolor=GRID_LINE,
            )
            fig_d_sup1.update_yaxes(title_text=None, tickfont=dict(size=9.8, color=INK))
            st.plotly_chart(fig_d_sup1, theme=None, width="stretch", config={"displayModeBar": False})

        with st.container(border=True):
            avg_d_val = float(det_cards_df["avg_days_closed"] or 0.0)
            d_add_title = "3. Days to Close"
            st.markdown(f'<div class="chart-title">{d_add_title}</div>', unsafe_allow_html=True)

            fig_d_add = go.Figure(
                go.Bar(
                    x=det_days_df["days"],
                    y=det_days_df["closed_tickets"],
                    width=0.60,
                    marker_color=VIOLET,
                    hovertemplate="Day %{x}<br>Closed Tickets: %{y:,}<extra></extra>",
                )
            )
            max_dy = float(det_days_df["closed_tickets"].max()) if not det_days_df.empty else 10.0
            fig_d_add.add_vline(
                x=avg_d_val,
                line_dash="dash",
                line_color=CORAL,
                line_width=1.4,
                annotation_text=f"Mean: {avg_d_val:.2f}d",
                annotation_position="top right",
                annotation_font=dict(size=9, color=CORAL),
                annotation_bgcolor="rgba(255,255,255,0.92)",
            )
            style_figure(fig_d_add, height=134, margin=dict(t=16, b=30, l=48, r=10))
            fig_d_add.update_yaxes(
                range=[0, max_dy * 1.28],
                title_text="Closed Tickets",
                gridcolor=GRID_LINE,
            )
            fig_d_add.update_xaxes(
                dtick=1,
                title_text="Days to Close",
                tickfont=dict(size=9.2, color=INK),
            )
            st.plotly_chart(fig_d_add, theme=None, width="stretch", config={"displayModeBar": False})

    # Row 3: Full-Width Bottom Visual (Category Churn Comparison)
    with st.container(border=True):
        d_bot_title = f"4. {selected_cat} Churn: Open vs Closed Tickets"
        st.markdown(f'<div class="chart-title">{d_bot_title}</div>', unsafe_allow_html=True)

        fig_d_bot = go.Figure(
            go.Bar(
                y=det_churn_df["status_group"],
                x=det_churn_df["churn_pct"],
                orientation="h",
                width=0.46,
                marker_color=[TEAL if h == 0 else CORAL for h in det_churn_df["has_open"]],
                text=[
                    f"<b>{row['churn_pct']:.2f}%</b> · {int(row['subs']):,} subs ({int(row['left_subs']):,} left)"
                    for _, row in det_churn_df.iterrows()
                ],
                textposition="outside",
                textfont=dict(size=10, color=INK),
                hovertemplate=(
                    "<b>%{y}</b><br>Churn Rate: %{x:.2f}%<br>"
                    "Subscribers: %{customdata[0]:,} · Left: %{customdata[1]:,}<extra></extra>"
                ),
                customdata=det_churn_df[["subs", "left_subs"]].values,
            )
        )
        max_dc = max(float(det_churn_df["churn_pct"].max()) if not det_churn_df.empty else 30.0, national_churn_ref)
        fig_d_bot.add_vline(
            x=national_churn_ref,
            line_dash="dash",
            line_color=INDIGO,
            line_width=1.4,
            annotation_text=f"National Avg: {national_churn_ref:.2f}%",
            annotation_position="top",
            annotation_font=dict(size=9.5, color=INDIGO),
        )
        style_figure(fig_d_bot, height=180, margin=dict(t=18, b=36, l=182, r=18))
        fig_d_bot.update_xaxes(
            range=[0, max_dc * 1.50],
            title_text="Churn Rate (%)",
            gridcolor=GRID_LINE,
        )
        fig_d_bot.update_yaxes(title_text=None, tickfont=dict(size=10.2, color=INK))
        st.plotly_chart(fig_d_bot, theme=None, width="stretch", config={"displayModeBar": False})

    # Important Information Summary Table (Detailed Category Analysis)
    cat_reg_df = run_query(
        f"""
        SELECT
            c.region,
            COUNT(*) AS tickets,
            ROUND(100.0 * SUM(x.is_resolved) / NULLIF(COUNT(*), 0), 2) AS closure_pct
        FROM complaints x
        JOIN customer_features c ON c.customer_id = x.customer_id
        WHERE x.category = ?
        {filter_and}
        GROUP BY c.region
        ORDER BY tickets DESC;
        """,
        cat_params,
    )

    top_chan_row = det_chan_df.iloc[-1] if not det_chan_df.empty else None
    top_chan_str = (
        f"{top_chan_row['channel']} ({top_chan_row['pct_closed']:.1f}% closed · {int(top_chan_row['tickets']):,} tickets)"
        if top_chan_row is not None
        else "N/A"
    )
    top_reg_cat_str = (
        f"{cat_reg_df.iloc[0]['region']} ({int(cat_reg_df.iloc[0]['tickets']):,} tickets · {cat_reg_df.iloc[0]['closure_pct']:.1f}% closed)"
        if not cat_reg_df.empty
        else "N/A"
    )
    low_reg_cat_str = (
        f"{cat_reg_df.iloc[-1]['region']} ({int(cat_reg_df.iloc[-1]['tickets']):,} tickets · {cat_reg_df.iloc[-1]['closure_pct']:.1f}% closed)"
        if not cat_reg_df.empty
        else "N/A"
    )
    cat_open_pct = (
        round(100.0 * int(det_cards_df["cat_open_tickets"]) / int(det_cards_df["cat_tickets"]), 2)
        if int(det_cards_df["cat_tickets"]) > 0
        else 0.0
    )

    with st.container(border=True):
        st.markdown(
            f'<div class="chart-title">{selected_cat} Summary</div>',
            unsafe_allow_html=True,
        )
        cat_summary_html = f"""
        <table class="info-table">
            <thead>
                <tr>
                    <th style="width: 24%;">Metric</th>
                    <th style="width: 34%;">Value</th>
                    <th style="width: 42%;">Category Note</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Category Complaints</strong></td>
                    <td><strong>{int(det_cards_df['cat_tickets']):,} tickets</strong> ({det_cards_df['cat_share_pct']:.1f}% of filtered)</td>
                    <td>Total {selected_cat} tickets raised Jan–Jun 2025</td>
                </tr>
                <tr>
                    <td><strong>Open Tickets</strong></td>
                    <td><strong>{int(det_cards_df['cat_open_tickets']):,} ({cat_open_pct:.2f}%)</strong></td>
                    <td>Unresolved {selected_cat} tickets still open</td>
                </tr>
                <tr>
                    <td><strong>Closure Rate &amp; SLA</strong></td>
                    <td><strong>{det_cards_df['cat_closed_pct']:.2f}% closed</strong> · {det_cards_df['avg_days_closed']:.2f} avg days</td>
                    <td>Mean closure time for resolved tickets only</td>
                </tr>
                <tr>
                    <td><strong>Open-Ticket Churn</strong></td>
                    <td><strong>{det_card3_df['left_pct']:.1f}%</strong> ({int(det_card3_df['left_subs']):,} of {int(det_card3_df['open_subs']):,} subs left)</td>
                    <td>Observed churn link among open-ticket subscribers</td>
                </tr>
                <tr>
                    <td><strong>Best Closure Channel</strong></td>
                    <td><strong>{top_chan_str}</strong></td>
                    <td>Channel with highest resolution rate for {selected_cat}</td>
                </tr>
                <tr>
                    <td><strong>Highest Volume Region</strong></td>
                    <td><strong>{top_reg_cat_str}</strong></td>
                    <td>Region generating most {selected_cat} tickets</td>
                </tr>
                <tr>
                    <td><strong>Lowest Volume Region</strong></td>
                    <td><strong>{low_reg_cat_str}</strong></td>
                    <td>Region generating fewest {selected_cat} tickets</td>
                </tr>
            </tbody>
        </table>
        """
        st.markdown(cat_summary_html, unsafe_allow_html=True)

    render_provenance()


# ---------------------------------------------------------------------------
# Sidebar Filters & Main Entrypoint
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div style="font-size:1.05rem;font-weight:800;color:#0F172A;margin-bottom:0.45rem;">'
        "Filters</div>",
        unsafe_allow_html=True,
    )
    conn_options = ["All"] + run_query(
        "SELECT DISTINCT connection_type FROM customer_features ORDER BY connection_type;"
    )["connection_type"].tolist()
    region_options = ["All"] + run_query(
        "SELECT DISTINCT region FROM customer_features ORDER BY region;"
    )["region"].tolist()

    selected_conn = st.selectbox("Connection Type", conn_options, index=0)
    selected_region = st.selectbox("Region", region_options, index=0)

    filter_clause, filter_params = build_filter_clause(selected_conn, selected_region, "c")
    filter_where = where_sql(filter_clause, "WHERE")
    filter_and = where_sql(filter_clause, "AND")
    filter_label = f"{selected_conn} · {selected_region}"

    sub_summary = run_query(
        f"""
        SELECT COUNT(*) AS subs,
               COALESCE(SUM(complaint_count), 0) AS tickets
        FROM customer_features c
        {filter_where};
        """,
        filter_params,
    ).iloc[0]
    st.markdown(
        f'<div style="font-size:0.80rem;color:#1E293B;margin-top:0.45rem;padding:0.45rem;background:#F1F5F9;border-radius:6px;">'
        f"<strong>Active Cohort:</strong><br>"
        f"• <strong>{int(sub_summary['subs']):,}</strong> Subscribers<br>"
        f"• <strong>{int(sub_summary['tickets']):,}</strong> Tickets</div>"
        f'<div style="font-size:0.73rem;color:#475569;margin-top:0.4rem;line-height:1.35;">'
        f"Overview Cards 1 &amp; 2 stay fixed to the full Jan–Jun 2025 base.</div>",
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="dash-header-box">'
    '<h1 class="dash-title">Customer Service Dashboard</h1>'
    '<p class="dash-reader"><strong>For the Head of Customer Service:</strong> '
    "Prioritize support capacity across complaint volume, open tickets, resolution rates, and churn links.</p>"
    "</div>",
    unsafe_allow_html=True,
)

tab_overview, tab_detail = st.tabs(
    ["📊 Overview", "📁 Category Detail"]
)

with tab_overview:
    render_overview_tab(filter_where, filter_params, filter_label)

with tab_detail:
    render_detail_tab(filter_where, filter_and, filter_params, filter_label)
