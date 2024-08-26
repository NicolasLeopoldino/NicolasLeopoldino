##SPANSISH

## Descripción

El **Sistema de Fichaje Ejecutivo para empleados** es una aplicación de escritorio desarrollada en Python que permite a los usuarios iniciar sesión mediante LDAP (por ejemplo, en un servidor de Active Directory) y registrar su entrada y salida de manera eficiente. La aplicación está construida utilizando PyQt5 para la interfaz gráfica y se conecta a una base de datos SQL Server para almacenar los registros de fichaje.

### Características

- **Inicio de sesión**: Los usuarios pueden iniciar sesión utilizando sus credenciales LDAP.
- **Registro de fichaje**: Permite registrar la entrada y salida del usuario, asegurando que se realicen correctamente y solo una vez por día.
- **Interfaz gráfica**: Utiliza PyQt5 para una experiencia de usuario intuitiva y atractiva.
- **Validaciones**: Verifica que los fichajes sean válidos y gestiona la conexión con la base de datos de manera segura.

## Requisitos

Para ejecutar este proyecto, necesitas tener instalados los siguientes paquetes de Python:

- `PyQt5` - Para la interfaz gráfica de usuario.
- `ldap3` - Para la conexión LDAP.
- `pyodbc` - Para la conexión a la base de datos SQL Server.
- `requests` - Para obtener la hora actual desde una API web.

Puedes instalar todas las dependencias ejecutando:

pip install -r requirements.txt

#ENGLISH

## Description

The **Employee Time Tracking System** is a desktop application developed in Python that allows users to log in using LDAP (e.g., on an Active Directory server) and record their entry and exit times efficiently. The application is built using PyQt5 for the graphical interface and connects to an SQL Server database to store the time tracking records.

### Features

- **Login**: Users can log in using their LDAP credentials.
- **Time Tracking**: Allows users to register their entry and exit times, ensuring that actions are performed correctly and only once per day.
- **Graphical Interface**: Uses PyQt5 for an intuitive and attractive user experience.
- **Validations**: Ensures valid time tracking entries and manages database connections securely.

## Requirements

To run this project, you need to have the following Python packages installed:

- `PyQt5` - For the graphical user interface.
- `ldap3` - For LDAP connectivity.
- `pyodbc` - For connecting to the SQL Server database.
- `requests` - For obtaining the current time from a web API.

You can install all dependencies by running:

```bash
pip install -r requirements.txt
