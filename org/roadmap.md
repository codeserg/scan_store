## Наши классы:

### Создаватель базы данных

в результате должен появиться файл sqlite с нашей структурой

### Формирование пути хранения по шаблону
по строке из базы воссоздать путь \клиент\акт\2024
надо будет убрать всякие нечитаемые и запрещенные символы

### Загрузчик файлов в нашу базу
Создает запись в базе
Копирует файл в хранилище
Желательно массовая загрузка, а не по одному. Хотя, каждому документу надо проставить категории и типы.
Какие будут категории документов? Сформировать словари

### Импорт клиентов и договоров из сторонней базы
первоначальная загрузка данных

### Окна на PyQT

Какие окна будут?
В каком порядке появляться?
Дизайн окон - какие элементы на них будут?

- Окно навигации с фильтрами
- Окно добавления документа

### Выгружатор. Наверно тоже отдельное окно
- Укажите нашу фирму
- Укажите клиента
- Укажите интервал дат
- Получите ZIP файл

### То что продумать: 
- Как хранить многофайловый документ? Например Договор отсканирован в виде 10 файлов

### Отдельный сайт проекта с описанием фишек.

### Определиться что есть MVP для нас (минимальный проект)
Сейчас я вижу так:
- Окно со списком файлов (показ из базы)
- Функция загрузки файла в хранилище (пока в 1 каталог)

