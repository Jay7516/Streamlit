from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message)
