"""
Report Agent - 整合所有Agent输出，生成最终专业报告
"""

import anthropic
import os
from memory.conversation_memory import ConversationMemory
from utils.logger import AgentLogger


class ReportAgent:
    """
    Report Agent: 整合所有Agent的输出，生成结构完整的专业报告
    """
    
    def __init__(self, memory: ConversationMemory):
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.memory = memory
        self.logger = AgentLogger("ReportAgent")
    
    def run(self, pipeline_results: dict, topic: str) -> str:
        """
        整合所有Agent结果，输出最终报告
        """
        self.logger.log("整合所有Agent结果，生成最终报告...")
        
        prompt = f"""你是一个专业报告撰写Agent。请基于以下多个专业Agent的分析结果，
生成一份完整的专业分析报告。

【主题】：{topic}

【背景研究结果】：
{pipeline_results.get('research', '')}

【深度分析结果】：
{pipeline_results.get('analysis', '')}

【执行摘要】：
{pipeline_results.get('summary', '')}

请生成一份结构完整的专业报告，包含：

# {topic} 智能分析报告

## 一、执行摘要
（从SummaryAgent提取精华）

## 二、文档背景与概述
（基于ResearchAgent的研究）

## 三、核心数据分析
（基于AnalysisAgent的数据提取）

## 四、趋势与洞察
（综合多Agent分析的关键发现）

## 五、风险与挑战
（识别的主要问题和不确定性）

## 六、结论与建议
（具体可执行的建议）

---
*本报告由 Smart-Doc-Agent 多Agent协作系统生成*
*处理流程：ResearchAgent → AnalysisAgent → SummaryAgent → ReportAgent*

请确保报告专业、完整、有深度。用中文撰写。"""
        
        message = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
