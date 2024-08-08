from app.models import Municipio, Colonia, Calle, Marca, Categoria, Genero, FormaPago, Color, \
    Material, TipoTamaño, DetalleTamaño, Producto, TipoSuscripcion, Suscripcion, Estatus, Pedido, DetallePedido

data = {
    Genero: [
        {"nombre_genero": "Masculino"},
        {"nombre_genero": "Femenino"}
    ],
    Municipio: [
        {"nombre_municipio": "El Marqués"},
        {"nombre_municipio": "Querétaro"},
        {"nombre_municipio": "Corregidora"}
    ],
    Colonia: [
        {"nombre_colonia": "Centro", "cp": "76000", "municipio_id": 2},  # Querétaro
        {"nombre_colonia": "Juriquilla", "cp": "76230", "municipio_id": 2},  # Querétaro
        {"nombre_colonia": "El Refugio", "cp": "76146", "municipio_id": 2},  # Querétaro
        {"nombre_colonia": "San Pablo", "cp": "76125", "municipio_id": 2},  # Querétaro
        {"nombre_colonia": "Cimatario", "cp": "76030", "municipio_id": 2},  # Querétaro
        {"nombre_colonia": "El Pueblito", "cp": "76900", "municipio_id": 3},  # Corregidora
        {"nombre_colonia": "Candiles", "cp": "76903", "municipio_id": 3},  # Corregidora
        {"nombre_colonia": "Los Olvera", "cp": "76904", "municipio_id": 3},  # Corregidora
        {"nombre_colonia": "La Pradera", "cp": "76269", "municipio_id": 1},  # El Marqués
        {"nombre_colonia": "Zibatá", "cp": "76269", "municipio_id": 1}  # El Marqués
    ],
    Calle: [
        {"nombre_calle": "Avenida 5 de Febrero", "colonia_id": 1},  # Centro
        {"nombre_calle": "Avenida Constituyentes", "colonia_id": 1},  # Centro
        {"nombre_calle": "Boulevard Bernardo Quintana", "colonia_id": 1},  # Centro
        {"nombre_calle": "Calle Corregidora", "colonia_id": 1},  # Centro
        {"nombre_calle": "Calle Madero", "colonia_id": 1},  # Centro
        {"nombre_calle": "Avenida Juriquilla", "colonia_id": 2},  # Juriquilla
        {"nombre_calle": "Calle Lago de Chapala", "colonia_id": 2},  # Juriquilla
        {"nombre_calle": "Calle Lago de Tequesquitengo", "colonia_id": 2},  # Juriquilla
        {"nombre_calle": "Calle Lago de Zumpango", "colonia_id": 2},  # Juriquilla
        {"nombre_calle": "Calle Lago de Pátzcuaro", "colonia_id": 2},  # Juriquilla
        {"nombre_calle": "Avenida El Refugio", "colonia_id": 3},  # El Refugio
        {"nombre_calle": "Calle Paseo de la Reforma", "colonia_id": 3},  # El Refugio
        {"nombre_calle": "Calle Paseo de los Toros", "colonia_id": 3},  # El Refugio
        {"nombre_calle": "Calle Paseo de las Lomas", "colonia_id": 3},  # El Refugio
        {"nombre_calle": "Calle Paseo de los Andes", "colonia_id": 3},  # El Refugio
        {"nombre_calle": "Avenida San Pablo", "colonia_id": 4},  # San Pablo
        {"nombre_calle": "Calle San Juan", "colonia_id": 4},  # San Pablo
        {"nombre_calle": "Calle San Pedro", "colonia_id": 4},  # San Pablo
        {"nombre_calle": "Calle San Lucas", "colonia_id": 4},  # San Pablo
        {"nombre_calle": "Calle San Mateo", "colonia_id": 4},  # San Pablo
        {"nombre_calle": "Avenida Cimatario", "colonia_id": 5},  # Cimatario
        {"nombre_calle": "Calle Cerro de las Campanas", "colonia_id": 5},  # Cimatario
        {"nombre_calle": "Calle Cerro del Tambor", "colonia_id": 5},  # Cimatario
        {"nombre_calle": "Calle Cerro del Sombrerete", "colonia_id": 5},  # Cimatario
        {"nombre_calle": "Calle Cerro del Cimatario", "colonia_id": 5},  # Cimatario
        {"nombre_calle": "Avenida El Pueblito", "colonia_id": 6},  # El Pueblito
        {"nombre_calle": "Calle Camino Real", "colonia_id": 6},  # El Pueblito
        {"nombre_calle": "Calle Camino a Los Olvera", "colonia_id": 7},  # Los Olvera
        {"nombre_calle": "Calle Camino a Candiles", "colonia_id": 7},  # Candiles
        {"nombre_calle": "Calle Camino a La Pradera", "colonia_id": 9}  # La Pradera
    ],
    Marca: [
        {"nombre_marca": "Carter's"},
        {"nombre_marca": "Gerber"},
        {"nombre_marca": "Baby Gap"},
        {"nombre_marca": "H&M Kids"},
        {"nombre_marca": "OshKosh B'gosh"},
        {"nombre_marca": "Tommy Hilfiger"},
        {"nombre_marca": "Nike"},
        {"nombre_marca": "Lego"},
        {"nombre_marca": "Fisher's Price"},
        {"nombre_marca": "Huggies"},
    ],
    Categoria: [
        {"tipo_categoria": "Calzado"},
        {"tipo_categoria": "Accesorios"},
        {"tipo_categoria": "Juguetes"},
        {"tipo_categoria": "Ropa"},
        {"tipo_categoria": "Cuidado personal"}
    ],
    FormaPago: [
        {"nombre_forma": "Tarjeta de Crédito"},
        {"nombre_forma": "PayPal"},
        {"nombre_forma": "Transferencia Bancaria"}
    ],
    Color: [
        {"nombre_color": "Rojo"},
        {"nombre_color": "Azul"},
        {"nombre_color": "Verde"},
        {"nombre_color": "Amarillo"},
        {"nombre_color": "Naranja"},
        {"nombre_color": "Morado"},
        {"nombre_color": "Rosa"},
        {"nombre_color": "Marrón"},
        {"nombre_color": "Negro"},
        {"nombre_color": "Blanco"},
        {"nombre_color": "Varios"},
    ],
    Material: [
        {"nombre_material": "Algodón"},
        {"nombre_material": "Poliéster"},
        {"nombre_material": "Lana"},
        {"nombre_material": "Seda"},
        {"nombre_material": "Lino"},
        {"nombre_material": "PVC"}
    ],
    TipoTamaño: [
        {"tipo_tamaño": "ropa"},
        {"tipo_tamaño": "zapato"},
        {"tipo_tamaño": "dimensiones"}
    ],
    DetalleTamaño: [
        {"id_tipo_tamaño": 1, "tamaño": "3 Meses"},
        {"id_tipo_tamaño": 1, "tamaño": "6 meses"},
        {"id_tipo_tamaño": 1, "tamaño": "12 meses"},
        {"id_tipo_tamaño": 1, "tamaño": "2 - 3 años"},
        {"id_tipo_tamaño": 1, "tamaño": "3 - 4 años"},
        {"id_tipo_tamaño": 2, "tamaño": "11 cm"},
        {"id_tipo_tamaño": 2, "tamaño": "12 cm"},
        {"id_tipo_tamaño": 2, "tamaño": "13 cm"},
        {"id_tipo_tamaño": 3, "tamaño": "30x20x10"},
        {"id_tipo_tamaño": 3, "tamaño": "60x70x80"}
    ],
    Estatus: [
        {"nombre": "En proceso"},
        {"nombre": "Completado"},
        {"nombre": "Cancelado"}
    ],
    TipoSuscripcion: [
        {"nombre_suscripcion": "normal", "precio": 0},
        {"nombre_suscripcion": "junior", "precio": 60},
        {"nombre_suscripcion": "vip", "precio": 180}
    ],
    Producto: [
        {"nombre_producto": "Camiseta GAP con logo", "cantidad": 2, "precio": 150, "id_categoria": 4, "id_color": 1,
         "id_material": 1, "id_detalle_tamaños": 4, "id_marca": 3, "id_genero": 2, "id_usuario": 1},
        {"nombre_producto": "Playera estampado halloween", "cantidad": 3, "precio": 300, "id_categoria": 4,
         "id_color": 2,
         "id_material": 1, "id_detalle_tamaños": 3, "id_marca": 2, "id_genero": 2, "id_usuario": 2},
        {"nombre_producto": "Playera con logo Tommy", "cantidad": 20, "precio": 100, "id_categoria": 4, "id_color": 3,
         "id_material": 1, "id_detalle_tamaños": 3, "id_marca": 6, "id_genero": 2, "id_usuario": 3},
        {"nombre_producto": "Conjunto sueter pantalón", "cantidad": 5, "precio": 130, "id_categoria": 4, "id_color": 4,
         "id_material": 3, "id_detalle_tamaños": 4, "id_marca": 4, "id_genero": 2, "id_usuario": 4},
        {"nombre_producto": "Chammarra con gorro", "cantidad": 3, "precio": 200, "id_categoria": 4, "id_color": 5,
         "id_material": 3, "id_detalle_tamaños": 3, "id_marca": 4, "id_genero": 1, "id_usuario": 5},
        {"nombre_producto": "Pantalón deportivo", "cantidad": 2, "precio": 150, "id_categoria": 4, "id_color": 6,
         "id_material": 1, "id_detalle_tamaños": 4, "id_marca": 4, "id_genero": 2, "id_usuario": 6},
        {"nombre_producto": "Sueter estampado Nike", "cantidad": 7, "precio": 200, "id_categoria": 4, "id_color": 7,
         "id_material": 1, "id_detalle_tamaños": 4, "id_marca": 7, "id_genero": 1, "id_usuario": 7},
        {"nombre_producto": "Playera gatito", "cantidad": 6, "precio": 60, "id_categoria": 4, "id_color": 8,
         "id_material": 1, "id_detalle_tamaños": 4, "id_marca": 4, "id_genero": 2, "id_usuario": 8},
        {"nombre_producto": "Pantalón tie-dye", "cantidad": 5, "precio": 90, "id_categoria": 4, "id_color": 9,
         "id_material": 1, "id_detalle_tamaños": 5, "id_marca": 4, "id_genero": 2, "id_usuario": 9},
        {"nombre_producto": "Pantalón floreado", "cantidad": 3, "precio": 80, "id_categoria": 4, "id_color": 10,
         "id_material": 3, "id_detalle_tamaños": 5, "id_marca": 4, "id_genero": 2, "id_usuario": 10},
        {"nombre_producto": "Playera my little pony", "cantidad": 1, "precio": 50, "id_categoria": 4, "id_color": 1,
         "id_material": 1, "id_detalle_tamaños": 4, "id_marca": 4, "id_genero": 2, "id_usuario": 1},
        {"nombre_producto": "Playera estampado carretera", "cantidad": 20, "precio": 50, "id_categoria": 4,
         "id_color": 10,
         "id_material": 1, "id_detalle_tamaños": 4, "id_marca": 4, "id_genero": 1, "id_usuario": 2},
        {"nombre_producto": "Vestido con moño", "cantidad": 18, "precio": 150, "id_categoria": 4, "id_color": 10,
         "id_material": 1, "id_detalle_tamaños": 3, "id_marca": 4, "id_genero": 2, "id_usuario": 3},
        {"nombre_producto": "Lego de Aventuras", "cantidad": 10, "precio": 100, "id_categoria": 3, "id_color": 11,
         "id_material": 6, "id_detalle_tamaños": 5, "id_marca": 7, "id_genero": 2, "id_usuario": 4},
        {"nombre_producto": "Rompecabezas animales", "cantidad": 12, "precio": 120, "id_categoria": 3, "id_color": 11,
         "id_material": 6, "id_detalle_tamaños": 5, "id_marca": 8, "id_genero": 2, "id_usuario": 5},
        {"nombre_producto": "Cochecito", "cantidad": 5, "precio": 30, "id_categoria": 3, "id_color": 2,
         "id_material": 6, "id_detalle_tamaños": 9, "id_marca": 8, "id_genero": 2, "id_usuario": 6},
        {"nombre_producto": "Biberón de Estrellas", "cantidad": 10, "precio": 20, "id_categoria": 2, "id_color": 10,
         "id_material": 6, "id_detalle_tamaños": 9, "id_marca": 9, "id_genero": 2, "id_usuario": 7},
        {"nombre_producto": "Carreola", "cantidad": 4, "precio": 1000, "id_categoria": 2, "id_color": 2,
         "id_material": 6, "id_detalle_tamaños": 10, "id_marca": 9, "id_genero": 1, "id_usuario":8},
        {"nombre_producto": "Pañalera", "cantidad": 3, "precio": 200, "id_categoria": 2, "id_color": 10,
         "id_material": 2, "id_detalle_tamaños": 9, "id_marca": 9, "id_genero": 1, "id_usuario": 9},
        {"nombre_producto": "Andadera", "cantidad": 4, "precio": 500, "id_categoria": 2, "id_color": 10,
         "id_material": 6, "id_detalle_tamaños": 10, "id_marca": 8, "id_genero": 2, "id_usuario":10},
        {"nombre_producto": "Sombrero del Sol", "cantidad": 5, "precio": 100, "id_categoria": 2, "id_color": 4,
         "id_material": 4, "id_detalle_tamaños": 4, "id_marca": 4, "id_genero": 2, "id_usuario": 1},
        {"nombre_producto": "Bufanda de Otoño", "cantidad": 8, "precio": 200, "id_categoria": 2, "id_color": 5,
         "id_material": 5, "id_detalle_tamaños": 5, "id_marca": 5, "id_genero": 1, "id_usuario": 2},
        {"nombre_producto": "Guantes de Uva", "cantidad": 12, "precio": 150, "id_categoria": 2, "id_color": 6,
         "id_material": 1, "id_detalle_tamaños": 1, "id_marca": 1, "id_genero": 2, "id_usuario": 3},
        {"nombre_producto": "Calcetines de Medianoche", "cantidad": 25, "precio": 50, "id_categoria": 4, "id_color": 9,
         "id_material": 4, "id_detalle_tamaños": 4, "id_marca": 4, "id_genero": 1, "id_usuario": 4},
        {"nombre_producto": "Peluche de Sueños", "cantidad": 15, "precio": 250, "id_categoria": 3, "id_color": 1,
         "id_material": 1, "id_detalle_tamaños": 1, "id_marca": 1, "id_genero": 1, "id_usuario": 5},
        {"nombre_producto": "Coche de Carrera", "cantidad": 20, "precio": 300, "id_categoria": 3, "id_color": 2,
         "id_material": 2, "id_detalle_tamaños": 2, "id_marca": 2, "id_genero": 2, "id_usuario": 6},
        {"nombre_producto": "Muñeca de Fantasía", "cantidad": 18, "precio": 350, "id_categoria": 3, "id_color": 3,
         "id_material": 3, "id_detalle_tamaños": 3, "id_marca": 3, "id_genero": 1, "id_usuario": 7},
        {"nombre_producto": "Lego de Aventuras", "cantidad": 10, "precio": 500, "id_categoria": 3, "id_color": 4,
         "id_material": 4, "id_detalle_tamaños": 4, "id_marca": 4, "id_genero": 2, "id_usuario": 8},
        {"nombre_producto": "Rompecabezas de Ingenio", "cantidad": 12, "precio": 150, "id_categoria": 3, "id_color": 5,
         "id_material": 5, "id_detalle_tamaños": 5, "id_marca": 5, "id_genero": 1, "id_usuario": 9},
        {"nombre_producto": "Biberón de Estrellas", "cantidad": 30, "precio": 100, "id_categoria": 5, "id_color": 7,
         "id_material": 2, "id_detalle_tamaños": 2, "id_marca": 2, "id_genero": 1, "id_usuario": 10},
    ]
}
