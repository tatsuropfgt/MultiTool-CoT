import argparse
import os
import textwrap
import time

import openai

from tools import cal, crp, mml

openai.organization = os.getenv("OPENAI_ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT_TEMPLATE = textwrap.dedent(
    """\
    {few_shot}

    Q: {question}
    """
)
TOOL_START_SEQUENCE = "<<"
TOOL_END_SEQUENCE = ">>"
MAX_CALL_TOOLS = 10


def make_api_call(model, prompt):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=500,
        temperature=0,
        stop=[TOOL_END_SEQUENCE],
    )
    return response["choices"][0]["text"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", help="Question to ask")
    parser.add_argument("--cal", default=True, help="Whether to use Calculator")
    parser.add_argument(
        "--crp", default=True, help="Whether to use Chemical Reaction Predictor"
    )
    parser.add_argument(
        "--mml", default=True, help="Whether to use Molecular Mass List"
    )
    parser.add_argument("--few_shot", help="Text file listing few-shot examples")
    parser.add_argument("--model", default="text-davinci-003", help="Model name")
    parser.add_argument("--output", help="Output file")
    args = parser.parse_args()

    question = args.question

    with open(args.few_shot) as f:
        few_shot = f.read()

    prompt = PROMPT_TEMPLATE.format(few_shot=few_shot, question=question)

    answer = ""
    for _ in range(MAX_CALL_TOOLS):
        # Wait for 1 second to avoid the api call limit
        time.sleep(1)
        # Get response from GPT-3
        response_gpt = make_api_call(model=args.model, prompt=prompt)
        # Update prompt and answer
        prompt += response_gpt
        answer += response_gpt

        if TOOL_START_SEQUENCE not in response_gpt:
            break

        # Get tool name
        i = 0
        while response_gpt[-i] != "<":
            i += 1
        tool_name = response_gpt[-i + 2 : -1]

        # Get tool response
        if tool_name == "Calculator" and args.cal:
            try:
                response_cal = cal(response_gpt[: -i - 2])
                prompt += TOOL_END_SEQUENCE + " " + response_cal + "\n"
                answer += TOOL_END_SEQUENCE + " " + response_cal + "\n"
            except Exception as e:
                print("Error is raised in Calculator:", e)
                prompt += TOOL_END_SEQUENCE
                answer += TOOL_END_SEQUENCE

        elif tool_name == "Chemical reaction predictor" and args.crp:
            try:
                response_crp = crp(response_gpt[: -i - 2])
                prompt += TOOL_END_SEQUENCE + "\n" + response_crp + "\n"
                answer += TOOL_END_SEQUENCE + "\n" + response_crp + "\n"
            except Exception as e:
                print("Error is raised in Chemical reaction predictor:", e)
                prompt += TOOL_END_SEQUENCE
                answer += TOOL_END_SEQUENCE

        elif tool_name == "Molar mass list" and args.mml:
            try:
                response_mml = mml(response_gpt[: -i - 2])
                prompt += TOOL_END_SEQUENCE + " " + response_mml + "\n"
                answer += TOOL_END_SEQUENCE + " " + response_mml + "\n"
            except Exception as e:
                print("Error is raised in Molar mass list:", e)
                prompt += TOOL_END_SEQUENCE
                answer += TOOL_END_SEQUENCE
        else:
            prompt += TOOL_END_SEQUENCE
            answer += TOOL_END_SEQUENCE

    with open(args.output, "w") as f:
        f.write(answer)

    print("Output saved to", args.output)

    print("Finished!")


if __name__ == "__main__":
    main()
