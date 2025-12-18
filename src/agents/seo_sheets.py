import pandas as pd

def get_all_data_from_google_sheet(url):
    """
    Reads all sheets from a Google Sheets URL into a dictionary of DataFrames.
    """
    try:
        # 1. Extract the unique File ID from the URL
        # Logic: Find the part between '/d/' and the next '/'
        file_id = url.split('/d/')[1].split('/')[0]
        
        # 2. Construct a download URL that exports the whole file as Excel (.xlsx)
        # This trick bypasses the need to know individual GIDs
        export_url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx"
        
        print(f"Accessing: {export_url}")
        
        # 3. Read the data
        # sheet_name=None tells pandas to read ALL tabs found in the file
        all_sheets = pd.read_excel(export_url, sheet_name=None)
        
        return all_sheets

    except Exception as e:
        print(f"Error accessing the sheet. Make sure the sheet is Public (Anyone with link).")
        print(f"Error details: {e}")
        return None

# --- Usage Example ---
current_link = "https://docs.google.com/spreadsheets/d/1zzf4ax_H2WiTBVrJigGjF2Q3Yz-qy2qMCbAMKvl6VEE/edit?gid=1438203274"

# This returns a dictionary: {'SheetName': DataFrame, ...}
data_dict = get_all_data_from_google_sheet(current_link)

if data_dict:
    print(f"\nSuccess! Found {len(data_dict)} sheets:")
    
    # You can now loop through them dynamically
    for sheet_name, df in data_dict.items():
        print(f"- Sheet '{sheet_name}' has {len(df)} rows.")
        
        # Example: accessing the 'accessibility_all' sheet if it exists
        if sheet_name == "accessibility_all":
            print("  -> Found the accessibility data!")
            # print(df.head())