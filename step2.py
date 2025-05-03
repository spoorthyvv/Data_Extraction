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
        target_sheet = None
        for sheet in xls.sheet_names:
            if "payout breakup" in sheet.lower():
                target_sheet = sheet
                break
        if not target_sheet:
            print(f"Not Found in file:{file}")
            continue
        raw_sheet = pd.read_excel(xls, sheet_name=target_sheet, header=None)
        header_row_idx = None
        for i, row in raw_sheet.iterrows():
            if row.astype(str).str.contains("Particulars", case=False).any():
                header_row_idx = i
                break

        if header_row_idx is None:
            print(f"No row found in sheet '{target_sheet}' of file: {file}")
            continue
        payout_df = pd.read_excel(xls, sheet_name=target_sheet, header=header_row_idx)
        payout_df = payout_df.loc[:, ~payout_df.columns.astype(str).str.contains("^Unnamed")]
        payout_df.reset_index(drop=True, inplace=True)
        payout_df["Brand Name"] = brand_name
        payout_df["Source File"] = os.path.basename(file)
        payout_breakup_data.append(payout_df)

    except Exception as e:
        print(f"Coudnt process file {file}:\n{e}")
breakup_summary_df = pd.concat(payout_breakup_data, ignore_index=True)
print(breakup_summary_df.head())
