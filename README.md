# Общее описание
### Задание
Разработать инструмент командной строки для учебного конфигурационного языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из 
входного формата в выходной. Синтаксические ошибки выявляются с выдачей сообщений. 

Входной текст на учебном конфигурационном языке принимается из стандартного ввода. Выходной текст на языке xml попадает в файл, путь к которому задан ключом командной строки. 
### Синтаксис учебного конфигурационного языка
Однострочные комментарии:
```
*> Это однострочный комментарий
```
Словари:
```
struct {
    имя = значение,
    имя = значение,
    имя = значение,
    ...
}
```
Имена:
```
[a-zA-Z][_a-zA-Z0-9]*
```
Значения:
```
• Числа
• Словари
```
Объявление констант на этапе трансляции:
```
def имя = значение
```
Вычисление констант на этапе трансляции:
```
[имя]
```
# Реализованный функционал
### grammar
Задается грамматика учебного конфигурационного языка для дальнейшего парсинга конфигурации.
### ConfigTransformer
Класс, в котором указываются правила преобразования каждого элемента из учебного конфигурационного языка. Все, реализованные в классе методы, в совокупности возвращают строку, содержащую конфигурацию на языке xml.
### parse_config
Функция парсит конфигурацию, поступившую на вход, по установленной ранее грамматике. Далее вызываются методы класса ConfigTransformer, благодаря чему поступившая конфигурация преобразуется в строку на языке xml. Помимо этого в функции реализован обработчик синтаксических ошибок.
### pretty_print_xml
Функция использует библиотеку xml.dom.minidom для преобразоваания строки на языке xml в красиво отформатированный файл на языке xml.
### main
Выполняется парсинг аргументов командной строки. Считывается конфигурация на учебном конфигурационном языке из стандартного потока ввода. Вызываются поочередно функции получения строки на языке xml и получения отформатированной строки на языке xml. Отформатированная строка записывается в файл, указанный ключом командной строки.
# Сборка и запуск проекта
1. Загрузить репозиторий на компьютер
```
git clone https://github.com/n1kpavlov/MIREA_config_converter
```
2. Прейдите в директорию репозитория
```
cd MIREA_config_converter
```
3. Запустите скрипт-установщик библиотек script.sh
```
script.sh
```
4. Запустить config_converter.py с указанием имени xml файла
```
py config_converter.py <имя_файла.xml>
```
5. Ввод конфигурации в командную строку. Для завершения ввода использовать ctrl + Z
# Примерs работы программы
### Настройка базы данных
**Входные данные:**
```
*> Configuring the database
def max_conn = 100
def timeout = 30
database {
    database = struct {
        host = 19216801,
        port = 5432,
        max_connections = [max_conn],
        connection_timeout = [timeout]
    }
}
```
**Выходные данные (XML):**
```
<?xml version="1.0" encoding="utf-8"?>
<database>
	<database type="dict">
		<host type="int">19216801</host>
		<port type="int">5432</port>
		<max_connections type="int">100</max_connections>
		<connection_timeout type="int">30</connection_timeout>
	</database>
</database>
```
### Конфигурация веб-приложения
**Входные данные:**
```
*> Web Application Configuration
def max_threads = 8
web_config {
    webserver = struct {
        hostname = 127001,
        port = 8080,
        threads = [max_threads],
        routes = struct {
            home = 1,
            login = 2,
            logout = 3
        }
    }
}
```
**Выходные данные (XML):**
```
<?xml version="1.0" encoding="utf-8"?>
<web_config>
	<webserver type="dict">
		<hostname type="int">127001</hostname>
		<port type="int">8080</port>
		<threads type="int">8</threads>
		<routes type="dict">
			<home type="int">1</home>
			<login type="int">2</login>
			<logout type="int">3</logout>
		</routes>
	</webserver>
</web_config>
```
### Конфигурация системы мониторинга
**Входные данные:**
```
*> Configuration of the monitoring system
def interval = 15
def retention = 365
monitoring_config {
    monitoring = struct {
        interval = [interval],
        retention_days = [retention],
        services = struct {
            first = 1,
            second = 2,
            third = 3,
            fourth = 4
        }
    }
}
```
**Выходные данные (XML):**
```
<?xml version="1.0" encoding="utf-8"?>
<monitoring_config>
	<monitoring type="dict">
		<interval type="int">15</interval>
		<retention_days type="int">365</retention_days>
		<services type="dict">
			<first type="int">1</first>
			<second type="int">2</second>
			<third type="int">3</third>
			<fourth type="int">4</fourth>
		</services>
	</monitoring>
</monitoring_config>
```
# Результаты тестирования
### Тест простой конфигурации
```
def test_simple_config(self):
	input_text = ('config {\n'
                      '\tsmth = 13\n'
                      '}\n')
        expected_output = '<config><smth type="int">13</smth></config>'
        self.assertEqual(parse_config(input_text), expected_output)
```
### Тест словаря
```
def test_dict(self):
	input_text = ('config {\n'
                      '\tnames = struct {\n'
                      '\t\tnikita = 1,\n'
                      '\t\tartem = 2\n'
                      '\t}\n'
                      '}\n')
        expected_output = '<config><names type="dict"><nikita type="int">1</nikita><artem type="int">2</artem></names></config>'
        self.assertEqual(parse_config(input_text), expected_output)
```
### Тест константы
```
def test_constant(self):
        input_text = ('def x = 5\n'
                      'config {\n'
                      '\tsmth = [x]\n'
                      '}\n')
        expected_output = '<config><smth type="int">5</smth></config>'
        self.assertEqual(parse_config(input_text), expected_output)
```
### Тест комментария
```
def test_comment(self):
        input_text = ('*> comment\n'
                      'config {\n'
                      '\tsmth = 10\n'
                      '}\n')
        expected_output = '<config><smth type="int">10</smth></config>'
        self.assertEqual(parse_config(input_text), expected_output)
```
### Тест синтаксической ошибки
```
def test_syntax_error(self):
        input_text = ('def x = 5\n'
                      'config {\n'
                      '\tsmth = x\n'
                      '}\n')
        result = parse_config(input_text)
        assert "Unexpected Characters" in result
```
### Тест использования необъявленной константы
```
def test_undefined_constant_error(self):
        input_text = ('config {\n'
                      '\tsmth = [undefined_constant]\n'
                      '}\n')
        result = parse_config(input_text)
        assert "В конфигурации использована неизвестная константа по имени undefined_constant" in result
```
### Тест повторного объявления константы
```
def test_duplicate_constant_error(self):
        input_text = ('def x = 5\n'
                      'def x = 10\n'
                      'config {\n'
                      '\tsmth = [x]\n'
                      '}\n')
        result = parse_config(input_text)
        assert "Константа x уже объявлена" in result
```
### Тест форматированного вывода
```
def test_output_xml(self):
        input_text = ('*> Test comment\n'
                      'def int = 10\n'
                      'main {\n'
                      '\tcombo = struct {\n'
                      '\t\tnumber = 19216801,\n'
                      '\tmax_connections = [int]\n'
                      '\t}\n'
                      '}\n')
        expected_output = ('<?xml version="1.0" encoding="utf-8"?>\n'
                        '<main>\n'
                        '\t<combo type="dict">\n'
                        '\t\t<number type="int">19216801</number>\n'
                        '\t\t<max_connections type="int">10</max_connections>\n'
                        '\t</combo>\n'
                        '</main>\n')
        self.assertEqual(pretty_print_xml(parse_config(input_text)), expected_output)
```
![image](https://github.com/user-attachments/assets/4f180366-0af7-44be-81a5-15770bd454dc)
