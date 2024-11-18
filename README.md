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
1. Установить библиотеку Lark
```
pip install lark
```
2. Загрузить репозиторий на компьютер
```
git clone https://github.com/n1kpavlov/MIREA_config_converter
```
3. Прейдите в директорию репозитория
```
cd MIREA_config_converter
```
4. Запустить config_converter.py с указанием имени xml файла
```
py config_converter.py <имя_файла.xml>
```
5. Ввод конфигурации в командную строку. Для завершения ввода использовать ctrl + Z
# Пример работы программы
### Граф зависимостей пакета Newtonsoft.Json с глубиной анализа 1
![output](https://github.com/user-attachments/assets/850ad660-7dff-4d92-8c07-d9e0f679bf24)
### Граф зависимостей пакета Newtonsoft.Json с глубиной анализа 2
![output](https://github.com/user-attachments/assets/95259622-ce49-4ac6-a56a-eefd2742abe4)
### Граф зависимостей пакета Newtonsoft.Json с неограниченной глубиной анализа
![output](https://github.com/user-attachments/assets/c7949dff-abc3-4d79-ab11-d1b0fb17034f)
# Результаты тестирования
### Тест функции получения зависимостей с глубиной анализа меньше 1
```
def test_empty_dependencies(self):
    package_path = "newtonsoft.json.13.0.3.nupkg"
    depth = 0
    dependencies = get_dependencies(package_path, depth)
    self.assertEqual(dependencies, {})
```
### Тест функции получения зависимостей пакета newtonsoft.json.13.0.3.nupkg с глубиной анализа 1
```
def test_dependencies(self):
    package_path = "newtonsoft.json.13.0.3.nupkg"
    depth = 1
    dependencies = get_dependencies(package_path, depth)
    self.assertEqual(dependencies, {'Newtonsoft.Json:13.0.3': ['Microsoft.CSharp:4.3.0',
                            'NETStandard.Library:1.6.1',
                            'System.ComponentModel.TypeConverter:4.3.0',
                            'System.Runtime.Serialization.Primitives:4.3.0',
                            'System.Runtime.Serialization.Formatters:4.3.0',
                            'System.Xml.XmlDocument:4.3.0']})
```
### Тест функции генерации кода Mermaid с пустым списком зависимостей
```
def test_empty_dependencies(self):
    dependencies = {}
    mermaid_code = generate_mermaid_graph(dependencies)
    self.assertEqual(mermaid_code, "graph TD;\n")
```
### Тест функции генерации кода Mermaid с одной зависимостью
```
def test_single_dependency(self):
    dependencies = {"TestPackage:1.0.0": ["DependencyPackage:1.0.0"]}
    mermaid_code = generate_mermaid_graph(dependencies)
    self.assertEqual(mermaid_code, "graph TD;\nTestPackage:1.0.0 --> DependencyPackage:1.0.0\n")
```
### Тест функции генерации кода Mermaid с несколькими зависимостями
```
def test_multiple_dependencies(self):
    dependencies = {"TestPackage:1.0.0": ["DependencyPackage:1.0.0", "AnotherDependency:1.0.0"]}
    mermaid_code = generate_mermaid_graph(dependencies)
    self.assertEqual(mermaid_code, "graph TD;\nTestPackage:1.0.0 --> DependencyPackage:1.0.0\nTestPackage:1.0.0 --> AnotherDependency:1.0.0\n")
```
### Тест функции генерации кода Mermaid с цепной зависимостью
```
def test_nested_dependencies(self):
    dependencies = {"TestPackage:1.0.0": ["DependencyPackage:1.0.0"], "DependencyPackage:1.0.0": ["NestedDependency:1.0.0"]}
    mermaid_code = generate_mermaid_graph(dependencies)
    self.assertEqual(mermaid_code, "graph TD;\nTestPackage:1.0.0 --> DependencyPackage:1.0.0\nDependencyPackage:1.0.0 --> NestedDependency:1.0.0\n")
```
### Тест функции генерации кода Mermaid с кольцевой зависимостью
```
def test_circular_dependencies(self):
    dependencies = {"TestPackage:1.0.0": ["DependencyPackage:1.0.0"], "DependencyPackage:1.0.0": ["CircularDependency:1.0.0"], "CircularDependency:1.0.0": ["TestPackage:1.0.0"]}
    mermaid_code = generate_mermaid_graph(dependencies)
    self.assertEqual(mermaid_code, "graph TD;\nTestPackage:1.0.0 --> DependencyPackage:1.0.0\nDependencyPackage:1.0.0 --> CircularDependency:1.0.0\nCircularDependency:1.0.0 --> TestPackage:1.0.0\n")
```
### Тестирование вызова функции с несуществующими файлами
```
def test_visualize_dependencies_call(self):
    mermaid_path = "mermaid"
    package_path = "test_package.nupkg"
    output_file = "test.png"
    depth = 1
    with self.assertRaises(FileNotFoundError):
        visualize_dependencies(mermaid_path, package_path, output_file, depth)
```
![image](https://github.com/user-attachments/assets/08078101-ca57-4820-b2f3-29bd2570d11c)
