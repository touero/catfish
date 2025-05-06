# Catfish

<!--
<p align="center">
    <img src="https://img.shields.io/badge/python_-%3E%3D3.8-blue" alt="">
    <img src="https://img.shields.io/badge/license_-MIT-blue" alt="">
    <a href="https://www.mysql.com/"><img src="https://img.shields.io/badge/-mysql-grey?style=plastic&logo=mysql" alt=""/></a>
    <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/fastapi-grey?style=plastic&logo=fastapi" alt=""></a>
    <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/docker-grey?style=plastic&logo=docker" alt=""></a>
    <a href="https://dataease.io/"><img src="https://img.shields.io/badge/dataease-grey" alt=""></a>
</p>
-->

## Repository Introduction
An easy-to-learn, lightweight, easy-to-deploy, download web page based on Django.
![login_preview](https://github.com/touero/catfish/blob/master/static/image/login.png)
![index_preview](https://github.com/touero/catfish/blob/master/static/image/index.png)  

[Click here to check the web video](https://github.com/touero/catfish/blob/master/static/image/video.webm)

## Install

### Clone this repo
This project uses [python](https://www.python.org/) [git](https://git-scm.com/). Go check them out if you don't have them locally installed.
```shell
git clone https://github.com/weiensong/catfish.git
```
### env
Create virtual environment installation dependencies
```shell
python -m venv .venv && 
source ./venv/bin/activate && 
pip install -r requirements.txt
```
## Usage
```shell
python manage.py runserver
```

### Create your own super user
```shell
python manage.py createsuperuser
```

### Database Migration Guide
Django uses a migration system to keep the database schema in sync with your models `models.py`.
 - Create migration files based on model changes:
 ```shell
python manage.py makemigrations
```
- Apply migrations to update the database schema:
```shell
python manage.py migrate
```

## Related Efforts

- [django](https://www.djangoproject.com/)
- [bootstrap](https://getbootstrap.com/)


## Maintainers
[@touero](https://github.com/touero)


## Contributing


Feel free to dive in! [Open an issue](https://github.com/weiensong/catfish/issues) or submit PRs.

Standard Python follows the [Python PEP-8](https://peps.python.org/pep-0008/) Code of Conduct.


### Contributors

This project exists thanks to all the people who contribute.



## License

[GNU General Public License v3.0](https://github.com/weiensong/opsariichthys-bidens/blob/master/LICENSE) © weiensong

