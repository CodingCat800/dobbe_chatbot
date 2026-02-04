import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage,SystemMessage
from dotenv import load_dotenv
from tools import book_appointment,show_doctor_availability
from memory import get_session, update_session

_=load_dotenv()

llm = ChatGroq(
     model="llama-3.1-8b-instant",
     temperature=0,
     api_key=os.getenv("CHATGROQ_API_KEY")
)

SYSTEM_INSTRUCTION = SystemMessage(
    content=(
        """INSTRUCTIONS ALWAYS FOLLOW:
            1)Always check if necessasry arguments are present otherwise prompt the user for the data required
            example 1:   
            tool =book_appointment
            data given=patient_name,doctor_name, time
            data absent=time,mail id
            response: please enter appointment time and mail id
            
            example 2:
            tool =show_doctor_availability
            data given=doctor_name
            data absent=date
            response: please enter the date you want to check appointment for <doctor_name>
            
            """
    )
)

TOOLS = [
    book_appointment,
    show_doctor_availability
]

llm_with_tools = llm.bind_tools(TOOLS)

async def run_agent(session_id: str, user_message: str):
    history = get_session(session_id)
    if not history:
        history.append(SYSTEM_INSTRUCTION)

    # User message to sesson history
    history.append(HumanMessage(content=user_message))

    # First LLM call with sesson history
    response = llm_with_tools.invoke(history)
    #print("here")
    #If tool is requested
    if response.tool_calls:
        print(response.tool_calls)
        tool_call = response.tool_calls[0]

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        tool_map = {
            "book_appointment": book_appointment,
            "show_doctor_availability": show_doctor_availability
        }

        tool_result = tool_map[tool_name].invoke(tool_args)

        tool_message = ToolMessage(
            content=tool_result,
            tool_call_id=tool_call["id"]
        )
        print(tool_result)

        history.append(response)
        history.append(tool_message)
        update_session(session_id, history)
        
        if tool_name in {
            "show_doctor_availability","book_appointment"
        }:
            return tool_result

        final_response = llm_with_tools.invoke(history)
        history.append(final_response)

        update_session(session_id, history)
        return final_response.content

    #No tool needed
    history.append(response)
    update_session(session_id, history)
    return response.content