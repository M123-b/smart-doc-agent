"""
Summary Agent - 多轮推理生成综合摘要
"""

import anthropic
import os
from memory.conversation_memory import ConversationMemory
from utils.logger import AgentLogger


class SummaryAgent:
    """
    Summary Agent: 整合前两个Agent的输出，通过多轮推理生成综合摘要
    这是系统中推理链最长的Agent
    """
    
    def __init__(self, memory: ConversationMemory):
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.memory = memory
        self.logger = AgentLogger("SummaryAgent")
        self.conversation_history = []
    
    def run(self, document_text: str, research_result: str, analysis_result: str) -> str:
        """
        4轮推理：草稿 → 批判 → 优化 → 最终输出
        """
        self.logger.log("开始4轮推理摘要生成...")
        
        system_prompt = """你是一个专业的摘要生成Agent，擅长整合多源信息生成高质量摘要。
你有两个前置Agent的分析结果可以参考。请用中文回复。"""
        
        context = f"""
【背景研究报告】
{research_result}

【深度分析报告】
{analysis_result}

【原始文档】
{document_text}
"""
        
        # Round 1: 生成初稿摘要
        self.conversation_history.append({
            "role": "user",
            "content": f"""基于以下资料，生成一份初稿摘要（约300字）：

{context}

摘要应包含：核心主题、关键数据、主要结论。"""
        })
        
        draft = self._call_claude(system_prompt)
        self.conversation_history.append({"role": "assistant", "content": draft})
        self.logger.log("  轮次1完成：生成初稿")
        
        # Round 2: 自我批判
        self.conversation_history.append({
            "role": "user",
            "content": """请对你刚才生成的摘要进行严格批判：
1. 有哪些重要信息被遗漏？
2. 哪些表述不够准确或清晰？
3. 逻辑结构是否合理？
4. 数据引用是否正确？

请列出至少5个需要改进的地方。"""
        })
        
        critique = self._call_claude(system_prompt)
        self.conversation_history.append({"role": "assistant", "content": critique})
        self.logger.log("  轮次2完成：自我批判")
        
        # Round 3: 优化改进
        self.conversation_history.append({
            "role": "user",
            "content": """基于你的批判意见，现在生成改进版摘要。
要求：
- 解决所有提出的问题
- 保持简洁（300-400字）
- 确保数据准确
- 逻辑清晰，层次分明"""
        })
        
        improved = self._call_claude(system_prompt)
        self.conversation_history.append({"role": "assistant", "content": improved})
        self.logger.log("  轮次3完成：优化改进")
        
        # Round 4: 最终精炼
        self.conversation_history.append({
            "role": "user",
            "content": """最后，请生成最终版「执行摘要」：
- 面向高层决策者
- 突出最重要的3-5个要点
- 每个要点配1-2句关键数据支撑
- 结尾给出1-2条行动建议

这是最终输出，请确保质量最高。"""
        })
        
        final = self._call_claude(system_prompt)
        self.logger.log("  轮次4完成：最终精炼")
        
        return final
    
    def _call_claude(self, system_prompt: str) -> str:
        message = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1500,
            system=system_prompt,
            messages=self.conversation_history
        )
        return message.content[0].text
