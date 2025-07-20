import inspect
from typing import Any, Dict, List, get_type_hints, get_origin, get_args
from collections.abc import Callable
from typeguard import check_type, TypeCheckError

def _check_argument_type(value: Any, expected_type: type) -> bool:
    """使用typeguard检查类型"""
    try:
        check_type(value, expected_type)
        return True
    except TypeCheckError:
        return False

def get_function_signature(func: Callable) -> Dict:
    """
    获取函数的完整签名信息（包含类型注释）
    Get the complete signature information of the function (including type annotations)
    
    返回一个包含以下信息的字典:
    Returns a dictionary containing the following information:
    - name: 函数名 name of the function
    - return_annotation: 返回类型注释 return type annotation
    - parameters: 参数列表 list of parameters
        - name: 参数名 name of the parameter
        - kind: 参数类型 type of the parameter
        - default: 默认值 default value
        - required: 是否是必须参数 whether it is a required parameter
        - annotation: 类型注释 (如果没有则为 typing.Any) type annotation (typing.Any if not specified)
    """
    signature = inspect.signature(func)
    type_hints = get_type_hints(func)
    
    parameters = []
    
    for name, param in signature.parameters.items():
        # 获取类型注释，如果没有则使用 Any
        annotation = type_hints.get(name, Any)
        
        param_info = {
            'name': name,
            'kind': param.kind,
            'default': param.default,
            'required': param.default is inspect.Parameter.empty,
            'annotation': annotation
        }
        parameters.append(param_info)
    
    return {
        'name': func.__name__,
        'return_annotation': type_hints.get('return', Any),
        'parameters': parameters
    }

class OverloadFunction:
    """
    重载函数装饰器
    Overload function decorator
    使用方法:
    Usage:
    ```
    @OverloadFunction
    def func(a: int, b: str) -> None:
        pass
    @func.overload
    def func(a: str, b: int) -> None:
        pass
    ```
    效果:
    Effect:
    ```
    func(1, '2')  # 调用第一个函数
    func('1', 2)  # 调用第二个函数
    func(1, 2)    # 抛出 TypeError
    func('1', '2') # 抛出 TypeError
    ```
    注意:
    Note:
    - 请勿使用装饰器OverloadFunction装饰包含参数*args或**kwargs的函数
    - Please do not use the decorator OverloadFunction to decorate functions containing parameters *args or **kwargs
    - 对函数进行类型注释以方便进行类型匹配
    - Type annotations for functions are recommended for type matching
    """
    def __init__(self, func: Callable):
        # 检查是否包含 *args 或 **kwargs 参数
        sig = inspect.signature(func)
        for param in sig.parameters.values():
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                raise ValueError("OverloadFunction cannot decorate functions with *args or **kwargs parameters")
        
        self.func_list: List[Callable] = [func]
        self.signatures: List[Dict] = [get_function_signature(func)]
        
    def __call__(self, *args, **kwargs):
        # 查找匹配的函数
        matched_funcs = []
        
        for func, signature in zip(self.func_list, self.signatures):
            try:
                # 尝试绑定参数
                bound_args = inspect.signature(func).bind(*args, **kwargs)
                bound_args.apply_defaults()
                
                # 使用 typeguard 检查类型
                type_matched = True
                for param in signature['parameters']:
                    if param['name'] in bound_args.arguments:
                        arg_value = bound_args.arguments[param['name']]
                        expected_type = param['annotation']
                        
                        # 如果类型不是 Any 则进行检查
                        if expected_type is not Any:                            
                            if not _check_argument_type(arg_value, expected_type):
                                type_matched = False
                                break                
                if type_matched:
                    matched_funcs.append(func)
            except TypeError:
                continue
        
        if len(matched_funcs) == 0:
            raise TypeError(f"No matching function found for args: {args}, kwargs: {kwargs}")
        elif len(matched_funcs) > 1:
            raise TypeError(f"Multiple functions matched for args: {args}, kwargs: {kwargs}")
        else:
            return matched_funcs[0](*args, **kwargs)
    
    def overload(self, func: Callable):
        # 检查是否包含 *args 或 **kwargs 参数
        sig = inspect.signature(func)
        for param in sig.parameters.values():
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                raise ValueError("OverloadFunction cannot decorate functions with *args or **kwargs parameters")
        
        self.func_list.append(func)
        self.signatures.append(get_function_signature(func))
        return self

    @staticmethod
    def overload_decorator(func: Callable):
        # 用于作为装饰器使用
        return OverloadFunction(func)
