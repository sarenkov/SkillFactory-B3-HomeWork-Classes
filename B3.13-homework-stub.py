class HTML:
    def __init__(self, output=None):
        self.output = output
        self.children = []

    def __str__(self):
        content = '<HTML>\n'
        if self.children:
            for child in self.children:
                content +=str(child) + '\n'
        return content

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        content = str(self) + '</HTML>'
        if self.output:
            with open(self.output, 'w') as file:
                file.write(content)
        else:
            print(content)

class TopLevelTag():
    def __init__(self, tag, text = None):
        self.tag = tag
        self.taxt = text
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self

    def __str__(self):
        content = f'<{self.tag}>\n'
        if self.children:
            for child in self.children:
                content += str(child) + '\n'
        content += f'</{self.tag}>'
        return content

class Tag():
    def __init__(self, tag: str, text: str = None, klass=None, is_single: bool = False, **kwargs):
        self.tag = tag
        self.is_single = is_single
        self.text = ''
        self.kwargs = kwargs
        self.klass = klass
        self.children = []

    def __str__(self):
        content = f'<{self.tag}'
        attrs = {}

        if self.klass:
            attrs['class'] = ' '.join(self.klass)

        if self.kwargs:
            for key, value in self.kwargs.items():
                if '_' in key:
                    key = key.replace('_', '-')
                attrs[key] = value

        if attrs:
            for key, value in attrs.items():
                content += f' {key}="{value}" '

        content += '>'

        if self.children:
            for child in self.children:
                content += '\n' + str(child)

        if self.is_single:
            return content
        return f'{content}{self.text}</{self.tag}>'

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self


if __name__ == "__main__":
    with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png",  data_image="responsive") as img:
                    div += img

                body += div

            doc += body