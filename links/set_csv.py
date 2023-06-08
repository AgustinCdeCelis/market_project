from datetime import date

def export_links_to_csv(links, store_name):
    today = date.today()
    d1 = today.strftime("%Y%m%d")
    filename = f'./csv/{store_name}/{d1}{store_name}_links.csv'
    links.to_csv(filename, encoding='utf-8', index=False)
    print(f'CSV file exported: {filename}')