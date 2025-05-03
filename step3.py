import pandas as pd
import glob
import os

folder_path = "/home/spoorthy/Downloads/Cleaning_of_Data_and_Merging_into_single_excel/Payout_Summary_and_Order_Level_Sales"
excel_files = glob.glob(os.path.join(folder_path, "*.xlsx"))
payout_breakup_data = []
for file in excel_files:
    try:
        df = pd.read_excel(file, sheet_name=0, header=None)
        brand_name = df.iloc[4, 1] if df.shape[0] > 4 and df.shape[1] > 1 else "NotFoundInDoc"
        xls = pd.ExcelFile(file)        
        order_level_data = None
        for sheet in xls.sheet_names:
            sheet_df = pd.read_excel(xls, sheet_name=sheet, header=None)
            if sheet_df.iloc[23, 1] == "Order Level":
                order_level_data = sheet_df.iloc[23:].reset_index(drop=True)
                break
        if order_level_data is None:
            print(f"No 'Order Level' data found in file: {file}")
            continue
        order_level_data = order_level_data.loc[:, ~order_level_data.columns.astype(str).str.contains("^Unnamed")]
        order_level_data.reset_index(drop=True, inplace=True)
        order_level_data["Brand Name"] = brand_name
        order_level_data["Source File"] = os.path.basename(file)
        payout_breakup_data.append(order_level_data)

    except Exception as e:
        print(f"Failed to process file {file}:\n{e}")
breakup_summary_df = pd.concat(payout_breakup_data, ignore_index=True)
print(breakup_summary_df.head())
