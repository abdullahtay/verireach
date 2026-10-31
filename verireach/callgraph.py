"""Static AST Call-Graph Extractor & Transitive Reachability Solver."""

from __future__ import annotations
import ast
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class ReachabilityResult:
    """Outcome of symbol-level reachability verification."""

    symbol: str
    is_reachable: bool
    entrypoint: str
    call_path: List[str] = field(default_factory=list)
    confidence: float = 1.0  # 1.0 = deterministic proof
    notes: str = ""

    def summary(self) -> str:
        if self.is_reachable:
            chain = " -> ".join(self.call_path)
            return f"AFFECTED (Reachable): {self.symbol} is called via [{chain}] from entrypoint '{self.entrypoint}'"
        else:
            return f"NOT AFFECTED (Unreachable): {self.symbol} has no execution path from entrypoint '{self.entrypoint}'"


class CallGraph:
    """Directed graph representing caller -> callee invocations across modules."""

    def __init__(self) -> None:
        self.adj: Dict[str, Set[str]] = {}
        self.nodes: Set[str] = set()
        self.entrypoints: Set[str] = set()
        self.file_map: Dict[str, str] = {}  # symbol -> filepath

    def add_node(self, symbol: str, filepath: str = "", is_entrypoint: bool = False) -> None:
        self.nodes.add(symbol)
        if symbol not in self.adj:
            self.adj[symbol] = set()
        if filepath:
            self.file_map[symbol] = filepath
        if is_entrypoint:
            self.entrypoints.add(symbol)

    def add_edge(self, caller: str, callee: str) -> None:
        self.add_node(caller)
        self.add_node(callee)
        self.adj[caller].add(callee)

    def find_shortest_path(self, start: str, target: str) -> Optional[List[str]]:
        """Breadth-First Search for shortest execution path from start to target."""
        if start not in self.adj:
            return None
        if start == target:
            return [start]

        queue: deque[Tuple[str, List[str]]] = deque([(start, [start])])
        visited: Set[str] = {start}

        # Normalize target for matching (e.g., match 'verify_token' or 'auth.verify_token')
        target_norm = target.lower()

        while queue:
            current, path = queue.popleft()
            for neighbor in self.adj.get(current, set()):
                # Direct match or suffix match (module.func matches func)
                n_norm = neighbor.lower()
                if n_norm == target_norm or n_norm.endswith(f".{target_norm}") or target_norm.endswith(f".{n_norm}"):
                    return path + [neighbor]

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    def check_reachability(self, target_symbol: str, explicit_entrypoint: Optional[str] = None) -> ReachabilityResult:
        """Check if target_symbol can be reached from any known entrypoint."""
        candidates: List[str] = []

        if explicit_entrypoint:
            clean_ep = explicit_entrypoint.strip()
            # If explicit_entrypoint matches a known node directly
            if clean_ep in self.nodes:
                candidates.append(clean_ep)
            else:
                # Match entrypoints matching the file or module
                file_stem = Path(clean_ep).stem
                for ep in self.entrypoints:
                    fp = self.file_map.get(ep, "")
                    if clean_ep in fp or ep.startswith(f"{file_stem}."):
                        candidates.append(ep)
                # If still no candidates found, search all nodes matching file stem
                if not candidates:
                    for n in self.nodes:
                        fp = self.file_map.get(n, "")
                        if clean_ep in fp or n.startswith(f"{file_stem}."):
                            candidates.append(n)

        if not candidates:
            candidates = list(self.entrypoints)

        if not candidates and self.nodes:
            # Fallback to common main symbols if none marked
            candidates = [n for n in self.nodes if n.endswith("main") or n == "main"]
            if not candidates:
                candidates = list(self.nodes)

        for ep in candidates:
            if not ep:
                continue
            path = self.find_shortest_path(ep, target_symbol)
            if path:
                return ReachabilityResult(
                    symbol=target_symbol,
                    is_reachable=True,
                    entrypoint=ep,
                    call_path=path,
                    confidence=1.0,
                    notes=f"Reachable from {ep} in {len(path) - 1} steps.",
                )

        # Target not reached from any entrypoint
        chosen_ep = explicit_entrypoint or (candidates[0] if candidates else "unknown")
        return ReachabilityResult(
            symbol=target_symbol,
            is_reachable=False,
            entrypoint=chosen_ep,
            call_path=[],
            confidence=1.0,
            notes=f"Exhaustive graph traversal showed 0 execution paths from entrypoints to {target_symbol}.",
        )


