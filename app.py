import pandas as pd
import plotly.express as px
import streamlit as st

from src.ai_assistant import generate_resolution_plan
from src.database import (
    clear_resolutions,
    get_resolutions,
    save_resolution,
)
from src.exception_rules import analyze_orders

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ERP Order Exception Monitor",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# COLOR SYSTEM
# Deep Maritime & Wine
# =========================================================

DEEP_NAVY = "#0B132B"
ABYSSAL_BLUE = "#1C2541"
SEA_SALT = "#F5F2EB"
ELECTRIC_TEAL = "#00A896"
PALE_MINT = "#84E2D8"
WINE_BURGUNDY = "#660033"


# =========================================================
# TYPOGRAPHY + GLOBAL STYLING
# =========================================================

st.markdown(
    f"""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* -----------------------------------------------------
       GLOBAL APPLICATION
       ----------------------------------------------------- */

    .stApp {{
        background-color: {DEEP_NAVY};
        color: {SEA_SALT};
    }}

    .main .block-container {{
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}

    /* -----------------------------------------------------
       TYPOGRAPHY SYSTEM
       ----------------------------------------------------- */

    html,
    body,
    [class*="css"] {{
        font-family:
            "Inter",
            "IBM Plex Sans",
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }}

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {{
        font-family:
            "Inter",
            "IBM Plex Sans",
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif !important;

        font-weight: 600 !important;
        letter-spacing: -0.02em;
        color: {SEA_SALT} !important;
    }}

    h1 {{
        text-align: center;
        font-size: 2.2rem !important;
        line-height: 1.2;
        margin-bottom: 0.5rem;
    }}

    h2,
    h3,
    h4 {{
        text-align: left;
    }}

    label,
    button,
    input,
    textarea,
    select {{
        font-family:
            "Inter",
            "IBM Plex Sans",
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif !important;
    }}

    /* Numerical and operational data */

    .data-value,
    .metric-value,
    .order-id,
    .sku,
    .tracking-id,
    .timestamp,
    .numeric-data {{
        font-family:
            "JetBrains Mono",
            "SFMono-Regular",
            Consolas,
            "Liberation Mono",
            monospace !important;

        font-variant-numeric: tabular-nums;
    }}

    [data-testid="stMetricValue"] {{
        font-family:
            "JetBrains Mono",
            "SFMono-Regular",
            Consolas,
            monospace !important;

        font-variant-numeric: tabular-nums;
        letter-spacing: -0.02em;
        color: {SEA_SALT} !important;
    }}

    [data-testid="stMetricLabel"] {{
        font-family:
            "Inter",
            "IBM Plex Sans",
            sans-serif !important;

        color: {PALE_MINT} !important;
        font-weight: 500 !important;
    }}

    /* -----------------------------------------------------
       BODY TEXT
       ----------------------------------------------------- */

    .stApp p,
    .stApp li {{
        color: {SEA_SALT};
        font-family:
            "Inter",
            "IBM Plex Sans",
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }}

    /* -----------------------------------------------------
       SIDEBAR
       ----------------------------------------------------- */

    section[data-testid="stSidebar"] {{
        background-color: {ABYSSAL_BLUE};
        border-right: 1px solid rgba(132, 226, 216, 0.12);
    }}

    section[data-testid="stSidebar"] * {{
        color: {SEA_SALT};
    }}

    /* -----------------------------------------------------
       PAGE HEADER
       ----------------------------------------------------- */

    .page-subtitle {{
        text-align: center;
        color: {PALE_MINT};
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 2rem;
        font-weight: 400;
        letter-spacing: 0.01em;
    }}

    /* -----------------------------------------------------
       KPI CARDS
       ----------------------------------------------------- */

    div[data-testid="stMetric"] {{
        background-color: {ABYSSAL_BLUE};
        border: 1px solid rgba(132, 226, 216, 0.10);
        border-radius: 8px;
        padding: 18px 20px;
    }}

    /* -----------------------------------------------------
       SELECT BOXES / INPUTS
       ----------------------------------------------------- */

    div[data-baseweb="select"] > div {{
        background-color: {ABYSSAL_BLUE};
        border-color: rgba(132, 226, 216, 0.18);
        color: {SEA_SALT};
    }}

    div[data-baseweb="select"] span {{
        color: {SEA_SALT};
    }}

    div[data-baseweb="input"] > div {{
        background-color: {ABYSSAL_BLUE};
        border-color: rgba(132, 226, 216, 0.18);
    }}

    /* -----------------------------------------------------
       ACTION TAKEN TEXT AREA
       ----------------------------------------------------- */

    .stTextArea textarea {{
        background-color: {ABYSSAL_BLUE} !important;
        color: {SEA_SALT} !important;
        caret-color: {PALE_MINT} !important;
        border: 1px solid rgba(132, 226, 216, 0.25) !important;
        border-radius: 6px !important;

        font-family:
            "Inter",
            "IBM Plex Sans",
            sans-serif !important;

        font-size: 0.92rem !important;
    }}

    .stTextArea textarea::placeholder {{
        color: {PALE_MINT} !important;
        opacity: 0.75 !important;
    }}

    .stTextArea textarea:focus {{
        border-color: {ELECTRIC_TEAL} !important;
        box-shadow: 0 0 0 1px {ELECTRIC_TEAL} !important;
    }}

    /* -----------------------------------------------------
       BUTTONS
       ----------------------------------------------------- */

    .stButton > button {{
        background-color: {ABYSSAL_BLUE};
        color: {SEA_SALT};
        border: 1px solid rgba(132, 226, 216, 0.20);
        border-radius: 6px;

        font-family:
            "Inter",
            "IBM Plex Sans",
            sans-serif;

        font-weight: 500;
        transition: all 0.15s ease;
    }}

    .stButton > button:hover {{
        background-color: {DEEP_NAVY};
        color: {ELECTRIC_TEAL};
        border-color: {ELECTRIC_TEAL};
    }}

    .stButton > button[kind="primary"] {{
        background-color: {ELECTRIC_TEAL};
        color: {DEEP_NAVY};
        border-color: {ELECTRIC_TEAL};
        font-weight: 600;
    }}

    .stButton > button[kind="primary"]:hover {{
        background-color: {PALE_MINT};
        color: {DEEP_NAVY};
        border-color: {PALE_MINT};
    }}

    /* -----------------------------------------------------
       ALERTS / INFO
       ----------------------------------------------------- */

    div[data-testid="stAlert"] {{
        background-color: {ABYSSAL_BLUE};
        border: 1px solid rgba(132, 226, 216, 0.12);
        color: {SEA_SALT};
    }}

    div[data-testid="stAlert"] p {{
        color: {SEA_SALT} !important;
    }}

    /* -----------------------------------------------------
       TABLES
       ----------------------------------------------------- */

    [data-testid="stDataFrame"] {{
        background-color: {ABYSSAL_BLUE};
        border-radius: 8px;
        overflow: hidden;
    }}

    [data-testid="stDataFrame"] td {{
        font-variant-numeric: tabular-nums;
    }}

    /* -----------------------------------------------------
       DIVIDERS
       ----------------------------------------------------- */

    hr {{
        border-color: rgba(132, 226, 216, 0.15);
    }}

    /* -----------------------------------------------------
       SECTION LABELS
       ----------------------------------------------------- */

    .section-label {{
        color: {PALE_MINT};
        font-family:
            "Inter",
            "IBM Plex Sans",
            sans-serif;
        font-size: 0.76rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.4rem;
    }}

    /* -----------------------------------------------------
       PRIORITY BADGES
       ----------------------------------------------------- */

    .priority-high {{
        display: inline-block;
        background-color: {WINE_BURGUNDY};
        color: {SEA_SALT};
        padding: 4px 10px;
        border-radius: 4px;

        font-family:
            "Inter",
            "IBM Plex Sans",
            sans-serif;

        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }}

    .priority-medium {{
        display: inline-block;
        background-color: rgba(132, 226, 216, 0.16);
        color: {PALE_MINT};
        padding: 4px 10px;
        border-radius: 4px;

        font-family:
            "Inter",
            "IBM Plex Sans",
            sans-serif;

        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }}

    .priority-low {{
        display: inline-block;
        background-color: rgba(132, 226, 216, 0.08);
        color: {PALE_MINT};
        padding: 4px 10px;
        border-radius: 4px;

        font-family:
            "Inter",
            "IBM Plex Sans",
            sans-serif;

        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }}

    /* -----------------------------------------------------
       DETAIL CARD
       ----------------------------------------------------- */

    .detail-card {{
        background-color: {ABYSSAL_BLUE};
        border: 1px solid rgba(132, 226, 216, 0.10);
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 18px;
    }}

    .detail-label {{
        color: {PALE_MINT} !important;
        font-family:
            "Inter",
            "IBM Plex Sans",
            sans-serif;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 3px;
    }}

    .detail-value {{
        color: {SEA_SALT} !important;
        font-family:
            "Inter",
            "IBM Plex Sans",
            sans-serif;
        font-size: 0.92rem;
        line-height: 1.45;
    }}

    .detail-number {{
        color: {SEA_SALT} !important;
        font-family:
            "JetBrains Mono",
            "SFMono-Regular",
            Consolas,
            monospace;

        font-size: 0.92rem;
        font-variant-numeric: tabular-nums;
    }}

    /* -----------------------------------------------------
       RECOMMENDATION CARD
       ----------------------------------------------------- */

    .recommendation-card {{
        background-color: {ABYSSAL_BLUE};
        border-left: 4px solid {ELECTRIC_TEAL};
        border-radius: 8px;
        padding: 14px 18px;
        margin: 14px 0 18px 0;
    }}

    .recommendation-title {{
        color: {PALE_MINT};
        font-family:
            "Inter",
            "IBM Plex Sans",
            sans-serif;
        font-size: 0.76rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 5px;
    }}

    .recommendation-text {{
        color: {SEA_SALT};
        font-family:
            "Inter",
            "IBM Plex Sans",
            sans-serif;
        font-size: 0.92rem;
        line-height: 1.55;
    }}

    /* -----------------------------------------------------
       RESOLUTION STATUS
       ----------------------------------------------------- */

    .status-open {{
        color: {WINE_BURGUNDY};
        font-weight: 600;
    }}

    .status-progress {{
        color: {PALE_MINT};
        font-weight: 600;
    }}

    .status-resolved {{
        color: {ELECTRIC_TEAL};
        font-weight: 600;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DATA LOADING
# =========================================================


@st.cache_data
def load_orders():
    return pd.read_csv("data/erp_orders.csv")


orders = load_orders()

exceptions = analyze_orders(orders)


# Clear resolution history when a new app session starts.
if "history_initialized" not in st.session_state:
    clear_resolutions()
    st.session_state["history_initialized"] = True

resolutions = get_resolutions()


# =========================================================
# PAGE HEADER
# =========================================================

st.title("ERP Order Exception Monitor")

st.markdown(
    """
    <div class="page-subtitle">
        Detect operational exceptions, investigate root causes,
        and take corrective action across ERP order workflows.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_exceptions = len(exceptions)

resolved_count = 0
in_progress_count = 0

if not resolutions.empty:
    resolved_count = len(resolutions[resolutions["status"] == "Resolved"])

    in_progress_count = len(resolutions[resolutions["status"] == "In Progress"])

open_count = max(
    total_exceptions - resolved_count - in_progress_count,
    0,
)


# =========================================================
# KPI DISPLAY
# =========================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "Total Exceptions",
        total_exceptions,
    )

