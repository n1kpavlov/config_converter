# Общее описание
### Задание
Разработать инструмент командной строки для визуализации графа зависимостей, включая транзитивные зависимости. Сторонние средства для получения зависимостей использовать нельзя.
Зависимости определяются по имени пакета **платформы .NET (nupkg)**. Для описания графа зависимостей используется представление **Mermaid**. Визуализатор должен выводить результат в виде сообщения об успешном выполнении и сохранять граф в файле формата **png**.
### Ключи командной строки
- Путь к программе для визуализации графов;
- Путь к анализируемому пакету;
- Путь к файлу с изображением графа зависимостей;
- Максимальная глубина анализа зависимостей.
# Реализованные функции
### get_dependencies
Используется для извлечения зависимых пакетов. В пакете используется файл с расширением .nuspec, где содержатся метаданные о пакете (в том числе и зависимые пакеты). Из метаданных извлекаются ID, версия текущего пакета и зависимые напрямую пакеты. Полученные данные добавляются в определенный программой список зависимостей. Проверяется, выполнялась ли функция для текущего пакета. Если не выполнялась, то устанавливаются определенные ранее зависимые пакеты, и функция вызывается рекурсивно для этих пакетов.
### generate_mermaid_graph
Используется для генерации кода mermaid из списка зависимостей. Код возвращается в виде строки, в которой по шаблону перезаписана каждая из зависимостей.
### visualize_dependencies
Функция взаимодействует с функцией получения зависимостей и вызыввает функцию генерации кода mermaid. Полученный код используется для визуализации графа зависимостей в формате .png с помощью Mermaid.js.
### main
Выполняется парсинг аргументов командной строки (Путь к программе для визуализации графов; Путь к анализируемому пакету; Путь к файлу с изображением графа зависимостей; Максимальная глубина анализа зависимостей.) и вызывается функция визуализации графа зависимостей.
# Сборка и запуск проекта
1. Установить пакет с расширением nupkg с [официального сайта](https://www.nuget.org/packages). В примере используется пакет [Newtonsoft.Json](https://www.nuget.org/packages/Newtonsoft.Json/#readme-body-tab)
2. Установить программу для визуализации графов [Mermaid](https://mermaid.js.org/)
3. Загрузить репозиторий на компьютер
```
git clone https://github.com/n1kpavlov/MIREA_dependency_visualizer
```
4. Прейдите в директорию репозитория
```
cd MIREA_dependency_visualizer
```
5. Запустить dependency_visualizer.py с указанием всех необходимых ключей
```
python dependency_visualizer.py <путь_к_mermaid.js> <путь_к_анализируемому_пакету.nupkg> <путь_к_файлу_вывода.png> <максимальная_глубина>
```
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
