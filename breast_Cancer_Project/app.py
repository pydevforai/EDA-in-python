from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Breast Cancer Insights",
    page_icon="🎗️",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "Breast_Cancer.csv"
STAGE_ORDER = ["IIA", "IIB", "IIIA", "IIIB", "IIIC"]
AGE_ORDER = ["30-39", "40-49", "50-59", "60-69"]
SIZE_ORDER = ["Small", "Medium", "Large"]


def pct(value):
    """Show a number as a percentage with one decimal, e.g. 15.3%."""
    return "—" if pd.isna(value) else f"{value:.1f}%"


def style_percent_chart(fig):
    """Put a % sign on bar labels and on the y-axis."""
    fig.update_traces(texttemplate="%{y:.1f}%", textposition="outside")
    fig.update_yaxes(ticksuffix="%", title="Mortality rate")
    return fig


def mortality_by(data, columns):
    """Mortality % and patient count for every group in the given column(s)."""
    table = (
        data.groupby(columns, observed=True)["Dead"]
        .agg(["mean", "count"])
        .reset_index()
    )
    table["Mortality_Pct"] = table["mean"] * 100
    return table.rename(columns={"count": "Patients"}).drop(columns="mean")


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    """Load the source data and apply the notebook's cleaning and features."""
    data = pd.read_csv(path)
    data = data.drop_duplicates().copy()
    data.columns = data.columns.str.strip()
    data = data.rename(
        columns={
            "Reginol Node Positive": "Nodes_Positive",
            "Regional Node Examined": "Nodes_Examined",
            "6th Stage": "Stage",
            "differentiate": "Differentiate",
        }
    )
    data.columns = data.columns.str.replace(" ", "_")
    for col in data.select_dtypes(exclude="number").columns:
        data[col] = data[col].str.strip()
    data["Grade"] = data["Grade"].replace({"anaplastic; Grade IV": "4"}).astype(int)
    data = data.drop(columns=["Differentiate"])

    data["Dead"] = (data["Status"] == "Dead").astype(int)
    data["Nodes_Ratio"] = data["Nodes_Positive"] / data["Nodes_Examined"] * 100
    data["Age_Group"] = pd.cut(
        data["Age"], bins=[29, 39, 49, 59, 69], labels=AGE_ORDER
    )
    data["Tumor_Size_Group"] = pd.cut(
        data["Tumor_Size"], bins=[0, 20, 50, 200], labels=SIZE_ORDER
    )
    data["Hormone_Profile"] = (
        "ER " + data["Estrogen_Status"] + " / PR " + data["Progesterone_Status"]
    )
    data["Follow_Up_Year"] = data["Survival_Months"] // 12 + 1
    return data


try:
    df = load_data(str(DATA_PATH))
except FileNotFoundError:
    st.error(f"Could not find the data file: {DATA_PATH.name}. Place it beside app.py.")
    st.stop()

st.title("🎗️ Breast Cancer Insights")
st.caption(
    "Explore how stage, hormone status, age and tumor size relate to patient "
    "survival. Educational project, not medical advice."
)

with st.sidebar:
    st.header("Filters")
    age_low, age_high = int(df["Age"].min()), int(df["Age"].max())
    selected_age = st.slider("Age range", age_low, age_high, (age_low, age_high))
    races = sorted(df["Race"].unique().tolist())
    stages = [s for s in STAGE_ORDER if s in df["Stage"].unique()]
    estrogen = sorted(df["Estrogen_Status"].unique().tolist())
    progesterone = sorted(df["Progesterone_Status"].unique().tolist())
    selected_races = st.multiselect("Race", races, default=races)
    selected_stages = st.multiselect("Stage", stages, default=stages)
    selected_er = st.multiselect("Estrogen status", estrogen, default=estrogen)
    selected_pr = st.multiselect("Progesterone status", progesterone, default=progesterone)

filtered = df[
    df["Age"].between(selected_age[0], selected_age[1])
    & df["Race"].isin(selected_races)
    & df["Stage"].isin(selected_stages)
    & df["Estrogen_Status"].isin(selected_er)
    & df["Progesterone_Status"].isin(selected_pr)
].copy()

