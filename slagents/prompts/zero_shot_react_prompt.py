from gentopia.prompt import PromptTemplate

ZendeskTicketZeroShotReactPrompt = PromptTemplate(
    input_variables=["instruction", "agent_scratchpad", "tool_names", "tool_description"],
    template=
"""Answer the following questions as best you can. You have access to the following tools:
{tool_description}.
Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do

Action: the action to take, should be one of [{tool_names}]

If No Action: you can skip the action and go to the next question or final answer

Action Input: the input to the action

Observation: the result of the action

Final Answer: the final answer to the original input question , provide detailed explanation of all checks, do not skip important data things that look good and things that look bad so you can provide complete daignosis and solution to the user.

Begin! After each Action Input.

Question: {instruction}
Thought:{agent_scratchpad}
    """
)