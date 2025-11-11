from app.graph_builder import build_graph

def main():
    print("\n Smart Info Agent (Azure OpenAI + Tools)\n")
    graph = build_graph()
    state = {"query": ""}
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye")
            break
        state["query"] = user_input
        result = graph.invoke(state)
        print(f"Agent: {result['response']}\n")

if __name__ == "__main__":
    main()
