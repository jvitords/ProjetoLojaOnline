from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Produtos (simulados a partir de um arquivo CSV)
products = [
    {"id": 1, "name": "Carrinho Hot Wheels", "price": 18.99},
    {"id": 2, "name": "Boneco Ben 10", "price": 43.89},
    {"id": 3, "name": "Boneca Barbie", "price": 39.99},
    {"id": 4, "name": "Pista de carrinhos", "price": 89.90},
    {"id": 5, "name": "Brinquedo Lego", "price": 119.90},
    {"id": 6, "name": "Ursinho de Pelúcia", "price": 30.80},
    {"id": 7, "name": "Banco Imobiliário", "price": 120.79},
    {"id": 8, "name": "Boneco Sônic", "price": 136.49},
    {"id": 9, "name": "Nerf", "price": 140.90},
    {"id": 10, "name": "Amoeba", "price": 6.79}
]

# Carrinho de compras (inicialmente vazio)
cart = []

@app.route('/', methods=['GET'])
def index():
    search_query = request.args.get('search')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    filtered_products = products

    if search_query:
        filtered_products = [product for product in filtered_products if search_query.lower(
        ) in product['name'].lower()]

    if min_price:
        min_price = float(min_price)
        filtered_products = [
            product for product in filtered_products if product['price'] >= min_price]

    if max_price:
        max_price = float(max_price)
        filtered_products = [
            product for product in filtered_products if product['price'] <= max_price]

    total_price = calculate_total_price()

    return render_template('index.html', products=filtered_products, cart=cart, total_price=total_price, search_query=search_query, min_price=min_price, max_price=max_price)

@app.route('/cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form.get('product_id'))
    quantity = int(request.form.get('quantity'))

    product = next((p for p in products if p['id'] == product_id), None)

    if product:
        cart.append({'product': product, 'quantity': quantity})

    return redirect('/')

@app.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    product_id = int(request.form.get('product_id'))

    for item in cart:
        if item['product']['id'] == product_id:
            cart.remove(item)
            break

    return redirect('/')

def calculate_total_price():
    total = 0.0
    for item in cart:
        total += item['product']['price'] * item['quantity']
    return total

if __name__ == '__main__':
    app.run(debug=True)
