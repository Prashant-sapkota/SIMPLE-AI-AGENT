from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv


load_dotenv()

@tool
def calculator(a:float, b:float) -> str:
    """useful for performing basic arthematic operations like addition, subtraction, multiplication, and division."""
    print("Tool has been called.")
    return f"the sum of {a} and {b} is {a + b}, the difference when {b} is subtracted from {a} is {a - b}, the product of {a} and {b} is {a * b}, and the quotient when {a} is divided by {b} is {a / b if b != 0 else 'undefined (cannot divide by zero)'}."

def main():
    model = ChatOpenAI(temperature=0)

    tools = [calculator]
    agent_executor = create_react_agent(model, tools)

    print("Agent is ready to answer your questions!")
    print("WELCOME! I AM YOUR AI ASSISTANT. HOW CAN I HELP YOU TODAY? TYPE 'quit' to EXIT.")
    print("you can ask me to perform calculation or chat with me.")


    while True:
        user_input = input("\nyou: ").strip()

        if user_input.lower() == "quit":
            print("Exiting the program. Goodbye!")
            break

        print("\nAssistant: ", end="",)
        for chunk in agent_executor.stream(
            {"messages":[HumanMessage(content=user_input)]}
        ):
            
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk ["agent"]["messages"]:
                    print(message.content, end="")
        
        print()  

if __name__ == "__main__":
    main()