if filtered.empty:
    st.info("No patients match these filters. Select at least one option in every filter.")
    st.stop()

st.caption(f"Showing {len(filtered):,} of {len(df):,} patients")

kpi_cols = st.columns(5)
kpi_cols[0].metric("Total Patients", f"{len(filtered):,}")
kpi_cols[1].metric("Mortality Rate", pct(filtered["Dead"].mean() * 100))
kpi_cols[2].metric("Avg Follow-up", f"{filtered['Survival_Months'].mean():.1f} months")
kpi_cols[3].metric("Avg Tumor Size", f"{filtered['Tumor_Size'].mean():.1f} mm")
kpi_cols[4].metric(
    "Estrogen Positive",
    pct((filtered["Estrogen_Status"] == "Positive").mean() * 100),
)

overview_tab, risk_tab, insights_tab, glossary_tab = st.tabs(
    ["Patient overview", "Risk factors", "Notebook insights", "Medical terms"]
)

with overview_tab:
    left, right = st.columns(2)
    with left:
        scatter = px.scatter(
            filtered,
            x="Tumor_Size",
            y="Survival_Months",
            color="Status",
            hover_data=["Age", "Stage", "Race"],
            title="Tumor Size vs Survival Months",
            labels={"Tumor_Size": "Tumor size (mm)", "Survival_Months": "Survival (months)"},
            opacity=0.6,
        )
        st.plotly_chart(scatter, width="stretch")
    with right:
        by_stage = mortality_by(filtered, "Stage")
        bar = px.bar(
            by_stage,
            x="Stage",
            y="Mortality_Pct",
            hover_data=["Patients"],
            title="Mortality Rate by Stage",
            category_orders={"Stage": STAGE_ORDER},
            color_discrete_sequence=["firebrick"],
        )
        st.plotly_chart(style_percent_chart(bar), width="stretch")

    left, right = st.columns(2)
    with left:
        deaths = (
            filtered[filtered["Dead"] == 1]
            .groupby("Follow_Up_Year", as_index=False)
            .size()
            .rename(columns={"size": "Deaths"})
        )
        line = px.line(
            deaths,
            x="Follow_Up_Year",
            y="Deaths",
            markers=True,
            title="Deaths by Follow-up Year",
            labels={"Follow_Up_Year": "Follow-up year", "Deaths": "Number of deaths"},
        )
        st.plotly_chart(line, width="stretch")
        st.caption("These are death counts, not rates. There is no date column, so follow-up time is used.")
    with right:
        corr_cols = [
            "Age", "Tumor_Size", "Nodes_Examined", "Nodes_Positive",
            "Survival_Months", "Dead", "Nodes_Ratio",
        ]
        heatmap = px.imshow(
            filtered[corr_cols].corr(),
            text_auto=".2f",
            color_continuous_scale="RdBu",
            color_continuous_midpoint=0,
            title="Correlation Heatmap",
            aspect="auto",
        )
        st.plotly_chart(heatmap, width="stretch")

with risk_tab:
    combo = mortality_by(filtered, ["Stage", "Estrogen_Status"])
    grouped = px.bar(
        combo,
        x="Stage",
        y="Mortality_Pct",
        color="Estrogen_Status",
        barmode="group",
        hover_data=["Patients"],
        title="Mortality Rate: Stage vs Estrogen Status",
        category_orders={"Stage": STAGE_ORDER},
    )
    st.plotly_chart(style_percent_chart(grouped), width="stretch")

    left, right = st.columns(2)
    with left:
        rates = combo.pivot(index="Stage", columns="Estrogen_Status", values="Mortality_Pct")
        st.markdown("**Mortality rate (%)**")
        st.dataframe(rates.style.format("{:.1f}%", na_rep="—"), width="stretch")
    with right:
        counts = combo.pivot(index="Stage", columns="Estrogen_Status", values="Patients")
        st.markdown("**Number of patients**")
        st.dataframe(counts.style.format("{:,.0f}", na_rep="—"), width="stretch")
    st.caption("Groups with fewer than 30 patients give unreliable percentages. Check the patient counts.")

    left, right = st.columns(2)
    with left:
        by_age = px.bar(
            mortality_by(filtered, "Age_Group"),
            x="Age_Group",
            y="Mortality_Pct",
            hover_data=["Patients"],
            title="Mortality Rate by Age Group",
            category_orders={"Age_Group": AGE_ORDER},
            labels={"Age_Group": "Age group"},
        )
        st.plotly_chart(style_percent_chart(by_age), width="stretch")
    with right:
        by_size = px.bar(
            mortality_by(filtered, "Tumor_Size_Group"),
            x="Tumor_Size_Group",
            y="Mortality_Pct",
            hover_data=["Patients"],
            title="Mortality Rate by Tumor Size",
            category_orders={"Tumor_Size_Group": SIZE_ORDER},
            labels={"Tumor_Size_Group": "Tumor size (Small ≤20mm, Medium 21-50mm, Large >50mm)"},
        )
        st.plotly_chart(style_percent_chart(by_size), width="stretch")

