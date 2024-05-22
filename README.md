# Daily Backup Script (Only for Windows 10/11)

This is a Python script to help you automatically create backups of certain directories.  
I use this to save cloud notes and a directory for work.

## Features

- Creates daily backups of specified folders, compressing them into ZIP.
- Displays a Windows notification after a successful backup.
- Configurable via JSON file.
- Supports excluding certain files and folders from backup.

## Installation

1. **Clone the repository or download the script**:
    ```bash
    git clone <repository_url>
    ```
    Or download the `backup.py` script directly.

2. **Edit the configuration file**:
    - Open `config.json` in a text editor.
    - Modify the configuration to match your requirements:
      ```json
      {
          "folders_to_backup": [
              {
                  "path": "C:/Users/valer/Documents/AghanimoffVault",
                  "exclude": [
                      "C:/Users/valer/Documents/AghanimoffVault/SomeFolder",
                      "C:/Users/valer/Documents/AghanimoffVault/SomeFile.txt"
                  ],
                  "backup_path": false
              }
          ],
          "backup_time": "01:00",
          "log_dir": ".logs",
          "log_max_bytes": 1048576,
          "log_backup_count": 5,
          "max_backup_size_mb": 500,
          "enable_notifications": true
      }
      ```

3. **Save the configuration file**.

## Usage

1. **Run the script manually**:
    - Open a command prompt and navigate to the directory containing the script:
      ```bash
      cd path/to/script
      ```
    - Execute the script:
      ```bash
      python backup.py
      ```

2. **Set up the script to run at system startup**:
    - Create a shortcut for `backup.py`.
    - Move the shortcut to the startup folder. To open the startup folder, press `Win + R`, type `shell:startup`, and press `Enter`.
    - Place the shortcut in the opened folder.

## How It Works

1. **Scheduling**:
    - The script uses the `schedule` library to run the `job` function every day at the time specified in `config.json`.
    - The `job` function creates backups and cleans up old backups.

2. **Backup Creation**:
    - The `backup_folder` function creates a ZIP file for each specified folder if a backup for the current day doesn't already exist.
    - It calculates the size of the backup and displays a Windows notification with the backup details.
    - It logs the actions to a session-specific log file.

3. **Cleanup**:
    - The `cleanup_old_backups` function deletes backups older than a week, except for backups created at the start of each month and year.
    - It logs the cleanup actions to the log file.

4. **Size Limit Enforcement**:
    - The script enforces a size limit on the backup directory, deleting the oldest backups if the total size exceeds the specified limit.
    - It logs the size enforcement actions to the log file.

5. **Run on Startup**:
    - The script ensures a backup is created if it was not run at the scheduled time by calling `job()` on startup.

### Configuration File (`config.json`)

The `config.json` file allows you to specify various settings for the backup script. Here is an example configuration:

```json
{
    "folders_to_backup": [
        {
            "path": "C:/Users/valer/Documents/AghanimoffVault",
            "exclude": [
                "C:/Users/valer/Documents/AghanimoffVault/SomeFolder",
                "C:/Users/valer/Documents/AghanimoffVault/SomeFile.txt"
            ],
            "backup_path": false
        }
    ],
    "backup_time": "01:00",
    "log_dir": ".logs",
    "log_max_bytes": 1048576,
    "log_backup_count": 5,
    "max_backup_size_mb": 500,
    "enable_notifications": true
}
```

- **folders_to_backup**: List of folders to back up. Each folder can have its own set of exclusions and a custom backup path.
- **backup_time**: Time at which the backup should run daily.
- **log_dir**: Directory where log files will be stored.
- **log_max_bytes**: Maximum size of a log file before it is rotated.
- **log_backup_count**: Number of rotated log files to keep.
- **max_backup_size_mb**: Maximum size of the backup directory in megabytes.
- **enable_notifications**: Boolean to enable or disable Windows notifications.

# Скрипт Ежедневного Резервного Копирования (Только под Windows 10/11)

Это Python скрипт для помощи в автоматическом создании бекапов определенных директорий.  
Я использую это для сохранения облачных заметок и директории для работы. 

## Возможности

- Создает ежедневные резервные копии указанных папок, сжимая в ZIP.
- Отображает уведомление Windows после успешного создания резервной копии.
- Настраивается через JSON-файл.
- Поддерживает исключение определенных файлов и папок из резервной копии.

