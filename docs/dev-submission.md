---
title: "Sendero: helping Noris prepare each child's next step with local open AI"
published: false
tags: devchallenge, weekendchallenge, hf26challenge
ai_disclosure_level: some_ai
---

*This is a submission for the [Hacktoberfest Weekend Challenge: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01).*

## What I Built

Noris teaches catechesis. She needs a record of each child's journey: when they arrive, the formation they receive, which requirements they have met, and when they move to a new stage.

I built **Sendero**, a local companion that turns that record into preparation for the next meeting. Its Spanish interface brings together periods, groups, participant profiles, multiple responsible adults, attendance, observations, stage requirements and a chronological history.

The open AI feature is at the start of the child's page: **Preparar acompañamiento**. An open-weight model selects and prioritizes two or three reviewed preparation actions and a question for the child's responsible adult, using the current requirement states and attendance counts. The proposal is saved with its model and evidence snapshot. If the record changes, Sendero marks it outdated.

Noris can create a dated period and its groups, enroll a participant with multiple responsible adults, record attendance and class topics under that enrollment, and consult the complete history. Existing profiles survive the schema upgrade; new enrollments do not duplicate the participant. She can mark a current AI proposal as reviewed, which records the review without changing requirements or stages.

The goal is modest: help Noris arrive at the next meeting knowing what to review, while keeping the decision about a child's progress in her hands.

I have tested the working prototype with fictional records. Reviewing the actual stage names and requirements with Noris is still the next acceptance step; I do not yet have feedback from her to report.

## Demo

[Watch the 33-second demonstration](https://github.com/yosef7/sendero-catequesis/blob/main/demo/sendero-demo.mp4).

The recording shows the complete new workflow: login with a fictional demo code, period and group creation, a participant with two responsible adults, attendance and a class topic, an observation, a real local model proposal, human review, and persistence after reload. All displayed records are fictional. The application is in Spanish; the video has no narration.

![Sendero periods and groups](https://raw.githubusercontent.com/yosef7/sendero-catequesis/main/demo/grupos.png)

![Sendero's local AI preparation proposal, with attendance and requirement counts](https://raw.githubusercontent.com/yosef7/sendero-catequesis/main/demo/ai-plan.png)

## Code

[Source code, setup instructions and MIT license](https://github.com/yosef7/sendero-catequesis).

The model has its own license: the [Qwen2.5-Coder-3B-Instruct model card](https://huggingface.co/Qwen/Qwen2.5-Coder-3B-Instruct) identifies it as `qwen-research`. The application's MIT license does not change those model terms.

## How I Built It

The application uses Python, Flask, SQLite, plain JavaScript and Ollama. I chose the available local `qwen2.5-coder:3b` model for the prototype and kept the adapter configurable through `OLLAMA_MODEL`.

The modules separate the interface, HTTP API, formation rules, persistence and local inference. SQLite foreign keys and transactions keep the records consistent; stage advancement also checks the expected current stage to reject a repeated transition. Versioned migrations add saved AI proposals, periods, groups, enrollments, responsible adults and human review without replacing existing child records. An invalid initial enrollment rolls back the entire new profile. Attendance must belong to the participant and fall within the enrollment period.

The model receives a small context: numbered requirements and their completion states, recorded-class and attendance counts, the current stage identifier and whether another stage exists. Names, contacts, class topics and free-text observations stay out of the model request.

My first free-text generation was structurally valid but suggested details not supported by the record. I changed the design: the JSON Schema supplies an allowed catalog of actions and questions, and the server validates membership and rejects duplicate actions before saving. The model can choose and prioritize within that catalog; it cannot introduce a new requirement through its response.

That is a deliberate limit on generative freedom. Sendero never treats AI output as proof that a requirement is complete, and the model has no tools to write to the formation record.

The expanded workflow passes **26 automated tests**. The final Chromium run completed login, period and group creation, enrollment with two responsible adults, attendance and topic entry, local inference, review, reload and a mobile contact edit with zero JavaScript errors. Four views at both 390 and 320 pixels had no horizontal overflow. Those are emulated mobile checks, not a test on a physical phone.

The final real Ollama request returned a valid proposal in **3.34 seconds**. An earlier run of this expansion took 20.37 seconds. These observations describe this machine and those requests, not a performance guarantee. The [browser validation](https://github.com/yosef7/sendero-catequesis/blob/main/demo/validacion-v1.json) records the final checks. The previous [three-case evaluation](https://github.com/yosef7/sendero-catequesis/blob/main/demo/evaluacion-ia.json) remains available as evidence from the earlier prototype.

The implementation follows [Ollama’s structured-output contract](https://docs.ollama.com/capabilities/structured-outputs). The earlier structural-validation approach was informed by [DevShakib's article on structured output](https://dev.to/devshakib/structured-output-from-llms-a-retry-repair-loop-your-parser-never-sees-through-3b0b) and [Mukunda Katta's explanation of rule-based output validation](https://dev.to/mukundakatta/rule-based-llm-output-validation-reject-bad-responses-before-they-reach-your-users-if0). A valid response is still a proposal for Noris to review, not a guarantee that its priorities are useful.

## Why Does Open Innovation Matter?

This project concerns children, so local operation is a practical design choice. Once the dependencies and model are downloaded, recording and inference can run without an external inference service or a paid API key. The AI request carries only numerical progress information and remains on the same machine.

Open local inference also let me inspect the request, change the response contract after an unsatisfactory result, and repeat the experiment. I can try a different local model through the same adapter, respecting its license, without rewriting the registration and formation modules. I have not fine-tuned the model or claimed that this is impossible with every closed API.

The current version is for one catechist on one trusted computer. It includes local access protection, a downloadable SQLite backup and printable records. Multiuser deployment, retention and consent procedures, and testing on a physical phone and acceptance testing with Noris remain future work. The demonstration uses fictional data throughout.

**AI assistance disclosure:** I used Codex to help implement, test and document Sendero, and to draft this article from the stated need and recorded validation results.
