const searchInput =
    document.getElementById("searchInput");

const categoryFilter =
    document.getElementById("categoryFilter");

const statusFilter =
    document.getElementById("statusFilter");


function filterProducts() {

    const search =
        searchInput.value.toLowerCase();

    const category =
        categoryFilter.value.toLowerCase();

    const status =
        statusFilter.value.toLowerCase();


    const products =
        document.querySelectorAll(".product-row");


    products.forEach(product => {

        const name =
            product.dataset.name;

        const productCategory =
            product.dataset.category;

        const stock =
            Number(product.dataset.stock);


        const matchesSearch =
            name.includes(search);


        const matchesCategory =
            category === "all" ||
            productCategory === category;


        const matchesStatus =
            status === "all" ||
            (status === "active" && stock > 0) ||
            (status === "out" && stock === 0);


        product.style.display =
            matchesSearch &&
            matchesCategory &&
            matchesStatus
                ? "grid"
                : "none";

    });

}


searchInput?.addEventListener(
    "input",
    filterProducts
);


categoryFilter?.addEventListener(
    "change",
    filterProducts
);


statusFilter?.addEventListener(
    "change",
    filterProducts
);


/* Delete modal */

function confirmDelete(id, name) {

    const modal =
        document.getElementById("deleteModal");

    const productName =
        document.getElementById("deleteProductName");

    const form =
        document.getElementById("deleteForm");


    productName.textContent = name;

    form.action =
        `/delete-product/${id}`;

    modal.classList.add("show");

}


function closeDeleteModal() {

    const modal =
        document.getElementById("deleteModal");

    modal.classList.remove("show");

}


/* Close when clicking outside */

document
    .getElementById("deleteModal")
    ?.addEventListener(
        "click",
        event => {

            if (
                event.target.id ===
                "deleteModal"
            ) {

                closeDeleteModal();

            }

        }
    );


/* Escape key */

document.addEventListener(
    "keydown",
    event => {

        if (event.key === "Escape") {

            closeDeleteModal();

        }

    }
);