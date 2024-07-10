// * Crea una tabla en el DOM con los datos de la tabla seleccionada
async function create_table(table_name) {
    try {
        let table_body = await select_all(table_name);
        let table_columns = await select_columns(table_name);
        let table_columns_grid = table_columns.map(column => ({field: column, filter: true}));

        // * Se agrega la columna personalizada con los botones al grid
        table_columns_grid.push({
            headerName: "",
            cellRenderer: ButtonCellRenderer,
            sortable: false,
            filter: false,
            minWidth: 150,
            maxWidth: 150
        });

        const gridOptions = {
            rowData: table_body,
            columnDefs: table_columns_grid,
            defaultColDef: {
                flex: 1,
                filter: "agTextColumnFilter",
                floatingFilter: true,
            },
            pagination: true,
            paginationPageSize: 10,
            paginationPageSizeSelector: [10, 20, 50, 100]
        }

        const table = document.querySelector("#main_table");
        while (table.firstChild) {
            table.removeChild(table.firstChild);
        }

        gridApi = agGrid.createGrid(table, gridOptions);

    } catch (error) {
        console.error(error);
    }
}
window.onload = () => {
    const current_table = get_current_table_name()
    if (current_table) {
        create_table(current_table);
    }
};


