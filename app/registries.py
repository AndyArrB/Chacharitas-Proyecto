from app.models import Municipio, Colonia, Calle, Direccion, Marca, Categoria, Genero, FormaPago, Color, \
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
    Direccion: [
        {"num_int": "101", "num_ext": "123", "calle_id": 7}
    ],
    Marca: [
        {"nombre_marca": "Carter's"},
        {"nombre_marca": "Gerber"},
        {"nombre_marca": "Baby Gap"},
        {"nombre_marca": "H&M Kids"},
        {"nombre_marca": "OshKosh B'gosh"}
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
        {"nombre_color": "Blanco"}
    ],
    Material: [
        {"nombre_material": "Algodón"},
        {"nombre_material": "Poliéster"},
        {"nombre_material": "Lana"},
        {"nombre_material": "Seda"},
        {"nombre_material": "Lino"}
    ],
    TipoTamaño: [
        {"tipo_tamaño": "ropa"},
        {"tipo_tamaño": "zapato"},
        {"tipo_tamaño": "dimensiones"}
    ],
    DetalleTamaño: [
        {"id_tipo_tamaño": 1, "tamaño": "3 Meses"},
        {"id_tipo_tamaño": 1, "tamaño": "4 meses"},
        {"id_tipo_tamaño": 1, "tamaño": "8 meses"},
        {"id_tipo_tamaño": 1, "tamaño": "10 meses"},
        {"id_tipo_tamaño": 3, "tamaño": "30x20x10"}
    ],
    Estatus: [
        {"nombre": "En proceso"},
        {"nombre": "completado"},
        {"nombre": "cancelado"}
    ],
    TipoSuscripcion: [
        {"nombre_suscripcion": "normal", "precio": 0},
        {"nombre_suscripcion": "junior", "precio": 60},
        {"nombre_suscripcion": "vip", "precio": 180}
    ]
}