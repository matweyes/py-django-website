from .settings import *

# Import the dj-database-url package at the beginning of the file
import dj_database_url


DATABASES = {
    'default': dj_database_url.config(
        default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}",
        conn_max_age=600
    )
}
