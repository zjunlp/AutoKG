from colorama import Fore
import os
import openai
from camel.agents import RolePlaying
from camel.utils import print_text_animated

openai.api_key="your api key"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
def main() -> None:
    task_prompt = "Construct and complete the Knowledge Graph of the following passage. " \
                  "Titanic, a film set in 1912 when the Titanic liner sank after hitting an iceberg on its maiden voyage, " \
                  "tells the touching story of two people from different walks of life, Jack, a poor painter, and Ruth, an aristocratic woman, who abandoned their worldly prejudices and fell in love, " \
                  "and eventually Jack gave up his chance of survival to Ruth."
    role_play_session = RolePlaying(
        "Consultant",
        "Knowledge Graph Domain Expert",
        task_prompt=task_prompt,
        with_task_specify=True,
    )

    print(
        Fore.GREEN +
        f"AI Assistant sys message:\n{role_play_session.assistant_sys_msg}\n")
    print(Fore.BLUE +
          f"AI User sys message:\n{role_play_session.user_sys_msg}\n")

    print(Fore.YELLOW + f"Original task prompt:\n{task_prompt}\n")
    print(
        Fore.CYAN +
        f"Specified task prompt:\n{role_play_session.specified_task_prompt}\n")
    print(Fore.RED + f"Final task prompt:\n{role_play_session.task_prompt}\n")

    chat_turn_limit, n = 20, 0
    assistant_msg, _ = role_play_session.init_chat()
    while n < chat_turn_limit:
        n += 1
        assistant_return, user_return = role_play_session.step(assistant_msg)
        assistant_msg, assistant_terminated, assistant_info = assistant_return
        user_msg, user_terminated, user_info = user_return

        if assistant_terminated:
            print(Fore.GREEN +
                  ("AI Assistant terminated. "
                   f"Reason: {assistant_info['termination_reasons']}."))
            break
        if user_terminated:
            print(Fore.GREEN +
                  ("AI User terminated. "
                   f"Reason: {user_info['termination_reasons']}."))
            break

        print_text_animated(Fore.BLUE + f"AI User:\n\n{user_msg.content}\n")
        print_text_animated(Fore.GREEN +
                            f"AI Assistant:\n\n{assistant_msg.content}\n")

        if "CAMEL_TASK_DONE" in user_msg.content:
            break


if __name__ == "__main__":
    main()
