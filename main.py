import pandas as pd
import glob
import os

DATA_FOLDER = r"file_path_to_your_data_folder"

all_series = []

for file_path in glob.glob(os.path.join(DATA_FOLDER, "*_pnl.csv")):
    
    # alpha_id from filename
    file_name = os.path.basename(file_path)
    alpha_id = file_name.replace("_pnl.csv", "")
    
    # read data
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"])
    
    # create time series
    pnl_series = df.set_index("date")["pnl"]
    pnl_series.name = alpha_id
    
    all_series.append(pnl_series)

# align by date (union of all dates)
pnl_df = pd.concat(all_series, axis=1)

# pearson correlation (pairwise, overlapping dates only)
corr_matrix = pnl_df.corr(method="pearson")

print(corr_matrix)
