from curses.ascii import isalpha
from nodes.textnode import TextNode, TextType

class MalformattedMarkdownError(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Scanner:
    def __init__(self, source: str, delimiter: str, text_type: TextType) -> None:
        self.source = source
        self.delimiter = delimiter
        self.text_type = text_type

        self.start = 0
        self.current = 0
        self.tokens: list[TextNode] = []

    def scan(self):
        while not self.__is_at_end():
            self.start = self.current
            c = self.__advance()

            match (c, self.text_type):
                case ("`", TextType.CODE):
                    code_text = self.__handle_single_delimiter()
                    node = TextNode(code_text, TextType.CODE)

                    self.tokens.append(node)
                case ("_", TextType.ITALIC):
                    italic_text = self.__handle_single_delimiter()
                    node = TextNode(italic_text, TextType.ITALIC)

                    self.tokens.append(node)
                case ("*", TextType.BOLD): 
                    self.__handle_multiple_delimiter() # TODO: Handle with **content**
                case _:
                    text = self.__handle_words()
                    node = TextNode(text, TextType.TEXT)

                    self.tokens.append(node)

        return self.tokens

    def __handle_words(self):
        while self.__peek() != self.delimiter and not self.__is_at_end():
           self.__advance()

        return self.source[self.start : self.current]

    def __handle_single_delimiter(self):
        while self.__peek() != self.delimiter and not self.__is_at_end():
           self.__advance()

        if self.__is_at_end():
            raise MalformattedMarkdownError(f"Malformatted block for delimiter '{self.delimiter}' -> {self.source}")
        
        self.__advance()
        value = self.source[self.start + 1 : self.current - 1]

        return value

    def __handle_multiple_delimiter(self):
        print("I'm a bold block")

    def __is_at_end(self):
        return self.current >= len(self.source)
    
    def __advance(self):        
        c = self.source[self.current]
        self.current += 1

        return c

    def __peek(self):
        if self.__is_at_end(): 
            return chr(0)
        return self.source[self.current]



def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        scanner = Scanner(node.text, delimiter, text_type)
        scanned_nodes = scanner.scan()
        
        print("\n-------\n")
        print(node.text)
        print(scanned_nodes)
        print("\n-------\n")

        new_nodes.extend(scanned_nodes)

    return new_nodes                

