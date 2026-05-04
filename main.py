"""
Smart Document Analysis Multi-Agent System
智能文档分析多Agent协作系统
"""

import os
import json
import time
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.summary_agent import SummaryAgent
from agents.report_agent import ReportAgent
from memory.conversation_memory import ConversationMemory
from utils.logger import AgentLogger

def run_multi_agent_pipeline(document_text: str, topic: str = "general"):
    """
    Main orchestrator that coordinates multiple agents to process a document.
    主协调器：调度多个Agent协作处理文档
    
    Pipeline:
    1. ResearchAgent  → 分析文档背景和上下文
    2. AnalysisAgent  → 深度分析内容，提取结构化数据
    3. SummaryAgent   → 多轮推理生成综合摘要
    4. ReportAgent    → 生成最终专业报告
    """
    logger = AgentLogger("Orchestrator")
    memory = ConversationMemory()
    
    logger.log("🚀 启动多Agent协作系统...")
    logger.log(f"📄 文档主题: {topic}")
    logger.log("=" * 60)
    
    results = {}
    
    # ── Agent 1: Research Agent ──────────────────────────────────
    logger.log("\n[Agent 1/4] ResearchAgent 启动 → 分析背景上下文...")
    research_agent = ResearchAgent(memory)
    research_result = research_agent.run(document_text, topic)
    results["research"] = research_result
    memory.add("research_context", research_result)
    logger.log("✅ ResearchAgent 完成")
    time.sleep(1)
    
    # ── Agent 2: Analysis Agent ──────────────────────────────────
    logger.log("\n[Agent 2/4] AnalysisAgent 启动 → 深度内容分析...")
    analysis_agent = AnalysisAgent(memory)
    analysis_result = analysis_agent.run(document_text, research_result)
    results["analysis"] = analysis_result
    memory.add("analysis_data", analysis_result)
    logger.log("✅ AnalysisAgent 完成")
    time.sleep(1)
    
    # ── Agent 3: Summary Agent (Multi-turn reasoning) ─────────────
    logger.log("\n[Agent 3/4] SummaryAgent 启动 → 多轮推理生成摘要...")
    summary_agent = SummaryAgent(memory)
    summary_result = summary_agent.run(document_text, research_result, analysis_result)
    results["summary"] = summary_result
    memory.add("summary", summary_result)
    logger.log("✅ SummaryAgent 完成")
    time.sleep(1)
    
    # ── Agent 4: Report Agent ─────────────────────────────────────
    logger.log("\n[Agent 4/4] ReportAgent 启动 → 生成最终专业报告...")
    report_agent = ReportAgent(memory)
    final_report = report_agent.run(results, topic)
    logger.log("✅ ReportAgent 完成")
    
    # ── Save results ──────────────────────────────────────────────
    output_path = f"output/report_{int(time.time())}.json"
    os.makedirs("output", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "topic": topic,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "pipeline_results": results,
            "final_report": final_report,
            "memory_log": memory.get_all()
        }, f, ensure_ascii=False, indent=2)
    
    logger.log(f"\n📁 结果已保存至: {output_path}")
    logger.log("\n" + "=" * 60)
    logger.log("🎉 多Agent协作流程完成！")
    logger.log("=" * 60)
    
    print("\n\n📋 最终报告：")
    print("-" * 60)
    print(final_report)
    print("-" * 60)
    
    return final_report, output_path


if __name__ == "__main__":
    sample_document = """
    2024年全球人工智能市场分析报告
    
    一、市场概况
    2024年全球AI市场规模达到5000亿美元，同比增长38%。
    大语言模型（LLM）成为增长最快的细分领域，占AI市场的35%。
    中国AI市场规模约为1200亿美元，全球占比24%，位居第二。
    
    二、主要趋势
    1. 企业级AI应用快速落地：超过60%的Fortune 500企业已部署AI解决方案
    2. 多模态模型崛起：图文音视频一体化处理成为新标准
    3. Agent自动化：AI Agent市场规模同比增长210%，是增速最快的赛道
    4. 开源模型影响力提升：开源LLM性能已接近闭源顶级模型
    
    三、投资数据
    - 全球AI领域风险投资总额：980亿美元
    - 大模型公司融资占比：45%
    - 基础设施（算力）投资：320亿美元
    - AI应用层投资：440亿美元
    
    四、挑战与风险
    1. 算力供给紧张，高端GPU短缺问题持续
    2. 数据隐私法规趋严，合规成本上升
    3. AI幻觉问题影响企业落地信心
    4. 人才短缺，AI工程师薪资持续攀升
    
    五、未来展望
    预计2025年全球AI市场将突破8000亿美元。
    Agent、具身智能、AI+科学计算将成为三大核心增长引擎。
    """
    
    run_multi_agent_pipeline(sample_document, topic="AI市场分析")
