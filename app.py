from flask import Flask, render_template

app = Flask(__name__)


products = [
    {
        "id": 1,
        "name": "Cat1",
        "category": "(category)",
        "price": 67.00,
        "stock": 32,
        "image": "https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif",
        "description": "temp desc."
    },
    {
        "id": 2,
        "name": "Cat2",
        "category": "(category)",
        "price": 67.00,
        "stock": 14,
        "image": "https://media.giphy.com/media/mlvseq9yvZhba/giphy.gif",
        "description": "temp desc."
    },
    {
        "id": 3,
        "name": "Cat3",
        "category": "(category)",
        "price": 159.90,
        "stock": 0,
        "image": "https://media.giphy.com/media/ICOgUNjpvO0PC/giphy.gif",
        "description": "temp desc."
    },
    {
        "id": 4,
        "name": "Cat4",
        "category": "(category)",
        "price": 1299.90,
        "stock": 8,
        "image": "https://media.giphy.com/media/13CoXDiaCcCoyk/giphy.gif",
        "description": "temp desc."
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