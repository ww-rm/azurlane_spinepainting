import json
from argparse import ArgumentParser
from pathlib import Path


class CustomJSONEncoder(json.JSONEncoder):
    """pages 键不缩进"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def iterencode(self, o, _one_shot=False):
        # 从顶层开始递归编码，初始缩进为0
        return self._iterencode(o, 0)

    def _iterencode(self, o, current_indent):
        # 如果设置了缩进，则使用相应数目的空格，否则缩进为0
        indent = self.indent if self.indent is not None else 0
        if isinstance(o, dict):
            yield '{'
            first = True
            for key, value in o.items():
                if first:
                    first = False
                else:
                    yield ','
                if self.indent is not None:
                    yield '\n' + ' ' * (current_indent + indent)
                # 编码键（确保字符串格式符合json标准）
                key_str = json.dumps(key, ensure_ascii=self.ensure_ascii)
                yield key_str + ':'
                # 如果键为'pages'则紧凑编码
                if key == 'pages':
                    yield json.dumps(value, ensure_ascii=self.ensure_ascii)
                else:
                    yield from self._iterencode(value, current_indent + indent)
            if self.indent is not None:
                yield '\n' + ' ' * current_indent
            yield '}'
        elif isinstance(o, list):
            yield '['
            first = True
            for item in o:
                if first:
                    first = False
                else:
                    yield ','
                if self.indent is not None:
                    yield '\n' + ' ' * (current_indent + indent)
                yield from self._iterencode(item, current_indent + indent)
            if self.indent is not None:
                yield '\n' + ' ' * current_indent
            yield ']'
        else:
            # 非容器类型直接用json.dumps处理（数字、字符串、布尔、None等）
            yield json.dumps(o, ensure_ascii=self.ensure_ascii)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("path")

    args = parser.parse_args()

    path = Path(args.path)

    data = json.loads(path.read_bytes())
    with path.open("w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"), indent=1, cls=CustomJSONEncoder)
