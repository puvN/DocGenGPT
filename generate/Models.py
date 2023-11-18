class DocPackageModel:
    def __init__(self, repo_name, doc_models: (), final_response):
        self._repo_name = repo_name
        self._doc_models = doc_models
        self._final_response = final_response

    def to_dict(self):
        if not self._final_response:
            print(f"Warning, no final response for repo name {self._repo_name}")
            return {}
        return {
            'repo_name': self._repo_name,
            'doc_models': [doc_model.to_dict() for doc_model in self._doc_models],
            'final_response': self._final_response
        }


class DocModel:
    def __init__(self, link, script_text, doc_text):
        self._link = link
        self._script_text = script_text
        self._doc_text = doc_text

    def to_dict(self):
        return {
            'link': self._link,
            'script_text': self._script_text,
            'doc_text': self._doc_text,
        }
