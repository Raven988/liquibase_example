# liquibase
Для подробной информации ознакомтесь с [официальной документацией.](https://docs.liquibase.com/home.html)  

Liquibase — это инструмент для управления схемой базы данных, который позволяет отслеживать, версионировать и применять изменения в базе данных. Он особенно полезен в проектах, где есть необходимость в управлении сложными изменениями схемы базы данных, синхронизации разных версий базы данных и обеспечения непрерывной интеграции (CI/CD).

Основные функции Liquibase включают:

 * Версионирование схемы базы данных: Позволяет отслеживать изменения в схеме базы данных с помощью так называемых "changelog-файлов". Эти файлы могут быть написаны в формате XML, YAML, JSON или SQL.  

 * Автоматическое применение изменений: Liquibase может автоматически применять изменения к базе данных, которые описаны в changelog-файлах. Это облегчает процесс развертывания изменений и уменьшает риск ошибок.  

 * Поддержка разных баз данных: Liquibase поддерживает множество популярных СУБД, таких как MySQL, PostgreSQL, Oracle, SQL Server и другие.  

 * Роллбек изменений: Liquibase позволяет откатывать изменения, если это необходимо. Это полезно для отмены некорректных изменений и восстановления предыдущего состояния базы данных.  

 * Сравнение и синхронизация баз данных: Liquibase может сравнивать схемы баз данных и генерировать скрипты для синхронизации различий. 

 * Интеграция с CI/CD: Liquibase можно интегрировать с системами непрерывной интеграции и развертывания, такими как Jenkins, GitHub Actions и другими.  

# Установка liquibase на Linux/Unix
## загрузка установочных файлов
Скачать с [официального сайта.](https://github.com/liquibase/liquibase/releases)

Пример с крайней версией на 17.05.2024
```bash
wget https://github.com/liquibase/liquibase/releases/download/v4.27.0/liquibase-4.27.0.tar.gz
```
```bash
sudo mkdir -p /usr/local/bin/liquibase-4.27.0
```
```bash
sudo tar -xzvf liquibase-4.27.0.tar.gz -C /usr/local/bin/liquibase-4.27.0
```
```bash
rm liquibase-4.27.0.tar.gz
```
```bash
export PATH=$PATH:/usr/local/bin/liquibase-4.27.0
```
или
```bash
echo 'export PATH=$PATH:/usr/local/bin/liquibase-4.27.0' >> ~/.bashrc
```

```bash
liquibase --version
```
## установка с помощью Debian / Ubuntu
```bash
sudo mkdir -p /usr/share/keyrings
```
```bash
wget -O- https://repo.liquibase.com/liquibase.asc | gpg --dearmor > liquibase-keyring.gpg && \
cat liquibase-keyring.gpg | sudo tee /usr/share/keyrings/liquibase-keyring.gpg > /dev/null && \
echo 'deb [arch=amd64 signed-by=/usr/share/keyrings/liquibase-keyring.gpg] https://repo.liquibase.com stable main' | sudo tee /etc/apt/sources.list.d/liquibase.list
```
```bash
sudo apt-get update
```
```bash
sudo apt-get install liquibase
```
Для проверки:
```bash
liquibase --version
```

# Пример использования liquibase с Postgresql
Предворительно установлен и настроен Postgresql.  
Примерная структура проекта:
```
project/  
├── sources/  
│   └─ db/  
│      ├── changelog/  
|      |      ├── v1/ 
|      |      |    ├── v1-changelog.xml
|      |      |    ├── changeset-create-cars-table.xml
|      |      |    ├── changeset-create-price-table.xml
|      |      |    ├── create-cars-table.sql
|      |      |    ├── create-price-table.sql
|      |      |    ├── drop-cars-table.sql
|      |      |    └── drop-price-table.sql
|      |      ├── v2/  
|      |      |    ├── v2-changelog.xml
|      |      |    ├── changeset-add-cars-color.xml
|      |      |    ├── add-cars-color.sql
|      |      |    └──  drop-cars-color.sql 
|      |      ├── v3/  
|      |      └── main_changelog.xml   
│      └── liquibase.properties  
├── .gitignore  
└── README.md  
```
Best Practices: использовать корневой main_changelog.xml со всеми изменениями.  
  
Настройки для подключения liquibase к базе данных.  
liquibase.properties:
```
url=jdbc:postgresql://localhost:5432/postgres
username=postgres
password=postgres
changeLogFile=sources/db/changelog/main_changelog.xml
```
main_changelog.xml:
```xml
<?xml version="1.0" encoding="UTF-8"?>

<databaseChangeLog
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:pro="http://www.liquibase.org/xml/ns/pro"
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-latest.xsd
        http://www.liquibase.org/xml/ns/pro
        http://www.liquibase.org/xml/ns/pro/liquibase-pro-latest.xsd ">

    # Установка типа драйвера для работы с БД
    <preConditions>
        <dbms type="postgresql"/>
    </preConditions>

    # Включение файла в миграцию
    <include file="v1/v1-changelog.xml" relativeToChangelogFile="true"/>

    # Установка тэга позволяет использовать rollbak по тэгу
    <changeSet id="v1" author="Roman" labels="example-label" context="example-context">
        <tagDatabase tag="v.1.0"/>
    </changeSet>

    <include file="v2/v2-changelog.xml" relativeToChangelogFile="true"/>

    <changeSet id="v2" author="Roman" labels="example-label" context="example-context">
        <tagDatabase tag="v.2.0"/>
    </changeSet>

    <include file="v3/v3-changelog.xml" relativeToChangelogFile="true"/>

    <changeSet id="v3" author="Roman" labels="example-label" context="example-context">
        <tagDatabase tag="v.3.0"/>
    </changeSet>

</databaseChangeLog>
```
v1/v1-changelog.xml:
```xml
<?xml version="1.0" encoding="UTF-8"?>

<databaseChangeLog
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:pro="http://www.liquibase.org/xml/ns/pro"
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-latest.xsd
        http://www.liquibase.org/xml/ns/pro
        http://www.liquibase.org/xml/ns/pro/liquibase-pro-latest.xsd ">

    <include file="changeset-create-cars-table.xml" relativeToChangelogFile="true"/>
    <include file="changeset-create-price-table.xml" relativeToChangelogFile="true"/>

</databaseChangeLog>
```
changeset-create-cars-table.xml:
```xml
<?xml version="1.0" encoding="UTF-8"?>

<databaseChangeLog
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:pro="http://www.liquibase.org/xml/ns/pro"
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-latest.xsd
        http://www.liquibase.org/xml/ns/pro
        http://www.liquibase.org/xml/ns/pro/liquibase-pro-latest.xsd ">

    # Параметры записываются во вспомогательную таблицу liquibase
    <changeSet id="v1" author="Roman" labels="example-label" context="example-context">
        <comment>Создание таблицы cars</comment>
        <sqlFile dbms="postgresql"
                 encoding="utf8"
                 relativeToChangelogFile="true"
                 splitStatements="true"
                 stripComments="true"                 
                 path="create-cars-table.sql"/> # указываем на SQL скрипт
        # Для возможности откатов необходимо так-же указать SQL скрипт
        # (вместо SQL можно использовать другие форматы: XML, YAML, JSON)
        <rollback>
            <sqlFile dbms="postgresql"
                     encoding="utf8"
                     relativeToChangelogFile="true"
                     splitStatements="true"
                     stripComments="true"
                     path="drop-users-table.sql"/>
        </rollback>
    </changeSet>

</databaseChangeLog>
```
create-cars-table.sql:
```sql
create table cars (
    id bigint not null,
    model varchar(50) not null,
    mark varchar(50) not null,
    primary key (id)
);
```
drop-users-table.sql:
```sql
drop table cars;
```
v2/v2-changelog.xml:
```xml
<?xml version="1.0" encoding="UTF-8"?>

<databaseChangeLog
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:pro="http://www.liquibase.org/xml/ns/pro"
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-latest.xsd
        http://www.liquibase.org/xml/ns/pro
        http://www.liquibase.org/xml/ns/pro/liquibase-pro-latest.xsd ">

    <include file="changeset-add-cars-color.xml" relativeToChangelogFile="true"/>

</databaseChangeLog>
```
changeset-add-cars-color.xml:
```xml
<?xml version="1.0" encoding="UTF-8"?>

<databaseChangeLog
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:pro="http://www.liquibase.org/xml/ns/pro"
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-latest.xsd
        http://www.liquibase.org/xml/ns/pro
        http://www.liquibase.org/xml/ns/pro/liquibase-pro-latest.xsd ">

    <changeSet id="v2" author="Roman" labels="example-label" context="example-context">
        <comment>Добавление колонки color</comment>
        <sqlFile dbms="postgresql"
                 encoding="utf8"
                 relativeToChangelogFile="true"
                 splitStatements="true"
                 stripComments="true"
                 path="add-cars-color.sql"/>
        <rollback>
            <sqlFile dbms="postgresql"
                     encoding="utf8"
                     relativeToChangelogFile="true"
                     splitStatements="true"
                     stripComments="true"
                     path="drop-cars-color.sql"/>
        </rollback>
    </changeSet>

</databaseChangeLog>
```
add-cars-color.sql:
```sql
alter table cars
add column color varchar(50);
```
drop-cars-color.sql:
```sql
alter table cars
drop column color;
```
Аналогично заполнена V3.  
  
Находять в директории project, выполните код в терминале:
```bash
liquibase --defaultsFile=./sources/db/liquibase.properties update
```
Для отката до тэга команда:
```bash
liquibase --defaultsFile=./sources/db/liquibase.properties rollback --tag=v.1.0
```

# Пример команды для запуска liquibase в контейнере.

```bash
docker run --rm --network=host -v {LOCAL_PATH}/db:/liquibase/db liquibase/liquibase:latest --defaultsFile=/liquibase/db/liquibase.properties update
```
* флаг --rm удаляет контейнер после выполнения
* флаг --network=host позволяет использовать локальные порты
* флаг -v монтирует папку в контейнер, двоеточие разделяет локальную папку и папку в контейнере
* LOCAL_PATH необходимо заменить
* liquibase/liquibase:latest - образ контейнера
* флаг --defaultsFile указывает уже в контейнере путь к настройкам liquibase
* update - команда liquibase

# Пример docker_compose для запуска postgres и liquibase
docker_compose.yaml
```yaml
version: '3.8'
services:
  db:
    image: postgres:latest
    container_name: postgres_db
    environment:
      POSTGRES_DB: ${POSTGRES_DB} # создание базы данных
      POSTGRES_PASSWORD: ${POSTGRES_DB_PASSWORD}
    ports:
      - ${POSTGRES_DB_PORT}:5432
    # network_mode: 'host'  # проблемы с подключением с локальной машины к контейнеру
    volumes:
      - .postgres_data:/var/lib/postgresql/data
    env_file:
      - .env
    restart: always

  liquibase:
    image: liquibase/liquibase:latest
    container_name: liquibase
    # network_mode: 'host'
    depends_on:
      - db
    command: bash -c 'while !</dev/tcp/localhost/5432; do sleep 1; done; liquibase --defaultsFile=/liquibase/db/liquibase.properties update'
    volumes:
      - ./db:/liquibase/db
```
Команда:
```bash
docker-compose up
```
Запускается из директории с файлом docker_compose.yaml.  

* В файле docker_compose.yaml прописываются два сервиса postgres и liquibase  
* Баш команда liquibase ждет готовности postgres, после чего выполняется миграция   
* После выполнения баш команды liquibase останавливается, postgres работает  
* ports проброс портов в контейнер  
* network_mode: 'host' позволяет использовать локальные порты  
* volumes монтирует папки в контейнер  
* env_file используется для хранения глобальных переменных которые обычно необходимо скрыть  
* restart позволяет повторно запускать контейнер в случае ошибок  

Для выполеннися отката по тэгу можно ввести команду:
```bash
docker run --rm --network=host -v {LOCAL_PATH}db:/liquibase/db liquibase/liquibase:latest --defaultsFile=/liquibase/db/liquibase.properties rollback --tag=v.1.0
```
