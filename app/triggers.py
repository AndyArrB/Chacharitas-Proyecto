from sqlalchemy import text
from app import db

def create_triggers_if_not_exist():
    trigger_names = [
        "after_user_insert", "limit_user_products", "after_detalle_pedido_insert",
        "log_cambios_producto", "update_fecha_renovacion"
    ]
    trigger_sqls = {
        "after_user_insert": """
            CREATE TRIGGER after_user_insert
            AFTER INSERT ON usuarios
            FOR EACH ROW
            BEGIN
                INSERT INTO suscripciones (fecha_inicio, fecha_renovacion, id_cliente, id_tipo_suscripcion)
                VALUES (CURRENT_DATE, NULL, NEW.id, 1);
            END;
        """,
        "limit_user_products": """
            CREATE TRIGGER limit_user_products
            BEFORE INSERT ON productos
            FOR EACH ROW
            BEGIN
                DECLARE product_count INT;
                SELECT COUNT(*) INTO product_count FROM productos WHERE id_usuario = NEW.id_usuario;
                IF (SELECT id_tipo_suscripcion FROM suscripciones WHERE id_cliente = NEW.id_usuario) = 1 AND product_count >= 3 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El usuario con suscripción ID 1 no puede tener más de 3 productos.';
                END IF;
            END;
        """,
        "after_detalle_pedido_insert": """
            CREATE TRIGGER after_detalle_pedido_insert
            AFTER INSERT ON detalles_pedidos
            FOR EACH ROW
            BEGIN
                UPDATE productos SET cantidad = cantidad - NEW.cantidad WHERE id = NEW.id_producto;
            END;
        """,
        "log_cambios_producto": """
            CREATE TABLE IF NOT EXISTS cambios_producto (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_producto INT,
                cantidad_antigua INT,
                cantidad_nueva INT,
                fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TRIGGER log_cambios_producto
            AFTER UPDATE ON productos
            FOR EACH ROW
            BEGIN
                INSERT INTO cambios_producto (id_producto, cantidad_antigua, cantidad_nueva)
                VALUES (OLD.id, OLD.cantidad, NEW.cantidad);
            END;
        """,
        "update_fecha_renovacion": """
            CREATE TRIGGER update_fecha_renovacion
            AFTER UPDATE ON suscripciones
            FOR EACH ROW
            BEGIN
                IF NEW.id_tipo_suscripcion != 1 THEN
                    SET NEW.fecha_renovacion = DATE_ADD(NEW.fecha_inicio, INTERVAL 1 MONTH);
                ELSE
                    SET NEW.fecha_renovacion = NULL;
                END IF;
            END;
        """
    }

    with db.engine.connect() as connection:
        for trigger_name in trigger_names:
            result = connection.execute(text(f"SHOW TRIGGERS LIKE '{trigger_name}'"))
            if result.rowcount == 0:
                connection.execute(text(trigger_sqls[trigger_name]))
                print(f'Trigger {trigger_name} created successfully')
            else:
                print(f'Trigger {trigger_name} already exists')