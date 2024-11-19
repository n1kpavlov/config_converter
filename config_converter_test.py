import unittest
from config_converter import parse_config, pretty_print_xml

class TestParseConfig(unittest.TestCase):
    def test_simple_config(self):
        input_text = ('config {\n'
                      '\tsmth = 13\n'
                      '}\n')
        expected_output = '<config><smth type="int">13</smth></config>'
        self.assertEqual(parse_config(input_text), expected_output)

    def test_dict(self):
        input_text = ('config {\n'
                      '\tnames = struct {\n'
                      '\t\tnikita = 1,\n'
                      '\t\tartem = 2\n'
                      '\t}\n'
                      '}\n')
        expected_output = '<config><names type="dict"><nikita type="int">1</nikita><artem type="int">2</artem></names></config>'
        self.assertEqual(parse_config(input_text), expected_output)

    def test_constant(self):
        input_text = ('def x = 5\n'
                      'config {\n'
                      '\tsmth = [x]\n'
                      '}\n')
        expected_output = '<config><smth type="int">5</smth></config>'
        self.assertEqual(parse_config(input_text), expected_output)

    def test_comment(self):
        input_text = ('*> comment\n'
                      'config {\n'
                      '\tsmth = 10\n'
                      '}\n')
        expected_output = '<config><smth type="int">10</smth></config>'
        self.assertEqual(parse_config(input_text), expected_output)

    def test_syntax_error(self):
        input_text = ('def x = 5\n'
                      'config {\n'
                      '\tsmth = x\n'
                      '}\n')
        result = parse_config(input_text)
        assert "Unexpected Characters" in result

    def test_undefined_constant_error(self):
        input_text = ('config {\n'
                      '\tsmth = [undefined_constant]\n'
                      '}\n')
        result = parse_config(input_text)
        assert "В конфигурации использована неизвестная константа по имени undefined_constant" in result

    def test_duplicate_constant_error(self):
        input_text = ('def x = 5\n'
                      'def x = 10\n'
                      'config {\n'
                      '\tsmth = [x]\n'
                      '}\n')
        result = parse_config(input_text)
        assert "Константа x уже объявлена" in result

class TestPrettyPrintXML(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()
