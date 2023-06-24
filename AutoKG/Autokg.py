import os
from colorama import Fore
from LC_CAMEL  import starting_convo,get_sys_msgs,CAMELAgent
from RE_CAMEL import Retrieval_Msg
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


os.environ["OPENAI_API_KEY"] = "Your_api_key"
word_limit = 50  # word limit for task brainstorming


def main() ->None:
    assistant_role_name = "Consultant"
    user_role_name = "Knowledge Graph Domain Expert"

    task = "Construct a Knowledge Graph about the movie \"Spider-Man: Across the Spider-Verse\"."

    specified_task, assistant_inception_prompt, user_inception_prompt = starting_convo(assistant_role_name, user_role_name, task, word_limit)
    assistant_sys_msg, user_sys_msg = get_sys_msgs(assistant_role_name, user_role_name, specified_task, assistant_inception_prompt, user_inception_prompt)
    assistant_agent = CAMELAgent(assistant_sys_msg, ChatOpenAI(temperature=0.2))
    user_agent = CAMELAgent(user_sys_msg, ChatOpenAI(temperature=0.2))

    # Reset agents
    assistant_agent.reset()
    user_agent.reset()

    # Initialize chats
    assistant_msg = HumanMessage(
        content=(f"{user_sys_msg.content}. "
                 "Now start to give me introductions one by one. "
                 "Only reply with Instruction and Input."))

    user_msg = HumanMessage(content=f"{assistant_sys_msg.content}")
    user_msg = assistant_agent.step(user_msg)

    print(Fore.RED+f"Original task prompt:\n{task}\n")
    print(Fore.GREEN+f"Specified task prompt:\n{specified_task}\n")

    chat_turn_limit, n = 30, 0
    while n < chat_turn_limit:
        n += 1
        user_ai_msg = user_agent.step(assistant_msg)
        user_msg = HumanMessage(content=user_ai_msg.content)
        print(Fore.BLUE+f"AI User ({user_role_name}):\n\n{user_msg.content}\n\n")

        Supplement_info = Retrieval_Msg(assistant_role_name, user_role_name, user_msg.content, 20)
        if Supplement_info != "" or "Agent Stoped" not in Supplement_info:
            Supplement_info_new = user_msg.content + "\n Additional information for the Instruction: " + Supplement_info
            Supplement_info_new = HumanMessage(content=Supplement_info_new)
            assistant_ai_msg = assistant_agent.step(Supplement_info_new)
            assistant_msg = HumanMessage(content=assistant_ai_msg.content)
            print(Fore.YELLOW + f"AI Assistant With Tool ({assistant_role_name}):\n\n{assistant_msg.content}\n\n")

        else:
            assistant_ai_msg = assistant_agent.step(user_msg)
            assistant_msg = HumanMessage(content=assistant_ai_msg.content)
            print(Fore.CYAN+f"AI Assistant ({assistant_role_name}):\n\n{assistant_msg.content}\n\n")

        if "CAMEL_TASK_DONE" in user_msg.content:
            break

if __name__ == "__main__":
    main()
