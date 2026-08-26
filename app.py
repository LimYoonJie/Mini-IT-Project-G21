from flask import Flask, render_template

app = Flask(__name__)


products = [
    {
        "id": 1,
        "name": "Gaming Mouse Pro",
        "category": "Gaming",
        "price": 99.90,
        "stock": 32,
        "description": "High-performance gaming mouse with precision tracking."
    },
    {
        "id": 2,
        "name": "Mechanical Keyboard",
        "category": "Accessories",
        "price": 249.90,
        "stock": 14,
        "description": "Mechanical keyboard designed for gaming and productivity."
    },
    {
        "id": 3,
        "name": "Wireless Headset",
        "category": "Gaming",
        "price": 159.90,
        "stock": 0,
        "description": "Wireless gaming headset with immersive audio."
    },
    {
        "id": 4,
        "name": "4K Monitor",
        "category": "Electronics",
        "price": 1299.90,
        "stock": 8,
        "description": "High-resolution 4K monitor for gaming and work."
    }
]


@app.route("/")
def home():
    return render_template(
        "home.html",
        products=products
    )


@app.route("/products")
def product_list():
    return render_template(
        "products.html",
        products=products
    )


@app.route("/product/<int:product_id>")
def product_detail(product_id):

    product = next(
        (p for p in products if p["id"] == product_id),
        None
    )

    if product is None:
        return "Product not found", 404

    return render_template(
        "product_detail.html",
        product=product
    )


if __name__ == "__main__":
    app.run(debug=True)