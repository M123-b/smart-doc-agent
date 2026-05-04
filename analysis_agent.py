"""
Analysis Agent - 负责深度内容分析，提取结构化数据
"""

import anthropic
import os
import json
from memory.conversation_memory import ConversationMemory
from utils.logger import AgentLogger


class AnalysisAgent:
    """
    Analysis Agent: 深度分析文档内容，提取数据、趋势、关键论点
    """
    
    def __init__(self, memory: ConversationMemory):
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.memory = memory
        self.logger = AgentLogger("AnalysisAgent")
        self.conversation_history = []
    
    def run(self, document_text: str, research_context: str) -> str:
        """
        基于ResearchAgent的背景研究，进行深度内容分析
        """
        self.logger.log("开始深度内容分析...")
        
        # 初始化对话，带入研究背景
        system_prompt = f"""你是一个专业的数据分析Agent。
你已经获得了文档的背景研究报告：
{research_context}

基于这个背景，你需要对文档进行深度分析。请用中文回复。"""
        
        # Round 1: 提取关键数据和统计信息
        self.conversation_history.append({
            "role": "user",
            "content": f"""请从以下文档中提取所有关键数据点和统计信息：

文档内容：
{document_text}

要求：
- 列出所有数字、百分比、金额
- 标注数据的时间维度
- 识别数据间的关联关系
- 用结构化格式呈现"""
        })
        
        response1 = self._call_claude(system_prompt)
        self.conversation_history.append({"role": "assistant", "content": response1})
        self.logger.log("  轮次1完成：数据提取")
        
        # Round 2: 趋势和模式分析
        self.conversation_history.append({
            "role": "user",
            "content": """基于提取的数据，请分析：
1. 主要趋势（上升/下降/稳定）
2. 异常数据点或值得关注的变化
3. 不同数据间的相关性
4. 潜在的因果关系推断

请进行深度逻辑推理。"""
        })
        
        response2 = self._call_claude(system_prompt)
        self.conversation_history.append({"role": "assistant", "content": response2})
        self.logger.log("  轮次2完成：趋势分析")
        
        # Round 3: 论点和结论分析
        self.conversation_history.append({
            "role": "user",
            "content": """最后，请分析文档的核心论点：
1. 文档的主要论述是什么？
2. 论据是否充分支撑论点？
3. 有哪些潜在的反驳观点？
4. 文档结论的可靠性评估

输出「深度分析报告」，整合以上三轮分析结果。"""
        })
        
        final_response = self._call_claude(system_prompt)
        self.logger.log("  轮次3完成：综合分析报告")
        
        return final_response
    
    def _call_claude(self, system_prompt: str) -> str:
        message = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=2000,
            system=system_prompt,
            messages=self.conversation_history
        )
        return message.content[0].text
