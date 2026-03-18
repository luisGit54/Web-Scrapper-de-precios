import request
from bs4 import BeatifulSoup
import csv
import time

BASE_URL = "http://books.toscrape.com/catalogue/page-1.html"

def fetch_page(url):
  #"de aqui se sacara el contenido HTML" #
  try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Lanza error si el status no es 200
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al obtener la página: {e}")
        return None

def parse_products(html):
    """Extrae nombre y precio de los productos del HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    products = []
    
    # Buscamos todos los artículos en la página
    articles = soup.find_all('article', class_='product_pod')
    
    for article in articles:
        try:
            # Extraer título (está en el atributo 'alt' de la imagen)
            title = article.h3.a['title']
            
            # Extraer precio (buscamos el elemento con clase 'price_color')
            price = article.find('p', class_='price_color').text.strip()
            
            products.append({
                'titulo': title,
                'precio': price
            })
            print(f"✅ Procesado: {title} - {price}")
            
        except AttributeError as e:
            print(f"⚠️ Error al procesar un producto: {e}")
            continue  # Continuamos con el siguiente si uno falla
    
    return products

def save_to_csv(products, filename='productos.csv'):
    #Guarda la lista de productos en un archivo CSV.
    if not products:
        print("⚠️ No hay productos para guardar.")
        return
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['titulo', 'precio'])
            writer.writeheader()
            writer.writerows(products)
        print(f"💾 Datos guardados exitosamente en '{filename}'")
    except IOError as e:
        print(f"❌ Error al guardar el archivo: {e}")

def main():
    #Función principal que orquesta el scraping.
    print("🚀 Iniciando Web Scraper de Precios...")
    
    html = fetch_page(BASE_URL)
    if not html:
        return
    
    products = parse_products(html)
    save_to_csv(products)
    
    print(f"\n📊 Total de productos extraídos: {len(products)}")
    print("✨ ¡Proceso completado!")

if __name__ == "__main__":
    main()
