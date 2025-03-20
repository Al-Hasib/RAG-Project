from src.chat import rag_chain

while True:
    user_input = input("Enter your question: ")
    result = rag_chain.invoke(user_input)
    print(result)
    if user_input == "exit":
        break