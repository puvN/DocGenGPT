CONSTANTS = {
    "INITIAL_PROMPT": {
        "en": ("I want you to be my system analyst for software product. I will ask you questions "
               "about the contents of source files and I want you to give me the idea how they work and what they "
               "do. All the files belong to one project. Do not use any assumptions, "
               "use strict definitions. After all questions, I will ask one general question about the project "
               "summary. In the answer to that question, I want the summary info about the project "
               "based on your previous answers about the files."),
        "ru": ("Я хочу, чтобы ты был моим системным аналитиком для программного продукта. "
               "Я буду задавать тебе вопросы о содержимом исходных файлов, и я хочу, чтобы ты дал мне представление "
               "о том, как они работают и что они делают. Все файлы принадлежат одному проекту. Не используй "
               "никаких предположений, используй строгие определения. После всех вопросов я задам один общий вопрос "
               "о сводке проекта. В ответе на этот вопрос я хочу получить общую информацию о проекте "
               "на основе твоих предыдущих ответов о файлах.")
    },
    "FILE_QUESTION": {
        "en": "What does this script do? What is the purpose of it? Here is the text:\n\n",
        "ru": "Что делает этот код? Какова его цель? Вот текст:\n\n"
    },
    "GENERAL_QUESTION": {
        "en": "Give me the summary of the project based on your previous answers.",
        "ru": "Дай мне сводку по проекту на основе твоих предыдущих ответов."
    }
}
