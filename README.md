# OverloadFunction Decorator

## 概述 / Overview

`OverloadFunction` 是一个 Python 装饰器，用于实现函数重载功能。它允许你为同一个函数名定义多个实现，根据传入参数的类型自动选择正确的函数版本。

`OverloadFunction` is a Python decorator that implements function overloading. It allows you to define multiple implementations for the same function name, automatically selecting the correct version based on the types of arguments passed.

## 功能特性 / Features

- 基于参数类型的函数重载 / Function overloading based on argument types
- 类型检查确保调用正确的函数版本 / Type checking ensures the correct function version is called
- 清晰的错误提示 / Clear error messages
- 支持详细的类型注解 / Supports detailed type annotations

## 安装 / Installation

```bash
pip install overload_function
```

## 使用示例 / Usage Example

```python
from typing import Union
from overload_function import OverloadFunction

@OverloadFunction
def process_data(a: int, b: str) -> None:
    print(f"Processing int {a} and string '{b}'")

@process_data.overload
def process_data(a: str, b: int) -> None:
    print(f"Processing string '{a}' and int {b}")

@process_data.overload
def process_data(a: Union[int, float], b: Union[int, float]) -> None:
    print(f"Processing numbers {a} and {b}")

# 正确调用 / Correct calls
process_data(1, "hello")    # 调用第一个版本 / Calls first version
process_data("hello", 2)   # 调用第二个版本 / Calls second version
process_data(3.14, 42)     # 调用第三个版本 / Calls third version

# 错误调用 / Incorrect calls
process_data("hello", "world")  # 抛出 TypeError / Raises TypeError
process_data([], {})           # 抛出 TypeError / Raises TypeError
```

## 注意事项 / Notes

1. **不支持可变参数** / **No support for variable arguments**:
   - 不能装饰包含 `*args` 或 `**kwargs` 的函数
   - Cannot decorate functions with `*args` or `**kwargs` parameters

2. **类型注解推荐** / **Type annotations recommended**:
   - 为获得最佳效果，请为函数参数添加类型注解
   - For best results, add type annotations to function parameters

3. **性能考虑** / **Performance considerations**:
   - 每次调用都会进行类型检查，可能影响性能
   - Type checking on each call may impact performance

4. **明确性** / **Explicitness**:
   - 当多个函数版本匹配时，会抛出异常
   - Raises an exception when multiple function versions match

## 许可证 / License

MIT License
