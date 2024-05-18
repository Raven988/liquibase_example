import subprocess


def run_liquibase_migration() -> None:
    """Запуск миграции."""
    try:
        command = [
            'liquibase',
            '--defaultsFile=sources/db/liquibase.properties',
            'update',
        ]
        subprocess.run(command, check=True)
        print('Миграции успешно применены')
    except subprocess.CalledProcessError as error:
        print('Ошибка при выполнении миграций с помощью Liquibase:', error)


def rollback_db() -> None:
    """Откат по тэгу."""
    try:
        command = [
            'liquibase',
            '--defaultsFile=sources/db/liquibase.properties',
            'rollback',
            '--tag=v.1.0',
        ]
        subprocess.run(command, check=True)
        print('Миграции успешно применены')
    except subprocess.CalledProcessError as error:
        print('Ошибка при выполнении миграций с помощью Liquibase:', error)

def main() -> None:
    """Main."""
    run_liquibase_migration()
    # rollback_db()


if __name__ == '__main__':
    main()
