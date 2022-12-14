# Justo
Proyecto para la asignacion de hits.

 ### Requerimientos
 - Docker
 - Docker Compose
 

 ### Instalar Docker
 El primer paso es instalar la aplicación Docker de escritorio para su máquina local:
 - [Docker para Mac](https://docs.docker.com/docker-for-mac/install/)
 - [Docker para Windows](https://docs.docker.com/docker-for-windows/install/)
 - [Docker para Linux](https://docs.docker.com/engine/install/#server)

 Docker Compose es una herramienta adicional que se incluye automáticamente con las descargas de Docker para Mac y Windows. Sin embargo, si está en Linux, deberá agregarlo manualmente. Puede hacer esto ejecutando el comando sudo pip install docker-compose una vez completada la instalación de Docker.


### Instalacion.

Clonar el proyecto
```sh
git clone https://github.com/jdht1992/spyagency.git
```

Para crear la imagen ejecutas los siguientes comandos
```sh
cd spyagency
docker-compose up --build
```

### Ejecutar proyecto.

Para ejecutar las migraciones, abrir otra terminal y entrar al contenedor y ejecutar los siguientes comandos.
```sh
docker-compose exec web bash 
python manage.py makemigrations
python manage.py migrate
```
Para cargar los usuarios base se ejecuta el siguiente comando
```sh
python manage.py loaddata fixtures/users.json
```

## Rutas del proyecto
### Acoounts

Los usuarios cargados para hacer pruebas son
```sh
"usuarios"
boss@gmail.com
manager10@gmail.com
hitmen11@gmail.com
hitmen12@gmail.com
hitmen13@gmail.com
manager20@gmail.com
hitmen21@gmail.com
hitmen22@gmail.com
hitmen23@gmail.com
manager30@gmail.com
hitmen31@gmail.com
hitmen32@gmail.com
hitmen33@gmail.com
"contraseña"
1234
```

Ingreso basado en el correo.
```sh
 localhost:8000
```
Puedes registrar a un hitmen
```sh
 localhost:8000/register/
```
### Hits
Muestra todos los hits en el sistema para ese usuario conectado
```sh
 localhost:8000/hits/
```
Muestra detalles sobre un hit
```sh
 localhost:8000/hits/<id>/
```
Crea un hit
```sh
 localhost:8000/hits/create/
```
Actualiza los hits de forma masiva ("no terminado quedo a la mitad")
```sh
 localhost:8000/hits/bulk/
```

### Hitmen
Muestra el listado de los Hitmen
```sh
 localhost:8000/hitmen/
```
Muestra el detalle de un hitmen
```sh
 localhost:8000/hitmen/<id>/
```
