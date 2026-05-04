# 🤖 Smart-Doc-Agent：智能文档分析多Agent协作系统

基于 Claude API 构建的多Agent协作框架，通过4个专业Agent的流水线协作，对文档进行深度分析并自动生成专业报告。

---

## 🧠 系统架构

```
用户输入文档
      ↓
┌─────────────────────────────────────────┐
│           Orchestrator（主协调器）         │
│                                         │
│  ┌─────────────┐   ┌─────────────────┐  │
│  │ ResearchAgent│→  │  AnalysisAgent  │  │
│  │  背景研究    │   │   深度分析      │  │
│  │  3轮推理    │   │   3轮推理       │  │
│  └─────────────┘   └────────┬────────┘  │
│                             ↓           │
│  ┌─────────────┐   ┌─────────────────┐  │
│  │  ReportAgent│←  │  SummaryAgent   │  │
│  │  报告生成   │   │  摘要生成       │  │
│  │  整合输出   │   │  4轮推理        │  │
│  └─────────────┘   └─────────────────┘  │
│                                         │
│         ConversationMemory（共享记忆）    │
└─────────────────────────────────────────┘
      ↓
 最终专业报告（JSON + 控制台输出）
```

---

## ✨ 核心特性

### 🔄 多Agent协作
- **4个专业Agent** 各司其职，流水线处理
- **共享记忆系统** 实现Agent间信息传递
- **Orchestrator** 统一调度，管理整体流程

### 🧩 长链推理
- ResearchAgent：**3轮**多轮对话推理
- AnalysisAgent：**3轮**深度分析推理
- SummaryAgent：**4轮**草稿→批判→优化→精炼
- 总计 **10+ 轮**推理链

### 💾 持久化存储
- 每次运行结果自动保存为 JSON
- 包含完整的Agent执行历史和记忆日志

### 🎨 可视化日志
- 每个Agent独立颜色标识
- 实时显示处理进度

---

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/M123-b/smart-doc-agent.git
cd smart-doc-agent
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 设置 API Key（Windows）
```bash
set ANTHROPIC_API_KEY=your_api_key_here
```

### 4. 运行
```bash
python main.py
```

---

## 📁 项目结构

```
smart-doc-agent/
├── main.py                    # 主入口 & Orchestrator
├── agents/
│   ├── research_agent.py      # 背景研究Agent（3轮推理）
│   ├── analysis_agent.py      # 深度分析Agent（3轮推理）
│   ├── summary_agent.py       # 摘要生成Agent（4轮推理）
│   └── report_agent.py        # 报告生成Agent（整合输出）
├── memory/
│   └── conversation_memory.py # 跨Agent共享记忆系统
├── utils/
│   └── logger.py              # 彩色日志系统
├── output/                    # 自动生成的报告（运行后出现）
├── requirements.txt
└── README.md
```

---

## 📊 处理流程详解

| Agent | 职责 | 推理轮次 | 输入 | 输出 |
|-------|------|---------|------|------|
| ResearchAgent | 背景研究、实体识别 | 3轮 | 原始文档 | 背景报告 |
| AnalysisAgent | 数据提取、趋势分析 | 3轮 | 文档+背景报告 | 深度分析 |
| SummaryAgent | 执行摘要生成 | 4轮 | 文档+前两者输出 | 执行摘要 |
| ReportAgent | 最终报告整合 | 1轮 | 所有Agent输出 | 专业报告 |

---

## 🛠 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.8+ | 主语言 |
| Anthropic Claude API | 核心AI推理 |
| claude-opus-4-5 | 推理模型 |
| JSON | 结果持久化 |

---

## 📋 输出示例

运行后将在控制台看到：
```
[10:23:01] [Orchestrator] 🚀 启动多Agent协作系统...
[10:23:01] [Orchestrator] 📄 文档主题: AI市场分析
[10:23:02] [ResearchAgent] 开始多轮推理分析文档背景...
[10:23:05] [ResearchAgent]   轮次1完成：文档类型识别
...
[10:23:45] [ReportAgent] 整合所有Agent结果，生成最终报告...
[10:23:50] [Orchestrator] 📁 结果已保存至: output/report_xxx.json
[10:23:50] [Orchestrator] 🎉 多Agent协作流程完成！
```

---

## 📄 License

MIT License

---

> Built with ❤️ using [Claude API](https://www.anthropic.com) | Multi-Agent Architecture by M123-b
