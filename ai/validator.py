import ast
from typing import List, Dict, Any


class ReadOnlyValidationError(Exception):
    pass


def validate_read_only(code: str) -> None:
    try:
        tree = ast.parse(code, mode="eval")
    except SyntaxError:
        try:
            tree = ast.parse(code, mode="exec")
        except SyntaxError as e:
            raise ReadOnlyValidationError(f"Invalid Python syntax: {e}")

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "tasks":
                    raise ReadOnlyValidationError(
                        "Cannot assign to 'tasks' variable - read-only operation required"
                    )
                if isinstance(target, ast.Attribute) and isinstance(
                    target.value, ast.Name
                ):
                    if target.value.id == "tasks":
                        raise ReadOnlyValidationError(
                            "Cannot modify 'tasks' object - read-only operation required"
                        )

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if (
                    isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "tasks"
                ):
                    mutation_methods = [
                        "append",
                        "extend",
                        "remove",
                        "pop",
                        "insert",
                        "clear",
                        "sort",
                        "reverse",
                        "__setitem__",
                        "__delitem__",
                    ]
                    if node.func.attr in mutation_methods:
                        raise ReadOnlyValidationError(
                            f"Cannot call '{node.func.attr}' on 'tasks' - read-only operation required"
                        )

        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ReadOnlyValidationError("Import statements are not allowed")

        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            raise ReadOnlyValidationError("Function/class definitions are not allowed")

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                forbidden = ["exec", "eval", "__import__", "compile", "open"]
                if node.func.id in forbidden:
                    raise ReadOnlyValidationError(
                        f"Function '{node.func.id}' is not allowed"
                    )

        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                forbidden_modules = ["os", "sys", "subprocess", "importlib"]
                if node.value.id in forbidden_modules:
                    raise ReadOnlyValidationError(
                        f"Access to '{node.value.id}' module is not allowed"
                    )


def safe_evaluate(code: str, tasks: List[Dict]) -> Any:
    validate_read_only(code)

    safe_builtins = {
        "max": max,
        "min": min,
        "len": len,
        "filter": filter,
        "map": map,
        "sorted": sorted,
        "sum": sum,
        "any": any,
        "all": all,
        "next": next,
        "enumerate": enumerate,
        "zip": zip,
        "range": range,
        "abs": abs,
        "round": round,
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict,
        "tuple": tuple,
        "set": set,
    }

    safe_globals = {
        "tasks": tasks,
        "__builtins__": safe_builtins,
    }

    try:
        result = eval(code, safe_globals, {})
        return result
    except Exception as e:
        raise RuntimeError(f"Error evaluating code: {e}")
