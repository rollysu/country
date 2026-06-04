import csv
import ipaddress
import sys
from collections import defaultdict
from pathlib import Path

input_name = sys.argv[1]
INPUT_FILE = f"{input_name}.csv"
OUTPUT_DIR = Path(f"db/{input_name}")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

countries = defaultdict(list)

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    
    first_row = next(reader)
    try:
        ipaddress.ip_address(first_row[0].strip())
        f.seek(0)
        reader = csv.reader(f)
    except ValueError:
        pass
    
    for row in reader:
        if len(row) < 3:
            continue
            
        ip_range_start = row[0].strip()
        ip_range_end = row[1].strip()
        country_code = row[2].strip().upper()
        
        if not country_code:
            continue
            
        try:
            start = ipaddress.ip_address(ip_range_start)
            end = ipaddress.ip_address(ip_range_end)
            
            networks = ipaddress.summarize_address_range(start, end)
            
            for network in networks:
                countries[country_code].append(str(network))
                
        except (ValueError, ipaddress.AddressValueError):
            continue

for code, networks in countries.items():
    clean_code = code.lower().replace(' ', '_').replace('-', '_')
    unique_networks = sorted(set(networks))
    
    # .lst
    lst_file = OUTPUT_DIR / f"{clean_code}.lst"
    with open(lst_file, "w", encoding="utf-8") as f:
        f.write("\n".join(unique_networks))
    
    # .yaml
    yaml_file = OUTPUT_DIR / f"{clean_code}.yaml"
    with open(yaml_file, "w", encoding="utf-8") as f:
        f.write("payload:\n")
        for net in unique_networks:
            f.write(f"  - {net}\n")
