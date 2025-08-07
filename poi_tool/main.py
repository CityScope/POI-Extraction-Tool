import argparse
import pandas as pd
from src.extractor import geocode_address, get_pois

def main():
    parser = argparse.ArgumentParser(description="Extract POIs from OpenStreetMap.")
    parser.add_argument("--address", type=str, help="Address to search for.")
    parser.add_argument("--lat", type=float, help="Latitude of the center point.")
    parser.add_argument("--lon", type=float, help="Longitude of the center point.")
    parser.add_argument("--output", type=str, default="pois.csv", help="Output CSV file name.")
    
    args = parser.parse_args()
    
    lat, lon = None, None
    
    if args.address:
        lat, lon = geocode_address(args.address)
        if not lat:
            print(f"Could not geocode address: {args.address}")
            return
            
    elif args.lat and args.lon:
        lat, lon = args.lat, args.lon
    
    else:
        print("Please provide either an address or latitude/longitude.")
        parser.print_help()
        return

    print(f"Searching for POIs around ({lat}, {lon})...")
    
    pois_df = get_pois(lat, lon)
    
    if pois_df.empty:
        print("No POIs found in the specified area.")
    else:
        pois_df.to_csv(args.output, index=False)
        print(f"Successfully extracted {len(pois_df)} POIs to {args.output}")

if __name__ == "__main__":
    main()
