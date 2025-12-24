import pandas as pd
import glob
import os

# ==========================
# CONFIG
# ==========================
DATA_FOLDER = r"<PATH_TO_YOUR_DATA_FOLDER>"   # <-- CHANGE THIS
OUTPUT_FILE = "correlation_matrix.xlsx"
START_YEAR = 2020
END_YEAR = 2022

# ==========================
# READ ALL ALPHA FILES
# ==========================
all_series = []

for file_path in glob.glob(os.path.join(DATA_FOLDER, "*_pnl.csv")):
    file_name = os.path.basename(file_path)
    alpha_id = file_name.replace("_pnl.csv", "")
    
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"])

    df = df[(df["date"].dt.year >= START_YEAR) &
            (df["date"].dt.year <= END_YEAR)]

    pnl_series = df.set_index("date")["pnl"]
    pnl_series.name = alpha_id
    
    all_series.append(pnl_series)

# ==========================
# ALIGN BY DATE
# ==========================
pnl_df = pd.concat(all_series, axis=1)

# ==========================
# PEARSON CORRELATION MATRIX
# ==========================
corr_matrix = pnl_df.corr(method="pearson").round(4)

# ==========================
# EXPORT TO EXCEL
# ==========================
with pd.ExcelWriter(OUTPUT_FILE, engine="xlsxwriter") as writer:
    corr_matrix.to_excel(writer, sheet_name="Correlation")
    worksheet = writer.sheets["Correlation"]
    
    # Freeze header row & column
    worksheet.freeze_panes(1, 1)
    
    # Conditional formatting (heatmap)
    n = corr_matrix.shape[0]
    worksheet.conditional_format(1, 1, n, n, {
        "type": "3_color_scale"
    })

print(f"Correlation matrix saved to: {OUTPUT_FILE}")
