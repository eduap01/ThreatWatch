#!/bin/bash

# Nombre del contenedor de PostgreSQL
CONTAINER_NAME=threatwatch_postgres_1
# Base de datos
DB_NAME=threatwatch
# Usuario
DB_USER=postgres
# Archivo temporal de volcado
DUMP_FILE=threatwatch_backup_local.sql

echo "Exportando base de datos desde local..."
pg_dump -h localhost -U $DB_USER $DB_NAME > $DUMP_FILE

echo "Importando en contenedor..."
docker cp $DUMP_FILE $CONTAINER_NAME:/tmp/$DUMP_FILE
docker exec -t $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -f /tmp/$DUMP_FILE

echo "¡Sincronización completa del local al contenedor!"
