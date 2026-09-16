import streamlit as st
import pandas as pd
import base64
import mimetypes
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from PIL import Image

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FOYUMI Business Analytics & Insights",
    page_icon="💄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PATHS
# ============================================================

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
ASSETS = BASE / "assets"
LOGO_DIR = ASSETS / "logo"
IMAGE_DIR = ASSETS / "images"

# Robust asset discovery — supports PNG, JPG, JPEG and WebP.
logo_files = sorted(
    [p for p in LOGO_DIR.iterdir() if p.is_file()]
) if LOGO_DIR.exists() else []

image_files = sorted(
    [
        p for p in IMAGE_DIR.iterdir()
        if p.is_file()
        and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    ]
) if IMAGE_DIR.exists() else []

# Customer-facing booking image.
# This is a dedicated square, top-cropped version of IMG_2151 so the
# subject's full head remains visible while the lower chest is cropped.
BOOKING_IMAGE = IMAGE_DIR / "IMG_2151_BOOKING.webp"


def render_booking_gallery():
    """Render the single booking image with a top-focused crop."""
    if BOOKING_IMAGE.exists():
        try:
            encoded = base64.b64encode(
                BOOKING_IMAGE.read_bytes()
            ).decode("ascii")

            st.markdown(
                f'<div class="booking-gallery single">'
                f'<img src="data:image/webp;base64,{encoded}" '
                f'alt="FOYUMI beauty work">'
                f'</div>',
                unsafe_allow_html=True,
            )
            return
        except Exception:
            pass

    st.markdown(
        """
        <div class="booking-gallery single"
             style="display:flex;align-items:center;justify-content:center;">
            <div style="text-align:center;padding:2rem;color:#786B66;">
                <div style="font-size:0.72rem;letter-spacing:0.16em;
                            text-transform:uppercase;font-weight:700;">
                    FOYUMI
                </div>
                <div style="margin-top:0.5rem;">
                    Your glam journey starts here.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
WHITE = "#FFFFFF"
BORDER = "#E8DDD8"
TEXT = "#625752"
MUTED = "#786B66"

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
        border-right: 1px solid {BORDER};
    }}

    .main-title {{
        font-size: 3.15rem;
        font-weight: 700;
        color: {BROWN};
        line-height: 1.05;
        margin-bottom: 0.4rem;
    }}

    .subtitle {{
        font-size: 1.15rem;
        color: #6E625E;
        max-width: 780px;
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
        margin-bottom: 0.6rem;
    }}

    .section-text {{
        color: {TEXT};
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
        color: {MUTED};
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
        margin: 0.7rem 0;
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
            rgba(255,255,255,0.97),
            rgba(244,238,234,0.94)
        );
        border-radius: 24px;
        padding: 3rem;
        margin-bottom: 2rem;
        border: 1px solid {BORDER};
    }}

    .audience-card {{
        background: white;
        padding: 1.6rem;
        border-radius: 18px;
        border: 1px solid #E9DDD7;
        min-height: 215px;
        box-shadow: 0 3px 14px rgba(80,50,40,0.04);
    }}

    .audience-title {{
        color: {BROWN};
        font-size: 1.25rem;
        font-weight: 700;
        margin: 0.45rem 0;
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

    /* BOOK YOUR GLAM — aligned image + form layout */
    .booking-gallery {{
        width: 100%;
        height: 690px;
        overflow: hidden;
        border: 1px solid #E8DDD8;
        border-radius: 16px;
        background: white;
        box-sizing: border-box;
    }}

    .booking-gallery.single {{
        height: 690px;
    }}

    .booking-gallery.two {{
        display: grid;
        grid-template-rows: 1fr 1fr;
        gap: 10px;
        padding: 10px;
    }}

    .booking-gallery img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: top center;
        display: block;
        border-radius: 10px;
    }}

    .booking-gallery.two img {{
        min-height: 0;
    }}

    /* The form is intentionally the same visual height as the image panel. */
    div[data-testid="stForm"] {{
        min-height: 690px;
        height: 690px;
        box-sizing: border-box;
        overflow: hidden;
        border-radius: 16px;
        border: 1px solid #E8DDD8;
        background: white;
        padding: 1.15rem 1.25rem 1rem 1.25rem;
    }}

    .booking-note {{
        background: #F4EEEA;
        border-left: 3px solid {PEACH};
        padding: 0.65rem 0.8rem;
        border-radius: 8px;
        color: {TEXT};
        font-size: 0.82rem;
        line-height: 1.45;
        margin-top: 0.25rem;
        margin-bottom: 0.55rem;
    }}

    @media (max-width: 900px) {{
        .booking-gallery,
        .booking-gallery.single,
        div[data-testid="stForm"] {{
            height: auto;
            min-height: 0;
        }}

        .booking-gallery.two {{
            grid-template-rows: 320px 320px;
        }}
    }}

    div[data-testid="stMetric"] {{
        background: white;
        border: 1px solid #E9DDD7;
        padding: 0.75rem;
        border-radius: 14px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# DATA LOADER
# ============================================================

@st.cache_data
def load_data():
    # Public deployment deliberately uses aggregate analytical
    # outputs rather than customer-level source records.
    return None, None, None


appointments, clients, sales = load_data()

# ============================================================
# OPTIONAL ANALYTICAL FILE LOADER
# ============================================================

def find_csv(keywords):
    if not DATA.exists():
        return None

    files = list(DATA.glob("*.csv"))

    for file in files:
        name = file.name.lower()
        if all(keyword.lower() in name for keyword in keywords):
            return file

    return None


@st.cache_data
def load_optional_file(filename):
    try:
        return pd.read_csv(filename)
    except Exception:
        return None


def load_optional(keywords):
    file = find_csv(keywords)
    if file is None:
        return None
    return load_optional_file(file)


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
# VALIDATED MANAGEMENT KPIs
# ============================================================

TOTAL_COMPLETED = 474
CUSTOMERS_COMPLETED = 235
COMPLETED_VALUE = 28_354_500
REPEAT_CUSTOMERS = 86
Q4_FORECAST = 60

# ============================================================
# VALIDATED FORECAST
# ============================================================

forecast_chart = pd.DataFrame(
    {
        "Month": ["October 2026", "November 2026", "December 2026"],
        "Baseline": [5, 18, 37],
        "Lower": [0, 10, 29],
        "Upper": [13, 26, 45],
    }
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    if logo_files:
        try:
            st.image(str(logo_files[0]), use_container_width=True)
        except Exception:
            pass

    st.markdown(
        "<div class='eyebrow'>FOYUMI</div>",
        unsafe_allow_html=True,
    )

    st.markdown("### Business Analytics & Insights")

    st.caption(
        "A management dashboard for understanding business performance, "
        "customer behaviour, service activity and booking demand."
    )

    st.divider()

    page = st.radio(
        "Navigate",
        [
            "Home",
            "Business Performance",
            "Customer Insights",
            "Service Performance",
            "Booking Insights",
            "Demand Planning",
            "Business & Data Strategy",
            "Book Your Glam",
        ],
    )

    st.divider()

    st.caption(
        "Management prototype built from validated aggregate business "
        "analysis derived from FOYUMI appointment, customer and sales data."
    )

# ============================================================
# HOME
# ============================================================

if page == "Home":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">FOYUMI • BUSINESS ANALYTICS & INSIGHTS</div>
            <div class="main-title">
                FOYUMI
            </div>
            <p class="subtitle">
                Business performance insights designed to help FOYUMI
                understand its customers, monitor its services and make
                more informed business decisions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.2, 1])

    with left:
        st.markdown(
            """
            <div class="section-title">More than makeup.</div>

            <p class="section-text">
                FOYUMI is a professional makeup artistry business serving
                studio, home-service and bridal clients. As the business
                grows, its operational records become an increasingly
                valuable source of business information.
            </p>

            <p class="section-text">
                The opportunity is to move beyond simply recording bookings
                and use those records to understand customer behaviour,
                service performance, booking activity and future demand.
            </p>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="insight-card">
                <b>Business objective:</b>
                Turn existing operational data into practical information
                that supports customer retention, service planning,
                booking management and demand planning.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        if image_files:
            try:
                st.image(
                    str(image_files[0]),
                    use_container_width=True,
                )
            except Exception:
                pass

    st.markdown("---")

    st.markdown(
        "<div class='section-title'>Choose your experience</div>",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            <div class="audience-card">
                <div class="eyebrow">FOR MANAGEMENT</div>
                <div class="audience-title">
                    Business Analytics & Insights
                </div>
                <p class="section-text">
                    Understand performance, customers, services, booking
                    behaviour and demand through a single management view.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "View Business Dashboard →",
            use_container_width=True,
            key="management_home",
        ):
            st.info(
                "Use the navigation menu to explore Business Performance, "
                "Customer Insights, Service Performance, Booking Insights "
                "and Demand Planning."
            )

    with c2:
        st.markdown(
            """
            <div class="audience-card">
                <div class="eyebrow">FOR CLIENTS</div>
                <div class="audience-title">
                    Book Your Glam
                </div>
                <p class="section-text">
                    Explore a simple customer booking journey for studio,
                    home-service and bridal beauty appointments.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Book Your Glam →",
            use_container_width=True,
            key="booking_home",
        ):
            st.info(
                "Select 'Book Your Glam' from the navigation menu to "
                "explore the proposed customer booking journey."
            )

    st.markdown("---")

    st.markdown(
        "<div class='section-title'>The business pathway</div>",
        unsafe_allow_html=True,
    )

    cols = st.columns(6)

    stages = [
        ("01", "DATA", "Capture"),
        ("02", "INTEGRATION", "Connect"),
        ("03", "CUSTOMER", "Understand"),
        ("04", "SERVICE", "Improve"),
        ("05", "DEMAND", "Plan"),
        ("06", "ACTION", "Decide"),
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
                unsafe_allow_html=True,
            )

# ============================================================
# BUSINESS PERFORMANCE
# ============================================================

elif page == "Business Performance":

    st.markdown(
        "<div class='eyebrow'>MANAGEMENT VIEW</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='section-title'>Business Performance</div>",
        unsafe_allow_html=True,
    )

    st.write(
        "A management view of realized booking activity, customer "
        "participation and completed appointment value."
    )

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        (
            "Completed bookings",
            f"{TOTAL_COMPLETED:,}",
            "Bookings reaching Completed status",
        ),
        (
            "Customers",
            f"{CUSTOMERS_COMPLETED:,}",
            "Customers with completed bookings",
        ),
        (
            "Completed value",
            f"₦{COMPLETED_VALUE:,.0f}",
            "Completed appointment value",
        ),
        (
            "Repeat customers",
            f"{REPEAT_CUSTOMERS:,}",
            "Customers with repeat bookings",
        ),
    ]

    for col, (label, value, note) in zip(
        [c1, c2, c3, c4], metrics
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
                unsafe_allow_html=True,
            )

    st.markdown(
        "<div class='section-title'>Historical booking demand</div>",
        unsafe_allow_html=True,
    )

    if monthly is not None and len(monthly) > 0:

        date_candidates = [
            x for x in monthly.columns
            if "month" in x.lower() or "date" in x.lower()
        ]

        value_candidates = [
            x for x in monthly.columns
            if "completed" in x.lower()
            and ("booking" in x.lower() or "count" in x.lower())
        ]

        if date_candidates and value_candidates:

            mdate = date_candidates[0]
            mvalue = value_candidates[0]

            chart_df = monthly.copy()
            chart_df[mdate] = pd.to_datetime(
                chart_df[mdate], errors="coerce"
            )
            chart_df = chart_df.dropna(subset=[mdate])

            fig = px.line(
                chart_df,
                x=mdate,
                y=mvalue,
                markers=True,
            )

            fig.update_traces(
                line=dict(color=PEACH, width=3),
                marker=dict(color=BROWN, size=7),
            )

            fig.update_layout(
                height=430,
                paper_bgcolor="white",
                plot_bgcolor="white",
                font=dict(color=BROWN),
                xaxis_title="Month",
                yaxis_title="Completed Bookings",
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info(
                "The public deployment does not currently include the "
                "monthly aggregate file. The validated KPI view remains "
                "available above."
            )
    else:
        st.info(
            "Historical monthly detail is retained in the analytical "
            "working model; this public prototype intentionally uses "
            "aggregate management outputs."
        )

    st.markdown(
        """
        <div class="insight-card">
        <b>Management insight:</b>
        Revenue is treated as a diagnostic business measure rather than
        the forecasting target. Booking volume provides a more direct
        operational measure of realized demand when service prices can
        change over time.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# CUSTOMER INSIGHTS
# ============================================================

elif page == "Customer Insights":

    st.markdown(
        "<div class='eyebrow'>CUSTOMER INSIGHTS</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='section-title'>Customer Insights</div>",
        unsafe_allow_html=True,
    )

    st.write(
        "RFM analysis converts historical booking behaviour into "
        "customer-management segments."
    )

    rfm_counts = pd.DataFrame(
        {
            "Segment": [
                "Champions",
                "Active",
                "At Risk",
                "Low Engagement",
                "No Completed Booking",
            ],
            "Customers": [47, 41, 60, 87, 44],
        }
    )

    fig = px.bar(
        rfm_counts,
        x="Segment",
        y="Customers",
    )

    fig.update_traces(
        marker_color=[
            BROWN,
            SAGE,
            PEACH,
            BLUE,
            NUDE,
        ]
    )

    fig.update_layout(
        height=420,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=BROWN),
        xaxis_title="",
        yaxis_title="Customers",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "<div class='section-title'>Customer value distribution</div>",
        unsafe_allow_html=True,
    )

    value_df = pd.DataFrame(
        {
            "Segment": [
                "Champions",
                "Active",
                "At Risk",
                "Low Engagement",
                "No Completed Booking",
            ],
            "Completed Value": [
                14_428_500,
                3_886_000,
                5_585_000,
                4_455_000,
                0,
            ],
        }
    )

    fig2 = px.bar(
        value_df,
        x="Segment",
        y="Completed Value",
    )

    fig2.update_traces(marker_color=PEACH)

    fig2.update_layout(
        height=420,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=BROWN),
        yaxis_tickprefix="₦",
        yaxis_title="Completed Appointment Value",
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(
        """
        <div class="insight-card">
        <b>Customer-management opportunity:</b>
        47 Champion customers account for approximately half of completed
        appointment value. This supports differentiated retention and
        relationship-management activity rather than treating every
        customer as an identical segment.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='section-title'>Illustrative customer profile</div>",
        unsafe_allow_html=True,
    )

    # Public-safe: no real customer name or personally identifiable
    # information is displayed.
    spotlight = {
        "Customer": "Champion Customer Profile",
        "Completed bookings": 21,
        "Completed appointment value": "₦1,645,000",
        "Recency": "2 days",
        "Segment": "Champion",
    }

    a, b = st.columns([1, 2])

    with a:
        if len(image_files) > 1:
            try:
                st.image(
                    str(image_files[1]),
                    use_container_width=True,
                )
            except Exception:
                pass

    with b:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="eyebrow">ILLUSTRATIVE CHAMPION PROFILE</div>
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
            unsafe_allow_html=True,
        )

    st.caption(
        "Illustrative profile shown for demonstration; customer identity "
        "is intentionally anonymized in the public prototype."
    )

# ============================================================
# SERVICE PERFORMANCE
# ============================================================

elif page == "Service Performance":

    st.markdown(
        "<div class='eyebrow'>SERVICE PERFORMANCE</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='section-title'>Service Performance</div>",
        unsafe_allow_html=True,
    )

    st.write(
        "Understanding where completed bookings occur helps FOYUMI "
        "plan capacity, service delivery and future booking strategy."
    )

    service_df = pd.DataFrame(
        {
            "Service": [
                "Studio Makeup",
                "Home Service",
                "Out-of-Port Harcourt",
                "Other / Non-Makeup",
                "Bridal",
                "Hair",
            ],
            "Total": [369, 229, 6, 5, 5, 1],
            "Completed": [290, 180, 3, 1, 0, 0],
            "Completion Rate": [78.6, 78.6, 50.0, 20.0, 0.0, 0.0],
        }
    )

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            service_df,
            x="Service",
            y="Completed",
        )

        fig.update_traces(marker_color=PEACH)

        fig.update_layout(
            height=430,
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color=BROWN),
            xaxis_title="",
            yaxis_title="Completed Bookings",
        )

        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.bar(
            service_df,
            x="Service",
            y="Completion Rate",
        )

        fig.update_traces(marker_color=SAGE)

        fig.update_layout(
            height=430,
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color=BROWN),
            xaxis_title="",
            yaxis_title="Completion Rate (%)",
            yaxis_range=[0, 100],
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "<div class='section-title'>Home-Service Coverage</div>",
        unsafe_allow_html=True,
    )

    axis_df = pd.DataFrame(
        {
            "Home-Service Axis": [
                "GRA / Oroazi / Stadium Road / Ada George",
                "Peter Odili / Woji YKC / Eliozu / Old GRA / Town",
                "Mgbuoba / Rumukoro / Rumudara / Rumuomasi",
                "Out of PH — Isiokpo / Elele",
                "Out of PH — Okrika / Ogoni",
            ],
            "Operational Use": [
                "Core service zone",
                "Core service zone",
                "Core service zone",
                "Out-of-city service",
                "Out-of-city service",
            ],
        }
    )

    st.dataframe(
        axis_df,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        """
        <div class="insight-card">
        <b>Strategic use:</b>
        Home-service geography can be converted from a booking description
        into an operational planning variable for scheduling, travel
        planning and service-capacity decisions.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# BOOKING INSIGHTS
# ============================================================

elif page == "Booking Insights":

    st.markdown(
        "<div class='eyebrow'>BOOKING INSIGHTS</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='section-title'>Booking Insights</div>",
        unsafe_allow_html=True,
    )

    st.write(
        "The booking-entry measure distinguishes how a booking entered "
        "FOYUMI's system. It is not treated as a marketing acquisition "
        "channel."
    )

    entry_df = pd.DataFrame(
        {
            "Entry Method": [
                "FOYUMI-Assisted",
                "Online / Client-Entered",
            ],
            "Total": [487, 128],
            "Completed": [395, 79],
            "Completion Rate": [81.1, 61.7],
        }
    )

    fig = px.bar(
        entry_df,
        x="Entry Method",
        y="Completion Rate",
    )

    fig.update_traces(
        marker_color=[PEACH, BLUE]
    )

    fig.update_layout(
        height=430,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=BROWN),
        yaxis_title="Completion Rate (%)",
        yaxis_range=[0, 100],
    )

    st.plotly_chart(fig, use_container_width=True)

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
            unsafe_allow_html=True,
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
                    A guided booking experience can preserve the convenience
                    of assisted booking while collecting cleaner and more
                    structured customer information.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="insight-card">
        <b>Interpretation:</b>
        “FOYUMI-Assisted” means the booking was entered into the system
        by FOYUMI staff or management on behalf of the client. It does
        not represent a marketing channel.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# DEMAND PLANNING
# ============================================================

elif page == "Demand Planning":

    st.markdown(
        "<div class='eyebrow'>DEMAND PLANNING</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='section-title'>Q4 2026 Demand Planning</div>",
        unsafe_allow_html=True,
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
        ("Q4 baseline", "60", "Completed bookings"),
    ]

    for col, (month, value, note) in zip(
        [c1, c2, c3, c4], forecast_metrics
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
                unsafe_allow_html=True,
            )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=forecast_chart["Month"],
            y=forecast_chart["Baseline"],
            name="Baseline",
            marker_color=PEACH,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_chart["Month"],
            y=forecast_chart["Upper"],
            mode="markers",
            name="Planning Upper",
            marker=dict(color=BROWN, size=9),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_chart["Month"],
            y=forecast_chart["Lower"],
            mode="markers",
            name="Planning Lower",
            marker=dict(color=SAGE, size=9),
        )
    )

    fig.update_layout(
        height=450,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=BROWN),
        yaxis_title="Completed Bookings",
        xaxis_title="",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        <div class="insight-card">
        <b>Forecast methodology:</b>
        Seasonal Naïve produced the lowest one-step validation error
        (MAE = 8.00 bookings; RMSE = 10.42) and showed the smallest
        deterioration during the historical stress test. It is therefore
        used as an operational baseline rather than a guarantee of future
        demand.
        </div>
        """,
        unsafe_allow_html=True,
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
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='section-title'>Operational Pipeline</div>",
        unsafe_allow_html=True,
    )

    st.info(
        "As of 15 September 2026, one future non-completed appointment "
        "was identified in the operational pipeline. It is kept separate "
        "from the statistical forecast."
    )

# ============================================================
# BUSINESS & DATA STRATEGY
# ============================================================

elif page == "Business & Data Strategy":

    st.markdown(
        "<div class='eyebrow'>STRATEGIC INTERVENTION</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='section-title'>From Records to Decisions</div>",
        unsafe_allow_html=True,
    )

    st.write(
        "The prototype demonstrates the proposed FOYUMI Customer & "
        "Booking Intelligence System as a business and data-management "
        "intervention."
    )

    stages = [
        ("RAW DATA", "Appointments, clients and sales", PEACH),
        (
            "CLEANING & GOVERNANCE",
            "Standardisation, quality checks and customer identity",
            SAGE,
        ),
        (
            "INTEGRATION",
            "Customer_ID and connected datasets",
            BLUE,
        ),
        (
            "CUSTOMER INSIGHTS",
            "RFM and customer value",
            LAVENDER,
        ),
        (
            "SERVICE PERFORMANCE",
            "Service mix, outcomes and geography",
            NUDE,
        ),
        (
            "DEMAND PLANNING",
            "Statistical booking-demand forecast",
            PEACH,
        ),
        (
            "MANAGEMENT ACTION",
            "Planning, retention and operational decisions",
            BROWN,
        ),
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
                <b style="color:{BROWN};">
                    {i+1:02d} — {title}
                </b>
                <br>
                <span style="color:#6E625E;">
                    {description}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div class='section-title'>Management actions enabled</div>",
        unsafe_allow_html=True,
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
            unsafe_allow_html=True,
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
            unsafe_allow_html=True,
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
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div class='section-title'>Data quality principles</div>",
        unsafe_allow_html=True,
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
        unsafe_allow_html=True,
    )

# ============================================================
# BOOK YOUR GLAM
# ============================================================

elif page == "Book Your Glam":

    st.markdown(
        "<div class='eyebrow'>FOYUMI CUSTOMER EXPERIENCE</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='section-title'>Book Your Glam</div>",
        unsafe_allow_html=True,
    )

    st.write(
        "Tell us where you would like your makeup done and what the "
        "occasion is. Our team will follow up to confirm the details "
        "and applicable service requirements."
    )

    # Image and form sit beside each other at equal desktop height.
    image_col, form_col = st.columns([1, 1], gap="large")

    with image_col:
        render_booking_gallery()

    with form_col:

        with st.form("booking_form"):

            st.markdown("### Tell FOYUMI what you need")

            name = st.text_input("Full name")
            contact = st.text_input("Phone or email")

            st.markdown("#### Where would you like your makeup done?")

            booking_location = st.radio(
                "Booking location",
                ["Studio", "Home Service"],
                horizontal=True,
                label_visibility="collapsed",
            )

            st.markdown(
                """
                <div class="booking-note">
                    <strong>Home Service:</strong> We will confirm your exact
                    location and the applicable home-service rate after your request.
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("#### What is the occasion?")

            makeup_occasion = st.selectbox(
                "Makeup occasion",
                [
                    "Event Guest",
                    "Bridesmaid",
                    "Birthday",
                    "Clubbing / Night Out",
                    "Other",
                ],
                label_visibility="collapsed",
            )

            requested_date = st.date_input("Preferred date")

            notes = st.text_area(
                "Additional information",
                placeholder=(
                    "Tell us anything we should know about your booking, "
                    "such as your event time, preferred look or other details."
                ),
            )

            submitted = st.form_submit_button(
                "Submit Booking Request",
                use_container_width=True,
            )

            if submitted:
                if not name.strip() or not contact.strip():
                    st.warning(
                        "Please provide your name and a phone number or email "
                        "so FOYUMI can follow up on the request."
                    )
                else:
                    st.success(
                        "Booking request captured in the prototype. "
                        "FOYUMI will follow up to confirm your location, "
                        "availability and booking details."
                    )

                    st.session_state["booking_request"] = {
                        "name": name,
                        "contact": contact,
                        "booking_location": booking_location,
                        "makeup_occasion": makeup_occasion,
                        "date": str(requested_date),
                        "notes": notes,
                    }

    # Full-width section underneath both the image and the form.
    st.markdown("---")

    st.markdown(
        "<div class='section-title'>What happens next?</div>",
        unsafe_allow_html=True,
    )

    step1, step2, step3 = st.columns(3)

    with step1:
        st.markdown(
            """
            <div class="action-card">
                <div class="eyebrow">01</div>
                <div class="action-title">Send your request</div>
                <p>
                    Tell FOYUMI your preferred makeup location and occasion.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with step2:
        st.markdown(
            """
            <div class="action-card">
                <div class="eyebrow">02</div>
                <div class="action-title">We confirm the details</div>
                <p>
                    For Home Service, FOYUMI confirms your exact location
                    and the applicable service requirements.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with step3:
        st.markdown(
            """
            <div class="action-card">
                <div class="eyebrow">03</div>
                <div class="action-title">Your glam is confirmed</div>
                <p>
                    Once availability and booking details are agreed,
                    your appointment can be confirmed.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.markdown(
        "<div class='section-title'>Connect with FOYUMI</div>",
        unsafe_allow_html=True,
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
        FOYUMI • Business Analytics & Insights<br>
        Business performance dashboard<br><br>
        MSc Data Science Management Strategic Intervention
    </div>
    """,
    unsafe_allow_html=True,
)
