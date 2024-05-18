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

# Пример использования liquibase


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
