import argparse
import os
import time

import openai

from tools import CAL, CRP, MML

openai.api_key = os.getenv("OPENAI_API_KEY")
MAX_CALL_TOOLS = 10


def gpt3_tools(args, fewshot):
    prompt = fewshot + "\n\nQ: " + args.question + "\n"
    answer = ""

    for _ in range(MAX_CALL_TOOLS):
        # wait for 1 second to avoid the api call limit
        time.sleep(1)
        # get response from GPT-3
        response_gpt = gpt_api(model=args.model, prompt=prompt)
        # update prompt and answer
        prompt += response_gpt
        answer += response_gpt

        if "<<" not in response_gpt:
            break

        # get toolname
        i = 0
        while response_gpt[-i] != "<":
            i += 1
        toolname = response_gpt[-i + 2 : -1]

        # get tool response
        if toolname == "Calculator" and args.CAL:
            try:
                response_CAL = CAL(response_gpt[: -i - 2])
                prompt += ">> " + response_CAL + "\n"
                answer += ">> " + response_CAL + "\n"
            except:  # noqa: E722
                print("Error is raised in Calculator")
                prompt += ">>"
                answer += ">>"

        elif toolname == "Chemical reaction predictor" and args.CRP:
            try:
                response_CRP = CRP(response_gpt[: -i - 2])
                prompt += ">>" + "\n" + response_CRP + "\n"
                answer += ">>" + "\n" + response_CRP + "\n"
            except:  # noqa: E722
                print("Error is raised in Chemical reaction predictor")
                prompt += ">>"
                answer += ">>"

        elif toolname == "Molar mass list" and args.MML:
            try:
                response_MML = MML(response_gpt[: -i - 2])
                prompt += ">> " + response_MML + "\n"
                answer += ">> " + response_MML + "\n"
            except:  # noqa: E722
                print("Error is raised in Molar mass list")
                prompt += ">>"
                answer += ">>"
        else:
            prompt += ">>"
            answer += ">>"

    return answer


def gpt_api(model, prompt):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=500,
        temperature=0,
        stop=[">>"],
    )
    return response["choices"][0]["text"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", help="question to ask")
    parser.add_argument("--CAL", default=True, help="whether to use Calculator")
    parser.add_argument(
        "--CRP", default=True, help="whether to use Chemical Reaction Predictor"
    )
    parser.add_argument(
        "--MML", default=True, help="whether to use Molecular Mass List"
    )
    parser.add_argument("--fewshotnum", help="number of fewshot examples")
    parser.add_argument("--model", default="text-davinci-003", help="model name")
    parser.add_argument("--output", help="output file")
    args = parser.parse_args()

    with open("prompt/fewshot_" + str(args.fewshotnum) + ".txt", "r") as f:
        fewshot = f.read()

    output = gpt3_tools(args, fewshot)

    with open(args.output, "w") as f:
        f.write(output)

    print("Output saved to", args.output)
    print("finished!")


if __name__ == "__main__":
    main()
