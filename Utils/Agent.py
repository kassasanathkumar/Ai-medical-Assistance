import os
from dotenv import load_dotenv
load_dotenv() 
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

class Agent:
    def __init__(self, medical_report=None, role=None, extra_info=None):
        self.medical_report = medical_report
        self.role = role
        self.extra_info = extra_info
        self.prompt_template = self.create_prompt_template()

        self.model = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-70b-8192",
            temperature=0.0
        )

    def create_prompt_template(self):
        if self.role == "MultidisciplinaryTeam":
            template = """You are a multidisciplinary medical team (Cardiologist, Psychologist, Pulmonologist).
You will be given reports from all three specialists. Based on them, return:

1. A brief list of 3 likely **disease predictions**
2. 3 tailored **diet recommendations**
3. 3 key **precautionary measures** to follow

Make the output clear and medically relevant.

Cardiologist Report:
{cardiologist_report}

Psychologist Report:
{psychologist_report}

Pulmonologist Report:
{pulmonologist_report}"""
            return PromptTemplate.from_template(template)
        else:
            template = f"""You are a medical specialist - {self.role}.
You will be given a patient's medical report. Your job is to return:

1. Possible **disease prediction(s)**
2. Personalized **diet recommendations**
3. Appropriate **precautionary measures**

Report:
{{medical_report}}"""
            return PromptTemplate.from_template(template)

    def run(self):
        print(f"{self.role} is running.....")
        try:
            if self.role == "MultidisciplinaryTeam":
                prompt = self.prompt_template.format(
                    cardiologist_report=self.extra_info.get("cardiologist_report", ""),
                    psychologist_report=self.extra_info.get("psychologist_report", ""),
                    pulmonologist_report=self.extra_info.get("pulmonologist_report", "")
                )
            else:
                prompt = self.prompt_template.format(medical_report=self.medical_report)

            response = self.model.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            print(f"Error Occurred in {self.role} agent: {e}")
            return None


class Cardiologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Cardiologist")


class Psychologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Psychologist")


class Pulmonologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Pulmonologist")


class MultidisciplinaryTeam(Agent):
    def __init__(self, cardiologist_report, psychologist_report, pulmonologist_report):
        extra_info = {
            "cardiologist_report": cardiologist_report,
            "psychologist_report": psychologist_report,
            "pulmonologist_report": pulmonologist_report
        }
        super().__init__(role="MultidisciplinaryTeam", extra_info=extra_info)
class Dietician(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Dietician")


class PreventiveSpecialist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "PreventiveSpecialist")

