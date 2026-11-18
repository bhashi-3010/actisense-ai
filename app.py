
import streamlit as st
from pathlib import Path
from collections import Counter
import html

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="MEWDF | Multi-Class HAR",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

ACTIVITIES = {
    0: "Null Activity",
    1: "Standing Still",
    2: "Sitting & Relaxing",
    3: "Lying Down",
    4: "Walking",
    5: "Climbing Stairs",
    6: "Waist Bends Forward",
    7: "Frontal Elevation of Arms",
    8: "Knees Bending",
    9: "Cycling",
    10: "Jogging",
    11: "Running",
    12: "Jump Front & Back"
}

# 24 columns: 23 sensor measurements + activity label
COLUMN_NAMES = [
    "Chest Acc X", "Chest Acc Y", "Chest Acc Z",
    "ECG Lead 1", "ECG Lead 2",
    "Ankle Acc X", "Ankle Acc Y", "Ankle Acc Z",
    "Ankle Gyro X", "Ankle Gyro Y", "Ankle Gyro Z",
    "Ankle Mag X", "Ankle Mag Y", "Ankle Mag Z",
    "Arm Acc X", "Arm Acc Y", "Arm Acc Z",
    "Arm Gyro X", "Arm Gyro Y", "Arm Gyro Z",
    "Arm Mag X", "Arm Mag Y", "Arm Mag Z",
    "Activity Label"
]

# =====================================================
# 2. DARK MOCHA DESIGN
# =====================================================

