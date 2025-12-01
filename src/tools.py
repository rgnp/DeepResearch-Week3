import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

def web_search(query):
    """
    【工具】联网搜索工具
    输入：搜索关键词 (query)
    输出：搜索到的顶层内容摘要
    """
    print(f"[Tool] 正在搜索：{query} ...")

    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    # search_depth="advanced" 表示深度搜索
    response = tavily.search(query=query, search_depth="advanced", max_results=5)

    # 提取我们需要的内容
    context = []
    for result in response['results']:
        context.append(f"标题: {result['title']}\n链接: {result['url']}\n摘要: {result['content']}\n")

    return "\n---\n".join(context)

def calculate(expression):
    """
    【工具】数学计算器
    输入：数学表达式字符串 (例如 "2 + 2")
    输出：计算结果
    """
    try:
        # eval 是危险函数，生产环境慎用，但做 Demo 没问题
        return str(eval(expression))
    except Exception as e:
        return f"计算错误：{e}"


# --- 单元测试 ---
if __name__ == "__main__":
    # 写完代码立刻测一下，这是好习惯
    # print(web_search("DeepSeek V3 最新评测"))
     print(calculate("2 + 2"))