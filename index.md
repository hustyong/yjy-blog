---
layout: home

hero:
  name: Claude Code
  text: 核心机制剖析
  tagline: 一套聚焦系统机制的解读——讲清各子系统"怎么运作、为何这样设计"，配 Mermaid 图，源码为准。
  actions:
    - theme: brand
      text: 开始阅读 →
      link: /guide/00-overview
    - theme: alt
      text: 核心中的核心：工具·调用·权限
      link: /guide/01-tool-call-authority

features:
  - title: 00 · 全景与主循环
    details: 五层架构 + 主循环状态机（Continue/Terminal）+ 全栈流式；一切的地基。
    link: /guide/00-overview
  - title: 01 · 工具·调用·权限系统
    details: 支持哪些工具、如何被调用回传、权限如何逐层校验、并发调度、ToolSearch、结果落盘。
    link: /guide/01-tool-call-authority
  - title: 02 · Agent 系统
    details: 子 Agent = 隔离上下文的主循环；普通/Fork/团队三路编排、后台任务、通信与记忆。
    link: /guide/02-agent
  - title: 03 · Skill 系统
    details: Skill = 提示流程；内联 vs 分叉执行；四源统一；延迟加载与发现。
    link: /guide/03-skill
  - title: 04 · 会话管理与压缩
    details: Transcript 持久化 + 三级压缩（Micro/Auto/Snip）+ 保留段重链保缓存 + SessionMemory。
    link: /guide/04-session-compaction
  - title: 05 · MCP 协议与认证
    details: 多传输层、工具/资源发现转换、OAuth/XAA 认证、通道权限、Elicitation。
    link: /guide/05-mcp
  - title: 06 · Plugin 系统
    details: 插件 = 贡献点批发包；发现/安装/开关；各贡献如何接线进主系统。
    link: /guide/06-plugin
  - title: 07 · Hooks 扩展系统
    details: 20+ 生命周期事件；命令/函数型执行；钩子如何改变流程（权限/输入/继续/注入）。
    link: /guide/07-hooks
  - title: 08 · 上下文装配与 system-reminder
    details: 每轮上下文是"装配"出来的；附件机制、全量/稀疏节流、状态持续重注。
    link: /guide/08-context-assembly
  - title: 09 · 启动与性能
    details: 并行预取、编译期死代码消除、懒加载、prompt 缓存共享、性能探针。
    link: /guide/09-bootstrap-performance
  - title: 10 · 权限规则系统
    details: 规则来源/优先级/解析/匹配、影子规则、"下次不再问"写回、路径边界、拒绝升级。
    link: /guide/10-permission-rules
  - title: 11 · Bash / 命令安全、沙箱与分类器
    details: AST 拆分、硬编码护栏、危险规则剥离、只读校验、沙箱、LLM 分类器内幕（附辟谣）。
    link: /guide/11-bash-security
---

## 阅读顺序

建议先读 **00 打地基**，再读 **01 工具·调用·权限**（最核心），随后按兴趣展开：

```mermaid
flowchart TB
    O["00 全景与主循环<br/>（地基：调模型→执行工具→喂回）"] --> TC["01 工具·调用·权限系统<br/>（核心中的核心）"]
    O --> CTX["08 上下文装配<br/>（每轮上下文如何拼出来）"]
    TC --> AG["02 Agent 系统"]
    TC --> SK["03 Skill 系统"]
    TC --> HK["07 Hooks 扩展系统"]
    TC --> PR["10 权限规则系统"]
    TC --> BS["11 Bash/命令安全与沙箱分类器"]
    PR --> BS
    AG --> SK
    O --> CP["04 会话管理与压缩"]
    TC --> MCP["05 MCP 协议与认证"]
    AG --> PL["06 Plugin 系统"]
    SK --> PL
    MCP --> PL
    HK --> PL
    O --> PF["09 启动与性能"]
```

## 贯穿全书的几条主线

留意这些**反复出现的设计母题**，它们把各篇串成一个整体：

- **工具结果即下一轮输入**：Agent 自主性的来源（00、01）。
- **保 prompt 缓存 = 前缀字节稳定**：工具结果预算冻结、压缩保留段重链、记忆稳定 header、会话内锁定易变因素——都服务于此（01/04/08/09）。
- **失败关闭**：证明不了安全就更保守（工具并发默认串行、Bash"超限即问"、权限多口硬 deny）。
- **状态被"持续重注"而非只存一次**：待办/任务等状态每轮以最新快照经 `<system-reminder>` 注入（08、01 §3.1）。
- **贡献点统一汇流**：内置/MCP/Skill/Plugin/Hooks 最终都并入同一批"工具池 / 命令池 / 钩子表 / Agent 表"（03/05/06/07）。
- **一套内核多处复用**：主循环 `query()` 同时服务 SDK、REPL、子 Agent、压缩、摘要（00、02、04）。
- **磁盘上的三套记录，各司其职**（都在 `~/.claude/` 下，别混）：
  - **会话 transcript**（`projects/<项目>/<sessionId>.jsonl`）——整段对话消息链，供 `--resume`（04）。
  - **工具结果落盘**（会话目录下 `tool-results/`）——单个超大工具结果全文，上下文只留预览（01）。
  - **文件历史备份**（`file-history/<sessionId>/`）——每次编辑前的文件副本，供 `rewind` 回退（04 §1.2）。

---

> **第一原则：源码为准。** 所有机制结论均从 `claude-code-cli` 源码求证；无法确证者显式标注「推断」。每篇文末附**涉及模块**便于回源码深挖。