with kpi2:
    st.metric(
        "Open",
        open_count,
    )

with kpi3:
    st.metric(
        "In Progress",
        in_progress_count,
    )

with kpi4:
    st.metric(
        "Resolved",
        resolved_count,
    )


st.divider()


# =========================================================
# FILTERS
# =========================================================

st.markdown(
    '<div class="section-label">Exception Filters</div>',
    unsafe_allow_html=True,
)

filter1, filter2, filter3 = st.columns(3)

with filter1:
    priority_options = [
        "All",
        "High",
        "Medium",
        "Low",
    ]

    selected_priority = st.selectbox(
        "Priority",
        priority_options,
    )


with filter2:
    problem_types = [
        "Inventory Shortage",
        "Delivery Risk",
        "Supplier Performance",
        "Data Quality",
    ]

    available_problem_types = sorted(exceptions["exception_type"].dropna().unique())

    problem_type_options = ["All"] + [
        problem for problem in problem_types if problem in available_problem_types
    ]

    selected_problem_type = st.selectbox(
        "Problem Type",
        problem_type_options,
    )


with filter3:
    region_options = ["All"]

    if "region" in exceptions.columns:
        region_options += sorted(exceptions["region"].dropna().unique().tolist())

    selected_region = st.selectbox(
        "Region",
        region_options,
    )


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_exceptions = exceptions.copy()

