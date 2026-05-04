"""
Conversation Memory - 跨Agent共享记忆系统
"""

from typing import Any, Dict, List
import time


class ConversationMemory:
    """
    跨Agent共享记忆系统
    - 存储每个Agent的输出
    - 支持Agent间信息共享
    - 记录完整的处理历史
    """
    
    def __init__(self):
        self._memory: Dict[str, Any] = {}
        self._history: List[Dict] = []
    
    def add(self, key: str, value: Any) -> None:
        """存储Agent输出"""
        self._memory[key] = value
        self._history.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "key": key,
            "value_length": len(str(value))
        })
    
    def get(self, key: str) -> Any:
        """获取指定记忆"""
        return self._memory.get(key, None)
    
    def get_all(self) -> Dict:
        """获取所有记忆"""
        return {
            "memory_keys": list(self._memory.keys()),
            "history": self._history
        }
    
    def has(self, key: str) -> bool:
        """检查记忆是否存在"""
        return key in self._memory
    
    def clear(self) -> None:
        """清空记忆"""
        self._memory.clear()
        self._history.clear()
