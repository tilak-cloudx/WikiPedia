import streamlit as st
import wikipedia

st.title("📚 Wikipedia Chatbot")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_wikipedia_summary(query):
    try:
        # Search for pages matching the query
        results = wikipedia.search(query)
        if not results:
            return "Sorry, I couldn't find anything on that topic."

        # Get summary of the top result (limit to 2 sentences)
        summary = wikipedia.summary(results[0], sentences=2, auto_suggest=False, redirect=True)
        return summary
    except wikipedia.DisambiguationError as e:
        return f"Your query is ambiguous, did you mean: {', '.join(e.options[:5])}?"
    except wikipedia.PageError:
        return "Sorry, I couldn't find a page matching your query."
    except Exception as e:
        return "Oops, something went wrong."

# User input
user_input = st.text_input("Ask me anything:")

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get Wikipedia response
    bot_response = get_wikipedia_summary(user_input)
    st.session_state.messages.append({"role": "bot", "content": bot_response})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")