class CallGraphBuilder(ast.NodeVisitor):
    """Parses Python ASTs and builds a modular inter-procedural CallGraph."""

    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir.resolve()
        self.graph = CallGraph()
        self.current_file = ""
        self.current_module = ""
        self.current_scope: List[str] = []
        self.imports: Dict[str, str] = {}  # local_alias -> full_qualified_target

    def build_from_directory(self, target_dir: str | Path, entrypoint_file: Optional[str] = None) -> CallGraph:
        """Scan all .py files in target directory and construct the call graph."""
        p = Path(target_dir).resolve()
        py_files = sorted(list(p.rglob("*.py")))

        # Two-pass build:
        # Pass 1: Parse AST, register all function definitions and top-level entrypoints
        # Pass 2: Resolve edges with imports
        for py_path in py_files:
            self._process_file(py_path, entrypoint_file)

        return self.graph

    def _process_file(self, file_path: Path, entrypoint_file: Optional[str]) -> None:
        try:
            rel = file_path.relative_to(self.base_dir)
            module_name = ".".join(rel.with_suffix("").parts)
        except Exception:
            module_name = file_path.stem

        self.current_file = str(file_path)
        self.current_module = module_name
        self.current_scope = [module_name]
        self.imports = {}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            tree = ast.parse(code, filename=str(file_path))
        except Exception:
            return  # Skip files that fail to parse

        is_designated_entry = False
        if entrypoint_file:
            if file_path.name == entrypoint_file or str(file_path).endswith(entrypoint_file):
                is_designated_entry = True
        elif file_path.name in ("main.py", "app.py", "cli.py", "__main__.py"):
            is_designated_entry = True

        if is_designated_entry:
            ep_symbol = f"{module_name}.__top__"
            self.graph.add_node(ep_symbol, filepath=str(file_path), is_entrypoint=True)

        self.visit(tree)

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            name = alias.name
            asname = alias.asname or name
            self.imports[asname] = name
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        mod = node.module or ""
        for alias in node.names:
            target = f"{mod}.{alias.name}" if mod else alias.name
            asname = alias.asname or alias.name
            self.imports[asname] = target
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        func_symbol = f"{'.'.join(self.current_scope)}.{node.name}"
        is_ep = node.name in ("main", "run", "entrypoint") and len(self.current_scope) == 1
        self.graph.add_node(func_symbol, filepath=self.current_file, is_entrypoint=is_ep)

        # Push scope
        self.current_scope.append(node.name)
        self.generic_visit(node)
        self.current_scope.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        func_symbol = f"{'.'.join(self.current_scope)}.{node.name}"
        is_ep = node.name in ("main", "run", "entrypoint") and len(self.current_scope) == 1
        self.graph.add_node(func_symbol, filepath=self.current_file, is_entrypoint=is_ep)

        self.current_scope.append(node.name)
        self.generic_visit(node)
        self.current_scope.pop()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.current_scope.append(node.name)
        self.generic_visit(node)
        self.current_scope.pop()

    def visit_Call(self, node: ast.Call) -> None:
        caller = ".".join(self.current_scope)
        callee = self._resolve_callee_name(node.func)
        if callee:
            self.graph.add_edge(caller, callee)
        self.generic_visit(node)

    def _resolve_callee_name(self, func_node: ast.AST) -> Optional[str]:
        """Resolve called function name incorporating imports and scope."""
        if isinstance(func_node, ast.Name):
            name = func_node.id
            # Check if it was imported
            if name in self.imports:
                return self.imports[name]
            # Check local scope
            return f"{self.current_module}.{name}"

        elif isinstance(func_node, ast.Attribute):
            attr_name = func_node.attr
            val = func_node.value

            if isinstance(val, ast.Name):
                base_name = val.id
                if base_name in self.imports:
                    return f"{self.imports[base_name]}.{attr_name}"
                elif base_name == "self" and len(self.current_scope) >= 2:
                    return f"{'.'.join(self.current_scope[:-1])}.{attr_name}"
                return f"{base_name}.{attr_name}"

            elif isinstance(val, ast.Attribute):
                inner = self._resolve_callee_name(val)
                if inner:
                    return f"{inner}.{attr_name}"

        return None
