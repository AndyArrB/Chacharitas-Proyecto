// * Este archivo solo se encarga de realizar una clase que contenga toda la funcionalidad
// * de los botones que se insertan en la última columna de la tabla de AgGrid.

class ButtonCellRenderer {
    init(params) {
        this.params = params;
        this.eGui = document.createElement('div');
        this.eGui.className = "button-container"

        const table_name = get_current_table_name()
        const row_data = this.params.node.data
        const id = row_data.id

        let editButton = document.createElement('button');
        editButton.className = "btn-edit btn btn-warning";
        editButton.innerHTML = '<i class="bi bi-pencil-square "></i>';
        editButton.addEventListener("click", async () => {
            show_modal({id: "main_modal", action:"PUT", registry_id: id})
        })

        let deleteButton = document.createElement('button');
        deleteButton.className = "btn-delete btn btn-danger";
        deleteButton.innerHTML = '<i class="bi bi-trash "></i>';
        deleteButton.addEventListener('click', async () => {
            await delete_from({table: table_name, id: id})
            gridApi.applyTransaction({ remove: [row_data] });
        });

        this.eGui.appendChild(editButton);
        this.eGui.appendChild(deleteButton);
    }

    getGui() {
        return this.eGui;
    }

    refresh(params) {
        return true;
    }
}