st.markdown("""
<style>
.stApp {
    background: #211D1A;
    color: #F3E8D6;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    color: #F3E8D6 !important;
}

p, label {
    color: #C7B8A4;
}

section[data-testid="stSidebar"] {
    background: #29231F;
    border-right: 1px solid #514236;
}

section[data-testid="stSidebar"] h1 {
    color: #F3E8D6 !important;
}

section[data-testid="stSidebar"] p {
    color: #BCA88E;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: #332B25;
    border: 1px solid #493B30;
    border-radius: 10px;
    padding: 9px;
    margin-bottom: 6px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    border-color: #C5A77F;
    background: #493B30;
}

.hero {
    background: linear-gradient(120deg, #38302A, #493B30);
    border: 1px solid #66513D;
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 25px;
}

.hero-tag {
    color: #C5A77F;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 2px;
}

.hero h1 {
    color: #F3E8D6 !important;
    font-size: 34px;
    margin: 14px 0;
}

.hero p {
    color: #D0C0AA;
    line-height: 1.7;
}

.section-title {
    color: #F3E8D6;
    font-size: 22px;
    font-weight: 750;
    margin-top: 28px;
    margin-bottom: 5px;
}

.section-subtitle {
    color: #AFA08D;
    font-size: 13px;
    margin-bottom: 18px;
}

.metric-card {
    background: #302923;
    border: 1px solid #554535;
    border-radius: 15px;
    padding: 20px;
    min-height: 115px;
    margin-bottom: 12px;
}

.metric-label {
    color: #C5A77F;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1px;
}

.metric-value {
    color: #F3E8D6;
    font-size: 27px;
    font-weight: bold;
    margin-top: 12px;
}

.panel {
    background: #302923;
    border: 1px solid #514236;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 15px;
}

.panel-title {
    color: #F3E8D6;
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 12px;
}

.bar-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 11px 0;
}

.bar-label {
    width: 145px;
    flex-shrink: 0;
    color: #D0C0AA;
    font-size: 12px;
}

.bar-track {
    flex: 1;
    height: 10px;
    background: #211D1A;
    border-radius: 20px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #80664D, #C5A77F);
    border-radius: 20px;
}

.bar-count {
    color: #C5A77F;
    width: 65px;
    text-align: right;
    font-size: 11px;
}

.info-box {
    background: #38302A;
    border: 1px solid #66513D;
    border-radius: 12px;
    padding: 16px;
    color: #D0C0AA;
    font-size: 13px;
    line-height: 1.7;
}

.footer {
    border-top: 1px solid #514236;
    margin-top: 35px;
    padding-top: 18px;
    color: #9D8B77;
    font-size: 12px;
    text-align: center;
}

div[data-testid="stAlert"] {
    background: #38302A;
    border: 1px solid #66513D;
    color: #F3E8D6;
}

.stButton button {
    background: #A88A65;
    color: #211D1A;
    border: 1px solid #C5A77F;
    border-radius: 9px;
    font-weight: bold;
}

hr {
    border-color: #514236 !important;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. REUSABLE COMPONENTS
# =====================================================

def hero(title, description):
    st.html(f"""
    <div class="hero">
        <div class="hero-tag">WEARABLE SENSOR INTELLIGENCE</div>
        <h1>{html.escape(title)}</h1>
        <p>{html.escape(description)}</p>
    </div>
    """)


def section(title, subtitle):
    st.html(f"""
    <div class="section-title">{html.escape(title)}</div>
    <div class="section-subtitle">{html.escape(subtitle)}</div>
    """)


def metric(label, value):
    st.html(f"""
    <div class="metric-card">
        <div class="metric-label">{html.escape(label)}</div>
        <div class="metric-value">{html.escape(str(value))}</div>
    </div>
    """)


def bar_chart(title, data, show_null=True):
    items = [
        (label, count)
        for label, count in data.items()
        if show_null or label != 0
    ]

    if not items:
        st.info("No records available for this selection.")
        return

    maximum = max(count for _, count in items)

    content = f"""
    <div class="panel">
        <div class="panel-title">{html.escape(title)}</div>
    """

    for label, count in items:
        name = ACTIVITIES.get(
            label, label if isinstance(label, str) else f"Activity {label}"
        )
        percentage = count / maximum * 100 if maximum else 0

        content += f"""
        <div class="bar-row">
            <div class="bar-label">{html.escape(name)}</div>
            <div class="bar-track">
                <div class="bar-fill" style="width:{percentage:.2f}%"></div>
            </div>
            <div class="bar-count">{count:,}</div>
        </div>
        """

    content += "</div>"
    st.html(content)


# =====================================================
# 4. READ ALL DATASET FILES
# =====================================================

@st.cache_data(show_spinner="Reading all 10 mHealth subject files...")
def load_dataset_summary():

    summary = {}
    combined = Counter()
    total_records = 0
    total_missing = 0
    column_counts = Counter()

    for subject in range(1, 11):

        file_path = DATA_DIR / f"mHealth_subject{subject}.log"

        if not file_path.exists():
            raise FileNotFoundError(
                f"Missing dataset file: {file_path.name}"
            )

        records = 0
        activities = Counter()
        missing = 0

        with open(file_path, "r", encoding="utf-8") as file:

            for line in file:
                values = line.split()

                if not values:
                    continue

                records += 1
                column_counts[len(values)] += 1

                missing += sum(
                    value.lower() in ["nan", "null", "none"]
                    for value in values
                )

                activities[int(float(values[-1]))] += 1

        summary[subject] = {
            "records": records,
            "activities": dict(activities),
            "missing": missing
        }

        total_records += records
        total_missing += missing
        combined.update(activities)

    return {
        "subjects": summary,
        "activities": dict(combined),
        "total_records": total_records,
        "total_missing": total_missing,
        "columns": dict(column_counts)
    }


# =====================================================
# 5. READ SELECTED SUBJECT PREVIEW
# =====================================================

@st.cache_data(show_spinner=False)
def load_preview(subject, activity_filter, limit=25):

    file_path = DATA_DIR / f"mHealth_subject{subject}.log"

    rows = []

    with open(file_path, "r", encoding="utf-8") as file:

        for line in file:

            values = line.split()

            if not values:
                continue

            activity = int(float(values[-1]))

            if activity_filter != "All activities":
                if activity != int(activity_filter):
                    continue

            rows.append(values)

            if len(rows) >= limit:
                break

    return rows




# =====================================================
# SENSOR ANALYSIS HELPERS
# =====================================================

SENSOR_OPTIONS = {
    "Chest": {
        "Accelerometer": {"X": 0, "Y": 1, "Z": 2},
        "ECG": {"Lead 1": 3, "Lead 2": 4},
    },
    "Left Ankle": {
        "Accelerometer": {"X": 5, "Y": 6, "Z": 7},
        "Gyroscope": {"X": 8, "Y": 9, "Z": 10},
        "Magnetometer": {"X": 11, "Y": 12, "Z": 13},
    },
    "Right Arm": {
        "Accelerometer": {"X": 14, "Y": 15, "Z": 16},
        "Gyroscope": {"X": 17, "Y": 18, "Z": 19},
        "Magnetometer": {"X": 20, "Y": 21, "Z": 22},
    },
}


@st.cache_data(show_spinner=False)
def load_sensor_signal(subject, activity_filter, column_index, limit=500):
    """Read up to one 10-second window (500 samples at 50 Hz)."""
    file_path = DATA_DIR / f"mHealth_subject{subject}.log"
    samples = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            values = line.split()
            if not values or len(values) != 24:
                continue

            activity = int(float(values[-1]))
            if activity_filter != "All activities" and activity != int(activity_filter):
                continue

            try:
                samples.append(float(values[column_index]))
            except (ValueError, IndexError):
                continue

            if len(samples) >= limit:
                break

    return samples


def signal_svg(samples, title):
    """Create a lightweight SVG signal chart without pandas or Plotly."""
    width, height = 1000, 300
    left, right, top, bottom = 65, 20, 25, 45
    plot_w = width - left - right
    plot_h = height - top - bottom

    if not samples:
        return '<div class="panel">No sensor samples found for this selection.</div>'

    low, high = min(samples), max(samples)
    if high == low:
        high = low + 1

    points = []
    for i, value in enumerate(samples):
        x = left + (i / max(len(samples) - 1, 1)) * plot_w
        y = top + ((high - value) / (high - low)) * plot_h
        points.append(f"{x:.1f},{y:.1f}")

    grid = ""
    for fraction in (0, 0.25, 0.5, 0.75, 1):
        y = top + fraction * plot_h
        grid += (
            f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" '
            f'y2="{y:.1f}" stroke="#554535" stroke-width="1"/>'
        )

    return f"""
    <div class="panel">
      <div class="panel-title">{html.escape(title)}</div>
      <div style="width:100%; overflow-x:auto;">
        <svg viewBox="0 0 {width} {height}" role="img"
             style="width:100%; min-width:600px; height:auto;">
          {grid}
          <polyline points="{' '.join(points)}" fill="none"
                    stroke="#C5A77F" stroke-width="2.2"
                    stroke-linejoin="round" stroke-linecap="round"/>
          <text x="{left}" y="16" fill="#BCA88E" font-size="12">{high:.3f}</text>
          <text x="{left}" y="{height-12}" fill="#BCA88E" font-size="12">{low:.3f}</text>
          <text x="{width/2}" y="{height-5}" text-anchor="middle"
                fill="#BCA88E" font-size="12">Sample index (50 samples/second)</text>
          <text x="15" y="{height/2}" transform="rotate(-90 15 {height/2})"
                text-anchor="middle" fill="#BCA88E" font-size="12">Sensor value</text>
        </svg>
      </div>
      <div style="color:#AFA08D; font-size:12px;">
        {len(samples)} samples · {len(samples)/50:.2f} seconds at 50 Hz
      </div>
    </div>
    """


# =====================================================
# MEWDF FEATURE ENGINEERING HELPERS
# Matched to the supplied random_split.ipynb notebook.
# =====================================================

import math

SAMPLE_RATE = 50
WINDOW_SECONDS = 10
WINDOW_SIZE = SAMPLE_RATE * WINDOW_SECONDS

# Preserve the exact 23-channel order used during Colab model training.
SENSOR_CHANNELS = list(range(23))

# Exact feature order from extract_features() in the Colab notebook.
FEATURE_NAMES = [
    "Mean", "Median", "Minimum", "Maximum", "Standard Deviation",
    "Variance", "Q1", "Q3", "IQR", "MAV", "RMS", "SSI",
    "Harmonic Mean", "Skewness", "Kurtosis"
]


def percentile(sorted_values, fraction):
    """NumPy-compatible linear percentile interpolation."""
    if not sorted_values:
        return None
    position = (len(sorted_values) - 1) * fraction
    lower = int(position)
    upper = min(lower + 1, len(sorted_values) - 1)
    weight = position - lower
    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight


def calculate_channel_features(values):
    """Reproduce the notebook's 15 features in the exact training order."""
    n = len(values)
    if n == 0:
        return {name: None for name in FEATURE_NAMES}

    mean_value = sum(values) / n
    variance = sum((value - mean_value) ** 2 for value in values) / n
    std_value = math.sqrt(variance)
    sorted_values = sorted(values)
    median_value = percentile(sorted_values, 0.50)
    q1 = percentile(sorted_values, 0.25)
    q3 = percentile(sorted_values, 0.75)
    mav = sum(abs(value) for value in values) / n
    squared_sum = sum(value * value for value in values)
    rms = math.sqrt(squared_sum / n)

    # Matches the notebook: use absolute values; return 0 if any sample is zero.
    if any(value == 0 for value in values):
        harmonic = 0.0
    else:
        harmonic = n / sum(1.0 / abs(value) for value in values)

    # scipy.stats.skew and kurtosis defaults: biased moments, Fisher kurtosis.
    if variance == 0:
        skewness = None
        kurt = None
    else:
        third_moment = sum((value - mean_value) ** 3 for value in values) / n
        fourth_moment = sum((value - mean_value) ** 4 for value in values) / n
        skewness = third_moment / (std_value ** 3)
        kurt = (fourth_moment / (variance ** 2)) - 3.0

    return {
        "Mean": mean_value,
        "Median": median_value,
        "Minimum": sorted_values[0],
        "Maximum": sorted_values[-1],
        "Standard Deviation": std_value,
        "Variance": variance,
        "Q1": q1,
        "Q3": q3,
        "IQR": q3 - q1,
        "MAV": mav,
        "RMS": rms,
        "SSI": squared_sum,
        "Harmonic Mean": harmonic,
        "Skewness": skewness,
        "Kurtosis": kurt,
    }


@st.cache_data(show_spinner="Applying notebook-matched MEWDF windows and extracting 345 features...")
def extract_mewdf_features(subject, include_null=False):
    """Match the notebook's subject -> activity grouping -> 500-row windows.

    The notebook removes label 0 (unless requested here), groups each subject's
    rows by activity label, and then creates non-overlapping 500-row chunks
    within each activity group. Incomplete tails are omitted.
    """
    file_path = DATA_DIR / f"mHealth_subject{subject}.log"
    activity_rows = {}
    activity_order = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            values = line.split()
            if len(values) != 24:
                continue
            try:
                label = int(float(values[-1]))
                numeric_row = [float(value) for value in values[:23]]
            except ValueError:
                continue

            if not include_null and label == 0:
                continue
            if label not in activity_rows:
                activity_rows[label] = []
                activity_order.append(label)
            activity_rows[label].append(numeric_row)

    output_rows = []
    window_number = 0
    for label in activity_order:
        rows = activity_rows[label]
        for start in range(0, len(rows) - WINDOW_SIZE + 1, WINDOW_SIZE):
            chunk = rows[start:start + WINDOW_SIZE]
            window_number += 1
            row_out = {
                "Subject": subject,
                "Window ID": window_number,
                "Activity Label": label,
                "Activity": ACTIVITIES.get(label, f"Activity {label}"),
                "Activity Group Sample Start": start,
                "Activity Group Sample End": start + WINDOW_SIZE - 1,
                "Samples": WINDOW_SIZE,
            }
            for channel_index in SENSOR_CHANNELS:
                channel_values = [sample[channel_index] for sample in chunk]
                stats = calculate_channel_features(channel_values)
                prefix = COLUMN_NAMES[channel_index]
                for feature_name in FEATURE_NAMES:
                    row_out[f"{prefix} | {feature_name}"] = stats[feature_name]
            output_rows.append(row_out)

    return output_rows


def signal_metric(label, value):
    metric(label, f"{value:.4f}" if isinstance(value, float) else value)


# =====================================================
# 6. LOAD DATA
# =====================================================

try:
    DATA = load_dataset_summary()

except Exception as error:
    st.error(f"Dataset loading error: {error}")
    st.info(
        "Check that all ten .log files are inside the data folder."
    )
    st.stop()


# =====================================================
# 7. SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("ActiSense AI")

    st.html("""
    <p style="color:#C5A77F; font-size:11px;
    letter-spacing:2px; font-weight:bold;">
    HUMAN ACTIVITY RECOGNITION
    </p>
    """)

    st.divider()

    st.markdown("### WORKSPACE")

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Dataset Explorer",
            "Sensor Analysis",
            "Feature Engineering",
            "Model Performance",
            "Activity Prediction"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### DATASET INFORMATION")

    st.html("""
    <div class="info-box">
        Dataset: mHealth<br>
        Subjects: 10<br>
        Sensor columns: 23<br>
        Total columns: 24<br>
        Sampling rate: 50 Hz<br>
        Window size: 10 seconds
    </div>
    """)

    st.divider()
    st.caption("MEWDF RESEARCH PROJECT")
    st.caption("Dark Mocha Edition")


# =====================================================
# 8. OVERVIEW
# =====================================================

if page == "Overview":

    hero(
        "Human Activity Recognition",
        "Statistical Feature Engineering for Multi-Class "
        "Human Activity Recognition Using mHealth Wearable Sensor Data."
    )

    st.markdown(
        "An intelligent research framework combining wearable "
        "sensor measurements, MEWDF segmentation, statistical "
        "feature extraction and machine learning classification."
    )

    section(
        "Research at a Glance",
        "Live statistics calculated from all 10 subject files"
    )

    cols = st.columns(4)

    values = [
        ("TOTAL RECORDS", f"{DATA['total_records']:,}"),
        ("SUBJECTS", "10"),
        ("SENSOR CHANNELS", "23"),
        ("MISSING VALUES", f"{DATA['total_missing']:,}")
    ]

    for col, (label, value) in zip(cols, values):
        with col:
            metric(label, value)

    section(
        "Dataset Activity Distribution",
        "Combined activity counts across all subjects"
    )

    bar_chart(
        "Records by Activity",
        DATA["activities"],
        show_null=True
    )

    section(
        "Research Workflow",
        "Major stages of the proposed framework"
    )

    cols = st.columns(4)

    for col, (number, name) in zip(
        cols,
        [
            ("01", "Sensor Data"),
            ("02", "MEWDF Segmentation"),
            ("03", "Feature Extraction"),
            ("04", "ML Classification")
        ]
    ):
        with col:
            st.html(f"""
            <div class="panel">
                <div style="color:#C5A77F;">STEP {number}</div>
                <div style="color:#F3E8D6;
                font-weight:bold; margin-top:12px;">
                    {name}
                </div>
            </div>
            """)


# =====================================================
# 9. DATASET EXPLORER
# =====================================================

elif page == "Dataset Explorer":

    hero(
        "Dataset Explorer",
        "Explore the actual mHealth dataset, subject records, "
        "activity distribution and sensor measurements."
    )

    section(
        "Dataset Statistics",
        "Calculated directly from all 10 subject files"
    )

    cols = st.columns(4)

    metrics = [
        ("TOTAL RECORDS", f"{DATA['total_records']:,}"),
        ("SUBJECTS", "10"),
        ("ACTIVITY CLASSES", "13"),
        ("MISSING VALUES", f"{DATA['total_missing']:,}")
    ]

    for col, (label, value) in zip(cols, metrics):
        with col:
            metric(label, value)

    # Activity chart controls

    section(
        "Activity Distribution",
        "Explore the frequency of each activity label"
    )

    show_null = st.checkbox(
        "Include null activity class (label 0)",
        value=False
    )

    bar_chart(
        "Combined Activity Distribution",
        DATA["activities"],
        show_null=show_null
    )

    # Subject comparison

    section(
        "Subject-wise Analysis",
        "Compare the number of records collected per subject"
    )

    subject_records = {
        subject: details["records"]
        for subject, details in DATA["subjects"].items()
    }

    maximum = max(subject_records.values())

    for subject, count in subject_records.items():

        percentage = count / maximum * 100

        st.html(f"""
        <div class="bar-row">
            <div class="bar-label">Subject {subject}</div>
            <div class="bar-track">
                <div class="bar-fill"
                style="width:{percentage:.2f}%"></div>
            </div>
            <div class="bar-count">{count:,}</div>
        </div>
        """)

    # Subject selection

    section(
        "Individual Subject Explorer",
        "Select a participant to inspect their records"
    )

    selected_subject = st.selectbox(
        "Select subject",
        list(range(1, 11)),
        format_func=lambda x: f"Subject {x}"
    )

    subject_info = DATA["subjects"][selected_subject]

    c1, c2, c3 = st.columns(3)

    with c1:
        metric("SUBJECT RECORDS", f"{subject_info['records']:,}")

    with c2:
        metric("ACTIVITY CLASSES", len(subject_info["activities"]))

    with c3:
        metric("MISSING VALUES", subject_info["missing"])

    bar_chart(
        f"Activity Distribution – Subject {selected_subject}",
        subject_info["activities"],
        show_null=True
    )

    # Sensor data preview

    section(
        "Raw Sensor Data Preview",
        "Inspect the actual sensor readings from the selected subject"
    )

    activity_options = ["All activities"] + [
        str(x) for x in range(13)
    ]

    selected_activity = st.selectbox(
        "Filter by activity",
        activity_options
    )

    preview_rows = load_preview(
        selected_subject,
        selected_activity,
        limit=25
    )

    st.caption(
        f"Showing up to {len(preview_rows)} matching records."
    )

    if preview_rows:

        # Build HTML table without pandas
        table = """
        <div style="overflow-x:auto; max-height:450px;
        overflow-y:auto; border:1px solid #554535;
        border-radius:10px;">
        <table style="width:100%; border-collapse:collapse;
        color:#F3E8D6; font-size:11px;">
        <thead><tr style="background:#493B30;">
        """

        table += "".join(
            f'<th style="padding:9px; position:sticky; top:0; '
            f'background:#493B30; color:#C5A77F; '
            f'white-space:nowrap;">{html.escape(name)}</th>'
            for name in COLUMN_NAMES
        )

        table += "</tr></thead><tbody>"

        for row in preview_rows:

            table += "<tr>"

            for value in row:
                table += (
                    '<td style="padding:8px; border-bottom:'
                    '1px solid #514236; white-space:nowrap;">'
                    + html.escape(value) + "</td>"
                )

            table += "</tr>"

        table += "</tbody></table></div>"

        st.html(table)

    else:
        st.warning("No matching records found.")

    # Dataset health

    section(
        "Dataset Health",
        "Basic data quality checks"
    )

    st.html(f"""
    <div class="panel">
        <div style="color:#C5A77F; font-weight:bold;">
            DATA VALIDATION REPORT
        </div>
        <p>Subjects inspected: 10 / 10</p>
        <p>Total records: {DATA['total_records']:,}</p>
        <p>Observed columns per record: 24</p>
        <p>Missing-value tokens detected: {DATA['total_missing']}</p>
        <p>Files with consistent 24-column rows:
        {"Yes" if list(DATA["columns"].keys()) == [24] else "Check required"}</p>
    </div>
    """)


# =====================================================
# 10. SENSOR ANALYSIS
# =====================================================

elif page == "Sensor Analysis":

    hero(
        "Sensor Analysis",
        "Explore real wearable sensor signals from the mHealth dataset."
    )

    section(
        "Signal Configuration",
        "Choose a participant, activity, sensor location and measurement"
    )

    control_cols = st.columns(4)

    with control_cols[0]:
        sensor_subject = st.selectbox(
            "Select subject",
            list(range(1, 11)),
            format_func=lambda x: f"Subject {x}",
            key="sensor_subject"
        )

    with control_cols[1]:
        sensor_activity = st.selectbox(
            "Select activity",
            ["All activities"] + [str(x) for x in range(13)],
            format_func=lambda x: (
                x if x == "All activities"
                else f"{x} - {ACTIVITIES[int(x)]}"
            ),
            key="sensor_activity"
        )

    with control_cols[2]:
        sensor_location = st.selectbox(
            "Sensor location",
            list(SENSOR_OPTIONS.keys()),
            key="sensor_location"
        )

    with control_cols[3]:
        sensor_type = st.selectbox(
            "Sensor type",
            list(SENSOR_OPTIONS[sensor_location].keys()),
            key="sensor_type"
        )

    axis_options = SENSOR_OPTIONS[sensor_location][sensor_type]
    selected_axis = st.selectbox(
        "Measurement / Axis",
        list(axis_options.keys()),
        key="sensor_axis"
    )
    column_index = axis_options[selected_axis]
    channel_name = COLUMN_NAMES[column_index]

    samples = load_sensor_signal(
        sensor_subject,
        sensor_activity,
        column_index,
        limit=500
    )

    section(
        "Signal Overview",
        "Raw sensor measurements selected directly from the subject data file"
    )

    if samples:
        mean_value = sum(samples) / len(samples)
        variance = sum((x - mean_value) ** 2 for x in samples) / len(samples)
        std_value = variance ** 0.5

        stat_cols = st.columns(4)
        stats = [
            ("SAMPLES", len(samples)),
            ("MEAN", mean_value),
            ("MINIMUM", min(samples)),
            ("MAXIMUM", max(samples)),
        ]
        for col, (label, value) in zip(stat_cols, stats):
            with col:
                signal_metric(label, value)

        st.markdown("### Sensor Signal Visualization")
        st.line_chart(
            {"Sensor Value": samples},
            height=350,
            use_container_width=True
        )
        st.caption(
            "X-axis: Sample index | Y-axis: Sensor measurement | "
            "Sampling frequency: 50 Hz"
        )

        extra_cols = st.columns(2)
        with extra_cols[0]:
            metric("STANDARD DEVIATION", f"{std_value:.4f}")
        with extra_cols[1]:
            metric("SIGNAL DURATION", f"{len(samples) / 50:.2f} seconds")

        section(
            "Sensor Interpretation",
            "How to read this visualization"
        )
        st.html(f"""
        <div class="info-box">
          <b style="color:#C5A77F;">Selected channel:</b> {html.escape(channel_name)}<br>
          <b style="color:#C5A77F;">Sampling frequency:</b> 50 Hz (50 readings per second)<br>
          <b style="color:#C5A77F;">Window represented:</b> Up to 500 consecutive matching samples
          (approximately 10 seconds).<br>
          <b style="color:#C5A77F;">Standard deviation:</b> {std_value:.4f} —
          describes how spread out the readings are around their mean.
        </div>
        """)
        st.caption(
            "Note: This page displays raw signal samples. The 500 samples are a "
            "10-second segment at 50 Hz; this view does not yet apply MEWDF feature extraction."
        )
    else:
        st.warning(
            "No numeric sensor samples were found for this subject and activity selection."
        )


# =====================================================
# 11. FEATURE ENGINEERING
# =====================================================

elif page == "Feature Engineering":

    hero(
        "MEWDF Feature Engineering",
        "Segment continuous wearable sensor data into mutually exclusive "
        "10-second windows and extract statistical features from all sensor channels."
    )

    section(
        "Segmentation Configuration",
        "Each complete window contains 500 consecutive samples at 50 Hz."
    )

    config_cols = st.columns(3)
    with config_cols[0]:
        feature_subject = st.selectbox(
            "Select subject",
            list(range(1, 11)),
            format_func=lambda value: f"Subject {value}",
            key="feature_subject"
        )
    with config_cols[1]:
        include_null_windows = st.checkbox(
            "Include null activity windows (label 0)",
            value=False,
            key="include_null_windows"
        )
    with config_cols[2]:
        st.metric("Window size", f"{WINDOW_SIZE} samples")

    st.html("""
    <div class="info-box">
      <b style="color:#C5A77F;">Notebook-matched MEWDF rule:</b> For each subject,
      null activity (label 0) is excluded by default. Records are grouped by activity
      label and divided into non-overlapping 500-sample windows. Incomplete tails are
      omitted. This reproduces the grouping logic in the supplied Colab notebook.
      <br><b style="color:#C5A77F;">Model compatibility:</b> 15 features × 23 channels = 345 inputs.
    </div>
    """)

    feature_rows = extract_mewdf_features(
        feature_subject,
        include_null_windows
    )

    section(
        "MEWDF Segmentation Results",
        "Window counts are calculated from the selected subject's actual data."
    )

    total_windows = len(feature_rows)
    activity_window_counts = Counter(row["Activity"] for row in feature_rows)
    metric_cols = st.columns(4)
    summary_metrics = [
        ("SUBJECT", f"{feature_subject}"),
        ("COMPLETE WINDOWS", f"{total_windows:,}"),
        ("SAMPLES / WINDOW", f"{WINDOW_SIZE}"),
        ("WINDOW DURATION", f"{WINDOW_SECONDS} seconds"),
    ]
    for col, (label, value) in zip(metric_cols, summary_metrics):
        with col:
            metric(label, value)

    if not feature_rows:
        st.warning(
            "No complete 500-sample windows were found for this selection. "
            "Try including null activity windows or select another subject."
        )
    else:
        bar_chart(
            "Extracted Windows by Activity",
            {
                label: count
                for label, count in activity_window_counts.items()
            },
            show_null=True
        )

        section(
            "Statistical Feature Explorer",
            "Choose a sensor channel to inspect its extracted feature values across windows."
        )

        channel_name = st.selectbox(
            "Select sensor channel",
            [COLUMN_NAMES[index] for index in SENSOR_CHANNELS],
            key="feature_channel"
        )
        selected_feature_columns = [
            f"{channel_name} | {feature_name}"
            for feature_name in FEATURE_NAMES
        ]
        display_columns = [
            "Subject", "Window ID", "Activity Label", "Activity",
            "Activity Group Sample Start", "Activity Group Sample End", "Samples"
        ] + selected_feature_columns
        preview_data = [
            {key: row.get(key) for key in display_columns}
            for row in feature_rows[:100]
        ]
        table_html = [
            '<div style="overflow-x:auto; max-height:480px; overflow-y:auto; '
            'border:1px solid #554535; border-radius:10px;">',
            '<table style="width:100%; border-collapse:collapse; '
            'color:#F3E8D6; font-size:11px;">',
            '<thead><tr style="background:#493B30;">'
        ]
        for column in display_columns:
            table_html.append(
                '<th style="padding:9px; position:sticky; top:0; '
                'background:#493B30; color:#C5A77F; white-space:nowrap;">'
                + html.escape(column) + '</th>'
            )
        table_html.append('</tr></thead><tbody>')
        for preview_row in preview_data:
            table_html.append('<tr>')
            for column in display_columns:
                value = preview_row.get(column)
                if isinstance(value, float):
                    rendered = f"{value:.6f}"
                else:
                    rendered = "" if value is None else str(value)
                table_html.append(
                    '<td style="padding:8px; border-bottom:1px solid #514236; '
                    'white-space:nowrap;">' + html.escape(rendered) + '</td>'
                )
            table_html.append('</tr>')
        table_html.append('</tbody></table></div>')
        st.html(''.join(table_html))
        st.caption(
            f"Showing up to 100 of {total_windows:,} windows. "
            "The complete export contains features from all 23 sensor channels."
        )

        section(
            "Feature Definition",
            "Fifteen numeric outputs are calculated for each sensor channel, in the exact order used by your Colab model."
        )
        feature_descriptions = [
            ("Mean", "Average of the 500 sensor readings."),
            ("Median", "Middle value of the sorted readings."),
            ("Minimum / Maximum", "Smallest and largest readings."),
            ("Standard Deviation", "Population spread around the mean."),
            ("Variance", "Population variance of the readings."),
            ("Q1 / Q3", "25th and 75th percentiles using linear interpolation."),
            ("IQR", "Interquartile range: Q3 minus Q1."),
            ("MAV", "Mean absolute value."),
            ("RMS", "Root mean square."),
            ("SSI", "Sum of squared readings."),
            ("Harmonic Mean", "Harmonic mean of absolute readings; set to 0 if any reading is zero, matching the notebook."),
            ("Skewness", "Biased third standardized central moment; unavailable for a constant window."),
            ("Kurtosis", "Biased Fisher excess kurtosis; a normal distribution has value 0."),
        ]
        definition_html = '<div class="panel">'
        for name, description in feature_descriptions:
            definition_html += (
                f'<p><b style="color:#C5A77F;">{html.escape(name)}:</b> '
                f'{html.escape(description)}</p>'
            )
        definition_html += '</div>'
        st.html(definition_html)

        section(
            "Export Feature Dataset",
            "Download the complete extracted feature matrix for this subject."
        )
        import csv
        import io

        csv_buffer = io.StringIO()
        fieldnames = list(feature_rows[0].keys())
        writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(feature_rows)
        st.download_button(
            "Download all extracted features as CSV",
            data=csv_buffer.getvalue(),
            file_name=f"MEWDF_subject_{feature_subject}_features.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.caption(
            f"Feature matrix: {len(FEATURE_NAMES)} numeric outputs × "
            f"{len(SENSOR_CHANNELS)} channels = "
            f"{len(FEATURE_NAMES) * len(SENSOR_CHANNELS)} feature columns, "
            "plus window metadata. Feature order and formulas match the supplied Colab notebook."
        )


# =====================================================
# 12. MODEL PERFORMANCE
# =====================================================

elif page == "Model Performance":

    hero(
        "Model Performance",
        "Compare the six classifiers evaluated using your MEWDF feature set."
    )

    # These values are transcribed from the experiment results supplied.
    model_accuracy = {
        "Logistic Regression": 100.00,
        "Random Forest": 100.00,
        "Decision Tree": 98.48,
        "KNN": 98.48,
        "SVM": 98.48,
        "Naive Bayes": 95.96,
    }

    rf_support = [18, 18, 18, 18, 18, 16, 16, 16, 18, 18, 18, 6]
    activity_labels = [f"Activity {i}" for i in range(1, 13)]

    section(
        "Evaluation Summary",
        "Results transcribed from the supplied random-split experiment"
    )

    best_accuracy = max(model_accuracy.values())
    best_models = [name for name, score in model_accuracy.items() if score == best_accuracy]
    total_test_samples = sum(rf_support)

    summary_cols = st.columns(4)
    summary_values = [
        ("TEST SAMPLES", f"{total_test_samples}"),
        ("MODELS EVALUATED", str(len(model_accuracy))),
        ("HIGHEST REPORTED ACCURACY", f"{best_accuracy:.2f}%"),
        ("RF MACRO F1-SCORE", "1.0000"),
    ]
    for col, (label, value) in zip(summary_cols, summary_values):
        with col:
            metric(label, value)

    section(
        "Model Accuracy Comparison",
        "Reported accuracy values from the random train-test split"
    )
    st.bar_chart(
        {"Accuracy (%)": model_accuracy},
        y="Accuracy (%)",
        height=360,
        use_container_width=True
    )

    accuracy_rows = [
        {"Model": name, "Accuracy (%)": f"{score:.2f}"}
        for name, score in model_accuracy.items()
    ]
    st.dataframe(accuracy_rows, use_container_width=True, hide_index=True)
    st.caption(
        "Highest reported accuracy: " + " and ".join(best_models) +
        ". Both models are tied at 100.00% in the supplied comparison."
    )

    section(
        "Random Forest Classification Report",
        "Per-class precision, recall, F1-score and support from the supplied report"
    )

    report_rows = []
    for idx, support in enumerate(rf_support, start=1):
        report_rows.append({
            "Activity class": idx,
            "Precision": "1.0000",
            "Recall": "1.0000",
            "F1-score": "1.0000",
            "Support": support,
        })
    report_rows.extend([
        {"Activity class": "Accuracy", "Precision": "—", "Recall": "—", "F1-score": "1.0000", "Support": total_test_samples},
        {"Activity class": "Macro average", "Precision": "1.0000", "Recall": "1.0000", "F1-score": "1.0000", "Support": total_test_samples},
        {"Activity class": "Weighted average", "Precision": "1.0000", "Recall": "1.0000", "F1-score": "1.0000", "Support": total_test_samples},
    ])
    st.dataframe(report_rows, use_container_width=True, hide_index=True)

    section(
        "Random Forest Per-Activity F1-Score",
        "The supplied chart reports an F1-score of 100% for each of the 12 activity classes"
    )
    st.bar_chart(
        {"F1-score (%)": {label: 100.0 for label in activity_labels}},
        y="F1-score (%)",
        height=330,
        use_container_width=True
    )

    section(
        "Random Forest Confusion Matrix",
        "Reconstructed from the supplied image, which shows only diagonal counts"
    )
    matrix_rows = []
    for row_idx, count in enumerate(rf_support):
        row = {"True class": f"Activity {row_idx + 1}"}
        for col_idx in range(12):
            row[f"Pred {col_idx + 1}"] = count if row_idx == col_idx else 0
        matrix_rows.append(row)
    st.dataframe(matrix_rows, use_container_width=True, hide_index=True)

    st.html("""
    <div class="info-box">
      <b>Interpretation:</b> The supplied Random Forest report shows perfect
      precision, recall and F1-score on 198 test samples. The accuracy chart
      reports Logistic Regression and Random Forest tied at 100.00%.
      These are the reported results, not an independent re-evaluation.
    </div>
    """)

    st.warning(
        "Research validation note: the supplied confusion-matrix axes are labelled "
        "0–11, while the classification report lists classes 1–12. Confirm the "
        "class-to-label mapping before using the matrix in your paper. Also, a "
        "random split of windows can place windows from the same participant in "
        "both train and test sets. For a stronger generalization claim, evaluate "
        "with a subject-wise/group split and report those results separately."
    )


# =====================================================
# 13. ACTIVITY PREDICTION
# =====================================================

elif page == "Activity Prediction":

    hero(
        "Activity Prediction",
        "Run your saved Random Forest model on real 10-second MEWDF windows from the mHealth dataset."
    )

    model_path = BASE_DIR / "random_forest_mewdf.joblib"
    sensor_columns_path = BASE_DIR / "sensor_columns.joblib"

    section(
        "Trained Model",
        "Load the Random Forest pipeline exported from your Colab notebook"
    )

    if not model_path.exists() or not sensor_columns_path.exists():
        st.error(
            "Model files were not found. Place random_forest_mewdf.joblib "
            "and sensor_columns.joblib in the same folder as app.py."
        )
        st.stop()

    try:
        import joblib
        trained_model = joblib.load(model_path)
        saved_sensor_columns = joblib.load(sensor_columns_path)
    except Exception as error:
        st.error(f"Could not load the trained model: {error}")
        st.warning(
            "The model was saved with scikit-learn 1.6.1. If loading fails, "
            "use a compatible Python/scikit-learn environment and check that "
            "the required packages are installed."
        )
        st.stop()

    expected_features = len(saved_sensor_columns) * len(FEATURE_NAMES)
    model_features = getattr(trained_model, "n_features_in_", None)

    if len(saved_sensor_columns) != 23 or model_features != expected_features:
        st.error(
            f"Model compatibility check failed. The model expects "
            f"{model_features} inputs, while the saved sensor/feature setup "
            f"produces {expected_features}."
        )
        st.stop()

    model_cols = st.columns(3)
    with model_cols[0]:
        metric("MODEL", "Random Forest")
    with model_cols[1]:
        metric("EXPECTED INPUTS", str(model_features))
    with model_cols[2]:
        metric("SENSOR CHANNELS", str(len(saved_sensor_columns)))

    st.success(
        "Model loaded successfully. The pipeline includes median imputation, "
        "standard scaling and a 300-tree Random Forest classifier."
    )

    section(
        "Choose a MEWDF Window",
        "Select a participant and one complete 500-sample window extracted using the notebook-matched method."
    )

    prediction_subject = st.selectbox(
        "Select subject",
        list(range(1, 11)),
        format_func=lambda value: f"Subject {value}",
        key="prediction_subject"
    )

    with st.spinner("Extracting MEWDF windows for prediction..."):
        prediction_rows = extract_mewdf_features(
            prediction_subject,
            include_null=False
        )

    if not prediction_rows:
        st.warning("No complete 500-sample activity windows were found for this subject.")
        st.stop()

    available_labels = sorted({
        row["Activity Label"] for row in prediction_rows
    })
    selected_prediction_activity = st.selectbox(
        "Select activity window group",
        available_labels,
        format_func=lambda value: f"{value} — {ACTIVITIES.get(value, 'Unknown')}",
        key="prediction_activity"
    )

    matching_windows = [
        row for row in prediction_rows
        if row["Activity Label"] == selected_prediction_activity
    ]

    selected_window_id = st.selectbox(
        "Select window",
        [row["Window ID"] for row in matching_windows],
        format_func=lambda value: f"Window {value}",
        key="prediction_window"
    )

    selected_window = next(
        row for row in matching_windows
        if row["Window ID"] == selected_window_id
    )

    # Build the input vector in the exact order used in the Colab notebook:
    # sensor channel order first, then the 15 features for each channel.
    input_vector = []
    missing_feature_names = []

    for channel_index, channel_name in enumerate(saved_sensor_columns):
        # The saved sensor_columns.joblib list is already in the exact
        # 23-channel order used by the Colab notebook. Use positional mapping
        # so ECG Lead 1/2 correctly map to ecg_1/ecg_2.
        if channel_index >= len(SENSOR_CHANNELS):
            missing_feature_names.append(channel_name)
            continue

        display_channel = COLUMN_NAMES[SENSOR_CHANNELS[channel_index]]

        for feature_name in FEATURE_NAMES:
            key = f"{display_channel} | {feature_name}"
            value = selected_window.get(key)
            if value is None:
                input_vector.append(float("nan"))
            else:
                input_vector.append(float(value))

    if missing_feature_names or len(input_vector) != model_features:
        st.error(
            "The selected feature row does not match the model input schema. "
            f"Generated {len(input_vector)} values; expected {model_features}. "
            f"Unmatched sensor channels: {missing_feature_names}"
        )
        st.stop()

    section(
        "Selected Window Details",
        "The ground-truth activity is shown for comparison with the model prediction."
    )

    details_cols = st.columns(4)
    detail_values = [
        ("SUBJECT", f"Subject {prediction_subject}"),
        ("WINDOW", str(selected_window["Window ID"])),
        ("SAMPLES", str(selected_window["Samples"])),
        ("KNOWN ACTIVITY", selected_window["Activity"]),
    ]
    for col, (label, value) in zip(details_cols, detail_values):
        with col:
            metric(label, value)

    if st.button("Predict Human Activity", type="primary", use_container_width=True):
        try:
            predicted_label = int(trained_model.predict([input_vector])[0])
            predicted_activity = ACTIVITIES.get(
                predicted_label, f"Activity {predicted_label}"
            )

            probabilities = None
            if hasattr(trained_model, "predict_proba"):
                probabilities = trained_model.predict_proba([input_vector])[0]
                class_labels = list(trained_model.named_steps["clf"].classes_)
                confidence = float(
                    probabilities[class_labels.index(predicted_label)] * 100
                )
            else:
                confidence = None

            st.session_state["last_activity_prediction"] = {
                "subject": prediction_subject,
                "window_id": selected_window["Window ID"],
                "actual_label": int(selected_window["Activity Label"]),
                "actual_activity": selected_window["Activity"],
                "predicted_label": predicted_label,
                "predicted_activity": predicted_activity,
                "confidence": confidence,
            }

        except Exception as error:
            st.error(f"Prediction failed: {error}")

    result = st.session_state.get("last_activity_prediction")

    if result:
        section(
            "Prediction Result",
            "Output generated by your saved Random Forest model"
        )

        result_cols = st.columns(2)
        with result_cols[0]:
            metric("PREDICTED ACTIVITY", result["predicted_activity"])
        with result_cols[1]:
            metric(
                "MODEL CONFIDENCE",
                f"{result['confidence']:.2f}%"
                if result["confidence"] is not None else "Not available"
            )

        if result["predicted_label"] == result["actual_label"]:
            st.success(
                f"Prediction matches the dataset label: {result['actual_activity']}."
            )
        else:
            st.warning(
                f"Dataset label: {result['actual_activity']} | "
                f"Model prediction: {result['predicted_activity']}."
            )

        st.caption(
            "Confidence is the Random Forest's predicted class probability; "
            "it is not a guarantee that the prediction is correct."
        )

    st.warning(
        "Research note: this demonstration predicts windows taken from the "
        "mHealth dataset used in your experiment. Because the model was trained "
        "with a random window split, a selected window may have been part of "
        "its training data. Do not present this as independent or unseen-subject "
        "validation. A subject-wise evaluation is needed for that claim."
    )


# =====================================================
# FOOTER
# =====================================================

st.html("""
<div class="footer">
    MEWDF | HUMAN ACTIVITY RECOGNITION |
    RESEARCH ANALYTICS PLATFORM
</div>
""")
