import pandas as pd
from blockchain.blockchain import add_product, get_all_products

def sync_excel_to_blockchain():
    excel_path = r".\data\datasheet.xlsx"
    
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        print(f"❌ Failed to load Excel file: {e}")
        return

    # Handle missing values safely
    df.fillna("", inplace=True)

    # Get data from blockchain
    try:
        blockchain_data = get_all_products()
    except Exception as e:
        print(f"❌ Failed to fetch blockchain data: {e}")
        return

    # Map blockchain data using product_code as key
    blockchain_dict = {
        str(p[0]): {  # hash_code
            "name_registration": str(p[1])
        }
        for p in blockchain_data
    }

    # Track stats
    added, updated, skipped, failed = 0, 0, 0, 0

    for _, row in df.iterrows():
        product_code = str(row['hash_code'])
        current_excel = {
            "name_registration": str(row['name_registration'])
        }

        try:
            if product_code not in blockchain_dict:
                print(f"🆕 Adding new product {product_code} to blockchain...")
                add_product(
                    product_code,
                    current_excel["name_registration"]
                    

                )
                added += 1
            elif blockchain_dict[product_code] != current_excel:
                print(f"🔄 Updating modified product {product_code}...")
                add_product(
                    product_code,
                    current_excel["name_registration"],
                    
                )
                updated += 1
            else:
                print(f"✅ Product {product_code} is up-to-date.")
                skipped += 1
        except Exception as e:
            print(f"❌ Error syncing product {product_code}: {e}")
            failed += 1


    print("\n📦 Sync Summary:")
    print(f"➕ Added: {added}")
    print(f"🔄 Updated: {updated}")
    print(f"⏭️ Skipped (up-to-date): {skipped}")
    print(f"❌ Failed: {failed}")
