
// * Muestra un modal en pantalla
function show_modal({id, action, registry_id = null}){
    let modal_element = document.getElementById(id ?? "main_modal");
    let modal_title = document.querySelector(".modal-title")

    modal_title.textContent = action === "POST" ? "Añadir registro" : "Editar Registro"

    // * Se insertan atributos para que nuestro modal pueda saber si se quiere
    // * añadir o editar un registro. En caso de esto último, se especifica el id.
    modal_element.setAttribute("action", action)
    modal_element.setAttribute("registry-id", registry_id)

    let modal_instance = new bootstrap.Modal(modal_element, {});
    modal_instance.show();
}

// * Obtiene el nombre de la tabla que se está editando al momento
function get_current_table_name(){
    return window.location.pathname.split('/')[2];
}


