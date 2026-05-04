"""
Research Agent - 负责分析文档背景和上下文
"""

import anthropic
import os
from memory.conversation_memory import ConversationMemory
from utils.logger import AgentLogger


class ResearchAgent:
    """
    Research Agent: 分析文档背景、识别主题领域、提取关键实体
    """
    
    def __init__(self, memory: ConversationMemory):
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.memory = memory
        self.logger = AgentLogger("ResearchAgent")
        self.conversation_history = []
    
    def run(self, document_text: str, topic: str) -> str:
        """
        Multi-turn reasoning: 通过多轮对话深入理解文档背景
        """
        self.logger.log("开始多轮推理分析文档背景...")
        
        # Round 1: 识别文档类型和领域
        self.conversation_history.append({
            "role": "user",
            "content": f"""你是一个专业的文档研究Agent。请分析以下文档，识别：
1. 文档类型（报告/论文/新闻/其他）
2. 主要领域和子领域
3. 时间范围
4. 关键实体（公司/人物/地区等）

文档内容：
{document_text}

请用JSON格式回复。"""
        })
        
        response1 = self._call_claude()
        self.conversation_history.append({
            "role": "assistant",
            "content": response1
        })
        self.logger.log("  轮次1完成：文档类型识别")
        
        # Round 2: 深入分析背景
        self.conversation_history.append({
            "role": "user",
            "content": f"""基于你的分析，现在请进一步：
1. 评估文档的可信度和数据来源质量
2. 识别文档中可能存在的偏见或局限性
3. 补充该领域的背景知识（主题：{topic}）
4. 列出需要重点关注的数据点

请详细分析。"""
        })
        
        response2 = self._call_claude()
        self.conversation_history.append({
            "role": "assistant",
            "content": response2
        })
        self.logger.log("  轮次2完成：背景深度分析")
        
        # Round 3: 综合输出
        self.conversation_history.append({
            "role": "user",
            "content": "请综合以上两轮分析，输出一份简洁的「文档背景研究报告」，包含：文档概述、领域背景、关键实体、数据可信度评估。"
        })
        
        final_response = self._call_claude()
        self.logger.log("  轮次3完成：综合输出")
        
        return final_response
    
    def _call_claude(self) -> str:
        message = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1500,
            system="你是一个专业的文档研究Agent，擅长分析文档背景、识别关键信息和评估数据质量。请用中文回复。",
            messages=self.conversation_history
        )
        return message.content[0].text
