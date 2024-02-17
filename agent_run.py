import dotenv
from gentopia import chat
from gentopia.assembler.agent_assembler import AgentAssembler

dotenv.load_dotenv(".env")  # load environmental keys
agent = AgentAssembler(file='slagents/controllers/controller_reAct.yaml').get_agent()

chat(agent)
# print(agent.run("not getting intercom call user 236154022679109146 and company 82488426438216692 and ticket id 46561"))
