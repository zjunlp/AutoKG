from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.agents import AgentType
from LC_CAMEL import CAMELAgent
from colorama import Fore
from langchain.chat_models import ChatOpenAI
import os
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    SystemMessage,
)

os.environ["SERPAPI_API_KEY"] = "your_serpapi_api_key"

def Retrieval_Msg(assistant_role_name, user_role_name, task, word_limit):
    retrieval_sys_msg = SystemMessage(content="You are an assistant who can use Google search to gather information")

    retrieval_specifier_prompt = (
        """Here is a task that {assistant_role_name} will help {user_role_name} to complete a Knowledge Graph Construction task based on the  {user_role_name}'s instruction and input: {task}.
        Suppose you are the {assistant_role_name}.
        You must know that you are able to perform web searches.
        You are never supposed to search for information about methodology questions.
        You must only search factual knowledge on the Internet.
        
        Please summarize the key information of the task and answer only in this form:

        Browsing Question: <YOUR_QUESTION>
        
        <YOUR_QUESTION> should be your browsing question suitable for Google search.
        If you think browsing is not necessary, then the answer should be \"none\".
        Be creative and imaginative. Please reply in {word_limit} words or less. Do not add anything else."""
    )

    retrieval_specifier_template = HumanMessagePromptTemplate.from_template(template=retrieval_specifier_prompt)
    retrieval_specify_agent = CAMELAgent(retrieval_sys_msg, ChatOpenAI(temperature=1.0))
    retrieval_specifier_msg = retrieval_specifier_template.format_messages(assistant_role_name=assistant_role_name,
                                                                 user_role_name=user_role_name,
                                                                 task=task, word_limit=word_limit)[0]
    specified_retrieval_msg = retrieval_specify_agent.step(retrieval_specifier_msg)
    print(Fore.GREEN+f"Specified retrieval:\n{specified_retrieval_msg.content}")
    specified_retrieval = specified_retrieval_msg.content
    response = ""

    if "Browsing Question:" in specified_retrieval:
        if "Browsing Question: none" in specified_retrieval:
            return  response
        else:
            specified_retrieval = specified_retrieval.replace("Browsing Question:","")
            # 加载 OpenAI 模型
            llm = OpenAI(temperature=0,max_tokens=2048)
             # 加载 serpapi 工具
            tools = load_tools(["serpapi"])
            # 工具加载后都需要初始化，verbose 参数为 True，会打印全部的执行详情
            agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
            # 运行 agent
            response = agent.run(specified_retrieval)

    return response