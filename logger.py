"""
Agent Logger - 统一日志系统
"""

import time


class AgentLogger:
    """统一的Agent日志输出"""
    
    COLORS = {
        "Orchestrator": "\033[95m",   # 紫色
        "ResearchAgent": "\033[94m",  # 蓝色
        "AnalysisAgent": "\033[92m",  # 绿色
        "SummaryAgent": "\033[93m",   # 黄色
        "ReportAgent": "\033[96m",    # 青色
    }
    RESET = "\033[0m"
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.color = self.COLORS.get(agent_name, "\033[97m")
    
    def log(self, message: str) -> None:
        timestamp = time.strftime("%H:%M:%S")
        print(f"{self.color}[{timestamp}] [{self.agent_name}]{self.RESET} {message}")