with insights_tab:
    st.caption("These insights use the full dataset, so they do not change with the filters.")

    stage_rate = df.groupby("Stage")["Dead"].mean() * 100
    stage_er = df.pivot_table(
        values="Dead", index="Stage", columns="Estrogen_Status", aggfunc="mean"
    ) * 100
    avg_tumor = df.groupby("Status")["Tumor_Size"].mean()

    st.subheader("Tumor Size vs Survival Months")
    st.markdown(
        f"Points are widely scattered and the correlation between tumor size and "
        f"survival months is only about **{df['Tumor_Size'].corr(df['Survival_Months']):.2f}**. "
        f"Patients who died had a slightly larger average tumor "
        f"(**{avg_tumor['Dead']:.1f} mm**) than patients who are alive "
        f"(**{avg_tumor['Alive']:.1f} mm**). Positive lymph nodes relate more strongly to death "
        f"(**{df['Nodes_Positive'].corr(df['Dead']):.2f}**) than tumor size "
        f"(**{df['Tumor_Size'].corr(df['Dead']):.2f}**). "
        f"Do not judge risk by tumor size alone; check lymph nodes and hormone status too."
    )

    st.subheader("Stage vs Mortality")
    st.markdown(
        f"Mortality rises at every stage, from **{pct(stage_rate['IIA'])}** in Stage IIA to "
        f"**{pct(stage_rate['IIIC'])}** in Stage IIIC, about "
        f"**{stage_rate['IIIC'] / stage_rate['IIA']:.0f} times** higher. "
        f"Promote early screening and give Stage IIIB and IIIC patients the most intensive follow-up."
    )

    st.subheader("Stage vs Estrogen Status")
    st.markdown(
        f"At every stage, estrogen negative patients have higher mortality. "
        f"In Stage IIIA it is **{pct(stage_er.loc['IIIA', 'Negative'])}** vs "
        f"**{pct(stage_er.loc['IIIA', 'Positive'])}**, and in Stage IIIC "
        f"**{pct(stage_er.loc['IIIC', 'Negative'])}** vs **{pct(stage_er.loc['IIIC', 'Positive'])}**. "
        f"Treat estrogen negative patients as high priority with closer monitoring."
    )

    st.subheader("Limitations")
    st.markdown(
        "- There is no date or treatment information, so results show association, not cause.\n"
        "- Some groups are small (Grade 4, Stage IIIB estrogen negative), so their percentages are less reliable.\n"
        "- Patients marked Alive have not died yet; their follow-up time is not a final survival time."
    )

with glossary_tab:
    st.markdown(
        "**Stage (IIA to IIIC):** how far the cancer has grown or spread. Higher means more advanced.\n\n"
        "**T Stage (T1 to T4):** size of the main tumor.\n\n"
        "**N Stage (N1 to N3):** how many nearby lymph nodes are affected.\n\n"
        "**Grade (1 to 4):** how abnormal the cancer cells look. Higher grade means faster growing.\n\n"
        "**Estrogen / Progesterone status:** whether the cancer cells have hormone receptors. "
        "Positive usually means hormone therapy can work.\n\n"
        "**Lymph nodes:** small glands that filter fluid. Cancer often spreads here first.\n\n"
        "**Mortality rate:** percentage of patients in a group who died.\n\n"
        "**Follow-up (Survival Months):** how long the patient was observed."
    )
