import dotenv
from gentopia import chat
from gentopia.assembler.agent_assembler import AgentAssembler

dotenv.load_dotenv(".env")  # load environmental keys
agent = AgentAssembler(file='intercom/agent.yaml').get_agent()

chat(agent)