## Установка

1. **Клонируйте репозиторий или скачайте скрипт**:
    ```bash
    git clone <repository_url>
    ```
    Или скачайте скрипт `daily_backup.py` напрямую.

2. **Отредактируйте файл конфигурации**:
    - Откройте `config.json` в текстовом редакторе.
    - Измените конфигурацию в соответствии с вашими требованиями:
      ```json
      {
          "folders_to_backup": [
              {
                  "path": "C:/Users/valer/Documents/AghanimoffVault",
                  "exclude": [
                      "C:/Users/valer/Documents/AghanimoffVault/SomeFolder",
                      "C:/Users/valer/Documents/AghanimoffVault/SomeFile.txt"
                  ],
                  "backup_path": false
              }
          ],
          "backup_time": "01:00",
          "log_dir": ".logs",
          "log_max_bytes": 1048576,
          "log_backup_count": 5,
          "max_backup_size_mb": 500,
          "enable_notifications": true
      }
      ```

3. **Сохраните файл конфигурации**.

## Использование

1. **Запустите скрипт вручную**:
    - Откройте командную строку и перейдите в директорию, содержащую скрипт:
      ```bash
      cd path/to/script
      ```
    - Выполните скрипт:
      ```bash
      python daily_backup.py
      ```

2. **Настройте автозапуск скрипта при старте системы**:
    - Создайте ярлык для `daily_backup.py`.
    - Переместите ярлык в папку автозагрузки. Чтобы открыть папку автозагрузки, нажмите `Win + R`, введите `shell:startup` и нажмите `Enter`.
    - Поместите ярлык в открывшуюся папку.

## Как Это Работает

1. **Планирование**:
    - Скрипт использует библиотеку `schedule` для запуска функции `job` каждый день в указанное в `config.json` время.
    - Функция `job` создает резервные копии и очищает старые резервные копии.

2. **Создание Резервных Копий**:
    - Функция `backup_folder` создает ZIP-файл для каждой указанной папки, если резервная копия на текущий день еще не существует.
    - Она вычисляет размер резервной копии и отображает уведомление Windows с деталями резервной копии.
    - Логирует действия в лог-файл, специфичный для сессии.

3. **Очистка**:
    - Функция `cleanup_old_backups` удаляет резервные копии старше недели, за исключением резервных копий, созданных в начале каждого месяца и года.
    - Логирует действия очистки в лог-файл.

4. **Ограничение Размера**:
    - Скрипт ограничивает размер директории резервных копий, удаляя старейшие резервные копии, если общий размер превышает указанный лимит.
    - Логирует действия по удалению резервных копий из-за превышения лимита размера в лог-файл.

5. **Запуск При Старте**:
    - Скрипт гарантирует создание резервной копии, если он не был запущен в запланированное время, вызывая `job()` при запуске.

### Файл Конфигурации (`config.json`)

Файл `config.json` позволяет вам указать различные настройки для скрипта резервного копирования. Пример конфигурации:

```json
{
    "folders_to_backup": [
        {
            "path": "C:/Users/valer/Documents/AghanimoffVault",
            "exclude": [
                "C:/Users/valer/Documents/AghanimoffVault/SomeFolder",
                "C:/Users/valer/Documents/AghanimoffVault/SomeFile.txt"
            ],
            "backup_path": false
        }
    ],
    "backup_time": "01:00",
    "log_dir": ".logs",
    "log_max_bytes": 1048576,
    "log_backup_count": 5,
    "max_backup_size_mb": 500,
    "enable_notifications": true
}
```

- **folders_to_backup**: Список папок для резервного копирования. Каждая папка может иметь свои собственные исключения и указанный путь для хранения бэкапов.
- **backup_time**: Время, в которое должно выполняться резервное копирование ежедневно.
- **log_dir**: Директория, в которой будут храниться лог-файлы.
- **log_max_bytes**: Максимальный размер лог-файла перед его ротацией.
- **log_backup_count**: Количество ротационных лог-файлов для хранения.
- **max_backup_size_mb**: Максимальный размер директории резервных копий в мегабайтах.
- **enable_notifications**: Логическое значение для включения или отключения уведомлений Windows.
