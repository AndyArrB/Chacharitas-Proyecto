document.addEventListener("DOMContentLoaded", () => {
    const checkbox_price_range_options = document.querySelectorAll("input[name='price-range']");
    const checkbox_category_options = document.querySelectorAll("input[name='category']");
    const checkbox_gender_options = document.querySelectorAll("input[name='gender']");
    const select_ordering_options = document.querySelector("select[name='order']");

    checkbox_price_range_options.forEach(option => option.addEventListener("click", fetch_filtered_products));
    checkbox_category_options.forEach(option => option.addEventListener("click", fetch_filtered_products));
    checkbox_gender_options.forEach(option => option.addEventListener("click", fetch_filtered_products));
    select_ordering_options.addEventListener("change", fetch_filtered_products);

    async function fetch_filtered_products() {
        const selectedPriceRanges = Array.from(document.querySelectorAll("input[name='price-range']:checked")).map(checkbox => checkbox.value);
        const selectedCategories = Array.from(document.querySelectorAll("input[name='category']:checked")).map(checkbox => checkbox.value);
        const selectedGenders = Array.from(document.querySelectorAll("input[name='gender']:checked")).map(checkbox => checkbox.value);
        const selectedOrder = document.querySelector("select[name='order']").value;

        const queryParams = new URLSearchParams();
        selectedPriceRanges.forEach(priceRange => queryParams.append('price_range', priceRange));
        selectedCategories.forEach(category => queryParams.append('category', category));
        selectedGenders.forEach(gender => queryParams.append('gender', gender));
        queryParams.append('sort_by', selectedOrder);

        let response = await axios.get(`/filter-products?${queryParams}`);
        let filtered_products = response.data;
        console.log(filtered_products)

        update_product_list(filtered_products);
    }

    function update_product_list(products) {
        const productContainer = document.querySelector("#product-container");
        productContainer.innerHTML = "";

        products.forEach(product => {
            const productElement = document.createElement("div");
            productElement.classList.add("col-md-4");
            productElement.innerHTML = `
                <div class="card mb-4 product-wap rounded-0">
                    <div class="card rounded-0">
                        <img class="card-img rounded-0 img-fluid" src="${product.image_url}">
                        <div class="card-img-overlay rounded-0 product-overlay d-flex align-items-center justify-content-center">
                            <ul class="list-unstyled">
                                <li><a class="btn btn-success text-white mt-2" href="/shop-single/${product.id}"><i class="far fa-eye"></i></a></li>
                            </ul>
                        </div>
                    </div>
                    <div class="card-body text-center">
                        <a href="/shop-single/${product.id}" class="h3 text-decoration-none text-center">${product.nombre_producto}</a>
                        <div class="row mt-2">
                            <div class="col-md-4">
                                <img class="img-fluid profile-picture-mini" src="${product.user_image_url}" alt="User Image">
                                <small>${product.user_name}</small>
                            </div>
                            <div class="col-md-8 d-flex flex-column align-items-center justify-content-center">
                                <a href="/shop-single/${product.id}" class="h3 text-decoration-none">${product.municipio}</a>
                                <a><small>${product.colonia}</small></a>
                            </div>
                        </div>
                        <p class="text-center mb-0 mt-2">$${product.precio}</p>
                    </div>
                </div>
            `;
            productContainer.appendChild(productElement);
        });
    }
});