from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

print("--- Privacy Shield Test Initiated ---")
class PrivacyShield:
    def __init__(self):
        configuration = {
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": "en", "model_name": "en_core_web_md"}],
        }

        provider = NlpEngineProvider(nlp_configuration=configuration)
        nlp_engine = provider.create_engine()

        self.analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["en"])
        self.anonymizer = AnonymizerEngine()

    def identify_and_mask(self, text:str):
        results = self.analyzer.analyze(
            text=text, 
            entities=["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "LOCATION", "URL"],
            language='en'
        )

        operators = {
            "PERSON": OperatorConfig("replace", {"new_value": "<NAME_REDACTED>"}),
            "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "<EMAIL_REDACTED>"}),
            "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "<PHONE_REDACTED>"}),
        }
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results,
            operators=operators
        )

        return anonymized_result.text 

if __name__ == "__main__":
    shield = PrivacyShield()
    sample_query = "Does student John Doe (UIN 661234567) need to sign the FERPA waiver?"
    print(f"Original: {sample_query}")
    print(f"Masked:   {shield.identify_and_mask(sample_query)}")
