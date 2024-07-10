let modal = document.getElementById("main_modal")
let modal_form = document.getElementById("modal_form")

modal_form.addEventListener("submit", async function (event) {
    event.preventDefault()
    const table_name = get_current_table_name()
    let form_data = new FormData(this);
    const action = modal.getAttribute("action")
    const registry_id = modal.getAttribute("registry-id")

    switch (action) {
        case("POST"):
            await insert_into({table: table_name, data: form_data});
            break;
        case("PUT"):
            await update_from({table: table_name, data: form_data, id: registry_id})
            break
    }
    await create_table(table_name)
    let bootstrapModal = bootstrap.Modal.getInstance(modal)
    bootstrapModal.hide()
})

let addButton = document.querySelector(".btn-add")
addButton.addEventListener('click', () => {
    show_modal({id: "main_modal", action: "POST"})
});


