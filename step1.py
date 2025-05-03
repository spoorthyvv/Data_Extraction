import pandas as pd
import os
import glob
import re
# MY MAIN FOLDER
folder_path = "/home/spoorthy/Downloads/Cleaning_of_Data_and_Merging_into_single_excel/Payout_Summary_and_Order_Level_Sales"
excel_files = glob.glob(os.path.join(folder_path, "*.xlsx"))
summary_data = []
for file in excel_files:
    try:
        df = pd.read_excel(file, sheet_name=0, header=None)

        # Extracting the brand name from cell B5 (index 4,1 in pandas)
        brand_name = df.iloc[4, 1] if df.shape[0] > 4 and df.shape[1] > 1 else "NotFoundInDoc"    
        text_blob = "\n".join(df.astype(str).fillna("").values.flatten())
        payout_period_match = re.search(r"Payout Period\s+([0-9A-Za-z\s\-]+)", text_blob)
        payout_period = payout_period_match.group(1).strip() if payout_period_match else ""
        payout_date_match = re.search(r"Payout Settlement Date\s+([0-9A-Za-z\s]+)", text_blob)
        payout_date = payout_date_match.group(1).strip() if payout_date_match else ""
        total_payout_match = re.search(r"Total Payout\s+₹?([\d,]+\.\d+)", text_blob)
        total_payout = float(total_payout_match.group(1).replace(",", "")) if total_payout_match else 0.0
        orders_match = re.search(r"Total Orders\s*\(Delivered \+ Cancelled\)\s*(\d+)", text_blob)
        total_orders = int(orders_match.group(1)) if orders_match else 0
        utr_match = re.search(r"Bank UTR\s*([A-Z0-9]+)", text_blob)
        utr = utr_match.group(1).strip() if utr_match else ""
        summary_data.append({
            "File": os.path.basename(file),
            "Brand Name": brand_name,
            "Payout Period": payout_period,
            "Payout Date": payout_date,
            "Total Payout": total_payout,
            "Total Orders": total_orders,
            "UTR": utr
        })
    except Exception as e:
        print(f"Error processing {file}: {e}")
summary_df = pd.DataFrame(summary_data)
# Removing 'nan' values
summary_df['Payout Period'] = summary_df['Payout Period'].replace({r'\n': '', 'nan': ''}, regex=True).str.strip()
summary_df['Payout Date'] = summary_df['Payout Date'].replace({r'\n': '', 'nan': ''}, regex=True).str.strip()
summary_df_clean = summary_df.dropna(subset=['Payout Period', 'Payout Date'])
print(summary_df_clean.head())
