import sys
import xml.etree.ElementTree as ET
from lark import Lark, Transformer, exceptions, LarkError

grammar = """
start: (const_decl | comment)* config

comment: "*>" /[a-zA-Z][ _a-zA-Z0-9]*/

config: NAME value

const_decl: "def" NAME "=" value
const_eval: "[" NAME "]"

value:  NUMBER | dict | const_eval

dict: "struct {" [pair (";" pair)*] "}"
pair: NAME "=" value

NAME: /[a-zA-Z][_a-zA-Z0-9]*/

%import common.NUMBER
%import common.WS
%ignore WS
"""

config_parser = Lark(grammar)

class ConfigTransformer(Transformer):
    def __init__(self):
        super().__init__()
        self.constants = {}

def parse_config(input_text):
    try:
        tree = config_parser.parse(input_text)
        transformer = ConfigTransformer()
        xml_output = transformer.transform(tree)
        return xml_output
    except exceptions.UnexpectedCharacters as uc:
        return f"Unexpected Characters:\n{str(uc)}"
    except exceptions.LarkError as le:
        return f"Ошибка при обработке:\n{str(le)}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python config_converter.py <выходной_файл.xml>")
        sys.exit(1)
    output_filename = sys.argv[1]
    input_text = sys.stdin.read()
    xml_str = parse_config(input_text)
    print(xml_str)