if selected_priority != "All":
    filtered_exceptions = filtered_exceptions[
        filtered_exceptions["severity"] == selected_priority
    ]

if selected_problem_type != "All":
    filtered_exceptions = filtered_exceptions[
        filtered_exceptions["exception_type"] == selected_problem_type
    ]

if selected_region != "All":
    filtered_exceptions = filtered_exceptions[
        filtered_exceptions["region"] == selected_region
    ]


st.divider()


# =========================================================
# DETECTED PROBLEMS + CHART
# =========================================================

left_col, right_col = st.columns([1.25, 1])


# =========================================================
# EXCEPTION TABLE
# =========================================================

with left_col:
    st.markdown(
        '<div class="section-label">Detected Problems</div>',
        unsafe_allow_html=True,
    )

    if filtered_exceptions.empty:
        st.info("No exceptions match the selected filters.")

    else:
        display_columns = [
            "order_id",
            "exception_type",
            "severity",
            "customer",
            "product",
            "supplier",
            "region",
            "order_value",
        ]

        display_df = filtered_exceptions[display_columns].copy()

        display_df = display_df.rename(
            columns={
                "order_id": "Order ID",
                "exception_type": "Problem Type",
                "severity": "Priority",
                "customer": "Customer",
                "product": "Product",
                "supplier": "Supplier",
                "region": "Region",
                "order_value": "Order Value",
            }
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# EXCEPTION DISTRIBUTION CHART
# =========================================================

with right_col:
    st.markdown(
        '<div class="section-label">Exception Distribution</div>',
        unsafe_allow_html=True,
    )

    all_problem_types = [
        "Inventory Shortage",
        "Delivery Risk",
        "Supplier Performance",
        "Data Quality",
    ]

    if filtered_exceptions.empty:
        chart_data = pd.DataFrame(
            {
                "Problem Type": all_problem_types,
                "Count": [0, 0, 0, 0],
            }
        )

    else:
        counts = (
            filtered_exceptions["exception_type"]
            .value_counts()
            .reindex(
                all_problem_types,
                fill_value=0,
            )
        )

        chart_data = pd.DataFrame(
            {
                "Problem Type": counts.index,
                "Count": counts.values,
            }
        )

    fig = px.bar(
        chart_data,
        x="Count",
        y="Problem Type",
        orientation="h",
        text="Count",
    )

    fig.update_traces(
        marker_color=ELECTRIC_TEAL,
        textfont={
            "color": SEA_SALT,
            "family": "JetBrains Mono",
        },
    )

    fig.update_layout(
        height=320,
        paper_bgcolor=DEEP_NAVY,
        plot_bgcolor=ABYSSAL_BLUE,
        font={
            "family": "Inter",
            "color": SEA_SALT,
        },
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
        xaxis=dict(
            title=None,
            color=PALE_MINT,
            gridcolor="rgba(132, 226, 216, 0.10)",
            tickfont={
                "family": "JetBrains Mono",
                "color": PALE_MINT,
            },
        ),
        yaxis=dict(
            title=None,
            color=SEA_SALT,
            automargin=True,
            tickfont={
                "family": "Inter",
                "color": SEA_SALT,
            },
        ),
        showlegend=False,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


st.divider()


# =========================================================
# ORDER INVESTIGATION
# =========================================================

st.markdown(
    '<div class="section-label">Order Investigation</div>',
    unsafe_allow_html=True,
)

if filtered_exceptions.empty:
    st.info("No orders are available for investigation " "under the current filters.")

else:
    exception_options = filtered_exceptions["order_id"].tolist()

    selected_order_id = st.selectbox(
        "Select Order",
        exception_options,
        format_func=lambda x: f"Order {x}",
    )

    order_exceptions = filtered_exceptions[
        filtered_exceptions["order_id"] == selected_order_id
    ]

    if not order_exceptions.empty:
        exception_types_for_order = order_exceptions["exception_type"].tolist()

        selected_exception_type = st.selectbox(
            "Select Problem",
            exception_types_for_order,
        )

        selected_exception = order_exceptions[
            order_exceptions["exception_type"] == selected_exception_type
        ].iloc[0]

        # =================================================
        # PROBLEM DETAILS
        # =================================================

        st.markdown("### Problem Details")

        priority = selected_exception["severity"]

        if priority == "High":
            priority_class = "priority-high"
        elif priority == "Medium":
            priority_class = "priority-medium"
        else:
            priority_class = "priority-low"

        st.markdown(
            f"""
            <div class="{priority_class}" style="margin-bottom: 16px;">
            {priority} Priority
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("**Order ID**")

        st.code(
            str(selected_exception["order_id"]),
            language=None,
        )

        st.markdown("**Problem**")

        st.write(selected_exception["problem"])

        st.markdown("**Business Impact**")

        st.write(selected_exception["impact"])

        # =================================================
        # RECOMMENDED FIX
        # =================================================

        st.markdown("### Recommended Fix")

        st.info(selected_exception["recommended_action"])

        # =================================================
        # AI RESOLUTION PLAN
        # =================================================

        st.markdown(
            '<div class="section-label">Resolution Assistance</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "Generate Resolution Plan",
            key="generate_resolution",
        ):
            with st.spinner("Generating resolution plan..."):
                resolution_plan = generate_resolution_plan(selected_exception)

            st.markdown("#### Resolution Summary")

            st.write(resolution_plan["summary"])

            st.markdown("#### Business Impact")

            st.write(resolution_plan["impact"])

            st.markdown("#### Recommended Action")

            st.write(resolution_plan["recommended_action"])

            st.markdown("### Next Steps")

            for index, step in enumerate(
                resolution_plan["next_steps"],
                start=1,
            ):
                st.markdown(f"**{index:02d}**  {step}")

            st.divider()

        # =================================================
        # RESOLUTION WORKFLOW
        # =================================================

        st.markdown(
            '<div class="section-label">Resolution Workflow</div>',
            unsafe_allow_html=True,
        )

        resolution_col1, resolution_col2 = st.columns(2)

        with resolution_col1:
            resolution_status = st.selectbox(
                "Status",
                [
                    "Open",
                    "In Progress",
                    "Resolved",
                ],
                key="resolution_status",
            )

        with resolution_col2:
            resolution_exception_type = st.selectbox(
                "Exception Type",
                [selected_exception_type],
                key="resolution_exception_type",
            )

        action_taken = st.text_area(
            "Action Taken",
            placeholder=(
                "Describe the corrective action taken " "to resolve the exception."
            ),
            key="action_taken",
            height=120,
        )

        if st.button(
            "Save Resolution",
            type="primary",
            key="save_resolution",
        ):
            if not action_taken.strip():
                st.warning("Enter the action taken before " "saving the resolution.")

            else:
                save_resolution(
                    order_id=int(selected_exception["order_id"]),
                    exception_type=(resolution_exception_type),
                    status=resolution_status,
                    action_taken=action_taken.strip(),
                )

                st.success("Resolution updated successfully.")

                st.rerun()


# =========================================================
# RESOLUTION HISTORY
# =========================================================

st.divider()

st.markdown(
    '<div class="section-label">Resolution History</div>',
    unsafe_allow_html=True,
)

resolutions = get_resolutions()

if resolutions.empty:
    st.info("No resolution actions have been recorded yet.")

else:
    history_df = resolutions.copy()

    history_df = history_df.rename(
        columns={
            "id": "ID",
            "order_id": "Order ID",
            "exception_type": "Exception Type",
            "status": "Status",
            "action_taken": "Action Taken",
            "resolved_at": "Resolved At",
        }
    )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True,
    )
