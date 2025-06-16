import requests
import pandas as pd
from datetime import datetime

# === API Info ===
api_key = "449d6f97d3msh849532c4193299fp10eb05jsndb43a6a85b5f"
url = "https://flights-sky.p.rapidapi.com/flights/price-calendar-web"
headers = {
    "x-rapidapi-host": "flights-sky.p.rapidapi.com",
    "x-rapidapi-key": api_key
}

# === Parameters ===
from_entity = "TLV"  # Always Israel
destinations = ['MXP', 'FCO', 'VIE', 'IST']  # Milan, Rome, Vienna, Istanbul
months = ['2025-06', '2025-07']

# === Collect results ===
all_results = []

for dest in destinations:
    for month in months:
        print(f"\n📡 Fetching TLV → {dest} for {month}...")
        querystring = {
            "fromEntityId": from_entity,
            "toEntityId": dest,
            "yearMonth": month
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        try:
            traces = data["data"].get("Traces", {})
            price_grid = data["data"].get("PriceGrids", {}).get("Grid", [[]])[0]

            for cell in price_grid:
                if "Direct" in cell:
                    price = cell["Direct"].get("Price")
                    trace_refs = cell["Direct"].get("TraceRefs", [])
                    currency = cell.get("DirectOutbound", {}).get("Currency", "Unknown")

                    for ref in trace_refs:
                        trace = traces.get(ref, "")
                        try:
                            parts = trace.split("*")
                            raw_date = parts[4]
                            flight_date = datetime.strptime(raw_date, "%Y%m%d").strftime("%Y-%m-%d")
                            airline = parts[5].upper()
                            all_results.append({
                                "From": from_entity,
                                "To": dest,
                                "Month": month,
                                "Date": flight_date,
                                "Price": price,
                                "Currency": currency,
                                "Airline": airline
                            })
                        except:
                            continue

        except Exception as e:
            print(f"❌ Failed to process {dest} - {month}: {e}")

# === Save to Excel ===
if all_results:
    df = pd.DataFrame(all_results)
    df.to_excel("flights_TLV_multi_dest.xlsx", index=False)
    print("\n✅ Excel file created: flights_TLV_multi_dest.xlsx")
else:
    print("\n🚫 No data was retrieved.")
