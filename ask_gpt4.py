# default args for update_from_scrapbox() as sample
import openai
from make_index import VectorStore, get_size, embed, clean
import pyperclip

INDEX_FILE = "qualia-san.pickle"

# Your reply should be shorter than 250 characters.
PROMPT = """
You are virtual character. Read sample output of the character in the following sample section. Then reply to the input.

## Sample
{text}

## Input
{input}
""".strip()


MAX_PROMPT_SIZE = 4096
RETURN_SIZE = 1000


def ask(input_str):
    input_str = clean(input_str)

    PROMPT_SIZE = get_size(PROMPT)
    rest = MAX_PROMPT_SIZE - RETURN_SIZE - PROMPT_SIZE
    input_size = get_size(input_str)
    print("input size:", input_size)
    if rest < input_size:
        raise RuntimeError("too large input!")
    rest -= input_size

    vs = VectorStore(INDEX_FILE)
    samples = vs.get_sorted(input_str)

    to_use = []
    used_title = []
    for _sim, body, title in samples:
        if title in used_title:
            continue
        size = get_size(body)
        if rest < size:
            break
        to_use.append(body)
        used_title.append(title)
        print("\nUSE:", title, body)
        rest -= size

    text = "\n\n".join(to_use)
    prompt = PROMPT.format(input=input_str, text=text)

    print("\nPROMPT:")
    print(prompt)
    pyperclip.copy(prompt)

    # print("\nTHINKING...")
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "user", "content": prompt}
    #     ],
    #     max_tokens=RETURN_SIZE,
    #     temperature=0.0,
    # )

    # print("\nRESPONSE:")
    # print(response)

    # # show question and answer
    # content = response['choices'][0]['message']['content']
    # print("\nANSWER:")
    # print(f">>>> {input_str}")
    # print(">", content)

    # # show reference
    # print("\nREFERENCE:", *[f"[{s}]" for s in used_title])


def main():
    pass


def test():
    ask("もっとも大事な問いとは何だろう？")


if __name__ == "__main__":
    main()
