// ? Provee toda la lógica de filtrado de la pestaña de "productos"
document.addEventListener("DOMContentLoaded", () => {

    // * Agarramos todos los <input> de tipo checkbox por cada sección de filtrado
    const checkbox_price_range_options = document.querySelectorAll("input[name='price-range']");
    const checkbox_category_options = document.querySelectorAll("input[name='category']");
    const checkbox_gender_options = document.querySelectorAll("input[name='gender']");
    const select_ordering_options = document.querySelector("select[name='order']");

    // * Y a cada uno de ellos les agregamos la funcionalidad de "fetch_filtered_products" al marcar o desmarcar el checkbox
    checkbox_price_range_options.forEach(option => option.addEventListener("click", fetch_filtered_products));
    checkbox_category_options.forEach(option => option.addEventListener("click", fetch_filtered_products));
    checkbox_gender_options.forEach(option => option.addEventListener("click", fetch_filtered_products));
    select_ordering_options.addEventListener("change", fetch_filtered_products);
    async function fetch_filtered_products(){
        const selectedPriceRanges = Array.from(document.querySelectorAll("input[name='price-range']:checked")).map(checkbox => checkbox.value);
        const selectedCategories = Array.from(document.querySelectorAll("input[name='category']:checked")).map(checkbox => checkbox.value);
        const selectedGenders = Array.from(document.querySelectorAll("input[name='gender']:checked")).map(checkbox => checkbox.value);
        const selectedOrder = document.querySelector("select[name='order']").value;

        console.log("selectedOrder:", selectedOrder)

        // * Construir la URL con parámetros de consulta
        const queryParams = new URLSearchParams();
        selectedPriceRanges.forEach(priceRange => queryParams.append('price_range', priceRange));
        selectedCategories.forEach(category => queryParams.append('category', category));
        selectedGenders.forEach(gender => queryParams.append('gender', gender));
        queryParams.append('sort_by', selectedOrder);

        let response = await axios.get(`/filter-products?${queryParams}`)
        let filtered_products = response.data
        console.log(filtered_products)

        filtered_products.forEach(product => console.log(product.nombre_producto))

    }

    async function update_product_list(products){

    }
});