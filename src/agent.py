import os
from dotenv import load_dotenv
# 引入 LangChain 的核心组件
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
# from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from tools import web_search, calculate  # 导入你刚才写的搜索工具

load_dotenv()

# --- 1. 定义工具 ---
# 使用 @tool 装饰器，LangChain 会自动读取函数的 docstring (注释)
# 告诉 LLM 这个工具是干嘛的。这非常关键！
@tool
def search_tool(query: str):
    """
    当需要获取实时信息、新闻、具体数据或你不知道的知识时，使用此工具。
    输入应该是具体的搜索关键词。
    """
    return web_search(query)

@tool
def calculate_tool(expression: str):
    """
    当用户询问数学计算、加减乘除问题时，使用此工具。
    输入应该是一个可执行的数学表达式，如 '200 * 5'。
    """
    return calculate(expression)

# --- 2. 初始化大脑 (LLM) ---
# 我们使用 DeepSeek，它完美兼容 OpenAI 的 Function Calling 格式
llm = ChatOpenAI(
    model="deepseek-chat", 
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    temperature=0.3  # 稍微有一点创造力，但不要太发散
)

# --- 3. 组装 Agent ---
def get_agent():
    # A. 准备工具箱
    tools = [search_tool, calculate_tool]
    
    # B. 设计 Prompt (人设)
    # {agent_scratchpad} 是 LangChain 预留的位置，用来存放 "思考-行动-观察" 的中间过程
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的深度研究员。你的目标是利用搜索工具，为用户提供详尽、有数据支持的报告。请不要瞎编，每一句话都要基于搜索结果。"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    # C. 创建 Agent (大脑 + 工具定义 + Prompt)
    # create_tool_calling_agent 是目前最先进的 Agent 模式
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # D. 创建执行器 (Executor)
    # Executor 负责真正的 "循环"：调用 LLM -> 解析结果 -> 执行 Python 函数 -> 把结果喂回给 LLM
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True  # 🔥 开启 verbose，你能在终端看到它思考的全过程！
    )
    
    return agent_executor

# --- 单元测试 ---
if __name__ == "__main__":
    agent = get_agent()
    print("🤖 Agent 正在启动...")
    
    # 测试一个需要联网的问题
    result = agent.invoke({"input": "DeepSeek V3 相比 V2 有哪些具体的性能提升？请列出数据。"})
    
    print("\n========== 最终回答 ==========")
    print(result['output'])