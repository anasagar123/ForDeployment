import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun
from langchain.agents import initialize_agent,AgentType
from langchain.callbacks import StreamlitCallbackHandler
import os
from dotenv import load_dotenv

## Arxiv Tools
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=200) #  ArxivAPIWrapper - it will use for search and fetch from the research paper
arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper) # # when we run ArxivQueryRun, it will interect with outside of the world for research paper
## Wikipedia Tools
api_wrapper = WikipediaAPIWrapper(top_k_resultd=1,doc_content_chars_max=200) # # WikipediaAPIWrapper - This wrapper will use the wikipedia API to conduct searches and fetch page summaries.it will return top-k results.
wiki = WikipediaQueryRun(api_wrapper=api_wrapper) # WikipediaQueryRun will interect for new content
## Search from the interet
search = DuckDuckGoSearchRun(name="Search")


                          ############ Streamlit
st.title("🔎 LangChain - Chat with search")

# StreamlitCallbackHandler - To display the thoughts and actions of an agent in an interective  Streamlit app.
"""
In this example, we're using `StreamlitCallbackHandler` to display the thoughts and actions of an agent in an interactive Streamlit app.
Try more LangChain 🤝 Streamlit Agent examples at [github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent).
"""

## Sidebar for settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter Your Groq API Key:",type="password")


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role":"assisstant","content":"Hi, I'm a chatbot who can search the web. How can i help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

if prompt:=st.chat_input(placeholder="what is machinelearning?"):
    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)

    llm = ChatGroq(groq_api_key=api_key,model_name="Llama3-8b-8192",streaming=True)
    tools = [search,arxiv,wiki]

    # Convert entire tools into a agent 
    search_agent = initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_errors=True)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages,callbacks=[st_cb])
        st.session_state.messages.append({'role':'assistant',"content":response})
        st.write(response)






