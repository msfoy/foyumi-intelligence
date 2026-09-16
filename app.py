
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from PIL import Image

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FOYUMI Intelligence",
    page_icon="💄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PATHS
# ============================================================

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
ASSETS = BASE / "assets"
LOGO_DIR = ASSETS / "logo"
IMAGE_DIR = ASSETS / "images"

# ============================================================
# FOYUMI BRAND SYSTEM
# ============================================================

PEACH = "#D1947B"
BROWN = "#6F4E45"
SAGE = "#A8B9A5"
BLUE = "#9FB7C9"
LAVENDER = "#B4A7C5"
NUDE = "#DCC7B8"
DUSTY_ROSE = "#C7A6A0"
CREAM = "#FAF6F3"
LIGHT = "#F4EEEA"
DARK = "#332723"

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background: {CREAM};
    }}

    section[data-testid="stSidebar"] {{
        background: white;
        border-right: 1px solid #E8DDD8;
    }}

    .main-title {{
        font-size: 3.2rem;
        font-weight: 700;
        color: {BROWN};
        line-height: 1.05;
        margin-bottom: 0.4rem;
    }}

    .subtitle {{
        font-size: 1.15rem;
        color: #6E625E;
        max-width: 760px;
        line-height: 1.6;
    }}

    .eyebrow {{
        text-transform: uppercase;
        letter-spacing: 0.18em;
        font-size: 0.72rem;
        font-weight: 700;
        color: {PEACH};
    }}

    .section-title {{
        color: {BROWN};
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 1.5rem;
    }}

    .section-text {{
        color: #625752;
        line-height: 1.65;
    }}

    .metric-card {{
        background: white;
        padding: 1.2rem;
        border-radius: 16px;
        border: 1px solid #E9DDD7;
        box-shadow: 0 3px 14px rgba(80,50,40,0.05);
        min-height: 120px;
    }}

    .metric-label {{
        color: #786B66;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}

    .metric-value {{
        color: {BROWN};
        font-size: 1.85rem;
        font-weight: 700;
        margin-top: 0.35rem;
    }}

    .metric-note {{
        color: #8C7D77;
        font-size: 0.78rem;
        margin-top: 0.3rem;
    }}

    .insight-card {{
        background: white;
        border-left: 5px solid {PEACH};
        padding: 1.1rem 1.25rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: #4D403B;
        line-height: 1.6;
    }}

    .action-card {{
        background: {LIGHT};
        padding: 1.25rem;
        border-radius: 14px;
        border: 1px solid #E6D8D1;
        height: 100%;
    }}

    .action-title {{
        color: {BROWN};
        font-weight: 700;
        font-size: 1rem;
    }}

    .hero {{
        background: linear-gradient(
            135deg,
            rgba(255,255,255,0.96),
            rgba(244,238,234,0.94)
        );
        border-radius: 24px;
        padding: 3rem;
        margin-bottom: 2rem;
        border: 1px solid #E8DDD8;
    }}

    .pill {{
        display: inline-block;
        background: {NUDE};
        color: {BROWN};
        padding: 0.35rem 0.75rem;
        border-radius: 30px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.35rem;
        margin-bottom: 0.35rem;
    }}

    .footer {{
        text-align: center;
        color: #8A7A73;
        padding: 3rem 0 1rem;
        font-size: 0.8rem;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# DATA LOADER
# ============================================================

@st.cache_data
def load_data():

    # Public deployment deliberately uses aggregated
    # management intelligence rather than customer-level
    # source records.

    return None, None, None


appointments, clients, sales = load_data()


# ============================================================
# OPTIONAL ANALYTICAL FILE LOADER
# ============================================================

def find_csv(keywords):

    files = list(DATA.glob("*.csv"))

    for file in files:
        name = file.name.lower()

        if all(keyword.lower() in name for keyword in keywords):
            return file

    return None


def load_optional(keywords):

    file = find_csv(keywords)

    if file is not None:
        try:
            return pd.read_csv(file)
        except:
            return None

    return None


monthly = load_optional(["monthly", "completed"])
rfm = load_optional(["rfm", "customer"])
rfm_summary = load_optional(["rfm", "summary"])
customer_summary = load_optional(["customer", "booking"])
outcome = load_optional(["outcome"])
entry = load_optional(["booking", "entry"])
service = load_optional(["service"])
axis = load_optional(["axis"])
forecast = load_optional(["forecast"])


# ============================================================
# DATA PREPARATION
# ============================================================

# The public prototype uses validated aggregate intelligence.
# Customer-level source records are intentionally excluded.

completed = pd.DataFrame()

status_col = None
date_col = None
service_group_col = None
customer_id_col = None

# ============================================================
# FIXED VALIDATED KPIs
# ============================================================

TOTAL_COMPLETED = 474
CUSTOMERS_COMPLETED = 235
COMPLETED_VALUE = 28_354_500
REPEAT_CUSTOMERS = 86
Q4_FORECAST = 60


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    if logo_files := list(LOGO_DIR.glob("*")):
        try:
            st.image(
                str(logo_files[0]),
                use_container_width=True
            )
        except:
            pass

    st.markdown(
        "<div class='eyebrow'>FOYUMI INTELLIGENCE</div>",
        unsafe_allow_html=True
    )

    st.markdown("### Strategic Prototype")

    st.markdown(
        """
        **Turning Beauty Data Into Better Business Decisions**
        
        An interactive proof-of-concept demonstrating how
        FOYUMI can move from operational records to integrated
        customer, service and demand intelligence.
        """
    )

    st.divider()

    page = st.radio(
        "Navigate",
        [
            "Home",
            "Business Intelligence",
            "Customer Intelligence",
            "Service Intelligence",
            "Booking Intelligence",
            "Demand Planner",
            "Data Strategy",
            "Book Your Glam"
        ]
    )

    st.divider()

    st.caption(
        "Prototype built from FOYUMI's cleaned and integrated "
        "appointment, client and sales datasets."
    )


# ============================================================
# HOME
# ============================================================

if page == "Home":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">BEAUTY • DATA • BUSINESS</div>
            <div class="main-title">
                FOYUMI<br>INTELLIGENCE
            </div>
            <p class="subtitle">
                Turning beauty expertise and operational data into
                smarter customer experiences, stronger service
                decisions and more informed business planning.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1.35, 1])

    with col1:

        st.markdown(
            """
            <div class="section-title">
                More than makeup.
            </div>
            <p class="section-text">
                FOYUMI is a professional makeup artistry business
                serving studio, home-service and bridal clients.
                The business combines beauty expertise with a
                customer-focused approach to long-lasting,
                skin-intelligent artistry.
            </p>

            <p class="section-text">
                As FOYUMI grows, the challenge is no longer simply
                collecting more booking records. The strategic
                opportunity is to transform those records into
                intelligence that supports customer retention,
                service planning, booking management and operational
                decision-making.
            </p>
            """,
            unsafe_allow_html=True
        )

        b1, b2 = st.columns(2)

        with b1:
            if st.button(
                "💄 Explore the Intelligence",
                use_container_width=True
            ):
                st.info(
                    "Use the navigation menu to explore the "
                    "management intelligence layer."
                )

        with b2:
            if st.button(
                "📅 Start a Booking",
                use_container_width=True
            ):
                st.info(
                    "Use 'Book Your Glam' in the navigation menu "
                    "to explore the proposed intelligent booking flow."
                )

    with col2:

        if image_files:

            try:
                img = Image.open(str(image_files[0]))
                st.image(
                    img,
                    use_container_width=True
                )
            except:
                pass

    st.markdown("---")

    st.markdown(
        "<div class='section-title'>The strategic intervention</div>",
        unsafe_allow_html=True
    )

    cols = st.columns(6)

    stages = [
        ("01", "DATA", "Capture"),
        ("02", "INTEGRATION", "Connect"),
        ("03", "CUSTOMER", "Understand"),
        ("04", "SERVICE", "Optimise"),
        ("05", "DEMAND", "Plan"),
        ("06", "ACTION", "Decide")
    ]

    for col, (number, title, text) in zip(cols, stages):

        with col:
            st.markdown(
                f"""
                <div class="action-card">
                    <div class="eyebrow">{number}</div>
                    <div class="action-title">{title}</div>
                    <div>{text}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# BUSINESS INTELLIGENCE
# ============================================================

elif page == "Business Intelligence":

    st.markdown(
        "<div class='eyebrow'>MANAGEMENT INTELLIGENCE</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='section-title'>FOYUMI Business Intelligence</div>",
        unsafe_allow_html=True
    )

    st.write(
        "A management view of realized booking activity, "
        "customer participation and business performance."
    )

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("Completed bookings", f"{TOTAL_COMPLETED:,}", "Realized booking demand"),
        ("Customers", f"{CUSTOMERS_COMPLETED:,}", "Customers with completed bookings"),
        ("Completed value", f"₦{COMPLETED_VALUE:,.0f}", "Completed appointment value"),
        ("Repeat customers", f"{REPEAT_CUSTOMERS:,}", "Customers with repeat bookings")
    ]

    for col, (label, value, note) in zip(
        [c1, c2, c3, c4],
        metrics
    ):

        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-note">{note}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        "<div class='section-title'>Historical booking demand</div>",
        unsafe_allow_html=True
    )

    if monthly is not None and len(monthly) > 0:

        date_candidates = [
            x for x in monthly.columns
            if "month" in x.lower() or "date" in x.lower()
        ]

        value_candidates = [
            x for x in monthly.columns
            if "completed" in x.lower() and
            ("booking" in x.lower() or "count" in x.lower())
        ]

        if date_candidates and value_candidates:

            mdate = date_candidates[0]
            mvalue = value_candidates[0]

            chart_df = monthly.copy()
            chart_df[mdate] = pd.to_datetime(
                chart_df[mdate],
                errors="coerce"
            )

            chart_df = chart_df.dropna(subset=[mdate])

            fig = px.line(
                chart_df,
                x=mdate,
                y=mvalue,
                markers=True
            )

            fig.update_traces(
                line=dict(color=PEACH, width=3),
                marker=dict(color=BROWN, size=7)
            )

            fig.update_layout(
                height=430,
                paper_bgcolor="white",
                plot_bgcolor="white",
                font=dict(color=BROWN),
                xaxis_title="Month",
                yaxis_title="Completed Bookings"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.markdown(
        """
        <div class="insight-card">
        <b>Management insight:</b>
        Revenue is intentionally treated as a diagnostic business
        measure rather than the forecasting target. Booking volume
        provides a more direct operational measure of realized demand
        when service prices can change over time.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CUSTOMER INTELLIGENCE
# ============================================================

elif page == "Customer Intelligence":

    st.markdown(
        "<div class='eyebrow'>CUSTOMER 360</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='section-title'>Customer Intelligence</div>",
        unsafe_allow_html=True
    )

    st.write(
        "RFM analysis converts historical booking behaviour into "
        "customer-management segments."
    )

    rfm_counts = pd.DataFrame({
        "Segment": [
            "Champions",
            "Active",
            "At Risk",
            "Low Engagement",
            "No Completed Booking"
        ],
        "Customers": [47, 41, 60, 87, 44]
    })

    fig = px.bar(
        rfm_counts,
        x="Segment",
        y="Customers"
    )

    fig.update_traces(
        marker_color=[
            BROWN,
            SAGE,
            PEACH,
            BLUE,
            NUDE
        ]
    )

    fig.update_layout(
        height=420,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=BROWN),
        xaxis_title="",
        yaxis_title="Customers"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        "<div class='section-title'>Customer value distribution</div>",
        unsafe_allow_html=True
    )

    value_df = pd.DataFrame({
        "Segment": [
            "Champions",
            "Active",
            "At Risk",
            "Low Engagement",
            "No Completed Booking"
        ],
        "Completed Value": [
            14_428_500,
            3_886_000,
            5_585_000,
            4_455_000,
            0
        ]
    })

    fig2 = px.bar(
        value_df,
        x="Segment",
        y="Completed Value"
    )

    fig2.update_traces(
        marker_color=PEACH
    )

    fig2.update_layout(
        height=420,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=BROWN),
        yaxis_tickprefix="₦",
        yaxis_title="Completed Appointment Value"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.markdown(
        """
        <div class="insight-card">
        <b>Customer-management opportunity:</b>
        47 Champions account for approximately half of completed
        appointment value. This supports differentiated retention
        and relationship strategies rather than treating every
        customer as an identical segment.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='section-title'>Customer Spotlight</div>",
        unsafe_allow_html=True
    )

    spotlight = {
        "Customer": "Braeyilagh Toby",
        "Completed bookings": 21,
        "Completed appointment value": "₦1,645,000",
        "Recency": "2 days",
        "Segment": "Champion"
    }

    a, b = st.columns([1, 2])

    with a:
        if image_files:
            try:
                st.image(
                    str(image_files[min(1, len(image_files)-1)]),
                    use_container_width=True
                )
            except:
                pass

    with b:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="eyebrow">CUSTOMER SPOTLIGHT</div>
                <h2 style="color:{BROWN};">
                    {spotlight["Customer"]}
                </h2>
                <p>
                    <span class="pill">{spotlight["Segment"]}</span>
                </p>
                <p>
                    <b>{spotlight["Completed bookings"]}</b>
                    completed bookings
                </p>
                <p>
                    <b>{spotlight["Completed appointment value"]}</b>
                    completed appointment value
                </p>
                <p>
                    Last completed booking:
                    <b>{spotlight["Recency"]} ago</b>
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# SERVICE INTELLIGENCE
# ============================================================

elif page == "Service Intelligence":

    st.markdown(
        "<div class='eyebrow'>SERVICE & PRICING INTELLIGENCE</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='section-title'>Service Intelligence</div>",
        unsafe_allow_html=True
    )

    st.write(
        "Understanding where completed bookings occur helps FOYUMI "
        "plan capacity, service delivery and future booking strategy."
    )

    service_df = pd.DataFrame({
        "Service": [
            "Studio Makeup",
            "Home Service",
            "Out-of-Port Harcourt",
            "Other / Non-Makeup",
            "Bridal",
            "Hair"
        ],
        "Total": [369, 229, 6, 5, 5, 1],
        "Completed": [290, 180, 3, 1, 0, 0],
        "Completion Rate": [
            78.6, 78.6, 50.0, 20.0, 0.0, 0.0
        ]
    })

    c1, c2 = st.columns(2)

    with c1:

        fig = px.bar(
            service_df,
            x="Service",
            y="Completed"
        )

        fig.update_traces(
            marker_color=PEACH
        )

        fig.update_layout(
            height=430,
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color=BROWN),
            xaxis_title="",
            yaxis_title="Completed Bookings"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:

        fig = px.bar(
            service_df,
            x="Service",
            y="Completion Rate"
        )

        fig.update_traces(
            marker_color=SAGE
        )

        fig.update_layout(
            height=430,
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color=BROWN),
            xaxis_title="",
            yaxis_title="Completion Rate (%)",
            yaxis_range=[0, 100]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown(
        "<div class='section-title'>Home-Service Coverage</div>",
        unsafe_allow_html=True
    )

    axis_df = pd.DataFrame({
        "Home-Service Axis": [
            "GRA / Oroazi / Stadium Road / Ada George",
            "Peter Odili / Woji YKC / Eliozu / Old GRA / Town",
            "Mgbuoba / Rumukoro / Rumudara / Rumuomasi",
            "Out of PH — Isiokpo / Elele",
            "Out of PH — Okrika / Ogoni"
        ],
        "Operational Use": [
            "Core service zone",
            "Core service zone",
            "Core service zone",
            "Out-of-city service",
            "Out-of-city service"
        ]
    })

    st.dataframe(
        axis_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        """
        <div class="insight-card">
        <b>Strategic use:</b>
        Home-service geography can be converted from a booking
        description into an operational planning variable for
        scheduling, travel planning and service-capacity decisions.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# BOOKING INTELLIGENCE
# ============================================================

elif page == "Booking Intelligence":

    st.markdown(
        "<div class='eyebrow'>BOOKING BEHAVIOUR</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='section-title'>Booking Intelligence</div>",
        unsafe_allow_html=True
    )

    st.write(
        "The booking-entry measure distinguishes how a booking entered "
        "FOYUMI's system. It is not treated as a marketing acquisition channel."
    )

    entry_df = pd.DataFrame({
        "Entry Method": [
            "FOYUMI-Assisted",
            "Online / Client-Entered"
        ],
        "Total": [487, 128],
        "Completed": [395, 79],
        "Completion Rate": [81.1, 61.7]
    })

    fig = px.bar(
        entry_df,
        x="Entry Method",
        y="Completion Rate"
    )

    fig.update_traces(
        marker_color=[
            PEACH,
            BLUE
        ]
    )

    fig.update_layout(
        height=430,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=BROWN),
        yaxis_title="Completion Rate (%)",
        yaxis_range=[0, 100]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            """
            <div class="action-card">
                <div class="eyebrow">OBSERVATION</div>
                <div class="action-title">
                    Staff-assisted bookings are prominent
                </div>
                <p>
                    487 bookings were created by FOYUMI compared with
                    128 client-entered online bookings.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            """
            <div class="action-card">
                <div class="eyebrow">INTERVENTION</div>
                <div class="action-title">
                    Improve digital booking capture
                </div>
                <p>
                    A guided booking experience can preserve the
                    convenience of assisted booking while collecting
                    cleaner and more structured customer information.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# DEMAND PLANNER
# ============================================================

elif page == "Demand Planner":

    st.markdown(
        "<div class='eyebrow'>STATISTICAL DEMAND INTELLIGENCE</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='section-title'>Q4 2026 Demand Planner</div>",
        unsafe_allow_html=True
    )

    st.write(
        "A short-horizon operational planning view based on the "
        "validated statistical forecasting work."
    )

    c1, c2, c3, c4 = st.columns(4)

    forecast_metrics = [
        ("October", "5", "Planning range: 0–13"),
        ("November", "18", "Planning range: 10–26"),
        ("December", "37", "Planning range: 29–45"),
        ("Q4 baseline", "60", "Completed bookings")
    ]

    for col, (month, value, note) in zip(
        [c1, c2, c3, c4],
        forecast_metrics
    ):

        with col:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{month}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-note">{note}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    forecast_chart = pd.DataFrame({
        "Month": [
            "October 2026",
            "November 2026",
            "December 2026"
        ],
        "Baseline": [5, 18, 37],
        "Lower": [0, 10, 29],
        "Upper": [13, 26, 45]
    })

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=forecast_chart["Month"],
            y=forecast_chart["Baseline"],
            name="Baseline",
            marker_color=PEACH
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_chart["Month"],
            y=forecast_chart["Upper"],
            mode="markers",
            name="Planning Upper",
            marker=dict(
                color=BROWN,
                size=9
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_chart["Month"],
            y=forecast_chart["Lower"],
            mode="markers",
            name="Planning Lower",
            marker=dict(
                color=SAGE,
                size=9
            )
        )
    )

    fig.update_layout(
        height=450,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=BROWN),
        yaxis_title="Completed Bookings",
        xaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        """
        <div class="insight-card">
        <b>Forecast methodology:</b>
        Seasonal Naïve produced the lowest one-step validation error
        (MAE = 8.00 bookings; RMSE = 10.42) and showed the smallest
        deterioration during the historical stress test. The model
        is therefore used as an operational baseline rather than a
        guarantee of future demand.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="insight-card">
        <b>Important:</b>
        Revenue is deliberately excluded from this forecast because
        service prices can change independently of booking volume.
        The forecast therefore focuses on completed booking demand.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='section-title'>Operational Pipeline</div>",
        unsafe_allow_html=True
    )

    st.info(
        "As of 15 September 2026, one future non-completed appointment "
        "was identified in the operational pipeline. It is kept "
        "separate from the statistical forecast."
    )


# ============================================================
# DATA STRATEGY
# ============================================================

elif page == "Data Strategy":

    st.markdown(
        "<div class='eyebrow'>THE STRATEGIC INTERVENTION</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='section-title'>From Records to Decisions</div>",
        unsafe_allow_html=True
    )

    st.write(
        "The prototype demonstrates the proposed FOYUMI Customer & "
        "Booking Intelligence System."
    )

    stages = [
        (
            "RAW DATA",
            "Appointments, clients and sales",
            PEACH
        ),
        (
            "CLEANING & GOVERNANCE",
            "Standardisation, quality checks and customer identity",
            SAGE
        ),
        (
            "INTEGRATION",
            "Customer_ID and connected datasets",
            BLUE
        ),
        (
            "CUSTOMER INTELLIGENCE",
            "RFM and customer value",
            LAVENDER
        ),
        (
            "SERVICE INTELLIGENCE",
            "Service mix, outcomes and geography",
            NUDE
        ),
        (
            "DEMAND FORECASTING",
            "Statistical booking-demand forecast",
            PEACH
        ),
        (
            "MANAGEMENT ACTION",
            "Planning, retention and operational decisions",
            BROWN
        )
    ]

    for i, (title, description, colour) in enumerate(stages):

        st.markdown(
            f"""
            <div style="
                background:white;
                border-left:6px solid {colour};
                padding:1rem 1.25rem;
                margin:0.55rem 0;
                border-radius:10px;
                border-top:1px solid #E9DDD7;
                border-right:1px solid #E9DDD7;
                border-bottom:1px solid #E9DDD7;
            ">
                <b style="color:{BROWN};">{i+1:02d} — {title}</b>
                <br>
                <span style="color:#6E625E;">
                    {description}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        "<div class='section-title'>Management actions enabled</div>",
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    with a:
        st.markdown(
            """
            <div class="action-card">
                <div class="action-title">Customer Retention</div>
                <p>
                    Use RFM segments to differentiate retention,
                    reactivation and relationship-management activity.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with b:
        st.markdown(
            """
            <div class="action-card">
                <div class="action-title">Capacity Planning</div>
                <p>
                    Use booking-demand patterns to support staffing,
                    scheduling and service-capacity decisions.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c:
        st.markdown(
            """
            <div class="action-card">
                <div class="action-title">Data Capture</div>
                <p>
                    Standardise customer, service, booking-entry,
                    cancellation and location information at the
                    point of booking.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        "<div class='section-title'>Data quality principles</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <span class="pill">Customer identity</span>
        <span class="pill">Booking status</span>
        <span class="pill">Service classification</span>
        <span class="pill">Home-service geography</span>
        <span class="pill">Booking entry method</span>
        <span class="pill">Cancellation reasons</span>
        <span class="pill">Auditability</span>
        <span class="pill">Responsible data use</span>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# BOOK YOUR GLAM
# ============================================================

elif page == "Book Your Glam":

    st.markdown(
        "<div class='eyebrow'>CUSTOMER EXPERIENCE + DATA CAPTURE</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='section-title'>Book Your Glam</div>",
        unsafe_allow_html=True
    )

    st.write(
        "This proof-of-concept demonstrates how a customer-facing "
        "booking journey can collect structured information while "
        "keeping the experience simple."
    )

    with st.form("booking_form"):

        st.markdown(
            "### Tell FOYUMI what you need"
        )

        name = st.text_input(
            "Full name"
        )

        contact = st.text_input(
            "Phone or email"
        )

        service_choice = st.selectbox(
            "Service",
            [
                "Studio Makeup",
                "Home Service",
                "Bridal Makeup",
                "Event Guest Makeup",
                "Bridesmaid Makeup"
            ]
        )

        booking_type = st.selectbox(
            "Booking preference",
            [
                "Studio",
                "Home Service"
            ]
        )

        if booking_type == "Home Service":

            axis_choice = st.selectbox(
                "Home-service area",
                [
                    "GRA / Oroazi / Stadium Road / Ada George",
                    "Peter Odili / Woji YKC / Eliozu / Old GRA / Town",
                    "Mgbuoba / Rumukoro / Rumudara / Rumuomasi",
                    "Out of PH — Isiokpo / Elele",
                    "Out of PH — Okrika / Ogoni",
                    "Other / To be confirmed"
                ]
            )

        else:
            axis_choice = "Studio"

        requested_date = st.date_input(
            "Preferred date"
        )

        notes = st.text_area(
            "Additional information"
        )

        submitted = st.form_submit_button(
            "Submit Booking Request",
            use_container_width=True
        )

        if submitted:

            st.success(
                "Booking request captured in the prototype. "
                "In a production implementation, this structured "
                "record would flow into the FOYUMI customer and "
                "booking intelligence system."
            )

            st.session_state["booking_request"] = {
                "name": name,
                "contact": contact,
                "service": service_choice,
                "booking_type": booking_type,
                "area": axis_choice,
                "date": str(requested_date),
                "notes": notes
            }

    st.markdown("---")

    st.markdown(
        "<div class='section-title'>Connect with FOYUMI</div>",
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("### 📸 Instagram")
        st.caption("FOYUMI beauty content & community")

    with c2:
        st.markdown("### 💬 WhatsApp")
        st.caption("Direct booking assistance")

    with c3:
        st.markdown("### ✉️ Contact Us")
        st.caption("Business enquiries & collaborations")


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        FOYUMI INTELLIGENCE • Interactive Strategic Prototype<br>
        Turning Beauty Data Into Better Business Decisions<br><br>
        MSc Data Science Management Strategic Intervention
    </div>
    """,
    unsafe_allow_html=True
)
